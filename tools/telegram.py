#!/usr/bin/env python3
"""텔레그램 — 실험 알림(서버가 먼저 말한다)과 조회(내가 묻는다).

    python3 tools/telegram.py register    # 봇에게 아무 말이나 보낸 뒤 한 번 실행 → chat_id 저장
    python3 tools/telegram.py notify      # 상태 변화가 있으면 알린다. refresh_all.sh 가 매분 부른다
    python3 tools/telegram.py bot         # 명령을 받는 롱폴링 루프 (상주)
    python3 tools/telegram.py ensure-bot  # 루프가 죽어 있으면 되살린다. refresh_all.sh 가 매분 부른다
    python3 tools/telegram.py send "글"   # 한 줄 보내기
    python3 tools/telegram.py ask "상태"  # 봇 없이 답만 확인

설정은 `.telegram.json` (저장소 밖으로 새지 않게 .gitignore 에 있다):

    {"token": "BotFather 가 준 토큰", "chat_id": 0}

토큰만 적어 두고 `register` 를 돌리면 chat_id 는 알아서 채운다.

## 무엇을 하지 않는가

명령으로 셸을 돌리지 않는다. 실험을 시작하거나 멈추지 않는다. 파일을 읽어 답만 한다.
등록된 chat_id 가 아닌 곳에서 온 메시지는 무시한다. 그래서 봇 주소를 남이 알아도
이 서버에서 할 수 있는 일이 없다.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONF = ROOT / ".telegram.json"
SEEN = ROOT / "dashboard" / ".telegram_seen.json"
LIVE = ROOT / "dashboard" / "live.json"
KST = timezone(timedelta(hours=9))
API = "https://api.telegram.org/bot{}/{}"


def conf():
    if not CONF.exists():
        return None
    try:
        c = json.loads(CONF.read_text(encoding="utf-8"))
        return c if c.get("token") else None
    except Exception:
        return None


def call(method, _timeout=20, **params):
    c = conf()
    if not c:
        return None
    url = API.format(c["token"], method)
    data = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None}).encode()
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=data), timeout=_timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:
        print("telegram %s 실패: %s: %s" % (method, type(e).__name__, e), file=sys.stderr)
        return None


def send(text, chat_id=None):
    c = conf()
    if not c:
        return False
    chat = chat_id or c.get("chat_id")
    if not chat:
        return False
    for i in range(0, max(1, len(text)), 3500):                  # 한 통 4096자 제한
        r = call("sendMessage", chat_id=chat, text=text[i:i + 3500], disable_web_page_preview="true")
        if not r or not r.get("ok"):
            return False
    return True


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
    lines = ["GPU (지금)"]
    for row in out.splitlines():
        p = [x.strip() for x in row.split(",")]
        if len(p) >= 5:
            lines.append("  GPU%s  %s%%  %.1f/%.0f GB  %s" % (p[0], p[2], int(p[3]) / 1024, int(p[4]) / 1024, p[1]))
    procs = sh("nvidia-smi --query-compute-apps=pid,used_memory --format=csv,noheader,nounits")
    lines.append("  계산 프로세스 %d개" % (len(procs.splitlines()) if procs else 0))
    return "\n".join(lines)


def q_status():
    d = live()
    if not d:
        return "live.json 이 없다. 파이프라인이 아직 안 돌았다."
    jobs = d.get("jobs", [])
    act = [r for r in d.get("runs", []) if r.get("active")]
    out = ["스냅샷 %s · %s" % (d.get("generated_at", "")[11:16], d.get("host", ""))]
    if jobs:
        out.append("실행 중 %d개" % len(jobs))
        for j in jobs:
            out.append("  %s × %s %s · GPU%s · %s 경과" % (j["model"], j["dataset"], j["task"], j["gpu"], dur(j["elapsed"])))
    else:
        out.append("실행 중인 실험 없음")
    for r in act:
        done = sum(1 for s in r.get("terminal", {}).values() if s.startswith("COMPLETE") or "SKIP" in s.upper())
        total = len(r.get("planned") or []) or "?"
        line = "진행 %s — %s/%s" % (r["id"], done, total)
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
    return "다음 할 일\n" + "\n".join("  · " + re.sub(r"^- \[.\] ", "", t) for t in items)


def q_journal():
    t = live().get("lab", {}).get("latest_journal_text") or ""
    t = re.sub(r"^---.*?---\n", "", t, flags=re.S).strip()
    return t[:1500] if t else "일지가 없다."


def q_runs():
    runs = live().get("runs", [])[:6]
    if not runs:
        return "기록된 실행이 없다."
    out = ["최근 실행"]
    for r in runs:
        c = {}
        for s in r.get("terminal", {}).values():
            u = s.upper()
            k = "완료" if s.startswith("COMPLETE") or "SKIP" in u else ("OOM/OOT" if ("OOM" in u or "OOT" in u) else "실패")
            c[k] = c.get(k, 0) + 1
        out.append("  %s%s — %s" % (r["id"], " (활성)" if r.get("active") else "",
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
            out.append("%s 일치 %s/%s · |Δ| 중앙값 %.2f" % (label, t["agree"], t["total"], t["median"]))
    outs = sum(len(p[k]["outliers"]) for k in ("T3", "T4", "T5") if p.get(k))
    out.append("이상치 %d칸 (|Δ| 3.0 초과)" % outs)
    out.append("표 전체는 서버별 대조 아티팩트에서 본다.")
    return "\n".join(out)


HELP = """실험 관리 봇 — 읽기만 한다. 실험을 시작하거나 멈추지 않는다.

  상태    지금 무엇이 돌고 있나
  gpu     GPU 사용률 (지금 값)
  실행    최근 실행 요약
  할일    열린 할 일
  일지    최근 일지
  논문    논문 대조 요약
  도움말  이 안내

