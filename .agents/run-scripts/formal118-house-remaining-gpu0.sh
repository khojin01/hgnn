#!/usr/bin/env bash
set -u
root=/home/dms2/hojin_workspace/hgnn
log_dir="$root/.agents/env-status/full-runs/formal118-house-remaining-gpu0-20260911"
mkdir -p "$log_dir"; cd "$root"
run() {
  name=$1; shift
  { date -Is; echo "MODEL=$name DATA=house"; echo "COMMAND=$*"; timeout 90m "$@"; code=$?; echo "EXIT_CODE=$code"; date -Is; } >"$log_dir/$name.log" 2>&1
  echo "$name $code" >>"$log_dir/status.tsv"
}
# Official 118.sh configuration.  GraphMAE2 requires the locally built DGL.
run graphmae2 env DGL_LIBRARY_PATH=/tmp/dgl-v2.1.0-build-r5 LD_LIBRARY_PATH=/tmp/dgl-v2.1.0-build-r5:/home/dms2/miniconda/envs/hgnn-dgl-src/lib conda run --no-capture-output -n hgnn-dgl-src python GraphMAE2/GraphMAE2_train.py --data house --num_seeds 20 --lr 0.0001 --mask_rate 0.5 --device 0 --task node
run hypergrl env DGL_LIBRARY_PATH=/tmp/dgl-v2.1.0-build-r5 LD_LIBRARY_PATH=/tmp/dgl-v2.1.0-build-r5:/home/dms2/miniconda/envs/hgnn-dgl-src/lib conda run --no-capture-output -n hgnn-dgl-src python HyperGRL/hyperGRL_train_our.py --data house --device cuda:0 --num_seeds 20
run phenomnn conda run --no-capture-output -n hgnn-pyg python PhenomNN/PhenomNN_train.py --data house --num_seeds 20 --lr 0.01 --device cuda:0 --task node --lam0 0.01 --lam1 10 --alp 1 --prop_step 8
# HyperGCL is explicitly last: wait until the other House queue reaches its
# terminal VilLain entry (success or a recorded diagnosable failure).
while ! rg -q '^villain ' "$root/.agents/env-status/full-runs/formal118-house-remaining-gpu1-20260911/status.tsv" 2>/dev/null; do sleep 60; done
run hypergcl conda run --no-capture-output -n hgnn-hypergcl python HyperGCL/HyperGCL_train.py --task node --epochs 200 --num_seeds 20 --data house --cuda 0
