#!/usr/bin/env python3
"""hgnn/vault/ — 옵시디언이 읽는 노트를 만든다. 서버에서 1분마다 돈다.

    python3 tools/vault_build.py            # vault/ 전체 갱신
    python3 tools/vault_build.py --dry-run  # 쓰지 않고 요약만
    python3 tools/vault_build.py --no-charts

읽는 곳
  dashboard/state.json                       clerk 원장 → 정식 20-seed 결과 + 논문 Δ (collector.py 가 만든다)
  .agents/env-status/full-runs/*/status.tsv  실행별 데이터셋 진행 상태
  .agents/run-scripts/*.sh                   실행 계획 (데이터셋 목록)
  .agents/*.md, .agents/env-status/, .agents/clerk-reports/   에이전트 정의·활동 흔적
  ps / nvidia-smi / git log                  살아 있는 프로세스, GPU, 커밋

쓰는 곳 (vault/)
  Home.md · 대시보드.md · 에이전트.md · 논문 대조.md · Charts.md · models/*.md · datasets/*.md
  모델 비교.base · 데이터셋 비교.base · assets/*.png

원칙
  - 구조(제목·표·목록·콜아웃)는 전부 마크다운으로 쓴다. CSS 스니펫이 없어도 읽혀야 한다.
  - 인라인 HTML 은 Δ 배지·상태 알약·진행 막대처럼 '없어도 글자로 읽히는' 장식에만 쓴다.
  - 콜아웃(`>`) 안에는 HTML 블록을 넣지 않는다. 옵시디언이 글자로 뿌린다.
  - 각 노트의 AUTO:BEGIN ~ AUTO:END 사이만 덮어쓴다. 그 아래 `## 메모` 는 보존된다.
  - 대시보드.md 는 매분 바뀌므로 git 에 넣지 않는다 (.gitignore). 로컬 PC 가 ssh 로 직접 받아간다.
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
STATE = ROOT / "dashboard" / "state.json"
RUNS = ROOT / ".agents" / "env-status" / "full-runs"
SCRIPTS = ROOT / ".agents" / "run-scripts"
ENV_STATUS = ROOT / ".agents" / "env-status"
CLERK_REPORTS = ROOT / ".agents" / "clerk-reports"
KST = timezone(timedelta(hours=9))
HOST = os.uname().nodename.split("-")[0] if hasattr(os, "uname") else "server"

AUTO_BEGIN = "<!-- AUTO:BEGIN -->"
AUTO_END = "<!-- AUTO:END -->"

# 원장 표기 → 논문 표기 (노트 이름은 논문 표기를 쓴다)
MODEL_ALIAS = {"GGD (H-GD)": "GGD", "H-GD (GGD)": "GGD", "HGD": "GGD", "H-GD": "GGD",
               "Hypeboy": "HypeBoy", "EDHNN": "ED-HNN", "SEHSSL": "SE-HSSL"}
# 논문 표기 → 레포 디렉토리 (프로세스 감지·링크용)
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
# 시간 · 셸
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


# --------------------------------------------------------------------------
# state.json → 구조화
# --------------------------------------------------------------------------
def parse_cell(text):
    """원장 셀 → dict(kind, ...). kind: val(수치) · lim(논문이 OOM/OOT) · na(미실행·보류)"""
    m = CELL_RE.search(text or "")
    if m:
        return dict(kind="val", value=float(m.group(1)), sd=float(m.group(2)),
                    delta=float(m.group(3).replace("−", "-")), text=text)
    t = (text or "").strip()
    low = t.lower()
    if "o.o.m" in low or "o.o.t" in low or "oom" in low or "oot" in low:
        return dict(kind="lim", label="OOM" if ("o.o.m" in low or "oom" in low) else "OOT",
                    text=t.lstrip("— ").strip())
    return dict(kind="na", reason=t.lstrip("— ").strip() or "미실행", text=t)


def load_state():
    s = json.loads(STATE.read_text(encoding="utf-8"))
    tasks = {}
    for t in s["tasks"]:
        header = t["header"][1:]
        rows = {}
        for r in t["rows"]:
            rows[MODEL_ALIAS.get(r[0], r[0])] = {ds: parse_cell(c) for ds, c in zip(header, r[1:])}
        ref = {MODEL_ALIAS.get(m, m): v for m, v in t.get("reference", {}).items()}
        tasks[t["key"]] = dict(header=header, rows=rows, reference=ref, metric=t["metric"])
    return s, tasks


def value_cols(task):
    """수치가 하나라도 있는 열만."""
    return [d for d in task["header"] if any(task["rows"][m][d]["kind"] == "val" for m in task["rows"])]


def task_stats(task):
    """(수치 셀 수, ±2 이내 수, |Δ| 중앙값, 완료 모델 수, 이상치 [(model, ds, cell)])"""
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
# 표기 — HTML 은 '없어도 글자로 읽히는' 장식에만
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
    """대조표 한 칸: 값 ±sd Δ / OOM / —"""
    if c["kind"] == "val":
        return f"{val(c)} {badge(c['delta'])}"
    if c["kind"] == "lim":
        return f'<span class="lim">{c["label"]}</span>'
    return "—"


def pill(text, kind=""):
    return f'<span class="pill {kind}">{text}</span>'


def bar(pct):
    return f'<span class="bar"><i style="width:{pct}%"></i></span> {pct}%'


def small(text):
    return f"<small>{text}</small>"


def stat_table(items):
    """카드 대신 쓰는 요약 표. (라벨, 큰 값, 설명)"""
    return "\n".join([
        "| " + " | ".join(k for k, _, _ in items) + " |",
        "|" + "---|" * len(items),
        "| " + " | ".join(f"**{v}**" for _, v, _ in items) + " |",
        "| " + " | ".join(small(n) for _, _, n in items) + " |",
    ])


def md_table(header, rows, align=None):
    align = align or ["---"] * len(header)
    out = ["| " + " | ".join(header) + " |", "|" + "|".join(align) + "|"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def callout(kind, title, body_lines, fold=True):
    """접이식 콜아웃. body 는 마크다운만 (HTML 블록 금지)."""
    out = [f"> [!{kind}]{'-' if fold else ''} {title}"]
    out += ["> " + l if l else ">" for l in body_lines]
    return "\n".join(out)


LEGEND = ("표기 · 값 <span class=\"sd\">±표준편차</span> · Δ = 우리 − 논문 · "
          f"{badge(0.3)} ±2 이내 · {badge(3.0)} 2–5 · {badge(7.0)} 5 초과 · "
          "<span class=\"lim\">OOM</span> 논문이 수치를 못 낸 칸 · — 미실행·보류")


def chart_block(labels, series, height=None):
    out = ["```chart", "type: bar", "labels: [" + ", ".join(labels) + "]", "series:"]
    for title, data in series:
        out += [f"  - title: {title}",
                "    data: [" + ", ".join("null" if v is None else f"{v:.1f}" for v in data) + "]"]
    out += ["tension: 0.2", "width: 100%", "labelColors: false", "fill: false",
            "beginAtZero: false", "legend: true", "stacked: false"]
    if height:
        out.append(f"height: {height}")
    out.append("```")
    return "\n".join(out)


# --------------------------------------------------------------------------
# 노트 쓰기
# --------------------------------------------------------------------------
VOLATILE_RE = re.compile(r"(갱신 |updated: )\d{4}-\d{2}-\d{2}[ T:\d]*")


def write_note(path, body, frontmatter=None, dry_run=False, volatile=False):
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
        if AUTO_BEGIN in tail and AUTO_END in tail:
            new = fm + block + tail.rsplit(AUTO_END, 1)[1]
        else:
            new = fm + block + "\n\n" + tail.lstrip()
    else:
        new = fm + block + "\n\n## 메모\n\n\n"
    if old is not None and not volatile and VOLATILE_RE.sub(r"\1<D>", old) == VOLATILE_RE.sub(r"\1<D>", new):
        return False
    if old == new:
        return False
    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(new, encoding="utf-8")
    return True


def front(kind, css=None, **kw):
    lines = [f"type: {kind}"]
    for k, v in kw.items():
        if isinstance(v, str) and not re.match(r"^[\w.\-]+$", v):
            v = '"' + v.replace('"', "'") + '"'
        lines.append(f"{k}: {v}")
    lines.append(f"updated: {stamp()}")
    tag = {"model": "hgnn/model", "dataset": "hgnn/dataset"}.get(kind, "hgnn/overview")
    lines.append(f"tags: [{tag}]")
    if css:
        lines.append(f"cssclasses: [{css}]")
    return lines


# --------------------------------------------------------------------------
# 1. 논문 대조
# --------------------------------------------------------------------------
def note_paper(state, tasks, dry):
    n3, n4 = task_stats(tasks["T3"]), task_stats(tasks["T4"])
    n5 = task_stats(tasks["T5"]) if "T5" in tasks else (0, 0, 0, 0, [])
    outs_all = len(n3[4]) + len(n4[4]) + len(n5[4])
    lines = ["# 논문 대조 — HyperGC Table 3·4·5", "",
             "clerk 원장의 정식 20-seed 결과를 KDD ’26 HyperGC 논문 표와 셀 단위로 대조한다. "
             f"Δ = 우리 평균 − 논문 평균. {small('갱신 ' + stamp())}", "",
             stat_table([("NC 일치율", f"{n3[1]}/{n3[0]}", f"±2 이내 · |Δ| 중앙값 {n3[2]:.2f}"),
                         ("HP 일치율", f"{n4[1]}/{n4[0]}", f"±2 이내 · |Δ| 중앙값 {n4[2]:.2f}"),
                         ("완료 모델", f"{n3[3]} · {n4[3]}", "NC / HP (19개 중)"),
                         ("이상치", f"{outs_all}", "|Δ| 3.0 초과 셀")]), ""]
    a = state.get("audit", {})
    if a.get("available"):
        lines += [f"> [!check] 원장의 Δ {a['checked']}칸을 `paper_reference.json`(HyperGC.pdf)과 대조 — "
                  f"일치 {a['agree']} · 불일치 {len(a['mismatch'])}", ""]
    lines += [LEGEND, ""]
    for key in ("T3", "T4", "T5"):
        if key not in tasks:
            continue
        t = tasks[key]; en, ko, metric, _, short = TASK_LABEL[key]
        cols = value_cols(t)
        lines += [f"## {en} — Table {key[1]} · {metric}", ""]
        if not cols:
            lines += ["정식 결과가 아직 없다. 원장에 등록된 모델: " + ", ".join(f"[[{m}]]" for m in sorted(t["rows"])), ""]
            continue
        rows = []
        for m in sorted(t["rows"], key=lambda m: (-sum(c["kind"] == "val" for c in t["rows"][m].values()), m)):
            rows.append([f"[[{m}]]"] + [cell(t["rows"][m][d]) for d in cols])
        lines += [md_table(["모델"] + cols, rows, ["---"] + ["---:"] * len(cols)), ""]
        empty = [d for d in t["header"] if d not in cols]
        if empty:
            lines += [small("표시하지 않은 열 (정식 결과 없음): " + ", ".join(empty)), ""]
    # 이상치 — 콜아웃 안은 마크다운 표만
    outs = []
    for key in ("T3", "T4", "T5"):
        if key in tasks:
            for m, ds, c in task_stats(tasks[key])[4]:
                ref = tasks[key]["reference"].get(m, {}).get(ds)
                outs.append((abs(c["delta"]), TASK_LABEL[key][4], m, ds, c, ref))
    outs.sort(key=lambda x: -x[0])
    body = []
    if outs:
        body += ["| 태스크 | 모델 | 데이터셋 | 우리 | 논문 | Δ |", "|---|---|---|---:|---:|---:|"]
        for _, tag, m, ds, c, ref in outs:
            refs = f"{ref:.1f}" if isinstance(ref, (int, float)) else "?"
            body.append(f"| {tag} | [[{m}]] | {ds} | {c['value']:.1f} | {refs} | {badge(c['delta'])} |")
    else:
        body.append("없음.")
    lines += [callout("warning", f"이상치 {len(outs)}개 — |Δ| 3.0 초과", body), ""]
    upd = state.get("updates", {})
    if upd.get("items"):
        lines += [callout("quote", f"원장의 최근 기록 — {upd.get('title', '')}",
                          [f"- {it}" for it in upd["items"][:8]]), ""]
    lines += [small("원본 `.agents/clerk-reports/experiment_now.md` → `dashboard/state.json` · 기준값 `dashboard/paper_reference.json`"),
              "", "관련: [[모델 비교]] · [[Charts]] · [[Home]]"]
    return write_note(VAULT / "논문 대조.md", "\n".join(lines),
                      front("overview", css="hg-wide, hg-sticky, wide-page, row-alt",
                            nc_agree=n3[1], nc_total=n3[0], hp_agree=n4[1], hp_total=n4[0], outliers=outs_all), dry)


# --------------------------------------------------------------------------
# 2. 모델 노트 · 3. 데이터셋 노트
# --------------------------------------------------------------------------
def note_models(state, tasks, dry):
    changed = 0
    for m in sorted({m for t in tasks.values() for m in t["rows"]}):
        per = {k: t["rows"][m] for k, t in tasks.items() if m in t["rows"]}
        props, stats = {}, []
        worst = None
        for key in ("T3", "T4", "T5"):
            if key not in per:
                continue
            vals = [c for c in per[key].values() if c["kind"] == "val"]
            short = TASK_LABEL[key][4].lower()
            if key != "T5":
                props[f"{short}_agree"] = sum(abs(c["delta"]) <= 2 for c in vals)
                props[f"{short}_done"] = len(vals)
                med = sorted(abs(c["delta"]) for c in vals)[len(vals) // 2] if vals else None
                stats.append((f"{TASK_LABEL[key][4]} 일치", f"{props[f'{short}_agree']}/{len(vals)}",
                              f"|Δ| 중앙값 {med:.2f}" if med is not None else "정식 결과 없음"))
            for ds, c in per[key].items():
                if c["kind"] == "val" and (worst is None or abs(c["delta"]) > abs(worst[2])):
                    worst = (key, ds, c["delta"])
        if worst:
            stats.append(("최대 편차", fmt_delta(worst[2]), f"{TASK_LABEL[worst[0]][1]} · {worst[1]}"))
        props["max_abs_delta"] = round(abs(worst[2]), 1) if worst else 0
        props["worst_cell"] = f"{TASK_LABEL[worst[0]][1]} {worst[1]} {fmt_delta(worst[2])}" if worst else ""
        nvals = props.get("nc_done", 0) + props.get("hp_done", 0)
        props["status"] = ("blocked" if nvals == 0 else
                           "complete" if props.get("nc_done", 0) >= 6 and props.get("hp_done", 0) >= 6 else "partial")
        d = MODEL_DIR.get(m, m)
        props["code_dir"] = d

        lines = [f"# {m}", "",
                 small(f"코드 `{d}/` · 결과 `results/result_*_{d}_*.txt` · 갱신 {stamp()}"), "",
                 stat_table(stats) if stats else "", ""]
        for key in ("T3", "T4", "T5"):
            if key not in per:
                continue
            en, ko, metric, _, short = TASK_LABEL[key]
            ref = tasks[key]["reference"].get(m, {})
            rows = []
            for ds in tasks[key]["header"]:
                c = per[key][ds]
                r = ref.get(ds)
                refs = f"{r:.1f}" if isinstance(r, (int, float)) else "—"
                if c["kind"] == "val":
                    rows.append([f"[[{ds}]]", val(c), refs, badge(c["delta"]), ""])
                elif c["kind"] == "lim":
                    rows.append([f"[[{ds}]]", '<span class="lim">' + c["label"] + "</span>", refs, "", c["text"]])
                else:
                    rows.append([f"[[{ds}]]", "—", refs, "", c["reason"]])
            lines += [f"## {en} — Table {key[1]} · {metric}", "",
                      md_table(["데이터셋", "우리", "논문", "Δ", "비고"], rows, ["---", "---:", "---:", "---:", "---"]), ""]
            cds = [ds for ds in tasks[key]["header"] if per[key][ds]["kind"] == "val"]
            if len(cds) >= 2:
                lines += [chart_block(cds, [("우리", [per[key][ds]["value"] for ds in cds]),
                                            ("논문", [ref.get(ds) if isinstance(ref.get(ds), (int, float)) else None for ds in cds])],
                                      height="220px"), ""]
        lines += [LEGEND, "", "관련: [[논문 대조]] · [[모델 비교]] · [[Home]]"]
        if write_note(VAULT / "models" / f"{m}.md", "\n".join(lines),
                      front("model", css="hg-model, row-alt", **props), dry):
            changed += 1
    return changed


def note_datasets(state, tasks, dry):
    changed = 0
    datasets = []
    for t in tasks.values():
        for d in t["header"]:
            if d not in datasets:
                datasets.append(d)
    for ds in datasets:
        props = {}
        lines = [f"# {ds}", "", small(f"갱신 {stamp()}"), ""]
        for key in ("T3", "T4", "T5"):
            t = tasks.get(key)
            if not t or ds not in t["header"]:
                continue
            en, ko, metric, _, short = TASK_LABEL[key]
            rows = [(m, t["rows"][m][ds]) for m in t["rows"]]
            vals = sorted([(m, c) for m, c in rows if c["kind"] == "val"], key=lambda x: -x[1]["value"])
            others = [(m, c) for m, c in rows if c["kind"] != "val"]
            if not vals and not others:
                continue
            lines += [f"## {en} — {metric}", ""]
            if vals:
                props[f"{short.lower()}_models"] = len(vals)
                props[f"{short.lower()}_best"] = vals[0][0]
                props[f"{short.lower()}_best_value"] = round(vals[0][1]["value"], 1)
                trows = []
                for i, (m, c) in enumerate(vals, 1):
                    r = t["reference"].get(m, {}).get(ds)
                    refs = f"{r:.1f}" if isinstance(r, (int, float)) else "—"
                    trows.append([i, f"[[{m}]]", val(c), refs, badge(c["delta"])])
                lines += [md_table(["#", "모델", "우리", "논문", "Δ"], trows, ["---:", "---", "---:", "---:", "---:"]), ""]
                if len(vals) >= 2:
                    refs_ = [t["reference"].get(m, {}).get(ds) for m, _ in vals]
                    lines += [chart_block([m for m, _ in vals],
                                          [("우리", [c["value"] for _, c in vals]),
                                           ("논문", [r if isinstance(r, (int, float)) else None for r in refs_])],
                                          height="260px"), ""]
            else:
                lines += ["정식 결과 없음.", ""]
            if others:
                lines += [small("미실행·보류: " + ", ".join(f"{m} ({c.get('label') or c.get('reason')})" for m, c in others)), ""]
        lines += ["관련: [[논문 대조]] · [[데이터셋 비교]] · [[Home]]"]
        if write_note(VAULT / "datasets" / f"{ds}.md", "\n".join(lines),
                      front("dataset", css="row-alt", **props), dry):
            changed += 1
    return changed


# --------------------------------------------------------------------------
# 4. 대시보드 — 살아 있는 것들
# --------------------------------------------------------------------------
def gpu_info():
    gpus = []
    for line in sh("nvidia-smi --query-gpu=index,name,utilization.gpu,memory.used,memory.total,uuid --format=csv,noheader,nounits").strip().splitlines():
        p = [x.strip() for x in line.split(",")]
        if len(p) >= 6:
            gpus.append(dict(index=int(p[0]), name=p[1].replace("NVIDIA GeForce ", ""), util=int(p[2]),
                             used=int(p[3]), total=int(p[4]), uuid=p[5], pids=[]))
    for line in sh("nvidia-smi --query-compute-apps=pid,gpu_uuid,used_memory --format=csv,noheader,nounits").strip().splitlines():
        p = [x.strip() for x in line.split(",")]
        if len(p) >= 2:
            for g in gpus:
                if g["uuid"] == p[1]:
                    g["pids"].append(int(p[0]))
    return gpus


def jobs():
    """모델 코드를 돌리고 있는 python 프로세스."""
    found = []
    for line in sh("ps -eo pid,etimes,args --no-headers").splitlines():
        parts = line.strip().split(None, 2)
        if len(parts) < 3:
            continue
        pid, et, args = int(parts[0]), int(parts[1]), parts[2]
        if "python" not in args or ".py" not in args or "conda run" in args:
            continue
        if any(x in args for x in ("dashboard/", "tools/", "run-scripts/", "vscode")):
            continue
        model = next((DIR_TO_MODEL[d.lower()] for d in MODEL_DIR.values()
                      if re.search(rf"(^|[\s/]){re.escape(d)}/", args)), None)
        if not model:
            continue
        m = re.search(r"--(?:dataset|data)[= ]([\w-]+)", args)
        t = re.search(r"--task[= ](\w+)", args)
        g = re.search(r"--(?:gpu|device|cuda)[= ](\d+)", args) or re.search(r"CUDA_VISIBLE_DEVICES=(\d+)", args)
        s = re.search(r"--num_seeds[= ](\d+)", args) or re.search(r"--seeds?[= ](\d+)", args)
        found.append(dict(pid=pid, elapsed=et, model=model,
                          dataset=DATASET_ALIAS.get(m.group(1), m.group(1)) if m else "?",
                          task=t.group(1) if t else "?", gpu=g.group(1) if g else "?", seeds=s.group(1) if s else "?"))
    return found


def planned_datasets(run_id):
    if not SCRIPTS.is_dir():
        return None
    for p in SCRIPTS.glob("*.sh"):
        try:
            txt = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
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
    return None


def parse_status(path):
    """status.tsv 형식 셋: (model ds STATE time) · (model ds code) · (ds code)"""
    rows = []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return rows
    for line in lines:
        p = line.rstrip("\n").split("\t")
        if len(p) == 1:
            p = line.split()
        if not p or not p[0]:
            continue
        state = ds = None
        if len(p) >= 3:
            ds, state = p[1], p[2]
        elif len(p) == 2:
            ds, state = p
        if state and state.isdigit():
            state = {"0": "COMPLETE", "124": "OOT"}.get(state, f"FAILED({state})")
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
                start = datetime.fromisoformat(p.read_text(encoding="utf-8", errors="replace").split("\n", 1)[0].strip())
                break
            except Exception:
                continue
        start = start or datetime.fromtimestamp(d.stat().st_ctime, KST)
        terminal = {r["dataset"]: r["state"] for r in parse_status(d / "status.tsv") if r["dataset"]}
        plan = planned_datasets(d.name)
        planned, script = plan if plan else (None, None)
        active_ds = None
        for p in logs:
            if p.stem not in terminal and (now() - (mtime(p) or now())).total_seconds() < 900:
                active_ds = p.stem
        tail = sh(f"tail -c 4000 '{d / (active_ds + '.log')}' | grep -v '^$' | tail -1").strip()[:110] if active_ds else ""
        out.append(dict(id=d.name, start=start, latest=latest, terminal=terminal, started=[p.stem for p in logs],
                        planned=planned, script=script, active_ds=active_ds, tail=tail,
                        active=(now() - latest).total_seconds() < 900))
    out.sort(key=lambda r: r["latest"], reverse=True)
    return out


def automation():
    pats = [("clerk 갱신 루프 (10분)", "clerk-refresh-loop.sh"), ("collector 루프 (5분)", "dashboard/collector.py"),
            ("웹 대시보드 :8765", "dashboard/server.py"), ("pixel bridge", "dashboard/pixel_bridge.py")]
    ps = sh("ps -eo pid,etimes,args --no-headers")
    rows = []
    for label, pat in pats:
        hit = [l for l in ps.splitlines() if pat in l and "grep" not in l and "ssh" not in l]
        if hit:
            p = hit[0].split(None, 2)
            rows.append((label, True, f"PID {p[0]} · {dur(int(p[1]))}"))
        else:
            rows.append((label, False, "—"))
    t = mtime(VAULT / ".sync.log")
    ok = bool(t and (now() - t).total_seconds() < 180)
    rows.append(("vault 동기화 (cron 1분)", ok, f"마지막 {ago(t)}" if t else "—"))
    return rows


def git_log(n=10):
    if not (ROOT / ".git").exists():
        return None, []
    head = sh(f"git -C '{ROOT}' rev-parse --short HEAD").strip()
    out = sh(f"git -C '{ROOT}' log -{n} --date=format:'%m-%d %H:%M' --format='%h|%ad|%s'")
    rows = [l.split("|", 2) for l in out.strip().splitlines() if l.count("|") >= 2]
    return dict(head=head, dirty=sh(f"git -C '{ROOT}' status --porcelain | wc -l").strip(),
                remote=sh(f"git -C '{ROOT}' remote get-url origin 2>/dev/null").strip()), rows


def state_pill(state):
    s = state.upper()
    if s.startswith("COMPLETE") or "SKIP_EXISTING" in s or "ALREADY" in s:
        return pill(state, "ok")
    if "OOM" in s or "OOT" in s or "SKIP" in s:
        return pill(state, "lim")
    if "FAIL" in s:
        return pill(state, "bad")
    return pill(state)


def note_dashboard(dry):
    t0 = now()
    gpus, live, runs = gpu_info(), jobs(), run_dirs()
    active = [r for r in runs if r["active"]]
    done24 = sum(1 for r in runs for st in r["terminal"].values()
                 if st.startswith("COMPLETE") and r["latest"] and (t0 - r["latest"]).days < 1)

    lines = [f"# 실험 대시보드 — {HOST}", "",
             f'<span class="live"><i></i></span>{t0.strftime("%Y-%m-%d %H:%M:%S")} KST · 1분마다 갱신', "",
             stat_table([("실행 중", str(len(live)), "모델 코드를 돌리는 python"),
                         ("활성 실행", str(len(active)), "15분 내 로그가 움직인 run"),
                         ("GPU", " · ".join(f"{g['util']}%" for g in gpus) or "—",
                          " · ".join(f"{g['used'] / 1024:.1f}/{g['total'] / 1024:.0f} GB" for g in gpus) or "nvidia-smi 없음"),
                         ("24h 완료", str(done24), "status.tsv COMPLETE")]), ""]

    rows = [[g["index"], g["name"], bar(g["util"]), f"{g['used']} / {g['total']} MiB",
             ", ".join(str(p) for p in g["pids"]) or small("유휴")] for g in gpus]
    lines += ["## GPU", "", md_table(["#", "모델", "사용률", "메모리", "프로세스"], rows or [["—", "nvidia-smi 응답 없음", "", "", ""]],
                                     ["---:", "---", "---", "---:", "---"]), ""]

    lines += ["## 진행 중 실험", ""]
    if not live and not active:
        lines += ["지금 돌아가는 실험이 없다.", ""]
    if live:
        rows = [[j["pid"], f"[[{j['model']}]]", j["dataset"], j["task"], j["gpu"], j["seeds"], dur(j["elapsed"])]
                for j in sorted(live, key=lambda x: -x["elapsed"])]
        lines += [md_table(["PID", "모델", "데이터셋", "태스크", "GPU", "seeds", "경과"], rows,
                           ["---:", "---", "---", "---", "---:", "---:", "---:"]), ""]
    for r in active:
        total = len(r["planned"]) if r["planned"] else None
        done = sum(1 for s in r["terminal"].values() if s.startswith("COMPLETE") or "SKIP" in s.upper())
        failed = sum(1 for s in r["terminal"].values() if any(k in s.upper() for k in ("FAIL", "OOM", "OOT")))
        pct = int(100 * done / total) if total else None
        lines += [f"### {r['id']}", "",
                  small(f"시작 {r['start'].strftime('%m-%d %H:%M')} · 경과 {dur((t0 - r['start']).total_seconds())} · "
                        f"마지막 로그 {ago(r['latest'])}" + (f" · `{r['script']}`" if r["script"] else "")), "",
                  (f"진행 {done}/{total} {bar(pct)}" if total else f"완료 {done}") + (f" · 실패 {failed}" if failed else ""), ""]
        if r["planned"]:
            rows = []
            for ds in r["planned"]:
                st = r["terminal"].get(ds)
                if st:
                    p = state_pill(st)
                elif ds == r["active_ds"]:
                    p = pill("RUNNING", "run")
                elif ds in r["started"]:
                    p = pill("STARTED")
                else:
                    p = pill("대기", "wait")
                rows.append([DATASET_ALIAS.get(ds, ds), p])
            lines += [md_table(["데이터셋", "상태"], rows), ""]
        if r["active_ds"] and r["tail"]:
            lines += [f"`{r['active_ds']}.log` 마지막 줄:", "", "```", r["tail"], "```", ""]

    body = ["| 실행 | 시작 | 마지막 활동 | 결과 |", "|---|---|---|---|"]
    for r in runs[:10]:
        summ = defaultdict(int)
        for s in r["terminal"].values():
            k = ("완료" if s.startswith("COMPLETE") or "SKIP" in s.upper()
                 else "OOM/OOT" if ("OOM" in s.upper() or "OOT" in s.upper()) else "실패")
            summ[k] += 1
        res = " · ".join(f"{k} {v}" for k, v in summ.items()) or "기록 없음"
        flag = " " + pill("활성", "run") if r["active"] else ""
        body.append(f"| `{r['id']}`{flag} | {r['start'].strftime('%m-%d %H:%M')} | {ago(r['latest'])} | {res} |")
    lines += [callout("info", "최근 실행 — full-runs 최신 10개", body), ""]

    rows = [[label, pill("on", "ok") if ok else pill("off", "bad"), info] for label, ok, info in automation()]
    lines += ["## 자동화 프로세스", "", md_table(["이름", "상태", "가동"], rows), ""]

    ginfo, commits = git_log()
    lines += ["## 커밋", ""]
    if ginfo is None:
        lines += ["아직 git 저장소가 아니다.", ""]
    else:
        lines += [small(f"HEAD `{ginfo['head']}` · 작업트리 변경 {ginfo['dirty']}건 · origin `{ginfo['remote'] or '미설정'}`"), "",
                  md_table(["커밋", "시각", "메시지"], [[f"`{h}`", d, msg] for h, d, msg in commits]), ""]
    lines += ["관련: [[에이전트]] · [[논문 대조]] · [[Home]]"]
    return write_note(VAULT / "대시보드.md", "\n".join(lines),
                      front("overview", css="hg-wide, wide-page", host=HOST,
                            running=len(live), active_runs=len(active)), dry, volatile=True)


# --------------------------------------------------------------------------
# 5. 에이전트
# --------------------------------------------------------------------------
AGENTS = [
    dict(name="clerk", file=".agents/clerk.md", short="결과 원장 관리",
         role="정식 20-seed 실행이 끝나면 `experiment_now.md` 에 값과 논문 Δ를 기록하고, 한글 보고서(개별/통합)를 쓴다. smoke 결과는 표에 올리지 않는다.",
         inputs="`results/` · `full-runs/status.tsv` · `paper_reference.json`",
         outputs="`clerk-reports/experiment_now.md` · `개별/` · `통합/` · `README.md`",
         process="clerk-refresh-loop.sh", activity=["clerk-reports/experiment_now.md", "clerk-reports/개별"]),
    dict(name="env-builder", file=".agents/env-builder.md", short="Conda 환경 구축",
         role="모델별 Conda 환경을 만들고 유지한다. 모델 코드는 건드리지 않고 환경 변경과 차단 요인을 기록한다. HyperGCL 은 다른 모델이 모두 끝난 뒤에만.",
         inputs="`*_require.txt` · env-checker 피드백",
         outputs="`env-status/env-builder.md` · `edge-builder-report.md`",
         process=None, activity=["env-status/env-builder.md", "env-status/edge-builder-report.md"]),
    dict(name="env-checker", file=".agents/env-checker.md", short="환경·모델 검증",
         role="env-builder 가 준비한 환경에서 모델을 검증한다. import → 1-seed 15-epoch smoke → 논문값과 대략 비교. 정식 실행의 게이트 파일(`*-check.ok`)을 만든다.",
         inputs="`env-status/` 빌더 핸드오프 · `time_node.sh`",
         outputs="`env-status/checker-*.md` · `edge-checker-report.md` · `*-check.ok`",
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


def note_agents(dry):
    t0 = now()
    ps = sh("ps -eo pid,etimes,args --no-headers")
    summary = []
    for a in AGENTS:
        proc = None
        if a["process"]:
            hit = [l for l in ps.splitlines() if a["process"] in l and "grep" not in l]
            if hit:
                p = hit[0].split(None, 2)
                proc = (int(p[0]), int(p[1]))
        act = latest_activity(a["activity"])
        age = (t0 - act[0]).total_seconds() if act else None
        if proc:
            state, kind, ctype, why = "활성", "ok", "success", "루프 프로세스가 돌고 있다"
        elif age is not None and age < 3600:
            state, kind, ctype, why = "활성", "ok", "success", "1시간 내 산출물 갱신"
        elif age is not None and age < 86400:
            state, kind, ctype, why = "대기", "wait", "note", "24시간 내 활동, 지금은 호출되지 않음"
        else:
            state, kind, ctype, why = "비활성", "bad", "failure", "24시간 넘게 산출물 변화 없음"
        summary.append((a, state, kind, ctype, why, proc, act))

    lines = [f"# 에이전트 — {HOST}", "",
             small(f"정의서 `.agents/*.md` · 상태는 프로세스와 산출물 파일의 시각에서 읽는다 · 갱신 {stamp()}"), "",
             md_table(["에이전트", "역할", "상태", "마지막 활동"],
                      [[f"[[#{a['name']}\\|{a['name']}]]", a["short"], pill(state, kind),
                        act[0].strftime("%m-%d %H:%M") if act else "—"] for a, state, kind, _, _, _, act in summary]), ""]

    runs = run_dirs()[:6]
    rows = []
    for r in runs:
        txt = ""
        if r["script"]:
            try:
                txt = (SCRIPTS / r["script"]).read_text(encoding="utf-8", errors="replace")
            except OSError:
                pass
        rows.append([f"`{r['id']}`" + (" " + pill("활성", "run") if r["active"] else ""),
                     "결과 기록" if r["terminal"] else "대기",
                     "게이트 검사" if "check.ok" in txt else ("smoke" if "smoke" in r["id"] else "—"),
                     "환경 제공" if "conda run" in txt else "—"])
    lines += ["## 최근 실행과의 관계", "", md_table(["실행", "clerk", "env-checker", "env-builder"], rows), ""]

    for a, state, kind, ctype, why, proc, act in summary:
        lines += ["---", "", f"## {a['name']}", "",
                  f"> [!{ctype}] {state} — {why}", "",
                  a["role"], "",
                  md_table(["항목", "내용"], [
                      ["정의서", f"`{a['file']}`"],
                      ["입력", a["inputs"]],
                      ["출력", a["outputs"]],
                      ["상주 프로세스", (f"`{a['process']}` · PID {proc[0]} · 시작 {(t0 - timedelta(seconds=proc[1])).strftime('%m-%d %H:%M')}"
                                    if proc else (f"`{a['process']}` (지금은 꺼짐)" if a["process"] else "없음 — Claude 세션이 필요할 때 호출"))],
                      ["마지막 활동", f"{act[0].strftime('%m-%d %H:%M')} · `{act[1]}`" if act else "—"],
                  ]), ""]
        if a["name"] == "clerk":
            reports = sorted((CLERK_REPORTS / "개별").glob("*.md"))[-5:] if (CLERK_REPORTS / "개별").is_dir() else []
            if reports:
                lines += ["최근 보고서", ""] + [f"- `{p.name}`" for p in reversed(reports)] + [""]
        if a["name"] == "env-checker":
            oks = sorted(ENV_STATUS.glob("*.ok"))
            if oks:
                lines += ["게이트 파일: " + " · ".join(f"`{p.name}` ({mtime(p).strftime('%m-%d %H:%M')})" for p in oks), ""]
    lines += ["관련: [[대시보드]] · [[Home]]"]
    return write_note(VAULT / "에이전트.md", "\n".join(lines),
                      front("overview", css="row-alt", host=HOST), dry)


# --------------------------------------------------------------------------
# 6. 차트 (PNG) · Charts.md · Home · Bases
# --------------------------------------------------------------------------
def charts(tasks, dry):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.colors import LinearSegmentedColormap
        from matplotlib.font_manager import findfont, FontProperties
    except Exception:
        return 0
    BLUE = ["#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7", "#3987e5",
            "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b"]
    THEME = {"light": dict(surface="#fcfcfb", ink="#0b0b0b", ink2="#52514e", empty="#f0efec", ramp=BLUE, hi="#ffffff", lo="#0b0b0b"),
             "dark": dict(surface="#1a1a19", ink="#ffffff", ink2="#c3c2b7", empty="#2a2a28", ramp=BLUE[::-1], hi="#0b0b0b", lo="#ffffff")}
    for name in ("Noto Sans CJK KR", "Noto Serif CJK KR", "Noto Sans CJK SC", "NanumGothic", "Malgun Gothic"):
        try:
            findfont(FontProperties(family=name), fallback_to_default=False)
            plt.rcParams["font.family"] = name
            break
        except Exception:
            continue
    plt.rcParams["axes.unicode_minus"] = False
    assets = VAULT / "assets"
    if not dry:
        assets.mkdir(parents=True, exist_ok=True)
    made = 0
    for key in ("T3", "T4"):
        t = tasks[key]; en, _, _, short, _ = TASK_LABEL[key]
        ds = value_cols(t)
        mdl = [m for m in t["rows"] if any(t["rows"][m][d]["kind"] == "val" for d in ds)]
        if not ds or not mdl:
            continue
        v = {(m, d): t["rows"][m][d]["value"] for m in mdl for d in ds if t["rows"][m][d]["kind"] == "val"}
        mdl.sort(key=lambda m: -sum(v[(m, d)] for d in ds if (m, d) in v) / max(1, sum((m, d) in v for d in ds)))
        for mode, th in THEME.items():
            cmap = LinearSegmentedColormap.from_list("b", th["ramp"])
            fig, ax = plt.subplots(figsize=(1.15 * len(ds) + 3.6, 0.36 * len(mdl) + 1.9))
            fig.patch.set_facecolor(th["surface"]); ax.set_facecolor(th["surface"])
            for s in ax.spines.values():
                s.set_visible(False)
            ax.tick_params(colors=th["ink2"], length=0, labelsize=9)
            rng = {d: (min(v[(m, d)] for m in mdl if (m, d) in v), max(v[(m, d)] for m in mdl if (m, d) in v)) for d in ds}
            for i, m in enumerate(mdl):
                for j, d in enumerate(ds):
                    x = v.get((m, d))
                    if x is None:
                        ax.add_patch(plt.Rectangle((j + .01, i + .01), .98, .98, facecolor=th["empty"], edgecolor="none"))
                        ax.text(j + .5, i + .5, "—", ha="center", va="center", color=th["ink2"], fontsize=8)
                        continue
                    lo, hi = rng[d]; f = .5 if hi == lo else (x - lo) / (hi - lo)
                    ax.add_patch(plt.Rectangle((j + .01, i + .01), .98, .98, facecolor=cmap(f), edgecolor="none"))
                    ax.text(j + .5, i + .5, f"{x:.1f}", ha="center", va="center", fontsize=8.5, color=th["hi"] if f > .55 else th["lo"])
            ax.set_xlim(0, len(ds)); ax.set_ylim(0, len(mdl))
            ax.set_xticks([j + .5 for j in range(len(ds))]); ax.set_xticklabels(ds, rotation=30, ha="right")
            ax.set_yticks([i + .5 for i in range(len(mdl))]); ax.set_yticklabels(mdl)
            ax.invert_yaxis(); ax.xaxis.set_ticks_position("top")
            ax.set_title(f"{en}\n색 = 각 열 안에서의 상대 위치 · 숫자 = 실제 값", color=th["ink"], fontsize=12, loc="left", pad=16, linespacing=1.6)
            fig.tight_layout()
            if not dry:
                fig.savefig(assets / f"{short}-heatmap-{mode}.png", dpi=170, facecolor=th["surface"])
            plt.close(fig); made += 1
    return made


def note_charts(tasks, dry):
    lines = ["# 차트", "", small(f"clerk 원장의 정식 결과 · 막대에 마우스를 올리면 값이 보인다 · 갱신 {stamp()}"), ""]
    for key in ("T3", "T4"):
        t = tasks[key]; en, _, metric, short, _ = TASK_LABEL[key]
        ds = value_cols(t)
        mdl = [m for m in t["rows"] if any(t["rows"][m][d]["kind"] == "val" for d in ds)]
        if not mdl:
            continue

        def mean_of(m, src):
            vals = [src(m, d) for d in ds]
            vals = [x for x in vals if isinstance(x, (int, float))]
            return sum(vals) / len(vals) if vals else None
        ours = {m: mean_of(m, lambda m, d: t["rows"][m][d]["value"] if t["rows"][m][d]["kind"] == "val" else None) for m in mdl}
        refs = {m: mean_of(m, lambda m, d: t["reference"].get(m, {}).get(d) if t["rows"][m][d]["kind"] == "val" else None) for m in mdl}
        mdl.sort(key=lambda m: -(ours[m] or 0))
        lines += [f"## {en} — {metric} · 데이터셋 {len(ds)}개 평균", "",
                  chart_block(mdl, [("우리", [ours[m] for m in mdl]), ("논문", [refs[m] for m in mdl])], height="320px"), ""]
        if (VAULT / "assets" / f"{short}-heatmap-light.png").exists():
            lines += [callout("note", "데이터셋별 히트맵 (PNG)",
                              [f"![[{short}-heatmap-light.png]]", "", "다크 테마에서는 같은 이름의 `-dark.png` 를 쓰면 된다."]), ""]
    lines += ["관련: [[논문 대조]] · [[모델 비교]] · [[Home]]"]
    return write_note(VAULT / "Charts.md", "\n".join(lines), front("overview", css="hg-wide, wide-page"), dry)


def note_home(tasks, dry):
    models = sorted({m for t in tasks.values() for m in t["rows"]})
    datasets = []
    for t in tasks.values():
        for d in t["header"]:
            if d not in datasets:
                datasets.append(d)
    lines = ["# HGNN 실험 노트", "",
             small(f"{HOST} 가 만들고 GitHub 를 거쳐 여기로 온다 · 갱신 {stamp()}"), "",
             "## 지금", "",
             "- [[대시보드]] — 실행 중 실험 · GPU · 최근 실행 · 자동화 · 커밋 (1분 갱신)",
             "- [[에이전트]] — clerk / env-builder / env-checker 역할과 활성 상태", "",
             "## 결과", "",
             "- [[논문 대조]] — HyperGC Table 3·4·5 vs 우리 정식 결과",
             "- [[모델 비교]] — 모델 19개를 일치율·편차로 정렬·필터 (Bases)",
             "- [[데이터셋 비교]] — 데이터셋별 1위 모델 (Bases)",
             "- [[Charts]] — 태스크별 순위 차트", "",
             "## 모델", ""] + [f"- [[{m}]]" for m in models] + ["", "## 데이터셋", ""] + [f"- [[{d}]]" for d in datasets]
    lines += ["", "## 어떻게 갱신되나", "",
              md_table(["무엇", "누가", "경로"], [
                  ["원장·Δ", "clerk (10분 루프) → `collector.py` (5분)", "`experiment_now.md` → `state.json`"],
                  ["이 노트들", "`tools/vault_build.py` (cron 1분)", "`vault/`"],
                  ["로컬 PC 로", "서버가 변경 시 git push → PC 가 1분마다 pull · 대시보드는 ssh", "`hgnn_sync.ps1`"]]), "",
              "> 각 노트의 자동 생성 구간(AUTO 주석 사이)만 덮어쓴다. **`## 메모`** 는 보존된다."]
    return write_note(VAULT / "Home.md", "\n".join(lines), front("home", css="hg-home"), dry)


BASES = {
    "모델 비교.base": """filters:
  and:
    - file.inFolder("hgnn/models")
