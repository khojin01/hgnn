#!/usr/bin/env bash
set -u
root=/home/dms2/hojin_workspace/hgnn
log_dir="$root/.agents/env-status/full-runs/formal118-hnhn-node-gpu1-20260911"
mkdir -p "$log_dir"; cd "$root"
run_case() {
  local data="$1" lr="$2" alpha="$3" beta="$4" code log
  log="$log_dir/${data}.log"
  { date -Is; echo "RUN_ID=formal118-hnhn-node-gpu1-20260911 DATA=$data"; echo "SOURCE=HNHN/118.sh (commented fixed configurations)"; echo "COMMAND=conda run -n hgnn-legacy python HNHN/HNHN_train.py --data $data --num_seeds 20 --lr $lr --HNHN_alpha $alpha --HNHN_beta $beta --device cuda:1 --task node"; timeout 30m conda run --no-capture-output -n hgnn-legacy python HNHN/HNHN_train.py --data "$data" --num_seeds 20 --lr "$lr" --HNHN_alpha "$alpha" --HNHN_beta "$beta" --device cuda:1 --task node; code=$?; echo "EXIT_CODE=$code"; date -Is; } >"$log" 2>&1
  echo "$data $code" >>"$log_dir/status.tsv"; return 0
}
run_case citeseer_cite 0.01 0 0
run_case cora_coauth 0.01 -0.5 -1.5
run_case imdb 0.001 0 -1.5
run_case pubmed_cite 0.01 -3 -2.5
run_case aminer 0.001 0.5 0
