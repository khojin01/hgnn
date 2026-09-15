---
type: model
code_dir: AllSet
nc_done: 6
nc_agree: 6
hp_done: 6
hp_agree: 6
max_abs_delta: 1.6
worst_cell: "노드 분류 Pubmed −1.6"
status: complete
updated: 2026-09-15 15:36
tags: [hgnn/model]
---

<!-- AUTO:BEGIN -->
# AllSet

실행법 → [[AllSet 실행]] · 코드 `AllSet/` · 결과 `results/result_*_AllSet_*.txt` · <small>갱신 2026-09-15 15:36</small>

NC 6/6 일치 · HP 6/6 일치 · 최대 편차 노드 분류 Pubmed −1.6

## Node classification — Table 3 · Accuracy

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 41.0 <span class="sd">±8.3</span> | 41.1 | <span class="d ok">−0.1</span> |  |
| [[Cora-CA]] | 53.1 <span class="sd">±6.4</span> | 53.6 | <span class="d ok">−0.5</span> |  |
| [[IMDB]] | 40.5 <span class="sd">±4.6</span> | 41.7 | <span class="d ok">−1.2</span> |  |
| [[House]] | 50.2 <span class="sd">±2.8</span> | 50.3 | <span class="d ok">−0.1</span> |  |
| [[Pubmed]] | 72.5 <span class="sd">±6.2</span> | 74.1 | <span class="d ok">−1.6</span> |  |
| [[AMiner]] | 29.6 <span class="sd">±3.5</span> | 29.8 | <span class="d ok">−0.2</span> |  |
| [[DBLP-A]] | — | 64.9 |  | deferred |
| [[MN-40]] | — | 89.4 |  | blocked-data |
| [[20News]] | — | 77.2 |  | blocked-data |

## Hyperedge prediction — Table 4 · AUROC

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 50.7 <span class="sd">±3.3</span> | 51.8 | <span class="d ok">−1.1</span> |  |
| [[Cora-CA]] | 50.8 <span class="sd">±2.5</span> | 51.2 | <span class="d ok">−0.4</span> |  |
| [[IMDB]] | 50.6 <span class="sd">±1.7</span> | 50.3 | <span class="d ok">+0.3</span> |  |
| [[House]] | 53.5 <span class="sd">±5.1</span> | 53.5 | <span class="d ok">+0.0</span> |  |
| [[Pubmed]] | 52.7 <span class="sd">±1.6</span> | 52.3 | <span class="d ok">+0.4</span> |  |
| [[AMiner]] | 50.5 <span class="sd">±1.3</span> | 51.0 | <span class="d ok">−0.5</span> |  |
| [[DBLP-P]] | — | 53.2 |  | pending |
| [[20News]] | — | 50.1 |  | blocked-data |

표기 · 값 <span class="sd">±표준편차</span> · Δ = 우리 − 논문 · <span class="d ok">+0.3</span> ±2 이내 · <span class="d warn">+3.0</span> 2–5 · <span class="d bad">+7.0</span> 5 초과 · <span class="lim">OOM</span> 논문이 수치를 못 낸 칸 · — 미실행·보류
<!-- AUTO:END -->

## 메모


