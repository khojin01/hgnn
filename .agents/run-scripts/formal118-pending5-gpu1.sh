#!/usr/bin/env bash
set -u
root=/home/dms2/hojin_workspace/hgnn
house_status="$root/.agents/env-status/full-runs/formal118-house-remaining-gpu0-20260911/status.tsv"
log_dir="$root/.agents/env-status/full-runs/formal118-pending5-gpu1-20260911"
mkdir -p "$log_dir"; cd "$root"
while ! rg -q '^hypergcl ' "$house_status" 2>/dev/null; do sleep 60; done
run() {
  name=$1; data=$2; shift 2
  { date -Is; echo "MODEL=$name DATA=$data"; echo "COMMAND=$*"; timeout 90m "$@"; code=$?; echo "EXIT_CODE=$code"; date -Is; } >"$log_dir/${name}_${data}.log" 2>&1
  echo "$name $data $code" >>"$log_dir/status.tsv"
}
# SE-HSSL settings are the model's supplied node.sh settings, changed only
# from one to the requested twenty fixed splits.
run sehssl citeseer_cite conda run --no-capture-output -n hgnn-pyg python SEHSSL/SEHSSL_train.py --task node --device 1 --num_seeds 20 --dataset citeseer_cite --num_layers 1 --hid_dim 128 --proj_dim 256 --drop_incidence_rate_1 0.1 --drop_incidence_rate_2 0.2 --drop_feature_rate_1 0.1 --drop_feature_rate_2 0.2 --tau 0.35 --tau_n 0.5 --tau_g 0.5 --tau_m 1 --w_g 1 --w_m 0.18 --n_epoch 200 --lr 0.0005 --weight_decay 0.2 --n_ratio 0.45 --e_ratio 0.45 --lr_lr 0.005 --lr_num_epochs 60 --lambda_n 0.00002 --lambda_g 0.00075 --beta 0.65 --K 4 --d 10
run sehssl cora_coauth conda run --no-capture-output -n hgnn-pyg python SEHSSL/SEHSSL_train.py --task node --device 1 --num_seeds 20 --dataset cora_coauth --num_layers 1 --hid_dim 128 --proj_dim 512 --drop_incidence_rate_1 0.05 --drop_incidence_rate_2 0.1 --drop_feature_rate_1 0.05 --drop_feature_rate_2 0.1 --tau 0.5 --tau_n 0.5 --tau_g 0.5 --tau_m 1 --w_g 1 --w_m 0 --n_epoch 200 --lr 0.0005 --weight_decay 0.05 --n_ratio 0.45 --e_ratio 0.45 --lr_lr 0.005 --lr_num_epochs 78 --lambda_n 0.0003 --lambda_g 0.00001 --beta 0.65 --K 4 --d 10
run sehssl imdb conda run --no-capture-output -n hgnn-pyg python SEHSSL/SEHSSL_train.py --task node --device 1 --num_seeds 20 --dataset imdb --drop_incidence_rate_1 0.6 --drop_incidence_rate_2 0.6 --drop_feature_rate_1 0.7 --drop_feature_rate_2 0.7 --tau_n 0.1 --tau_g 0.3 --tau_m 0.9 --w_g 4 --w_m 0.5 --lr 0.001 --hid_dim 128 --proj_dim 128 --weight_decay 1e-06 --num_layers 2 --n_epoch 200
run sehssl pubmed_cite conda run --no-capture-output -n hgnn-pyg python SEHSSL/SEHSSL_train.py --task node --device 1 --num_seeds 20 --dataset pubmed_cite --num_layers 1 --hid_dim 128 --proj_dim 512 --drop_incidence_rate_1 0.1 --drop_incidence_rate_2 0.2 --drop_feature_rate_1 0.1 --drop_feature_rate_2 0.2 --tau 0.5 --tau_n 0.5 --tau_g 0.5 --tau_m 1 --w_g 1 --w_m 0.1 --n_epoch 200 --lr 0.000355 --weight_decay 0.000045 --lr_lr 0.03 --lr_wd 0 --lr_num_epochs 65 --lambda_n 0.0015 --lambda_g 0.0055 --beta 0.65 --K 2 --d 10
run sehssl aminer conda run --no-capture-output -n hgnn-pyg python SEHSSL/SEHSSL_train.py --task node --device 1 --num_seeds 20 --dataset aminer --drop_incidence_rate_1 0.5 --drop_incidence_rate_2 0.5 --drop_feature_rate_1 0.2 --drop_feature_rate_2 0.2 --tau_n 0.6 --tau_g 0.7 --tau_m 1 --w_g 1 --w_m 0.0625 --lr 0.0005 --hid_dim 128 --proj_dim 128 --weight_decay 1e-06 --num_layers 2 --n_epoch 200
for data in citeseer_cite cora_coauth imdb pubmed_cite aminer; do
  run tricl "$data" conda run --no-capture-output -n hgnn-pyg python TriCL/TriCL_train.py --data "$data" --num_seeds 20 --device 1 --task node
done
run villain citeseer_cite conda run --no-capture-output -n hgnn-pyg python VilLain/eval.py --data citeseer_cite --num_seeds 20 --task node --device 1 --num_step 4 --num_step_gen 100 --lr 0.0001
run villain cora_coauth conda run --no-capture-output -n hgnn-pyg python VilLain/eval.py --data cora_coauth --num_seeds 20 --task node --device 1 --num_step 4 --num_step_gen 100 --lr 0.001
run villain imdb conda run --no-capture-output -n hgnn-pyg python VilLain/eval.py --data imdb --num_seeds 20 --task node --device 1 --num_step 4 --num_step_gen 100 --lr 0.01
run villain pubmed_cite conda run --no-capture-output -n hgnn-pyg python VilLain/eval.py --data pubmed_cite --num_seeds 20 --task node --device 1 --num_step 4 --num_step_gen 10 --lr 0.01
run villain aminer conda run --no-capture-output -n hgnn-pyg python VilLain/eval.py --data aminer --num_seeds 20 --task node --device 1 --num_step 4 --num_step_gen 10 --lr 0.01
