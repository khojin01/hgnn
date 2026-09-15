---
type: dataset
updated: 2026-09-15 13:09
tags: [hgnn/dataset]
---

<!-- AUTO:BEGIN -->
# Cora-CA

<span class="lgn">갱신 2026-09-15 13:09</span>

## Node classification <span class="m">Accuracy</span>

| # | 모델 | 우리 | 논문 | Δ |
|---:|---|---:|---:|---:|
| 1 | [[HypeBoy]] | <span class="v">67.0</span><span class="sd">±3.7</span> | 67.0 | <span class="d ok">+0.0</span> |
| 2 | [[GraphMAE2]] | <span class="v">64.0</span><span class="sd">±5.8</span> | 64.3 | <span class="d ok">−0.3</span> |
| 3 | [[SE-HSSL]] | <span class="v">64.0</span><span class="sd">±4.9</span> | 63.9 | <span class="d ok">+0.1</span> |
| 4 | [[TriCL]] | <span class="v">61.9</span><span class="sd">±5.8</span> | 63.4 | <span class="d ok">−1.5</span> |
| 5 | [[MaskGAE]] | <span class="v">56.5</span><span class="sd">±6.8</span> | 59.8 | <span class="d warn">−3.3</span> |
| 6 | [[PhenomNN]] | <span class="v">56.3</span><span class="sd">±7.5</span> | 56.2 | <span class="d ok">+0.1</span> |
| 7 | [[UniGCN2]] | <span class="v">53.1</span><span class="sd">±7.3</span> | 55.3 | <span class="d warn">−2.2</span> |
| 8 | [[AllSet]] | <span class="v">53.1</span><span class="sd">±6.4</span> | 53.6 | <span class="d ok">−0.5</span> |
| 9 | [[HNHN]] | <span class="v">51.0</span><span class="sd">±6.6</span> | 53.1 | <span class="d warn">−2.1</span> |
| 10 | [[UniGIN]] | <span class="v">47.6</span><span class="sd">±6.5</span> | 49.2 | <span class="d ok">−1.6</span> |
| 11 | [[UniGCN]] | <span class="v">47.2</span><span class="sd">±5.2</span> | 46.3 | <span class="d ok">+0.9</span> |
| 12 | [[HGNN]] | <span class="v">46.6</span><span class="sd">±7.9</span> | 44.3 | <span class="d warn">+2.3</span> |
| 13 | [[HyperGCN]] | <span class="v">45.0</span><span class="sd">±9.5</span> | 45.0 | <span class="d ok">+0.0</span> |
| 14 | [[HyperGRL]] | <span class="v">42.0</span><span class="sd">±6.7</span> | 41.8 | <span class="d ok">+0.2</span> |
| 15 | [[MLP]] | <span class="v">37.2</span><span class="sd">±4.3</span> | 36.0 | <span class="d ok">+1.2</span> |
| 16 | [[ED-HNN]] | <span class="v">36.5</span><span class="sd">±7.5</span> | 36.3 | <span class="d ok">+0.2</span> |
| 17 | [[VilLain]] | <span class="v">31.4</span><span class="sd">±4.1</span> | 31.4 | <span class="d ok">+0.0</span> |
| 18 | [[GGD]] | <span class="v">28.3</span><span class="sd">±4.6</span> | 32.2 | <span class="d warn">−3.9</span> |
| 19 | [[HyperGCL]] | <span class="v">16.3</span><span class="sd">±4.0</span> | 61.8 | <span class="d bad">−45.5</span> |

## Hyperedge prediction <span class="m">AUROC</span>

| # | 모델 | 우리 | 논문 | Δ |
|---:|---|---:|---:|---:|
| 1 | [[HypeBoy]] | <span class="v">87.4</span><span class="sd">±1.5</span> | 87.3 | <span class="d ok">+0.1</span> |
| 2 | [[SE-HSSL]] | <span class="v">85.7</span><span class="sd">±2.3</span> | 85.6 | <span class="d ok">+0.1</span> |
| 3 | [[TriCL]] | <span class="v">85.0</span><span class="sd">±2.0</span> | 87.8 | <span class="d warn">−2.8</span> |
| 4 | [[MaskGAE]] | <span class="v">76.1</span><span class="sd">±2.2</span> | 76.5 | <span class="d ok">−0.4</span> |
| 5 | [[GraphMAE2]] | <span class="v">74.7</span><span class="sd">±2.9</span> | 74.7 | <span class="d ok">+0.0</span> |
| 6 | [[VilLain]] | <span class="v">64.7</span><span class="sd">±2.5</span> | 64.4 | <span class="d ok">+0.3</span> |
| 7 | [[HGNN]] | <span class="v">64.5</span><span class="sd">±5.9</span> | 65.0 | <span class="d ok">−0.5</span> |
| 8 | [[UniGCN]] | <span class="v">61.1</span><span class="sd">±5.7</span> | 60.0 | <span class="d ok">+1.1</span> |
| 9 | [[UniGIN]] | <span class="v">59.7</span><span class="sd">±7.6</span> | 58.7 | <span class="d ok">+1.0</span> |
| 10 | [[ED-HNN]] | <span class="v">59.2</span><span class="sd">±3.2</span> | 58.9 | <span class="d ok">+0.3</span> |
| 11 | [[MLP]] | <span class="v">58.6</span><span class="sd">±2.9</span> | 58.6 | <span class="d ok">+0.0</span> |
| 12 | [[UniGCN2]] | <span class="v">52.2</span><span class="sd">±4.5</span> | 51.9 | <span class="d ok">+0.3</span> |
| 13 | [[HNHN]] | <span class="v">51.8</span><span class="sd">±1.8</span> | 51.6 | <span class="d ok">+0.2</span> |
| 14 | [[HyperGCL]] | <span class="v">51.1</span><span class="sd">±3.1</span> | 81.1 | <span class="d bad">−30.0</span> |
| 15 | [[AllSet]] | <span class="v">50.8</span><span class="sd">±2.5</span> | 51.2 | <span class="d ok">−0.4</span> |
| 16 | [[PhenomNN]] | <span class="v">50.7</span><span class="sd">±1.3</span> | 50.3 | <span class="d ok">+0.4</span> |
| 17 | [[HyperGCN]] | <span class="v">48.9</span><span class="sd">±1.6</span> | 49.3 | <span class="d ok">−0.4</span> |
| 18 | [[GGD]] | <span class="v">43.9</span><span class="sd">±10.3</span> | 73.2 | <span class="d bad">−29.3</span> |

<span class="lgn">미실행·보류: HyperGRL (unavailable: EP implementation missing)</span>

## Community detection <span class="m">NMI</span>

| # | 모델 | 우리 | 논문 | Δ |
|---:|---|---:|---:|---:|

<span class="lgn">미실행·보류: VilLain (pending), HyperGCL (pending), MaskGAE (pending), HyperGRL (pending)</span>

관련: [[논문 대조]] · [[Home]]
<!-- AUTO:END -->

## 메모


