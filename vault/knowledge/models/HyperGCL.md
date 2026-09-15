---
type: model
code_dir: HyperGCL
nc_done: 3
nc_agree: 0
hp_done: 4
hp_agree: 0
cd_done: 1
cd_agree: 0
max_abs_delta: 45.5
worst_cell: "노드 분류 Cora-CA −45.5"
status: partial
updated: 2026-09-15 22:52
tags: [hgnn/model]
---

<!-- AUTO:BEGIN -->
# HyperGCL

실행법 → [[HyperGCL 실행]] · 코드 `HyperGCL/` · 결과 `results/result_*_HyperGCL_*.txt` · <small>갱신 2026-09-15 22:52</small>

NC 0/3 일치 · HP 0/4 일치 · CD 0/1 일치 · 최대 편차 노드 분류 Cora-CA −45.5

## Node classification — Table 3 · Accuracy

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 18.5 <span class="sd">±3.5</span> | 43.4 | <span class="d bad">−24.9</span> |  |
| [[Cora-CA]] | 16.3 <span class="sd">±4.0</span> | 61.8 | <span class="d bad">−45.5</span> |  |
| [[IMDB]] | — | 48.4 |  | diagnostic only: splits 19–20 (no formal aggregate) |
| [[House]] | 54.6 <span class="sd">±5.5</span> | 63.7 | <span class="d bad">−9.1</span> |  |
| [[Pubmed]] | — | 71.0 |  | pending |
| [[AMiner]] | — | 30.4 |  | pending |
| [[DBLP-A]] | — | 69.5 |  | blocked-data |
| [[MN-40]] | — | 94.6 |  | blocked-data |
| [[20News]] | — | 74.0 |  | blocked-data |

## Hyperedge prediction — Table 4 · AUROC

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 51.9 <span class="sd">±2.9</span> | 73.9 | <span class="d bad">−22.0</span> |  |
| [[Cora-CA]] | 51.1 <span class="sd">±3.1</span> | 81.1 | <span class="d bad">−30.0</span> |  |
| [[IMDB]] | 50.9 <span class="sd">±2.8</span> | 53.8 | <span class="d warn">−2.9</span> |  |
| [[House]] | 63.3 <span class="sd">±9.5</span> | 76.3 | <span class="d bad">−13.0</span> |  |
| [[Pubmed]] | — | 89.6 |  | pending |
| [[AMiner]] | — | 82.1 |  | pending |
| [[DBLP-P]] | <span class="lim">OOM</span> | 83.6 |  | O.O.M skip |
| [[20News]] | — | 76.3 |  | blocked-data |

## Community detection — Table 5 · NMI

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 3.8 <span class="sd">±0.2</span> | 22.2 | <span class="d bad">−18.4</span> |  |
| [[Cora-CA]] | — | 30.6 |  | pending |
| [[IMDB]] | — | 1.4 |  | pending |
| [[House]] | — | 11.5 |  | pending |
| [[Pubmed]] | — | 24.2 |  | pending |
| [[AMiner]] | — | 31.9 |  | pending |
| [[DBLP-P]] | <span class="lim">OOM</span> | — |  | O.O.M skip |
| [[20News]] | — | 38.2 |  | pending |

표기 · 값 <span class="sd">±표준편차</span> · Δ = 우리 − 논문 · <span class="d ok">+0.3</span> ±2 이내 · <span class="d warn">+3.0</span> 2–5 · <span class="d bad">+7.0</span> 5 초과 · <span class="lim">OOM</span> 논문이 수치를 못 낸 칸 · — 미실행·보류
<!-- AUTO:END -->

## 메모


