#!/usr/bin/env bash
# Table 5 (community detection) — VilLain.
#
# 학습은 다시 하지 않는다. VilLain 이 이미 저장한 merged 임베딩을 118.sh 의 고정 설정대로
# 골라 k-means 로 군집하고 NMI 를 잰다. 규약대로 seed 20개(k-means random_state 0..19)다.
#
# 임베딩이 없는 데이터셋은 SKIP_NO_EMB 로 남기고 넘어간다. 한 칸이 실패해도 다음 칸을 계속한다.
set -uo pipefail

ROOT=/home/dms2/hojin_workspace/hgnn
CONDA=/home/dms2/miniconda/bin/conda
ENV=hgnn-pyg
MODEL=VilLain
run_id="cd-villain-$(date +%Y%m%d)"
OUT="$ROOT/.agents/env-status/full-runs/$run_id"
mkdir -p "$OUT"
STATUS="$OUT/status.tsv"

# 118.sh 의 데이터셋별 고정 설정: <데이터셋> <num_step_gen> <lr>
settings=(
  "citeseer_cite 100 0.0001"
  "cora_coauth   100 0.001"
  "imdb          100 0.01"
  "house         100 0.0001"
  "pubmed_cite   10  0.01"
  "aminer        10  0.01"
  "dblp_coauth   100 0.01"
  "modelnet_40   100 0.001"
  "news          100 0.01"
  "cora_cite     100 0.01"
  "dblp_copub    100 0.01"
)

say() { printf '%s\t%s\t%s\t%s\n' "$MODEL" "$1" "$2" "$(date -Iseconds)" >> "$STATUS"; }

cd "$ROOT" || exit 1
for row in "${settings[@]}"; do
  set -- $row
  ds="$1"; nsg="$2"; lr="$3"
  log="$OUT/$ds.log"
  date -Iseconds > "$log"

  result="$ROOT/results/result_${ds}_${MODEL}_cluster.txt"
  if [[ -s "$result" ]]; then
    echo "SKIP_EXISTING $result" >> "$log"; say "$ds" SKIP_EXISTING; continue
  fi

  emb="$ROOT/$MODEL/embs/${ds}_dim128_ns4_nsg${nsg}_lr${lr}_merged.pkl"
  if [[ ! -f "$emb" ]]; then
    echo "임베딩 없음: $emb" >> "$log"; say "$ds" SKIP_NO_EMB; continue
  fi

  echo "emb=$emb" >> "$log"
  timeout 24h "$CONDA" run --no-capture-output -n "$ENV" \
    python tools/cluster_eval.py --model-dir "$MODEL" --data "$ds" --emb "$emb" >> "$log" 2>&1
  code=$?
  if (( code == 0 )); then say "$ds" COMPLETE
  elif (( code == 124 )); then say "$ds" OOT
  elif grep -qi "out of memory" "$log"; then say "$ds" OOM
  else say "$ds" "FAILED_$code"; fi
done
echo "끝" >> "$OUT/_done"
