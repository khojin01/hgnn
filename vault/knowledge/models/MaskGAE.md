---
type: model
code_dir: MaskGAE
nc_done: 6
nc_agree: 5
hp_done: 6
hp_agree: 6
cd_done: 6
cd_agree: 6
max_abs_delta: 3.3
worst_cell: "노드 분류 Cora-CA −3.3"
status: complete
updated: 2026-09-15 19:20
tags: [hgnn/model]
---

<!-- AUTO:BEGIN -->
# MaskGAE

실행법 → [[MaskGAE 실행]] · 코드 `MaskGAE/` · 결과 `results/result_*_MaskGAE_*.txt` · <small>갱신 2026-09-15 19:20</small>

NC 5/6 일치 · HP 6/6 일치 · CD 6/6 일치 · 최대 편차 노드 분류 Cora-CA −3.3

## Node classification — Table 3 · Accuracy

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 52.7 <span class="sd">±10.4</span> | 53.2 | <span class="d ok">−0.5</span> |  |
| [[Cora-CA]] | 56.5 <span class="sd">±6.8</span> | 59.8 | <span class="d warn">−3.3</span> |  |
| [[IMDB]] | 44.7 <span class="sd">±3.5</span> | 45.0 | <span class="d ok">−0.3</span> |  |
| [[House]] | 52.2 <span class="sd">±3.0</span> | 53.0 | <span class="d ok">−0.8</span> |  |
| [[Pubmed]] | 74.6 <span class="sd">±4.2</span> | 75.4 | <span class="d ok">−0.8</span> |  |
| [[AMiner]] | 32.5 <span class="sd">±1.7</span> | 33.8 | <span class="d ok">−1.3</span> |  |
| [[DBLP-A]] | — | 78.2 |  | blocked-data |
| [[MN-40]] | — | 91.0 |  | blocked-data |
| [[20News]] | — | — |  | blocked-data |

## Hyperedge prediction — Table 4 · AUROC

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 86.7 <span class="sd">±1.7</span> | 86.7 | <span class="d ok">+0.0</span> |  |
| [[Cora-CA]] | 76.1 <span class="sd">±2.2</span> | 76.5 | <span class="d ok">−0.4</span> |  |
| [[IMDB]] | 54.5 <span class="sd">±1.3</span> | 54.4 | <span class="d ok">+0.1</span> |  |
| [[House]] | 88.2 <span class="sd">±3.6</span> | 88.0 | <span class="d ok">+0.2</span> |  |
| [[Pubmed]] | 95.5 <span class="sd">±0.3</span> | 95.5 | <span class="d ok">+0.0</span> |  |
| [[AMiner]] | 87.6 <span class="sd">±0.9</span> | 87.6 | <span class="d ok">+0.0</span> |  |
| [[DBLP-P]] | — | 94.8 |  | pending |
| [[20News]] | <span class="lim">OOT</span> | — |  | O.O.T skip |

## Community detection — Table 5 · NMI

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 34.4 <span class="sd">±0.1</span> | 34.8 | <span class="d ok">−0.4</span> |  |
| [[Cora-CA]] | 39.4 <span class="sd">±1.3</span> | 38.0 | <span class="d ok">+1.4</span> |  |
| [[IMDB]] | 3.2 <span class="sd">±0.0</span> | 2.9 | <span class="d ok">+0.3</span> |  |
| [[House]] | 0.2 <span class="sd">±0.0</span> | 1.4 | <span class="d ok">−1.2</span> |  |
| [[Pubmed]] | 29.9 <span class="sd">±0.0</span> | 28.9 | <span class="d ok">+1.0</span> |  |
| [[AMiner]] | 36.3 <span class="sd">±0.1</span> | 36.3 | <span class="d ok">+0.0</span> |  |
| [[DBLP-P]] | — | 61.6 |  | pending |
| [[20News]] | <span class="lim">OOT</span> | — |  | O.O.T skip |

표기 · 값 <span class="sd">±표준편차</span> · Δ = 우리 − 논문 · <span class="d ok">+0.3</span> ±2 이내 · <span class="d warn">+3.0</span> 2–5 · <span class="d bad">+7.0</span> 5 초과 · <span class="lim">OOM</span> 논문이 수치를 못 낸 칸 · — 미실행·보류
<!-- AUTO:END -->

## 메모


