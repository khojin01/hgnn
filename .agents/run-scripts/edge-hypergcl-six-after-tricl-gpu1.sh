#!/usr/bin/env bash
# HyperGCL follows TriCL on GPU 1 and uses the repaired GPU sampler path.
set +e

workspace="/home/dms2/hojin_workspace/hgnn"
run_id="edge-hypergcl-six-gpu1-20260913"
log_dir="$workspace/.agents/env-status/full-runs/$run_id"
status_file="$log_dir/status.tsv"
mkdir -p "$log_dir"
touch "$status_file"
cd "$workspace" || exit 1

while kill -0 1897580 2>/dev/null; do sleep 30; done

for dataset in citeseer_cite cora_coauth imdb house pubmed_cite aminer; do
  result="$workspace/results/result_${dataset}_HyperGCL_edge.txt"
  log="$log_dir/${dataset}.log"
  if [[ -s "$result" ]]; then
    printf 'hypergcl\t%s\tSKIP_EXISTING\t%s\n' "$dataset" "$(date -Is)" >> "$status_file"
    continue
  fi
  command_line="python HyperGCL/HyperGCL_train.py --data $dataset --num_seeds 20 --epochs 200 --cuda 1 --task edge --negative_sampling_method gpu"
  {
    date -Is
    echo "RUN_ID=$run_id MODEL=HyperGCL DATASET=$dataset TASK=edge DEVICE=1 SEEDS=20"
    echo "COMMAND=$command_line"
  } > "$log"
  timeout 12h conda run --no-capture-output -n hgnn-hypergcl bash -lc "$command_line" >> "$log" 2>&1
  code=$?
  if [[ $code -eq 0 && -s "$result" ]]; then state="COMPLETE"
  elif [[ $code -eq 124 ]]; then state="OOT"
  elif rg -qi 'out of memory|CUDA error: out of memory' "$log"; then state="OOM"
  else state="FAILED"; fi
  echo "EXIT_CODE=$code STATE=$state" >> "$log"
  date -Is >> "$log"
  printf 'hypergcl\t%s\t%s\t%s\n' "$dataset" "$state" "$(date -Is)" >> "$status_file"
done
