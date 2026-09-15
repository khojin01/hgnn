# Clerk 30-minute refresh procedure

The periodic worker is [clerk-refresh-loop.sh](../run-scripts/clerk-refresh-loop.sh).
It invokes `clerk_refresh.py` every 1,800 seconds and appends its audit output to
`.agents/env-status/clerk-refresh-loop.log`. Its PID is recorded in
`.agents/env-status/clerk-refresh-loop.pid` while the worker is alive.

## Safety contract

- Only `results/result_<dataset>_<model>_<task>.txt` files are considered.
- A value is written only when the **final** metric record contains exactly 20
  raw values and an adjacent `mean ± std` summary. Plain arrays and
  `tensor([...])` arrays are both supported.
- The model, dataset column, and matching HyperGC paper value must already be
  known. The script computes `Δ = measured mean − paper mean`; it never
  estimates a metric.
- It fills only an em-dash (`—`) cell in an existing row. Existing measurements,
  `running`, `O.O.M`, and manually documented diagnostics are never overwritten.
- Unrecognised filenames, partial arrays, missing paper references, or absent
  rows are appended to `clerk-refresh-queue.md` for a human/clerk review.
- Every pass invokes `dashboard/collector.py`, including a no-op pass.

## Manual operation

Run one safe incremental pass:

```bash
python3 .agents/run-scripts/clerk_refresh.py
```

Inspect queued exceptions and worker health:

```bash
tail -n 80 .agents/clerk-reports/clerk-refresh-queue.md
tail -n 80 .agents/env-status/clerk-refresh-loop.log
ps -p "$(cat .agents/env-status/clerk-refresh-loop.pid)" -o pid,etime,cmd
```

Do not edit `.clerk-refresh-state.json` to force an old file through the parser.
If a previously completed result needs correction, review the raw log/result and
update the ledger intentionally; the refresh worker is deliberately append-only
for blank cells.
