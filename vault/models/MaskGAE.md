---
type: model
nc_agree: 5
nc_done: 6
hp_agree: 6
hp_done: 6
max_abs_delta: 3.3
worst_cell: "노드 분류 Cora-CA −3.3"
status: complete
code_dir: MaskGAE
updated: 2026-09-15 15:11
tags: [hgnn/model]
cssclasses: [hg-model, row-alt]
---

<!-- AUTO:BEGIN -->
# MaskGAE

<small>코드 `MaskGAE/` · 결과 `results/result_*_MaskGAE_*.txt` · 갱신 2026-09-15 15:11</small>

| NC 일치 | HP 일치 | 최대 편차 |
|---|---|---|
| **5/6** | **6/6** | **−3.3** |
| <small>|Δ| 중앙값 0.80</small> | <small>|Δ| 중앙값 0.10</small> | <small>노드 분류 · Cora-CA</small> |

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

```chart
type: bar
labels: [Citeseer, Cora-CA, IMDB, House, Pubmed, AMiner]
series:
  - title: 우리
    data: [52.7, 56.5, 44.7, 52.2, 74.6, 32.5]
  - title: 논문
    data: [53.2, 59.8, 45.0, 53.0, 75.4, 33.8]
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
| [[Citeseer]] | 86.7 <span class="sd">±1.7</span> | 86.7 | <span class="d ok">+0.0</span> |  |
| [[Cora-CA]] | 76.1 <span class="sd">±2.2</span> | 76.5 | <span class="d ok">−0.4</span> |  |
| [[IMDB]] | 54.5 <span class="sd">±1.3</span> | 54.4 | <span class="d ok">+0.1</span> |  |
| [[House]] | 88.2 <span class="sd">±3.6</span> | 88.0 | <span class="d ok">+0.2</span> |  |
| [[Pubmed]] | 95.5 <span class="sd">±0.3</span> | 95.5 | <span class="d ok">+0.0</span> |  |
| [[AMiner]] | 87.6 <span class="sd">±0.9</span> | 87.6 | <span class="d ok">+0.0</span> |  |
| [[DBLP-P]] | — | 94.8 |  | pending |
| [[20News]] | <span class="lim">OOT</span> | — |  | O.O.T skip |

```chart
type: bar
labels: [Citeseer, Cora-CA, IMDB, House, Pubmed, AMiner]
series:
  - title: 우리
    data: [86.7, 76.1, 54.5, 88.2, 95.5, 87.6]
  - title: 논문
    data: [86.7, 76.5, 54.4, 88.0, 95.5, 87.6]
tension: 0.2
width: 100%
labelColors: false
fill: false
beginAtZero: false
legend: true
stacked: false
height: 220px
```

## Community detection — Table 5 · NMI

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Cora-CA]] | — | 38.0 |  | pending |
| [[DBLP-P]] | — | 61.6 |  | pending |
| [[20News]] | <span class="lim">OOT</span> | — |  | O.O.T skip |

표기 · 값 <span class="sd">±표준편차</span> · Δ = 우리 − 논문 · <span class="d ok">+0.3</span> ±2 이내 · <span class="d warn">+3.0</span> 2–5 · <span class="d bad">+7.0</span> 5 초과 · <span class="lim">OOM</span> 논문이 수치를 못 낸 칸 · — 미실행·보류

관련: [[논문 대조]] · [[모델 비교]] · [[Home]]
<!-- AUTO:END -->

## 메모


