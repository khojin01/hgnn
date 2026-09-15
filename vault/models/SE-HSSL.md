---
type: model
nc_agree: 4
nc_done: 6
hp_agree: 6
hp_done: 6
max_abs_delta: 12.7
worst_cell: "노드 분류 House +12.7"
status: complete
code_dir: SEHSSL
updated: 2026-09-15 15:11
tags: [hgnn/model]
cssclasses: [hg-model, row-alt]
---

<!-- AUTO:BEGIN -->
# SE-HSSL

<small>코드 `SEHSSL/` · 결과 `results/result_*_SEHSSL_*.txt` · 갱신 2026-09-15 15:11</small>

| NC 일치 | HP 일치 | 최대 편차 |
|---|---|---|
| **4/6** | **6/6** | **+12.7** |
| <small>|Δ| 중앙값 0.10</small> | <small>|Δ| 중앙값 0.50</small> | <small>노드 분류 · House</small> |

## Node classification — Table 3 · Accuracy

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 57.0 <span class="sd">±8.3</span> | 57.0 | <span class="d ok">+0.0</span> |  |
| [[Cora-CA]] | 64.0 <span class="sd">±4.9</span> | 63.9 | <span class="d ok">+0.1</span> |  |
| [[IMDB]] | 48.9 <span class="sd">±4.0</span> | 48.9 | <span class="d ok">+0.0</span> |  |
| [[House]] | 60.7 <span class="sd">±7.0</span> | 48.0 | <span class="d bad">+12.7</span> |  |
| [[Pubmed]] | 63.4 <span class="sd">±9.1</span> | 69.8 | <span class="d bad">−6.4</span> |  |
| [[AMiner]] | 34.7 <span class="sd">±4.2</span> | 34.8 | <span class="d ok">−0.1</span> |  |
| [[DBLP-A]] | — | 77.1 |  | blocked-data |
| [[MN-40]] | — | 85.8 |  | blocked-data |
| [[20News]] | — | 75.8 |  | blocked-data |

```chart
type: bar
labels: [Citeseer, Cora-CA, IMDB, House, Pubmed, AMiner]
series:
  - title: 우리
    data: [57.0, 64.0, 48.9, 60.7, 63.4, 34.7]
  - title: 논문
    data: [57.0, 63.9, 48.9, 48.0, 69.8, 34.8]
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
| [[Citeseer]] | 90.6 <span class="sd">±1.1</span> | 90.5 | <span class="d ok">+0.1</span> |  |
| [[Cora-CA]] | 85.7 <span class="sd">±2.3</span> | 85.6 | <span class="d ok">+0.1</span> |  |
| [[IMDB]] | 54.1 <span class="sd">±2.0</span> | 55.6 | <span class="d ok">−1.5</span> |  |
| [[House]] | 79.9 <span class="sd">±3.1</span> | 80.4 | <span class="d ok">−0.5</span> |  |
| [[Pubmed]] | 95.0 <span class="sd">±0.4</span> | 94.5 | <span class="d ok">+0.5</span> |  |
| [[AMiner]] | 87.4 <span class="sd">±0.6</span> | 87.5 | <span class="d ok">−0.1</span> |  |
| [[DBLP-P]] | — | 94.0 |  | pending |
| [[20News]] | — | 95.2 |  | blocked-data |

```chart
type: bar
labels: [Citeseer, Cora-CA, IMDB, House, Pubmed, AMiner]
series:
  - title: 우리
    data: [90.6, 85.7, 54.1, 79.9, 95.0, 87.4]
  - title: 논문
    data: [90.5, 85.6, 55.6, 80.4, 94.5, 87.5]
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


