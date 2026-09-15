#!/usr/bin/env bash
# Continue the cancelled IMDB run from predefined splits 19–20 using the
# GPU-resident augmentation and negative sampler, then run the remaining NC
# datasets with the same code path.
set +e

run_id="hypergcl-gpu-path-resume-gpu0-20260912"
log_dir=".agents/env-status/full-runs/${run_id}"
mkdir -p "$log_dir"
: > "$log_dir/status.tsv"

run() {
  local label="$1"
  shift
  local code
  {
    date -Is
    echo "RUN_ID=$run_id MODEL=HyperGCL TASK=node DATA=$label"
    echo "COMMAND=$*"
    timeout 8h "$@"
    code=$?
    echo "EXIT_CODE=$code"
    date -Is
  } >"$log_dir/${label}.log" 2>&1
  echo "hypergcl $label $code" >> "$log_dir/status.tsv"
}

run imdb_splits_19_20 conda run --no-capture-output -n hgnn-hypergcl python HyperGCL/HyperGCL_train.py \
  --task node --epochs 200 --num_seeds 2 --seed_start 18 --data imdb --cuda 0 --negative_sampling_method gpu
run pubmed_cite conda run --no-capture-output -n hgnn-hypergcl python HyperGCL/HyperGCL_train.py \
  --task node --epochs 200 --num_seeds 20 --data pubmed_cite --cuda 0 --negative_sampling_method gpu
run aminer conda run --no-capture-output -n hgnn-hypergcl python HyperGCL/HyperGCL_train.py \
  --task node --epochs 200 --num_seeds 20 --data aminer --cuda 0 --negative_sampling_method gpu