properties:
  file.name:
    displayName: 모델
  nc_agree:
    displayName: NC 일치
  nc_done:
    displayName: NC 완료
  hp_agree:
    displayName: HP 일치
  hp_done:
    displayName: HP 완료
  max_abs_delta:
    displayName: 최대 |Δ|
  worst_cell:
    displayName: 최대 편차 위치
  status:
    displayName: 상태
  code_dir:
    displayName: 코드
views:
  - type: table
    name: 전체
    order:
      - file.name
      - status
      - nc_agree
      - nc_done
      - hp_agree
      - hp_done
      - max_abs_delta
      - worst_cell
    sort:
      - property: max_abs_delta
        direction: DESC
  - type: table
    name: 편차 5 초과
    filters:
      and:
        - max_abs_delta > 5
    order:
      - file.name
      - max_abs_delta
      - worst_cell
      - nc_agree
      - hp_agree
    sort:
      - property: max_abs_delta
        direction: DESC
  - type: table
    name: 미완료
    filters:
      and:
        - status != "complete"
    order:
      - file.name
      - status
      - nc_done
      - hp_done
  - type: cards
    name: 카드
    order:
      - file.name
      - status
      - nc_agree
      - hp_agree
      - max_abs_delta
""",
    "데이터셋 비교.base": """filters:
  and:
    - file.inFolder("hgnn/datasets")
