---
type: model
code_dir: UniGCN2
nc_done: 6
nc_agree: 5
hp_done: 6
hp_agree: 6
max_abs_delta: 2.2
worst_cell: "노드 분류 Cora-CA −2.2"
status: complete
updated: 2026-09-15 15:36
tags: [hgnn/model]
---

<!-- AUTO:BEGIN -->
# UniGCN2

실행법 → [[UniGCN2 실행]] · 코드 `UniGCN2/` · 결과 `results/result_*_UniGCN2_*.txt` · <small>갱신 2026-09-15 15:36</small>

NC 5/6 일치 · HP 6/6 일치 · 최대 편차 노드 분류 Cora-CA −2.2

## Node classification — Table 3 · Accuracy

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 41.5 <span class="sd">±9.2</span> | 39.6 | <span class="d ok">+1.9</span> |  |
| [[Cora-CA]] | 53.1 <span class="sd">±7.3</span> | 55.3 | <span class="d warn">−2.2</span> |  |
| [[IMDB]] | 42.5 <span class="sd">±3.2</span> | 41.6 | <span class="d ok">+0.9</span> |  |
| [[House]] | 58.7 <span class="sd">±10.1</span> | 58.8 | <span class="d ok">−0.1</span> |  |
| [[Pubmed]] | 72.5 <span class="sd">±4.6</span> | 72.6 | <span class="d ok">−0.1</span> |  |
| [[AMiner]] | 32.2 <span class="sd">±1.8</span> | 32.3 | <span class="d ok">−0.1</span> |  |
| [[DBLP-A]] | — | 58.7 |  | blocked-data |
| [[MN-40]] | — | 79.7 |  | blocked-data |
| [[20News]] | — | 76.8 |  | blocked-data |

## Hyperedge prediction — Table 4 · AUROC

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 60.3 <span class="sd">±2.1</span> | 60.2 | <span class="d ok">+0.1</span> |  |
| [[Cora-CA]] | 52.2 <span class="sd">±4.5</span> | 51.9 | <span class="d ok">+0.3</span> |  |
| [[IMDB]] | 57.1 <span class="sd">±6.0</span> | 57.5 | <span class="d ok">−0.4</span> |  |
| [[House]] | 50.0 <span class="sd">±0.0</span> | 50.0 | <span class="d ok">+0.0</span> |  |
| [[Pubmed]] | 69.1 <span class="sd">±1.0</span> | 69.1 | <span class="d ok">+0.0</span> |  |
| [[AMiner]] | 46.2 <span class="sd">±4.5</span> | 45.9 | <span class="d ok">+0.3</span> |  |
| [[DBLP-P]] | — | 60.2 |  | pending |
| [[20News]] | — | 50.0 |  | blocked-data |

표기 · 값 <span class="sd">±표준편차</span> · Δ = 우리 − 논문 · <span class="d ok">+0.3</span> ±2 이내 · <span class="d warn">+3.0</span> 2–5 · <span class="d bad">+7.0</span> 5 초과 · <span class="lim">OOM</span> 논문이 수치를 못 낸 칸 · — 미실행·보류
<!-- AUTO:END -->

## 메모


