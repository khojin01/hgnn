---
type: dataset
updated: 2026-09-15 13:09
tags: [hgnn/dataset]
---

<!-- AUTO:BEGIN -->
# AMiner

<span class="lgn">갱신 2026-09-15 13:09</span>

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

관련: [[논문 대조]] · [[Home]]
<!-- AUTO:END -->

## 메모


