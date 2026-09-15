#!/usr/bin/env bash
set -u
root=/home/dms2/hojin_workspace/hgnn
log_dir="$root/.agents/env-status/full-runs/formal118-graphmae2-node-gpu1-20260911"
mkdir -p "$log_dir"; cd "$root"
for spec in \
  'citeseer_cite|0.0001|0.5' \
  'cora_coauth|0.0001|0.5' \
  'imdb|0.001|0.75' \
  'pubmed_cite|0.01|0.5' \
  'aminer|0.0001|0.5'; do
  IFS='|' read -r data lr mask_rate <<EOF
$spec
EOF
  log="$log_dir/${data}.log"
  { date -Is; echo "RUN_ID=formal118-graphmae2-node-gpu1-20260911 DATA=$data"; echo "SOURCE=GraphMAE2/118.sh"; echo "CHECKPOINT=none (pretrain runs in-process)"; echo "COMMAND=DGL_LIBRARY_PATH=/tmp/dgl-v2.1.0-build-r5 LD_LIBRARY_PATH=/tmp/dgl-v2.1.0-build-r5:/home/dms2/miniconda/envs/hgnn-dgl-src/lib conda run -n hgnn-dgl-src python GraphMAE2/GraphMAE2_train.py --data $data --num_seeds 20 --lr $lr --mask_rate $mask_rate --device 1 --task node"; timeout 60m env DGL_LIBRARY_PATH=/tmp/dgl-v2.1.0-build-r5 LD_LIBRARY_PATH=/tmp/dgl-v2.1.0-build-r5:/home/dms2/miniconda/envs/hgnn-dgl-src/lib conda run --no-capture-output -n hgnn-dgl-src python GraphMAE2/GraphMAE2_train.py --data "$data" --num_seeds 20 --lr "$lr" --mask_rate "$mask_rate" --device 1 --task node; code=$?; echo "EXIT_CODE=$code"; date -Is; } >"$log" 2>&1
  echo "$data $code" >>"$log_dir/status.tsv"
done
