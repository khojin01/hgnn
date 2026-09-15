---
type: protocol
model: ED-HNN
env: hgnn-pyg
updated: 2026-09-15 15:36
tags: [hgnn/protocol]
---

<!-- AUTO:BEGIN -->
# ED-HNN 실행

결과 → [[ED-HNN]] · 코드 `EDHNN/` · 환경 `hgnn-pyg` · <small>갱신 2026-09-15 15:36</small>

## 정식 명령 (`EDHNN/118.sh`)

```bash
conda run --no-capture-output -n hgnn-pyg bash -lc '\
  cd /home/dms2/hojin_workspace/hgnn && \
  python EDHNN/EDHNN_train.py --data citeseer_cite --lr 0.001 --restart_alpha 0.7 --device cuda:$device --task node --num_seeds 20 \
  python EDHNN/EDHNN_train.py --data cora_cite --lr 0.01 --restart_alpha 1 --device cuda:$device --task node --num_seeds 20 \
  python EDHNN/EDHNN_train.py --data dblp_copub --lr 0.01 --restart_alpha 0.9 --device cuda:$device --task node --num_seeds 20 \
  python EDHNN/EDHNN_train.py --data cora_coauth --lr 0.001 --restart_alpha 0.8 --device cuda:$device --task node --num_seeds 20 \
  python EDHNN/EDHNN_train.py --data imdb --lr 0.001 --restart_alpha 1 --device cuda:$device --task node --num_seeds 20 \
  python EDHNN/EDHNN_train.py --data house --lr 0.01 --restart_alpha 1 --device cuda:$device --task node --num_seeds 20 \
  python EDHNN/EDHNN_train.py --data pubmed_cite --lr 0.01 --restart_alpha 1 --device cuda:$device --task node --num_seeds 20 \
  python EDHNN/EDHNN_train.py --data dblp_coauth --lr 0.001 --restart_alpha 0.9 --device cuda:$device --task node --num_seeds 20 \
  python EDHNN/EDHNN_train.py --data aminer --lr 0.01 --restart_alpha 0.9 --device cuda:$device --task node --num_seeds 20 \
  python EDHNN/EDHNN_train.py --data modelnet_40 --lr 0.01 --restart_alpha 1 --device cuda:$device --task node --num_seeds 20 \
  python EDHNN/EDHNN_train.py --data news --lr 0.001 --restart_alpha 0.9 --device cuda:$device --task node --num_seeds 20'
```

<small>한 줄이 데이터셋 하나. `--gpu`/`--device` 값은 스크립트 변수(`$gpu`)로 바꿔 쓴다.</small>

## 파일

| 항목 | 내용 |
|---|---|
| 스크립트 | `118.sh` · `exp.sh` · `exp_edge.sh` · `time_node.sh` |
| 실행에 쓴 run-scripts | `edge-fast-first-gpu1.sh` · `edge-fast-resume-gpu1.sh` · `edge-known-models-gpu1.sh` · `edge-six-resume-gpu1.sh` · `formal118-edhnn-node-gpu0.sh` · `formal118-house-gpu0.sh` |
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
- restart_alpha: {0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0}
```

관련: [[실행 규약]] · [[ED-HNN]]
<!-- AUTO:END -->

## 함정과 판단

<!-- 이 모델을 돌리며 알게 된 것: 실패 원인, 고친 것, 다시 보지 말아야 할 길. AUTO 구간은 덮어써진다. -->

