#!/usr/bin/env bash
# Formal Table-3 node classification run: available common datasets only.
# Dataset-specific files for DBLP-A, MN-40 and 20News are tracked separately.
set -u
root=/home/dms2/hojin_workspace/hgnn
log_dir="$root/.agents/env-status/full-runs/formal118-unigcn-node-gpu1-20260911"
mkdir -p "$log_dir"; cd "$root"
for spec in \
  'citeseer_cite|0.001' \
  'cora_coauth|0.01' \
  'imdb|0.01' \
  'pubmed_cite|0.001' \
  'aminer|0.001'; do
  IFS='|' read -r data lr <<EOF
$spec
EOF
  log="$log_dir/${data}.log"
  { date -Is; echo "RUN_ID=formal118-unigcn-node-gpu1-20260911 DATA=$data"; echo "SOURCE=UniGCN/118.sh"; echo "COMMAND=conda run -n hgnn-pyg python UniGCN/UniGCN_train.py --data $data --num_seeds 20 --lr $lr --device cuda:1 --task node"; timeout 30m conda run --no-capture-output -n hgnn-pyg python UniGCN/UniGCN_train.py --data "$data" --num_seeds 20 --lr "$lr" --device cuda:1 --task node; code=$?; echo "EXIT_CODE=$code"; date -Is; } >"$log" 2>&1
  echo "$data $code" >>"$log_dir/status.tsv"
done
