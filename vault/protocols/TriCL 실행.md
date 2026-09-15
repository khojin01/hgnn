---
type: protocol
model: TriCL
env: hgnn-pyg
updated: 2026-09-15 19:33
tags: [hgnn/protocol]
---

<!-- AUTO:BEGIN -->
# TriCL 실행

결과 → [[TriCL]] · 코드 `TriCL/` · 환경 `hgnn-pyg` · <small>갱신 2026-09-15 19:33</small>

## 정식 명령 (`TriCL/118.sh`)

```bash
conda run --no-capture-output -n hgnn-pyg bash -lc '\
  cd /home/dms2/hojin_workspace/hgnn && \
  python TriCL/TriCL_train.py --data dblp_coauth --num_seeds 20 --device $device'
```

<small>한 줄이 데이터셋 하나. `--gpu`/`--device` 값은 스크립트 변수(`$gpu`)로 바꿔 쓴다.</small>

## 파일

| 항목 | 내용 |
|---|---|
| 스크립트 | `118.sh` · `exp_embed.sh` · `time_node.sh` |
| 실행에 쓴 run-scripts | `edge-tricl-six-after-gpu1.sh` · `formal118-house-remaining-gpu1.sh` · `formal118-house-resume-gpu1.sh` · `formal118-pending5-gpu1.sh` · `node-failure-repair-gpu1.sh` · `node-priority-order-after-hypergcn.sh` |
| 게이트 파일 | — |
| 정식 완료 | NC 6칸 · HP 6칸 · CD 2칸 |
| 돌리지 말 것 | 없음 |

관련: [[실행 규약]] · [[TriCL]]
<!-- AUTO:END -->

## 함정과 판단

<!-- 이 모델을 돌리며 알게 된 것: 실패 원인, 고친 것, 다시 보지 말아야 할 길. AUTO 구간은 덮어써진다. -->

