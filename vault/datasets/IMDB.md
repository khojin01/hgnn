---
type: dataset
nc_models: 17
nc_best: SE-HSSL
nc_best_value: 48.9
hp_models: 18
hp_best: HGNN
hp_best_value: 62.8
updated: 2026-09-15 15:11
tags: [hgnn/dataset]
cssclasses: [row-alt]
---

<!-- AUTO:BEGIN -->
# IMDB

<small>갱신 2026-09-15 15:11</small>

## Node classification — Accuracy

| # | 모델 | 우리 | 논문 | Δ |
|---:|---|---:|---:|---:|
| 1 | [[SE-HSSL]] | 48.9 <span class="sd">±4.0</span> | 48.9 | <span class="d ok">+0.0</span> |
| 2 | [[HypeBoy]] | 48.0 <span class="sd">±5.0</span> | 48.3 | <span class="d ok">−0.3</span> |
| 3 | [[TriCL]] | 47.9 <span class="sd">±5.3</span> | 47.5 | <span class="d ok">+0.4</span> |
| 4 | [[GraphMAE2]] | 44.7 <span class="sd">±4.2</span> | 45.6 | <span class="d ok">−0.9</span> |
| 5 | [[MaskGAE]] | 44.7 <span class="sd">±3.5</span> | 45.0 | <span class="d ok">−0.3</span> |
| 6 | [[UniGCN2]] | 42.5 <span class="sd">±3.2</span> | 41.6 | <span class="d ok">+0.9</span> |
| 7 | [[PhenomNN]] | 42.1 <span class="sd">±2.9</span> | 42.1 | <span class="d ok">+0.0</span> |
| 8 | [[HGNN]] | 41.9 <span class="sd">±4.5</span> | 41.5 | <span class="d ok">+0.4</span> |
| 9 | [[HNHN]] | 41.8 <span class="sd">±3.7</span> | 42.5 | <span class="d ok">−0.7</span> |
| 10 | [[UniGIN]] | 41.1 <span class="sd">±3.9</span> | 41.7 | <span class="d ok">−0.6</span> |
| 11 | [[HyperGCN]] | 40.6 <span class="sd">±3.2</span> | 40.6 | <span class="d ok">+0.0</span> |
| 12 | [[UniGCN]] | 40.5 <span class="sd">±3.3</span> | 41.0 | <span class="d ok">−0.5</span> |
| 13 | [[AllSet]] | 40.5 <span class="sd">±4.6</span> | 41.7 | <span class="d ok">−1.2</span> |
| 14 | [[VilLain]] | 39.2 <span class="sd">±3.9</span> | 39.7 | <span class="d ok">−0.5</span> |
| 15 | [[MLP]] | 38.2 <span class="sd">±2.7</span> | 37.6 | <span class="d ok">+0.6</span> |
| 16 | [[ED-HNN]] | 38.0 <span class="sd">±2.8</span> | 37.2 | <span class="d ok">+0.8</span> |
| 17 | [[GGD]] | 36.7 <span class="sd">±2.6</span> | 37.6 | <span class="d ok">−0.9</span> |

```chart
type: bar
labels: [SE-HSSL, HypeBoy, TriCL, GraphMAE2, MaskGAE, UniGCN2, PhenomNN, HGNN, HNHN, UniGIN, HyperGCN, UniGCN, AllSet, VilLain, MLP, ED-HNN, GGD]
series:
  - title: 우리
    data: [48.9, 48.0, 47.9, 44.7, 44.7, 42.5, 42.1, 41.9, 41.8, 41.1, 40.6, 40.5, 40.5, 39.2, 38.2, 38.0, 36.7]
  - title: 논문
    data: [48.9, 48.3, 47.5, 45.6, 45.0, 41.6, 42.1, 41.5, 42.5, 41.7, 40.6, 41.0, 41.7, 39.7, 37.6, 37.2, 37.6]
tension: 0.2
width: 100%
labelColors: false
fill: false
beginAtZero: false
legend: true
stacked: false
height: 260px
```

