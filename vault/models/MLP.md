---
type: model
nc_agree: 6
nc_done: 6
hp_agree: 6
hp_done: 6
max_abs_delta: 1.2
worst_cell: "노드 분류 Cora-CA +1.2"
status: complete
code_dir: MLP
updated: 2026-09-15 15:02
tags: [hgnn/model]
cssclasses: [hg-model, table-wide, row-alt]
---

<!-- AUTO:BEGIN -->
# MLP

<small>코드 `MLP/` · 결과 `results/result_*_MLP_*.txt` · 갱신 2026-09-15 15:02</small>

| NC 일치 | HP 일치 | 최대 편차 |
|---|---|---|
| **6/6** | **6/6** | **+1.2** |
| <small>|Δ| 중앙값 0.31</small> | <small>|Δ| 중앙값 0.00</small> | <small>노드 분류 · Cora-CA</small> |

## Node classification — Table 3 · Accuracy

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 32.4 <span class="sd">±8.1</span> | 32.4 | <span class="d ok">+0.0</span> |  |
| [[Cora-CA]] | 37.2 <span class="sd">±4.3</span> | 36.0 | <span class="d ok">+1.2</span> |  |
| [[IMDB]] | 38.2 <span class="sd">±2.7</span> | 37.6 | <span class="d ok">+0.6</span> |  |
| [[House]] | 73.1 <span class="sd">±3.2</span> | 73.1 | <span class="d ok">+0.0</span> |  |
| [[Pubmed]] | 62.7 <span class="sd">±3.3</span> | 62.8 | <span class="d ok">−0.1</span> |  |
| [[AMiner]] | 22.4 <span class="sd">±1.4</span> | 22.7 | <span class="d ok">−0.3</span> |  |
| [[DBLP-A]] | — | 56.6 |  | blocked-data |
| [[MN-40]] | — | 88.5 |  | blocked-data |
| [[20News]] | — | 73.3 |  | blocked-data |

```chart
type: bar
labels: [Citeseer, Cora-CA, IMDB, House, Pubmed, AMiner]
series:
  - title: 우리
    data: [32.4, 37.2, 38.2, 73.1, 62.7, 22.4]
  - title: 논문
    data: [32.4, 36.0, 37.6, 73.1, 62.8, 22.7]
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
| [[Citeseer]] | 65.6 <span class="sd">±2.0</span> | 65.6 | <span class="d ok">+0.0</span> |  |
| [[Cora-CA]] | 58.6 <span class="sd">±2.9</span> | 58.6 | <span class="d ok">+0.0</span> |  |
| [[IMDB]] | 41.7 <span class="sd">±2.5</span> | 42.0 | <span class="d ok">−0.3</span> |  |
| [[House]] | 54.8 <span class="sd">±5.4</span> | 54.8 | <span class="d ok">+0.0</span> |  |
| [[Pubmed]] | 88.3 <span class="sd">±0.6</span> | 88.3 | <span class="d ok">+0.0</span> |  |
| [[AMiner]] | 82.3 <span class="sd">±0.9</span> | 82.3 | <span class="d ok">+0.0</span> |  |
| [[DBLP-P]] | — | 90.2 |  | pending |
| [[20News]] | — | 95.1 |  | blocked-data |

```chart
type: bar
labels: [Citeseer, Cora-CA, IMDB, House, Pubmed, AMiner]
series:
  - title: 우리
    data: [65.6, 58.6, 41.7, 54.8, 88.3, 82.3]
  - title: 논문
    data: [65.6, 58.6, 42.0, 54.8, 88.3, 82.3]
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


