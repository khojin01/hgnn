#!/usr/bin/env bash
# Parallel VilLain EP worker: run Cora-CA on GPU 0 while the main queue uses GPU 1.
set +e
workspace="/home/dms2/hojin_workspace/hgnn"
run_id="edge-villain-cora-gpu0-parallel-20260914"
log_dir="$workspace/.agents/env-status/full-runs/$run_id"
status_file="$log_dir/status.tsv"
mkdir -p "$log_dir" "$workspace/VilLain/embs/edge"
cd "$workspace" || exit 1
dataset="cora_coauth"
nsg=100
lr=0.001
result="$workspace/results/result_${dataset}_VilLain_edge.txt"

if [[ -s "$result" ]]; then
  printf 'villain\t%s\tSKIP_EXISTING\t%s\n' "$dataset" "$(date -Is)" >> "$status_file"
  exit 0
fi

echo "$(date -Is) RUN_ID=$run_id MODEL=VilLain DATASET=$dataset TASK=edge DEVICE=0" > "$log_dir/cora_coauth.log"
embeddings_ok=1
for nl in 2 3 4 5 6 7 8; do
  pattern="$workspace/VilLain/embs/edge/split*_${dataset}_dim128_nl${nl}_ns4_nsg${nsg}_lr${lr}.pkl"
  count=$(compgen -G "$pattern" | wc -l)
  if [[ $count -eq 20 ]]; then
    echo "SKIP_EXISTING_EMBEDDINGS nl=$nl count=20" >> "$log_dir/cora_coauth.log"
    continue
  fi
  command_line="python VilLain/main.py --gpu 0 --dataset $dataset --num_step 4 --num_step_gen $nsg --lr $lr --num_labels $nl --dim 128 --num_seeds 20 --task edge"
  echo "COMMAND=$command_line" >> "$log_dir/cora_coauth.log"
  timeout 24h conda run --no-capture-output -n hgnn-pyg bash -lc "$command_line" >> "$log_dir/cora_coauth.log" 2>&1
  code=$?
  count=$(compgen -G "$pattern" | wc -l)
  if [[ $code -ne 0 || $count -ne 20 ]]; then
    echo "EMBEDDING_FAILURE nl=$nl EXIT_CODE=$code COUNT=$count" >> "$log_dir/cora_coauth.log"
    embeddings_ok=0
  fi
done

if [[ $embeddings_ok -ne 1 ]]; then
  printf 'villain\t%s\tFAILED_EMBEDDINGS\t%s\n' "$dataset" "$(date -Is)" >> "$status_file"
  exit 1
fi

command_line="python VilLain/eval.py --data $dataset --num_seeds 20 --num_step 4 --num_step_gen $nsg --lr $lr --device 0 --task edge"
echo "COMMAND=$command_line" >> "$log_dir/cora_coauth.log"
timeout 12h conda run --no-capture-output -n hgnn-pyg bash -lc "$command_line" >> "$log_dir/cora_coauth.log" 2>&1
code=$?
if [[ $code -eq 0 && -s "$result" ]]; then state="COMPLETE"; else state="FAILED_EVAL"; fi
echo "EXIT_CODE=$code STATE=$state" >> "$log_dir/cora_coauth.log"
printf 'villain\t%s\t%s\t%s\n' "$dataset" "$state" "$(date -Is)" >> "$status_file"
