#!/usr/bin/env bash
# Wait for the supervised GPU-1 queue, then run TriCL's repaired edge route.
set +e

workspace="/home/dms2/hojin_workspace/hgnn"
run_id="edge-tricl-six-gpu1-20260912"
log_dir="$workspace/.agents/env-status/full-runs/$run_id"
status_file="$log_dir/status.tsv"
mkdir -p "$log_dir"
touch "$status_file"
cd "$workspace" || exit 1

while pgrep -f '[e]dge-six-resume-gpu1.sh|[e]dge-six-resume-v2-gpu1-20260912' >/dev/null; do
  sleep 30
done

for dataset in citeseer_cite cora_coauth imdb house pubmed_cite aminer; do
  result="$workspace/results/result_${dataset}_TriCL_edge.txt"
  log="$log_dir/${dataset}.log"
  if [[ -s "$result" ]]; then
    printf 'tricl\t%s\tSKIP_EXISTING\t%s\n' "$dataset" "$(date -Is)" >> "$status_file"
    continue
  fi
  command_line="python TriCL/TriCL_train.py --data $dataset --num_seeds 20 --device 1 --task edge"
  {
    date -Is
    echo "RUN_ID=$run_id MODEL=TriCL DATASET=$dataset TASK=edge DEVICE=1 SEEDS=20"
    echo "SOURCE=Drive-original latent edge branch plus verified minimal activation"
    echo "COMMAND=$command_line"
  } > "$log"
  timeout 8h conda run --no-capture-output -n hgnn-pyg bash -lc "$command_line" >> "$log" 2>&1
  code=$?
  if [[ $code -eq 0 && -s "$result" ]]; then
    state="COMPLETE"
  elif [[ $code -eq 124 ]]; then
    state="OOT"
  else
    state="FAILED"
  fi
  echo "EXIT_CODE=$code STATE=$state" >> "$log"
  date -Is >> "$log"
  printf 'tricl\t%s\t%s\t%s\n' "$dataset" "$state" "$(date -Is)" >> "$status_file"
done
