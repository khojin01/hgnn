---
type: protocol
model: MLP
env: hgnn-pyg
updated: 2026-09-15 15:36
tags: [hgnn/protocol]
---

<!-- AUTO:BEGIN -->
# MLP 실행

결과 → [[MLP]] · 코드 `MLP/` · 환경 `hgnn-pyg` · <small>갱신 2026-09-15 15:36</small>

## 정식 명령 (`MLP/118.sh`)

```bash
conda run --no-capture-output -n hgnn-pyg bash -lc '\
  cd /home/dms2/hojin_workspace/hgnn && \
  python MLP/MLP_train.py --data citeseer_cite --num_seeds 20 --lr 0.01 --task node \
  python MLP/MLP_train.py --data cora_cite --num_seeds 20 --lr 0.01 --task node \
  python MLP/MLP_train.py --data dblp_copub --num_seeds 20 --lr 0.01 --task node \
  python MLP/MLP_train.py --data cora_coauth --num_seeds 20 --lr 0.01 --task node \
  python MLP/MLP_train.py --data imdb --num_seeds 20 --lr 0.01 --task node \
  python MLP/MLP_train.py --data house --num_seeds 20 --lr 0.01 --task node \
  python MLP/MLP_train.py --data pubmed_cite --num_seeds 20 --lr 0.001 --task node \
  python MLP/MLP_train.py --data dblp_coauth --num_seeds 20 --lr 0.001 --task node \
  python MLP/MLP_train.py --data aminer --num_seeds 20 --lr 0.01 --task node \
  python MLP/MLP_train.py --data modelnet_40 --num_seeds 20 --lr 0.01 --task node \
  python MLP/MLP_train.py --data news --num_seeds 20 --lr 0.001 --task node'
```

<small>한 줄이 데이터셋 하나. `--gpu`/`--device` 값은 스크립트 변수(`$gpu`)로 바꿔 쓴다.</small>

## 파일

| 항목 | 내용 |
|---|---|
| 스크립트 | `118.sh` · `exp_edge.sh` · `exp_node.sh` · `time_node.sh` |
| 실행에 쓴 run-scripts | `edge-fast-first-gpu1.sh` · `formal118-house-gpu0.sh` · `formal118-mlp-node-gpu0.sh` · `node20-mlp-gpu0.sh` |
| 게이트 파일 | — |
| 정식 완료 | NC 6칸 · HP 6칸 |
| 돌리지 말 것 | 없음 |

## info.txt

```
Hyperparameter
- num_layers: 2
- hidden_dim: 128
- drop rate: 0.5
- weight decay: 10^-6
- lr: {0.05,0.01,0.005,0.001,0.0005,0.0001}
```

관련: [[실행 규약]] · [[MLP]]
<!-- AUTO:END -->

## 함정과 판단

<!-- 이 모델을 돌리며 알게 된 것: 실패 원인, 고친 것, 다시 보지 말아야 할 길. AUTO 구간은 덮어써진다. -->