<small>미실행·보류: HyperGRL (OOM), HyperGCL (diagnostic only: splits 19–20 (no formal aggregate))</small>

## Hyperedge prediction — AUROC

| # | 모델 | 우리 | 논문 | Δ |
|---:|---|---:|---:|---:|
| 1 | [[HGNN]] | 62.8 <span class="sd">±1.4</span> | 60.5 | <span class="d warn">+2.3</span> |
| 2 | [[HypeBoy]] | 59.3 <span class="sd">±1.8</span> | 59.4 | <span class="d ok">−0.1</span> |
| 3 | [[UniGCN2]] | 57.1 <span class="sd">±6.0</span> | 57.5 | <span class="d ok">−0.4</span> |
| 4 | [[TriCL]] | 56.8 <span class="sd">±3.8</span> | 58.9 | <span class="d warn">−2.1</span> |
| 5 | [[MaskGAE]] | 54.5 <span class="sd">±1.3</span> | 54.4 | <span class="d ok">+0.1</span> |
| 6 | [[SE-HSSL]] | 54.1 <span class="sd">±2.0</span> | 55.6 | <span class="d ok">−1.5</span> |
| 7 | [[UniGIN]] | 53.9 <span class="sd">±4.5</span> | 54.6 | <span class="d ok">−0.7</span> |
| 8 | [[UniGCN]] | 53.3 <span class="sd">±4.1</span> | 53.7 | <span class="d ok">−0.4</span> |
| 9 | [[HyperGCL]] | 50.9 <span class="sd">±2.8</span> | 53.8 | <span class="d warn">−2.9</span> |
| 10 | [[AllSet]] | 50.6 <span class="sd">±1.7</span> | 50.3 | <span class="d ok">+0.3</span> |
| 11 | [[PhenomNN]] | 49.8 <span class="sd">±0.9</span> | 49.7 | <span class="d ok">+0.1</span> |
| 12 | [[ED-HNN]] | 49.1 <span class="sd">±1.3</span> | 49.4 | <span class="d ok">−0.3</span> |
| 13 | [[HyperGCN]] | 48.4 <span class="sd">±1.9</span> | 48.4 | <span class="d ok">+0.0</span> |
| 14 | [[HNHN]] | 48.2 <span class="sd">±0.7</span> | 48.2 | <span class="d ok">+0.0</span> |
| 15 | [[GraphMAE2]] | 47.4 <span class="sd">±1.0</span> | 47.2 | <span class="d ok">+0.2</span> |
| 16 | [[GGD]] | 46.1 <span class="sd">±3.3</span> | 53.1 | <span class="d bad">−7.0</span> |
| 17 | [[VilLain]] | 43.6 <span class="sd">±2.6</span> | 43.9 | <span class="d ok">−0.3</span> |
| 18 | [[MLP]] | 41.7 <span class="sd">±2.5</span> | 42.0 | <span class="d ok">−0.3</span> |

```chart
type: bar
labels: [HGNN, HypeBoy, UniGCN2, TriCL, MaskGAE, SE-HSSL, UniGIN, UniGCN, HyperGCL, AllSet, PhenomNN, ED-HNN, HyperGCN, HNHN, GraphMAE2, GGD, VilLain, MLP]
series:
  - title: 우리
    data: [62.8, 59.3, 57.1, 56.8, 54.5, 54.1, 53.9, 53.3, 50.9, 50.6, 49.8, 49.1, 48.4, 48.2, 47.4, 46.1, 43.6, 41.7]
  - title: 논문
    data: [60.5, 59.4, 57.5, 58.9, 54.4, 55.6, 54.6, 53.7, 53.8, 50.3, 49.7, 49.4, 48.4, 48.2, 47.2, 53.1, 43.9, 42.0]
tension: 0.2
width: 100%
labelColors: false
fill: false
beginAtZero: false
legend: true
stacked: false
height: 260px
```

<small>미실행·보류: HyperGRL (unavailable: EP implementation missing)</small>

관련: [[논문 대조]] · [[데이터셋 비교]] · [[Home]]
<!-- AUTO:END -->

## 메모


