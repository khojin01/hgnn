---
type: dataset
nc_models: 17
nc_best: PhenomNN
nc_best_value: 76.7
hp_models: 17
hp_best: TriCL
hp_best_value: 96.1
updated: 2026-09-15 15:11
tags: [hgnn/dataset]
cssclasses: [row-alt]
---

<!-- AUTO:BEGIN -->
# Pubmed

<small>갱신 2026-09-15 15:11</small>

## Node classification — Accuracy

| # | 모델 | 우리 | 논문 | Δ |
|---:|---|---:|---:|---:|
| 1 | [[PhenomNN]] | 76.7 <span class="sd">±3.6</span> | 76.8 | <span class="d ok">−0.1</span> |
| 2 | [[TriCL]] | 75.0 <span class="sd">±3.4</span> | 74.0 | <span class="d ok">+1.0</span> |
| 3 | [[MaskGAE]] | 74.6 <span class="sd">±4.2</span> | 75.4 | <span class="d ok">−0.8</span> |
| 4 | [[HypeBoy]] | 73.7 <span class="sd">±4.4</span> | 73.7 | <span class="d ok">+0.0</span> |
| 5 | [[VilLain]] | 73.7 <span class="sd">±3.3</span> | 73.7 | <span class="d ok">+0.0</span> |
| 6 | [[UniGCN2]] | 72.5 <span class="sd">±4.6</span> | 72.6 | <span class="d ok">−0.1</span> |
| 7 | [[AllSet]] | 72.5 <span class="sd">±6.2</span> | 74.1 | <span class="d ok">−1.6</span> |
| 8 | [[GraphMAE2]] | 72.2 <span class="sd">±4.7</span> | 72.6 | <span class="d ok">−0.4</span> |
| 9 | [[HGNN]] | 70.6 <span class="sd">±3.6</span> | 70.8 | <span class="d ok">−0.2</span> |
| 10 | [[UniGIN]] | 69.7 <span class="sd">±4.3</span> | 70.4 | <span class="d ok">−0.7</span> |
| 11 | [[HNHN]] | 69.5 <span class="sd">±3.4</span> | 69.1 | <span class="d ok">+0.3</span> |
| 12 | [[UniGCN]] | 68.6 <span class="sd">±5.0</span> | 67.6 | <span class="d ok">+1.0</span> |
| 13 | [[SE-HSSL]] | 63.4 <span class="sd">±9.1</span> | 69.8 | <span class="d bad">−6.4</span> |
| 14 | [[MLP]] | 62.7 <span class="sd">±3.3</span> | 62.8 | <span class="d ok">−0.1</span> |
| 15 | [[GGD]] | 62.2 <span class="sd">±5.0</span> | 64.9 | <span class="d warn">−2.7</span> |
| 16 | [[ED-HNN]] | 61.0 <span class="sd">±3.9</span> | 61.9 | <span class="d ok">−0.9</span> |
| 17 | [[HyperGCN]] | 59.3 <span class="sd">±15.2</span> | 59.3 | <span class="d ok">+0.0</span> |

```chart
type: bar
labels: [PhenomNN, TriCL, MaskGAE, HypeBoy, VilLain, UniGCN2, AllSet, GraphMAE2, HGNN, UniGIN, HNHN, UniGCN, SE-HSSL, MLP, GGD, ED-HNN, HyperGCN]
series:
  - title: 우리
    data: [76.7, 75.0, 74.6, 73.7, 73.7, 72.5, 72.5, 72.2, 70.6, 69.7, 69.5, 68.6, 63.4, 62.7, 62.2, 61.0, 59.3]
  - title: 논문
    data: [76.8, 74.0, 75.4, 73.7, 73.7, 72.6, 74.1, 72.6, 70.8, 70.4, 69.1, 67.6, 69.8, 62.8, 64.9, 61.9, 59.3]
tension: 0.2
width: 100%
labelColors: false
fill: false
beginAtZero: false
legend: true
stacked: false
height: 260px
```

