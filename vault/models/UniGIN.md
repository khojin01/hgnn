---
type: model
nc_agree: 6
nc_done: 6
hp_agree: 6
hp_done: 6
max_abs_delta: 1.6
worst_cell: "노드 분류 Cora-CA −1.6"
status: complete
code_dir: UniGIN
updated: 2026-09-15 14:20
tags: [hgnn/model]
cssclasses: [hg-model]
---

<!-- AUTO:BEGIN -->
# UniGIN

<span class="lgn">코드 `UniGIN/` · 결과 `results/result_*_UniGIN_*.txt` · 갱신 2026-09-15 14:20</span>

<div class="hg-cards"><div class="hg-card"><span class="k">NC 일치</span><span class="big">6/6</span><span class="note">|Δ| 중앙값 0.66</span></div><div class="hg-card"><span class="k">HP 일치</span><span class="big">6/6</span><span class="note">|Δ| 중앙값 0.40</span></div><div class="hg-card"><span class="k">최대 편차</span><span class="big">−1.6</span><span class="note">노드 분류 · Cora-CA</span></div></div>

## Node classification <span class="m">Table 3 · Accuracy</span>

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | <span class="v">40.3</span><span class="sd">±9.4</span> | 41.4 | <span class="d ok">−1.1</span> | |
| [[Cora-CA]] | <span class="v">47.6</span><span class="sd">±6.5</span> | 49.2 | <span class="d ok">−1.6</span> | |
| [[IMDB]] | <span class="v">41.1</span><span class="sd">±3.9</span> | 41.7 | <span class="d ok">−0.6</span> | |
| [[House]] | <span class="v">51.0</span><span class="sd">±2.3</span> | 50.8 | <span class="d ok">+0.2</span> | |
| [[Pubmed]] | <span class="v">69.7</span><span class="sd">±4.3</span> | 70.4 | <span class="d ok">−0.7</span> | |
| [[AMiner]] | <span class="v">30.7</span><span class="sd">±1.2</span> | 30.8 | <span class="d ok">−0.1</span> | |
| [[DBLP-A]] | <span class="na">—</span> | 63.1 | | blocked-data |
| [[MN-40]] | <span class="na">—</span> | 87.1 | | blocked-data |
| [[20News]] | <span class="na">—</span> | 68.1 | | blocked-data |

```chart
type: bar
labels: [Citeseer, Cora-CA, IMDB, House, Pubmed, AMiner]
series:
  - title: 우리
    data: [40.3, 47.6, 41.1, 51.0, 69.7, 30.7]
  - title: 논문
    data: [41.4, 49.2, 41.7, 50.8, 70.4, 30.8]
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
| [[Citeseer]] | <span class="v">53.3</span><span class="sd">±3.4</span> | 52.9 | <span class="d ok">+0.4</span> | |
| [[Cora-CA]] | <span class="v">59.7</span><span class="sd">±7.6</span> | 58.7 | <span class="d ok">+1.0</span> | |
| [[IMDB]] | <span class="v">53.9</span><span class="sd">±4.5</span> | 54.6 | <span class="d ok">−0.7</span> | |
| [[House]] | <span class="v">50.0</span><span class="sd">±0.0</span> | 50.0 | <span class="d ok">+0.0</span> | |
| [[Pubmed]] | <span class="v">51.7</span><span class="sd">±3.6</span> | 51.5 | <span class="d ok">+0.2</span> | |
| [[AMiner]] | <span class="v">68.9</span><span class="sd">±1.2</span> | 69.1 | <span class="d ok">−0.2</span> | |
| [[DBLP-P]] | <span class="na">—</span> | 69.2 | | pending |
| [[20News]] | <span class="na">—</span> | 50.0 | | blocked-data |

```chart
type: bar
labels: [Citeseer, Cora-CA, IMDB, House, Pubmed, AMiner]
series:
  - title: 우리
    data: [53.3, 59.7, 53.9, 50.0, 51.7, 68.9]
  - title: 논문
    data: [52.9, 58.7, 54.6, 50.0, 51.5, 69.1]
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


