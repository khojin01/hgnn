#!/usr/bin/env bash
set -u
root=/home/dms2/hojin_workspace/hgnn; log_dir="$root/.agents/env-status/full-runs/formal118-house-gpu0-20260911"; mkdir -p "$log_dir"; cd "$root"
run(){ name=$1; shift; { date -Is; echo "MODEL=$name DATA=house"; echo "COMMAND=$*"; timeout 75m "$@"; code=$?; echo "EXIT_CODE=$code"; date -Is; } >"$log_dir/$name.log" 2>&1; echo "$name $code" >>"$log_dir/status.tsv"; }
run allset conda run --no-capture-output -n hgnn-pyg python AllSet/AllSet_train.py --data house --num_seeds 20 --lr 0.0001 --heads 8 --device cuda:0 --task node
run edhnn conda run --no-capture-output -n hgnn-pyg python EDHNN/EDHNN_train.py --data house --num_seeds 20 --lr 0.01 --restart_alpha 1 --device cuda:0 --task node
run mlp conda run --no-capture-output -n hgnn-pyg python MLP/MLP_train.py --data house --num_seeds 20 --lr 0.01 --task node
run hgd conda run --no-capture-output -n hgnn-pyg python H-GD/H-GD_train.py --data house --num_seeds 20 --lr 0.0001 --device cuda:0 --task node --p_e 0.2 --p_x 0.3
run hypeboy conda run --no-capture-output -n hgnn-pyg python Hypeboy/Hypeboy_train.py --data house --num_seeds 20 --device cuda:0 --task node
run hypergcn conda run --no-capture-output -n hgnn-pyg python HyperGCN/HyperGCN_train.py --data house --num_seeds 20 --lr 0.01 --device cuda:0 --task node
