---
type: dataset
updated: 2026-09-15 13:09
tags: [hgnn/dataset]
---

<!-- AUTO:BEGIN -->
# House

<span class="lgn">갱신 2026-09-15 13:09</span>

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

관련: [[논문 대조]] · [[Home]]
<!-- AUTO:END -->

## 메모


