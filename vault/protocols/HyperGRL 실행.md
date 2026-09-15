---
type: protocol
model: HyperGRL
env: hgnn-dgl-src
updated: 2026-09-15 15:36
tags: [hgnn/protocol]
---

<!-- AUTO:BEGIN -->
# HyperGRL 실행

결과 → [[HyperGRL]] · 코드 `HyperGRL/` · 환경 `hgnn-dgl-src` · <small>갱신 2026-09-15 15:36</small>

## 정식 명령 (`HyperGRL/118.sh`)

```bash
conda run --no-capture-output -n hgnn-dgl-src bash -lc '\
  cd /home/dms2/hojin_workspace/hgnn && \
  python HyperGRL/hyperGRL_train_our.py --data house --device cuda:1 --num_seeds 20 \
  python HyperGRL/hyperGRL_train_our.py --data pubmed_cite --device cuda:1 --num_seeds 20 \
  python HyperGRL/hyperGRL_train_our.py --data dblp_coauth --device cuda:1 --num_seeds 20 \
  python HyperGRL/hyperGRL_train_our.py --data aminer --device cuda:1 --num_seeds 20 \
  python HyperGRL/hyperGRL_train_our.py --data modelnet_40 --device cuda:1 --num_seeds 20 \
  python HyperGRL/hyperGRL_train_our.py --data news --device cuda:1 --num_seeds 20'
```

<small>한 줄이 데이터셋 하나. `--gpu`/`--device` 값은 스크립트 변수(`$gpu`)로 바꿔 쓴다.</small>

## 파일

| 항목 | 내용 |
|---|---|
| 스크립트 | `118.sh` · `exp_embed.sh` · `exp_time.sh` |
| 실행에 쓴 run-scripts | `formal118-house-remaining-gpu0.sh` · `formal118-house-resume-gpu0.sh` · `formal118-pending5-gpu0.sh` · `node-failure-repair-gpu1.sh` · `node-priority-order-after-hypergcn.sh` |
| 게이트 파일 | — |
| 정식 완료 | NC 2칸 · HP 0칸 · CD 0칸 |
| 돌리지 말 것 | Citeseer (NC), IMDB (NC), Pubmed (NC), AMiner (NC), 20News (HP), 20News (CD) |

관련: [[실행 규약]] · [[HyperGRL]]
<!-- AUTO:END -->

## 함정과 판단

<!-- 이 모델을 돌리며 알게 된 것: 실패 원인, 고친 것, 다시 보지 말아야 할 길. AUTO 구간은 덮어써진다. -->

