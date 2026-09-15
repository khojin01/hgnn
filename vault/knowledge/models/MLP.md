---
type: model
code_dir: MLP
nc_done: 6
nc_agree: 6
hp_done: 6
hp_agree: 6
max_abs_delta: 1.2
worst_cell: "노드 분류 Cora-CA +1.2"
status: complete
updated: 2026-09-15 15:36
tags: [hgnn/model]
---

<!-- AUTO:BEGIN -->
# MLP

실행법 → [[MLP 실행]] · 코드 `MLP/` · 결과 `results/result_*_MLP_*.txt` · <small>갱신 2026-09-15 15:36</small>

NC 6/6 일치 · HP 6/6 일치 · 최대 편차 노드 분류 Cora-CA +1.2

## Node classification — Table 3 · Accuracy

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 32.4 <span class="sd">±8.1</span> | 32.4 | <span class="d ok">+0.0</span> |  |
| [[Cora-CA]] | 37.2 <span class="sd">±4.3</span> | 36.0 | <span class="d ok">+1.2</span> |  |
| [[IMDB]] | 38.2 <span class="sd">±2.7</span> | 37.6 | <span class="d ok">+0.6</span> |  |
| [[House]] | 73.1 <span class="sd">±3.2</span> | 73.1 | <span class="d ok">+0.0</span> |  |
| [[Pubmed]] | 62.7 <span class="sd">±3.3</span> | 62.8 | <span class="d ok">−0.1</span> |  |
| [[AMiner]] | 22.4 <span class="sd">±1.4</span> | 22.7 | <span class="d ok">−0.3</span> |  |
| [[DBLP-A]] | — | 56.6 |  | blocked-data |
| [[MN-40]] | — | 88.5 |  | blocked-data |
| [[20News]] | — | 73.3 |  | blocked-data |

## Hyperedge prediction — Table 4 · AUROC

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 65.6 <span class="sd">±2.0</span> | 65.6 | <span class="d ok">+0.0</span> |  |
| [[Cora-CA]] | 58.6 <span class="sd">±2.9</span> | 58.6 | <span class="d ok">+0.0</span> |  |
| [[IMDB]] | 41.7 <span class="sd">±2.5</span> | 42.0 | <span class="d ok">−0.3</span> |  |
| [[House]] | 54.8 <span class="sd">±5.4</span> | 54.8 | <span class="d ok">+0.0</span> |  |
| [[Pubmed]] | 88.3 <span class="sd">±0.6</span> | 88.3 | <span class="d ok">+0.0</span> |  |
| [[AMiner]] | 82.3 <span class="sd">±0.9</span> | 82.3 | <span class="d ok">+0.0</span> |  |
| [[DBLP-P]] | — | 90.2 |  | pending |
| [[20News]] | — | 95.1 |  | blocked-data |

표기 · 값 <span class="sd">±표준편차</span> · Δ = 우리 − 논문 · <span class="d ok">+0.3</span> ±2 이내 · <span class="d warn">+3.0</span> 2–5 · <span class="d bad">+7.0</span> 5 초과 · <span class="lim">OOM</span> 논문이 수치를 못 낸 칸 · — 미실행·보류
<!-- AUTO:END -->

## 메모


