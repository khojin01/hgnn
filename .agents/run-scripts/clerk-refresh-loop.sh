#!/usr/bin/env bash
# Project-local periodic clerk refresh.  No system cron is used.
set -u
ROOT="/home/dms2/hojin_workspace/hgnn"
LOG="$ROOT/.agents/env-status/clerk-refresh-loop.log"
PIDFILE="$ROOT/.agents/env-status/clerk-refresh-loop.pid"
echo "$$" > "$PIDFILE"
cleanup() { rm -f "$PIDFILE"; exit 0; }
trap cleanup INT TERM EXIT
while true; do
  date '+[%F %T %Z] clerk 갱신' >> "$LOG"
  python3 "$ROOT/.agents/run-scripts/clerk_refresh.py" >> "$LOG" 2>&1
  # Refresh the clerk report and dashboard artifact every 10 minutes.
  sleep 600
done
