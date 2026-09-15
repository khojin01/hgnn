#!/usr/bin/env bash
set -u
root=/home/dms2/hojin_workspace/hgnn
log_dir="$root/.agents/env-status/full-runs/formal118-allset-node-gpu0-20260911"
mkdir -p "$log_dir"; cd "$root"
for spec in \
  'citeseer_cite|0.001|8' \
  'cora_coauth|0.001|4' \
  'imdb|0.001|8' \
  'pubmed_cite|0.001|8' \
  'aminer|0.001|2'; do
  IFS='|' read -r data lr heads <<EOF
$spec
EOF
  log="$log_dir/${data}.log"
  { date -Is; echo "RUN_ID=formal118-allset-node-gpu0-20260911 DATA=$data"; echo "SOURCE=AllSet/118.sh"; echo "COMMAND=conda run -n hgnn-pyg python AllSet/AllSet_train.py --data $data --num_seeds 20 --lr $lr --heads $heads --device cuda:0 --task node"; timeout 45m conda run --no-capture-output -n hgnn-pyg python AllSet/AllSet_train.py --data "$data" --num_seeds 20 --lr "$lr" --heads "$heads" --device cuda:0 --task node; code=$?; echo "EXIT_CODE=$code"; date -Is; } >"$log" 2>&1
  echo "$data $code" >>"$log_dir/status.tsv"
done
