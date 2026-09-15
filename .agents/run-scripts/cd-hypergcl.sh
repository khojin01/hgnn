#!/usr/bin/env bash
# Table 5 (community detection) — HyperGCL.
#
# HyperGCL 도 118.sh 가 없다. 정식 노드 실행이 쓴 명령이 곧 고정 설정이고, 나머지는 코드 기본값이다:
#   --task node --epochs 200 --num_seeds 20 --data <데이터셋> --cuda <번호>
# 학습은 seed 루프 안에서 돌아가므로 첫 seed 모델의 노드 표현(forward_cl)을 받아 쓴다.
#
# 학습이 끝난 노드 임베딩을 받아 k-means seed 20개로 NMI 를 잰다.
# 추가한 것은 --save-emb 하나뿐이고, 주지 않으면 원래 동작과 같다.
set -uo pipefail

ROOT=/home/dms2/hojin_workspace/hgnn
CONDA=/home/dms2/miniconda/bin/conda
ENV=hgnn-hypergcl
MODEL=HyperGCL
GPU=${1:-0}
run_id="cd-hypergcl-gpu${GPU}-$(date +%Y%m%d)"
OUT="$ROOT/.agents/env-status/full-runs/$run_id"
mkdir -p "$OUT" "$ROOT/$MODEL/embs"
STATUS="$OUT/status.tsv"

datasets=(citeseer_cite cora_coauth imdb house pubmed_cite aminer)

say() { printf '%s\t%s\t%s\t%s\n' "$MODEL" "$1" "$2" "$(date -Iseconds)" >> "$STATUS"; }

cd "$ROOT" || exit 1
for ds in "${datasets[@]}"; do
  log="$OUT/$ds.log"
  date -Iseconds > "$log"

  result="$ROOT/results/result_${ds}_HyperGCL_cluster.txt"
  if [[ -s "$result" ]]; then
    echo SKIP_EXISTING >> "$log"; say "$ds" SKIP_EXISTING; continue
  fi

  emb="$ROOT/$MODEL/embs/${ds}_formal.pkl"
  if [[ ! -f "$emb" ]]; then
    echo "설정: $args" >> "$log"
    # shellcheck disable=SC2086
    timeout 24h "$CONDA" run --no-capture-output -n "$ENV" \
      python "$MODEL/${MODEL}_train.py" $args --num_seeds 20 --device "$GPU" --save-emb "$emb" >> "$log" 2>&1
    code=$?
    if (( code == 124 )); then say "$ds" OOT; continue; fi
    if grep -qi "out of memory" "$log"; then say "$ds" OOM; continue; fi
    if (( code != 0 )) || [[ ! -f "$emb" ]]; then say "$ds" "FAILED_TRAIN_$code"; continue; fi
  fi

  timeout 24h "$CONDA" run --no-capture-output -n "$ENV" \
    python tools/cluster_eval.py --model-dir "$MODEL" --data "$ds" --emb "$emb" --out-name HyperGCL >> "$log" 2>&1
  code=$?
  if (( code == 0 )); then say "$ds" COMPLETE
  elif (( code == 124 )); then say "$ds" OOT
  else say "$ds" "FAILED_EVAL_$code"; fi
done
echo "끝" >> "$OUT/_done"
