---
type: model
nc_agree: 6
nc_done: 6
hp_agree: 6
hp_done: 6
max_abs_delta: 1.0
worst_cell: "노드 분류 House +1.0"
status: complete
code_dir: Hypeboy
updated: 2026-09-15 15:11
tags: [hgnn/model]
cssclasses: [hg-model, row-alt]
---

<!-- AUTO:BEGIN -->
# HypeBoy

<small>코드 `Hypeboy/` · 결과 `results/result_*_Hypeboy_*.txt` · 갱신 2026-09-15 15:11</small>

| NC 일치 | HP 일치 | 최대 편차 |
|---|---|---|
| **6/6** | **6/6** | **+1.0** |
| <small>|Δ| 중앙값 0.30</small> | <small>|Δ| 중앙값 0.10</small> | <small>노드 분류 · House</small> |

## Node classification — Table 3 · Accuracy

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 57.6 <span class="sd">±10.5</span> | 57.7 | <span class="d ok">−0.1</span> |  |
| [[Cora-CA]] | 67.0 <span class="sd">±3.7</span> | 67.0 | <span class="d ok">+0.0</span> |  |
| [[IMDB]] | 48.0 <span class="sd">±5.0</span> | 48.3 | <span class="d ok">−0.3</span> |  |
| [[House]] | 68.7 <span class="sd">±6.0</span> | 67.7 | <span class="d ok">+1.0</span> |  |
| [[Pubmed]] | 73.7 <span class="sd">±4.4</span> | 73.7 | <span class="d ok">+0.0</span> |  |
| [[AMiner]] | 34.2 <span class="sd">±3.0</span> | 34.6 | <span class="d ok">−0.4</span> |  |
| [[DBLP-A]] | — | 81.2 |  | blocked-data |
| [[MN-40]] | — | 89.2 |  | blocked-data |
| [[20News]] | — | 75.7 |  | blocked-data |

```chart
type: bar
labels: [Citeseer, Cora-CA, IMDB, House, Pubmed, AMiner]
series:
  - title: 우리
    data: [57.6, 67.0, 48.0, 68.7, 73.7, 34.2]
  - title: 논문
    data: [57.7, 67.0, 48.3, 67.7, 73.7, 34.6]
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
| [[Citeseer]] | 86.4 <span class="sd">±2.1</span> | 86.4 | <span class="d ok">+0.0</span> |  |
| [[Cora-CA]] | 87.4 <span class="sd">±1.5</span> | 87.3 | <span class="d ok">+0.1</span> |  |
| [[IMDB]] | 59.3 <span class="sd">±1.8</span> | 59.4 | <span class="d ok">−0.1</span> |  |
| [[House]] | 87.0 <span class="sd">±3.0</span> | 87.2 | <span class="d ok">−0.2</span> |  |
| [[Pubmed]] | 92.1 <span class="sd">±0.5</span> | 92.1 | <span class="d ok">+0.0</span> |  |
| [[AMiner]] | 89.7 <span class="sd">±0.6</span> | 89.7 | <span class="d ok">+0.0</span> |  |
| [[DBLP-P]] | — | 95.2 |  | pending |
| [[20News]] | — | 97.2 |  | blocked-data |

```chart
type: bar
labels: [Citeseer, Cora-CA, IMDB, House, Pubmed, AMiner]
series:
  - title: 우리
    data: [86.4, 87.4, 59.3, 87.0, 92.1, 89.7]
  - title: 논문
    data: [86.4, 87.3, 59.4, 87.2, 92.1, 89.7]
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


