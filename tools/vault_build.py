#!/usr/bin/env python3
"""hgnn/vault/ — 옵시디언이 읽는 노트를 만든다. 서버에서 1분마다 돈다.

    python3 tools/vault_build.py            # vault/ 전체 갱신
    python3 tools/vault_build.py --dry-run  # 쓰지 않고 요약만

읽는 곳
  dashboard/state.json                     clerk 원장 → 정식 20-seed 결과 + 논문 Δ (collector.py 가 만든다)
  .agents/env-status/full-runs/*/status.tsv  실행별 데이터셋 진행 상태
  .agents/run-scripts/*.sh                 실행 계획 (데이터셋 목록)
  .agents/*.md, .agents/env-status/, .agents/clerk-reports/   에이전트 정의·활동 흔적
  ps / nvidia-smi / git log                살아 있는 프로세스, GPU, 커밋

쓰는 곳 (vault/)
  Home.md · 대시보드.md · 에이전트.md · 논문 대조.md · models/*.md · datasets/*.md · assets/*.png

각 노트의 AUTO:BEGIN ~ AUTO:END 사이만 덮어쓴다. 그 아래 `## 메모` 는 보존된다.
대시보드.md 는 매분 바뀌므로 git 에 넣지 않는다 (.gitignore). 로컬 PC 가 ssh 로 직접 받아간다.
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
# 원시 데이터셋 이름 → 논문 표기
DATASET_ALIAS = {"citeseer_cite": "Citeseer", "cora_coauth": "Cora-CA", "imdb": "IMDB",
                 "house": "House", "pubmed_cite": "Pubmed", "aminer": "AMiner",
                 "dblp_copub": "DBLP-A", "dblp_coauth": "DBLP-A", "dblp_p": "DBLP-P",
                 "modelnet_40": "MN-40", "news": "20News", "cora_cite": "Cora"}
TASK_LABEL = {"T3": ("Node classification", "노드 분류", "Accuracy", "node"),
              "T4": ("Hyperedge prediction", "하이퍼엣지 예측", "AUROC", "edge"),
              "T5": ("Community detection", "커뮤니티 탐지", "NMI", "cluster")}

# 노트 안 인라인 HTML 은 로컬 .obsidian/snippets/hgnn.css 가 색을 입힌다.
CELL_RE = re.compile(r"\*\*([-\d.]+)\s*±\s*([-\d.]+)\*\*\s*\(Δ\s*\*\*([−+\-]?[\d.]+)\*\*\)")


def now():
    return datetime.now(KST)


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
        return subprocess.run(cmd, shell=True, capture_output=True, text=True,
                              timeout=timeout).stdout
    except Exception:
        return ""


# --------------------------------------------------------------------------
# state.json → 구조화
# --------------------------------------------------------------------------
def parse_cell(text):
    """원장 셀 → dict(kind, value, sd, delta, text).
    kind: val(수치) · lim(논문이 OOM/OOT 로 보고) · na(미실행·보류·차단)"""
    m = CELL_RE.search(text or "")
    if m:
        d = float(m.group(3).replace("−", "-"))
        return dict(kind="val", value=float(m.group(1)), sd=float(m.group(2)), delta=d, text=text)
    t = (text or "").strip()
    low = t.lower()
    if "o.o.m" in low or "o.o.t" in low or "oom" in low or "oot" in low:
        label = "OOM" if "o.o.m" in low or "oom" in low else "OOT"
        return dict(kind="lim", label=label, text=t.lstrip("— ").strip())
    reason = t.lstrip("— ").strip() or "미실행"
    return dict(kind="na", reason=reason, text=t)


def load_state():
    s = json.loads(STATE.read_text(encoding="utf-8"))
    tasks = {}
    for t in s["tasks"]:
        key = t["key"]
        header = t["header"][1:]
        rows = {}
        for r in t["rows"]:
            model = MODEL_ALIAS.get(r[0], r[0])
            rows[model] = {ds: parse_cell(c) for ds, c in zip(header, r[1:])}
        ref = {MODEL_ALIAS.get(m, m): v for m, v in t.get("reference", {}).items()}
        tasks[key] = dict(header=header, rows=rows, reference=ref, metric=t["metric"])
    return s, tasks


def delta_class(d):
    a = abs(d)
    return "ok" if a <= 2 else ("warn" if a <= 5 else "bad")


def fmt_delta(d):
    return ("+" if d >= 0 else "−") + f"{abs(d):.1f}"


def cell_html(c, ref=None):
    if c["kind"] == "val":
        return (f'<span class="v">{c["value"]:.1f}</span><span class="sd">±{c["sd"]:.1f}</span>'
                f'<span class="d {delta_class(c["delta"])}">{fmt_delta(c["delta"])}</span>')
    if c["kind"] == "lim":
        return f'<span class="lim" title="{c["text"]}">{c["label"]}</span>'
    return f'<span class="na" title="{c["reason"]}">—</span>'


def cards_html(cards):
    inner = "".join(
        f'<div class="hg-card"><span class="k">{k}</span><span class="big">{big}</span>'
        f'<span class="note">{note}</span></div>' for k, big, note in cards)
    return f'<div class="hg-cards">{inner}</div>'


def legend_html():
    return ('<div class="hg-legend"><span>우리값 <span class="sd">±표준편차</span></span>'
            '<span class="d ok">±2 이내</span><span class="d warn">2–5</span>'
            '<span class="d bad">5 초과</span><span class="lim">OOM</span>'
            '<span class="lgn">논문이 수치를 못 낸 칸</span><span class="na">—</span>'
            '<span class="lgn">미실행·보류</span></div>')


def task_stats(task):
    """(수치 셀 수, ±2 이내 수, |Δ| 중앙값, 완료 모델 수, 이상치 목록)"""
    deltas, agree, done_models, outliers = [], 0, 0, []
    for model, cells in task["rows"].items():
        vals = [c for c in cells.values() if c["kind"] == "val"]
        if vals:
            done_models += 1
        for ds, c in cells.items():
            if c["kind"] != "val":
                continue
            deltas.append(abs(c["delta"]))
            if abs(c["delta"]) <= 2:
                agree += 1
            if abs(c["delta"]) > 3:
                outliers.append((model, ds, c))
    med = sorted(deltas)[len(deltas) // 2] if deltas else 0.0
    return len(deltas), agree, med, done_models, outliers


# --------------------------------------------------------------------------
# 노트 쓰기
# --------------------------------------------------------------------------
VOLATILE_RE = re.compile(r"(갱신 |updated: )\d{4}-\d{2}-\d{2}[ T:\d]*")


def write_note(path, body, frontmatter=None, dry_run=False, volatile=False):
    """frontmatter + AUTO 블록을 교체하고 그 뒤 사용자 메모는 보존한다.
    volatile=False 이면 날짜만 바뀐 경우 쓰지 않는다 (git 커밋 잡음 방지)."""
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


def front(kind, **kw):
    lines = [f"type: {kind}"] + [f"{k}: {v}" for k, v in kw.items()]
    lines.append(f"updated: {now().strftime('%Y-%m-%d %H:%M')}")
    tag = {"model": "hgnn/model", "dataset": "hgnn/dataset", "agent": "hgnn/agent"}.get(kind, "hgnn/overview")
    lines.append(f"tags: [{tag}]")
    return lines


# --------------------------------------------------------------------------
# 1. 논문 대조 노트
# --------------------------------------------------------------------------
def note_paper(state, tasks, dry):
    today = now().strftime("%Y-%m-%d %H:%M")
    n3 = task_stats(tasks["T3"]); n4 = task_stats(tasks["T4"])
    total_outliers = len(n3[4]) + len(n4[4]) + (len(task_stats(tasks["T5"])[4]) if "T5" in tasks else 0)
    lines = ["# 논문 대조 — HyperGC Table 3·4·5", "",
             f"clerk 원장(`experiment_now.md`)의 정식 20-seed 결과를 KDD ’26 HyperGC 논문 표와 셀 단위로 대조한다. "
             f"Δ = 우리 평균 − 논문 평균. 갱신 {today}.", "",
             cards_html([
                 ("NC 일치율", f"{n3[1]}/{n3[0]}", f"±2 이내 · |Δ| 중앙값 {n3[2]:.2f}"),
                 ("HP 일치율", f"{n4[1]}/{n4[0]}", f"±2 이내 · |Δ| 중앙값 {n4[2]:.2f}"),
                 ("완료 모델", f"{n3[3]} · {n4[3]}", "NC / HP (19개 중)"),
                 ("이상치", f"{total_outliers}", "|Δ| 3.0 초과 셀"),
             ]), ""]
    if state.get("audit", {}).get("available"):
        a = state["audit"]
        lines += [f'> [!check] 기준값 검증 — 원장의 Δ {a["checked"]}칸을 `paper_reference.json`(HyperGC.pdf)과 대조: '
                  f'일치 {a["agree"]} · 불일치 {len(a["mismatch"])}', ""]
    for key in ("T3", "T4", "T5"):
        if key not in tasks:
            continue
        t = tasks[key]; en, ko, metric, _ = TASK_LABEL[key]
        # 열 정리: 수치가 하나도 없는 열은 뒤로 뺀다
        cols = [d for d in t["header"] if any(t["rows"][m][d]["kind"] == "val" for m in t["rows"])]
        empty = [d for d in t["header"] if d not in cols]
        lines += [f"## {en} <span class=\"m\">{key.replace('T', 'Table ')} · {metric}</span>", "",
                  legend_html(), "",
                  "| 모델 | " + " | ".join(cols) + " |", "|---|" + "---:|" * len(cols)]
        order = sorted(t["rows"], key=lambda m: -sum(c["kind"] == "val" for c in t["rows"][m].values()))
        for m in sorted(order):
            lines.append(f"| [[{m}]] | " + " | ".join(cell_html(t["rows"][m][d]) for d in cols) + " |")
        if empty:
            lines += ["", f"<span class=\"lgn\">표시하지 않은 열 (정식 결과 없음): {', '.join(empty)}</span>"]
        lines.append("")
    # 이상치
    outs = []
    for key in ("T3", "T4", "T5"):
        if key in tasks:
            tag = {"T3": "NC", "T4": "HP", "T5": "CD"}[key]
            for m, ds, c in task_stats(tasks[key])[4]:
                ref = tasks[key]["reference"].get(m, {}).get(ds)
                outs.append((abs(c["delta"]), tag, m, ds, c, ref))
    outs.sort(key=lambda x: -x[0])
    lines += ["## 이상치 <span class=\"m\">|Δ| 3.0 초과</span>", ""]
    if outs:
        lines.append('<ul class="hg-out">')
        for _, tag, m, ds, c, ref in outs:
            refs = f"{ref:.1f}" if isinstance(ref, (int, float)) else "?"
            lines.append(f'<li><span class="tag">{tag}</span><b>{m}</b><span class="ds">{ds}</span>'
                         f'<span class="nums">{c["value"]:.1f}<em>vs</em>{refs}</span>'
                         f'<span class="d {delta_class(c["delta"])}">{fmt_delta(c["delta"])}</span></li>')
        lines.append("</ul>")
    else:
        lines.append("없음.")
    # 최근 완료 소식 (원장에서)
    upd = state.get("updates", {})
    if upd.get("items"):
        lines += ["", f"## 원장의 최근 기록 <span class=\"m\">{upd.get('title', '')}</span>", ""]
        lines += [f"- {it}" for it in upd["items"][:8]]
    lines += ["", f"원본: `.agents/clerk-reports/experiment_now.md` → `dashboard/state.json` · 기준값 `dashboard/paper_reference.json`",
              "", "관련: [[Home]] · [[대시보드]]"]
    return write_note(VAULT / "논문 대조.md", "\n".join(lines), front("overview"), dry)


# --------------------------------------------------------------------------
# 2. 모델 노트 · 3. 데이터셋 노트
# --------------------------------------------------------------------------
def note_models(state, tasks, dry):
    changed = 0
    models = sorted({m for t in tasks.values() for m in t["rows"]})
    for m in models:
        per = {}
        for key, t in tasks.items():
            if m in t["rows"]:
                per[key] = t["rows"][m]
        # 카드
        cards = []
        for key in ("T3", "T4"):
            if key in per:
                vals = [c for c in per[key].values() if c["kind"] == "val"]
                agree = sum(abs(c["delta"]) <= 2 for c in vals)
                med = sorted(abs(c["delta"]) for c in vals)[len(vals) // 2] if vals else None
                cards.append((f"{'NC' if key == 'T3' else 'HP'} 일치", f"{agree}/{len(vals)}",
                              f"|Δ| 중앙값 {med:.2f}" if med is not None else "정식 결과 없음"))
        worst = None
        for key in per:
            for ds, c in per[key].items():
                if c["kind"] == "val" and (worst is None or abs(c["delta"]) > abs(worst[2])):
                    worst = (key, ds, c["delta"])
        if worst:
            cards.append(("최대 편차", fmt_delta(worst[2]),
                          f"{TASK_LABEL[worst[0]][1]} · {worst[1]}"))
        d = MODEL_DIR.get(m, m)
        lines = [f"# {m}", "",
                 f"<span class=\"lgn\">코드 `{d}/` · 결과 `results/result_*_{d}_*.txt` · 갱신 {now().strftime('%Y-%m-%d %H:%M')}</span>", "",
                 cards_html(cards), ""]
        for key in ("T3", "T4", "T5"):
            if key not in per:
                continue
            en, ko, metric, _ = TASK_LABEL[key]
            ref = tasks[key]["reference"].get(m, {})
            lines += [f"## {en} <span class=\"m\">{key.replace('T', 'Table ')} · {metric}</span>", "",
                      "| 데이터셋 | 우리 | 논문 | Δ | 비고 |", "|---|---:|---:|---:|---|"]
            for ds in tasks[key]["header"]:
                c = per[key][ds]
                r = ref.get(ds)
                refs = f"{r:.1f}" if isinstance(r, (int, float)) else "—"
                if c["kind"] == "val":
                    lines.append(f"| [[{ds}]] | <span class=\"v\">{c['value']:.1f}</span><span class=\"sd\">±{c['sd']:.1f}</span> "
                                 f"| {refs} | <span class=\"d {delta_class(c['delta'])}\">{fmt_delta(c['delta'])}</span> | |")
                elif c["kind"] == "lim":
                    lines.append(f"| [[{ds}]] | <span class=\"lim\">{c['label']}</span> | {refs} | | {c['text']} |")
                else:
                    lines.append(f"| [[{ds}]] | <span class=\"na\">—</span> | {refs} | | {c['reason']} |")
            lines.append("")
        lines += [legend_html(), "", "관련: [[논문 대조]] · [[Home]]"]
        if write_note(VAULT / "models" / f"{m}.md", "\n".join(lines), front("model", datasets=len(tasks["T3"]["header"])), dry):
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
        lines = [f"# {ds}", "", f"<span class=\"lgn\">갱신 {now().strftime('%Y-%m-%d %H:%M')}</span>", ""]
        any_val = False
        for key in ("T3", "T4", "T5"):
            t = tasks.get(key)
            if not t or ds not in t["header"]:
                continue
            en, ko, metric, _ = TASK_LABEL[key]
            rows = [(m, t["rows"][m][ds]) for m in t["rows"]]
            vals = sorted([(m, c) for m, c in rows if c["kind"] == "val"], key=lambda x: -x[1]["value"])
            others = [(m, c) for m, c in rows if c["kind"] != "val"]
            if not vals and not others:
                continue
            lines += [f"## {en} <span class=\"m\">{metric}</span>", "",
                      "| # | 모델 | 우리 | 논문 | Δ |", "|---:|---|---:|---:|---:|"]
            for i, (m, c) in enumerate(vals, 1):
                any_val = True
                r = t["reference"].get(m, {}).get(ds)
                refs = f"{r:.1f}" if isinstance(r, (int, float)) else "—"
                lines.append(f"| {i} | [[{m}]] | <span class=\"v\">{c['value']:.1f}</span><span class=\"sd\">±{c['sd']:.1f}</span> "
                             f"| {refs} | <span class=\"d {delta_class(c['delta'])}\">{fmt_delta(c['delta'])}</span> |")
            if others:
                lines += ["", "<span class=\"lgn\">미실행·보류: " +
                          ", ".join(f"{m} ({c.get('label') or c.get('reason')})" for m, c in others) + "</span>"]
            lines.append("")
        lines += ["관련: [[논문 대조]] · [[Home]]"]
        if write_note(VAULT / "datasets" / f"{ds}.md", "\n".join(lines), front("dataset"), dry):
            changed += 1
    return changed


# --------------------------------------------------------------------------
# 4. 대시보드 — 살아 있는 것들
# --------------------------------------------------------------------------
def gpu_info():
    gpus = []
    out = sh("nvidia-smi --query-gpu=index,name,utilization.gpu,memory.used,memory.total,uuid --format=csv,noheader,nounits")
    for line in out.strip().splitlines():
        p = [x.strip() for x in line.split(",")]
        if len(p) >= 6:
            gpus.append(dict(index=int(p[0]), name=p[1].replace("NVIDIA GeForce ", ""), util=int(p[2]),
                             used=int(p[3]), total=int(p[4]), uuid=p[5], pids=[]))
    apps = sh("nvidia-smi --query-compute-apps=pid,gpu_uuid,used_memory --format=csv,noheader,nounits")
    for line in apps.strip().splitlines():
        p = [x.strip() for x in line.split(",")]
        if len(p) >= 2:
            for g in gpus:
                if g["uuid"] == p[1]:
                    g["pids"].append(int(p[0]))
    return gpus


def jobs():
    """모델 코드를 돌리고 있는 python 프로세스."""
    out = sh("ps -eo pid,etimes,args --no-headers")
    found = []
    for line in out.splitlines():
        parts = line.strip().split(None, 2)
        if len(parts) < 3:
            continue
        pid, et, args = int(parts[0]), int(parts[1]), parts[2]
        if "python" not in args or ".py" not in args or "conda run" in args:
            continue
        if "dashboard/" in args or "tools/" in args or "run-scripts/" in args or "vscode" in args:
            continue
        model = None
        for d in MODEL_DIR.values():
            if re.search(rf"(^|[\s/]){re.escape(d)}/", args):
                model = DIR_TO_MODEL[d.lower()]
                break
        if not model:
            continue
        m = re.search(r"--(?:dataset|data)[= ]([\w-]+)", args)
        ds = DATASET_ALIAS.get(m.group(1), m.group(1)) if m else "?"
        t = re.search(r"--task[= ](\w+)", args)
        g = re.search(r"--(?:gpu|device|cuda)[= ](\d+)", args) or re.search(r"CUDA_VISIBLE_DEVICES=(\d+)", args)
        s = re.search(r"--num_seeds[= ](\d+)", args) or re.search(r"--seeds?[= ](\d+)", args)
        found.append(dict(pid=pid, elapsed=et, model=model, dataset=ds,
                          task=t.group(1) if t else "?", gpu=g.group(1) if g else "?",
                          seeds=s.group(1) if s else "?", cmd=args[:140]))
    return found


def planned_datasets(run_id):
    """run-scripts 에서 run_id 를 선언한 스크립트를 찾아 데이터셋 목록을 읽는다."""
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
    """status.tsv 는 형식이 셋이다: (model ds STATE time) · (model ds code) · (ds code)."""
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
        state, when, ds, model = None, None, None, None
        if len(p) >= 4:
            model, ds, state, when = p[0], p[1], p[2], p[3]
        elif len(p) == 3:
            model, ds, code = p
            state = code
        elif len(p) == 2:
            ds, state = p
        if state and state.isdigit():
            state = {"0": "COMPLETE", "124": "OOT"}.get(state, f"FAILED({state})")
        rows.append(dict(model=model, dataset=ds, state=state or "?", when=when))
    return rows


def run_dirs():
    """full-runs 의 실행들. 최신 활동순."""
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
                first = p.read_text(encoding="utf-8", errors="replace").split("\n", 1)[0].strip()
                start = datetime.fromisoformat(first)
                break
            except Exception:
                continue
        if start is None:
            start = datetime.fromtimestamp(d.stat().st_ctime, KST)
        st = parse_status(d / "status.tsv")
        terminal = {r["dataset"]: r["state"] for r in st if r["dataset"]}
        started = [p.stem for p in logs]
        plan = planned_datasets(d.name)
        planned, script = (plan if plan else (None, None))
        active_ds = None
        for p in logs:
            if p.stem not in terminal and (now() - (mtime(p) or now())).total_seconds() < 900:
                active_ds = p.stem
        # 활성 데이터셋의 마지막 줄 (진행률 단서)
        tail = ""
        if active_ds:
            tail = sh(f"tail -c 4000 '{d / (active_ds + '.log')}' | grep -v '^$' | tail -1").strip()[:110]
        out.append(dict(id=d.name, path=d, start=start, latest=latest, terminal=terminal,
                        started=started, planned=planned, script=script, active_ds=active_ds, tail=tail,
                        active=(now() - latest).total_seconds() < 900))
    out.sort(key=lambda r: r["latest"], reverse=True)
    return out


def automation():
    pats = [("clerk 갱신 루프", "clerk-refresh-loop.sh"), ("collector 루프 (5분)", "dashboard/collector.py"),
            ("웹 대시보드 :8765", "dashboard/server.py"), ("pixel bridge", "dashboard/pixel_bridge.py")]
    out = sh("ps -eo pid,etimes,args --no-headers")
    rows = []
    for label, pat in pats:
        hit = [l for l in out.splitlines() if pat in l and "grep" not in l and "ssh" not in l]
        if hit:
            p = hit[0].split(None, 2)
            rows.append((label, "on", int(p[0]), int(p[1])))
        else:
            rows.append((label, "off", None, None))
    # vault 동기화는 1초짜리 cron 이라 프로세스가 아니라 로그의 최근성으로 본다
    t = mtime(VAULT / ".sync.log")
    rows.append(("vault 동기화 (cron 1분)", "on" if t and (now() - t).total_seconds() < 180 else "off", None,
                 int((now() - t).total_seconds()) if t else None))
    cron = sh("crontab -l 2>/dev/null")
    return rows, cron


def git_log(n=12):
    if not (ROOT / ".git").exists():
        return None, []
    head = sh(f"git -C '{ROOT}' rev-parse --short HEAD").strip()
    out = sh(f"git -C '{ROOT}' log -{n} --date=format:'%m-%d %H:%M' --format='%h|%ad|%s'")
    rows = [l.split("|", 2) for l in out.strip().splitlines() if l.count("|") >= 2]
    dirty = sh(f"git -C '{ROOT}' status --porcelain | wc -l").strip()
    remote = sh(f"git -C '{ROOT}' remote get-url origin 2>/dev/null").strip()
    return dict(head=head, dirty=dirty, remote=remote), rows


def status_pill(state):
    s = state.upper()
    if s.startswith("COMPLETE") or s == "SKIP_EXISTING" or s == "ALREADY-COMPLETE":
        return f'<span class="pill ok">{state}</span>'
    if "OOM" in s or "OOT" in s or "SKIP" in s:
        return f'<span class="pill lim">{state}</span>'
    if "FAIL" in s:
        return f'<span class="pill bad">{state}</span>'
    return f'<span class="pill">{state}</span>'


def note_dashboard(dry):
    t0 = now()
    gpus = gpu_info()
    live = jobs()
    runs = run_dirs()
    auto, cron = automation()
    ginfo, commits = git_log()
    active_runs = [r for r in runs if r["active"]]
    n_done_today = sum(1 for r in runs for ds, st in r["terminal"].items()
                       if st.startswith("COMPLETE") and r["latest"] and (t0 - r["latest"]).days < 1)

    lines = [f"# 실험 대시보드 <span class=\"m\">{HOST}</span>", "",
             f'<span class="live"><i></i>{t0.strftime("%Y-%m-%d %H:%M:%S")} KST · 1분마다 갱신</span>', "",
             cards_html([
                 ("실행 중 프로세스", str(len(live)), "모델 코드를 돌리는 python"),
                 ("활성 실행", str(len(active_runs)), "15분 내 로그가 움직인 run"),
                 ("GPU", " · ".join(f"{g['util']}%" for g in gpus) or "—",
                  " · ".join(f"{g['used'] / 1024:.1f}/{g['total'] / 1024:.0f}G" for g in gpus)),
                 ("최근 24h 완료", str(n_done_today), "status.tsv COMPLETE"),
             ]), ""]

    # GPU
    lines += ["## GPU", "", "| # | 모델 | 사용률 | 메모리 | 프로세스 |", "|---:|---|---:|---:|---|"]
    for g in gpus:
        bar = f'<span class="bar"><i style="width:{g["util"]}%"></i></span> {g["util"]}%'
        pids = ", ".join(str(p) for p in g["pids"]) or "<span class=\"lgn\">유휴</span>"
        lines.append(f"| {g['index']} | {g['name']} | {bar} | {g['used']} / {g['total']} MiB | {pids} |")
    if not gpus:
        lines.append("| — | nvidia-smi 응답 없음 | | | |")
    lines.append("")

    # 진행 중
    lines += ["## 진행 중 실험", ""]
    if not live and not active_runs:
        lines += ['<span class="lgn">지금 돌아가는 실험이 없다.</span>', ""]
    if live:
        lines += ["| PID | 모델 | 데이터셋 | 태스크 | GPU | seeds | 경과 |", "|---:|---|---|---|---:|---:|---:|"]
        for j in sorted(live, key=lambda x: -x["elapsed"]):
            lines.append(f"| {j['pid']} | [[{j['model']}]] | {j['dataset']} | {j['task']} | {j['gpu']} | {j['seeds']} | {dur(j['elapsed'])} |")
        lines.append("")
    for r in active_runs:
        total = len(r["planned"]) if r["planned"] else None
        done = sum(1 for s in r["terminal"].values() if s.startswith("COMPLETE") or "SKIP" in s.upper())
        failed = sum(1 for s in r["terminal"].values() if "FAIL" in s.upper() or "OOM" in s.upper() or "OOT" in s.upper())
        prog = f"{done}/{total}" if total else f"{done} 완료"
        pct = int(100 * done / total) if total else None
        bar = f'<span class="bar"><i style="width:{pct}%"></i></span> {pct}%' if pct is not None else ""
        lines += [f"### {r['id']}", "",
                  f"<span class=\"lgn\">시작 {r['start'].strftime('%m-%d %H:%M')} · 경과 {dur((t0 - r['start']).total_seconds())} · "
                  f"마지막 로그 {ago(r['latest'])}" + (f" · 스크립트 `{r['script']}`" if r['script'] else "") + "</span>", "",
                  f"진행 {prog} {bar}" + (f" · 실패 {failed}" if failed else ""), ""]
        if r["planned"]:
            cells = []
            for ds in r["planned"]:
                st = r["terminal"].get(ds)
                if st:
                    cells.append(f"{DATASET_ALIAS.get(ds, ds)} {status_pill(st)}")
                elif ds == r["active_ds"]:
                    cells.append(f"{DATASET_ALIAS.get(ds, ds)} <span class=\"pill run\">RUNNING</span>")
                elif ds in r["started"]:
                    cells.append(f"{DATASET_ALIAS.get(ds, ds)} <span class=\"pill\">STARTED</span>")
                else:
                    cells.append(f"{DATASET_ALIAS.get(ds, ds)} <span class=\"pill wait\">대기</span>")
            lines += ["  ".join(cells), ""]
        if r["active_ds"] and r["tail"]:
            lines += [f"`{r['active_ds']}.log` 마지막 줄:", "", f"```", r["tail"], "```", ""]

    # 최근 실행 이력
    lines += ["## 최근 실행 <span class=\"m\">full-runs · 최신 10개</span>", "",
              "| 실행 | 시작 | 마지막 활동 | 결과 |", "|---|---|---|---|"]
    for r in runs[:10]:
        summ = defaultdict(int)
        for s in r["terminal"].values():
            k = "완료" if s.startswith("COMPLETE") or "SKIP" in s.upper() else ("OOM/OOT" if "OOM" in s.upper() or "OOT" in s.upper() else "실패")
            summ[k] += 1
        res = " · ".join(f"{k} {v}" for k, v in summ.items()) or "<span class=\"lgn\">기록 없음</span>"
        flag = ' <span class="pill run">활성</span>' if r["active"] else ""
        lines.append(f"| `{r['id']}`{flag} | {r['start'].strftime('%m-%d %H:%M')} | {ago(r['latest'])} | {res} |")
    lines.append("")

    # 자동화 프로세스
    lines += ["## 자동화 프로세스", "", "| 이름 | 상태 | PID | 가동 시간 |", "|---|---|---:|---:|"]
    for label, st, pid, et in auto:
        pill = '<span class="pill ok">on</span>' if st == "on" else '<span class="pill bad">off</span>'
        et_s = ("마지막 " + ago(now() - timedelta(seconds=et))) if (et is not None and pid is None) else (dur(et) if et else "—")
        lines.append(f"| {label} | {pill} | {pid or '—'} | {et_s} |")
    lines.append("")

    # 커밋
    lines += ["## 커밋 <span class=\"m\">git</span>", ""]
    if ginfo is None:
        lines += ['<span class="lgn">아직 git 저장소가 아니다.</span>', ""]
    else:
        lines += [f"HEAD `{ginfo['head']}` · 작업트리 변경 {ginfo['dirty']}건 · origin `{ginfo['remote'] or '미설정'}`", "",
                  "| 커밋 | 시각 | 메시지 |", "|---|---|---|"]
        for h, d, msg in commits:
            lines.append(f"| `{h}` | {d} | {msg} |")
        lines.append("")
    lines += ["관련: [[에이전트]] · [[논문 대조]] · [[Home]]"]
    return write_note(VAULT / "대시보드.md", "\n".join(lines), front("overview", host=HOST), dry, volatile=True)


# --------------------------------------------------------------------------
# 5. 에이전트
# --------------------------------------------------------------------------
AGENTS = [
    dict(name="clerk", file=".agents/clerk.md",
         role="결과 원장 관리자. 정식 20-seed 실행이 끝나면 `experiment_now.md` 에 값과 논문 Δ를 기록하고, 한글 보고서(개별/통합)를 쓴다. smoke 결과는 표에 올리지 않는다.",
         inputs="results/ · full-runs/status.tsv · paper_reference.json",
         outputs="clerk-reports/experiment_now.md · 개별/ · 통합/ · README.md",
         process="clerk-refresh-loop.sh", activity=["clerk-reports/experiment_now.md", "env-status/clerk-refresh-loop.log", "clerk-reports/개별"]),
    dict(name="env-builder", file=".agents/env-builder.md",
         role="모델별 Conda 환경 구축·유지. 모델 코드는 건드리지 않고 환경 변경과 차단 요인을 기록한다. HyperGCL 은 다른 모델이 모두 끝난 뒤에만.",
         inputs="*_require.txt · env-checker 피드백",
         outputs="env-status/env-builder.md · edge-builder-report.md",
         process=None, activity=["env-status/env-builder.md", "env-status/edge-builder-report.md"]),
    dict(name="env-checker", file=".agents/env-checker.md",
         role="env-builder 가 준비한 환경에서 모델을 검증. import → 1-seed 15-epoch smoke → 논문값과 대략 비교. 정식 실행의 게이트 파일(`*-check.ok`)을 만든다.",
         inputs="env-status/ 빌더 핸드오프 · time_node.sh",
         outputs="env-status/checker-*.md · edge-checker-report.md · *-check.ok",
         process=None, activity=["env-status/edge-checker-report.md", "env-status/checker-", "env-status/villain-edge-check.ok"]),
]


def latest_activity(patterns):
    best = None
    for pat in patterns:
        p = ROOT / ".agents" / pat
        cands = []
        if p.is_dir():
            cands = list(p.iterdir())
        elif p.exists():
            cands = [p]
        else:
            cands = list(p.parent.glob(p.name + "*"))
        for c in cands:
            t = mtime(c)
            if t and (best is None or t > best[0]):
                best = (t, c.relative_to(ROOT).as_posix())
    return best


def note_agents(dry):
    t0 = now()
    ps = sh("ps -eo pid,etimes,args --no-headers")
    lines = [f"# 에이전트 <span class=\"m\">{HOST}</span>", "",
             f"<span class=\"lgn\">정의서 `.agents/*.md` · 상태는 프로세스와 산출물 파일의 갱신 시각에서 읽는다 · {t0.strftime('%Y-%m-%d %H:%M')}</span>", ""]
    summary = []
    detail = []
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
            state, pill = "활성 (루프 실행 중)", "ok"
        elif age is not None and age < 3600:
            state, pill = "활성 (1시간 내 산출물 갱신)", "ok"
        elif age is not None and age < 86400:
            state, pill = "대기 (24시간 내 활동)", "wait"
        else:
            state, pill = "비활성", "bad"
        summary.append((a, state, pill, proc, act))
    lines += ["| 에이전트 | 상태 | 프로세스 | 마지막 활동 | 산출물 |", "|---|---|---|---|---|"]
    for a, state, pill, proc, act in summary:
        pr = (f"PID {proc[0]} · 시작 {(t0 - timedelta(seconds=proc[1])).strftime('%m-%d %H:%M')}"
              if proc else "<span class=\"lgn\">상주 프로세스 없음 (Claude 세션에서 호출)</span>")
        la = f"{act[0].strftime('%m-%d %H:%M')} · `{act[1]}`" if act else "—"
        lines.append(f"| [[#{a['name']}\\|{a['name']}]] | <span class=\"pill {pill}\">{state}</span> | {pr} | {la} | {a['outputs']} |")
    lines.append("")

    # 관여 실험: 활성 run + 최근 run 에서 게이트/원장 근거
    runs = run_dirs()
    recent = runs[:6]
    lines += ["## 실행과의 관계", "",
              "| 실행 | clerk | env-checker | env-builder |", "|---|---|---|---|"]
    for r in recent:
        script_txt = ""
        if r["script"]:
            try:
                script_txt = (SCRIPTS / r["script"]).read_text(encoding="utf-8", errors="replace")
            except OSError:
                pass
        clerk_c = "결과 기록" if r["terminal"] else "대기"
        chk = "게이트 `*.ok` 검사" if "check.ok" in script_txt else ("smoke 검증" if "smoke" in r["id"] else "—")
        bld = "환경 제공 (`conda run -n`)" if "conda run" in script_txt else "—"
        flag = ' <span class="pill run">활성</span>' if r["active"] else ""
        lines.append(f"| `{r['id']}`{flag} | {clerk_c} | {chk} | {bld} |")
    lines.append("")

    # 상세
    for a, state, pill, proc, act in summary:
        lines += [f"## {a['name']}", "",
                  f"<span class=\"pill {pill}\">{state}</span>", "",
                  a["role"], "",
                  "| | |", "|---|---|",
                  f"| 정의서 | `{a['file']}` |",
                  f"| 입력 | {a['inputs']} |",
                  f"| 출력 | {a['outputs']} |",
                  f"| 상주 프로세스 | {a['process'] or '없음 — Claude 세션이 필요할 때 호출'} |", ""]
        if a["name"] == "clerk":
            reports = sorted((CLERK_REPORTS / "개별").glob("*.md"))[-5:] if (CLERK_REPORTS / "개별").is_dir() else []
            queue = CLERK_REPORTS / "clerk-refresh-queue.md"
            qn = 0
            if queue.exists():
                qn = sum(1 for l in queue.read_text(encoding="utf-8", errors="replace").splitlines() if l.startswith("- ") or l.startswith("| "))
            lines += [f"최근 보고서 {len(reports)}건 · 갱신 대기열 {qn}줄", ""]
            lines += [f"- `{p.name}`" for p in reversed(reports)] + [""]
        if a["name"] == "env-checker":
            oks = sorted(ENV_STATUS.glob("*.ok"))
            if oks:
                lines += ["게이트 파일: " + " · ".join(f"`{p.name}` ({mtime(p).strftime('%m-%d %H:%M')})" for p in oks), ""]
    lines += ["관련: [[대시보드]] · [[Home]]"]
    return write_note(VAULT / "에이전트.md", "\n".join(lines), front("overview", host=HOST), dry)


# --------------------------------------------------------------------------
# 6. 차트 (state.json 기준) · 7. Home
# --------------------------------------------------------------------------
def charts(tasks, dry):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.colors import LinearSegmentedColormap
    except Exception:
        return 0
    BLUE = ["#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7", "#3987e5",
            "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b"]
    THEME = {"light": dict(surface="#fcfcfb", ink="#0b0b0b", ink2="#52514e", grid="#e5e4e0", bar="#2a78d6",
                           empty="#f0efec", ramp=BLUE, hi="#ffffff", lo="#0b0b0b"),
             "dark": dict(surface="#1a1a19", ink="#ffffff", ink2="#c3c2b7", grid="#383835", bar="#3987e5",
                          empty="#2a2a28", ramp=BLUE[::-1], hi="#0b0b0b", lo="#ffffff")}
    for name in ("Noto Sans CJK KR", "Noto Serif CJK KR", "Noto Sans CJK SC", "NanumGothic", "Malgun Gothic"):
        try:
            from matplotlib.font_manager import findfont, FontProperties
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
        t = tasks[key]; en, ko, metric, short = TASK_LABEL[key]
        ds = [d for d in t["header"] if any(t["rows"][m][d]["kind"] == "val" for m in t["rows"])]
        mdl = [m for m in t["rows"] if any(t["rows"][m][d]["kind"] == "val" for d in ds)]
        if not ds or not mdl:
            continue
        val = {(m, d): t["rows"][m][d]["value"] for m in mdl for d in ds if t["rows"][m][d]["kind"] == "val"}
        mean = {m: (sum(val[(m, d)] for d in ds if (m, d) in val) / max(1, sum((m, d) in val for d in ds)),
                    sum((m, d) in val for d in ds)) for m in mdl}
        mdl.sort(key=lambda m: mean[m][0], reverse=True)
        for mode, th in THEME.items():
            cmap = LinearSegmentedColormap.from_list("b", th["ramp"])
            fig, ax = plt.subplots(figsize=(1.15 * len(ds) + 3.6, 0.36 * len(mdl) + 1.9))
            fig.patch.set_facecolor(th["surface"]); ax.set_facecolor(th["surface"])
            for s in ax.spines.values():
                s.set_visible(False)
            ax.tick_params(colors=th["ink2"], length=0, labelsize=9)
            rng = {d: (min(val[(m, d)] for m in mdl if (m, d) in val), max(val[(m, d)] for m in mdl if (m, d) in val)) for d in ds}
            for i, m in enumerate(mdl):
                for j, d in enumerate(ds):
                    v = val.get((m, d))
                    if v is None:
                        ax.add_patch(plt.Rectangle((j + .01, i + .01), .98, .98, facecolor=th["empty"], edgecolor="none"))
                        ax.text(j + .5, i + .5, "—", ha="center", va="center", color=th["ink2"], fontsize=8)
                        continue
                    lo, hi = rng[d]; f = .5 if hi == lo else (v - lo) / (hi - lo)
                    ax.add_patch(plt.Rectangle((j + .01, i + .01), .98, .98, facecolor=cmap(f), edgecolor="none"))
                    ax.text(j + .5, i + .5, f"{v:.1f}", ha="center", va="center", fontsize=8.5,
                            color=th["hi"] if f > .55 else th["lo"])
            ax.set_xlim(0, len(ds)); ax.set_ylim(0, len(mdl))
            ax.set_xticks([j + .5 for j in range(len(ds))]); ax.set_xticklabels(ds, rotation=30, ha="right")
            ax.set_yticks([i + .5 for i in range(len(mdl))]); ax.set_yticklabels(mdl)
            ax.invert_yaxis(); ax.xaxis.set_ticks_position("top")
            ax.set_title(f"{en}\n색 = 각 열 안에서의 상대 위치 · 숫자 = 실제 값", color=th["ink"], fontsize=12, loc="left", pad=16, linespacing=1.6)
            fig.tight_layout()
            if not dry:
                fig.savefig(assets / f"{short}-heatmap-{mode}.png", dpi=170, facecolor=th["surface"])
            plt.close(fig); made += 1
            # 순위
            rev = list(reversed(mdl)); vals = [mean[m][0] for m in rev]
            fig, ax = plt.subplots(figsize=(6.8, 0.34 * len(rev) + 1.8))
            fig.patch.set_facecolor(th["surface"]); ax.set_facecolor(th["surface"])
            for s in ax.spines.values():
                s.set_visible(False)
            ax.tick_params(colors=th["ink2"], length=0, labelsize=9)
            ax.xaxis.grid(True, color=th["grid"], linewidth=.8); ax.set_axisbelow(True)
            ax.barh(range(len(rev)), vals, height=.62, color=th["bar"], edgecolor=th["surface"], linewidth=1.2)
            for i, m in enumerate(rev):
                ax.text(vals[i] + max(vals) * .012, i, f"{vals[i]:.1f}", va="center", fontsize=8.5, color=th["ink2"])
            ax.set_yticks(range(len(rev))); ax.set_yticklabels([f"{m}  ({mean[m][1]})" for m in rev])
            ax.set_xlim(0, max(vals) * 1.12); ax.set_xlabel(metric, color=th["ink2"], fontsize=9)
            ax.set_title(f"{en}\n데이터셋 {len(ds)}개 평균 · 괄호는 측정된 데이터셋 수", color=th["ink"], fontsize=12, loc="left", pad=14, linespacing=1.6)
            fig.tight_layout()
            if not dry:
                fig.savefig(assets / f"{short}-rank-{mode}.png", dpi=170, facecolor=th["surface"])
            plt.close(fig); made += 1
    return made


def note_home(tasks, dry, n_charts):
    models = sorted({m for t in tasks.values() for m in t["rows"]})
    datasets = []
    for t in tasks.values():
        for d in t["header"]:
            if d not in datasets:
                datasets.append(d)
    lines = ["# HGNN 실험 노트", "",
             f"<span class=\"lgn\">{HOST} 가 만들고 GitHub 를 거쳐 여기로 온다 · 갱신 {now().strftime('%Y-%m-%d %H:%M')}</span>", "",
             "## 지금", "",
             "- [[대시보드]] — 실행 중 실험 · GPU · 최근 실행 · 자동화 프로세스 · 커밋 (1분 갱신)",
             "- [[에이전트]] — clerk / env-builder / env-checker 의 역할과 활성 상태", "",
             "## 결과", "",
             "- [[논문 대조]] — HyperGC Table 3·4·5 vs 우리 정식 결과, Δ 배지", ""]
    if n_charts:
        lines += ["- [[Charts]] — 태스크별 히트맵·순위", ""]
    lines += ["## 모델", ""] + [f"- [[{m}]]" for m in models] + ["", "## 데이터셋", ""] + [f"- [[{d}]]" for d in datasets]
    lines += ["", "## 어떻게 갱신되나", "",
              "| 무엇 | 누가 | 경로 |", "|---|---|---|",
              "| 원장·Δ | clerk (10분 루프) → `collector.py` (5분) | `experiment_now.md` → `state.json` |",
              "| 이 노트들 | `tools/vault_build.py` (cron 1분) | `vault/` |",
              "| 로컬 PC 로 | 서버가 변경 시 git push → PC 가 1분마다 pull · 대시보드.md 는 ssh 로 직접 | `hgnn_sync.ps1` |", "",
              "> 각 노트의 자동 생성 구간(AUTO 주석 사이)만 덮어쓴다. **`## 메모`** 는 보존된다."]
    return write_note(VAULT / "Home.md", "\n".join(lines), front("home"), dry)


def note_charts(dry):
    lines = ["# 차트", "", f"<span class=\"lgn\">값은 clerk 원장의 정식 결과 · 갱신 {now().strftime('%Y-%m-%d %H:%M')}</span>", ""]
    for short, en in (("node", "Node classification"), ("edge", "Hyperedge prediction")):
        lines += [f"## {en}", "", f"![[{short}-heatmap-light.png]]", "", f"![[{short}-rank-light.png]]", ""]
    lines += ["> 다크 테마에서는 같은 이름의 `-dark.png` 를 쓰면 된다.", "", "관련: [[논문 대조]] · [[Home]]"]
    return write_note(VAULT / "Charts.md", "\n".join(lines), front("overview"), dry)


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
    if n_charts:
        changed += note_charts(dry)
    changed += note_agents(dry)
    changed += note_home(tasks, dry, n_charts)
    dash = note_dashboard(dry)
    print(f"{'변경될' if dry else '갱신된'} 노트 {changed}개 (+대시보드 {'갱신' if dash else '동일'}) · 차트 {n_charts}장 · vault: {VAULT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
