---
type: dataset
nc_models: 18
nc_best: HypeBoy
nc_best_value: 57.6
hp_models: 18
hp_best: SE-HSSL
hp_best_value: 90.6
updated: 2026-09-15 15:11
tags: [hgnn/dataset]
cssclasses: [row-alt]
---

<!-- AUTO:BEGIN -->
# Citeseer

<small>갱신 2026-09-15 15:11</small>

## Node classification — Accuracy

| # | 모델 | 우리 | 논문 | Δ |
|---:|---|---:|---:|---:|
| 1 | [[HypeBoy]] | 57.6 <span class="sd">±10.5</span> | 57.7 | <span class="d ok">−0.1</span> |
| 2 | [[SE-HSSL]] | 57.0 <span class="sd">±8.3</span> | 57.0 | <span class="d ok">+0.0</span> |
| 3 | [[MaskGAE]] | 52.7 <span class="sd">±10.4</span> | 53.2 | <span class="d ok">−0.5</span> |
| 4 | [[TriCL]] | 52.7 <span class="sd">±13.9</span> | 53.0 | <span class="d ok">−0.3</span> |
| 5 | [[GraphMAE2]] | 51.7 <span class="sd">±12.9</span> | 51.7 | <span class="d ok">+0.0</span> |
| 6 | [[PhenomNN]] | 45.1 <span class="sd">±11.7</span> | 42.2 | <span class="d warn">+2.9</span> |
| 7 | [[HNHN]] | 43.3 <span class="sd">±8.0</span> | 44.2 | <span class="d ok">−0.9</span> |
| 8 | [[UniGCN2]] | 41.5 <span class="sd">±9.2</span> | 39.6 | <span class="d ok">+1.9</span> |
| 9 | [[AllSet]] | 41.0 <span class="sd">±8.3</span> | 41.1 | <span class="d ok">−0.1</span> |
| 10 | [[UniGIN]] | 40.3 <span class="sd">±9.4</span> | 41.4 | <span class="d ok">−1.1</span> |
| 11 | [[HGNN]] | 38.1 <span class="sd">±10.7</span> | 38.1 | <span class="d ok">−0.0</span> |
| 12 | [[UniGCN]] | 37.7 <span class="sd">±8.6</span> | 39.8 | <span class="d warn">−2.1</span> |
| 13 | [[ED-HNN]] | 34.0 <span class="sd">±8.8</span> | 32.9 | <span class="d ok">+1.1</span> |
| 14 | [[HyperGCN]] | 33.7 <span class="sd">±7.3</span> | 33.8 | <span class="d ok">−0.1</span> |
| 15 | [[MLP]] | 32.4 <span class="sd">±8.1</span> | 32.4 | <span class="d ok">+0.0</span> |
| 16 | [[VilLain]] | 28.5 <span class="sd">±8.2</span> | 33.6 | <span class="d bad">−5.1</span> |
| 17 | [[GGD]] | 27.5 <span class="sd">±6.4</span> | 34.0 | <span class="d bad">−6.5</span> |
| 18 | [[HyperGCL]] | 18.5 <span class="sd">±3.5</span> | 43.4 | <span class="d bad">−24.9</span> |

```chart
type: bar
labels: [HypeBoy, SE-HSSL, MaskGAE, TriCL, GraphMAE2, PhenomNN, HNHN, UniGCN2, AllSet, UniGIN, HGNN, UniGCN, ED-HNN, HyperGCN, MLP, VilLain, GGD, HyperGCL]
series:
  - title: 우리
    data: [57.6, 57.0, 52.7, 52.7, 51.7, 45.1, 43.3, 41.5, 41.0, 40.3, 38.1, 37.7, 34.0, 33.7, 32.4, 28.5, 27.5, 18.5]
  - title: 논문
    data: [57.7, 57.0, 53.2, 53.0, 51.7, 42.2, 44.2, 39.6, 41.1, 41.4, 38.1, 39.8, 32.9, 33.8, 32.4, 33.6, 34.0, 43.4]
tension: 0.2
width: 100%
labelColors: false
fill: false
beginAtZero: false
legend: true
stacked: false
height: 260px
```

