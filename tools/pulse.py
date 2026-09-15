#!/usr/bin/env python3
"""서버 상태를 한 줄로 요약한다. 클로드 세션이 이 줄이 바뀔 때만 깨어난다.

    python3 tools/pulse.py          # <서명> <사람이 읽는 요약>

시각처럼 매분 바뀌는 값은 넣지 않는다. 여기 담긴 것이 바뀌었을 때만 관제 페이지를
다시 만들 이유가 생긴다. 아무 일도 없으면 줄이 그대로라서 세션은 잠들어 있는다.

  - 돌고 있는 실험 (모델 × 데이터셋 × 태스크)
  - 실행별 종료 상태 (완료 · 실패 · OOM)
  - 자동화 프로세스 on/off
  - git HEAD
  - 열린 할 일 · 열린 질문 수
  - 논문 대조 일치 수
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIVE = ROOT / "dashboard" / "live.json"


def main():
    try:
        d = json.loads(LIVE.read_text(encoding="utf-8"))
    except Exception as e:
        print("없음 live.json 을 읽지 못함: %s" % e)
        return 0

    jobs = sorted("%s/%s/%s" % (j["model"], j["dataset"], j["task"]) for j in d.get("jobs", []))
    term = {r["id"]: dict(r.get("terminal", {})) for r in d.get("runs", [])}
    auto = {a["name"]: bool(a.get("on")) for a in d.get("automation", [])}
    lab = d.get("lab", {})
    todo = [t for t in lab.get("todo", []) if t.startswith("- [ ]")]
    paper = {k: (d.get("paper", {}).get(k) or {}).get("agree") for k in ("T3", "T4", "T5")}
    head = (d.get("git") or {}).get("head")

    state = json.dumps([jobs, term, auto, todo, paper, head, lab.get("questions"),
                        lab.get("latest_journal")], ensure_ascii=False, sort_keys=True)
    sig = hashlib.sha1(state.encode("utf-8")).hexdigest()[:12]

    bits = ["실행 %d" % len(jobs)]
    if jobs:
        bits.append(" · ".join(jobs[:3]))
    done = sum(1 for t in term.values() for s in t.values() if s.startswith("COMPLETE"))
    bad = sum(1 for t in term.values() for s in t.values()
              if "FAIL" in s.upper() or "OOM" in s.upper() or "OOT" in s.upper())
    bits.append("완료 %d · 막힘 %d" % (done, bad))
    bits.append("할 일 %d" % len(todo))
    off = [n for n, on in auto.items() if not on]
    if off:
        bits.append("꺼짐: " + ", ".join(off))
    bits.append("HEAD %s" % head)
    print("%s %s" % (sig, " · ".join(bits)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
