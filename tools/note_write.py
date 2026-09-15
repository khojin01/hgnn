#!/usr/bin/env python3
"""관제 아티팩트에서 편집한 연구 노트를 파일에 쓴다. 파일만 쓴다 — 명령을 실행하지 않는다.

    python3 tools/note_write.py < payload.json

payload
  {"kind":"todo","items":[{"text":"...","done":false}, ...]}
      vault/lab/다음 할 일.md 의 체크리스트를 통째로 교체한다. 목록 위의 머리말은 남긴다.
  {"kind":"journal","date":"2026-09-15","text":"# 2026-09-15\n..."}
      vault/lab/일지/<date>.md 의 본문을 교체한다. 프런트매터는 있으면 남기고 없으면 만든다.

출력: 한 줄 JSON {"status":"done|failed","result":"..."}
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LAB = ROOT / "vault" / "lab"
LOG = ROOT / "dashboard" / "orders.log"
KST = timezone(timedelta(hours=9))


def write_todo(items):
    p = LAB / "다음 할 일.md"
    head = []
    if p.exists():
        for l in p.read_text(encoding="utf-8").splitlines():
            if l.startswith("- ["):
                break
            head.append(l)
    if not head:
        head = ["---", "type: lab", "tags: [hgnn/lab]", "---", "", "# 다음 할 일", ""]
    while head and not head[-1].strip():
        head.pop()
    body = []
    for i in items:
        t = str(i.get("text", "")).strip()
        if t:
            body.append("- [x] " + t if i.get("done") else "- [ ] " + t)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("\n".join(head + [""] + body) + "\n", encoding="utf-8")
    return "다음 할 일 %d줄 기록" % len(body)


def write_journal(date, text):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date or ""):
        raise ValueError("날짜 형식이 아니다: %s" % date)
    p = LAB / "일지" / (date + ".md")
    fm = "---\ntype: lab\ndate: %s\ntags: [hgnn/lab]\n---\n" % date
    if p.exists():
        m = re.match(r"^---\n.*?\n---\n", p.read_text(encoding="utf-8"), re.S)
        if m:
            fm = m.group(0)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(fm + "\n" + text.strip() + "\n", encoding="utf-8")
    return "일지 %s.md %d줄 기록" % (date, len(text.splitlines()))


def main():
    try:
        d = json.loads(sys.stdin.read())
        kind = d.get("kind")
        if kind == "todo":
            status, result = "done", write_todo(d.get("items") or [])
        elif kind == "journal":
            status, result = "done", write_journal(d.get("date"), d.get("text") or "")
        else:
            status, result = "failed", "모르는 종류: %s" % kind
    except Exception as e:
        status, result = "failed", "%s: %s" % (type(e).__name__, e)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write("\n[%s] 노트 편집 → %s\n%s\n" % (datetime.now(KST).isoformat(timespec="seconds"), status, result))
    print(json.dumps(dict(status=status, result=result), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
