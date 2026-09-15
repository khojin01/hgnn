#!/usr/bin/env bash
set -u
root=/home/dms2/hojin_workspace/hgnn
log_dir="$root/.agents/env-status/full-runs/formal118-maskgae-node-gpu1-20260911"
mkdir -p "$log_dir"; cd "$root"
for spec in \
  'citeseer_cite|0.0001|0.002|0.5' \
  'cora_coauth|0.001|0.003|0.5' \
  'imdb|0.001|0.001|0.25' \
  'pubmed_cite|0.01|0.002|0.75' \
  'aminer|0.0001|0.002|0.5'; do
  IFS='|' read -r data lr alpha p <<EOF
$spec
EOF
  log="$log_dir/${data}.log"
  { date -Is; echo "RUN_ID=formal118-maskgae-node-gpu1-20260911 DATA=$data"; echo "SOURCE=MaskGAE/118.sh"; echo "COMMAND=conda run -n hgnn-pyg python MaskGAE/MaskGAE_train.py --data $data --num_seeds 20 --lr $lr --device 1 --task node --alpha $alpha --p $p"; timeout 75m conda run --no-capture-output -n hgnn-pyg python MaskGAE/MaskGAE_train.py --data "$data" --num_seeds 20 --lr "$lr" --device 1 --task node --alpha "$alpha" --p "$p"; code=$?; echo "EXIT_CODE=$code"; date -Is; } >"$log" 2>&1
  echo "$data $code" >>"$log_dir/status.tsv"
done
