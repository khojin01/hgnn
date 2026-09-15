#!/usr/bin/env bash
# The IMDB process loaded HyperGCL before the edge timing guard was patched.
# Preserve its completed 20-seed aggregate even if the obsolete footer exits 1.
set +e
workspace="/home/dms2/hojin_workspace/hgnn"
pid=1938916
result="$workspace/results/result_imdb_HyperGCL_edge.txt"
log="$workspace/.agents/env-status/full-runs/edge-hypergcl-six-gpu1-20260913/imdb.log"
status="$workspace/.agents/env-status/full-runs/edge-hypergcl-six-gpu1-20260913/status.tsv"

while kill -0 "$pid" 2>/dev/null; do sleep 30; done
sleep 5
if [[ -s "$result" ]] && rg -q 'Final Test:' "$log"; then
  printf 'hypergcl\timdb\tCOMPLETE_RESULT_PRESERVED\t%s\n' "$(date -Is)" >> "$status"
else
  printf 'hypergcl\timdb\tFAILED_NO_COMPLETE_RESULT\t%s\n' "$(date -Is)" >> "$status"
fi
