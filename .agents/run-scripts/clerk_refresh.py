#!/usr/bin/env python3
"""Incremental, evidence-only clerk refresh for formal result files.

This deliberately recognises only the common ``result_<dataset>_<model>_<task>.txt``
format with an explicit final 20-value array (plain ``[...]`` or ``tensor([...])``).
Everything else is queued for a human or a dedicated clerk pass; this avoids
silently treating smoke runs as benchmarks.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results"
RUNS = ROOT / ".agents" / "env-status" / "full-runs"
REPORT = ROOT / ".agents" / "clerk-reports" / "experiment_now.md"
QUEUE = ROOT / ".agents" / "clerk-reports" / "clerk-refresh-queue.md"
STATE = ROOT / ".agents" / "clerk-reports" / ".clerk-refresh-state.json"
REFERENCE = ROOT / "dashboard" / "paper_reference.json"
KST = timezone(timedelta(hours=9))

DATASET = {
    "citeseer_cite": "Citeseer", "cora_coauth": "Cora-CA", "imdb": "IMDB",
    "house": "House", "pubmed_cite": "Pubmed", "aminer": "AMiner",
    "dblp_copub": "DBLP-A", "dblp_p": "DBLP-P", "modelnet_40": "MN-40",
    "news": "20News", "20news": "20News",
}
MODEL = {"EDHNN": "ED-HNN", "Hyper_GCN": "HyperGCN",
         "SEHSSL": "SE-HSSL", "Hypeboy": "HypeBoy"}
TABLE = {"node": "Node classification", "edge": "Hyperedge prediction",
         "cluster": "Community detection"}
PAPER_KEY = {"Node classification": "T3", "Hyperedge prediction": "T4",
             "Community detection": "T5"}
PAPER_MODEL = {"GGD (H-GD)": "GGD", "HGD": "GGD", "Hypeboy": "HypeBoy",
               "EDHNN": "ED-HNN"}


def stamp(p: Path) -> str:
    s = p.stat()
    return f"{s.st_mtime_ns}:{s.st_size}"


def load_state() -> dict:
    if not STATE.exists():
        return {"seen": {}, "queued": {}}
    try:
        return json.loads(STATE.read_text())
    except Exception:
        return {"seen": {}, "queued": {}}


def queue_item(state: dict, path: Path, reason: str) -> None:
    key = str(path.relative_to(ROOT))
    marker = f"{stamp(path)}:{reason}"
    if state["queued"].get(key) == marker:
        return
    now = datetime.now(KST).strftime("%Y-%m-%d %H:%M KST")
    if not QUEUE.exists():
        QUEUE.write_text("# Clerk refresh queue\n\n자동 처리하지 않은 새 결과 후보입니다. 원본을 검토한 뒤 정식 20-seed 결과만 원장에 반영하세요.\n")
    with QUEUE.open("a") as out:
        out.write(f"\n- [{now}] 갱신 요청: `{key}` — {reason}\n")
    state["queued"][key] = marker


def parse_file(path: Path):
    m = re.fullmatch(r"result_(.+)_([^_]+(?:_[^_]+)?)_(node|edge|cluster)\.txt", path.name)
    if not m:
        return None, "파일명이 표준 result_<dataset>_<model>_<task>.txt 형식이 아님"
    # Dataset names contain underscores; choose the known dataset prefix first.
    body = path.name[len("result_"):-4]
    task = body.rsplit("_", 1)[1]
    stem = body[:-(len(task) + 1)]
    dataset_key = next((k for k in sorted(DATASET, key=len, reverse=True)
                        if stem.startswith(k + "_")), None)
    if not dataset_key:
        return None, "알 수 없는 데이터셋 접두사"
    raw_model = stem[len(dataset_key) + 1:]
    model = MODEL.get(raw_model, raw_model)
    if task not in TABLE:
        return None, "지원하지 않는 task"
    # Node ledger uses the historical display name ``GGD (H-GD)``, whereas
    # Table 4 has an explicit HGD row.  Preserve the task-specific identity
    # instead of accidentally filling the unrelated smoke-only GGD row.
    if raw_model == "HGD" and task != "edge":
        model = "GGD (H-GD)"
    text = path.read_text(errors="replace")
    # Most trainers write a plain NumPy-style ``[v1, ..., v20],mean ± std``;
    # HyperGCL uses ``tensor([...]),mean ± std``.  Bind the summary to the
    # immediately preceding array so a tuning hyperparameter list cannot be
    # mistaken for the final metric.
    records = list(re.finditer(
        r"(?:tensor\(\s*)?\[([^\[\]]+)\]\s*\)?\s*,?\s*"
        r"(\d+(?:\.\d+)?)\s*±\s*(\d+(?:\.\d+)?)", text, re.S))
    if not records:
        return None, "원시 배열과 평균±표준편차가 한 쌍으로 기록되지 않음"
    raw, mean_s, std_s = records[-1].groups()
    nums = re.findall(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?", raw)
    if len(nums) != 20:
        return None, f"최종 원시 배열 seed 수가 {len(nums)}개(정식 20개 필요)"
    mean, std = float(mean_s), float(std_s)
    return (TABLE[task], model, DATASET[dataset_key], mean, std), None


def find_table(lines: list[str], title: str):
    for i, line in enumerate(lines):
        if line.startswith("## ") and line[3:].startswith(title):
            for j in range(i + 1, len(lines) - 1):
                if lines[j].startswith("|") and "---" in lines[j + 1]:
                    return j
    return None


def update_report(result, refs) -> str | None:
    task, model, dataset, mean, std = result
    lines = REPORT.read_text().splitlines()
    start = find_table(lines, task)
    if start is None:
        return f"원장에 {task} 표가 없음"
    header = [x.strip() for x in lines[start].strip("|").split("|")]
    if dataset not in header:
        return f"원장 {task} 표에 {dataset} 열이 없음"
    col = header.index(dataset)
    row_i = next((i for i in range(start + 2, len(lines))
                  if lines[i].startswith("|") and lines[i].strip("|").split("|")[0].strip() == model), None)
    if row_i is None:
        return f"원장 {task} 표에 {model} 행이 없음"
    cells = [x.strip() for x in lines[row_i].strip("|").split("|")]
    if not cells[col].startswith("—"):
        return "already-recorded"
    paper = refs.get("tables", {}).get(PAPER_KEY[task], {}).get("models", {}).get(PAPER_MODEL.get(model, model), {}).get(dataset)
    if paper is None:
        return "논문 기준값이 없어 Δ를 안전하게 산출할 수 없음"
    delta = mean - float(paper)
    sign = "+" if delta >= 0 else "−"
    cells[col] = f"**{mean:.1f} ± {std:.1f}** (Δ **{sign}{abs(delta):.1f}**)"
    lines[row_i] = "| " + " | ".join(cells) + " |"
    REPORT.write_text("\n".join(lines) + "\n")
    return None


def main():
    state = load_state()
    refs = json.loads(REFERENCE.read_text())
    changed = 0
    candidates = sorted(RESULTS.glob("result_*.txt"), key=lambda p: p.stat().st_mtime)
    for path in candidates:
        key, mark = str(path.relative_to(ROOT)), stamp(path)
        if state["seen"].get(key) == mark:
            continue
        parsed, reason = parse_file(path)
        if parsed is None:
            queue_item(state, path, reason)
        else:
            result = update_report(parsed, refs)
            if result not in (None, "already-recorded"):
                queue_item(state, path, result)
            elif result is None:
                changed += 1
        state["seen"][key] = mark
    # A successful supervisor status is evidence that a run finished, but it is
    # not by itself a benchmark metric.  Inspect it every cycle and surface any
    # newly-completed run whose parser/output format needs a clerk decision.
    for path in sorted(RUNS.rglob("status.tsv")):
        key, mark = str(path.relative_to(ROOT)), stamp(path)
        if state["seen"].get(key) == mark:
            continue
        body = path.read_text(errors="replace")
        if re.search(r"(?:^|\s)(?:0|EXIT_CODE=0)(?:\s|$)", body, re.M):
            queue_item(state, path, "완료 상태는 있으나 정식 지표 형식/결과 파일 연결을 자동 검증할 수 없음")
        state["seen"][key] = mark
    STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")
    # The dashboard should reflect even a no-op audit (e.g. a manually edited report).
    subprocess.run([sys.executable, str(ROOT / "dashboard" / "collector.py")], check=False)
    print(f"clerk refresh complete: recorded={changed}, scanned={len(candidates)}")


if __name__ == "__main__":
    main()
