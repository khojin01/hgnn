#!/usr/bin/env python3
"""`experiment_now.md` → 대시보드 스냅샷(`state.json`).

Clerk의 라이브 원장 하나만 읽는다. 원장은 표뿐 아니라 최근 완료 소식과
증거 경로도 담고 있으므로, 표만 긁지 않고 문서 전체를 구조화한다.

여기에 더해 원장이 적어 둔 Δ가 **정말 논문값 대비인지** 대조한다.
Δ = 내 평균 − 논문 평균 이므로 (값, Δ)에서 '원장이 가정한 논문값'을 되돌릴 수
있고, 그걸 `paper_reference.json`(HyperGC.pdf에서 뽑은 값)과 비교하면 기준이
어긋난 칸이 드러난다. 원장 값을 고치지는 않는다 — 불일치를 보고만 한다.

    python3 dashboard/paper_reference.py   # 먼저 논문값 확보 (한 번)
    python3 dashboard/collector.py         # state.json 갱신
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DASH = Path(__file__).resolve().parent
SOURCE = ROOT / ".agents" / "clerk-reports" / "experiment_now.md"
REFERENCE = DASH / "paper_reference.json"
STATE = DASH / "state.json"
KST = timezone(timedelta(hours=9))

# 원장 표 제목 → 논문 표 키
TASK_KEY = {
    "Node classification": "T3",
    "Hyperedge prediction": "T4",
    "Community detection": "T5",
}
# 원장의 행 이름 → 논문 표기
MODEL_ALIAS = {"GGD (H-GD)": "GGD", "H-GD (GGD)": "GGD", "HGD": "GGD", "H-GD": "GGD",
               "Hypeboy": "HypeBoy", "EDHNN": "ED-HNN", "SEHSSL": "SE-HSSL",
               "HyperGC": None}   # 제안 모델 — 베이스라인 대조 대상이 아니다
# 원장과 논문이 같은 칸을 가리키는지 판단할 때 허용하는 반올림 오차.
# 원장은 소수 첫째~둘째 자리를 섞어 쓴다.
TOLERANCE = 0.051


def cells(line: str) -> list[str]:
    return [item.strip() for item in line.strip().strip("|").split("|")]


def parse_document(text: str) -> dict:
    """원장을 섹션 단위로 나눈다: 머리말 / 최근 완료 / 표들 / 증거."""
    lines = text.splitlines()
    doc: dict = {"note": "", "updates": {"title": "", "items": []},
                 "tasks": [], "evidence": []}

    heading = ""
    index = 0
    # 'Latest formal completions' 아래에는 완료 소식 목록이 먼저 오고, 빈 줄과
    # 형식 설명 문단을 지나 Δ 범례 목록이 이어진다. 둘 다 같은 `##` 아래라
    # 목록이 한 번 끊기면 그 뒤 항목은 더 받지 않는다.
    updates_closed = False
    while index < len(lines):
        line = lines[index]

        if line.startswith("> "):
            # 머리말 인용문 중 '마지막 확인' 줄만 쓸모가 있다.
            body = line[2:].strip()
            if "마지막 확인" in body or "Last" in body:
                doc["note"] = re.sub(r"\*\*(.*?)\*\*", r"\1", body)
            index += 1
            continue

        if line.startswith("## "):
            heading = line[3:].strip()
            if heading.startswith("Latest formal completions"):
                doc["updates"]["title"] = heading
                updates_closed = False
            index += 1
            continue

        if heading.startswith("Latest formal completions"):
            if line.startswith("- ") and not updates_closed:
                doc["updates"]["items"].append(re.sub(r"\*\*(.*?)\*\*", r"\1", line[2:].strip()))
                index += 1
                continue
            # 목록이 시작된 뒤 본문 줄을 만나면 완료 소식은 끝난 것으로 본다.
            if line.strip() and not line.startswith("- ") and doc["updates"]["items"]:
                updates_closed = True

        if line.startswith("- ") and heading.startswith("Evidence"):
            doc["evidence"].append(re.sub(r"\*\*(.*?)\*\*", r"\1", line[2:].strip()))
            index += 1
            continue

        if line.startswith("|") and index + 1 < len(lines) and "---" in lines[index + 1]:
            header = cells(lines[index])
            index += 2
            rows = []
            while index < len(lines) and lines[index].startswith("|"):
                rows.append(cells(lines[index]))
                index += 1
            base = heading.split("—")[0].strip()
            doc["tasks"].append({
                "title": heading,
                "base": base,
                "metric": heading.split("·")[-1].strip() if "·" in heading else "",
                "key": TASK_KEY.get(base, ""),
                "header": header,
                "rows": rows,
                # 논문 기준값은 attach_reference()가 채운다.
                "reference": {},
            })
            continue

        index += 1
    return doc


def read_value_and_delta(cell: str) -> tuple[float, float] | None:
    """`**41.05 ± 8.26** (Δ **+0.45**)` → (41.05, 0.45). 둘 다 있어야 한다."""
    plain = cell.replace("**", "")
    value = re.search(r"(\d+(?:\.\d+)?)\s*±", plain) or re.match(r"\s*(\d+(?:\.\d+)?)(?=\s)", plain)
    delta = re.search(r"Δ\s*([+−-])\s*([\d.]+)", plain)
    if not value or not delta:
        return None
    sign = 1 if delta.group(1) == "+" else -1
    return float(value.group(1)), sign * float(delta.group(2))


def attach_reference(doc: dict, reference: dict) -> None:
    """각 표에 논문 기준값을 붙인다.

    화면이 보여주는 Δ는 이 값으로 다시 계산한다. 원장에 적힌 Δ를 쓰지 않는
    이유는 `audit()`이 찾아내는 기준 불일치 때문이다 — 측정값은 원장 것을
    그대로 쓰고, 비교 기준만 논문에서 가져온다.
    """
    tables = reference.get("tables", {})
    for task in doc["tasks"]:
        models = tables.get(task["key"], {}).get("models", {})
        if not models:
            continue
        datasets = task["header"][1:]
        for row in task["rows"]:
            paper_row = models.get(MODEL_ALIAS.get(row[0], row[0]))
            if paper_row is None:
                continue
            task["reference"][row[0]] = {ds: paper_row.get(ds) for ds in datasets}


def audit(doc: dict, reference: dict) -> dict:
    """원장 Δ가 가정한 논문값과 실제 논문값을 대조한다."""
    result = {"available": bool(reference), "checked": 0, "agree": 0,
              "mismatch": [], "unmapped": []}
    if not reference:
        return result

    tables = reference.get("tables", {})
    for task in doc["tasks"]:
        table = tables.get(task["key"], {}).get("models", {})
        if not table:
            continue
        datasets = task["header"][1:]
        for row in task["rows"]:
            model = row[0]
            alias = MODEL_ALIAS.get(model, model)
            paper_row = table.get(alias) if alias is not None else None
            if paper_row is None:
                # 논문 표에서 못 찾은 행. 조용히 넘기면 그 행의 Δ가 아무 검증 없이
                # 통과해 버린다 — 실제로 `HGD` 행이 그렇게 Table 3 기준으로 계산된
                # Δ를 들고 통과했다. 이름을 맞추라고 보고한다.
                if alias is not None and any(
                        re.search(r"Δ", c) for c in row[1:]):
                    result["unmapped"].append({"task": task["key"], "model": model,
                                               "cells": sum(1 for c in row[1:]
                                                            if re.search(r"Δ", c))})
                continue
            for dataset, cell in zip(datasets, row[1:]):
                parsed = read_value_and_delta(cell)
                if parsed is None:
                    continue
                mine, delta = parsed
                assumed = round(mine - delta, 2)
                actual = paper_row.get(dataset)
                if actual is None:
                    continue
                result["checked"] += 1
                if abs(assumed - actual) <= TOLERANCE:
                    result["agree"] += 1
                    continue
                # 그 값이 실제로는 어느 행의 것인지 찾아 주면 원인 추적이 쉬워진다.
                owners = [name for name, cols in table.items()
                          if cols.get(dataset) is not None
                          and abs(cols[dataset] - assumed) <= TOLERANCE
                          and name != MODEL_ALIAS.get(model, model)]
                result["mismatch"].append({
                    "task": task["key"], "model": model, "dataset": dataset,
                    "mine": mine, "ledger_delta": delta, "ledger_assumed": assumed,
                    "paper": actual, "true_delta": round(mine - actual, 2),
                    "owners": owners,
                })
    result["mismatch"].sort(key=lambda m: -abs(m["ledger_delta"] - m["true_delta"]))
    return result


def main() -> int:
    if not SOURCE.exists():
        raise SystemExit(f"{SOURCE} 없음")
    doc = parse_document(SOURCE.read_text(encoding="utf-8"))

    reference = {}
    if REFERENCE.exists():
        try:
            reference = json.loads(REFERENCE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            reference = {}

    attach_reference(doc, reference)
    checks = audit(doc, reference)
    STATE.write_text(json.dumps({
        "generated_at": datetime.now(KST).isoformat(),
        "source": str(SOURCE.relative_to(ROOT)),
        "source_mtime": SOURCE.stat().st_mtime,
        "reference_source": reference.get("source", ""),
        "note": doc["note"],
        "updates": doc["updates"],
        "tasks": doc["tasks"],
        "evidence": doc["evidence"],
        "audit": checks,
    }, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"원장 {SOURCE.relative_to(ROOT)}")
    for task in doc["tasks"]:
        print(f"  {task['key']} {task['base']}: 모델 {len(task['rows'])} · 데이터셋 {len(task['header']) - 1}")
    print(f"  최근 완료 {len(doc['updates']['items'])}건 · 증거 {len(doc['evidence'])}건")
    if checks["available"]:
        line = f"  논문 대조: {checks['agree']}/{checks['checked']} 일치 · 불일치 {len(checks['mismatch'])}"
        if checks["unmapped"]:
            names = ", ".join(f"{u['model']}({u['task']}, {u['cells']}칸)"
                              for u in checks["unmapped"])
            line += f" · 미대조 {len(checks['unmapped'])}행 [{names}]"
        print(line)
    else:
        print("  논문 대조 건너뜀 — paper_reference.json 없음")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
