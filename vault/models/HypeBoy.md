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
updated: 2026-09-15 14:48
tags: [hgnn/model]
cssclasses: [hg-model, table-wide, row-alt]
---

<!-- AUTO:BEGIN -->
# HypeBoy

<span class="lgn">코드 `Hypeboy/` · 결과 `results/result_*_Hypeboy_*.txt` · 갱신 2026-09-15 14:48</span>

<div class="hg-cards"><div class="hg-card"><span class="k">NC 일치</span><span class="big">6/6</span><span class="note">|Δ| 중앙값 0.30</span></div><div class="hg-card"><span class="k">HP 일치</span><span class="big">6/6</span><span class="note">|Δ| 중앙값 0.10</span></div><div class="hg-card"><span class="k">최대 편차</span><span class="big">+1.0</span><span class="note">노드 분류 · House</span></div></div>

## Node classification <span class="m">Table 3 · Accuracy</span>

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | <span class="v">57.6</span><span class="sd">±10.5</span> | 57.7 | <span class="d ok">−0.1</span> | |
| [[Cora-CA]] | <span class="v">67.0</span><span class="sd">±3.7</span> | 67.0 | <span class="d ok">+0.0</span> | |
| [[IMDB]] | <span class="v">48.0</span><span class="sd">±5.0</span> | 48.3 | <span class="d ok">−0.3</span> | |
| [[House]] | <span class="v">68.7</span><span class="sd">±6.0</span> | 67.7 | <span class="d ok">+1.0</span> | |
| [[Pubmed]] | <span class="v">73.7</span><span class="sd">±4.4</span> | 73.7 | <span class="d ok">+0.0</span> | |
| [[AMiner]] | <span class="v">34.2</span><span class="sd">±3.0</span> | 34.6 | <span class="d ok">−0.4</span> | |
| [[DBLP-A]] | <span class="na">—</span> | 81.2 | | blocked-data |
| [[MN-40]] | <span class="na">—</span> | 89.2 | | blocked-data |
| [[20News]] | <span class="na">—</span> | 75.7 | | blocked-data |

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


## Hyperedge prediction <span class="m">Table 4 · AUROC</span>

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | <span class="v">86.4</span><span class="sd">±2.1</span> | 86.4 | <span class="d ok">+0.0</span> | |
| [[Cora-CA]] | <span class="v">87.4</span><span class="sd">±1.5</span> | 87.3 | <span class="d ok">+0.1</span> | |
| [[IMDB]] | <span class="v">59.3</span><span class="sd">±1.8</span> | 59.4 | <span class="d ok">−0.1</span> | |
| [[House]] | <span class="v">87.0</span><span class="sd">±3.0</span> | 87.2 | <span class="d ok">−0.2</span> | |
| [[Pubmed]] | <span class="v">92.1</span><span class="sd">±0.5</span> | 92.1 | <span class="d ok">+0.0</span> | |
| [[AMiner]] | <span class="v">89.7</span><span class="sd">±0.6</span> | 89.7 | <span class="d ok">+0.0</span> | |
| [[DBLP-P]] | <span class="na">—</span> | 95.2 | | pending |
| [[20News]] | <span class="na">—</span> | 97.2 | | blocked-data |

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


<div class="hg-legend"><span>우리값 <span class="sd">±표준편차</span></span><span class="d ok">±2 이내</span><span class="d warn">2–5</span><span class="d bad">5 초과</span><span class="lim">OOM</span><span class="lgn">논문이 수치를 못 낸 칸</span><span class="na">—</span><span class="lgn">미실행·보류</span></div>

관련: [[논문 대조]] · [[모델 비교]] · [[Home]]
<!-- AUTO:END -->

## 메모


