#!/usr/bin/env bash
set -u
root=/home/dms2/hojin_workspace/hgnn
repair_status="$root/.agents/env-status/full-runs/node-failure-repair-gpu1-20260911/status.tsv"
log_dir="$root/.agents/env-status/full-runs/hypergcl-after-repairs-gpu0-20260911"
mkdir -p "$log_dir"; cd "$root"
# HyperGCL is deliberately deferred until all non-HyperGCL recoveries have a
# terminal status.  VilLain IMDB is the final entry in that dependency queue.
while ! rg -q '^villain-repair imdb ' "$repair_status" 2>/dev/null; do sleep 60; done
run() { data=$1; { date -Is; echo "MODEL=hypergcl DATA=$data"; timeout 8h conda run --no-capture-output -n hgnn-hypergcl python HyperGCL/HyperGCL_train.py --task node --epochs 200 --num_seeds 20 --data "$data" --cuda 0; code=$?; echo "EXIT_CODE=$code"; date -Is; } >"$log_dir/${data}.log" 2>&1; echo "hypergcl $data $code" >>"$log_dir/status.tsv"; }
for data in house citeseer_cite cora_coauth imdb pubmed_cite aminer; do run "$data"; done
