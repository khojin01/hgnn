#!/usr/bin/env bash
# Start SE-HSSL after the existing PhenomNN/HypeBoy GPU-0 queue. Reuse the
# supplied dataset-specific time.sh settings, changing only task and seed count.
set +e

workspace="/home/dms2/hojin_workspace/hgnn"
run_id="edge-sehssl-six-gpu0-20260913"
log_dir="$workspace/.agents/env-status/full-runs/$run_id"
status_file="$log_dir/status.tsv"
mkdir -p "$log_dir"
touch "$status_file"
cd "$workspace" || exit 1

while kill -0 1898142 2>/dev/null; do sleep 30; done

for dataset in citeseer_cite cora_coauth imdb house pubmed_cite aminer; do
  result="$workspace/results/result_${dataset}_SEHSSL_edge.txt"
  log="$log_dir/${dataset}.log"
  if [[ -s "$result" ]]; then
    printf 'sehssl\t%s\tSKIP_EXISTING\t%s\n' "$dataset" "$(date -Is)" >> "$status_file"
    continue
  fi
  command_line="$(awk -v data="$dataset" '$0 ~ /^python SEHSSL\/SEHSSL_train.py/ && $0 ~ ("--dataset " data "([[:space:]]|$)") {print; exit}' SEHSSL/time.sh)"
  command_line="${command_line//--task node/--task edge}"
  command_line="${command_line//--num_seeds 1/--num_seeds 20}"
  command_line="${command_line//--device 1/--device 0}"
  if [[ -z "$command_line" ]]; then
    printf 'sehssl\t%s\tBLOCKED_NO_COMMAND\t%s\n' "$dataset" "$(date -Is)" >> "$status_file"
    continue
  fi
  {
    date -Is
    echo "RUN_ID=$run_id MODEL=SE-HSSL DATASET=$dataset TASK=edge DEVICE=0 SEEDS=20"
    echo "SOURCE=SEHSSL/time.sh dataset-specific settings"
    echo "COMMAND=$command_line"
  } > "$log"
  timeout 12h conda run --no-capture-output -n hgnn-pyg bash -lc "$command_line" >> "$log" 2>&1
  code=$?
  if [[ $code -eq 0 && -s "$result" ]]; then state="COMPLETE"
  elif [[ $code -eq 124 ]]; then state="OOT"
  elif rg -qi 'out of memory|CUDA error: out of memory' "$log"; then state="OOM"
  else state="FAILED"; fi
  echo "EXIT_CODE=$code STATE=$state" >> "$log"
  date -Is >> "$log"
  printf 'sehssl\t%s\t%s\t%s\n' "$dataset" "$state" "$(date -Is)" >> "$status_file"
done
