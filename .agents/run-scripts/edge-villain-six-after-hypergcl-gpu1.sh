#!/usr/bin/env bash
# VilLain starts only after HyperGCL and an independent env-checker gate.
set +e

workspace="/home/dms2/hojin_workspace/hgnn"
run_id="edge-villain-six-gpu1-20260913"
log_dir="$workspace/.agents/env-status/full-runs/$run_id"
status_file="$log_dir/status.tsv"
gate="$workspace/.agents/env-status/villain-edge-check.ok"
mkdir -p "$log_dir" "$workspace/VilLain/embs/edge"
touch "$status_file"
cd "$workspace" || exit 1

while pgrep -f '[e]dge-hypergcl-six-after-tricl-gpu1.sh' >/dev/null; do sleep 30; done
while [[ ! -s "$gate" ]]; do sleep 60; done

settings=(
  "citeseer_cite 100 0.0001"
  "cora_coauth 100 0.001"
  "imdb 100 0.01"
  "house 100 0.0001"
  "pubmed_cite 10 0.0001"
  "aminer 10 0.01"
)

for setting in "${settings[@]}"; do
  read -r dataset nsg lr <<< "$setting"
  result="$workspace/results/result_${dataset}_VilLain_edge.txt"
  log="$log_dir/${dataset}.log"
  if [[ -s "$result" ]]; then
    printf 'villain\t%s\tSKIP_EXISTING\t%s\n' "$dataset" "$(date -Is)" >> "$status_file"
    continue
  fi
  {
    date -Is
    echo "RUN_ID=$run_id MODEL=VilLain DATASET=$dataset TASK=edge DEVICE=1 SEEDS=20"
    echo "CHECKER_GATE=$gate"
  } > "$log"

  embeddings_ok=1
  for nl in 2 3 4 5 6 7 8; do
    pattern="$workspace/VilLain/embs/edge/split*_${dataset}_dim128_nl${nl}_ns4_nsg${nsg}_lr${lr}.pkl"
    count=$(compgen -G "$pattern" | wc -l)
    if [[ $count -eq 20 ]]; then
      echo "SKIP_EXISTING_EMBEDDINGS nl=$nl count=20" >> "$log"
      continue
    fi
    command_line="python VilLain/main.py --gpu 1 --dataset $dataset --num_step 4 --num_step_gen $nsg --lr $lr --num_labels $nl --dim 128 --num_seeds 20 --task edge"
    echo "COMMAND=$command_line" >> "$log"
    timeout 24h conda run --no-capture-output -n hgnn-pyg bash -lc "$command_line" >> "$log" 2>&1
    code=$?
    count=$(compgen -G "$pattern" | wc -l)
    if [[ $code -ne 0 || $count -ne 20 ]]; then
      echo "EMBEDDING_FAILURE nl=$nl EXIT_CODE=$code COUNT=$count" >> "$log"
      embeddings_ok=0
    fi
  done

  if [[ $embeddings_ok -ne 1 ]]; then
    state="FAILED_EMBEDDINGS"
    printf 'villain\t%s\t%s\t%s\n' "$dataset" "$state" "$(date -Is)" >> "$status_file"
    continue
  fi

  command_line="python VilLain/eval.py --data $dataset --num_seeds 20 --num_step 4 --num_step_gen $nsg --lr $lr --device 1 --task edge"
  echo "COMMAND=$command_line" >> "$log"
  timeout 12h conda run --no-capture-output -n hgnn-pyg bash -lc "$command_line" >> "$log" 2>&1
  code=$?
  if [[ $code -eq 0 && -s "$result" ]]; then state="COMPLETE"
  elif [[ $code -eq 124 ]]; then state="OOT"
  elif rg -qi 'out of memory|CUDA error: out of memory' "$log"; then state="OOM"
  else state="FAILED_EVAL"; fi
  echo "EXIT_CODE=$code STATE=$state" >> "$log"
  date -Is >> "$log"
  printf 'villain\t%s\t%s\t%s\n' "$dataset" "$state" "$(date -Is)" >> "$status_file"
done
