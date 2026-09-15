---
type: protocol
model: HypeBoy
env: hgnn-pyg
updated: 2026-09-15 22:19
tags: [hgnn/protocol]
---

<!-- AUTO:BEGIN -->
# HypeBoy 실행

결과 → [[HypeBoy]] · 코드 `Hypeboy/` · 환경 `hgnn-pyg` · <small>갱신 2026-09-15 22:19</small>

## 정식 명령 (`Hypeboy/118.sh`)

```bash
conda run --no-capture-output -n hgnn-pyg bash -lc '\
  cd /home/dms2/hojin_workspace/hgnn && \
  python Hypeboy/Hypeboy_train.py --data citeseer_cite --task node --device cuda:0 \
  python Hypeboy/Hypeboy_train.py --data cora_cite --task node --device cuda:0 \
  python Hypeboy/Hypeboy_train.py --data dblp_copub --task node --device cuda:0 \
  python Hypeboy/Hypeboy_train.py --data cora_coauth --task node --device cuda:0 \
  python Hypeboy/Hypeboy_train.py --data imdb --task node --device cuda:0 \
  python Hypeboy/Hypeboy_train.py --data house --task node --device cuda:0 \
  python Hypeboy/Hypeboy_train.py --data pubmed_cite --task node --device cuda:0 \
  python Hypeboy/Hypeboy_train.py --data dblp_coauth --task node --device cuda:0 \
  python Hypeboy/Hypeboy_train.py --data aminer --task node --device cuda:0 \
  python Hypeboy/Hypeboy_train.py --data modelnet_40 --task node --device cuda:0 \
  python Hypeboy/Hypeboy_train.py --data news --task node --device cuda:0'
```

<small>한 줄이 데이터셋 하나. `--gpu`/`--device` 값은 스크립트 변수(`$gpu`)로 바꿔 쓴다.</small>

## 파일

| 항목 | 내용 |
|---|---|
| 스크립트 | `118.sh` · `time_node.sh` |
| 실행에 쓴 run-scripts | `cd-hypeboy.sh` · `edge-phenom-hypeboy-after-hgd-gpu0.sh` · `formal118-house-gpu0.sh` · `formal118-hypeboy-node-gpu0.sh` |
| 게이트 파일 | — |
| 정식 완료 | NC 6칸 · HP 6칸 · CD 5칸 |
| 돌리지 말 것 | 없음 |

관련: [[실행 규약]] · [[HypeBoy]]
<!-- AUTO:END -->

## 함정과 판단

<!-- 이 모델을 돌리며 알게 된 것: 실패 원인, 고친 것, 다시 보지 말아야 할 길. AUTO 구간은 덮어써진다. -->

