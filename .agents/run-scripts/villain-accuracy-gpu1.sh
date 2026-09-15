#!/usr/bin/env bash
set -u
root=/home/dms2/hojin_workspace/hgnn
log_dir="$root/.agents/env-status/full-runs/villain-accuracy-gpu1-20260912"
mkdir -p "$log_dir"; cd "$root"
run() { data=$1; lr=$2; nsg=$3; { date -Is; echo "MODEL=villain-accuracy DATA=$data"; timeout 90m conda run --no-capture-output -n hgnn-pyg python VilLain/eval.py --data "$data" --num_seeds 20 --task node --device 1 --num_step 4 --num_step_gen "$nsg" --lr "$lr"; code=$?; echo "EXIT_CODE=$code"; date -Is; } >"$log_dir/${data}.log" 2>&1; echo "villain $data $code" >>"$log_dir/status.tsv"; }
run citeseer_cite 0.0001 100
run cora_coauth 0.001 100
run imdb 0.01 100
run house 0.0001 100
run pubmed_cite 0.01 10
run aminer 0.01 10
