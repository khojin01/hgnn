#!/usr/bin/env python3
"""디스코드 — 실험 알림(서버가 먼저 말한다)과 조회(내가 묻는다).

    python3 tools/discord_bot.py notify      # 상태 변화가 있으면 웹훅으로 알린다. refresh_all.sh 가 매분 부른다
    python3 tools/discord_bot.py send "글"   # 한 줄 보내기
    python3 tools/discord_bot.py ask 상태    # 봇 없이 답만 확인
    ~/.venvs/discord/bin/python tools/discord_bot.py bot         # 명령을 받는 게이트웨이 루프 (상주)
    python3 tools/discord_bot.py ensure-bot  # 루프가 죽어 있으면 되살린다. refresh_all.sh 가 매분 부른다

설정은 `.discord.json` (저장소에 안 들어간다):

    {
      "webhook": "채널 설정 → 연동 → 웹후크에서 만든 URL",   ← 알림만 하려면 이것만 있으면 된다
      "token":   "개발자 포털에서 만든 봇 토큰",              ← 조회까지 하려면 필요
      "channel": 0                                          ← 비워 두면 봇이 보이는 모든 채널에서 답한다
    }

알림은 파이썬 표준 라이브러리만 쓴다. 조회 루프만 discord.py 가 필요하고,
그건 `~/.venvs/discord` 안에만 설치해서 실험 환경을 건드리지 않는다.

## 무엇을 하지 않는가

명령으로 셸을 돌리지 않는다. 실험을 시작하거나 멈추지 않는다. 파일을 읽어 답만 한다.
설정에 channel 을 적어 두면 그 채널 밖의 말은 무시한다.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONF = ROOT / ".discord.json"
SEEN = ROOT / "dashboard" / ".discord_seen.json"
LIVE = ROOT / "dashboard" / "live.json"
VENV = Path.home() / ".venvs" / "discord" / "bin" / "python"
KST = timezone(timedelta(hours=9))

BLUE, GREEN, AMBER, RED, GREY = 0x3D7FB5, 0x3C7A5C, 0xE0761F, 0xB53B2C, 0x87A2B4


def conf():
    if not CONF.exists():
        return {}
    try:
        return json.loads(CONF.read_text(encoding="utf-8"))
    except Exception:
        return {}


def webhook():
    w = str(conf().get("webhook", "")).replace("discordapp.com", "discord.com")   # 옛 주소도 받는다
    return w if w.startswith("https://discord.com/api/webhooks/") else None


def post(payload):
    url = webhook()
    if not url:
        return False
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20):
            return True
    except Exception as e:
        print("discord 웹훅 실패: %s: %s" % (type(e).__name__, e), file=sys.stderr)
        return False


def send(text):
    return post({"content": text[:1900]})


def embed(title, body, color=BLUE):
    return post({"embeds": [{"title": title[:250], "description": body[:3900], "color": color,
                             "footer": {"text": datetime.now(KST).strftime("%m-%d %H:%M") + " · dms2"}}]})


def live():
    try:
        return json.loads(LIVE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def sh(cmd):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, timeout=20).stdout.decode("utf-8", "replace").strip()
    except Exception:
        return ""


def dur(s):
    s = int(s)
    return "%d분" % (s // 60) if s < 3600 else "%d시간 %d분" % (s // 3600, s % 3600 // 60)


# ── 조회 ──────────────────────────────────────────────────────────────────────

def q_gpu():
    """nvidia-smi 를 그 자리에서 읽는다 — 스냅샷이 아니라 지금 값이다."""
    out = sh("nvidia-smi --query-gpu=index,name,utilization.gpu,memory.used,memory.total --format=csv,noheader,nounits")
    if not out:
        return "nvidia-smi 를 읽지 못했다."
    rows = []
    for row in out.splitlines():
        p = [x.strip() for x in row.split(",")]
        if len(p) >= 5:
            u = int(p[2])
            bar = "█" * round(u / 10) + "·" * (10 - round(u / 10))
            rows.append("GPU%s  %s %3d%%   %.1f/%.0f GB   %s" % (p[0], bar, u, int(p[3]) / 1024, int(p[4]) / 1024, p[1]))
    procs = sh("nvidia-smi --query-compute-apps=pid,used_memory --format=csv,noheader,nounits")
    rows.append("계산 프로세스 %d개" % (len(procs.splitlines()) if procs else 0))
    return "```\n" + "\n".join(rows) + "\n```"


def q_status():
    d = live()
    if not d:
        return "live.json 이 없다. 파이프라인이 아직 안 돌았다."
    jobs = d.get("jobs", [])
    out = ["스냅샷 %s · %s" % (d.get("generated_at", "")[11:16], d.get("host", ""))]
    if jobs:
        out.append("**실행 중 %d개**" % len(jobs))
        for j in jobs:
            out.append("· %s × %s %s — GPU%s · %s 경과" % (j["model"], j["dataset"], j["task"], j["gpu"], dur(j["elapsed"])))
    else:
        out.append("실행 중인 실험 없음")
    for r in [r for r in d.get("runs", []) if r.get("active")]:
        done = sum(1 for s in r.get("terminal", {}).values() if s.startswith("COMPLETE") or "SKIP" in s.upper())
        total = len(r.get("planned") or []) or "?"
        line = "진행 `%s` — %s/%s" % (r["id"], done, total)
        if r.get("active_ds"):
            line += " · 지금 " + r["active_ds"]
        out.append(line)
    for a in d.get("automation", []):
        if not a.get("on"):
            out.append("경고: %s 꺼짐" % a["name"])
    return "\n".join(out)


def q_todo():
    items = [t for t in live().get("lab", {}).get("todo", []) if t.startswith("- [ ]")]
    if not items:
        return "열린 할 일이 없다."
    return "\n".join("· " + re.sub(r"^- \[.\] ", "", t) for t in items)


def q_journal():
    t = live().get("lab", {}).get("latest_journal_text") or ""
    t = re.sub(r"^---.*?---\n", "", t, flags=re.S).strip()
    return t[:1800] if t else "일지가 없다."


def q_runs():
    runs = live().get("runs", [])[:6]
    if not runs:
        return "기록된 실행이 없다."
    out = []
    for r in runs:
        c = {}
        for s in r.get("terminal", {}).values():
            u = s.upper()
            k = "완료" if s.startswith("COMPLETE") or "SKIP" in u else ("OOM/OOT" if ("OOM" in u or "OOT" in u) else "실패")
            c[k] = c.get(k, 0) + 1
        out.append("`%s`%s — %s" % (r["id"], " (활성)" if r.get("active") else "",
                                   " · ".join("%s %d" % kv for kv in c.items()) or "기록 없음"))
    return "\n".join(out)


def q_paper():
    p = live().get("paper", {})
    if not p:
        return "논문 대조 자료가 없다."
    out = []
    for k, label in (("T3", "NC"), ("T4", "HP"), ("T5", "CD")):
        t = p.get(k)
        if t:
            out.append("**%s** 일치 %s/%s · |Δ| 중앙값 %.2f" % (label, t["agree"], t["total"], t["median"]))
    outs = sum(len(p[k]["outliers"]) for k in ("T3", "T4", "T5") if p.get(k))
    out.append("이상치 %d칸 (|Δ| 3.0 초과)" % outs)
    out.append("표 전체는 서버별 대조 아티팩트에서 본다.")
    return "\n".join(out)


HELP = """읽기만 한다. 실험을 시작하거나 멈추지 않는다.

