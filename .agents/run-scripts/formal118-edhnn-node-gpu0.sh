#!/usr/bin/env bash
set -u
root=/home/dms2/hojin_workspace/hgnn
log_dir="$root/.agents/env-status/full-runs/formal118-edhnn-node-gpu0-20260911"
mkdir -p "$log_dir"; cd "$root"
run_case() {
  local data="$1" lr="$2" alpha="$3" code log
  log="$log_dir/${data}.log"
  { date -Is; echo "RUN_ID=formal118-edhnn-node-gpu0-20260911 DATA=$data"; echo "SOURCE=EDHNN/118.sh"; echo "COMMAND=conda run -n hgnn-pyg python EDHNN/EDHNN_train.py --data $data --lr $lr --restart_alpha $alpha --device cuda:0 --task node --num_seeds 20"; timeout 30m conda run --no-capture-output -n hgnn-pyg python EDHNN/EDHNN_train.py --data "$data" --lr "$lr" --restart_alpha "$alpha" --device cuda:0 --task node --num_seeds 20; code=$?; echo "EXIT_CODE=$code"; date -Is; } >"$log" 2>&1
  echo "$data $code" >>"$log_dir/status.tsv"; return 0
}
run_case citeseer_cite 0.001 0.7
run_case cora_coauth 0.001 0.8
run_case imdb 0.001 1
run_case pubmed_cite 0.01 1
run_case aminer 0.01 0.9
