---
type: model
nc_agree: 5
nc_done: 6
hp_agree: 6
hp_done: 6
max_abs_delta: 2.1
worst_cell: "노드 분류 Cora-CA −2.1"
status: complete
code_dir: HNHN
updated: 2026-09-15 15:11
tags: [hgnn/model]
cssclasses: [hg-model, row-alt]
---

<!-- AUTO:BEGIN -->
# HNHN

<small>코드 `HNHN/` · 결과 `results/result_*_HNHN_*.txt` · 갱신 2026-09-15 15:11</small>

| NC 일치 | HP 일치 | 최대 편차 |
|---|---|---|
| **5/6** | **6/6** | **−2.1** |
| <small>|Δ| 중앙값 0.66</small> | <small>|Δ| 중앙값 0.00</small> | <small>노드 분류 · Cora-CA</small> |

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

```chart
type: bar
labels: [Citeseer, Cora-CA, IMDB, House, Pubmed, AMiner]
series:
  - title: 우리
    data: [43.3, 51.0, 41.8, 56.7, 69.5, 31.8]
  - title: 논문
    data: [44.2, 53.1, 42.5, 56.7, 69.1, 32.1]
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
| [[Citeseer]] | 53.7 <span class="sd">±2.5</span> | 53.7 | <span class="d ok">+0.0</span> |  |
| [[Cora-CA]] | 51.8 <span class="sd">±1.8</span> | 51.6 | <span class="d ok">+0.2</span> |  |
| [[IMDB]] | 48.2 <span class="sd">±0.7</span> | 48.2 | <span class="d ok">+0.0</span> |  |
| [[House]] | 69.7 <span class="sd">±5.6</span> | 69.7 | <span class="d ok">+0.0</span> |  |
| [[Pubmed]] | 64.3 <span class="sd">±2.5</span> | 65.7 | <span class="d ok">−1.4</span> |  |
| [[AMiner]] | 48.1 <span class="sd">±1.3</span> | 48.1 | <span class="d ok">+0.0</span> |  |
| [[DBLP-P]] | — | 51.2 |  | pending |
| [[20News]] | — | 56.0 |  | blocked-data |

```chart
type: bar
labels: [Citeseer, Cora-CA, IMDB, House, Pubmed, AMiner]
series:
  - title: 우리
    data: [53.7, 51.8, 48.2, 69.7, 64.3, 48.1]
  - title: 논문
    data: [53.7, 51.6, 48.2, 69.7, 65.7, 48.1]
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


