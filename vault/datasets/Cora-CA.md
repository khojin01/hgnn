---
type: dataset
nc_models: 19
nc_best: HypeBoy
nc_best_value: 67.0
hp_models: 18
hp_best: HypeBoy
hp_best_value: 87.4
updated: 2026-09-15 15:02
tags: [hgnn/dataset]
cssclasses: [table-wide, row-alt]
---

<!-- AUTO:BEGIN -->
# Cora-CA

<small>갱신 2026-09-15 15:02</small>

## Node classification — Accuracy

| # | 모델 | 우리 | 논문 | Δ |
|---:|---|---:|---:|---:|
| 1 | [[HypeBoy]] | 67.0 <span class="sd">±3.7</span> | 67.0 | <span class="d ok">+0.0</span> |
| 2 | [[GraphMAE2]] | 64.0 <span class="sd">±5.8</span> | 64.3 | <span class="d ok">−0.3</span> |
| 3 | [[SE-HSSL]] | 64.0 <span class="sd">±4.9</span> | 63.9 | <span class="d ok">+0.1</span> |
| 4 | [[TriCL]] | 61.9 <span class="sd">±5.8</span> | 63.4 | <span class="d ok">−1.5</span> |
| 5 | [[MaskGAE]] | 56.5 <span class="sd">±6.8</span> | 59.8 | <span class="d warn">−3.3</span> |
| 6 | [[PhenomNN]] | 56.3 <span class="sd">±7.5</span> | 56.2 | <span class="d ok">+0.1</span> |
| 7 | [[UniGCN2]] | 53.1 <span class="sd">±7.3</span> | 55.3 | <span class="d warn">−2.2</span> |
| 8 | [[AllSet]] | 53.1 <span class="sd">±6.4</span> | 53.6 | <span class="d ok">−0.5</span> |
| 9 | [[HNHN]] | 51.0 <span class="sd">±6.6</span> | 53.1 | <span class="d warn">−2.1</span> |
| 10 | [[UniGIN]] | 47.6 <span class="sd">±6.5</span> | 49.2 | <span class="d ok">−1.6</span> |
| 11 | [[UniGCN]] | 47.2 <span class="sd">±5.2</span> | 46.3 | <span class="d ok">+0.9</span> |
| 12 | [[HGNN]] | 46.6 <span class="sd">±7.9</span> | 44.3 | <span class="d warn">+2.3</span> |
| 13 | [[HyperGCN]] | 45.0 <span class="sd">±9.5</span> | 45.0 | <span class="d ok">+0.0</span> |
| 14 | [[HyperGRL]] | 42.0 <span class="sd">±6.7</span> | 41.8 | <span class="d ok">+0.2</span> |
| 15 | [[MLP]] | 37.2 <span class="sd">±4.3</span> | 36.0 | <span class="d ok">+1.2</span> |
| 16 | [[ED-HNN]] | 36.5 <span class="sd">±7.5</span> | 36.3 | <span class="d ok">+0.2</span> |
| 17 | [[VilLain]] | 31.4 <span class="sd">±4.1</span> | 31.4 | <span class="d ok">+0.0</span> |
| 18 | [[GGD]] | 28.3 <span class="sd">±4.6</span> | 32.2 | <span class="d warn">−3.9</span> |
| 19 | [[HyperGCL]] | 16.3 <span class="sd">±4.0</span> | 61.8 | <span class="d bad">−45.5</span> |

```chart
type: bar
labels: [HypeBoy, GraphMAE2, SE-HSSL, TriCL, MaskGAE, PhenomNN, UniGCN2, AllSet, HNHN, UniGIN, UniGCN, HGNN, HyperGCN, HyperGRL, MLP, ED-HNN, VilLain, GGD, HyperGCL]
series:
  - title: 우리
    data: [67.0, 64.0, 64.0, 61.9, 56.5, 56.3, 53.1, 53.1, 51.0, 47.6, 47.2, 46.6, 45.0, 42.0, 37.2, 36.5, 31.4, 28.3, 16.3]
  - title: 논문
    data: [67.0, 64.3, 63.9, 63.4, 59.8, 56.2, 55.3, 53.6, 53.1, 49.2, 46.3, 44.3, 45.0, 41.8, 36.0, 36.3, 31.4, 32.2, 61.8]
tension: 0.2
width: 100%
labelColors: false
fill: false
beginAtZero: false
legend: true
stacked: false
height: 260px
```

