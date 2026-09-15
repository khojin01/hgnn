#!/usr/bin/env bash
set -u
root=/home/dms2/hojin_workspace/hgnn
log_dir="$root/.agents/env-status/full-runs/formal118-house-remaining-gpu1-20260911"
mkdir -p "$log_dir"; cd "$root"
run() { name=$1; shift; { date -Is; echo "MODEL=$name DATA=house"; echo "COMMAND=$*"; timeout 90m "$@"; code=$?; echo "EXIT_CODE=$code"; date -Is; } >"$log_dir/$name.log" 2>&1; echo "$name $code" >>"$log_dir/status.tsv"; }
run sehssl conda run --no-capture-output -n hgnn-pyg python SEHSSL/SEHSSL_train.py --task node --device 1 --num_seeds 20 --dataset house --drop_incidence_rate_1 0.7 --drop_incidence_rate_2 0.7 --drop_feature_rate_1 0.5 --drop_feature_rate_2 0.5 --tau_n 0.3 --tau_g 0.9 --tau_m 0.8 --w_g 0.25 --w_m 2 --lr 0.001 --hid_dim 128 --proj_dim 128 --weight_decay 1e-06 --num_layers 2 --n_epoch 200
run tricl conda run --no-capture-output -n hgnn-pyg python TriCL/TriCL_train.py --data house --num_seeds 20 --device 1 --task node
run villain conda run --no-capture-output -n hgnn-pyg python VilLain/eval.py --data house --num_seeds 20 --task node --device 1 --num_step 4 --num_step_gen 100 --lr 0.0001
