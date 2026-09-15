"""정적 리포트(`hypergc-report.html`)를 만든다. 손으로 옮기는 값은 하나도 없다.

원장(state.json)의 측정값 + 논문(paper_reference.json)의 기준값 →
Δ를 여기서 직접 계산한다. 원장이 적어 둔 Δ는 대조용으로만 따로 싣는다.
"""
import hashlib
import json
import re
from pathlib import Path

DASH = Path(__file__).resolve().parent
state = json.loads((DASH / "state.json").read_text(encoding="utf-8"))
ref = json.loads((DASH / "paper_reference.json").read_text(encoding="utf-8"))

ALIAS = {"GGD (H-GD)": "GGD", "Hypeboy": "HypeBoy", "EDHNN": "ED-HNN"}
STATES = [
    (r"O\.O\.[MT]", "limit", "OOM/OOT"),
    (r"blocked-data", "blocked", "데이터 결손"),
    (r"timeout-repair", "blocked", "시간 초과·복구 중"),
    (r"timeout", "blocked", "시간 초과"),
    (r"NMI-only", "blocked", "NMI 전용 러너"),
    (r"deferred", "blocked", "보류"),
    (r"metric collecting", "running", "수치 수집 중"),
    (r"running", "running", "실행 중"),
    (r"pending", "pending", "대기"),
]


def parse(raw):
    plain = str(raw or "").replace("**", "").strip()
    out = {"mean": None, "std": None, "ledger_delta": None, "grade": None,
           "state": None, "label": ""}
    if not plain or plain == "—":
        out.update(state="pending", label="대기")
        return out
    d = re.search(r"Δ\s*([+−-])\s*([\d.]+)", plain)
    if d:
        out["ledger_delta"] = (1 if d.group(1) == "+" else -1) * float(d.group(2))
    v = re.search(r"(\d+(?:\.\d+)?)\s*±\s*(nan|[\d.]+)", plain, re.I)
    if v:
        out["mean"] = float(v.group(1))
        out["std"] = None if v.group(2).lower() == "nan" else float(v.group(2))
    else:
        b = re.match(r"(\d+(?:\.\d+)?)(?=\s)", plain)
        if b:
            out["mean"] = float(b.group(1))
    if out["mean"] is not None:
        if re.search(r"formal", plain, re.I) or "**" in str(raw):
            out["grade"] = "formal"
        elif re.search(r"source-1split", plain, re.I):
            out["grade"] = "1split"
        elif re.search(r"smoke", plain, re.I):
            out["grade"] = "smoke"
        return out
    for pattern, st, label in STATES:
        if re.search(pattern, plain, re.I):
            out.update(state=st, label=label)
            return out
    out.update(state="pending", label=plain.lstrip("— ")[:28] or "대기")
    return out


tasks, mismatches, outliers = [], [], []
for task in state["tasks"]:
    key = task["key"]
    paper_models = ref["tables"].get(key, {}).get("models", {})
    datasets = task["header"][1:]
    rows = []
    for raw_row in task["rows"]:
        name = raw_row[0]
        prow = paper_models.get(ALIAS.get(name, name), {})
        cells = []
        for ds, raw in zip(datasets, raw_row[1:]):
            c = parse(raw)
            c["paper"] = prow.get(ds)
            c["delta"] = (round(c["mean"] - c["paper"], 2)
                          if c["mean"] is not None and c["paper"] is not None else None)
            # 논문이 O.O.M/O.O.T로 보고한 칸은 재현 대상이 아니다
            if c["mean"] is None and c["paper"] is None and ds in ref["datasets"] and prow:
                c["state"], c["label"] = "limit", "OOM/OOT"
            cells.append(c)
            if c["delta"] is not None and abs(c["delta"]) > 3:
                outliers.append({"task": key, "model": name, "ds": ds,
                                 "mine": c["mean"], "paper": c["paper"], "delta": c["delta"]})
            if c["ledger_delta"] is not None and c["delta"] is not None:
                assumed = round(c["mean"] - c["ledger_delta"], 2)
                if abs(assumed - c["paper"]) > 0.051:
                    owners = [m for m, cols in paper_models.items()
                              if cols.get(ds) is not None
                              and abs(cols[ds] - assumed) <= 0.051
                              and m != ALIAS.get(name, name)]
                    mismatches.append({"task": key, "model": name, "ds": ds,
                                       "mine": c["mean"], "assumed": assumed,
                                       "paper": c["paper"], "ledger_delta": c["ledger_delta"],
                                       "delta": c["delta"], "owners": owners})
        rows.append({"name": name, "cells": cells})
    live = [i for i, _ in enumerate(datasets)
            if any(r["cells"][i]["mean"] is not None for r in rows)]
    tasks.append({"key": key, "base": task["base"], "metric": task["metric"],
                  "datasets": datasets, "rows": rows, "live": live})

