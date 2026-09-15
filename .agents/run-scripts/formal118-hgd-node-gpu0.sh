#!/usr/bin/env bash
set -u
root=/home/dms2/hojin_workspace/hgnn
log_dir="$root/.agents/env-status/full-runs/formal118-hgd-node-gpu0-20260911"
mkdir -p "$log_dir"; cd "$root"
for spec in \
  'citeseer_cite|0.0001|0.3|0.2' \
  'cora_coauth|0.0001|0.1|0.1' \
  'imdb|0.001|0.2|0.1' \
  'pubmed_cite|0.0001|0.4|0.4' \
  'aminer|0.0001|0.2|0.2'; do
  IFS='|' read -r data lr pe px <<EOF
$spec
EOF
  log="$log_dir/${data}.log"
  { date -Is; echo "RUN_ID=formal118-hgd-node-gpu0-20260911 DATA=$data"; echo "SOURCE=H-GD/118.sh"; echo "COMMAND=conda run -n hgnn-pyg python H-GD/H-GD_train.py --data $data --num_seeds 20 --lr $lr --device cuda:0 --task node --p_e $pe --p_x $px"; timeout 45m conda run --no-capture-output -n hgnn-pyg python H-GD/H-GD_train.py --data "$data" --num_seeds 20 --lr "$lr" --device cuda:0 --task node --p_e "$pe" --p_x "$px"; code=$?; echo "EXIT_CODE=$code"; date -Is; } >"$log" 2>&1
  echo "$data $code" >>"$log_dir/status.tsv"
done
