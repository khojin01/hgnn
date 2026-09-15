---
type: model
nc_agree: 2
nc_done: 6
hp_agree: 0
hp_done: 6
max_abs_delta: 37.9
worst_cell: "하이퍼엣지 예측 House −37.9"
status: complete
code_dir: H-GD
updated: 2026-09-15 14:48
tags: [hgnn/model]
cssclasses: [hg-model, table-wide, row-alt]
---

<!-- AUTO:BEGIN -->
# GGD

<span class="lgn">코드 `H-GD/` · 결과 `results/result_*_H-GD_*.txt` · 갱신 2026-09-15 14:48</span>

<div class="hg-cards"><div class="hg-card"><span class="k">NC 일치</span><span class="big">2/6</span><span class="note">|Δ| 중앙값 3.90</span></div><div class="hg-card"><span class="k">HP 일치</span><span class="big">0/6</span><span class="note">|Δ| 중앙값 34.20</span></div><div class="hg-card"><span class="k">최대 편차</span><span class="big">−37.9</span><span class="note">하이퍼엣지 예측 · House</span></div></div>

## Node classification <span class="m">Table 3 · Accuracy</span>

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | <span class="v">27.5</span><span class="sd">±6.4</span> | 34.0 | <span class="d bad">−6.5</span> | |
| [[Cora-CA]] | <span class="v">28.3</span><span class="sd">±4.6</span> | 32.2 | <span class="d warn">−3.9</span> | |
| [[IMDB]] | <span class="v">36.7</span><span class="sd">±2.6</span> | 37.6 | <span class="d ok">−0.9</span> | |
| [[House]] | <span class="v">49.9</span><span class="sd">±1.3</span> | 50.6 | <span class="d ok">−0.7</span> | |
| [[Pubmed]] | <span class="v">62.2</span><span class="sd">±5.0</span> | 64.9 | <span class="d warn">−2.7</span> | |
| [[AMiner]] | <span class="v">16.6</span><span class="sd">±2.7</span> | 31.5 | <span class="d bad">−14.9</span> | |
| [[DBLP-A]] | <span class="na">—</span> | 58.8 | | blocked-data |
| [[MN-40]] | <span class="na">—</span> | 76.8 | | blocked-data |
| [[20News]] | <span class="na">—</span> | 47.5 | | blocked-data |

```chart
type: bar
labels: [Citeseer, Cora-CA, IMDB, House, Pubmed, AMiner]
series:
  - title: 우리
    data: [27.5, 28.3, 36.7, 49.9, 62.2, 16.6]
  - title: 논문
    data: [34.0, 32.2, 37.6, 50.6, 64.9, 31.5]
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
| [[Citeseer]] | <span class="v">52.9</span><span class="sd">±4.2</span> | 72.2 | <span class="d bad">−19.3</span> | |
| [[Cora-CA]] | <span class="v">43.9</span><span class="sd">±10.3</span> | 73.2 | <span class="d bad">−29.3</span> | |
| [[IMDB]] | <span class="v">46.1</span><span class="sd">±3.3</span> | 53.1 | <span class="d bad">−7.0</span> | |
| [[House]] | <span class="v">50.0</span><span class="sd">±0.0</span> | 87.9 | <span class="d bad">−37.9</span> | |
| [[Pubmed]] | <span class="v">51.0</span><span class="sd">±2.7</span> | 87.2 | <span class="d bad">−36.2</span> | |
| [[AMiner]] | <span class="v">50.7</span><span class="sd">±8.3</span> | 84.9 | <span class="d bad">−34.2</span> | |
| [[DBLP-P]] | <span class="na">—</span> | 91.6 | | pending |
| [[20News]] | <span class="na">—</span> | 87.9 | | blocked-data |

```chart
type: bar
labels: [Citeseer, Cora-CA, IMDB, House, Pubmed, AMiner]
series:
  - title: 우리
    data: [52.9, 43.9, 46.1, 50.0, 51.0, 50.7]
  - title: 논문
    data: [72.2, 73.2, 53.1, 87.9, 87.2, 84.9]
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