## Hyperedge prediction — AUROC

| # | 모델 | 우리 | 논문 | Δ |
|---:|---|---:|---:|---:|
| 1 | [[HypeBoy]] | 87.4 <span class="sd">±1.5</span> | 87.3 | <span class="d ok">+0.1</span> |
| 2 | [[SE-HSSL]] | 85.7 <span class="sd">±2.3</span> | 85.6 | <span class="d ok">+0.1</span> |
| 3 | [[TriCL]] | 85.0 <span class="sd">±2.0</span> | 87.8 | <span class="d warn">−2.8</span> |
| 4 | [[MaskGAE]] | 76.1 <span class="sd">±2.2</span> | 76.5 | <span class="d ok">−0.4</span> |
| 5 | [[GraphMAE2]] | 74.7 <span class="sd">±2.9</span> | 74.7 | <span class="d ok">+0.0</span> |
| 6 | [[VilLain]] | 64.7 <span class="sd">±2.5</span> | 64.4 | <span class="d ok">+0.3</span> |
| 7 | [[HGNN]] | 64.5 <span class="sd">±5.9</span> | 65.0 | <span class="d ok">−0.5</span> |
| 8 | [[UniGCN]] | 61.1 <span class="sd">±5.7</span> | 60.0 | <span class="d ok">+1.1</span> |
| 9 | [[UniGIN]] | 59.7 <span class="sd">±7.6</span> | 58.7 | <span class="d ok">+1.0</span> |
| 10 | [[ED-HNN]] | 59.2 <span class="sd">±3.2</span> | 58.9 | <span class="d ok">+0.3</span> |
| 11 | [[MLP]] | 58.6 <span class="sd">±2.9</span> | 58.6 | <span class="d ok">+0.0</span> |
| 12 | [[UniGCN2]] | 52.2 <span class="sd">±4.5</span> | 51.9 | <span class="d ok">+0.3</span> |
| 13 | [[HNHN]] | 51.8 <span class="sd">±1.8</span> | 51.6 | <span class="d ok">+0.2</span> |
| 14 | [[HyperGCL]] | 51.1 <span class="sd">±3.1</span> | 81.1 | <span class="d bad">−30.0</span> |
| 15 | [[AllSet]] | 50.8 <span class="sd">±2.5</span> | 51.2 | <span class="d ok">−0.4</span> |
| 16 | [[PhenomNN]] | 50.7 <span class="sd">±1.3</span> | 50.3 | <span class="d ok">+0.4</span> |
| 17 | [[HyperGCN]] | 48.9 <span class="sd">±1.6</span> | 49.3 | <span class="d ok">−0.4</span> |
| 18 | [[GGD]] | 43.9 <span class="sd">±10.3</span> | 73.2 | <span class="d bad">−29.3</span> |

```chart
type: bar
labels: [HypeBoy, SE-HSSL, TriCL, MaskGAE, GraphMAE2, VilLain, HGNN, UniGCN, UniGIN, ED-HNN, MLP, UniGCN2, HNHN, HyperGCL, AllSet, PhenomNN, HyperGCN, GGD]
series:
  - title: 우리
    data: [87.4, 85.7, 85.0, 76.1, 74.7, 64.7, 64.5, 61.1, 59.7, 59.2, 58.6, 52.2, 51.8, 51.1, 50.8, 50.7, 48.9, 43.9]
  - title: 논문
    data: [87.3, 85.6, 87.8, 76.5, 74.7, 64.4, 65.0, 60.0, 58.7, 58.9, 58.6, 51.9, 51.6, 81.1, 51.2, 50.3, 49.3, 73.2]
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

## Community detection — NMI

정식 결과 없음.

<small>미실행·보류: VilLain (pending), HyperGCL (pending), MaskGAE (pending), HyperGRL (pending)</small>

관련: [[논문 대조]] · [[데이터셋 비교]] · [[Home]]
<!-- AUTO:END -->

## 메모


