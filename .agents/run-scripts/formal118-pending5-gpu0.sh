#!/usr/bin/env bash
set -u
root=/home/dms2/hojin_workspace/hgnn
house_status="$root/.agents/env-status/full-runs/formal118-house-remaining-gpu0-20260911/status.tsv"
log_dir="$root/.agents/env-status/full-runs/formal118-pending5-gpu0-20260911"
mkdir -p "$log_dir"; cd "$root"
# Do not begin these five-dataset jobs until the House priority queue, ending
# in HyperGCL, has a terminal result.
while ! rg -q '^hypergcl ' "$house_status" 2>/dev/null; do sleep 60; done
run() {
  name=$1; data=$2; shift 2
  { date -Is; echo "MODEL=$name DATA=$data"; echo "COMMAND=$*"; timeout 90m "$@"; code=$?; echo "EXIT_CODE=$code"; date -Is; } >"$log_dir/${name}_${data}.log" 2>&1
  echo "$name $data $code" >>"$log_dir/status.tsv"
}
# HyperGRL follows its 118.sh fixed runner.  It uses the DGL source build.
for data in citeseer_cite cora_coauth imdb pubmed_cite aminer; do
  run hypergrl "$data" env DGL_LIBRARY_PATH=/tmp/dgl-v2.1.0-build-r5 LD_LIBRARY_PATH=/tmp/dgl-v2.1.0-build-r5:/home/dms2/miniconda/envs/hgnn-dgl-src/lib conda run --no-capture-output -n hgnn-dgl-src python HyperGRL/hyperGRL_train_our.py --data "$data" --device cuda:0 --num_seeds 20
done
run phenomnn citeseer_cite conda run --no-capture-output -n hgnn-pyg python PhenomNN/PhenomNN_train.py --data citeseer_cite --num_seeds 20 --lr 0.01 --device cuda:0 --task node --lam0 10 --lam1 1 --alp 1 --prop_step 16
run phenomnn cora_coauth conda run --no-capture-output -n hgnn-pyg python PhenomNN/PhenomNN_train.py --data cora_coauth --num_seeds 20 --lr 0.01 --device cuda:0 --task node --lam0 20 --lam1 10 --alp 0.1 --prop_step 8
run phenomnn imdb conda run --no-capture-output -n hgnn-pyg python PhenomNN/PhenomNN_train.py --data imdb --num_seeds 20 --lr 0.01 --device cuda:0 --task node --lam0 0 --lam1 5 --alp 0.01 --prop_step 8
run phenomnn pubmed_cite conda run --no-capture-output -n hgnn-pyg python PhenomNN/PhenomNN_train.py --data pubmed_cite --num_seeds 20 --lr 0.01 --device cuda:0 --task node --lam0 10 --lam1 5 --alp 1 --prop_step 16
run phenomnn aminer conda run --no-capture-output -n hgnn-pyg python PhenomNN/PhenomNN_train.py --data aminer --num_seeds 20 --lr 0.01 --device cuda:0 --task node --lam0 10 --lam1 10 --alp 0.1 --prop_step 8
# HyperGCL remains globally last: start it only after GPU 1 completes all
# non-HyperGCL five-dataset jobs.
while ! rg -q '^villain aminer ' "$root/.agents/env-status/full-runs/formal118-pending5-gpu1-20260911/status.tsv" 2>/dev/null; do sleep 60; done
for data in citeseer_cite cora_coauth imdb pubmed_cite aminer; do
  run hypergcl "$data" conda run --no-capture-output -n hgnn-hypergcl python HyperGCL/HyperGCL_train.py --task node --epochs 200 --num_seeds 20 --data "$data" --cuda 0
done
