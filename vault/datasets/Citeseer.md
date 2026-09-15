---
type: dataset
updated: 2026-09-15 13:09
tags: [hgnn/dataset]
---

<!-- AUTO:BEGIN -->
# Citeseer

<span class="lgn">갱신 2026-09-15 13:09</span>

## Node classification <span class="m">Accuracy</span>

| # | 모델 | 우리 | 논문 | Δ |
|---:|---|---:|---:|---:|
| 1 | [[HypeBoy]] | <span class="v">57.6</span><span class="sd">±10.5</span> | 57.7 | <span class="d ok">−0.1</span> |
| 2 | [[SE-HSSL]] | <span class="v">57.0</span><span class="sd">±8.3</span> | 57.0 | <span class="d ok">+0.0</span> |
| 3 | [[MaskGAE]] | <span class="v">52.7</span><span class="sd">±10.4</span> | 53.2 | <span class="d ok">−0.5</span> |
| 4 | [[TriCL]] | <span class="v">52.7</span><span class="sd">±13.9</span> | 53.0 | <span class="d ok">−0.3</span> |
| 5 | [[GraphMAE2]] | <span class="v">51.7</span><span class="sd">±12.9</span> | 51.7 | <span class="d ok">+0.0</span> |
| 6 | [[PhenomNN]] | <span class="v">45.1</span><span class="sd">±11.7</span> | 42.2 | <span class="d warn">+2.9</span> |
| 7 | [[HNHN]] | <span class="v">43.3</span><span class="sd">±8.0</span> | 44.2 | <span class="d ok">−0.9</span> |
| 8 | [[UniGCN2]] | <span class="v">41.5</span><span class="sd">±9.2</span> | 39.6 | <span class="d ok">+1.9</span> |
| 9 | [[AllSet]] | <span class="v">41.0</span><span class="sd">±8.3</span> | 41.1 | <span class="d ok">−0.1</span> |
| 10 | [[UniGIN]] | <span class="v">40.3</span><span class="sd">±9.4</span> | 41.4 | <span class="d ok">−1.1</span> |
| 11 | [[HGNN]] | <span class="v">38.1</span><span class="sd">±10.7</span> | 38.1 | <span class="d ok">−0.0</span> |
| 12 | [[UniGCN]] | <span class="v">37.7</span><span class="sd">±8.6</span> | 39.8 | <span class="d warn">−2.1</span> |
| 13 | [[ED-HNN]] | <span class="v">34.0</span><span class="sd">±8.8</span> | 32.9 | <span class="d ok">+1.1</span> |
| 14 | [[HyperGCN]] | <span class="v">33.7</span><span class="sd">±7.3</span> | 33.8 | <span class="d ok">−0.1</span> |
| 15 | [[MLP]] | <span class="v">32.4</span><span class="sd">±8.1</span> | 32.4 | <span class="d ok">+0.0</span> |
| 16 | [[VilLain]] | <span class="v">28.5</span><span class="sd">±8.2</span> | 33.6 | <span class="d bad">−5.1</span> |
| 17 | [[GGD]] | <span class="v">27.5</span><span class="sd">±6.4</span> | 34.0 | <span class="d bad">−6.5</span> |
| 18 | [[HyperGCL]] | <span class="v">18.5</span><span class="sd">±3.5</span> | 43.4 | <span class="d bad">−24.9</span> |

<span class="lgn">미실행·보류: HyperGRL (OOM)</span>

## Hyperedge prediction <span class="m">AUROC</span>

| # | 모델 | 우리 | 논문 | Δ |
|---:|---|---:|---:|---:|
| 1 | [[SE-HSSL]] | <span class="v">90.6</span><span class="sd">±1.1</span> | 90.5 | <span class="d ok">+0.1</span> |
| 2 | [[TriCL]] | <span class="v">89.1</span><span class="sd">±1.3</span> | 90.5 | <span class="d ok">−1.4</span> |
| 3 | [[MaskGAE]] | <span class="v">86.7</span><span class="sd">±1.7</span> | 86.7 | <span class="d ok">+0.0</span> |
| 4 | [[HypeBoy]] | <span class="v">86.4</span><span class="sd">±2.1</span> | 86.4 | <span class="d ok">+0.0</span> |
| 5 | [[GraphMAE2]] | <span class="v">78.1</span><span class="sd">±2.4</span> | 78.2 | <span class="d ok">−0.1</span> |
| 6 | [[MLP]] | <span class="v">65.6</span><span class="sd">±2.0</span> | 65.6 | <span class="d ok">+0.0</span> |
| 7 | [[UniGCN2]] | <span class="v">60.3</span><span class="sd">±2.1</span> | 60.2 | <span class="d ok">+0.1</span> |
| 8 | [[ED-HNN]] | <span class="v">58.1</span><span class="sd">±2.8</span> | 58.0 | <span class="d ok">+0.1</span> |
| 9 | [[VilLain]] | <span class="v">57.2</span><span class="sd">±2.4</span> | 58.3 | <span class="d ok">−1.1</span> |
| 10 | [[HyperGCN]] | <span class="v">54.9</span><span class="sd">±2.1</span> | 54.9 | <span class="d ok">+0.0</span> |
| 11 | [[PhenomNN]] | <span class="v">54.3</span><span class="sd">±2.2</span> | 54.5 | <span class="d ok">−0.2</span> |
| 12 | [[HGNN]] | <span class="v">54.2</span><span class="sd">±3.7</span> | 54.8 | <span class="d ok">−0.6</span> |
| 13 | [[UniGCN]] | <span class="v">53.7</span><span class="sd">±5.2</span> | 54.7 | <span class="d ok">−1.0</span> |
| 14 | [[HNHN]] | <span class="v">53.7</span><span class="sd">±2.5</span> | 53.7 | <span class="d ok">+0.0</span> |
| 15 | [[UniGIN]] | <span class="v">53.3</span><span class="sd">±3.4</span> | 52.9 | <span class="d ok">+0.4</span> |
| 16 | [[GGD]] | <span class="v">52.9</span><span class="sd">±4.2</span> | 72.2 | <span class="d bad">−19.3</span> |
| 17 | [[HyperGCL]] | <span class="v">51.9</span><span class="sd">±2.9</span> | 73.9 | <span class="d bad">−22.0</span> |
| 18 | [[AllSet]] | <span class="v">50.7</span><span class="sd">±3.3</span> | 51.8 | <span class="d ok">−1.1</span> |

<span class="lgn">미실행·보류: HyperGRL (unavailable: EP implementation missing)</span>

관련: [[논문 대조]] · [[Home]]
<!-- AUTO:END -->

## 메모