# 분할이 어긋나 Δ가 성립하지 않던 행은 2026-09-12에 정정·재실행했다.
# 남겨 두는 이유는 값이 왜 크게 바뀌었는지 읽는 사람이 알 수 있게 하기 위해서다.
CAVEATS = {}

outliers.sort(key=lambda o: -abs(o["delta"]))
mismatches.sort(key=lambda m: -abs(m["ledger_delta"] - m["delta"]))

flat = [c for t in tasks for r in t["rows"] for i, c in enumerate(r["cells"]) if i in t["live"]]
withd = [c for c in flat if c["delta"] is not None]
absd = sorted(abs(c["delta"]) for c in withd)

payload = {
    "generated_at": state["generated_at"],
    "note": state["note"],
    "updates": state["updates"],
    "evidence": state["evidence"],
    "tasks": tasks,
    "mismatches": mismatches,
    "outliers": outliers,
    "caveats": [{"model": m, "task": t, **v} for (m, t), v in CAVEATS.items()],
    "summary": {
        "matched": sum(1 for c in withd if abs(c["delta"]) <= 2),
        "compared": len(withd),
        "median": round(absd[len(absd) // 2], 2) if absd else None,
        "formal": sum(1 for c in flat if c["grade"] == "formal"),
        "cells": len(flat),
        "outliers": len(outliers),
        "pending": sum(1 for c in flat if c["mean"] is None),
        "mismatches": len(mismatches),
    },
}

# 페이로드를 템플릿에 구워 정적 리포트를 만든다. 발행만 따로 하면 된다.
#
# 데이터가 그대로면 파일을 다시 쓰지 않는다. `generated_at`은 실행할 때마다
# 바뀌므로 무조건 쓰면 mtime·해시가 매번 달라지고, 발행 여부를 그걸로 판단하는
# 쪽에서 내용이 같은데도 매번 새로 발행하게 된다.
template = DASH / "report_template.html"
report = DASH / "hypergc-report.html"
fingerprint_path = DASH / ".report-fingerprint"

core = {k: v for k, v in payload.items() if k != "generated_at"}
fingerprint = hashlib.sha256(
    json.dumps(core, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()

previous = fingerprint_path.read_text(encoding="utf-8").strip() if fingerprint_path.exists() else ""
if fingerprint == previous and report.exists():
    print("데이터 변경 없음 — 리포트 그대로 둔다")
    changed = False
else:
    report.write_text(
        template.read_text(encoding="utf-8").replace(
            "__PAYLOAD__", json.dumps(payload, ensure_ascii=False, separators=(",", ":"))),
        encoding="utf-8")
    fingerprint_path.write_text(fingerprint + "\n", encoding="utf-8")
    changed = True
out = report

s = payload["summary"]
print(f"대조 {s['matched']}/{s['compared']} (±2 이내) · 중앙값 {s['median']}")
print(f"정식 {s['formal']}/{s['cells']} · 이상치 {s['outliers']} · 미실행 {s['pending']}")
print(f"원장 Δ 불일치 {s['mismatches']}")
print(f"리포트 {out.name} {out.stat().st_size} bytes {'(갱신)' if changed else '(변경 없음)'}")
print("\n이상치 상위 8 (내가 계산한 Δ 기준):")
for o in outliers[:8]:
    print(f"  {o['task']} {o['model']:<12} {o['ds']:<9} {o['mine']:>6} vs {o['paper']:>6}  {o['delta']:+.2f}")
