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
updated: 2026-09-15 14:20
tags: [hgnn/model]
cssclasses: [hg-model]
---

<!-- AUTO:BEGIN -->
# UniGCN

<span class="lgn">코드 `UniGCN/` · 결과 `results/result_*_UniGCN_*.txt` · 갱신 2026-09-15 14:20</span>

<div class="hg-cards"><div class="hg-card"><span class="k">NC 일치</span><span class="big">5/6</span><span class="note">|Δ| 중앙값 0.91</span></div><div class="hg-card"><span class="k">HP 일치</span><span class="big">6/6</span><span class="note">|Δ| 중앙값 0.80</span></div><div class="hg-card"><span class="k">최대 편차</span><span class="big">−2.1</span><span class="note">노드 분류 · Citeseer</span></div></div>

## Node classification <span class="m">Table 3 · Accuracy</span>

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | <span class="v">37.7</span><span class="sd">±8.6</span> | 39.8 | <span class="d warn">−2.1</span> | |
| [[Cora-CA]] | <span class="v">47.2</span><span class="sd">±5.2</span> | 46.3 | <span class="d ok">+0.9</span> | |
| [[IMDB]] | <span class="v">40.5</span><span class="sd">±3.3</span> | 41.0 | <span class="d ok">−0.5</span> | |
| [[House]] | <span class="v">51.5</span><span class="sd">±2.7</span> | 51.7 | <span class="d ok">−0.2</span> | |
| [[Pubmed]] | <span class="v">68.6</span><span class="sd">±5.0</span> | 67.6 | <span class="d ok">+1.0</span> | |
| [[AMiner]] | <span class="v">29.6</span><span class="sd">±1.5</span> | 29.8 | <span class="d ok">−0.2</span> | |
| [[DBLP-A]] | <span class="na">—</span> | 59.4 | | blocked-data |
| [[MN-40]] | <span class="na">—</span> | 75.7 | | blocked-data |
| [[20News]] | <span class="na">—</span> | 67.4 | | blocked-data |

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


## Hyperedge prediction <span class="m">Table 4 · AUROC</span>

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | <span class="v">53.7</span><span class="sd">±5.2</span> | 54.7 | <span class="d ok">−1.0</span> | |
| [[Cora-CA]] | <span class="v">61.1</span><span class="sd">±5.7</span> | 60.0 | <span class="d ok">+1.1</span> | |
| [[IMDB]] | <span class="v">53.3</span><span class="sd">±4.1</span> | 53.7 | <span class="d ok">−0.4</span> | |
| [[House]] | <span class="v">50.0</span><span class="sd">±0.0</span> | 50.0 | <span class="d ok">+0.0</span> | |
| [[Pubmed]] | <span class="v">51.3</span><span class="sd">±2.8</span> | 52.1 | <span class="d ok">−0.8</span> | |
| [[AMiner]] | <span class="v">68.5</span><span class="sd">±1.9</span> | 69.0 | <span class="d ok">−0.5</span> | |
| [[DBLP-P]] | <span class="na">—</span> | 67.0 | | pending |
| [[20News]] | <span class="na">—</span> | 50.0 | | blocked-data |

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


<div class="hg-legend"><span>우리값 <span class="sd">±표준편차</span></span><span class="d ok">±2 이내</span><span class="d warn">2–5</span><span class="d bad">5 초과</span><span class="lim">OOM</span><span class="lgn">논문이 수치를 못 낸 칸</span><span class="na">—</span><span class="lgn">미실행·보류</span></div>

관련: [[논문 대조]] · [[모델 비교]] · [[Home]]
<!-- AUTO:END -->

## 메모


