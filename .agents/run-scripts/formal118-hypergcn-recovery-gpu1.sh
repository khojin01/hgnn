#!/usr/bin/env bash
set -u
root=/home/dms2/hojin_workspace/hgnn
log_dir="$root/.agents/env-status/full-runs/formal118-hypergcn-recovery-gpu1-20260911"
mkdir -p "$log_dir"; cd "$root"
{ date -Is; echo "MODEL=hypergcn DATA=aminer"; echo "CONFIG=HyperGCN/118.sh"; timeout 8h conda run --no-capture-output -n hgnn-pyg python HyperGCN/HyperGCN_train.py --data aminer --num_seeds 20 --lr 0.01 --device cuda:1 --task node; code=$?; echo "EXIT_CODE=$code"; date -Is; } >"$log_dir/aminer.log" 2>&1
echo "hypergcn aminer $code" >>"$log_dir/status.tsv"
