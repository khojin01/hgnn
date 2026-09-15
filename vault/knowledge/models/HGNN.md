---
type: model
code_dir: HGNN
nc_done: 6
nc_agree: 5
hp_done: 6
hp_agree: 5
max_abs_delta: 2.3
worst_cell: "하이퍼엣지 예측 IMDB +2.3"
status: complete
updated: 2026-09-15 15:36
tags: [hgnn/model]
---

<!-- AUTO:BEGIN -->
# HGNN

실행법 → [[HGNN 실행]] · 코드 `HGNN/` · 결과 `results/result_*_HGNN_*.txt` · <small>갱신 2026-09-15 15:36</small>

NC 5/6 일치 · HP 5/6 일치 · 최대 편차 하이퍼엣지 예측 IMDB +2.3

## Node classification — Table 3 · Accuracy

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 38.1 <span class="sd">±10.7</span> | 38.1 | <span class="d ok">−0.0</span> |  |
| [[Cora-CA]] | 46.6 <span class="sd">±7.9</span> | 44.3 | <span class="d warn">+2.3</span> |  |
| [[IMDB]] | 41.9 <span class="sd">±4.5</span> | 41.5 | <span class="d ok">+0.4</span> |  |
| [[House]] | 51.9 <span class="sd">±4.7</span> | 51.9 | <span class="d ok">+0.0</span> |  |
| [[Pubmed]] | 70.6 <span class="sd">±3.6</span> | 70.8 | <span class="d ok">−0.2</span> |  |
| [[AMiner]] | 30.5 <span class="sd">±1.6</span> | 29.7 | <span class="d ok">+0.8</span> |  |
| [[DBLP-A]] | — | 65.0 |  | blocked-data |
| [[MN-40]] | — | 89.5 |  | blocked-data |
| [[20News]] | — | 67.1 |  | blocked-data |

## Hyperedge prediction — Table 4 · AUROC

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 54.2 <span class="sd">±3.7</span> | 54.8 | <span class="d ok">−0.6</span> |  |
| [[Cora-CA]] | 64.5 <span class="sd">±5.9</span> | 65.0 | <span class="d ok">−0.5</span> |  |
| [[IMDB]] | 62.8 <span class="sd">±1.4</span> | 60.5 | <span class="d warn">+2.3</span> |  |
| [[House]] | 50.0 <span class="sd">±0.0</span> | 50.4 | <span class="d ok">−0.4</span> |  |
| [[Pubmed]] | 66.1 <span class="sd">±1.7</span> | 65.9 | <span class="d ok">+0.2</span> |  |
| [[AMiner]] | 69.1 <span class="sd">±1.6</span> | 69.6 | <span class="d ok">−0.5</span> |  |
| [[DBLP-P]] | — | 61.0 |  | pending |
| [[20News]] | — | 49.4 |  | blocked-data |

표기 · 값 <span class="sd">±표준편차</span> · Δ = 우리 − 논문 · <span class="d ok">+0.3</span> ±2 이내 · <span class="d warn">+3.0</span> 2–5 · <span class="d bad">+7.0</span> 5 초과 · <span class="lim">OOM</span> 논문이 수치를 못 낸 칸 · — 미실행·보류
<!-- AUTO:END -->

## 메모


