#!/usr/bin/env bash
set -u
root=/home/dms2/hojin_workspace/hgnn
log_dir="$root/.agents/env-status/full-runs/formal118-hypergcn-recovery-gpu0-20260911"
mkdir -p "$log_dir"; cd "$root"
{ date -Is; echo "MODEL=hypergcn DATA=pubmed_cite"; echo "CONFIG=HyperGCN/118.sh"; timeout 8h conda run --no-capture-output -n hgnn-pyg python HyperGCN/HyperGCN_train.py --data pubmed_cite --num_seeds 20 --lr 0.01 --device cuda:0 --task node; code=$?; echo "EXIT_CODE=$code"; date -Is; } >"$log_dir/pubmed_cite.log" 2>&1
echo "hypergcn pubmed_cite $code" >>"$log_dir/status.tsv"
