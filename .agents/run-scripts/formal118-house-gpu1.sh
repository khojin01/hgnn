#!/usr/bin/env bash
set -u
root=/home/dms2/hojin_workspace/hgnn; log_dir="$root/.agents/env-status/full-runs/formal118-house-gpu1-20260911"; mkdir -p "$log_dir"; cd "$root"
run(){ name=$1; shift; { date -Is; echo "MODEL=$name DATA=house"; echo "COMMAND=$*"; timeout 75m "$@"; code=$?; echo "EXIT_CODE=$code"; date -Is; } >"$log_dir/$name.log" 2>&1; echo "$name $code" >>"$log_dir/status.tsv"; }
run hgnn conda run --no-capture-output -n hgnn-pyg python HGNN/HGNN_train.py --data house --num_seeds 20 --lr 0.001 --device cuda:1 --task node
run hnhn conda run --no-capture-output -n hgnn-pyg python HNHN/HNHN_train.py --data house --num_seeds 20 --lr 0.001 --HNHN_alpha -2 --HNHN_beta -1 --device cuda:1 --task node
run unigcn conda run --no-capture-output -n hgnn-pyg python UniGCN/UniGCN_train.py --data house --num_seeds 20 --lr 0.01 --device cuda:1 --task node
run unigcn2 conda run --no-capture-output -n hgnn-pyg python UniGCN2/UniGCN2_train.py --data house --num_seeds 20 --lr 0.01 --device cuda:1 --task node
run unigin conda run --no-capture-output -n hgnn-pyg python UniGIN/UniGIN_train.py --data house --num_seeds 20 --lr 0.01 --device cuda:1 --task node
