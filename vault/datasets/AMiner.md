---
type: dataset
nc_models: 16
nc_best: GraphMAE2
nc_best_value: 34.8
hp_models: 16
hp_best: HypeBoy
hp_best_value: 89.7
updated: 2026-09-15 14:48
tags: [hgnn/dataset]
cssclasses: [table-wide, row-alt]
---

<!-- AUTO:BEGIN -->
# AMiner

<span class="lgn">갱신 2026-09-15 14:48</span>

## Node classification <span class="m">Accuracy</span>

| # | 모델 | 우리 | 논문 | Δ |
|---:|---|---:|---:|---:|
| 1 | [[GraphMAE2]] | <span class="v">34.8</span><span class="sd">±2.4</span> | 34.7 | <span class="d ok">+0.1</span> |
| 2 | [[SE-HSSL]] | <span class="v">34.7</span><span class="sd">±4.2</span> | 34.8 | <span class="d ok">−0.1</span> |
| 3 | [[HypeBoy]] | <span class="v">34.2</span><span class="sd">±3.0</span> | 34.6 | <span class="d ok">−0.4</span> |
| 4 | [[TriCL]] | <span class="v">33.6</span><span class="sd">±2.5</span> | 34.6 | <span class="d ok">−1.0</span> |
| 5 | [[MaskGAE]] | <span class="v">32.5</span><span class="sd">±1.7</span> | 33.8 | <span class="d ok">−1.3</span> |
| 6 | [[UniGCN2]] | <span class="v">32.2</span><span class="sd">±1.8</span> | 32.3 | <span class="d ok">−0.1</span> |
| 7 | [[HNHN]] | <span class="v">31.8</span><span class="sd">±2.0</span> | 32.1 | <span class="d ok">−0.3</span> |
| 8 | [[UniGIN]] | <span class="v">30.7</span><span class="sd">±1.2</span> | 30.8 | <span class="d ok">−0.1</span> |
| 9 | [[HGNN]] | <span class="v">30.5</span><span class="sd">±1.6</span> | 29.7 | <span class="d ok">+0.8</span> |
| 10 | [[AllSet]] | <span class="v">29.6</span><span class="sd">±3.5</span> | 29.8 | <span class="d ok">−0.2</span> |
| 11 | [[UniGCN]] | <span class="v">29.6</span><span class="sd">±1.5</span> | 29.8 | <span class="d ok">−0.2</span> |
| 12 | [[ED-HNN]] | <span class="v">26.6</span><span class="sd">±3.0</span> | 27.1 | <span class="d ok">−0.5</span> |
| 13 | [[HyperGCN]] | <span class="v">26.4</span><span class="sd">±2.9</span> | 26.8 | <span class="d ok">−0.4</span> |
| 14 | [[MLP]] | <span class="v">22.4</span><span class="sd">±1.4</span> | 22.7 | <span class="d ok">−0.3</span> |
| 15 | [[VilLain]] | <span class="v">19.9</span><span class="sd">±1.2</span> | 19.9 | <span class="d ok">+0.0</span> |
| 16 | [[GGD]] | <span class="v">16.6</span><span class="sd">±2.7</span> | 31.5 | <span class="d bad">−14.9</span> |

<span class="lgn">미실행·보류: HyperGRL (OOM), PhenomNN (OOM), HyperGCL (pending)</span>

```chart
type: bar
labels: [GraphMAE2, SE-HSSL, HypeBoy, TriCL, MaskGAE, UniGCN2, HNHN, UniGIN, HGNN, AllSet, UniGCN, ED-HNN, HyperGCN, MLP, VilLain, GGD]
series:
  - title: 우리
    data: [34.8, 34.7, 34.2, 33.6, 32.5, 32.2, 31.8, 30.7, 30.5, 29.6, 29.6, 26.6, 26.4, 22.4, 19.9, 16.6]
  - title: 논문
    data: [34.7, 34.8, 34.6, 34.6, 33.8, 32.3, 32.1, 30.8, 29.7, 29.8, 29.8, 27.1, 26.8, 22.7, 19.9, 31.5]
tension: 0.2
width: 100%
labelColors: false
fill: false
beginAtZero: false
legend: true
stacked: false
height: 260px
```


