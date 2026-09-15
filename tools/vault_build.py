#!/usr/bin/env python3
"""hgnn/vault/ — 클로드(서버 Claude Code)가 실험할 때 읽고 쓰는 연구 노트북을 만든다.

    python3 tools/vault_build.py            # knowledge/ · protocols/ · Home · dashboard/live.json 갱신
    python3 tools/vault_build.py --dry-run

구조 (vault/)
  CLAUDE.md          클로드가 이 볼트를 쓰는 규칙 (레포 루트 CLAUDE.md 와 같은 내용)
  Home.md            색인
  knowledge/         사실 — 생성기가 만든다. 손대지 않는다.
    논문 대조.md · models/<Model>.md · datasets/<DS>.md · 에이전트.md
  protocols/         실행법 — AUTO 구간은 생성, '## 함정과 판단' 은 클로드·사람이 쌓는다.
    실행 규약.md · <Model> 실행.md
  lab/               클로드가 쓴다. 생성기는 없으면 시드만 만들고 건드리지 않는다.
    일지/YYYY-MM-DD.md · 다음 할 일.md · 질문.md
  (papers/ 는 로컬 옵시디언에만 있다 — 사람의 공부 기록)

관제(실행 중 실험·GPU·최근 실행)는 노트가 아니라 dashboard/live.json 으로 내보내고,
Claude 아티팩트가 그걸 심어 사람에게 보여준다. live.json 은 git 에 넣지 않는다.

원칙
  - 구조는 마크다운. 인라인 HTML 은 Δ 배지처럼 없어도 글자로 읽히는 장식뿐.
  - 각 노트의 AUTO:BEGIN ~ AUTO:END 사이만 덮어쓴다. 그 아래는 보존된다.
  - 날짜만 바뀐 노트는 쓰지 않는다 (커밋 잡음 방지).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VAULT = ROOT / "vault"
KNOW, PROT, LAB = VAULT / "knowledge", VAULT / "protocols", VAULT / "lab"
STATE = ROOT / "dashboard" / "state.json"
LIVE = ROOT / "dashboard" / "live.json"
RUNS = ROOT / ".agents" / "env-status" / "full-runs"
SCRIPTS = ROOT / ".agents" / "run-scripts"
ENV_STATUS = ROOT / ".agents" / "env-status"
CLERK_REPORTS = ROOT / ".agents" / "clerk-reports"
KST = timezone(timedelta(hours=9))
HOST = os.uname().nodename.split("-")[0] if hasattr(os, "uname") else "server"

AUTO_BEGIN = "<!-- AUTO:BEGIN -->"
AUTO_END = "<!-- AUTO:END -->"

MODEL_ALIAS = {"GGD (H-GD)": "GGD", "H-GD (GGD)": "GGD", "HGD": "GGD", "H-GD": "GGD",
               "Hypeboy": "HypeBoy", "EDHNN": "ED-HNN", "SEHSSL": "SE-HSSL"}
MODEL_DIR = {"AllSet": "AllSet", "ED-HNN": "EDHNN", "GGD": "H-GD", "GraphMAE2": "GraphMAE2",
             "HGNN": "HGNN", "HNHN": "HNHN", "HypeBoy": "Hypeboy", "HyperGCL": "HyperGCL",
             "HyperGCN": "HyperGCN", "HyperGRL": "HyperGRL", "MaskGAE": "MaskGAE", "MLP": "MLP",
             "PhenomNN": "PhenomNN", "SE-HSSL": "SEHSSL", "TriCL": "TriCL", "UniGCN": "UniGCN",
             "UniGCN2": "UniGCN2", "UniGIN": "UniGIN", "VilLain": "VilLain"}
DIR_TO_MODEL = {v.lower(): k for k, v in MODEL_DIR.items()}
DATASET_ALIAS = {"citeseer_cite": "Citeseer", "cora_coauth": "Cora-CA", "imdb": "IMDB",
                 "house": "House", "pubmed_cite": "Pubmed", "aminer": "AMiner",
                 "dblp_copub": "DBLP-A", "dblp_coauth": "DBLP-A", "dblp_p": "DBLP-P",
                 "modelnet_40": "MN-40", "news": "20News", "cora_cite": "Cora"}
TASK_LABEL = {"T3": ("Node classification", "노드 분류", "Accuracy", "node", "NC"),
              "T4": ("Hyperedge prediction", "하이퍼엣지 예측", "AUROC", "edge", "HP"),
              "T5": ("Community detection", "커뮤니티 탐지", "NMI", "cluster", "CD")}
CELL_RE = re.compile(r"\*\*([-\d.]+)\s*±\s*([-\d.]+)\*\*\s*\(Δ\s*\*\*([−+\-]?[\d.]+)\*\*\)")


# --------------------------------------------------------------------------
def now():
    return datetime.now(KST)


def stamp(dt=None):
    return (dt or now()).strftime("%Y-%m-%d %H:%M")


def ago(dt):
    if dt is None:
        return "—"
    s = int((now() - dt).total_seconds())
    if s < 60:
        return f"{s}초 전"
    if s < 3600:
        return f"{s // 60}분 전"
    if s < 86400:
        return f"{s // 3600}시간 {s % 3600 // 60}분 전"
    return f"{s // 86400}일 {s % 86400 // 3600}시간 전"


def dur(seconds):
    seconds = int(seconds)
    if seconds < 3600:
        return f"{seconds // 60}분"
    if seconds < 86400:
        return f"{seconds // 3600}시간 {seconds % 3600 // 60}분"
    return f"{seconds // 86400}일 {seconds % 86400 // 3600}시간"


def mtime(path):
    try:
        return datetime.fromtimestamp(Path(path).stat().st_mtime, KST)
    except OSError:
        return None


def sh(cmd, timeout=10):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout).stdout
    except Exception:
        return ""


def read(path, limit=None):
    try:
        t = Path(path).read_text(encoding="utf-8", errors="replace")
        return t if limit is None else t[:limit]
    except OSError:
        return ""


# --------------------------------------------------------------------------
# state.json
# --------------------------------------------------------------------------
def parse_cell(text):
    m = CELL_RE.search(text or "")
    if m:
        return dict(kind="val", value=float(m.group(1)), sd=float(m.group(2)),
                    delta=float(m.group(3).replace("−", "-")), text=text)
    t = (text or "").strip()
    low = t.lower()
    if "o.o.m" in low or "o.o.t" in low or "oom" in low or "oot" in low:
        return dict(kind="lim", label="OOM" if ("o.o.m" in low or "oom" in low) else "OOT", text=t.lstrip("— ").strip())
    return dict(kind="na", reason=t.lstrip("— ").strip() or "미실행", text=t)


def load_state():
    s = json.loads(STATE.read_text(encoding="utf-8"))
    tasks = {}
    for t in s["tasks"]:
        header = t["header"][1:]
        rows = {MODEL_ALIAS.get(r[0], r[0]): {ds: parse_cell(c) for ds, c in zip(header, r[1:])} for r in t["rows"]}
        ref = {MODEL_ALIAS.get(m, m): v for m, v in t.get("reference", {}).items()}
        tasks[t["key"]] = dict(header=header, rows=rows, reference=ref, metric=t["metric"])
    return s, tasks


def value_cols(task):
    return [d for d in task["header"] if any(task["rows"][m][d]["kind"] == "val" for m in task["rows"])]


def task_stats(task):
    deltas, agree, done, outliers = [], 0, 0, []
    for model, cells in task["rows"].items():
        vals = [c for c in cells.values() if c["kind"] == "val"]
        if vals:
            done += 1
        for ds, c in cells.items():
            if c["kind"] != "val":
                continue
            deltas.append(abs(c["delta"]))
            agree += abs(c["delta"]) <= 2
            if abs(c["delta"]) > 3:
                outliers.append((model, ds, c))
    med = sorted(deltas)[len(deltas) // 2] if deltas else 0.0
    return len(deltas), agree, med, done, outliers


# --------------------------------------------------------------------------
# 표기
# --------------------------------------------------------------------------
def delta_class(d):
    a = abs(d)
    return "ok" if a <= 2 else ("warn" if a <= 5 else "bad")


def fmt_delta(d):
    return ("+" if d >= 0 else "−") + f"{abs(d):.1f}"


def badge(d):
    return f'<span class="d {delta_class(d)}">{fmt_delta(d)}</span>'


def val(c):
    return f'{c["value"]:.1f} <span class="sd">±{c["sd"]:.1f}</span>'


def cell(c):
    if c["kind"] == "val":
        return f"{val(c)} {badge(c['delta'])}"
    if c["kind"] == "lim":
        return f'<span class="lim">{c["label"]}</span>'
    return "—"


def small(text):
    return f"<small>{text}</small>"


def md_table(header, rows, align=None):
    align = align or ["---"] * len(header)
    out = ["| " + " | ".join(header) + " |", "|" + "|".join(align) + "|"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def callout(kind, title, body_lines, fold=True):
    out = [f"> [!{kind}]{'-' if fold else ''} {title}"]
    out += ["> " + l if l else ">" for l in body_lines]
    return "\n".join(out)


LEGEND = ("표기 · 값 <span class=\"sd\">±표준편차</span> · Δ = 우리 − 논문 · "
          f"{badge(0.3)} ±2 이내 · {badge(3.0)} 2–5 · {badge(7.0)} 5 초과 · "
          "<span class=\"lim\">OOM</span> 논문이 수치를 못 낸 칸 · — 미실행·보류")

VOLATILE_RE = re.compile(r"(갱신 |updated: )\d{4}-\d{2}-\d{2}[ T:\d]*")


def write_note(path, body, frontmatter=None, dry_run=False, tail_default="\n\n## 메모\n\n\n"):
    fm = "---\n" + "\n".join(frontmatter) + "\n---\n\n" if frontmatter else ""
    block = f"{AUTO_BEGIN}\n{body}\n{AUTO_END}"
    old = None
    if path.exists():
        old = path.read_text(encoding="utf-8")
        tail = old
        if tail.startswith("---\n"):
            end = tail.find("\n---\n", 4)
            if end != -1:
                tail = tail[end + 5:]
        new = fm + block + (tail.rsplit(AUTO_END, 1)[1] if AUTO_BEGIN in tail and AUTO_END in tail
                            else "\n\n" + tail.lstrip())
    else:
        new = fm + block + tail_default
    if old is not None and VOLATILE_RE.sub(r"\1<D>", old) == VOLATILE_RE.sub(r"\1<D>", new):
        return False
    if old == new:
        return False
    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(new, encoding="utf-8")
    return True


def front(kind, **kw):
    lines = [f"type: {kind}"]
    for k, v in kw.items():
        if isinstance(v, str) and not re.match(r"^[\w.\-]+$", v):
            v = '"' + v.replace('"', "'") + '"'
        lines.append(f"{k}: {v}")
    lines.append(f"updated: {stamp()}")
    lines.append(f"tags: [hgnn/{kind}]")
    return lines


# --------------------------------------------------------------------------
# knowledge/
# --------------------------------------------------------------------------
def note_paper(state, tasks, dry):
    n3, n4 = task_stats(tasks["T3"]), task_stats(tasks["T4"])
    n5 = task_stats(tasks["T5"]) if "T5" in tasks else (0, 0, 0, 0, [])
    outs_all = len(n3[4]) + len(n4[4]) + len(n5[4])
    lines = ["# 논문 대조 — HyperGC Table 3·4·5", "",
             "clerk 원장의 정식 20-seed 결과를 KDD ’26 HyperGC 논문 표와 셀 단위로 대조한다. Δ = 우리 평균 − 논문 평균. "
             + small("갱신 " + stamp()), "",
             md_table(["NC 일치율", "HP 일치율", "완료 모델 (NC · HP)", "이상치 |Δ|>3"],
                      [[f"**{n3[1]}/{n3[0]}**", f"**{n4[1]}/{n4[0]}**", f"**{n3[3]} · {n4[3]}** / 19", f"**{outs_all}**"],
                       [small(f"|Δ| 중앙값 {n3[2]:.2f}"), small(f"|Δ| 중앙값 {n4[2]:.2f}"), "", ""]]), ""]
    a = state.get("audit", {})
    if a.get("available"):
        lines += [f"> [!check] 원장의 Δ {a['checked']}칸을 `paper_reference.json`(HyperGC.pdf)과 대조 — 일치 {a['agree']} · 불일치 {len(a['mismatch'])}", ""]
    lines += [LEGEND, ""]
    for key in ("T3", "T4", "T5"):
        if key not in tasks:
            continue
        t = tasks[key]; en, _, metric, _, _ = TASK_LABEL[key]
        cols = value_cols(t)
        lines += [f"## {en} — Table {key[1]} · {metric}", ""]
        if not cols:
            lines += ["정식 결과가 아직 없다. 원장에 등록된 모델: " + ", ".join(f"[[{m}]]" for m in sorted(t["rows"])), ""]
            continue
        rows = [[f"[[{m}]]"] + [cell(t["rows"][m][d]) for d in cols]
                for m in sorted(t["rows"], key=lambda m: (-sum(c["kind"] == "val" for c in t["rows"][m].values()), m))]
        lines += [md_table(["모델"] + cols, rows, ["---"] + ["---:"] * len(cols)), ""]
        empty = [d for d in t["header"] if d not in cols]
        if empty:
            lines += [small("표시하지 않은 열 (정식 결과 없음): " + ", ".join(empty)), ""]
    outs = []
    for key in ("T3", "T4", "T5"):
        if key in tasks:
            for m, ds, c in task_stats(tasks[key])[4]:
                outs.append((abs(c["delta"]), TASK_LABEL[key][4], m, ds, c, tasks[key]["reference"].get(m, {}).get(ds)))
    outs.sort(key=lambda x: -x[0])
    body = ["| 태스크 | 모델 | 데이터셋 | 우리 | 논문 | Δ |", "|---|---|---|---:|---:|---:|"] if outs else ["없음."]
    for _, tag, m, ds, c, ref in outs:
        body.append(f"| {tag} | [[{m}]] | {ds} | {c['value']:.1f} | {ref:.1f} | {badge(c['delta'])} |"
                    if isinstance(ref, (int, float)) else f"| {tag} | [[{m}]] | {ds} | {c['value']:.1f} | ? | {badge(c['delta'])} |")
    lines += [callout("warning", f"이상치 {len(outs)}개 — |Δ| 3.0 초과", body), ""]
    upd = state.get("updates", {})
    if upd.get("items"):
        lines += [callout("quote", f"원장의 최근 기록 — {upd.get('title', '')}", [f"- {it}" for it in upd["items"][:8]]), ""]
    lines += [small("원본 `.agents/clerk-reports/experiment_now.md` → `dashboard/state.json` · 기준값 `dashboard/paper_reference.json`")]
    return write_note(KNOW / "논문 대조.md", "\n".join(lines),
                      front("knowledge", nc_agree=n3[1], nc_total=n3[0], hp_agree=n4[1], hp_total=n4[0], outliers=outs_all), dry)


def note_models(tasks, dry):
    changed = 0
    for m in sorted({m for t in tasks.values() for m in t["rows"]}):
        per = {k: t["rows"][m] for k, t in tasks.items() if m in t["rows"]}
        props, worst = {}, None
        for key in per:
            vals = [c for c in per[key].values() if c["kind"] == "val"]
            short = TASK_LABEL[key][4].lower()
            props[f"{short}_done"] = len(vals)
            props[f"{short}_agree"] = sum(abs(c["delta"]) <= 2 for c in vals)
            for ds, c in per[key].items():
                if c["kind"] == "val" and (worst is None or abs(c["delta"]) > abs(worst[2])):
                    worst = (key, ds, c["delta"])
        props["max_abs_delta"] = round(abs(worst[2]), 1) if worst else 0
        props["worst_cell"] = f"{TASK_LABEL[worst[0]][1]} {worst[1]} {fmt_delta(worst[2])}" if worst else ""
        props["status"] = ("blocked" if props.get("nc_done", 0) + props.get("hp_done", 0) == 0 else
                           "complete" if props.get("nc_done", 0) >= 6 and props.get("hp_done", 0) >= 6 else "partial")
        d = MODEL_DIR.get(m, m)
        lines = [f"# {m}", "",
                 f"실행법 → [[{m} 실행]] · 코드 `{d}/` · 결과 `results/result_*_{d}_*.txt` · " + small("갱신 " + stamp()), ""]
        summ = [f"{TASK_LABEL[k][4]} {props[TASK_LABEL[k][4].lower() + '_agree']}/{props[TASK_LABEL[k][4].lower() + '_done']} 일치"
                for k in per if props.get(TASK_LABEL[k][4].lower() + "_done")]
        if summ:
            lines += [" · ".join(summ) + (f" · 최대 편차 {props['worst_cell']}" if worst else ""), ""]
        for key in ("T3", "T4", "T5"):
            if key not in per:
                continue
            en, _, metric, _, _ = TASK_LABEL[key]
            ref = tasks[key]["reference"].get(m, {})
            rows = []
            for ds in tasks[key]["header"]:
                c, r = per[key][ds], ref.get(ds)
                refs = f"{r:.1f}" if isinstance(r, (int, float)) else "—"
                if c["kind"] == "val":
                    rows.append([f"[[{ds}]]", val(c), refs, badge(c["delta"]), ""])
                elif c["kind"] == "lim":
                    rows.append([f"[[{ds}]]", f'<span class="lim">{c["label"]}</span>', refs, "", c["text"]])
                else:
                    rows.append([f"[[{ds}]]", "—", refs, "", c["reason"]])
            lines += [f"## {en} — Table {key[1]} · {metric}", "",
                      md_table(["데이터셋", "우리", "논문", "Δ", "비고"], rows, ["---", "---:", "---:", "---:", "---"]), ""]
        lines += [LEGEND]
        if write_note(KNOW / "models" / f"{m}.md", "\n".join(lines), front("model", code_dir=d, **props), dry):
            changed += 1
    return changed


def note_datasets(tasks, dry):
    changed = 0
    datasets = []
    for t in tasks.values():
        datasets += [d for d in t["header"] if d not in datasets]
    for ds in datasets:
        props, lines = {}, [f"# {ds}", "", small("갱신 " + stamp()), ""]
        for key in ("T3", "T4", "T5"):
            t = tasks.get(key)
            if not t or ds not in t["header"]:
                continue
            en, _, metric, _, short = TASK_LABEL[key]
            rows = [(m, t["rows"][m][ds]) for m in t["rows"]]
            vals = sorted([(m, c) for m, c in rows if c["kind"] == "val"], key=lambda x: -x[1]["value"])
            others = [(m, c) for m, c in rows if c["kind"] != "val"]
            if not vals and not others:
                continue
            lines += [f"## {en} — {metric}", ""]
            if vals:
                props[f"{short.lower()}_models"] = len(vals)
                props[f"{short.lower()}_best"] = vals[0][0]
                trows = []
                for i, (m, c) in enumerate(vals, 1):
                    r = t["reference"].get(m, {}).get(ds)
                    trows.append([i, f"[[{m}]]", val(c), f"{r:.1f}" if isinstance(r, (int, float)) else "—", badge(c["delta"])])
                lines += [md_table(["#", "모델", "우리", "논문", "Δ"], trows, ["---:", "---", "---:", "---:", "---:"]), ""]
            else:
                lines += ["정식 결과 없음.", ""]
            if others:
                lines += [small("미실행·보류: " + ", ".join(f"{m} ({c.get('label') or c.get('reason')})" for m, c in others)), ""]
        if write_note(KNOW / "datasets" / f"{ds}.md", "\n".join(lines), front("dataset", **props), dry):
            changed += 1
    return changed


# --------------------------------------------------------------------------
# 에이전트 · 실행 이력 (knowledge/에이전트.md 는 드물게 바뀜, 실시간은 live.json)
# --------------------------------------------------------------------------
AGENTS = [
    dict(name="clerk", file=".agents/clerk.md", short="결과 원장 관리",
         role="정식 20-seed 실행이 끝나면 `experiment_now.md` 에 값과 논문 Δ를 기록하고, 한글 보고서(개별/통합)를 쓴다. smoke 결과는 표에 올리지 않는다.",
         inputs="`results/` · `full-runs/status.tsv` · `paper_reference.json`",
         outputs="`clerk-reports/experiment_now.md` · `개별/` · `통합/`",
         process="tools/refresh_all.sh (cron 1분)", activity=["clerk-reports/experiment_now.md", "clerk-reports/개별"]),
    dict(name="env-builder", file=".agents/env-builder.md", short="Conda 환경 구축",
         role="모델별 Conda 환경을 만들고 유지한다. 모델 코드는 건드리지 않고 환경 변경과 차단 요인을 기록한다. HyperGCL 은 다른 모델이 모두 끝난 뒤에만.",
         inputs="`*_require.txt` · env-checker 피드백", outputs="`env-status/env-builder.md` · `edge-builder-report.md`",
         process=None, activity=["env-status/env-builder.md", "env-status/edge-builder-report.md"]),
    dict(name="env-checker", file=".agents/env-checker.md", short="환경·모델 검증",
         role="env-builder 가 준비한 환경에서 모델을 검증한다. import → 1-seed 15-epoch smoke → 논문값과 대략 비교. 정식 실행의 게이트 파일(`*-check.ok`)을 만든다.",
         inputs="`env-status/` 빌더 핸드오프 · `time_node.sh`", outputs="`env-status/checker-*.md` · `*-check.ok`",
         process=None, activity=["env-status/edge-checker-report.md", "env-status/checker-", "env-status/villain-edge-check.ok"]),
]


def latest_activity(patterns):
    best = None
    for pat in patterns:
        p = ROOT / ".agents" / pat
        cands = list(p.iterdir()) if p.is_dir() else ([p] if p.exists() else list(p.parent.glob(p.name + "*")))
        for c in cands:
            t = mtime(c)
            if t and (best is None or t > best[0]):
                best = (t, c.relative_to(ROOT).as_posix())
    return best


def agent_status():
    ps = sh("ps -eo pid,etimes,args --no-headers")
    out = []
    for a in AGENTS:
        proc = None
        if a["process"]:
            hit = [l for l in ps.splitlines() if a["process"] in l and "grep" not in l]
            if hit:
                p = hit[0].split(None, 2)
                proc = dict(pid=int(p[0]), uptime=int(p[1]))
        act = latest_activity(a["activity"])
        age = (now() - act[0]).total_seconds() if act else None
        if proc:
            state, why = "active", "루프 프로세스가 돌고 있다"
        elif age is not None and age < 3600:
            state, why = "active", "1시간 내 산출물 갱신"
        elif age is not None and age < 86400:
            state, why = "idle", "24시간 내 활동, 지금은 호출되지 않음"
        else:
            state, why = "inactive", "24시간 넘게 산출물 변화 없음"
        out.append(dict(a, state=state, why=why, proc=proc,
                        last=act[0].isoformat() if act else None, last_file=act[1] if act else None))
    return out


def note_agents(dry):
    ags = agent_status()
    label = {"active": "활성", "idle": "대기", "inactive": "비활성"}
    lines = [f"# 에이전트 — {HOST}", "", small(f"정의서 `.agents/*.md` · 실시간 상태는 관제 아티팩트에서 · 갱신 {stamp()}"), "",
             md_table(["에이전트", "역할", "상주 프로세스", "산출물"],
                      [[f"[[#{a['name']}\\|{a['name']}]]", a["short"], f"`{a['process']}`" if a["process"] else "없음 (Claude 세션이 호출)", a["outputs"]] for a in ags]), ""]
    for a in ags:
        lines += ["---", "", f"## {a['name']}", "", a["role"], "",
                  md_table(["항목", "내용"], [["정의서", f"`{a['file']}`"], ["입력", a["inputs"]], ["출력", a["outputs"]],
                                            ["상주 프로세스", f"`{a['process']}`" if a["process"] else "없음 — Claude 세션이 필요할 때 호출"],
                                            ["판정 기준", "프로세스 생존 → 활성 · 산출물 1시간 내 → 활성 · 24시간 내 → 대기 · 그 외 비활성"]]), ""]
    return write_note(KNOW / "에이전트.md", "\n".join(lines), front("knowledge", host=HOST), dry)


# --------------------------------------------------------------------------
# protocols/
# --------------------------------------------------------------------------
def env_map():
    """env-status/README.md 의 모델 상태표에서 모델 → 환경 이름."""
    txt = read(ENV_STATUS / "README.md")
    out = {}
    for line in txt.splitlines():
        m = re.match(r"\|\s*\d+(?:\s*\(last\))?\s*\|\s*([A-Za-z0-9\-]+)\s*\|\s*`([^`]+)`", line)
        if m:
            name = MODEL_ALIAS.get(m.group(1), m.group(1))
            name = DIR_TO_MODEL.get(m.group(1).lower(), name)
            out[name] = m.group(2)
    return out


def env_table():
    txt = read(ENV_STATUS / "README.md")
    rows = []
    for line in txt.splitlines():
        m = re.match(r"\|\s*`([a-z0-9\-]+)`\s*\|\s*([^|]+)\|\s*([^|]+)\|", line)
        if m:
            rows.append([f"`{m.group(1)}`", m.group(2).strip(), m.group(3).strip()])
    return rows


def formal_commands(d):
    """<dir>/118.sh 의 python 줄 — 정식 설정."""
    txt = read(ROOT / d / "118.sh")
    cmds = [l.strip() for l in txt.splitlines() if l.strip().startswith("python")]
    return cmds


def note_protocol_common(tasks, dry):
    oom = []
    for key, t in tasks.items():
        for m, cells in t["rows"].items():
            for ds, c in cells.items():
                if c["kind"] == "lim":
                    oom.append(f"{m} × {ds} ({TASK_LABEL[key][4]}, {c['label']})")
    lines = ["# 실행 규약", "", small("공통 규칙. 모델별 명령은 각 `<모델> 실행` 노트에. 갱신 " + stamp()), "",
             "## 정식 실행이란", "",
             "- 전임자 `<모델>/118.sh` 의 **고정 설정** · 기본 **200 epoch** · **20 split/seed**. 이것만 원장(Table 3·4·5)에 올라간다.",
             "- smoke(1 seed · 15 epoch)는 실행 가능성 확인용이다. 원장에 쓰지 않는다.",
             "- 노드 분류 분할은 `data_split_0.01.pickle` (train 1% / valid 1% / test 98%) — HyperGC 4장 프로토콜. `data_split_118.pickle`(10/10/80)은 Table 3 대비가 성립하지 않는다.",
             "- 하이퍼엣지 예측 분할은 60 / 20 / 20, 음성 하이퍼엣지는 정답과 같은 수, 지표는 AUROC.", "",
             "## 환경", "", md_table(["환경", "requirement", "모델"], env_table() or [["?", "README.md 표를 못 읽음", ""]]), "",
             "실행은 `conda run --no-capture-output -n <env> bash -lc \"<명령>\"`. GPU 는 `--gpu`/`--device` 인자 또는 `CUDA_VISIBLE_DEVICES`.", "",
             "## 실행 스크립트 규약 (`.agents/run-scripts/*.sh`)", "",
             "- `run_id=\"<이름>-gpu<N>-<YYYYMMDD>\"`, 로그는 `.agents/env-status/full-runs/<run_id>/<dataset>.log`",
             "- 데이터셋 하나가 끝날 때마다 `status.tsv` 에 `모델\\t데이터셋\\t상태\\t시각` 을 append. 상태: `COMPLETE` · `FAILED_*` · `OOM` · `OOT` · `SKIP_EXISTING`",
             "- 결과 파일이 이미 있으면 건너뛴다 (`SKIP_EXISTING`). 결과는 `results/result_<dataset>_<Dir>_<task>.txt`",
             "- `timeout 24h` 로 감싼다. 종료 코드 124 = OOT.",
             "- 다른 실행을 기다릴 땐 `pgrep -f '[스]크립트명'` 루프, env-checker 승인은 `*-check.ok` 파일 존재로 판단한다.", "",
             "## 돌리지 말 것 (논문이 O.O.M / O.O.T 로 보고)", ""] + [f"- {x}" for x in oom] + ["",
             "## 데이터셋 이름", "", md_table(["원시 이름", "논문 표기"], [[k, v] for k, v in DATASET_ALIAS.items()]), "",
             "## 결과가 원장에 오르는 길", "",
             "`results/*.txt` → `tools/refresh_all.sh` 가 1분마다 한 줄로 돌린다: `clerk_refresh.py` 가 `experiment_now.md` 에 값·Δ 기록 → `collector.py` 가 `state.json` → `vault_build.py` 가 [[논문 대조]] · `knowledge/models/` 갱신 → 바뀐 노트만 커밋·푸시.",
             "실험 직후 노트에 안 보이면 어느 단계에서 멈췄는지 `dashboard/pipeline.log` 로 본다."]
    return write_note(PROT / "실행 규약.md", "\n".join(lines), front("protocol"), dry,
                      tail_default="\n\n## 함정과 판단\n\n<!-- 클로드·사람이 실험하며 알게 된 것을 여기 쌓는다. 위 AUTO 구간은 덮어써진다. -->\n\n")


def note_protocols(tasks, dry):
    changed = 0
    envs = env_map()
    scripts_txt = {p.name: read(p) for p in SCRIPTS.glob("*.sh")} if SCRIPTS.is_dir() else {}
    for m in sorted({m for t in tasks.values() for m in t["rows"]}):
        d = MODEL_DIR.get(m, m)
        cmds = formal_commands(d)
        files = sorted(p.name for p in (ROOT / d).glob("*.sh")) if (ROOT / d).is_dir() else []
        info = read(ROOT / d / "info.txt", 1200).strip()
        used_by = [n for n, t in scripts_txt.items() if f"{d}/" in t]
        gates = sorted({g for t in scripts_txt.values() for g in re.findall(r"env-status/([\w\-]+\.ok)", t) if d.lower().split("-")[0][:5] in g.lower()})
        done = {k: sum(c["kind"] == "val" for c in tasks[k]["rows"][m].values()) for k in tasks if m in tasks[k]["rows"]}
        lim = [f"{ds} ({TASK_LABEL[k][4]})" for k in tasks if m in tasks[k]["rows"] for ds, c in tasks[k]["rows"][m].items() if c["kind"] == "lim"]
        lines = [f"# {m} 실행", "",
                 f"결과 → [[{m}]] · 코드 `{d}/` · 환경 `{envs.get(m, '?')}` · " + small("갱신 " + stamp()), "",
                 "## 정식 명령 (`" + d + "/118.sh`)", ""]
        if cmds:
            lines += ["```bash", f"conda run --no-capture-output -n {envs.get(m, '<env>')} bash -lc '\\", "  cd " + str(ROOT) + " && \\"]
            lines += ["  " + c + (" \\" if i < len(cmds) - 1 else "'") for i, c in enumerate(cmds)]
            lines += ["```", "", small("한 줄이 데이터셋 하나. `--gpu`/`--device` 값은 스크립트 변수(`$gpu`)로 바꿔 쓴다."), ""]
        else:
            lines += ["`118.sh` 가 없다. 아래 스크립트 목록에서 정식 설정을 확인할 것.", ""]
        lines += ["## 파일", "", md_table(["항목", "내용"], [
            ["스크립트", " · ".join(f"`{f}`" for f in files) or "—"],
            ["실행에 쓴 run-scripts", " · ".join(f"`{n}`" for n in sorted(used_by)) or "—"],
            ["게이트 파일", " · ".join(f"`{g}`" for g in gates) or "—"],
            ["정식 완료", " · ".join(f"{TASK_LABEL[k][4]} {v}칸" for k, v in done.items()) or "—"],
            ["돌리지 말 것", ", ".join(lim) or "없음"]]), ""]
        if info:
            lines += ["## info.txt", "", "```", info, "```", ""]
        lines += [f"관련: [[실행 규약]] · [[{m}]]"]
        if write_note(PROT / f"{m} 실행.md", "\n".join(lines), front("protocol", model=m, env=envs.get(m, "")), dry,
                      tail_default="\n\n## 함정과 판단\n\n<!-- 이 모델을 돌리며 알게 된 것: 실패 원인, 고친 것, 다시 보지 말아야 할 길. AUTO 구간은 덮어써진다. -->\n\n"):
            changed += 1
    return changed


# --------------------------------------------------------------------------
# lab/ — 시드만. 이후엔 클로드가 쓴다.
# --------------------------------------------------------------------------
def seed_lab(dry):
    made = 0
    seeds = {
        LAB / "다음 할 일.md": "\n".join([
            "---", "type: lab", "tags: [hgnn/lab]", "---", "", "# 다음 할 일", "",
            "실험을 시작하기 전에 읽고, 끝내면 체크한다. 새 항목은 위에 추가한다.", "",
            "- [ ] HyperGCL 하이퍼엣지 예측 — Pubmed · AMiner (원장 pending)",
            "- [ ] VilLain 하이퍼엣지 예측 — HyperGCL 뒤에 대기 중 (`villain-edge-check.ok` 게이트)",
            "- [ ] Community detection (Table 5) — VilLain · MaskGAE · HyperGCL 전부 pending, HyperGRL 은 코드 없음",
            "- [ ] TriCL HP 편차 (House −5.4 · AMiner −4.4) — `num_edges` 확장을 max() 대신 스플릿 기준 재계산으로",
            "- [ ] SE-HSSL × House NC (+12.7) — 저장소 어느 설정으로도 논문값 48.0 이 재현되지 않음. 원인 미상",
            "- [ ] GGD 전 데이터셋 하향 — 매핑 착오 아님. 코드 차이 확인", ""]),
        LAB / "질문.md": "\n".join([
            "---", "type: lab", "tags: [hgnn/lab]", "---", "", "# 열린 질문", "",
            "답을 찾으면 답과 근거 경로를 적고 `[x]` 로 닫는다. 지우지 않는다.", "",
            "- [ ] HyperGCL NC 가 Citeseer −24.9 · Cora-CA −45.5 인데 논문 수치가 맞나, 우리 GPU 샘플러 경로가 다른가?",
            "- [ ] VilLain HP 를 새로 구현했다 (원본 eval.py 의 edge 분기가 주석 처리). 논문의 평가 절차와 같은가?",
            "- [ ] `VilLain/emb_concat.py` 파일 필터가 부분일치라 `ns4_nsg10` 이 `nsg100` 도 잡는다 — 결과 오염 범위는?",
            "- [ ] HyperGRL 은 노드 임베딩을 반환하지 않아 HP 평가에 연결할 코드가 없다. 구현할 것인가, 불가로 둘 것인가?", ""]),
        LAB / "일지" / "_템플릿.md": "\n".join([
            "---", "type: lab", "date: YYYY-MM-DD", "tags: [hgnn/lab]", "---", "", "# YYYY-MM-DD", "",
            "## 한 일", "", "- **무엇** · **왜** · 명령/스크립트 · run_id", "",
            "## 결과", "", "- 수치 (결과 파일 경로) · 원장 반영 여부", "",
            "## 판단", "", "- 무엇을 배웠고, 다음에 무엇을 할지. `다음 할 일` · `질문` 갱신.", ""]),
    }
    for p, body in seeds.items():
        if p.exists():
            continue
        if not dry:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(body, encoding="utf-8")
        made += 1
    return made


# --------------------------------------------------------------------------
# Home
# --------------------------------------------------------------------------
def note_home(tasks, dry):
    models = sorted({m for t in tasks.values() for m in t["rows"]})
    journals = sorted(p.name for p in (LAB / "일지").glob("20*.md")) if (LAB / "일지").is_dir() else []
    lines = ["# HGNN 연구 노트북", "", small(f"{HOST} 의 `vault/` · 클로드가 실험할 때 읽고 쓰는 곳 · 사람은 관제 아티팩트를 본다 · 갱신 {stamp()}"), "",
             "## 실험 전에", "",
             "- [[실행 규약]] — 정식 실행 정의 · 분할 · 환경 · 스크립트 규약 · 돌리지 말 것",
             "- [[다음 할 일]] · [[질문]] — 무엇을 왜 하는지",
             "- `protocols/<모델> 실행` — 그 모델의 정식 명령과 함정", "",
             "## 실험 후에", "",
             "- `lab/일지/오늘.md` 에 무엇·왜·결과·판단 (템플릿 `_템플릿.md`, 명령 `/lab-log`)",
             "- 새로 안 함정은 해당 `protocols/` 노트의 **함정과 판단** 에", "",
             "## 사실 (자동 생성 · 손대지 않는다)", "",
             "- [[논문 대조]] — HyperGC Table 3·4·5 vs 우리 정식 결과",
             "- [[에이전트]] — clerk / env-builder / env-checker",
             "- `knowledge/models/` " + " · ".join(f"[[{m}]]" for m in models), "",
             "## 최근 일지", ""] + ([f"- [[{j[:-3]}]]" for j in reversed(journals[-5:])] or ["- 아직 없음"]) + ["",
             "## 갱신 흐름", "",
             md_table(["무엇", "누가", "주기"], [
                 ["원장·Δ", "clerk → `collector.py`", "10분 · 5분"],
                 ["knowledge/ · protocols/ AUTO 구간 · `live.json`", "`tools/vault_build.py`", "1분 (내용 바뀔 때만 커밋)"],
                 ["lab/ · protocols 의 함정과 판단", "클로드 (실험할 때)", "그때그때"],
                 ["로컬 옵시디언", "`hgnn_sync.ps1` git pull", "1분"],
                 ["관제 아티팩트", "Claude 세션 (온디맨드 · 루프)", "요청 시 · 5분"]])]
    return write_note(VAULT / "Home.md", "\n".join(lines), front("home"), dry, tail_default="\n")


# --------------------------------------------------------------------------
# live.json — 관제 아티팩트용
# --------------------------------------------------------------------------
def gpu_info():
    gpus = []
    for line in sh("nvidia-smi --query-gpu=index,name,utilization.gpu,memory.used,memory.total,uuid --format=csv,noheader,nounits").strip().splitlines():
        p = [x.strip() for x in line.split(",")]
        if len(p) >= 6:
            gpus.append(dict(index=int(p[0]), name=p[1].replace("NVIDIA GeForce ", ""), util=int(p[2]), used=int(p[3]), total=int(p[4]), uuid=p[5], pids=[]))
    for line in sh("nvidia-smi --query-compute-apps=pid,gpu_uuid --format=csv,noheader,nounits").strip().splitlines():
        p = [x.strip() for x in line.split(",")]
        for g in gpus:
            if len(p) >= 2 and g["uuid"] == p[1]:
                g["pids"].append(int(p[0]))
    for g in gpus:
        g.pop("uuid", None)
    return gpus


def jobs():
    found = []
    for line in sh("ps -eo pid,etimes,args --no-headers").splitlines():
        parts = line.strip().split(None, 2)
        if len(parts) < 3:
            continue
        pid, et, args = int(parts[0]), int(parts[1]), parts[2]
        if "python" not in args or ".py" not in args or "conda run" in args or any(x in args for x in ("dashboard/", "tools/", "run-scripts/", "vscode")):
            continue
        model = next((DIR_TO_MODEL[d.lower()] for d in MODEL_DIR.values() if re.search(rf"(^|[\s/]){re.escape(d)}/", args)), None)
        if not model:
            continue
        m = re.search(r"--(?:dataset|data)[= ]([\w-]+)", args)
        t = re.search(r"--task[= ](\w+)", args)
        g = re.search(r"--(?:gpu|device|cuda)[= ](\d+)", args) or re.search(r"CUDA_VISIBLE_DEVICES=(\d+)", args)
        s = re.search(r"--num_seeds[= ](\d+)", args)
        found.append(dict(pid=pid, elapsed=et, model=model, dataset=DATASET_ALIAS.get(m.group(1), m.group(1)) if m else "?",
                          task=t.group(1) if t else "?", gpu=g.group(1) if g else "?", seeds=s.group(1) if s else "?"))
    return found


def planned_datasets(run_id):
    if not SCRIPTS.is_dir():
        return None, None
    for p in SCRIPTS.glob("*.sh"):
        txt = read(p)
        if f'run_id="{run_id}"' not in txt and f"run_id={run_id}" not in txt:
            continue
        m = re.search(r"settings=\((.*?)\)", txt, re.S)
        if m:
            ds = re.findall(r'"\s*([a-z][a-z0-9_]+)\b', m.group(1))
            if ds:
                return ds, p.name
        m = re.search(r"for\s+(?:dataset|ds|data)\s+in\s+([^;\n]+)", txt)
        if m:
            ds = [x.strip('"\'') for x in m.group(1).split() if re.match(r"^[a-z][a-z0-9_]+$", x.strip('"\''))]
            if ds:
                return ds, p.name
        return None, p.name
    return None, None


def parse_status(path):
    rows = []
    for line in read(path).splitlines():
        p = line.rstrip("\n").split("\t")
        if len(p) == 1:
            p = line.split()
        if not p or not p[0]:
            continue
        ds, state = (p[1], p[2]) if len(p) >= 3 else ((p[0], p[1]) if len(p) == 2 else (None, None))
        if state and state.isdigit():
            state = {"0": "COMPLETE", "124": "OOT"}.get(state, f"FAILED({state})")
        if ds:
            rows.append(dict(dataset=ds, state=state or "?"))
    return rows


def run_dirs():
    out = []
    if not RUNS.is_dir():
        return out
    for d in RUNS.iterdir():
        if not d.is_dir():
            continue
        logs = sorted(d.glob("*.log"))
        latest = max([mtime(p) for p in logs + [d / "status.tsv"] if p.exists()] + [mtime(d)], key=lambda x: x or now())
        start = None
        for p in sorted(logs, key=lambda p: p.stat().st_mtime):
            try:
                start = datetime.fromisoformat(read(p).split("\n", 1)[0].strip())
                break
            except Exception:
                continue
        start = start or datetime.fromtimestamp(d.stat().st_ctime, KST)
        terminal = {r["dataset"]: r["state"] for r in parse_status(d / "status.tsv")}
        planned, script = planned_datasets(d.name)
        active_ds = next((p.stem for p in logs if p.stem not in terminal and (now() - (mtime(p) or now())).total_seconds() < 900), None)
        tail = sh(f"tail -c 4000 '{d / (active_ds + '.log')}' | grep -v '^$' | tail -1").strip()[:120] if active_ds else ""
        out.append(dict(id=d.name, start=start.isoformat(), latest=latest.isoformat(), terminal=terminal,
                        started=[p.stem for p in logs], planned=planned, script=script, active_ds=active_ds, tail=tail,
                        active=(now() - latest).total_seconds() < 900))
    out.sort(key=lambda r: r["latest"], reverse=True)
    return out


def automation():
    pats = [("웹 대시보드 :8765", "dashboard/server.py"), ("텔레그램 봇", "telegram.py bot")]
    ps = sh("ps -eo pid,etimes,args --no-headers")
    rows = []
    for label, pat in pats:
        hit = [l for l in ps.splitlines() if pat in l and "grep" not in l and "ssh" not in l]
        rows.append(dict(name=label, on=bool(hit), pid=int(hit[0].split()[0]) if hit else None, uptime=int(hit[0].split()[1]) if hit else None))
    t = mtime(ROOT / "dashboard" / "pipeline.log")
    rows.insert(0, dict(name="실험 파이프라인 (cron 1분)", on=bool(t and (now() - t).total_seconds() < 180), pid=None,
                        uptime=None, last=t.isoformat() if t else None))
    return rows


def git_log(n=30):
    if not (ROOT / ".git").exists():
        return None
    out = sh(f"git -C '{ROOT}' log -{n} --date=iso-strict --format='%h|%ad|%s'")
    ahead = sh(f"git -C '{ROOT}' rev-list --count origin/main..HEAD 2>/dev/null").strip()
    last_push = mtime(ROOT / ".git" / "refs" / "remotes" / "origin" / "main") or mtime(ROOT / ".git" / "FETCH_HEAD")
    return dict(head=sh(f"git -C '{ROOT}' rev-parse --short HEAD").strip(),
                head_full=sh(f"git -C '{ROOT}' rev-parse HEAD").strip(),
                origin_main=sh(f"git -C '{ROOT}' rev-parse --short origin/main 2>/dev/null").strip(),
                ahead=int(ahead) if ahead.isdigit() else None,
                dirty=int(sh(f"git -C '{ROOT}' status --porcelain | wc -l").strip() or 0),
                last_push=last_push.isoformat() if last_push else None,
                remote=sh(f"git -C '{ROOT}' remote get-url origin 2>/dev/null").strip(),
                total=int(sh(f"git -C '{ROOT}' rev-list --count HEAD 2>/dev/null").strip() or 0),
                commits=[dict(zip(("hash", "date", "msg"), l.split("|", 2))) for l in out.strip().splitlines() if l.count("|") >= 2])


def live_json(state, tasks, dry):
    paper = {}
    for key, t in tasks.items():
        n = task_stats(t)
        cols = value_cols(t)
        paper[key] = dict(title=TASK_LABEL[key][0], metric=t["metric"], cols=cols, total=n[0], agree=n[1], median=n[2], done=n[3],
                          rows={m: {d: t["rows"][m][d] for d in cols} for m in t["rows"]},
                          reference={m: {d: t["reference"].get(m, {}).get(d) for d in cols} for m in t["rows"]},
                          outliers=[dict(model=m, dataset=ds, value=c["value"], delta=c["delta"], ref=t["reference"].get(m, {}).get(ds)) for m, ds, c in n[4]])
    journals = sorted((LAB / "일지").glob("20*.md")) if (LAB / "일지").is_dir() else []
    latest_j = read(journals[-1], 3000) if journals else ""
    todo = [l for l in read(LAB / "다음 할 일.md").splitlines() if l.startswith("- [")]
    live = dict(generated_at=now().isoformat(), host=HOST, gpus=gpu_info(), jobs=jobs(), runs=run_dirs()[:12],
                automation=automation(), git=git_log(), agents=agent_status(), paper=paper,
                audit=state.get("audit"), updates=state.get("updates"),
                lab=dict(latest_journal=journals[-1].name if journals else None, latest_journal_text=latest_j,
                         todo=todo, questions=len([l for l in read(LAB / "질문.md").splitlines() if l.startswith("- [ ]")])))
    if not dry:
        LIVE.write_text(json.dumps(live, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    return True


# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-charts", action="store_true")   # 호환용, 무시
    args = ap.parse_args()
    dry = args.dry_run
    if not STATE.exists():
        print(f"state.json 없음: {STATE}", file=sys.stderr)
        return 1
    state, tasks = load_state()
    changed = 0
    changed += note_paper(state, tasks, dry)
    changed += note_models(tasks, dry)
    changed += note_datasets(tasks, dry)
    changed += note_agents(dry)
    changed += note_protocol_common(tasks, dry)
    changed += note_protocols(tasks, dry)
    seeded = seed_lab(dry)
    changed += note_home(tasks, dry)
    live_json(state, tasks, dry)
    print(f"{'변경될' if dry else '갱신된'} 노트 {changed}개 · lab 시드 {seeded}개 · live.json 갱신 · vault: {VAULT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
