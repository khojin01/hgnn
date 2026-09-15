---
type: model
code_dir: VilLain
nc_done: 6
nc_agree: 5
hp_done: 6
hp_agree: 6
cd_done: 6
cd_agree: 5
max_abs_delta: 5.1
worst_cell: "노드 분류 Citeseer −5.1"
status: complete
updated: 2026-09-15 19:20
tags: [hgnn/model]
---

<!-- AUTO:BEGIN -->
# VilLain

실행법 → [[VilLain 실행]] · 코드 `VilLain/` · 결과 `results/result_*_VilLain_*.txt` · <small>갱신 2026-09-15 19:20</small>

NC 5/6 일치 · HP 6/6 일치 · CD 5/6 일치 · 최대 편차 노드 분류 Citeseer −5.1

## Node classification — Table 3 · Accuracy

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 28.5 <span class="sd">±8.2</span> | 33.6 | <span class="d bad">−5.1</span> |  |
| [[Cora-CA]] | 31.4 <span class="sd">±4.1</span> | 31.4 | <span class="d ok">+0.0</span> |  |
| [[IMDB]] | 39.2 <span class="sd">±3.9</span> | 39.7 | <span class="d ok">−0.5</span> |  |
| [[House]] | 49.3 <span class="sd">±1.5</span> | 50.6 | <span class="d ok">−1.3</span> |  |
| [[Pubmed]] | 73.7 <span class="sd">±3.3</span> | 73.7 | <span class="d ok">+0.0</span> |  |
| [[AMiner]] | 19.9 <span class="sd">±1.2</span> | 19.9 | <span class="d ok">+0.0</span> |  |
| [[DBLP-A]] | — | 40.4 |  | blocked-data |
| [[MN-40]] | — | 69.7 |  | blocked-data |
| [[20News]] | — | 74.3 |  | blocked-data |

## Hyperedge prediction — Table 4 · AUROC

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 57.2 <span class="sd">±2.4</span> | 58.3 | <span class="d ok">−1.1</span> |  |
| [[Cora-CA]] | 64.7 <span class="sd">±2.5</span> | 64.4 | <span class="d ok">+0.3</span> |  |
| [[IMDB]] | 43.6 <span class="sd">±2.6</span> | 43.9 | <span class="d ok">−0.3</span> |  |
| [[House]] | 77.5 <span class="sd">±5.6</span> | 77.2 | <span class="d ok">+0.3</span> |  |
| [[Pubmed]] | 84.3 <span class="sd">±0.8</span> | 83.7 | <span class="d ok">+0.6</span> |  |
| [[AMiner]] | 61.9 <span class="sd">±0.7</span> | 62.7 | <span class="d ok">−0.8</span> |  |
| [[DBLP-P]] | — | 56.3 |  | pending |
| [[20News]] | — | 59.2 |  | blocked-data |

## Community detection — Table 5 · NMI

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 9.1 <span class="sd">±4.5</span> | 11.3 | <span class="d warn">−2.2</span> |  |
| [[Cora-CA]] | 9.7 <span class="sd">±2.2</span> | 9.7 | <span class="d ok">+0.0</span> |  |
| [[IMDB]] | 0.0 <span class="sd">±0.0</span> | 0.1 | <span class="d ok">−0.1</span> |  |
| [[House]] | 0.1 <span class="sd">±0.0</span> | 0.1 | <span class="d ok">+0.0</span> |  |
| [[Pubmed]] | 32.9 <span class="sd">±0.0</span> | 32.9 | <span class="d ok">+0.0</span> |  |
| [[AMiner]] | 17.7 <span class="sd">±0.7</span> | 16.2 | <span class="d ok">+1.5</span> |  |
| [[DBLP-P]] | — | 40.1 |  | pending |
| [[20News]] | — | 38.8 |  | pending |

표기 · 값 <span class="sd">±표준편차</span> · Δ = 우리 − 논문 · <span class="d ok">+0.3</span> ±2 이내 · <span class="d warn">+3.0</span> 2–5 · <span class="d bad">+7.0</span> 5 초과 · <span class="lim">OOM</span> 논문이 수치를 못 낸 칸 · — 미실행·보류
<!-- AUTO:END -->

## 메모


