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
updated: 2026-09-15 14:48
tags: [hgnn/model]
cssclasses: [hg-model, table-wide, row-alt]
---

<!-- AUTO:BEGIN -->
# MLP

<span class="lgn">코드 `MLP/` · 결과 `results/result_*_MLP_*.txt` · 갱신 2026-09-15 14:48</span>

<div class="hg-cards"><div class="hg-card"><span class="k">NC 일치</span><span class="big">6/6</span><span class="note">|Δ| 중앙값 0.31</span></div><div class="hg-card"><span class="k">HP 일치</span><span class="big">6/6</span><span class="note">|Δ| 중앙값 0.00</span></div><div class="hg-card"><span class="k">최대 편차</span><span class="big">+1.2</span><span class="note">노드 분류 · Cora-CA</span></div></div>

## Node classification <span class="m">Table 3 · Accuracy</span>

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | <span class="v">32.4</span><span class="sd">±8.1</span> | 32.4 | <span class="d ok">+0.0</span> | |
| [[Cora-CA]] | <span class="v">37.2</span><span class="sd">±4.3</span> | 36.0 | <span class="d ok">+1.2</span> | |
| [[IMDB]] | <span class="v">38.2</span><span class="sd">±2.7</span> | 37.6 | <span class="d ok">+0.6</span> | |
| [[House]] | <span class="v">73.1</span><span class="sd">±3.2</span> | 73.1 | <span class="d ok">+0.0</span> | |
| [[Pubmed]] | <span class="v">62.7</span><span class="sd">±3.3</span> | 62.8 | <span class="d ok">−0.1</span> | |
| [[AMiner]] | <span class="v">22.4</span><span class="sd">±1.4</span> | 22.7 | <span class="d ok">−0.3</span> | |
| [[DBLP-A]] | <span class="na">—</span> | 56.6 | | blocked-data |
| [[MN-40]] | <span class="na">—</span> | 88.5 | | blocked-data |
| [[20News]] | <span class="na">—</span> | 73.3 | | blocked-data |

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


## Hyperedge prediction <span class="m">Table 4 · AUROC</span>

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | <span class="v">65.6</span><span class="sd">±2.0</span> | 65.6 | <span class="d ok">+0.0</span> | |
| [[Cora-CA]] | <span class="v">58.6</span><span class="sd">±2.9</span> | 58.6 | <span class="d ok">+0.0</span> | |
| [[IMDB]] | <span class="v">41.7</span><span class="sd">±2.5</span> | 42.0 | <span class="d ok">−0.3</span> | |
| [[House]] | <span class="v">54.8</span><span class="sd">±5.4</span> | 54.8 | <span class="d ok">+0.0</span> | |
| [[Pubmed]] | <span class="v">88.3</span><span class="sd">±0.6</span> | 88.3 | <span class="d ok">+0.0</span> | |
| [[AMiner]] | <span class="v">82.3</span><span class="sd">±0.9</span> | 82.3 | <span class="d ok">+0.0</span> | |
| [[DBLP-P]] | <span class="na">—</span> | 90.2 | | pending |
| [[20News]] | <span class="na">—</span> | 95.1 | | blocked-data |

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


<div class="hg-legend"><span>우리값 <span class="sd">±표준편차</span></span><span class="d ok">±2 이내</span><span class="d warn">2–5</span><span class="d bad">5 초과</span><span class="lim">OOM</span><span class="lgn">논문이 수치를 못 낸 칸</span><span class="na">—</span><span class="lgn">미실행·보류</span></div>

관련: [[논문 대조]] · [[모델 비교]] · [[Home]]
<!-- AUTO:END -->

## 메모


