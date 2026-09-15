#!/usr/bin/env bash
set -u
root=/home/dms2/hojin_workspace/hgnn
log_dir="$root/.agents/env-status/full-runs/formal118-unigin-node-gpu1-20260911"
mkdir -p "$log_dir"; cd "$root"
run_case() {
  local data="$1" lr="$2" code log
  log="$log_dir/${data}.log"
  { date -Is; echo "RUN_ID=formal118-unigin-node-gpu1-20260911 DATA=$data"; echo "SOURCE=UniGIN/118.sh"; echo "COMMAND=conda run -n hgnn-legacy python UniGIN/UniGIN_train.py --data $data --num_seeds 20 --lr $lr --device cuda:1 --task node"; timeout 30m conda run --no-capture-output -n hgnn-legacy python UniGIN/UniGIN_train.py --data "$data" --num_seeds 20 --lr "$lr" --device cuda:1 --task node; code=$?; echo "EXIT_CODE=$code"; date -Is; } >"$log" 2>&1
  echo "$data $code" >>"$log_dir/status.tsv"; return 0
}
run_case citeseer_cite 0.01
run_case cora_coauth 0.01
run_case imdb 0.01
run_case pubmed_cite 0.001
run_case aminer 0.001
