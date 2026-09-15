#!/usr/bin/env bash
set -u
root=/home/dms2/hojin_workspace/hgnn
gpu0_status="$root/.agents/env-status/full-runs/formal118-hypergcn-recovery-gpu0-20260911/status.tsv"
gpu1_status="$root/.agents/env-status/full-runs/formal118-hypergcn-recovery-gpu1-20260911/status.tsv"
log_dir="$root/.agents/env-status/full-runs/continue-after-hypergcn-20260911"
mkdir -p "$log_dir"; cd "$root"
# Both remaining HyperGCN datasets must first reach a terminal result.
while ! { rg -q '^hypergcn pubmed_cite ' "$gpu0_status" 2>/dev/null && rg -q '^hypergcn aminer ' "$gpu1_status" 2>/dev/null; }; do sleep 60; done
date -Is > "$log_dir/hypergcn-complete-at.txt"
# Resume the non-HyperGCL repair work on GPU 1.  It contains HyperGRL,
# PhenomNN, TriCL and VilLain in dependency order.
exec bash "$root/.agents/run-scripts/node-failure-repair-gpu1.sh"
