---
type: model
nc_agree: 6
nc_done: 6
hp_agree: 6
hp_done: 6
max_abs_delta: 0.9
worst_cell: "노드 분류 IMDB −0.9"
status: complete
code_dir: GraphMAE2
updated: 2026-09-15 15:02
tags: [hgnn/model]
cssclasses: [hg-model, table-wide, row-alt]
---

<!-- AUTO:BEGIN -->
# GraphMAE2

<small>코드 `GraphMAE2/` · 결과 `results/result_*_GraphMAE2_*.txt` · 갱신 2026-09-15 15:02</small>

| NC 일치 | HP 일치 | 최대 편차 |
|---|---|---|
| **6/6** | **6/6** | **−0.9** |
| <small>|Δ| 중앙값 0.40</small> | <small>|Δ| 중앙값 0.20</small> | <small>노드 분류 · IMDB</small> |

## Node classification — Table 3 · Accuracy

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 51.7 <span class="sd">±12.9</span> | 51.7 | <span class="d ok">+0.0</span> |  |
| [[Cora-CA]] | 64.0 <span class="sd">±5.8</span> | 64.3 | <span class="d ok">−0.3</span> |  |
| [[IMDB]] | 44.7 <span class="sd">±4.2</span> | 45.6 | <span class="d ok">−0.9</span> |  |
| [[House]] | 52.0 <span class="sd">±3.2</span> | 52.4 | <span class="d ok">−0.4</span> |  |
| [[Pubmed]] | 72.2 <span class="sd">±4.7</span> | 72.6 | <span class="d ok">−0.4</span> |  |
| [[AMiner]] | 34.8 <span class="sd">±2.4</span> | 34.7 | <span class="d ok">+0.1</span> |  |
| [[DBLP-A]] | — | 77.2 |  | blocked-data |
| [[MN-40]] | — | 90.6 |  | blocked-data |
| [[20News]] | — | 71.8 |  | blocked-data |

```chart
type: bar
labels: [Citeseer, Cora-CA, IMDB, House, Pubmed, AMiner]
series:
  - title: 우리
    data: [51.7, 64.0, 44.7, 52.0, 72.2, 34.8]
  - title: 논문
    data: [51.7, 64.3, 45.6, 52.4, 72.6, 34.7]
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
| [[Citeseer]] | 78.1 <span class="sd">±2.4</span> | 78.2 | <span class="d ok">−0.1</span> |  |
| [[Cora-CA]] | 74.7 <span class="sd">±2.9</span> | 74.7 | <span class="d ok">+0.0</span> |  |
| [[IMDB]] | 47.4 <span class="sd">±1.0</span> | 47.2 | <span class="d ok">+0.2</span> |  |
| [[House]] | 71.8 <span class="sd">±5.6</span> | 71.6 | <span class="d ok">+0.2</span> |  |
| [[Pubmed]] | 93.9 <span class="sd">±1.8</span> | 93.6 | <span class="d ok">+0.3</span> |  |
| [[AMiner]] | 78.1 <span class="sd">±0.9</span> | 78.1 | <span class="d ok">+0.0</span> |  |
| [[DBLP-P]] | — | 92.7 |  | pending |
| [[20News]] | — | 87.0 |  | blocked-data |

```chart
type: bar
labels: [Citeseer, Cora-CA, IMDB, House, Pubmed, AMiner]
series:
  - title: 우리
    data: [78.1, 74.7, 47.4, 71.8, 93.9, 78.1]
  - title: 논문
    data: [78.2, 74.7, 47.2, 71.6, 93.6, 78.1]
tension: 0.2
width: 100%
labelColors: false
fill: false
beginAtZero: false
legend: true
stacked: false
height: 220px
```

표기 · 값 <span class="sd">±표준편차</span> · Δ = 우리 − 논문 · <span class="d ok">+0.3</span> ±2 이내 · <span class="d warn">+3.0</span> 2–5 · <span class="d bad">+7.0</span> 5 초과 · <span class="lim">OOM</span> 논문이 수치를 못 낸 칸 · — 미실행·보류

관련: [[논문 대조]] · [[모델 비교]] · [[Home]]
<!-- AUTO:END -->

## 메모


