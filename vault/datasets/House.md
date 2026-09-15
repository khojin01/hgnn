---
type: dataset
nc_models: 19
nc_best: MLP
nc_best_value: 73.1
hp_models: 18
hp_best: MaskGAE
hp_best_value: 88.2
updated: 2026-09-15 14:48
tags: [hgnn/dataset]
cssclasses: [table-wide, row-alt]
---

<!-- AUTO:BEGIN -->
# House

<span class="lgn">갱신 2026-09-15 14:48</span>

## Node classification <span class="m">Accuracy</span>

| # | 모델 | 우리 | 논문 | Δ |
|---:|---|---:|---:|---:|
| 1 | [[MLP]] | <span class="v">73.1</span><span class="sd">±3.2</span> | 73.1 | <span class="d ok">+0.0</span> |
| 2 | [[ED-HNN]] | <span class="v">71.7</span><span class="sd">±4.8</span> | 71.0 | <span class="d ok">+0.7</span> |
| 3 | [[PhenomNN]] | <span class="v">69.4</span><span class="sd">±7.0</span> | 69.4 | <span class="d ok">+0.0</span> |
| 4 | [[HypeBoy]] | <span class="v">68.7</span><span class="sd">±6.0</span> | 67.7 | <span class="d ok">+1.0</span> |
| 5 | [[TriCL]] | <span class="v">63.5</span><span class="sd">±7.4</span> | 65.2 | <span class="d ok">−1.7</span> |
| 6 | [[SE-HSSL]] | <span class="v">60.7</span><span class="sd">±7.0</span> | 48.0 | <span class="d bad">+12.7</span> |
| 7 | [[UniGCN2]] | <span class="v">58.7</span><span class="sd">±10.1</span> | 58.8 | <span class="d ok">−0.1</span> |
| 8 | [[HNHN]] | <span class="v">56.7</span><span class="sd">±4.0</span> | 56.7 | <span class="d ok">+0.0</span> |
| 9 | [[HyperGCL]] | <span class="v">54.6</span><span class="sd">±5.5</span> | 63.7 | <span class="d bad">−9.1</span> |
| 10 | [[MaskGAE]] | <span class="v">52.2</span><span class="sd">±3.0</span> | 53.0 | <span class="d ok">−0.8</span> |
| 11 | [[GraphMAE2]] | <span class="v">52.0</span><span class="sd">±3.2</span> | 52.4 | <span class="d ok">−0.4</span> |
| 12 | [[HGNN]] | <span class="v">51.9</span><span class="sd">±4.7</span> | 51.9 | <span class="d ok">+0.0</span> |
| 13 | [[UniGCN]] | <span class="v">51.5</span><span class="sd">±2.7</span> | 51.7 | <span class="d ok">−0.2</span> |
| 14 | [[UniGIN]] | <span class="v">51.0</span><span class="sd">±2.3</span> | 50.8 | <span class="d ok">+0.2</span> |
| 15 | [[HyperGRL]] | <span class="v">50.6</span><span class="sd">±1.8</span> | 50.4 | <span class="d ok">+0.2</span> |
| 16 | [[AllSet]] | <span class="v">50.2</span><span class="sd">±2.8</span> | 50.3 | <span class="d ok">−0.1</span> |
| 17 | [[GGD]] | <span class="v">49.9</span><span class="sd">±1.3</span> | 50.6 | <span class="d ok">−0.7</span> |
| 18 | [[VilLain]] | <span class="v">49.3</span><span class="sd">±1.5</span> | 50.6 | <span class="d ok">−1.3</span> |
| 19 | [[HyperGCN]] | <span class="v">48.2</span><span class="sd">±0.9</span> | 48.2 | <span class="d ok">+0.0</span> |

