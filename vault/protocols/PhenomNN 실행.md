---
type: protocol
model: PhenomNN
env: hgnn-pyg
updated: 2026-09-15 15:36
tags: [hgnn/protocol]
---

<!-- AUTO:BEGIN -->
# PhenomNN 실행

결과 → [[PhenomNN]] · 코드 `PhenomNN/` · 환경 `hgnn-pyg` · <small>갱신 2026-09-15 15:36</small>

## 정식 명령 (`PhenomNN/118.sh`)

```bash
conda run --no-capture-output -n hgnn-pyg bash -lc '\
  cd /home/dms2/hojin_workspace/hgnn && \
  python PhenomNN/PhenomNN_train.py --data citeseer_cite --num_seeds 20 --lr 0.01 --device cuda:$device --task node --lam0 10 --lam1 1 --alp 1 --prop_step 16 --task node \
  python PhenomNN/PhenomNN_train.py --data cora_cite --num_seeds 20 --lr 0.01 --device cuda:$device --task node --lam0 80 --lam1 20 --alp 1 --prop_step 16 --task node \
  python PhenomNN/PhenomNN_train.py --data dblp_copub --num_seeds 20 --lr 0.01 --device cuda:$device --task node --lam0 0.5 --lam1 20 --alp 1 --prop_step 8 --task node \
  python PhenomNN/PhenomNN_train.py --data cora_coauth --num_seeds 20 --lr 0.01 --device cuda:$device --task node --lam0 20 --lam1 10 --alp 0.1 --prop_step 8 --task node \
  python PhenomNN/PhenomNN_train.py --data imdb --num_seeds 20 --lr 0.01 --device cuda:$device --task node --lam0 0 --lam1 5 --alp 0.01 --prop_step 8 --task node \
  python PhenomNN/PhenomNN_train.py --data house --num_seeds 20 --lr 0.01 --device cuda:$device --task node --lam0 0.01 --lam1 10 --alp 1 --prop_step 8 --task node \
  python PhenomNN/PhenomNN_train.py --data pubmed_cite --num_seeds 20 --lr 0.01 --device cuda:$device --task node --lam0 10 --lam1 5 --alp 1 --prop_step 16 --task node \
  python PhenomNN/PhenomNN_train.py --data modelnet_40 --num_seeds 20 --lr 0.01 --device cuda:$device --task node --lam0 10 --lam1 10 --alp 0.1 --prop_step 8 --task node'
```

<small>한 줄이 데이터셋 하나. `--gpu`/`--device` 값은 스크립트 변수(`$gpu`)로 바꿔 쓴다.</small>

## 파일

| 항목 | 내용 |
|---|---|
| 스크립트 | `118.sh` · `exp.sh` · `time_node.sh` |
| 실행에 쓴 run-scripts | `edge-phenom-hypeboy-after-hgd-gpu0.sh` · `edge-sehssl-six-after-gpu0.sh` · `formal118-house-remaining-gpu0.sh` · `formal118-house-resume-gpu0.sh` · `formal118-pending5-gpu0.sh` · `node-failure-repair-gpu1.sh` · `node-priority-order-after-hypergcn.sh` |
| 게이트 파일 | — |
| 정식 완료 | NC 5칸 · HP 5칸 |
| 돌리지 말 것 | AMiner (NC), AMiner (HP), DBLP-P (HP), 20News (HP) |

## info.txt

```
Hyperparameter
- num_layers: 2
- hidden_dim: 128
- drop rate: 0.5
- weight decay: 10^-6
- lr: {0.05,0.01,0.005,0.001,0.0005,0.0001}
- lam0: {0, 0.1, 20, 50, 80, 100}
- lam1: {0, 0.1, 20, 50, 80, 100}
- alp: {0.05, 0.1, 1}
- prop_step: {4, 8, 16}
```

관련: [[실행 규약]] · [[PhenomNN]]
<!-- AUTO:END -->

## 함정과 판단

<!-- 이 모델을 돌리며 알게 된 것: 실패 원인, 고친 것, 다시 보지 말아야 할 길. AUTO 구간은 덮어써진다. -->

