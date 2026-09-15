---
type: dataset
nc_models: 19
nc_best: MLP
hp_models: 18
hp_best: MaskGAE
updated: 2026-09-15 15:36
tags: [hgnn/dataset]
---

<!-- AUTO:BEGIN -->
# House

<small>갱신 2026-09-15 15:36</small>

## Node classification — Accuracy

| # | 모델 | 우리 | 논문 | Δ |
|---:|---|---:|---:|---:|
| 1 | [[MLP]] | 73.1 <span class="sd">±3.2</span> | 73.1 | <span class="d ok">+0.0</span> |
| 2 | [[ED-HNN]] | 71.7 <span class="sd">±4.8</span> | 71.0 | <span class="d ok">+0.7</span> |
| 3 | [[PhenomNN]] | 69.4 <span class="sd">±7.0</span> | 69.4 | <span class="d ok">+0.0</span> |
| 4 | [[HypeBoy]] | 68.7 <span class="sd">±6.0</span> | 67.7 | <span class="d ok">+1.0</span> |
| 5 | [[TriCL]] | 63.5 <span class="sd">±7.4</span> | 65.2 | <span class="d ok">−1.7</span> |
| 6 | [[SE-HSSL]] | 60.7 <span class="sd">±7.0</span> | 48.0 | <span class="d bad">+12.7</span> |
| 7 | [[UniGCN2]] | 58.7 <span class="sd">±10.1</span> | 58.8 | <span class="d ok">−0.1</span> |
| 8 | [[HNHN]] | 56.7 <span class="sd">±4.0</span> | 56.7 | <span class="d ok">+0.0</span> |
| 9 | [[HyperGCL]] | 54.6 <span class="sd">±5.5</span> | 63.7 | <span class="d bad">−9.1</span> |
| 10 | [[MaskGAE]] | 52.2 <span class="sd">±3.0</span> | 53.0 | <span class="d ok">−0.8</span> |
| 11 | [[GraphMAE2]] | 52.0 <span class="sd">±3.2</span> | 52.4 | <span class="d ok">−0.4</span> |
| 12 | [[HGNN]] | 51.9 <span class="sd">±4.7</span> | 51.9 | <span class="d ok">+0.0</span> |
| 13 | [[UniGCN]] | 51.5 <span class="sd">±2.7</span> | 51.7 | <span class="d ok">−0.2</span> |
| 14 | [[UniGIN]] | 51.0 <span class="sd">±2.3</span> | 50.8 | <span class="d ok">+0.2</span> |
| 15 | [[HyperGRL]] | 50.6 <span class="sd">±1.8</span> | 50.4 | <span class="d ok">+0.2</span> |
| 16 | [[AllSet]] | 50.2 <span class="sd">±2.8</span> | 50.3 | <span class="d ok">−0.1</span> |
| 17 | [[GGD]] | 49.9 <span class="sd">±1.3</span> | 50.6 | <span class="d ok">−0.7</span> |
| 18 | [[VilLain]] | 49.3 <span class="sd">±1.5</span> | 50.6 | <span class="d ok">−1.3</span> |
| 19 | [[HyperGCN]] | 48.2 <span class="sd">±0.9</span> | 48.2 | <span class="d ok">+0.0</span> |

## Hyperedge prediction — AUROC

| # | 모델 | 우리 | 논문 | Δ |
|---:|---|---:|---:|---:|
| 1 | [[MaskGAE]] | 88.2 <span class="sd">±3.6</span> | 88.0 | <span class="d ok">+0.2</span> |
| 2 | [[HyperGCN]] | 87.7 <span class="sd">±2.5</span> | 87.7 | <span class="d ok">+0.0</span> |
| 3 | [[HypeBoy]] | 87.0 <span class="sd">±3.0</span> | 87.2 | <span class="d ok">−0.2</span> |
| 4 | [[TriCL]] | 84.6 <span class="sd">±3.5</span> | 90.0 | <span class="d bad">−5.4</span> |
| 5 | [[SE-HSSL]] | 79.9 <span class="sd">±3.1</span> | 80.4 | <span class="d ok">−0.5</span> |
| 6 | [[VilLain]] | 77.5 <span class="sd">±5.6</span> | 77.2 | <span class="d ok">+0.3</span> |
| 7 | [[GraphMAE2]] | 71.8 <span class="sd">±5.6</span> | 71.6 | <span class="d ok">+0.2</span> |
| 8 | [[HNHN]] | 69.7 <span class="sd">±5.6</span> | 69.7 | <span class="d ok">+0.0</span> |
| 9 | [[HyperGCL]] | 63.3 <span class="sd">±9.5</span> | 76.3 | <span class="d bad">−13.0</span> |
| 10 | [[MLP]] | 54.8 <span class="sd">±5.4</span> | 54.8 | <span class="d ok">+0.0</span> |
| 11 | [[AllSet]] | 53.5 <span class="sd">±5.1</span> | 53.5 | <span class="d ok">+0.0</span> |
| 12 | [[PhenomNN]] | 50.6 <span class="sd">±1.2</span> | 50.8 | <span class="d ok">−0.2</span> |
| 13 | [[ED-HNN]] | 50.3 <span class="sd">±0.9</span> | 50.6 | <span class="d ok">−0.3</span> |
| 14 | [[UniGCN]] | 50.0 <span class="sd">±0.0</span> | 50.0 | <span class="d ok">+0.0</span> |
| 15 | [[UniGIN]] | 50.0 <span class="sd">±0.0</span> | 50.0 | <span class="d ok">+0.0</span> |
| 16 | [[UniGCN2]] | 50.0 <span class="sd">±0.0</span> | 50.0 | <span class="d ok">+0.0</span> |
| 17 | [[HGNN]] | 50.0 <span class="sd">±0.0</span> | 50.4 | <span class="d ok">−0.4</span> |
| 18 | [[GGD]] | 50.0 <span class="sd">±0.0</span> | 87.9 | <span class="d bad">−37.9</span> |

<small>미실행·보류: HyperGRL (unavailable: EP implementation missing)</small>

<!-- AUTO:END -->

## 메모


