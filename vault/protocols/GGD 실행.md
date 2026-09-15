---
type: protocol
model: GGD
env: hgnn-pyg
updated: 2026-09-15 19:19
tags: [hgnn/protocol]
---

<!-- AUTO:BEGIN -->
# GGD 실행

결과 → [[GGD]] · 코드 `H-GD/` · 환경 `hgnn-pyg` · <small>갱신 2026-09-15 19:19</small>

## 정식 명령 (`H-GD/118.sh`)

```bash
conda run --no-capture-output -n hgnn-pyg bash -lc '\
  cd /home/dms2/hojin_workspace/hgnn && \
  python H-GD/H-GD_train.py --data citeseer_cite --num_seeds 20 --lr 0.0001 --device cuda:$device --task node --p_e 0.3 --p_x 0.2 \
  python H-GD/H-GD_train.py --data cora_cite --num_seeds 20 --lr 0.0001 --device cuda:$device --task node --p_e 0.1 --p_x 0.3 \
  python H-GD/H-GD_train.py --data dblp_copub --num_seeds 20 --lr 0.0001 --device cuda:$device --task node --p_e 0.2 --p_x 0.2 \
  python H-GD/H-GD_train.py --data cora_coauth --num_seeds 20 --lr 0.0001 --device cuda:$device --task node --p_e 0.1 --p_x 0.1 \
  python H-GD/H-GD_train.py --data imdb --num_seeds 20 --lr 0.001 --device cuda:$device --task node --p_e 0.2 --p_x 0.1 \
  python H-GD/H-GD_train.py --data house --num_seeds 20 --lr 0.0001 --device cuda:$device --task node --p_e 0.2 --p_x 0.3 \
  python H-GD/H-GD_train.py --data pubmed_cite --num_seeds 20 --lr 0.0001 --device cuda:$device --task node --p_e 0.4 --p_x 0.4 \
  python H-GD/H-GD_train.py --data aminer --num_seeds 20 --lr 0.0001 --device cuda:$device --task node --p_e 0.2 --p_x 0.2 \
  python H-GD/H-GD_train.py --data modelnet_40 --num_seeds 20 --lr 0.0001 --device cuda:$device --task node --p_e 0.2 --p_x 0.2 \
  python H-GD/H-GD_train.py --data dblp_coauth --num_seeds 20 --lr 0.0001 --device cuda:$device --task node --p_e 0.2 --p_x 0.2 \
  python H-GD/H-GD_train.py --data news --num_seeds 20 --lr 0.0001 --device cuda:$device --task node --p_e 0.2 --p_x 0.2'
```

<small>한 줄이 데이터셋 하나. `--gpu`/`--device` 값은 스크립트 변수(`$gpu`)로 바꿔 쓴다.</small>

## 파일

| 항목 | 내용 |
|---|---|
| 스크립트 | `118.sh` · `exp_node.sh` · `time_node.sh` |
| 실행에 쓴 run-scripts | `edge-hgd-six-gpu0.sh` · `formal118-hgd-node-gpu0.sh` · `formal118-house-gpu0.sh` |
| 게이트 파일 | `villain-edge-check.ok` |
| 정식 완료 | NC 6칸 · HP 6칸 · CD 0칸 |
| 돌리지 말 것 | 없음 |

## info.txt

```
Hyperparameter
- hid_dim: 128
- weight decay: 1e^-6
- p_x: {0.2,0.3,0.4}
- p_e: {0.2,0.3,0.4}
- lr: {0.01,0.001,0.0001}
```

관련: [[실행 규약]] · [[GGD]]
<!-- AUTO:END -->

## 함정과 판단

<!-- 이 모델을 돌리며 알게 된 것: 실패 원인, 고친 것, 다시 보지 말아야 할 길. AUTO 구간은 덮어써진다. -->

