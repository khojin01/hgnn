---
type: model
code_dir: HyperGCN
nc_done: 6
nc_agree: 6
hp_done: 6
hp_agree: 6
max_abs_delta: 0.4
worst_cell: "노드 분류 AMiner −0.4"
status: complete
updated: 2026-09-15 15:36
tags: [hgnn/model]
---

<!-- AUTO:BEGIN -->
# HyperGCN

실행법 → [[HyperGCN 실행]] · 코드 `HyperGCN/` · 결과 `results/result_*_HyperGCN_*.txt` · <small>갱신 2026-09-15 15:36</small>

NC 6/6 일치 · HP 6/6 일치 · 최대 편차 노드 분류 AMiner −0.4

## Node classification — Table 3 · Accuracy

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 33.7 <span class="sd">±7.3</span> | 33.8 | <span class="d ok">−0.1</span> |  |
| [[Cora-CA]] | 45.0 <span class="sd">±9.5</span> | 45.0 | <span class="d ok">+0.0</span> |  |
| [[IMDB]] | 40.6 <span class="sd">±3.2</span> | 40.6 | <span class="d ok">+0.0</span> |  |
| [[House]] | 48.2 <span class="sd">±0.9</span> | 48.2 | <span class="d ok">+0.0</span> |  |
| [[Pubmed]] | 59.3 <span class="sd">±15.2</span> | 59.3 | <span class="d ok">+0.0</span> |  |
| [[AMiner]] | 26.4 <span class="sd">±2.9</span> | 26.8 | <span class="d ok">−0.4</span> |  |
| [[DBLP-A]] | — | 64.3 |  | blocked-data |
| [[MN-40]] | — | 57.8 |  | blocked-data |
| [[20News]] | — | 71.7 |  | blocked-data |

## Hyperedge prediction — Table 4 · AUROC

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 54.9 <span class="sd">±2.1</span> | 54.9 | <span class="d ok">+0.0</span> |  |
| [[Cora-CA]] | 48.9 <span class="sd">±1.6</span> | 49.3 | <span class="d ok">−0.4</span> |  |
| [[IMDB]] | 48.4 <span class="sd">±1.9</span> | 48.4 | <span class="d ok">+0.0</span> |  |
| [[House]] | 87.7 <span class="sd">±2.5</span> | 87.7 | <span class="d ok">+0.0</span> |  |
| [[Pubmed]] | 74.2 <span class="sd">±0.6</span> | 74.1 | <span class="d ok">+0.1</span> |  |
| [[AMiner]] | 50.6 <span class="sd">±2.6</span> | 50.8 | <span class="d ok">−0.2</span> |  |
| [[DBLP-P]] | — | 53.9 |  | pending |
| [[20News]] | — | 55.6 |  | blocked-data |

표기 · 값 <span class="sd">±표준편차</span> · Δ = 우리 − 논문 · <span class="d ok">+0.3</span> ±2 이내 · <span class="d warn">+3.0</span> 2–5 · <span class="d bad">+7.0</span> 5 초과 · <span class="lim">OOM</span> 논문이 수치를 못 낸 칸 · — 미실행·보류
<!-- AUTO:END -->

## 메모


