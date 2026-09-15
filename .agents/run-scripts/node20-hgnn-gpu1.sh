#!/usr/bin/env bash
set -u
root=/home/dms2/hojin_workspace/hgnn
log_dir="$root/.agents/env-status/full-runs/node20-hgnn-gpu1-20260911"
mkdir -p "$log_dir"
cd "$root"

run_case() {
  local data="$1"
  local lr="$2"
  local log="$log_dir/${data}.log"
  {
    date -Is
    echo "RUN_ID=node20-hgnn-gpu1-20260911 DATA=$data"
    echo "COMMAND=conda run -n hgnn-legacy python HGNN/HGNN_train.py --data $data --num_seeds 20 --lr $lr --device cuda:1 --task node --epoch 20"
    timeout 30m conda run --no-capture-output -n hgnn-legacy python HGNN/HGNN_train.py --data "$data" --num_seeds 20 --lr "$lr" --device cuda:1 --task node --epoch 20
    code=$?
    echo "EXIT_CODE=$code"
    date -Is
  } >"$log" 2>&1
  echo "$data $code" >>"$log_dir/status.tsv"
  return 0
}

run_case dblp_copub 0.01
run_case cora_coauth 0.01
run_case imdb 0.01
run_case pubmed_cite 0.001
run_case aminer 0.01
run_case modelnet_40 0.01
run_case news 0.001
