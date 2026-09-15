---
type: protocol
model: HyperGCL
env: hgnn-hypergcl
updated: 2026-09-15 15:36
tags: [hgnn/protocol]
---

<!-- AUTO:BEGIN -->
# HyperGCL 실행

결과 → [[HyperGCL]] · 코드 `HyperGCL/` · 환경 `hgnn-hypergcl` · <small>갱신 2026-09-15 15:36</small>

## 정식 명령 (`HyperGCL/118.sh`)

`118.sh` 가 없다. 아래 스크립트 목록에서 정식 설정을 확인할 것.

## 파일

| 항목 | 내용 |
|---|---|
| 스크립트 | `exp_node.sh` · `time_node.sh` |
| 실행에 쓴 run-scripts | `edge-hypergcl-six-after-tricl-gpu1.sh` · `formal118-house-remaining-gpu0.sh` · `formal118-house-resume-gpu0.sh` · `formal118-pending5-gpu0.sh` · `hypergcl-after-repairs-gpu0.sh` · `hypergcl-gpu-path-resume-gpu0.sh` · `node-priority-order-after-hypergcn.sh` |
| 게이트 파일 | — |
| 정식 완료 | NC 3칸 · HP 4칸 · CD 0칸 |
| 돌리지 말 것 | DBLP-P (HP), DBLP-P (CD) |

## info.txt

```
Hyperparameter
- num_layers: 2
- hidden_dim: 128
- drop rate: 0.5
- weight decay: 10^-6
- lr: {0.01 0.001 0.0001}
- g_lr: {0.01 0.001 0.0001}
- a_l: {0.5 1 2}
```

관련: [[실행 규약]] · [[HyperGCL]]
<!-- AUTO:END -->

## 함정과 판단

<!-- 이 모델을 돌리며 알게 된 것: 실패 원인, 고친 것, 다시 보지 말아야 할 길. AUTO 구간은 덮어써진다. -->

