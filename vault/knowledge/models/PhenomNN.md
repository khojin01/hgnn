---
type: model
code_dir: PhenomNN
nc_done: 5
nc_agree: 4
hp_done: 5
hp_agree: 5
max_abs_delta: 2.9
worst_cell: "노드 분류 Citeseer +2.9"
status: partial
updated: 2026-09-15 15:36
tags: [hgnn/model]
---

<!-- AUTO:BEGIN -->
# PhenomNN

실행법 → [[PhenomNN 실행]] · 코드 `PhenomNN/` · 결과 `results/result_*_PhenomNN_*.txt` · <small>갱신 2026-09-15 15:36</small>

NC 4/5 일치 · HP 5/5 일치 · 최대 편차 노드 분류 Citeseer +2.9

## Node classification — Table 3 · Accuracy

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 45.1 <span class="sd">±11.7</span> | 42.2 | <span class="d warn">+2.9</span> |  |
| [[Cora-CA]] | 56.3 <span class="sd">±7.5</span> | 56.2 | <span class="d ok">+0.1</span> |  |
| [[IMDB]] | 42.1 <span class="sd">±2.9</span> | 42.1 | <span class="d ok">+0.0</span> |  |
| [[House]] | 69.4 <span class="sd">±7.0</span> | 69.4 | <span class="d ok">+0.0</span> |  |
| [[Pubmed]] | 76.7 <span class="sd">±3.6</span> | 76.8 | <span class="d ok">−0.1</span> |  |
| [[AMiner]] | <span class="lim">OOM</span> | — |  | O.O.M (paper skip) |
| [[DBLP-A]] | — | 70.3 |  | blocked-data |
| [[MN-40]] | — | 94.0 |  | blocked-data |
| [[20News]] | — | — |  | blocked-data |

## Hyperedge prediction — Table 4 · AUROC

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 54.3 <span class="sd">±2.2</span> | 54.5 | <span class="d ok">−0.2</span> |  |
| [[Cora-CA]] | 50.7 <span class="sd">±1.3</span> | 50.3 | <span class="d ok">+0.4</span> |  |
| [[IMDB]] | 49.8 <span class="sd">±0.9</span> | 49.7 | <span class="d ok">+0.1</span> |  |
| [[House]] | 50.6 <span class="sd">±1.2</span> | 50.8 | <span class="d ok">−0.2</span> |  |
| [[Pubmed]] | 65.1 <span class="sd">±1.7</span> | 64.0 | <span class="d ok">+1.1</span> |  |
| [[AMiner]] | <span class="lim">OOM</span> | — |  | O.O.M skip |
| [[DBLP-P]] | <span class="lim">OOM</span> | — |  | O.O.M skip |
| [[20News]] | <span class="lim">OOT</span> | — |  | O.O.T skip |

표기 · 값 <span class="sd">±표준편차</span> · Δ = 우리 − 논문 · <span class="d ok">+0.3</span> ±2 이내 · <span class="d warn">+3.0</span> 2–5 · <span class="d bad">+7.0</span> 5 초과 · <span class="lim">OOM</span> 논문이 수치를 못 낸 칸 · — 미실행·보류
<!-- AUTO:END -->

## 메모


