#!/usr/bin/env bash
# Continue GPU 0 after H-GD. Each dataset is isolated and failures do not stop
# the queue. PhenomNN AMiner is a mandatory Table-4 O.O.M skip.
set +e

workspace="/home/dms2/hojin_workspace/hgnn"
run_id="edge-phenom-hypeboy-gpu0-20260912"
log_dir="$workspace/.agents/env-status/full-runs/$run_id"
status_file="$log_dir/status.tsv"
mkdir -p "$log_dir"
touch "$status_file"
cd "$workspace" || exit 1

while kill -0 1897260 2>/dev/null; do
  sleep 30
done

run_one() {
  local model="$1" dataset="$2" result="$3" command_line="$4"
  local log="$log_dir/${model}_${dataset}.log" code state
  if [[ -s "$result" ]]; then
    printf '%s\t%s\tSKIP_EXISTING\t%s\n' "$model" "$dataset" "$(date -Is)" >> "$status_file"
    return
  fi
  {
    date -Is
    echo "RUN_ID=$run_id MODEL=$model DATASET=$dataset TASK=edge DEVICE=0 SEEDS=20"
    echo "COMMAND=$command_line"
  } > "$log"
  timeout 8h conda run --no-capture-output -n hgnn-pyg bash -lc "$command_line" >> "$log" 2>&1
  code=$?
  if [[ $code -eq 0 && -s "$result" ]]; then state="COMPLETE"
  elif [[ $code -eq 124 ]]; then state="OOT"
  elif rg -q 'out of memory|CUDA error: out of memory' "$log"; then state="OOM"
  else state="FAILED"; fi
  echo "EXIT_CODE=$code STATE=$state" >> "$log"
  date -Is >> "$log"
  printf '%s\t%s\t%s\t%s\n' "$model" "$dataset" "$state" "$(date -Is)" >> "$status_file"
}

run_one phenomnn citeseer_cite "$workspace/results/result_citeseer_cite_PhenomNN_edge.txt" \
  "python PhenomNN/PhenomNN_train.py --data citeseer_cite --num_seeds 20 --lr 0.01 --device cuda:0 --task edge --lam0 10 --lam1 1 --alp 1 --prop_step 16"
run_one phenomnn cora_coauth "$workspace/results/result_cora_coauth_PhenomNN_edge.txt" \
  "python PhenomNN/PhenomNN_train.py --data cora_coauth --num_seeds 20 --lr 0.01 --device cuda:0 --task edge --lam0 20 --lam1 10 --alp 0.1 --prop_step 8"
run_one phenomnn imdb "$workspace/results/result_imdb_PhenomNN_edge.txt" \
  "python PhenomNN/PhenomNN_train.py --data imdb --num_seeds 20 --lr 0.01 --device cuda:0 --task edge --lam0 0 --lam1 5 --alp 0.01 --prop_step 8"
run_one phenomnn house "$workspace/results/result_house_PhenomNN_edge.txt" \
  "python PhenomNN/PhenomNN_train.py --data house --num_seeds 20 --lr 0.01 --device cuda:0 --task edge --lam0 0.01 --lam1 10 --alp 1 --prop_step 8"
run_one phenomnn pubmed_cite "$workspace/results/result_pubmed_cite_PhenomNN_edge.txt" \
  "python PhenomNN/PhenomNN_train.py --data pubmed_cite --num_seeds 20 --lr 0.01 --device cuda:0 --task edge --lam0 10 --lam1 5 --alp 1 --prop_step 16"
printf 'phenomnn\taminer\tSKIPPED_PAPER_OOM\t%s\n' "$(date -Is)" >> "$status_file"

for dataset in citeseer_cite cora_coauth imdb house pubmed_cite aminer; do
  result="$workspace/results/result_${dataset}_Hypeboy_edge.txt"
  run_one hypeboy "$dataset" "$result" \
    "python Hypeboy/Hypeboy_train.py --data $dataset --task edge --num_seeds 20 --device cuda:0"
done
