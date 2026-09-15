---
type: protocol
model: VilLain
env: hgnn-pyg
updated: 2026-09-15 19:20
tags: [hgnn/protocol]
---

<!-- AUTO:BEGIN -->
# VilLain 실행

결과 → [[VilLain]] · 코드 `VilLain/` · 환경 `hgnn-pyg` · <small>갱신 2026-09-15 19:20</small>

## 정식 명령 (`VilLain/118.sh`)

```bash
conda run --no-capture-output -n hgnn-pyg bash -lc '\
  cd /home/dms2/hojin_workspace/hgnn && \
  python VilLain/eval.py --data cora_cite --num_step 4 --num_step_gen 100 --device $gpu --lr 0.01 \
  python VilLain/eval.py --data citeseer_cite --num_step 4 --num_step_gen 100 --device $gpu --lr 0.0001 \
  python VilLain/eval.py --data cora_coauth --num_step 4 --num_step_gen 100 --device $gpu --lr 0.001 \
  python VilLain/eval.py --data dblp_copub --num_step 4 --num_step_gen 100 --device $gpu --lr 0.01 \
  python VilLain/eval.py --data house --num_step 4 --num_step_gen 100 --device $gpu --lr 0.0001 \
  python VilLain/eval.py --data imdb --num_step 4 --num_step_gen 100 --device $gpu --lr 0.01 \
  python VilLain/eval.py --data pubmed_cite --num_step 4 --num_step_gen 10 --device $gpu --lr 0.01 \
  python VilLain/eval.py --data aminer --num_step 4 --num_step_gen 10 --device $gpu --lr 0.01 \
  python VilLain/eval.py --data dblp_coauth --num_step 4 --num_step_gen 100 --device $gpu --lr 0.01 \
  python VilLain/eval.py --data modelnet_40 --num_step 4 --num_step_gen 100 --device $gpu --lr 0.001 \
  python VilLain/eval.py --data news --num_step 4 --num_step_gen 100 --device $gpu --lr 0.01'
```

<small>한 줄이 데이터셋 하나. `--gpu`/`--device` 값은 스크립트 변수(`$gpu`)로 바꿔 쓴다.</small>

## 파일

| 항목 | 내용 |
|---|---|
| 스크립트 | `118.sh` · `edge.sh` · `node.sh` · `time.sh` |
| 실행에 쓴 run-scripts | `edge-villain-six-after-hypergcl-gpu1.sh` · `formal118-house-remaining-gpu1.sh` · `formal118-house-resume-gpu1.sh` · `formal118-pending5-gpu1.sh` · `node-failure-repair-gpu1.sh` · `node-priority-order-after-hypergcn.sh` · `villain-accuracy-gpu1.sh` · `villain-cora-gpu0-parallel.sh` |
| 게이트 파일 | `villain-edge-check.ok` |
| 정식 완료 | NC 6칸 · HP 6칸 · CD 6칸 |
| 돌리지 말 것 | 없음 |

관련: [[실행 규약]] · [[VilLain]]
<!-- AUTO:END -->

## 함정과 판단

<!-- 이 모델을 돌리며 알게 된 것: 실패 원인, 고친 것, 다시 보지 말아야 할 길. AUTO 구간은 덮어써진다. -->

