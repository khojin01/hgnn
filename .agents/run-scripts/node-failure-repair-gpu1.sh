#!/usr/bin/env bash
set -u
root=/home/dms2/hojin_workspace/hgnn
log_dir="$root/.agents/env-status/full-runs/node-failure-repair-gpu1-20260911"
mkdir -p "$log_dir"; cd "$root"
run() { name=$1; data=$2; shift 2; { date -Is; echo "MODEL=$name DATA=$data"; echo "COMMAND=$*"; timeout 90m "$@"; code=$?; echo "EXIT_CODE=$code"; date -Is; } >"$log_dir/${name}_${data}.log" 2>&1; echo "$name $data $code" >>"$log_dir/status.tsv"; }
# HyperGRL: process one graph at a time in the DGL evaluator to avoid the
# previous 4–13 GiB batched-clique allocation.
for data in citeseer_cite imdb pubmed_cite aminer; do
  run hypergrl-repair "$data" env DGL_LIBRARY_PATH=/tmp/dgl-v2.1.0-build-r5 LD_LIBRARY_PATH=/tmp/dgl-v2.1.0-build-r5:/home/dms2/miniconda/envs/hgnn-dgl-src/lib conda run --no-capture-output -n hgnn-dgl-src python HyperGRL/hyperGRL_train_our.py --data "$data" --device cuda:1 --num_seeds 20 --batch_size 1
done
# This is a dense-inverse model; run the AMiner case by itself on the empty
# second GPU rather than alongside the prior HyperGRL process.
run phenomnn-repair aminer conda run --no-capture-output -n hgnn-pyg python PhenomNN/PhenomNN_train.py --data aminer --num_seeds 20 --lr 0.01 --device cuda:1 --task node --lam0 10 --lam1 10 --alp 0.1 --prop_step 8
# TriCL's node-classification runner has no --task option.
for data in house citeseer_cite cora_coauth imdb pubmed_cite aminer; do
  run tricl-repair "$data" conda run --no-capture-output -n hgnn-pyg python TriCL/TriCL_train.py --data "$data" --num_seeds 20 --device 1
done
# Produce missing node-pretraining embeddings before evaluation, then merge
# them in the exact filename scheme expected by eval.py.
run villain-pretrain house conda run --no-capture-output -n hgnn-pyg python VilLain/main.py --dataset house --gpu 1 --epochs 5000 --lr 0.0001 --num_step 4 --num_step_gen 100 --task node
run villain-merge house conda run --no-capture-output -n hgnn-pyg python VilLain/emb_concat.py --dataset house --dim 128 --lr 0.0001 --num_step 4 --num_step_gen 100 --task node
run villain-repair house conda run --no-capture-output -n hgnn-pyg python VilLain/eval.py --data house --num_seeds 20 --task node --device 1 --num_step 4 --num_step_gen 100 --lr 0.0001
run villain-pretrain citeseer_cite conda run --no-capture-output -n hgnn-pyg python VilLain/main.py --dataset citeseer_cite --gpu 1 --epochs 5000 --lr 0.0001 --num_step 4 --num_step_gen 100 --task node
run villain-merge citeseer_cite conda run --no-capture-output -n hgnn-pyg python VilLain/emb_concat.py --dataset citeseer_cite --dim 128 --lr 0.0001 --num_step 4 --num_step_gen 100 --task node
run villain-repair citeseer_cite conda run --no-capture-output -n hgnn-pyg python VilLain/eval.py --data citeseer_cite --num_seeds 20 --task node --device 1 --num_step 4 --num_step_gen 100 --lr 0.0001
run villain-pretrain imdb conda run --no-capture-output -n hgnn-pyg python VilLain/main.py --dataset imdb --gpu 1 --epochs 5000 --lr 0.01 --num_step 4 --num_step_gen 100 --task node
run villain-merge imdb conda run --no-capture-output -n hgnn-pyg python VilLain/emb_concat.py --dataset imdb --dim 128 --lr 0.01 --num_step 4 --num_step_gen 100 --task node
run villain-repair imdb conda run --no-capture-output -n hgnn-pyg python VilLain/eval.py --data imdb --num_seeds 20 --task node --device 1 --num_step 4 --num_step_gen 100 --lr 0.01
