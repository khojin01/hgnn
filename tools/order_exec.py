#!/usr/bin/env python3
"""관제 아티팩트에서 온 지시를 연구 노트에 적는다. 파일만 쓴다 — 명령을 실행하지 않는다.

    python3 tools/order_exec.py '<json>'
    json: {"id","kind":"todo|run|stop|free","model","dataset","task","gpu","text"}

출력: 한 줄 JSON {"status": "done|failed", "result": "..."}
모든 지시는 dashboard/orders.log 에 남는다.

kind
  todo  lab/다음 할 일.md 맨 위 항목에 추가
  free  같은 곳에 "[지시]" 로 추가
  run   같은 곳에 "[실행 요청]" 으로 추가. 실제 실행은 클로드 세션이 protocols/ 를 읽고 판단해서 한다.
  stop  같은 곳에 "[중지 요청]" 으로 추가. 실제 중지도 클로드 세션이 한다.

웹 폼에서 온 글로 셸 명령을 만들지 않는다. 실행·중지는 사람이 보는 세션 안에서 클로드가 결정한다.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TODO = ROOT / "vault" / "lab" / "다음 할 일.md"
LOG = ROOT / "dashboard" / "orders.log"
KST = timezone(timedelta(hours=9))
LABEL = {"todo": "", "free": "[지시] ", "run": "[실행 요청] ", "stop": "[중지 요청] "}


def now():
    return datetime.now(KST)


def add_todo(text, tag):
    lines = TODO.read_text(encoding="utf-8").splitlines() if TODO.exists() else ["# 다음 할 일", ""]
    entry = f"- [ ] {text}  ({tag} {now().strftime('%m-%d %H:%M')})"
    for i, l in enumerate(lines):
        if l.startswith("- ["):
            lines.insert(i, entry)
            break
    else:
        lines += [entry]
    TODO.parent.mkdir(parents=True, exist_ok=True)
    TODO.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return entry


def main():
    order = json.loads(sys.argv[1])
    kind = order.get("kind", "")
    text = (order.get("text") or "").strip()
    if kind == "run":
        text = f"{order.get('model')} × {order.get('dataset')} {order.get('task')} GPU{order.get('gpu')}" + (f" — {text}" if text else "")
    if kind not in LABEL:
        status, result = "failed", f"모르는 종류: {kind}"
    elif not text:
        status, result = "failed", "내용이 비어 있다"
    else:
        try:
            status, result = "done", "다음 할 일에 추가: " + add_todo(LABEL[kind] + text, f"관제 지시 {order.get('id', '?')[:8]}")
        except Exception as e:
            status, result = "failed", f"{type(e).__name__}: {e}"
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"\n[{now().isoformat(timespec='seconds')}] 관제 지시 {order.get('id', '?')} {kind} → {status}\n{json.dumps(order, ensure_ascii=False)}\n{result}\n")
    print(json.dumps(dict(status=status, result=result), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