`상태` 지금 무엇이 돌고 있나
`gpu` GPU 사용률 (지금 값)
`실행` 최근 실행 요약
`할일` 열린 할 일
`일지` 최근 일지
`논문` 논문 대조 요약
`도움말` 이 안내

실행이 끝나거나 실패하면 묻지 않아도 알린다."""

ROUTES = [
    (("상태", "status", "지금"), "실행 상태", q_status),
    (("gpu", "지피유", "그래픽"), "GPU", q_gpu),
    (("실행", "runs", "run"), "최근 실행", q_runs),
    (("할일", "할 일", "todo"), "다음 할 일", q_todo),
    (("일지", "log", "journal"), "최근 일지", q_journal),
    (("논문", "paper", "대조"), "논문 대조", q_paper),
    (("도움말", "help", "?"), "실험 관리 봇", lambda: HELP),
]


def answer(text):
    """(제목, 본문) 또는 None — 아는 말이 아니면 조용히 넘긴다."""
    t = text.strip().lstrip("!/").lower()
    for keys, title, fn in ROUTES:
        if any(t == k or t.startswith(k + " ") for k in keys):
            return title, fn()
    return None


# ── 알림 ──────────────────────────────────────────────────────────────────────

def snapshot(d):
    """알림 판정에 쓰는 최소 상태. 여기 담긴 값이 바뀔 때만 알린다."""
    return {
        "jobs": sorted("%s × %s %s" % (j["model"], j["dataset"], j["task"]) for j in d.get("jobs", [])),
        "terminal": {r["id"]: dict(r.get("terminal", {})) for r in d.get("runs", [])},
        "automation": {a["name"]: bool(a.get("on")) for a in d.get("automation", [])},
    }


def notify():
    d = live()
    if not d or not webhook():
        return 0
    cur = snapshot(d)
    try:
        old = json.loads(SEEN.read_text(encoding="utf-8"))
    except Exception:
        SEEN.write_text(json.dumps(cur, ensure_ascii=False), encoding="utf-8")   # 첫 실행은 기준만 잡는다
        return 0

    events = []          # (색, 줄)
    for j in [x for x in cur["jobs"] if x not in old.get("jobs", [])]:
        events.append((BLUE, "시작 — " + j))
    ended = [x for x in old.get("jobs", []) if x not in cur["jobs"]]
    for j in ended:
        events.append((GREY, "프로세스 종료 — " + j))

    for run, term in cur["terminal"].items():
        before = old.get("terminal", {}).get(run, {})
        for ds, state in term.items():
            if before.get(ds) == state:
                continue
            u = state.upper()
            if u.startswith("COMPLETE"):
                events.append((GREEN, "완료 — `%s` · %s" % (run, ds)))
            elif "OOM" in u or "OOT" in u:
                events.append((AMBER, "자원 한계 — `%s` · %s · %s" % (run, ds, state)))
            elif "FAIL" in u:
                events.append((RED, "실패 — `%s` · %s · %s" % (run, ds, state)))

    for name, on in cur["automation"].items():
        if old.get("automation", {}).get(name) and not on:
            events.append((RED, "자동화 '%s' 가 멈췄다" % name))

    if events:
        if ended and not cur["jobs"]:
            events.append((GREY, "남은 실험 없음 — GPU 비었다"))
        worst = min(events, key=lambda e: [RED, AMBER, BLUE, GREEN, GREY].index(e[0]))[0]
        title = {RED: "실패", AMBER: "자원 한계", BLUE: "실험 시작", GREEN: "실험 완료", GREY: "실험 종료"}[worst]
        embed(title, "\n".join(l for _, l in events[:20]), worst)
    SEEN.write_text(json.dumps(cur, ensure_ascii=False), encoding="utf-8")
    return len(events)


# ── 조회 루프 (discord.py 필요) ───────────────────────────────────────────────

def bot():
    try:
        import discord
    except ImportError:
        print("discord.py 가 없다. %s 로 실행해라." % VENV, file=sys.stderr)
        return 1
    c = conf()
    token, channel = c.get("token"), c.get("channel")
    if not token:
        print(".discord.json 에 token 이 없다", file=sys.stderr)
        return 1

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print("봇 접속: %s" % client.user)

    @client.event
    async def on_message(m):
        if m.author.bot:
            return
        if channel and m.channel.id != int(channel):     # 정해진 채널 밖은 무시한다
            return
        a = answer(m.content)
        if not a:
            return
        title, body = a
        await m.channel.send(embed=discord.Embed(title=title, description=body[:3900], color=BLUE))

    client.run(token, log_handler=None)
    return 0


def ensure_bot():
    if not conf().get("token") or not VENV.exists():
        return 0
    if sh("ps -eo args --no-headers | grep 'discord_bot.py bot' | grep -v grep"):
        return 0
    log = ROOT / "dashboard" / "discord.log"
    subprocess.Popen("nohup '%s' '%s' bot >> '%s' 2>&1 &" % (VENV, Path(__file__), log),
                     shell=True, start_new_session=True)
    print("discord bot 시작")
    return 1


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd == "notify":
        n = notify()
        print("알림 %d건" % n if n else "알릴 변화 없음")
    elif cmd == "bot":
        return bot()
    elif cmd == "ensure-bot":
        ensure_bot()
    elif cmd == "send":
        print("보냄" if send(" ".join(sys.argv[2:])) else "보내지 못함")
    elif cmd == "test":
        print("보냄" if embed("연결 확인", "웹훅이 살아 있다. 이제 실험이 끝나거나 실패하면 알린다.", GREEN) else "보내지 못함")
    elif cmd == "ask":
        a = answer(" ".join(sys.argv[2:]))
        print("%s\n%s" % a if a else "모르는 말이다.\n\n" + HELP)
    else:
        print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main())
