---
type: model
nc_agree: 5
nc_done: 6
hp_agree: 6
hp_done: 6
max_abs_delta: 5.1
worst_cell: "노드 분류 Citeseer −5.1"
status: complete
code_dir: VilLain
updated: 2026-09-15 14:48
tags: [hgnn/model]
cssclasses: [hg-model, table-wide, row-alt]
---

<!-- AUTO:BEGIN -->
# VilLain

<span class="lgn">코드 `VilLain/` · 결과 `results/result_*_VilLain_*.txt` · 갱신 2026-09-15 14:48</span>

<div class="hg-cards"><div class="hg-card"><span class="k">NC 일치</span><span class="big">5/6</span><span class="note">|Δ| 중앙값 0.50</span></div><div class="hg-card"><span class="k">HP 일치</span><span class="big">6/6</span><span class="note">|Δ| 중앙값 0.60</span></div><div class="hg-card"><span class="k">최대 편차</span><span class="big">−5.1</span><span class="note">노드 분류 · Citeseer</span></div></div>

## Node classification <span class="m">Table 3 · Accuracy</span>

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | <span class="v">28.5</span><span class="sd">±8.2</span> | 33.6 | <span class="d bad">−5.1</span> | |
| [[Cora-CA]] | <span class="v">31.4</span><span class="sd">±4.1</span> | 31.4 | <span class="d ok">+0.0</span> | |
| [[IMDB]] | <span class="v">39.2</span><span class="sd">±3.9</span> | 39.7 | <span class="d ok">−0.5</span> | |
| [[House]] | <span class="v">49.3</span><span class="sd">±1.5</span> | 50.6 | <span class="d ok">−1.3</span> | |
| [[Pubmed]] | <span class="v">73.7</span><span class="sd">±3.3</span> | 73.7 | <span class="d ok">+0.0</span> | |
| [[AMiner]] | <span class="v">19.9</span><span class="sd">±1.2</span> | 19.9 | <span class="d ok">+0.0</span> | |
| [[DBLP-A]] | <span class="na">—</span> | 40.4 | | blocked-data |
| [[MN-40]] | <span class="na">—</span> | 69.7 | | blocked-data |
| [[20News]] | <span class="na">—</span> | 74.3 | | blocked-data |

```chart
type: bar
labels: [Citeseer, Cora-CA, IMDB, House, Pubmed, AMiner]
series:
  - title: 우리
    data: [28.5, 31.4, 39.2, 49.3, 73.7, 19.9]
  - title: 논문
    data: [33.6, 31.4, 39.7, 50.6, 73.7, 19.9]
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
| [[Citeseer]] | <span class="v">57.2</span><span class="sd">±2.4</span> | 58.3 | <span class="d ok">−1.1</span> | |
| [[Cora-CA]] | <span class="v">64.7</span><span class="sd">±2.5</span> | 64.4 | <span class="d ok">+0.3</span> | |
| [[IMDB]] | <span class="v">43.6</span><span class="sd">±2.6</span> | 43.9 | <span class="d ok">−0.3</span> | |
| [[House]] | <span class="v">77.5</span><span class="sd">±5.6</span> | 77.2 | <span class="d ok">+0.3</span> | |
| [[Pubmed]] | <span class="v">84.3</span><span class="sd">±0.8</span> | 83.7 | <span class="d ok">+0.6</span> | |
| [[AMiner]] | <span class="v">61.9</span><span class="sd">±0.7</span> | 62.7 | <span class="d ok">−0.8</span> | |
| [[DBLP-P]] | <span class="na">—</span> | 56.3 | | pending |
| [[20News]] | <span class="na">—</span> | 59.2 | | blocked-data |

```chart
type: bar
labels: [Citeseer, Cora-CA, IMDB, House, Pubmed, AMiner]
series:
  - title: 우리
    data: [57.2, 64.7, 43.6, 77.5, 84.3, 61.9]
  - title: 논문
    data: [58.3, 64.4, 43.9, 77.2, 83.7, 62.7]
tension: 0.2
width: 100%
labelColors: false
fill: false
beginAtZero: false
legend: true
stacked: false
height: 220px
```


## Community detection <span class="m">Table 5 · NMI</span>

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Cora-CA]] | <span class="na">—</span> | 9.7 | | pending |
| [[DBLP-P]] | <span class="na">—</span> | 40.1 | | pending |
| [[20News]] | <span class="na">—</span> | 38.8 | | pending |

<div class="hg-legend"><span>우리값 <span class="sd">±표준편차</span></span><span class="d ok">±2 이내</span><span class="d warn">2–5</span><span class="d bad">5 초과</span><span class="lim">OOM</span><span class="lgn">논문이 수치를 못 낸 칸</span><span class="na">—</span><span class="lgn">미실행·보류</span></div>

관련: [[논문 대조]] · [[모델 비교]] · [[Home]]
<!-- AUTO:END -->

## 메모


