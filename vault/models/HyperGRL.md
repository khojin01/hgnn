---
type: model
nc_agree: 2
nc_done: 2
hp_agree: 0
hp_done: 0
max_abs_delta: 0.2
worst_cell: "노드 분류 Cora-CA +0.2"
status: partial
code_dir: HyperGRL
updated: 2026-09-15 15:02
tags: [hgnn/model]
cssclasses: [hg-model, table-wide, row-alt]
---

<!-- AUTO:BEGIN -->
# HyperGRL

<small>코드 `HyperGRL/` · 결과 `results/result_*_HyperGRL_*.txt` · 갱신 2026-09-15 15:02</small>

| NC 일치 | HP 일치 | 최대 편차 |
|---|---|---|
| **2/2** | **0/0** | **+0.2** |
| <small>|Δ| 중앙값 0.20</small> | <small>정식 결과 없음</small> | <small>노드 분류 · Cora-CA</small> |

## Node classification — Table 3 · Accuracy

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | <span class="lim">OOM</span> | 35.1 |  | O.O.M (batch-1 retry) |
| [[Cora-CA]] | 42.0 <span class="sd">±6.7</span> | 41.8 | <span class="d ok">+0.2</span> |  |
| [[IMDB]] | <span class="lim">OOM</span> | 35.7 |  | O.O.M (batch-1 retry) |
| [[House]] | 50.6 <span class="sd">±1.8</span> | 50.4 | <span class="d ok">+0.2</span> |  |
| [[Pubmed]] | <span class="lim">OOM</span> | 50.2 |  | O.O.M (batch-1 retry) |
| [[AMiner]] | <span class="lim">OOM</span> | 28.0 |  | O.O.M (batch-1 retry) |
| [[DBLP-A]] | — | 41.1 |  | blocked-data |
| [[MN-40]] | — | 89.4 |  | blocked-data |
| [[20News]] | — | — |  | blocked-data |

```chart
type: bar
labels: [Cora-CA, House]
series:
  - title: 우리
    data: [42.0, 50.6]
  - title: 논문
    data: [41.8, 50.4]
tension: 0.2
width: 100%
labelColors: false
fill: false
beginAtZero: false
legend: true
stacked: false
height: 220px
```

## Hyperedge prediction — Table 4 · AUROC

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | — | 83.2 |  | unavailable: EP implementation missing |
| [[Cora-CA]] | — | 80.0 |  | unavailable: EP implementation missing |
| [[IMDB]] | — | 54.7 |  | unavailable: EP implementation missing |
| [[House]] | — | 88.2 |  | unavailable: EP implementation missing |
| [[Pubmed]] | — | 78.3 |  | unavailable: EP implementation missing |
| [[AMiner]] | — | 81.5 |  | unavailable: EP implementation missing |
| [[DBLP-P]] | — | 88.2 |  | unavailable: EP implementation missing |
| [[20News]] | <span class="lim">OOT</span> | — |  | O.O.T skip |

## Community detection — Table 5 · NMI

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Cora-CA]] | — | 34.5 |  | pending |
| [[DBLP-P]] | — | 57.4 |  | pending |
| [[20News]] | <span class="lim">OOT</span> | — |  | O.O.T skip |

표기 · 값 <span class="sd">±표준편차</span> · Δ = 우리 − 논문 · <span class="d ok">+0.3</span> ±2 이내 · <span class="d warn">+3.0</span> 2–5 · <span class="d bad">+7.0</span> 5 초과 · <span class="lim">OOM</span> 논문이 수치를 못 낸 칸 · — 미실행·보류

관련: [[논문 대조]] · [[모델 비교]] · [[Home]]
<!-- AUTO:END -->

## 메모


