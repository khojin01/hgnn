---
type: model
nc_agree: 5
nc_done: 6
hp_agree: 6
hp_done: 6
max_abs_delta: 2.1
worst_cell: "노드 분류 Citeseer −2.1"
status: complete
code_dir: UniGCN
updated: 2026-09-15 15:02
tags: [hgnn/model]
cssclasses: [hg-model, table-wide, row-alt]
---

<!-- AUTO:BEGIN -->
# UniGCN

<small>코드 `UniGCN/` · 결과 `results/result_*_UniGCN_*.txt` · 갱신 2026-09-15 15:02</small>

| NC 일치 | HP 일치 | 최대 편차 |
|---|---|---|
| **5/6** | **6/6** | **−2.1** |
| <small>|Δ| 중앙값 0.91</small> | <small>|Δ| 중앙값 0.80</small> | <small>노드 분류 · Citeseer</small> |

## Node classification — Table 3 · Accuracy

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 37.7 <span class="sd">±8.6</span> | 39.8 | <span class="d warn">−2.1</span> |  |
| [[Cora-CA]] | 47.2 <span class="sd">±5.2</span> | 46.3 | <span class="d ok">+0.9</span> |  |
| [[IMDB]] | 40.5 <span class="sd">±3.3</span> | 41.0 | <span class="d ok">−0.5</span> |  |
| [[House]] | 51.5 <span class="sd">±2.7</span> | 51.7 | <span class="d ok">−0.2</span> |  |
| [[Pubmed]] | 68.6 <span class="sd">±5.0</span> | 67.6 | <span class="d ok">+1.0</span> |  |
| [[AMiner]] | 29.6 <span class="sd">±1.5</span> | 29.8 | <span class="d ok">−0.2</span> |  |
| [[DBLP-A]] | — | 59.4 |  | blocked-data |
| [[MN-40]] | — | 75.7 |  | blocked-data |
| [[20News]] | — | 67.4 |  | blocked-data |

```chart
type: bar
labels: [Citeseer, Cora-CA, IMDB, House, Pubmed, AMiner]
series:
  - title: 우리
    data: [37.7, 47.2, 40.5, 51.5, 68.6, 29.6]
  - title: 논문
    data: [39.8, 46.3, 41.0, 51.7, 67.6, 29.8]
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
| [[Citeseer]] | 53.7 <span class="sd">±5.2</span> | 54.7 | <span class="d ok">−1.0</span> |  |
| [[Cora-CA]] | 61.1 <span class="sd">±5.7</span> | 60.0 | <span class="d ok">+1.1</span> |  |
| [[IMDB]] | 53.3 <span class="sd">±4.1</span> | 53.7 | <span class="d ok">−0.4</span> |  |
| [[House]] | 50.0 <span class="sd">±0.0</span> | 50.0 | <span class="d ok">+0.0</span> |  |
| [[Pubmed]] | 51.3 <span class="sd">±2.8</span> | 52.1 | <span class="d ok">−0.8</span> |  |
| [[AMiner]] | 68.5 <span class="sd">±1.9</span> | 69.0 | <span class="d ok">−0.5</span> |  |
| [[DBLP-P]] | — | 67.0 |  | pending |
| [[20News]] | — | 50.0 |  | blocked-data |

```chart
type: bar
labels: [Citeseer, Cora-CA, IMDB, House, Pubmed, AMiner]
series:
  - title: 우리
    data: [53.7, 61.1, 53.3, 50.0, 51.3, 68.5]
  - title: 논문
    data: [54.7, 60.0, 53.7, 50.0, 52.1, 69.0]
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