<small>미실행·보류: HyperGRL (OOM)</small>

## Hyperedge prediction — AUROC

| # | 모델 | 우리 | 논문 | Δ |
|---:|---|---:|---:|---:|
| 1 | [[SE-HSSL]] | 90.6 <span class="sd">±1.1</span> | 90.5 | <span class="d ok">+0.1</span> |
| 2 | [[TriCL]] | 89.1 <span class="sd">±1.3</span> | 90.5 | <span class="d ok">−1.4</span> |
| 3 | [[MaskGAE]] | 86.7 <span class="sd">±1.7</span> | 86.7 | <span class="d ok">+0.0</span> |
| 4 | [[HypeBoy]] | 86.4 <span class="sd">±2.1</span> | 86.4 | <span class="d ok">+0.0</span> |
| 5 | [[GraphMAE2]] | 78.1 <span class="sd">±2.4</span> | 78.2 | <span class="d ok">−0.1</span> |
| 6 | [[MLP]] | 65.6 <span class="sd">±2.0</span> | 65.6 | <span class="d ok">+0.0</span> |
| 7 | [[UniGCN2]] | 60.3 <span class="sd">±2.1</span> | 60.2 | <span class="d ok">+0.1</span> |
| 8 | [[ED-HNN]] | 58.1 <span class="sd">±2.8</span> | 58.0 | <span class="d ok">+0.1</span> |
| 9 | [[VilLain]] | 57.2 <span class="sd">±2.4</span> | 58.3 | <span class="d ok">−1.1</span> |
| 10 | [[HyperGCN]] | 54.9 <span class="sd">±2.1</span> | 54.9 | <span class="d ok">+0.0</span> |
| 11 | [[PhenomNN]] | 54.3 <span class="sd">±2.2</span> | 54.5 | <span class="d ok">−0.2</span> |
| 12 | [[HGNN]] | 54.2 <span class="sd">±3.7</span> | 54.8 | <span class="d ok">−0.6</span> |
| 13 | [[UniGCN]] | 53.7 <span class="sd">±5.2</span> | 54.7 | <span class="d ok">−1.0</span> |
| 14 | [[HNHN]] | 53.7 <span class="sd">±2.5</span> | 53.7 | <span class="d ok">+0.0</span> |
| 15 | [[UniGIN]] | 53.3 <span class="sd">±3.4</span> | 52.9 | <span class="d ok">+0.4</span> |
| 16 | [[GGD]] | 52.9 <span class="sd">±4.2</span> | 72.2 | <span class="d bad">−19.3</span> |
| 17 | [[HyperGCL]] | 51.9 <span class="sd">±2.9</span> | 73.9 | <span class="d bad">−22.0</span> |
| 18 | [[AllSet]] | 50.7 <span class="sd">±3.3</span> | 51.8 | <span class="d ok">−1.1</span> |

```chart
type: bar
labels: [SE-HSSL, TriCL, MaskGAE, HypeBoy, GraphMAE2, MLP, UniGCN2, ED-HNN, VilLain, HyperGCN, PhenomNN, HGNN, UniGCN, HNHN, UniGIN, GGD, HyperGCL, AllSet]
series:
  - title: 우리
    data: [90.6, 89.1, 86.7, 86.4, 78.1, 65.6, 60.3, 58.1, 57.2, 54.9, 54.3, 54.2, 53.7, 53.7, 53.3, 52.9, 51.9, 50.7]
  - title: 논문
    data: [90.5, 90.5, 86.7, 86.4, 78.2, 65.6, 60.2, 58.0, 58.3, 54.9, 54.5, 54.8, 54.7, 53.7, 52.9, 72.2, 73.9, 51.8]
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


