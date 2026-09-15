---
type: protocol
model: MaskGAE
env: hgnn-pyg
updated: 2026-09-15 19:20
tags: [hgnn/protocol]
---

<!-- AUTO:BEGIN -->
# MaskGAE 실행

결과 → [[MaskGAE]] · 코드 `MaskGAE/` · 환경 `hgnn-pyg` · <small>갱신 2026-09-15 19:20</small>

## 정식 명령 (`MaskGAE/118.sh`)

```bash
conda run --no-capture-output -n hgnn-pyg bash -lc '\
  cd /home/dms2/hojin_workspace/hgnn && \
  python MaskGAE/MaskGAE_train.py --data citeseer_cite --num_seeds 20 --lr 0.0001 --device $device --task node --alpha 0.002 --p 0.5 \
  python MaskGAE/MaskGAE_train.py --data cora_cite --num_seeds 20 --lr 0.001 --device $device --task node --alpha 0.003 --p 0.75 \
  python MaskGAE/MaskGAE_train.py --data dblp_copub --num_seeds 20 --lr 0.001 --device $device --task node --alpha 0.003 --p 0.75 \
  python MaskGAE/MaskGAE_train.py --data cora_coauth --num_seeds 20 --lr 0.001 --device $device --task node --alpha 0.003 --p 0.5 \
  python MaskGAE/MaskGAE_train.py --data imdb --num_seeds 20 --lr 0.001 --device $device --task node --alpha 0.001 --p 0.25 \
  python MaskGAE/MaskGAE_train.py --data house --num_seeds 20 --lr 0.01 --device $device --task node --alpha 0.003 --p 0.5 \
  python MaskGAE/MaskGAE_train.py --data pubmed_cite --num_seeds 20 --lr 0.01 --device $device --task node --alpha 0.002 --p 0.75 \
  python MaskGAE/MaskGAE_train.py --data dblp_coauth --num_seeds 20 --lr 0.001 --device $device --task node --alpha 0.001 --p 0.75 \
  python MaskGAE/MaskGAE_train.py --data aminer --num_seeds 20 --lr 0.0001 --device $device --task node --alpha 0.002 --p 0.5 \
  python MaskGAE/MaskGAE_train.py --data modelnet_40 --num_seeds 20 --lr 0.01 --device $device --task node --alpha 0.002 --p 0.5'
```

<small>한 줄이 데이터셋 하나. `--gpu`/`--device` 값은 스크립트 변수(`$gpu`)로 바꿔 쓴다.</small>

## 파일

| 항목 | 내용 |
|---|---|
| 스크립트 | `118.sh` · `exp_edge.sh` · `exp_node.sh` · `time_node.sh` |
| 실행에 쓴 run-scripts | `edge-fast-first-gpu1.sh` · `edge-fast-resume-gpu1.sh` · `edge-known-models-gpu1.sh` · `edge-six-resume-gpu1.sh` · `formal118-house-remaining-gpu1.sh` · `formal118-maskgae-node-gpu1.sh` |
| 게이트 파일 | — |
| 정식 완료 | NC 6칸 · HP 6칸 · CD 6칸 |
| 돌리지 말 것 | 20News (HP), 20News (CD) |

## info.txt

```
Hyperparameter
- num_layers(encoder_layers,decoder_layers): 2
- hidden_dim(encoder_channels,hidden_channels,decoder_channels): 128
- drop rate(encoder_dropout,decoder_drop_out): 0.5
- weight decay,nodeclas_weight_decay: 1e^-6
- lr: {0.01,0.001,0.0001}
- alpha: {0.001,0.002,0.003}
- p: {0.25,0.5,0.75}
```

관련: [[실행 규약]] · [[MaskGAE]]
<!-- AUTO:END -->

## 함정과 판단

<!-- 이 모델을 돌리며 알게 된 것: 실패 원인, 고친 것, 다시 보지 말아야 할 길. AUTO 구간은 덮어써진다. -->

