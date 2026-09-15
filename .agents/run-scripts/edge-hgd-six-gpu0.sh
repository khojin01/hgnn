#!/usr/bin/env bash
# Formal H-GD edge runs. The Drive original has an edge branch but no
# exp_edge.sh, so these retain the supplied 118.sh per-dataset settings and
# change only --task node to --task edge.
set +e

workspace="/home/dms2/hojin_workspace/hgnn"
run_id="edge-hgd-six-gpu0-20260912"
log_dir="$workspace/.agents/env-status/full-runs/$run_id"
status_file="$log_dir/status.tsv"
mkdir -p "$log_dir"
touch "$status_file"
cd "$workspace" || exit 1

commands=(
  "python H-GD/H-GD_train.py --data citeseer_cite --num_seeds 20 --lr 0.0001 --device cuda:0 --task edge --p_e 0.3 --p_x 0.2"
  "python H-GD/H-GD_train.py --data cora_coauth --num_seeds 20 --lr 0.0001 --device cuda:0 --task edge --p_e 0.1 --p_x 0.1"
  "python H-GD/H-GD_train.py --data imdb --num_seeds 20 --lr 0.001 --device cuda:0 --task edge --p_e 0.2 --p_x 0.1"
  "python H-GD/H-GD_train.py --data house --num_seeds 20 --lr 0.0001 --device cuda:0 --task edge --p_e 0.2 --p_x 0.3"
  "python H-GD/H-GD_train.py --data pubmed_cite --num_seeds 20 --lr 0.0001 --device cuda:0 --task edge --p_e 0.4 --p_x 0.4"
  "python H-GD/H-GD_train.py --data aminer --num_seeds 20 --lr 0.0001 --device cuda:0 --task edge --p_e 0.2 --p_x 0.2"
)

for command_line in "${commands[@]}"; do
  dataset="$(sed -n 's/.*--data \([^ ]*\).*/\1/p' <<< "$command_line")"
  result="$workspace/results/result_${dataset}_HGD_edge.txt"
  log="$log_dir/${dataset}.log"

  # H-GD writes one physical line containing its seed array. A 20-seed line
  # is formal; the existing one-seed checker result must not cause a skip.
  if [[ -s "$result" ]] && awk -F',' 'NF >= 20 {found=1} END {exit !found}' "$result"; then
    printf 'hgd\t%s\tSKIP_EXISTING\t%s\n' "$dataset" "$(date -Is)" >> "$status_file"
    continue
  fi

  {
    date -Is
    echo "RUN_ID=$run_id MODEL=H-GD DATASET=$dataset TASK=edge DEVICE=0 SEEDS=20"
    echo "SOURCE=H-GD/118.sh (task switched from node to edge)"
    echo "COMMAND=$command_line"
  } > "$log"
  timeout 4h conda run --no-capture-output -n hgnn-pyg bash -lc "$command_line" >> "$log" 2>&1
  code=$?
  if [[ $code -eq 0 ]] && awk -F',' 'NF >= 20 {found=1} END {exit !found}' "$result" 2>/dev/null; then
    state="COMPLETE"
  elif [[ $code -eq 124 ]]; then
    state="OOT"
  else
    state="FAILED"
  fi
  echo "EXIT_CODE=$code STATE=$state" >> "$log"
  date -Is >> "$log"
  printf 'hgd\t%s\t%s\t%s\n' "$dataset" "$state" "$(date -Is)" >> "$status_file"
done
