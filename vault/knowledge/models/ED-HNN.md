---
type: model
code_dir: EDHNN
nc_done: 6
nc_agree: 6
hp_done: 6
hp_agree: 6
max_abs_delta: 1.1
worst_cell: "노드 분류 Citeseer +1.1"
status: complete
updated: 2026-09-15 15:36
tags: [hgnn/model]
---

<!-- AUTO:BEGIN -->
# ED-HNN

실행법 → [[ED-HNN 실행]] · 코드 `EDHNN/` · 결과 `results/result_*_EDHNN_*.txt` · <small>갱신 2026-09-15 15:36</small>

NC 6/6 일치 · HP 6/6 일치 · 최대 편차 노드 분류 Citeseer +1.1

## Node classification — Table 3 · Accuracy

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 34.0 <span class="sd">±8.8</span> | 32.9 | <span class="d ok">+1.1</span> |  |
| [[Cora-CA]] | 36.5 <span class="sd">±7.5</span> | 36.3 | <span class="d ok">+0.2</span> |  |
| [[IMDB]] | 38.0 <span class="sd">±2.8</span> | 37.2 | <span class="d ok">+0.8</span> |  |
| [[House]] | 71.7 <span class="sd">±4.8</span> | 71.0 | <span class="d ok">+0.7</span> |  |
| [[Pubmed]] | 61.0 <span class="sd">±3.9</span> | 61.9 | <span class="d ok">−0.9</span> |  |
| [[AMiner]] | 26.6 <span class="sd">±3.0</span> | 27.1 | <span class="d ok">−0.5</span> |  |
| [[DBLP-A]] | — | 58.3 |  | blocked-data |
| [[MN-40]] | — | 73.0 |  | blocked-data |
| [[20News]] | — | 75.7 |  | blocked-data |

## Hyperedge prediction — Table 4 · AUROC

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 58.1 <span class="sd">±2.8</span> | 58.0 | <span class="d ok">+0.1</span> |  |
| [[Cora-CA]] | 59.2 <span class="sd">±3.2</span> | 58.9 | <span class="d ok">+0.3</span> |  |
| [[IMDB]] | 49.1 <span class="sd">±1.3</span> | 49.4 | <span class="d ok">−0.3</span> |  |
| [[House]] | 50.3 <span class="sd">±0.9</span> | 50.6 | <span class="d ok">−0.3</span> |  |
| [[Pubmed]] | 53.3 <span class="sd">±3.1</span> | 53.2 | <span class="d ok">+0.1</span> |  |
| [[AMiner]] | 56.8 <span class="sd">±4.5</span> | 56.0 | <span class="d ok">+0.8</span> |  |
| [[DBLP-P]] | — | 51.2 |  | pending |
| [[20News]] | — | 51.4 |  | blocked-data |

표기 · 값 <span class="sd">±표준편차</span> · Δ = 우리 − 논문 · <span class="d ok">+0.3</span> ±2 이내 · <span class="d warn">+3.0</span> 2–5 · <span class="d bad">+7.0</span> 5 초과 · <span class="lim">OOM</span> 논문이 수치를 못 낸 칸 · — 미실행·보류
<!-- AUTO:END -->

## 메모


