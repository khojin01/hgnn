---
type: protocol
model: GraphMAE2
env: hgnn-dgl-src
updated: 2026-09-15 22:12
tags: [hgnn/protocol]
---

<!-- AUTO:BEGIN -->
# GraphMAE2 실행

결과 → [[GraphMAE2]] · 코드 `GraphMAE2/` · 환경 `hgnn-dgl-src` · <small>갱신 2026-09-15 22:12</small>

## 정식 명령 (`GraphMAE2/118.sh`)

```bash
conda run --no-capture-output -n hgnn-dgl-src bash -lc '\
  cd /home/dms2/hojin_workspace/hgnn && \
  python GraphMAE2/GraphMAE2_train.py --data citeseer_cite --num_seeds 20 --lr 0.0001 --mask_rate 0.5 --device $device --task node \
  python GraphMAE2/GraphMAE2_train.py --data cora_cite --num_seeds 20 --lr 0.001 --mask_rate 0.25 --device $device --task node \
  python GraphMAE2/GraphMAE2_train.py --data dblp_copub --num_seeds 20 --lr 0.001 --mask_rate 0.75 --device $device --task node \
  python GraphMAE2/GraphMAE2_train.py --data cora_coauth --num_seeds 20 --lr 0.0001 --mask_rate 0.5 --device $device --task node \
  python GraphMAE2/GraphMAE2_train.py --data imdb --num_seeds 20 --lr 0.001 --mask_rate 0.75 --device $device --task node \
  python GraphMAE2/GraphMAE2_train.py --data house --num_seeds 20 --lr 0.0001 --mask_rate 0.5 --device $device --task node \
  python GraphMAE2/GraphMAE2_train.py --data pubmed_cite --num_seeds 20 --lr 0.01 --mask_rate 0.5 --device $device --task node \
  python GraphMAE2/GraphMAE2_train.py --data dblp_coauth --num_seeds 20 --lr 0.001 --mask_rate 0.5 --device $device --task node \
  python GraphMAE2/GraphMAE2_train.py --data aminer --num_seeds 20 --lr 0.0001 --mask_rate 0.5 --device $device --task node \
  python GraphMAE2/GraphMAE2_train.py --data modelnet_40 --num_seeds 20 --lr 0.001 --mask_rate 0.25 --device $device --task node \
  python GraphMAE2/GraphMAE2_train.py --data news --num_seeds 20 --lr 0.001 --mask_rate 0.5 --device $device --task node'
```

<small>한 줄이 데이터셋 하나. `--gpu`/`--device` 값은 스크립트 변수(`$gpu`)로 바꿔 쓴다.</small>

## 파일

| 항목 | 내용 |
|---|---|
| 스크립트 | `118.sh` · `exp0.sh` · `exp1.sh` · `time_node.sh` |
| 실행에 쓴 run-scripts | `edge-graphmae2-gpu0.sh` · `formal118-graphmae2-node-gpu1.sh` · `formal118-house-remaining-gpu0.sh` |
| 게이트 파일 | — |
| 정식 완료 | NC 6칸 · HP 6칸 · CD 6칸 |
| 돌리지 말 것 | 없음 |

관련: [[실행 규약]] · [[GraphMAE2]]
<!-- AUTO:END -->

## 함정과 판단

<!-- 이 모델을 돌리며 알게 된 것: 실패 원인, 고친 것, 다시 보지 말아야 할 길. AUTO 구간은 덮어써진다. -->

