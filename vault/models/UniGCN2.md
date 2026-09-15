---
type: model
nc_agree: 5
nc_done: 6
hp_agree: 6
hp_done: 6
max_abs_delta: 2.2
worst_cell: "노드 분류 Cora-CA −2.2"
status: complete
code_dir: UniGCN2
updated: 2026-09-15 14:20
tags: [hgnn/model]
cssclasses: [hg-model]
---

<!-- AUTO:BEGIN -->
# UniGCN2

<span class="lgn">코드 `UniGCN2/` · 결과 `results/result_*_UniGCN2_*.txt` · 갱신 2026-09-15 14:20</span>

<div class="hg-cards"><div class="hg-card"><span class="k">NC 일치</span><span class="big">5/6</span><span class="note">|Δ| 중앙값 0.90</span></div><div class="hg-card"><span class="k">HP 일치</span><span class="big">6/6</span><span class="note">|Δ| 중앙값 0.30</span></div><div class="hg-card"><span class="k">최대 편차</span><span class="big">−2.2</span><span class="note">노드 분류 · Cora-CA</span></div></div>

## Node classification <span class="m">Table 3 · Accuracy</span>

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | <span class="v">41.5</span><span class="sd">±9.2</span> | 39.6 | <span class="d ok">+1.9</span> | |
| [[Cora-CA]] | <span class="v">53.1</span><span class="sd">±7.3</span> | 55.3 | <span class="d warn">−2.2</span> | |
| [[IMDB]] | <span class="v">42.5</span><span class="sd">±3.2</span> | 41.6 | <span class="d ok">+0.9</span> | |
| [[House]] | <span class="v">58.7</span><span class="sd">±10.1</span> | 58.8 | <span class="d ok">−0.1</span> | |
| [[Pubmed]] | <span class="v">72.5</span><span class="sd">±4.6</span> | 72.6 | <span class="d ok">−0.1</span> | |
| [[AMiner]] | <span class="v">32.2</span><span class="sd">±1.8</span> | 32.3 | <span class="d ok">−0.1</span> | |
| [[DBLP-A]] | <span class="na">—</span> | 58.7 | | blocked-data |
| [[MN-40]] | <span class="na">—</span> | 79.7 | | blocked-data |
| [[20News]] | <span class="na">—</span> | 76.8 | | blocked-data |

```chart
type: bar
labels: [Citeseer, Cora-CA, IMDB, House, Pubmed, AMiner]
series:
  - title: 우리
    data: [41.5, 53.1, 42.5, 58.7, 72.5, 32.2]
  - title: 논문
    data: [39.6, 55.3, 41.6, 58.8, 72.6, 32.3]
tension: 0.2
width: 100%
labelColors: false
fill: false
beginAtZero: false
legend: true
stacked: false
height: 220px
```


## Hyperedge prediction <span class="m">Table 4 · AUROC</span>

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | <span class="v">60.3</span><span class="sd">±2.1</span> | 60.2 | <span class="d ok">+0.1</span> | |
| [[Cora-CA]] | <span class="v">52.2</span><span class="sd">±4.5</span> | 51.9 | <span class="d ok">+0.3</span> | |
| [[IMDB]] | <span class="v">57.1</span><span class="sd">±6.0</span> | 57.5 | <span class="d ok">−0.4</span> | |
| [[House]] | <span class="v">50.0</span><span class="sd">±0.0</span> | 50.0 | <span class="d ok">+0.0</span> | |
| [[Pubmed]] | <span class="v">69.1</span><span class="sd">±1.0</span> | 69.1 | <span class="d ok">+0.0</span> | |
| [[AMiner]] | <span class="v">46.2</span><span class="sd">±4.5</span> | 45.9 | <span class="d ok">+0.3</span> | |
| [[DBLP-P]] | <span class="na">—</span> | 60.2 | | pending |
| [[20News]] | <span class="na">—</span> | 50.0 | | blocked-data |

```chart
type: bar
labels: [Citeseer, Cora-CA, IMDB, House, Pubmed, AMiner]
series:
  - title: 우리
    data: [60.3, 52.2, 57.1, 50.0, 69.1, 46.2]
  - title: 논문
    data: [60.2, 51.9, 57.5, 50.0, 69.1, 45.9]
tension: 0.2
width: 100%
labelColors: false
fill: false
beginAtZero: false
legend: true
stacked: false
height: 220px
```


<div class="hg-legend"><span>우리값 <span class="sd">±표준편차</span></span><span class="d ok">±2 이내</span><span class="d warn">2–5</span><span class="d bad">5 초과</span><span class="lim">OOM</span><span class="lgn">논문이 수치를 못 낸 칸</span><span class="na">—</span><span class="lgn">미실행·보류</span></div>

관련: [[논문 대조]] · [[모델 비교]] · [[Home]]
<!-- AUTO:END -->

## 메모


