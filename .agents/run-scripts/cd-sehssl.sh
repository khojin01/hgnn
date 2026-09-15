#!/usr/bin/env bash
# Table 5 (community detection) — SE-HSSL.
#
# SE-HSSL 은 118.sh 가 없다. 데이터셋별 고정 설정은 `SEHSSL/time.sh` 에 한 줄씩 들어 있고,
# 정식 Table 3 실행(formal118-house-*.sh)도 그 줄을 그대로 꺼내 썼다. 같은 방식을 쓴다.
# time.sh 줄은 탐색용이라 `--num_seeds 1` 이므로 뒤에 20 을 덧붙여 덮어쓴다 (argparse 는 뒤가 이긴다).
#
# 학습이 끝난 노드 임베딩을 받아 k-means seed 20개로 NMI 를 잰다.
# 추가한 것은 --save-emb 하나뿐이고, 주지 않으면 원래 동작과 같다.
set -uo pipefail

ROOT=/home/dms2/hojin_workspace/hgnn
CONDA=/home/dms2/miniconda/bin/conda
ENV=hgnn-pyg
MODEL=SEHSSL
GPU=${1:-0}
run_id="cd-sehssl-gpu${GPU}-$(date +%Y%m%d)"
OUT="$ROOT/.agents/env-status/full-runs/$run_id"
mkdir -p "$OUT" "$ROOT/$MODEL/embs"
STATUS="$OUT/status.tsv"

datasets=(citeseer_cite cora_coauth imdb house pubmed_cite aminer)

say() { printf '%s\t%s\t%s\t%s\n' "$MODEL" "$1" "$2" "$(date -Iseconds)" >> "$STATUS"; }

cd "$ROOT" || exit 1
for ds in "${datasets[@]}"; do
  log="$OUT/$ds.log"
  date -Iseconds > "$log"

  result="$ROOT/results/result_${ds}_SEHSSL_cluster.txt"
  if [[ -s "$result" ]]; then
    echo SKIP_EXISTING >> "$log"; say "$ds" SKIP_EXISTING; continue
  fi

  # time.sh 에서 이 데이터셋의 고정 설정 줄을 꺼낸다
  line="$(awk -v d="$ds" '$0 ~ /^python SEHSSL\/SEHSSL_train.py/ && $0 ~ ("--dataset " d "([[:space:]]|$)") {print; exit}' "$ROOT/SEHSSL/time.sh")"
  if [[ -z "$line" ]]; then
    echo "time.sh 에 $ds 설정 없음" >> "$log"; say "$ds" SKIP_NO_CONFIG; continue
  fi
  args="${line#python SEHSSL/SEHSSL_train.py }"

  emb="$ROOT/$MODEL/embs/${ds}_time.pkl"
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
    python tools/cluster_eval.py --model-dir "$MODEL" --data "$ds" --emb "$emb" --out-name SEHSSL >> "$log" 2>&1
  code=$?
  if (( code == 0 )); then say "$ds" COMPLETE
  elif (( code == 124 )); then say "$ds" OOT
  else say "$ds" "FAILED_EVAL_$code"; fi
done
echo "끝" >> "$OUT/_done"
