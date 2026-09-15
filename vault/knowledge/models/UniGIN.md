---
type: model
code_dir: UniGIN
nc_done: 6
nc_agree: 6
hp_done: 6
hp_agree: 6
max_abs_delta: 1.6
worst_cell: "노드 분류 Cora-CA −1.6"
status: complete
updated: 2026-09-15 15:36
tags: [hgnn/model]
---

<!-- AUTO:BEGIN -->
# UniGIN

실행법 → [[UniGIN 실행]] · 코드 `UniGIN/` · 결과 `results/result_*_UniGIN_*.txt` · <small>갱신 2026-09-15 15:36</small>

NC 6/6 일치 · HP 6/6 일치 · 최대 편차 노드 분류 Cora-CA −1.6

## Node classification — Table 3 · Accuracy

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 40.3 <span class="sd">±9.4</span> | 41.4 | <span class="d ok">−1.1</span> |  |
| [[Cora-CA]] | 47.6 <span class="sd">±6.5</span> | 49.2 | <span class="d ok">−1.6</span> |  |
| [[IMDB]] | 41.1 <span class="sd">±3.9</span> | 41.7 | <span class="d ok">−0.6</span> |  |
| [[House]] | 51.0 <span class="sd">±2.3</span> | 50.8 | <span class="d ok">+0.2</span> |  |
| [[Pubmed]] | 69.7 <span class="sd">±4.3</span> | 70.4 | <span class="d ok">−0.7</span> |  |
| [[AMiner]] | 30.7 <span class="sd">±1.2</span> | 30.8 | <span class="d ok">−0.1</span> |  |
| [[DBLP-A]] | — | 63.1 |  | blocked-data |
| [[MN-40]] | — | 87.1 |  | blocked-data |
| [[20News]] | — | 68.1 |  | blocked-data |

## Hyperedge prediction — Table 4 · AUROC

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 53.3 <span class="sd">±3.4</span> | 52.9 | <span class="d ok">+0.4</span> |  |
| [[Cora-CA]] | 59.7 <span class="sd">±7.6</span> | 58.7 | <span class="d ok">+1.0</span> |  |
| [[IMDB]] | 53.9 <span class="sd">±4.5</span> | 54.6 | <span class="d ok">−0.7</span> |  |
| [[House]] | 50.0 <span class="sd">±0.0</span> | 50.0 | <span class="d ok">+0.0</span> |  |
| [[Pubmed]] | 51.7 <span class="sd">±3.6</span> | 51.5 | <span class="d ok">+0.2</span> |  |
| [[AMiner]] | 68.9 <span class="sd">±1.2</span> | 69.1 | <span class="d ok">−0.2</span> |  |
| [[DBLP-P]] | — | 69.2 |  | pending |
| [[20News]] | — | 50.0 |  | blocked-data |

표기 · 값 <span class="sd">±표준편차</span> · Δ = 우리 − 논문 · <span class="d ok">+0.3</span> ±2 이내 · <span class="d warn">+3.0</span> 2–5 · <span class="d bad">+7.0</span> 5 초과 · <span class="lim">OOM</span> 논문이 수치를 못 낸 칸 · — 미실행·보류
<!-- AUTO:END -->

## 메모


