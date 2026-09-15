#!/usr/bin/env bash
set -u
root=/home/dms2/hojin_workspace/hgnn
log_dir="$root/.agents/env-status/full-runs/formal118-hypergcn-node-gpu0-20260911"
mkdir -p "$log_dir"; cd "$root"
for data in citeseer_cite cora_coauth imdb pubmed_cite aminer; do
  log="$log_dir/${data}.log"
  { date -Is; echo "RUN_ID=formal118-hypergcn-node-gpu0-20260911 DATA=$data"; echo "SOURCE=HyperGCN/118.sh"; echo "COMMAND=conda run -n hgnn-pyg python HyperGCN/HyperGCN_train.py --data $data --num_seeds 20 --lr 0.01 --device cuda:0 --task node"; timeout 30m conda run --no-capture-output -n hgnn-pyg python HyperGCN/HyperGCN_train.py --data "$data" --num_seeds 20 --lr 0.01 --device cuda:0 --task node; code=$?; echo "EXIT_CODE=$code"; date -Is; } >"$log" 2>&1
  echo "$data $code" >>"$log_dir/status.tsv"
done
