---
type: model
code_dir: TriCL
nc_done: 6
nc_agree: 6
hp_done: 6
hp_agree: 1
cd_done: 6
cd_agree: 5
max_abs_delta: 5.4
worst_cell: "하이퍼엣지 예측 House −5.4"
status: complete
updated: 2026-09-15 19:37
tags: [hgnn/model]
---

<!-- AUTO:BEGIN -->
# TriCL

실행법 → [[TriCL 실행]] · 코드 `TriCL/` · 결과 `results/result_*_TriCL_*.txt` · <small>갱신 2026-09-15 19:37</small>

NC 6/6 일치 · HP 1/6 일치 · CD 5/6 일치 · 최대 편차 하이퍼엣지 예측 House −5.4

## Node classification — Table 3 · Accuracy

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 52.7 <span class="sd">±13.9</span> | 53.0 | <span class="d ok">−0.3</span> |  |
| [[Cora-CA]] | 61.9 <span class="sd">±5.8</span> | 63.4 | <span class="d ok">−1.5</span> |  |
| [[IMDB]] | 47.9 <span class="sd">±5.3</span> | 47.5 | <span class="d ok">+0.4</span> |  |
| [[House]] | 63.5 <span class="sd">±7.4</span> | 65.2 | <span class="d ok">−1.7</span> |  |
| [[Pubmed]] | 75.0 <span class="sd">±3.4</span> | 74.0 | <span class="d ok">+1.0</span> |  |
| [[AMiner]] | 33.6 <span class="sd">±2.5</span> | 34.6 | <span class="d ok">−1.0</span> |  |
| [[DBLP-A]] | — | 80.3 |  | blocked-data |
| [[MN-40]] | — | 93.0 |  | blocked-data |
| [[20News]] | — | 73.8 |  | blocked-data |

## Hyperedge prediction — Table 4 · AUROC

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 89.1 <span class="sd">±1.3</span> | 90.5 | <span class="d ok">−1.4</span> |  |
| [[Cora-CA]] | 85.0 <span class="sd">±2.0</span> | 87.8 | <span class="d warn">−2.8</span> |  |
| [[IMDB]] | 56.8 <span class="sd">±3.8</span> | 58.9 | <span class="d warn">−2.1</span> |  |
| [[House]] | 84.6 <span class="sd">±3.5</span> | 90.0 | <span class="d bad">−5.4</span> |  |
| [[Pubmed]] | 96.1 <span class="sd">±0.6</span> | 91.9 | <span class="d warn">+4.2</span> |  |
| [[AMiner]] | 86.0 <span class="sd">±0.9</span> | 90.4 | <span class="d warn">−4.4</span> |  |
| [[DBLP-P]] | — | 94.8 |  | pending |
| [[20News]] | — | 98.2 |  | blocked-data |

## Community detection — Table 5 · NMI

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 39.0 <span class="sd">±0.1</span> | 38.5 | <span class="d ok">+0.5</span> |  |
| [[Cora-CA]] | 45.2 <span class="sd">±0.9</span> | 40.9 | <span class="d warn">+4.3</span> |  |
| [[IMDB]] | 5.4 <span class="sd">±0.1</span> | 5.5 | <span class="d ok">−0.1</span> |  |
| [[House]] | 2.7 <span class="sd">±0.1</span> | 2.9 | <span class="d ok">−0.2</span> |  |
| [[Pubmed]] | 31.0 <span class="sd">±0.1</span> | 32.7 | <span class="d ok">−1.7</span> |  |
| [[AMiner]] | 40.7 <span class="sd">±0.3</span> | 40.9 | <span class="d ok">−0.2</span> |  |
| [[DBLP-P]] | — | 61.7 |  | pending |
| [[20News]] | — | 35.9 |  | pending |

표기 · 값 <span class="sd">±표준편차</span> · Δ = 우리 − 논문 · <span class="d ok">+0.3</span> ±2 이내 · <span class="d warn">+3.0</span> 2–5 · <span class="d bad">+7.0</span> 5 초과 · <span class="lim">OOM</span> 논문이 수치를 못 낸 칸 · — 미실행·보류
<!-- AUTO:END -->

## 메모