## Hyperedge prediction <span class="m">AUROC</span>

| # | 모델 | 우리 | 논문 | Δ |
|---:|---|---:|---:|---:|
| 1 | [[HypeBoy]] | <span class="v">89.7</span><span class="sd">±0.6</span> | 89.7 | <span class="d ok">+0.0</span> |
| 2 | [[MaskGAE]] | <span class="v">87.6</span><span class="sd">±0.9</span> | 87.6 | <span class="d ok">+0.0</span> |
| 3 | [[SE-HSSL]] | <span class="v">87.4</span><span class="sd">±0.6</span> | 87.5 | <span class="d ok">−0.1</span> |
| 4 | [[TriCL]] | <span class="v">86.0</span><span class="sd">±0.9</span> | 90.4 | <span class="d warn">−4.4</span> |
| 5 | [[MLP]] | <span class="v">82.3</span><span class="sd">±0.9</span> | 82.3 | <span class="d ok">+0.0</span> |
| 6 | [[GraphMAE2]] | <span class="v">78.1</span><span class="sd">±0.9</span> | 78.1 | <span class="d ok">+0.0</span> |
| 7 | [[HGNN]] | <span class="v">69.1</span><span class="sd">±1.6</span> | 69.6 | <span class="d ok">−0.5</span> |
| 8 | [[UniGIN]] | <span class="v">68.9</span><span class="sd">±1.2</span> | 69.1 | <span class="d ok">−0.2</span> |
| 9 | [[UniGCN]] | <span class="v">68.5</span><span class="sd">±1.9</span> | 69.0 | <span class="d ok">−0.5</span> |
| 10 | [[VilLain]] | <span class="v">61.9</span><span class="sd">±0.7</span> | 62.7 | <span class="d ok">−0.8</span> |
| 11 | [[ED-HNN]] | <span class="v">56.8</span><span class="sd">±4.5</span> | 56.0 | <span class="d ok">+0.8</span> |
| 12 | [[GGD]] | <span class="v">50.7</span><span class="sd">±8.3</span> | 84.9 | <span class="d bad">−34.2</span> |
| 13 | [[HyperGCN]] | <span class="v">50.6</span><span class="sd">±2.6</span> | 50.8 | <span class="d ok">−0.2</span> |
| 14 | [[AllSet]] | <span class="v">50.5</span><span class="sd">±1.3</span> | 51.0 | <span class="d ok">−0.5</span> |
| 15 | [[HNHN]] | <span class="v">48.1</span><span class="sd">±1.3</span> | 48.1 | <span class="d ok">+0.0</span> |
| 16 | [[UniGCN2]] | <span class="v">46.2</span><span class="sd">±4.5</span> | 45.9 | <span class="d ok">+0.3</span> |

<span class="lgn">미실행·보류: PhenomNN (OOM), HyperGCL (pending), HyperGRL (unavailable: EP implementation missing)</span>

```chart
type: bar
labels: [HypeBoy, MaskGAE, SE-HSSL, TriCL, MLP, GraphMAE2, HGNN, UniGIN, UniGCN, VilLain, ED-HNN, GGD, HyperGCN, AllSet, HNHN, UniGCN2]
series:
  - title: 우리
    data: [89.7, 87.6, 87.4, 86.0, 82.3, 78.1, 69.1, 68.9, 68.5, 61.9, 56.8, 50.7, 50.6, 50.5, 48.1, 46.2]
  - title: 논문
    data: [89.7, 87.6, 87.5, 90.4, 82.3, 78.1, 69.6, 69.1, 69.0, 62.7, 56.0, 84.9, 50.8, 51.0, 48.1, 45.9]
tension: 0.2
width: 100%
labelColors: false
fill: false
beginAtZero: false
legend: true
stacked: false
height: 260px
```


관련: [[논문 대조]] · [[데이터셋 비교]] · [[Home]]
<!-- AUTO:END -->

## 메모


