#!/usr/bin/env bash
# Robust edge-prediction queue for models that ship a formal exp_edge.sh.
# `if` deliberately captures non-zero model exits so missing datasets or a
# result-writer bug never stops the rest of the campaign.
set +e

run_id="edge-known-models-gpu1-20260912"
log_dir=".agents/env-status/full-runs/${run_id}"
mkdir -p "$log_dir"
: > "$log_dir/status.tsv"

run_model() {
  local model="$1"
  local script="$2"
  local log="$log_dir/${model}.log"
  local code
  {
    date -Is
    echo "RUN_ID=$run_id MODEL=$model TASK=edge DEVICE=1"
    echo "COMMAND=conda run --no-capture-output -n hgnn-pyg bash $script 1"
  } > "$log"
  if timeout 8h conda run --no-capture-output -n hgnn-pyg bash "$script" 1 >> "$log" 2>&1; then
    code=0
  else
    code=$?
  fi
  {
    echo "EXIT_CODE=$code"
    date -Is
  } >> "$log"
  echo "$model $code" >> "$log_dir/status.tsv"
  return 0
}

# MLP and UniGCN have already produced the currently available six-dataset
# results.  Continue with the other fast formal edge scripts first.
run_model unigin UniGIN/exp_edge.sh
run_model unigcn2 UniGCN2/exp_edge.sh
run_model hgnn HGNN/exp_edge.sh
run_model hnhn HNHN/exp_edge.sh
run_model edhnn EDHNN/exp_edge.sh
run_model allset AllSet/exp_edge.sh
run_model hypergcn HyperGCN/exp_edge.sh
run_model maskgae MaskGAE/exp_edge.sh
