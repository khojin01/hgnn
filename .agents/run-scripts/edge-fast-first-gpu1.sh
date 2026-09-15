#!/usr/bin/env bash
# Formal hyperedge-prediction queue.  The model-specific exp_edge.sh files
# contain the fixed 20-seed configurations supplied with each implementation.
# Individual data/model failures must be logged without aborting the remaining
# queue (several unavailable datasets are expected to fail independently).
set +e

run_id="edge-fast-first-gpu1-20260912"
log_dir=".agents/env-status/full-runs/${run_id}"
mkdir -p "$log_dir"
: > "$log_dir/status.tsv"

run_model() {
  local model="$1"
  local script="$2"
  local code
  {
    date -Is
    echo "RUN_ID=$run_id MODEL=$model TASK=edge DEVICE=1"
    echo "COMMAND=conda run --no-capture-output -n hgnn-pyg bash $script 1"
    timeout 8h conda run --no-capture-output -n hgnn-pyg bash "$script" 1
    code=$?
    echo "EXIT_CODE=$code"
    date -Is
  } >"$log_dir/${model}.log" 2>&1
  echo "$model $code" >> "$log_dir/status.tsv"
}

# Ordered by the observed NC throughput: lightweight supervised baselines and
# Uni-family first, followed by the remaining implementations with edge scripts.
run_model mlp MLP/exp_edge.sh
run_model unigcn UniGCN/exp_edge.sh
run_model unigin UniGIN/exp_edge.sh
run_model unigcn2 UniGCN2/exp_edge.sh
run_model hgnn HGNN/exp_edge.sh
run_model hnhn HNHN/exp_edge.sh
run_model edhnn EDHNN/exp_edge.sh
run_model allset AllSet/exp_edge.sh
run_model hypergcn HyperGCN/exp_edge.sh
run_model maskgae MaskGAE/exp_edge.sh
