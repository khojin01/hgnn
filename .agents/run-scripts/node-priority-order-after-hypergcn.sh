#!/usr/bin/env bash
set -u
root=/home/dms2/hojin_workspace/hgnn
log_dir="$root/.agents/env-status/full-runs/node-priority-order-20260911"
mkdir -p "$log_dir"; cd "$root"
while ! { rg -q '^hypergcn pubmed_cite ' "$root/.agents/env-status/full-runs/formal118-hypergcn-recovery-gpu0-20260911/status.tsv" 2>/dev/null && rg -q '^hypergcn aminer ' "$root/.agents/env-status/full-runs/formal118-hypergcn-recovery-gpu1-20260911/status.tsv" 2>/dev/null; }; do sleep 60; done
run() { model=$1; data=$2; shift 2; { date -Is; echo "MODEL=$model DATA=$data"; echo "COMMAND=$*"; timeout 90m "$@"; code=$?; echo "EXIT_CODE=$code"; date -Is; } >"$log_dir/${model}_${data}.log" 2>&1; echo "$model $data $code" >>"$log_dir/status.tsv"; }
run_long() { model=$1; data=$2; shift 2; { date -Is; echo "MODEL=$model DATA=$data"; echo "COMMAND=$*"; timeout 8h "$@"; code=$?; echo "EXIT_CODE=$code"; date -Is; } >"$log_dir/${model}_${data}.log" 2>&1; echo "$model $data $code" >>"$log_dir/status.tsv"; }
note_done() { echo "$1 already-complete" >>"$log_dir/status.tsv"; }
# 1. HyperGCN just completed above.  2. MaskGAE passed all six current cells.
note_done maskgae
# 3. PhenomNN: only AMiner needs recovery.
run phenomnn aminer conda run --no-capture-output -n hgnn-pyg python PhenomNN/PhenomNN_train.py --data aminer --num_seeds 20 --lr 0.01 --device cuda:0 --task node --lam0 10 --lam1 10 --alp 0.1 --prop_step 8
# 4. SE-HSSL passed its six current cells.
note_done sehssl
# 5. TriCL: rerun all six without the unsupported --task argument.
for data in house citeseer_cite cora_coauth imdb pubmed_cite aminer; do run tricl "$data" conda run --no-capture-output -n hgnn-pyg python TriCL/TriCL_train.py --data "$data" --num_seeds 20 --device 0; done
# 6. UniGCN2 passed its six current cells.
note_done unigcn2
# 7. VilLain: only House, Citeseer and IMDB lack pretraining embeddings.
for spec in 'house|0.0001|100' 'citeseer_cite|0.0001|100' 'imdb|0.01|100'; do
  IFS='|' read -r data lr nsg <<EOF
$spec
EOF
  run villain-pretrain "$data" conda run --no-capture-output -n hgnn-pyg python VilLain/main.py --dataset "$data" --gpu 0 --epochs 5000 --lr "$lr" --num_step 4 --num_step_gen "$nsg" --task node
  run villain-merge "$data" conda run --no-capture-output -n hgnn-pyg python VilLain/emb_concat.py --dataset "$data" --dim 128 --lr "$lr" --num_step 4 --num_step_gen "$nsg" --task node
  run villain "$data" conda run --no-capture-output -n hgnn-pyg python VilLain/eval.py --data "$data" --num_seeds 20 --task node --device 0 --num_step 4 --num_step_gen "$nsg" --lr "$lr"
done
# 8. HyperGRL: retry only its OOM cells using a single graph per DGL batch.
for data in citeseer_cite imdb pubmed_cite aminer; do run hypergrl "$data" env DGL_LIBRARY_PATH=/tmp/dgl-v2.1.0-build-r5 LD_LIBRARY_PATH=/tmp/dgl-v2.1.0-build-r5:/home/dms2/miniconda/envs/hgnn-dgl-src/lib conda run --no-capture-output -n hgnn-dgl-src python HyperGRL/hyperGRL_train_our.py --data "$data" --device cuda:0 --num_seeds 20 --batch_size 1; done
# 9. HyperGCL is strictly last.
for data in house citeseer_cite cora_coauth imdb pubmed_cite aminer; do run_long hypergcl "$data" conda run --no-capture-output -n hgnn-hypergcl python HyperGCL/HyperGCL_train.py --task node --epochs 200 --num_seeds 20 --data "$data" --cuda 0; done
