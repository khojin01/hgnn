#!/usr/bin/env bash
# Table 5 (community detection) — GraphMAE2.
# 118.sh 고정 설정으로 한 번 학습해 임베딩을 받고, k-means seed 20개로 NMI 를 잰다.
# 학습 옵션은 118.sh 그대로이고 추가한 것은 --save-emb 하나뿐이다.
set -uo pipefail

ROOT=/home/dms2/hojin_workspace/hgnn
CONDA=/home/dms2/miniconda/bin/conda
ENV=hgnn-dgl-src
MODEL=GraphMAE2
GPU=${1:-1}
run_id="cd-graphmae2-gpu${GPU}-$(date +%Y%m%d)"
OUT="$ROOT/.agents/env-status/full-runs/$run_id"
mkdir -p "$OUT" "$ROOT/$MODEL/embs"
STATUS="$OUT/status.tsv"

# <데이터셋> <lr> <mask_rate>
settings=(
  "citeseer_cite 0.0001 0.5"
  "cora_coauth   0.0001 0.5"
  "imdb          0.001  0.75"
  "house         0.0001 0.5"
  "pubmed_cite   0.01   0.5"
  "aminer        0.0001 0.5"
)

say() { printf '%s\t%s\t%s\t%s\n' "$MODEL" "$1" "$2" "$(date -Iseconds)" >> "$STATUS"; }

cd "$ROOT" || exit 1
for row in "${settings[@]}"; do
  set -- $row
  ds="$1"; lr="$2"; mr="$3"
  log="$OUT/$ds.log"; date -Iseconds > "$log"

  result="$ROOT/results/result_${ds}_${MODEL}_cluster.txt"
  if [[ -s "$result" ]]; then echo SKIP_EXISTING >> "$log"; say "$ds" SKIP_EXISTING; continue; fi

  emb="$ROOT/$MODEL/embs/${ds}_lr${lr}_mr${mr}.pkl"
  if [[ ! -f "$emb" ]]; then
    timeout 24h "$CONDA" run --no-capture-output -n "$ENV" \
      python "$MODEL/${MODEL}_train.py" --data "$ds" --num_seeds 20 --lr "$lr" \
        --mask_rate "$mr" --device "$GPU" --task node --save-emb "$emb" >> "$log" 2>&1
    code=$?
    if (( code == 124 )); then say "$ds" OOT; continue; fi
    if grep -qi "out of memory" "$log"; then say "$ds" OOM; continue; fi
    if (( code != 0 )) || [[ ! -f "$emb" ]]; then say "$ds" "FAILED_TRAIN_$code"; continue; fi
  fi

  timeout 24h "$CONDA" run --no-capture-output -n "$ENV" \
    python tools/cluster_eval.py --model-dir "$MODEL" --data "$ds" --emb "$emb" >> "$log" 2>&1
  code=$?
  if (( code == 0 )); then say "$ds" COMPLETE
  elif (( code == 124 )); then say "$ds" OOT
  else say "$ds" "FAILED_EVAL_$code"; fi
done
echo "끝" >> "$OUT/_done"