<small>미실행·보류: HyperGRL (OOM), HyperGCL (pending)</small>

## Hyperedge prediction — AUROC

| # | 모델 | 우리 | 논문 | Δ |
|---:|---|---:|---:|---:|
| 1 | [[TriCL]] | 96.1 <span class="sd">±0.6</span> | 91.9 | <span class="d warn">+4.2</span> |
| 2 | [[MaskGAE]] | 95.5 <span class="sd">±0.3</span> | 95.5 | <span class="d ok">+0.0</span> |
| 3 | [[SE-HSSL]] | 95.0 <span class="sd">±0.4</span> | 94.5 | <span class="d ok">+0.5</span> |
| 4 | [[GraphMAE2]] | 93.9 <span class="sd">±1.8</span> | 93.6 | <span class="d ok">+0.3</span> |
| 5 | [[HypeBoy]] | 92.1 <span class="sd">±0.5</span> | 92.1 | <span class="d ok">+0.0</span> |
| 6 | [[MLP]] | 88.3 <span class="sd">±0.6</span> | 88.3 | <span class="d ok">+0.0</span> |
| 7 | [[VilLain]] | 84.3 <span class="sd">±0.8</span> | 83.7 | <span class="d ok">+0.6</span> |
| 8 | [[HyperGCN]] | 74.2 <span class="sd">±0.6</span> | 74.1 | <span class="d ok">+0.1</span> |
| 9 | [[UniGCN2]] | 69.1 <span class="sd">±1.0</span> | 69.1 | <span class="d ok">+0.0</span> |
| 10 | [[HGNN]] | 66.1 <span class="sd">±1.7</span> | 65.9 | <span class="d ok">+0.2</span> |
| 11 | [[PhenomNN]] | 65.1 <span class="sd">±1.7</span> | 64.0 | <span class="d ok">+1.1</span> |
| 12 | [[HNHN]] | 64.3 <span class="sd">±2.5</span> | 65.7 | <span class="d ok">−1.4</span> |
| 13 | [[ED-HNN]] | 53.3 <span class="sd">±3.1</span> | 53.2 | <span class="d ok">+0.1</span> |
| 14 | [[AllSet]] | 52.7 <span class="sd">±1.6</span> | 52.3 | <span class="d ok">+0.4</span> |
| 15 | [[UniGIN]] | 51.7 <span class="sd">±3.6</span> | 51.5 | <span class="d ok">+0.2</span> |
| 16 | [[UniGCN]] | 51.3 <span class="sd">±2.8</span> | 52.1 | <span class="d ok">−0.8</span> |
| 17 | [[GGD]] | 51.0 <span class="sd">±2.7</span> | 87.2 | <span class="d bad">−36.2</span> |

```chart
type: bar
labels: [TriCL, MaskGAE, SE-HSSL, GraphMAE2, HypeBoy, MLP, VilLain, HyperGCN, UniGCN2, HGNN, PhenomNN, HNHN, ED-HNN, AllSet, UniGIN, UniGCN, GGD]
series:
  - title: 우리
    data: [96.1, 95.5, 95.0, 93.9, 92.1, 88.3, 84.3, 74.2, 69.1, 66.1, 65.1, 64.3, 53.3, 52.7, 51.7, 51.3, 51.0]
  - title: 논문
    data: [91.9, 95.5, 94.5, 93.6, 92.1, 88.3, 83.7, 74.1, 69.1, 65.9, 64.0, 65.7, 53.2, 52.3, 51.5, 52.1, 87.2]
tension: 0.2
width: 100%
labelColors: false
fill: false
beginAtZero: false
legend: true
stacked: false
height: 260px
```

<small>미실행·보류: HyperGCL (pending), HyperGRL (unavailable: EP implementation missing)</small>

관련: [[논문 대조]] · [[데이터셋 비교]] · [[Home]]
<!-- AUTO:END -->

## 메모