properties:
  file.name:
    displayName: 데이터셋
  nc_models:
    displayName: NC 모델 수
  nc_best:
    displayName: NC 1위
  nc_best_value:
    displayName: NC 1위 값
  hp_models:
    displayName: HP 모델 수
  hp_best:
    displayName: HP 1위
  hp_best_value:
    displayName: HP 1위 값
views:
  - type: table
    name: 전체
    order:
      - file.name
      - nc_models
      - nc_best
      - nc_best_value
      - hp_models
      - hp_best
      - hp_best_value
    sort:
      - property: nc_models
        direction: DESC
""",
}


def note_bases(dry):
    changed = 0
    for name, body in BASES.items():
        p = VAULT / name
        if p.exists() and p.read_text(encoding="utf-8") == body:
            continue
        if not dry:
            p.write_text(body, encoding="utf-8")
        changed += 1
    return changed


# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-charts", action="store_true")
    args = ap.parse_args()
    dry = args.dry_run
    if not STATE.exists():
        print(f"state.json 없음: {STATE}", file=sys.stderr)
        return 1
    state, tasks = load_state()
    changed = 0
    changed += note_paper(state, tasks, dry)
    changed += note_models(state, tasks, dry)
    changed += note_datasets(state, tasks, dry)
    n_charts = 0 if args.no_charts else charts(tasks, dry)
    changed += note_charts(tasks, dry)
    changed += note_bases(dry)
    changed += note_agents(dry)
    changed += note_home(tasks, dry)
    dash = note_dashboard(dry)
    print(f"{'변경될' if dry else '갱신된'} 노트 {changed}개 (+대시보드 {'갱신' if dash else '동일'}) · 차트 {n_charts}장 · vault: {VAULT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