```chart
type: bar
labels: [MLP, ED-HNN, PhenomNN, HypeBoy, TriCL, SE-HSSL, UniGCN2, HNHN, HyperGCL, MaskGAE, GraphMAE2, HGNN, UniGCN, UniGIN, HyperGRL, AllSet, GGD, VilLain, HyperGCN]
series:
  - title: 우리
    data: [73.1, 71.7, 69.4, 68.7, 63.5, 60.7, 58.7, 56.7, 54.6, 52.2, 52.0, 51.9, 51.5, 51.0, 50.6, 50.2, 49.9, 49.3, 48.2]
  - title: 논문
    data: [73.1, 71.0, 69.4, 67.7, 65.2, 48.0, 58.8, 56.7, 63.7, 53.0, 52.4, 51.9, 51.7, 50.8, 50.4, 50.3, 50.6, 50.6, 48.2]
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
| 1 | [[MaskGAE]] | <span class="v">88.2</span><span class="sd">±3.6</span> | 88.0 | <span class="d ok">+0.2</span> |
| 2 | [[HyperGCN]] | <span class="v">87.7</span><span class="sd">±2.5</span> | 87.7 | <span class="d ok">+0.0</span> |
| 3 | [[HypeBoy]] | <span class="v">87.0</span><span class="sd">±3.0</span> | 87.2 | <span class="d ok">−0.2</span> |
| 4 | [[TriCL]] | <span class="v">84.6</span><span class="sd">±3.5</span> | 90.0 | <span class="d bad">−5.4</span> |
| 5 | [[SE-HSSL]] | <span class="v">79.9</span><span class="sd">±3.1</span> | 80.4 | <span class="d ok">−0.5</span> |
| 6 | [[VilLain]] | <span class="v">77.5</span><span class="sd">±5.6</span> | 77.2 | <span class="d ok">+0.3</span> |
| 7 | [[GraphMAE2]] | <span class="v">71.8</span><span class="sd">±5.6</span> | 71.6 | <span class="d ok">+0.2</span> |
| 8 | [[HNHN]] | <span class="v">69.7</span><span class="sd">±5.6</span> | 69.7 | <span class="d ok">+0.0</span> |
| 9 | [[HyperGCL]] | <span class="v">63.3</span><span class="sd">±9.5</span> | 76.3 | <span class="d bad">−13.0</span> |
| 10 | [[MLP]] | <span class="v">54.8</span><span class="sd">±5.4</span> | 54.8 | <span class="d ok">+0.0</span> |
| 11 | [[AllSet]] | <span class="v">53.5</span><span class="sd">±5.1</span> | 53.5 | <span class="d ok">+0.0</span> |
| 12 | [[PhenomNN]] | <span class="v">50.6</span><span class="sd">±1.2</span> | 50.8 | <span class="d ok">−0.2</span> |
| 13 | [[ED-HNN]] | <span class="v">50.3</span><span class="sd">±0.9</span> | 50.6 | <span class="d ok">−0.3</span> |
| 14 | [[UniGCN]] | <span class="v">50.0</span><span class="sd">±0.0</span> | 50.0 | <span class="d ok">+0.0</span> |
| 15 | [[UniGIN]] | <span class="v">50.0</span><span class="sd">±0.0</span> | 50.0 | <span class="d ok">+0.0</span> |
| 16 | [[UniGCN2]] | <span class="v">50.0</span><span class="sd">±0.0</span> | 50.0 | <span class="d ok">+0.0</span> |
| 17 | [[HGNN]] | <span class="v">50.0</span><span class="sd">±0.0</span> | 50.4 | <span class="d ok">−0.4</span> |
| 18 | [[GGD]] | <span class="v">50.0</span><span class="sd">±0.0</span> | 87.9 | <span class="d bad">−37.9</span> |

<span class="lgn">미실행·보류: HyperGRL (unavailable: EP implementation missing)</span>

```chart
type: bar
labels: [MaskGAE, HyperGCN, HypeBoy, TriCL, SE-HSSL, VilLain, GraphMAE2, HNHN, HyperGCL, MLP, AllSet, PhenomNN, ED-HNN, UniGCN, UniGIN, UniGCN2, HGNN, GGD]
series:
  - title: 우리
    data: [88.2, 87.7, 87.0, 84.6, 79.9, 77.5, 71.8, 69.7, 63.3, 54.8, 53.5, 50.6, 50.3, 50.0, 50.0, 50.0, 50.0, 50.0]
  - title: 논문
    data: [88.0, 87.7, 87.2, 90.0, 80.4, 77.2, 71.6, 69.7, 76.3, 54.8, 53.5, 50.8, 50.6, 50.0, 50.0, 50.0, 50.4, 87.9]
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


