---
type: model
nc_agree: 5
nc_done: 6
hp_agree: 5
hp_done: 6
max_abs_delta: 2.3
worst_cell: "하이퍼엣지 예측 IMDB +2.3"
status: complete
code_dir: HGNN
updated: 2026-09-15 15:02
tags: [hgnn/model]
cssclasses: [hg-model, table-wide, row-alt]
---

<!-- AUTO:BEGIN -->
# HGNN

<small>코드 `HGNN/` · 결과 `results/result_*_HGNN_*.txt` · 갱신 2026-09-15 15:02</small>

| NC 일치 | HP 일치 | 최대 편차 |
|---|---|---|
| **5/6** | **5/6** | **+2.3** |
| <small>|Δ| 중앙값 0.38</small> | <small>|Δ| 중앙값 0.50</small> | <small>하이퍼엣지 예측 · IMDB</small> |

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

```chart
type: bar
labels: [Citeseer, Cora-CA, IMDB, House, Pubmed, AMiner]
series:
  - title: 우리
    data: [38.1, 46.6, 41.9, 51.9, 70.6, 30.5]
  - title: 논문
    data: [38.1, 44.3, 41.5, 51.9, 70.8, 29.7]
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
| [[Citeseer]] | 54.2 <span class="sd">±3.7</span> | 54.8 | <span class="d ok">−0.6</span> |  |
| [[Cora-CA]] | 64.5 <span class="sd">±5.9</span> | 65.0 | <span class="d ok">−0.5</span> |  |
| [[IMDB]] | 62.8 <span class="sd">±1.4</span> | 60.5 | <span class="d warn">+2.3</span> |  |
| [[House]] | 50.0 <span class="sd">±0.0</span> | 50.4 | <span class="d ok">−0.4</span> |  |
| [[Pubmed]] | 66.1 <span class="sd">±1.7</span> | 65.9 | <span class="d ok">+0.2</span> |  |
| [[AMiner]] | 69.1 <span class="sd">±1.6</span> | 69.6 | <span class="d ok">−0.5</span> |  |
| [[DBLP-P]] | — | 61.0 |  | pending |
| [[20News]] | — | 49.4 |  | blocked-data |

```chart
type: bar
labels: [Citeseer, Cora-CA, IMDB, House, Pubmed, AMiner]
series:
  - title: 우리
    data: [54.2, 64.5, 62.8, 50.0, 66.1, 69.1]
  - title: 논문
    data: [54.8, 65.0, 60.5, 50.4, 65.9, 69.6]
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