실행이 끝나거나 실패하면 묻지 않아도 알린다."""

ROUTES = [
    (("상태", "status", "지금"), q_status),
    (("gpu", "지피유", "그래픽"), q_gpu),
    (("실행", "runs", "run"), q_runs),
    (("할일", "할 일", "todo"), q_todo),
    (("일지", "log", "journal"), q_journal),
    (("논문", "paper", "대조"), q_paper),
    (("도움말", "help", "start", "?"), lambda: HELP),
]


def answer(text):
    t = text.strip().lstrip("/").lower()
    for keys, fn in ROUTES:
        if any(t == k or t.startswith(k) for k in keys):
            return fn()
    return "모르는 말이다.\n\n" + HELP


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
    if not d or not conf():
        return 0
    cur = snapshot(d)
    try:
        old = json.loads(SEEN.read_text(encoding="utf-8"))
    except Exception:
        SEEN.write_text(json.dumps(cur, ensure_ascii=False), encoding="utf-8")   # 첫 실행은 기준만 잡는다
        return 0

    msgs = []
    started = [j for j in cur["jobs"] if j not in old.get("jobs", [])]
    ended = [j for j in old.get("jobs", []) if j not in cur["jobs"]]
    msgs += ["시작 — " + j for j in started]
    msgs += ["프로세스 종료 — " + j for j in ended]

    for run, term in cur["terminal"].items():
        before = old.get("terminal", {}).get(run, {})
        for ds, state in term.items():
            if before.get(ds) == state:
                continue
            u = state.upper()
            if u.startswith("COMPLETE"):
                msgs.append("완료 — %s · %s" % (run, ds))
            elif "OOM" in u or "OOT" in u:
                msgs.append("자원 한계 — %s · %s · %s" % (run, ds, state))
            elif "FAIL" in u:
                msgs.append("실패 — %s · %s · %s" % (run, ds, state))

    for name, on in cur["automation"].items():
        if old.get("automation", {}).get(name) and not on:
            msgs.append("경고 — 자동화 '%s' 가 멈췄다" % name)

    if msgs:
        if ended and not cur["jobs"]:
            msgs.append("남은 실험 없음 — GPU 비었다")
        send("\n".join(msgs[:20]) + "\n\n" + datetime.now(KST).strftime("%m-%d %H:%M"))
    SEEN.write_text(json.dumps(cur, ensure_ascii=False), encoding="utf-8")
    return len(msgs)


# ── 루프 ──────────────────────────────────────────────────────────────────────

def bot():
    c = conf()
    if not c:
        print("설정이 없다", file=sys.stderr)
        return 1
    chat, offset = c.get("chat_id"), None
    send("봇 시작. '도움말' 이라고 보내면 쓸 수 있는 말이 나온다.")
    while True:
        r = call("getUpdates", _timeout=80, offset=offset, timeout=60)
        if not r or not r.get("ok"):
            time.sleep(10)
            continue
        for u in r.get("result", []):
            offset = u["update_id"] + 1
            m = u.get("message") or u.get("edited_message") or {}
            text, frm = m.get("text"), (m.get("chat") or {}).get("id")
            if not text or not frm:
                continue
            if chat and str(frm) != str(chat):        # 등록된 대화가 아니면 무시한다
                continue
            send(answer(text), chat_id=frm)


def ensure_bot():
    if not conf():
        return 0
    if sh("ps -eo args --no-headers | grep 'telegram.py bot' | grep -v grep"):
        return 0
    log = ROOT / "dashboard" / "telegram.log"
    subprocess.Popen("nohup %s '%s' bot >> '%s' 2>&1 &" % (sys.executable, Path(__file__), log),
                     shell=True, start_new_session=True)
    print("telegram bot 시작")
    return 1


def register():
    if not conf():
        print("%s 에 토큰을 먼저 적어라: {\"token\": \"...\", \"chat_id\": 0}" % CONF)
        return 1
    r = call("getUpdates", timeout=0)
    ids = [i for i in [((u.get("message") or {}).get("chat") or {}).get("id") for u in (r or {}).get("result", [])] if i]
    if not ids:
        print("아직 받은 메시지가 없다. 텔레그램에서 봇에게 아무 말이나 보낸 뒤 다시 실행해라.")
        return 1
    c = conf()
    c["chat_id"] = ids[-1]
    CONF.write_text(json.dumps(c, ensure_ascii=False, indent=2), encoding="utf-8")
    CONF.chmod(0o600)
    print("chat_id %s 저장" % ids[-1])
    send("등록 완료. 이제 실험이 끝나거나 실패하면 알린다.")
    return 0


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd == "notify":
        n = notify()
        print("알림 %d건" % n if n else "알릴 변화 없음")
    elif cmd == "bot":
        return bot()
    elif cmd == "ensure-bot":
        ensure_bot()
    elif cmd == "register":
        return register()
    elif cmd == "send":
        print("보냄" if send(" ".join(sys.argv[2:])) else "보내지 못함")
    elif cmd == "ask":
        print(answer(" ".join(sys.argv[2:])))
    else:
        print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main())
