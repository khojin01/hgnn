#!/usr/bin/env python3
"""서버 바깥(디스코드 등)에서 온 지시함. 클로드 세션이 여기를 비운다.

    python3 tools/inbox.py add '<json>'   # {"text": "...", "who": "..."} — 한 건 넣는다
    python3 tools/inbox.py list           # 아직 처리 안 한 건만 JSON 한 줄씩
    python3 tools/inbox.py done <id> ...  # 처리했다고 표시한다

관제 아티팩트의 지시는 아티팩트 DB 에 쌓이고 페이지가 세션을 깨운다. 디스코드에는 그런 길이
없어서, 여기에 쌓아 두고 관제 갱신이 돌 때 세션이 가져간다.

파일만 쓴다. 여기 담긴 글로 명령을 만들지 않는다.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOX = ROOT / "dashboard" / "inbox.jsonl"
KST = timezone(timedelta(hours=9))


def load():
    if not BOX.exists():
        return []
    out = []
    for line in BOX.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except Exception:
                pass
    return out


def save(rows):
    BOX.parent.mkdir(parents=True, exist_ok=True)
    BOX.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows[-500:]), encoding="utf-8")


def add(d):
    rows = load()
    now = datetime.now(KST)
    row = {"id": now.strftime("%m%d-%H%M%S"), "at": now.isoformat(timespec="seconds"),
           "who": str(d.get("who", "?"))[:40], "text": str(d.get("text", "")).strip(), "handled": False}
    if not row["text"]:
        print(json.dumps({"status": "failed", "result": "내용이 비어 있다"}, ensure_ascii=False))
        return 0
    rows.append(row)
    save(rows)
    print(json.dumps({"status": "done", "result": "지시함에 넣었다", "id": row["id"]}, ensure_ascii=False))
    return 0


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "add":
        return add(json.loads(sys.argv[2]))
    if cmd == "list":
        for r in load():
            if not r.get("handled"):
                print(json.dumps(r, ensure_ascii=False))
        return 0
    if cmd == "done":
        ids = set(sys.argv[2:])
        rows = load()
        n = 0
        for r in rows:
            if r.get("id") in ids and not r.get("handled"):
                r["handled"] = True
                r["handled_at"] = datetime.now(KST).isoformat(timespec="seconds")
                n += 1
        save(rows)
        print("%d건 처리 표시" % n)
        return 0
    print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main())
