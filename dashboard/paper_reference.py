#!/usr/bin/env python3
"""`HyperGC.pdf`의 Table 3·4·5에서 베이스라인 기준값을 뽑아 JSON으로 굳힌다.

왜 필요한가.  대시보드가 보여주는 Δ는 Clerk 원장이 이미 계산해 둔 값이다.
그 Δ가 정말 논문값 대비인지 확인할 방법이 없으면, 기준이 어긋난 채로 표가
그럴듯하게 보인다.  그래서 논문 쪽 값을 따로 확보해 두고 대조한다.

손으로 옮기지 않는다.  `pdftotext -layout`의 출력에서 표 블록을 찾아 파싱한다.

    python3 dashboard/paper_reference.py          # paper_reference.json 갱신
    python3 dashboard/paper_reference.py --show   # 뽑힌 값 확인
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "HyperGC.pdf"
OUT = Path(__file__).resolve().parent / "paper_reference.json"

# Table 3·4·5가 공유하는 열 순서. 캡션 다음 줄의 머리글과 같다.
DATASETS = ["Citeseer", "Cora", "DBLP-A", "Cora-CA", "IMDB", "House",
            "Pubmed", "DBLP-P", "AMiner", "MN-40", "20News"]

TABLES = {
    "T3": ("Table 3: Accuracy comparison", "node", "Accuracy"),
    "T4": ("Table 4: Accuracy comparison", "edge", "AUROC"),
    "T5": ("Table 5: Accuracy comparison", "community", "NMI"),
}

# Table 3·4는 `평균 ± 표준편차`, Table 5는 평균만 적는다. 둘 다 받는다.
CELL = re.compile(r"(\d+\.\d+\s*±\s*\d+\.\d+|O\.O\.[MT]\.?|\d+\.\d+)")
# 표 안에서 세로로 흐르는 그룹 라벨. 모델 행으로 오인하면 안 된다.
NOT_A_MODEL = re.compile(r"^(Semi-supervised|Self-supervised|Improvement|Table|Figure)")


def pdf_text() -> list[str]:
    if not PDF.is_file():
        raise SystemExit(f"{PDF} 없음")
    if not shutil.which("pdftotext"):
        raise SystemExit("pdftotext가 없다. poppler-utils를 설치한다.")
    done = subprocess.run(["pdftotext", "-layout", str(PDF), "-"],
                          capture_output=True, text=True, check=False)
    if done.returncode != 0:
        raise SystemExit(f"pdftotext 실패: {done.stderr.strip()[:200]}")
    return done.stdout.splitlines()


def parse_table(lines: list[str], caption: str) -> tuple[dict, dict]:
    """(평균 표, 표준편차 표)를 돌려준다.

    평균만 있으면 Δ 계산에는 충분하지만, 원장의 `Table target` 열은
    `41.1 ± 9.8` 형태라 표준편차까지 있어야 고쳐 쓸 수 있다.
    Table 5는 논문이 평균만 싣는다 — 그 경우 std는 None이다.
    """
    start = next((i for i, l in enumerate(lines) if l.strip().startswith(caption)), None)
    if start is None:
        return {}, {}
    end = next((i for i, l in enumerate(lines[start + 1:], start + 1)
                if l.strip().startswith("Table ")), len(lines))

    means: dict[str, dict[str, float | None]] = {}
    stds: dict[str, dict[str, float | None]] = {}
    for line in lines[start:end]:
        text = line.strip()
        if not text or "Citeseer" in text or NOT_A_MODEL.match(text):
            continue
        name = re.match(r"([A-Za-z][A-Za-z0-9\-_ ]*?)\s{2,}", text)
        cells = CELL.findall(text)
        if not name or len(cells) < 11:
            continue
        model = name.group(1).strip()
        # HyperGC50/75/100은 제안 모델이다. HyperGCN·HyperGCL은 베이스라인이므로
        # 접두사로 거르면 안 된다.
        if re.fullmatch(r"HyperGC\d+", model):
            continue
        mean_row: dict[str, float | None] = {}
        std_row: dict[str, float | None] = {}
        for dataset, raw in zip(DATASETS, cells[:11]):
            value = raw.strip()
            if value.startswith("O.O."):
                mean_row[dataset] = std_row[dataset] = None
                continue
            parts = value.split("±")
            mean_row[dataset] = float(parts[0])
            std_row[dataset] = float(parts[1]) if len(parts) > 1 else None
        means[model] = mean_row
        stds[model] = std_row
    return means, stds


def build() -> dict:
    lines = pdf_text()
    tables = {}
    for key, (caption, task, metric) in TABLES.items():
        means, stds = parse_table(lines, caption)
        tables[key] = {"task": task, "metric": metric, "models": means, "stds": stds}
    return {"source": PDF.name, "datasets": DATASETS, "tables": tables}


def main() -> int:
    data = build()
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    for key, table in data["tables"].items():
        print(f"{key} ({table['metric']}): 베이스라인 {len(table['models'])}개")
    print(f"→ {OUT.relative_to(ROOT)}")
    if "--show" in sys.argv:
        for key, table in data["tables"].items():
            print(f"\n=== {key} ===")
            for model, row in table["models"].items():
                cells = " ".join(f"{d}={'—' if v is None else v}" for d, v in row.items())
                print(f"  {model:<12} {cells}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
