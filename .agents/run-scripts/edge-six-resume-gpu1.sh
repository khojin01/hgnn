#!/usr/bin/env bash
# Resume formal 20-seed hyperedge prediction on the six complete datasets.
# Every model/dataset is isolated, and an existing aggregate result is never rerun.
set +e

workspace="/home/dms2/hojin_workspace/hgnn"
run_id="edge-six-resume-v2-gpu1-20260912"
log_dir="$workspace/.agents/env-status/full-runs/$run_id"
status_file="$log_dir/status.tsv"
mkdir -p "$log_dir"
touch "$status_file"
cd "$workspace" || exit 1

datasets=(citeseer_cite cora_coauth imdb house pubmed_cite aminer)
models=(unigcn2 hgnn hnhn edhnn allset hypergcn maskgae)

script_for() {
  case "$1" in
    unigcn2) echo "UniGCN2/exp_edge.sh" ;;
    hgnn) echo "HGNN/exp_edge.sh" ;;
    hnhn) echo "HNHN/exp_edge.sh" ;;
    edhnn) echo "EDHNN/exp_edge.sh" ;;
    allset) echo "AllSet/exp_edge.sh" ;;
    hypergcn) echo "HyperGCN/exp_edge.sh" ;;
    maskgae) echo "MaskGAE/exp_edge.sh" ;;
  esac
}

result_stem_for() {
  case "$1" in
    unigcn2) echo "UniGCN2" ;;
    hgnn) echo "HGNN" ;;
    hnhn) echo "HNHN" ;;
    edhnn) echo "EDHNN" ;;
    allset) echo "AllSet" ;;
    hypergcn) echo "Hyper_GCN" ;;
    maskgae) echo "MaskGAE" ;;
  esac
}

for model in "${models[@]}"; do
  script="$(script_for "$model")"
  result_stem="$(result_stem_for "$model")"
  for dataset in "${datasets[@]}"; do
    result="$workspace/results/result_${dataset}_${result_stem}_edge.txt"
    log="$log_dir/${model}_${dataset}.log"
    if [[ -s "$result" ]]; then
      printf '%s\t%s\tSKIP_EXISTING\t%s\n' "$model" "$dataset" "$(date -Is)" >> "$status_file"
      continue
    fi

    command_line="$(awk -v data="$dataset" '$0 ~ /^python / && $0 ~ ("--data " data "([[:space:]]|$)") {print; exit}' "$script")"
    if [[ -z "$command_line" ]]; then
      printf '%s\t%s\tBLOCKED_NO_COMMAND\t%s\n' "$model" "$dataset" "$(date -Is)" >> "$status_file"
      continue
    fi
    command_line="${command_line//\$device/1}"

    {
      date -Is
      echo "RUN_ID=$run_id MODEL=$model DATASET=$dataset TASK=edge DEVICE=1 SEEDS=20"
      echo "SOURCE=$script"
      echo "COMMAND=$command_line"
    } > "$log"

    timeout 4h conda run --no-capture-output -n hgnn-pyg bash -lc "$command_line" >> "$log" 2>&1
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
    printf '%s\t%s\t%s\t%s\n' "$model" "$dataset" "$state" "$(date -Is)" >> "$status_file"
  done
done
