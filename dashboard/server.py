#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime, timezone, timedelta

HERE = Path(__file__).resolve().parent
STATE = HERE / "state.json"
EVENTS = HERE / "webhook-events.jsonl"
KST = timezone(timedelta(hours=9))

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw): super().__init__(*a, directory=str(HERE), **kw)
    def log_message(self, *_): pass
    def send_json(self, payload, status=200):
        body=json.dumps(payload,ensure_ascii=False).encode(); self.send_response(status)
        self.send_header("Content-Type","application/json; charset=utf-8"); self.send_header("Cache-Control","no-store")
        self.send_header("Content-Length",str(len(body))); self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        if urlparse(self.path).path == "/api/state":
            self.send_json(json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {"tasks":[]}); return
        if self.path == "/": self.path = "/index.html"
        super().do_GET()
    def do_POST(self):
        if urlparse(self.path).path != "/api/webhook": self.send_json({"error":"not found"},404); return
        size=int(self.headers.get("Content-Length","0")); raw=self.rfile.read(min(size,1_000_000))
        try: payload=json.loads(raw)
        except json.JSONDecodeError: self.send_json({"error":"invalid json"},400); return
        payload["received_at"]=datetime.now(KST).isoformat()
        with EVENTS.open("a",encoding="utf-8") as f: f.write(json.dumps(payload,ensure_ascii=False)+"\n")
        self.send_json({"ok":True,"received_at":payload["received_at"]},202)

parser=argparse.ArgumentParser(); parser.add_argument("--host",default="0.0.0.0"); parser.add_argument("--port",type=int,default=8765)
if __name__ == "__main__":
    args=parser.parse_args(); print(f"Task dashboard: http://{args.host}:{args.port}/",flush=True)
    ThreadingHTTPServer((args.host,args.port),Handler).serve_forever()
