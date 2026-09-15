---
type: model
code_dir: HNHN
nc_done: 6
nc_agree: 5
hp_done: 6
hp_agree: 6
max_abs_delta: 2.1
worst_cell: "노드 분류 Cora-CA −2.1"
status: complete
updated: 2026-09-15 15:36
tags: [hgnn/model]
---

<!-- AUTO:BEGIN -->
# HNHN

실행법 → [[HNHN 실행]] · 코드 `HNHN/` · 결과 `results/result_*_HNHN_*.txt` · <small>갱신 2026-09-15 15:36</small>

NC 5/6 일치 · HP 6/6 일치 · 최대 편차 노드 분류 Cora-CA −2.1

## Node classification — Table 3 · Accuracy

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 43.3 <span class="sd">±8.0</span> | 44.2 | <span class="d ok">−0.9</span> |  |
| [[Cora-CA]] | 51.0 <span class="sd">±6.6</span> | 53.1 | <span class="d warn">−2.1</span> |  |
| [[IMDB]] | 41.8 <span class="sd">±3.7</span> | 42.5 | <span class="d ok">−0.7</span> |  |
| [[House]] | 56.7 <span class="sd">±4.0</span> | 56.7 | <span class="d ok">+0.0</span> |  |
| [[Pubmed]] | 69.5 <span class="sd">±3.4</span> | 69.1 | <span class="d ok">+0.3</span> |  |
| [[AMiner]] | 31.8 <span class="sd">±2.0</span> | 32.1 | <span class="d ok">−0.3</span> |  |
| [[DBLP-A]] | — | 69.0 |  | blocked-data |
| [[MN-40]] | — | 89.2 |  | blocked-data |
| [[20News]] | — | 74.4 |  | blocked-data |

## Hyperedge prediction — Table 4 · AUROC

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 53.7 <span class="sd">±2.5</span> | 53.7 | <span class="d ok">+0.0</span> |  |
| [[Cora-CA]] | 51.8 <span class="sd">±1.8</span> | 51.6 | <span class="d ok">+0.2</span> |  |
| [[IMDB]] | 48.2 <span class="sd">±0.7</span> | 48.2 | <span class="d ok">+0.0</span> |  |
| [[House]] | 69.7 <span class="sd">±5.6</span> | 69.7 | <span class="d ok">+0.0</span> |  |
| [[Pubmed]] | 64.3 <span class="sd">±2.5</span> | 65.7 | <span class="d ok">−1.4</span> |  |
| [[AMiner]] | 48.1 <span class="sd">±1.3</span> | 48.1 | <span class="d ok">+0.0</span> |  |
| [[DBLP-P]] | — | 51.2 |  | pending |
| [[20News]] | — | 56.0 |  | blocked-data |

표기 · 값 <span class="sd">±표준편차</span> · Δ = 우리 − 논문 · <span class="d ok">+0.3</span> ±2 이내 · <span class="d warn">+3.0</span> 2–5 · <span class="d bad">+7.0</span> 5 초과 · <span class="lim">OOM</span> 논문이 수치를 못 낸 칸 · — 미실행·보류
<!-- AUTO:END -->

## 메모


