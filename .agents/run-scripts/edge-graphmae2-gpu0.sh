#!/usr/bin/env bash
# Use GraphMAE2's supplied per-dataset 20-seed settings, changing only the
# task from node classification to hyperedge prediction.
set +e
run_id="edge-graphmae2-gpu0-20260912"
log_dir=".agents/env-status/full-runs/${run_id}"
mkdir -p "$log_dir"
log="$log_dir/graphmae2.log"
{
  date -Is
  echo "RUN_ID=$run_id MODEL=GraphMAE2 TASK=edge DEVICE=0"
  echo "SOURCE=GraphMAE2/118.sh (task switched to edge)"
} > "$log"
if sed 's/--task node/--task edge/g' GraphMAE2/118.sh | \
  env DGL_LIBRARY_PATH=/tmp/dgl-v2.1.0-build-r5 LD_LIBRARY_PATH=/tmp/dgl-v2.1.0-build-r5:/home/dms2/miniconda/envs/hgnn-dgl-src/lib \
  timeout 8h conda run --no-capture-output -n hgnn-dgl-src bash -s 0 >> "$log" 2>&1; then
  code=0
else
  code=$?
fi
echo "EXIT_CODE=$code" >> "$log"
date -Is >> "$log"
echo "graphmae2 $code" > "$log_dir/status.tsv"
