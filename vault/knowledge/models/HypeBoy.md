---
type: model
code_dir: Hypeboy
nc_done: 6
nc_agree: 6
hp_done: 6
hp_agree: 6
cd_done: 3
cd_agree: 1
max_abs_delta: 2.8
worst_cell: "커뮤니티 탐지 Cora-CA +2.8"
status: complete
updated: 2026-09-15 22:18
tags: [hgnn/model]
---

<!-- AUTO:BEGIN -->
# HypeBoy

실행법 → [[HypeBoy 실행]] · 코드 `Hypeboy/` · 결과 `results/result_*_Hypeboy_*.txt` · <small>갱신 2026-09-15 22:18</small>

NC 6/6 일치 · HP 6/6 일치 · CD 1/3 일치 · 최대 편차 커뮤니티 탐지 Cora-CA +2.8

## Node classification — Table 3 · Accuracy

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 57.6 <span class="sd">±10.5</span> | 57.7 | <span class="d ok">−0.1</span> |  |
| [[Cora-CA]] | 67.0 <span class="sd">±3.7</span> | 67.0 | <span class="d ok">+0.0</span> |  |
| [[IMDB]] | 48.0 <span class="sd">±5.0</span> | 48.3 | <span class="d ok">−0.3</span> |  |
| [[House]] | 68.7 <span class="sd">±6.0</span> | 67.7 | <span class="d ok">+1.0</span> |  |
| [[Pubmed]] | 73.7 <span class="sd">±4.4</span> | 73.7 | <span class="d ok">+0.0</span> |  |
| [[AMiner]] | 34.2 <span class="sd">±3.0</span> | 34.6 | <span class="d ok">−0.4</span> |  |
| [[DBLP-A]] | — | 81.2 |  | blocked-data |
| [[MN-40]] | — | 89.2 |  | blocked-data |
| [[20News]] | — | 75.7 |  | blocked-data |

## Hyperedge prediction — Table 4 · AUROC

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 86.4 <span class="sd">±2.1</span> | 86.4 | <span class="d ok">+0.0</span> |  |
| [[Cora-CA]] | 87.4 <span class="sd">±1.5</span> | 87.3 | <span class="d ok">+0.1</span> |  |
| [[IMDB]] | 59.3 <span class="sd">±1.8</span> | 59.4 | <span class="d ok">−0.1</span> |  |
| [[House]] | 87.0 <span class="sd">±3.0</span> | 87.2 | <span class="d ok">−0.2</span> |  |
| [[Pubmed]] | 92.1 <span class="sd">±0.5</span> | 92.1 | <span class="d ok">+0.0</span> |  |
| [[AMiner]] | 89.7 <span class="sd">±0.6</span> | 89.7 | <span class="d ok">+0.0</span> |  |
| [[DBLP-P]] | — | 95.2 |  | pending |
| [[20News]] | — | 97.2 |  | blocked-data |

## Community detection — Table 5 · NMI

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 38.7 <span class="sd">±0.1</span> | 40.9 | <span class="d warn">−2.2</span> |  |
| [[Cora-CA]] | 44.7 <span class="sd">±0.9</span> | 41.9 | <span class="d warn">+2.8</span> |  |
| [[IMDB]] | 8.9 <span class="sd">±0.0</span> | 8.6 | <span class="d ok">+0.3</span> |  |
| [[House]] | — | 0.0 |  | pending |
| [[Pubmed]] | — | 30.4 |  | pending |
| [[AMiner]] | — | 42.2 |  | pending |
| [[DBLP-P]] | — | 60.8 |  | pending |
| [[20News]] | — | 38.0 |  | pending |

표기 · 값 <span class="sd">±표준편차</span> · Δ = 우리 − 논문 · <span class="d ok">+0.3</span> ±2 이내 · <span class="d warn">+3.0</span> 2–5 · <span class="d bad">+7.0</span> 5 초과 · <span class="lim">OOM</span> 논문이 수치를 못 낸 칸 · — 미실행·보류
<!-- AUTO:END -->

## 메모


