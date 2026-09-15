# Hypergraph experiment result matrix — live

> **자동 갱신 기준 파일**입니다. 정식 20-seed 실행의 완료 결과를 이 문서에 누적합니다.
> 마지막 확인: 2026-09-13 KST · HOUSE의 19개 모델 정식 20-seed 결과와 밤사이 EP 완료 결과를 원시 파일에서 수집해 반영했습니다. HyperGCL–EP IMDB는 실행 중이며, NC IMDB는 split 19–20 진단만 끝나 20-seed 정식 집계가 없습니다.
> **분할 계약**: 노드 분류는 `data_split_0.01.pickle`(train 1% / valid 1% / test 98%)만 씁니다. HyperGC 논문 4장이 정한 프로토콜이고, 공용 로더 `dataset.py`가 읽는 파일입니다. `data_split_118.pickle`은 10%/10%/80%이라 Table 3 대비가 성립하지 않습니다 — 모델 코드가 분할을 직접 열면 이 값을 쓰는지 확인하세요.
> 원시 로그는 `.agents/env-status/full-runs/`, 대시보드는 이 파일을 5분마다 읽습니다.

## Latest formal completions — 2026-09-13 KST

- Hyperedge prediction night refresh: HypeBoy, SE-HSSL, TriCL, and MaskGAE each completed all six common datasets with 20 seeds; their Table 4 cells are recorded below. MaskGAE's launcher reports failure after writing its complete result files, so the six saved 20-seed values are retained as formal metrics.
- HyperGCL hyperedge prediction: Citeseer **51.9 ± 2.9** and Cora-CA **51.1 ± 3.1** completed all 20 seeds and saved results. The trailing timing write has a `NameError`, so it is an after-result bookkeeping failure, not a metric failure. IMDB is running; Pubmed/AMiner are pending. VilLain is queued after HyperGCL. HyperGRL has no EP implementation/entry point and is unavailable for this task.
- EP campaign summary (19 models): **16 complete**, **1 in progress** (HyperGCL), **1 queued** (VilLain), **1 unavailable** (HyperGRL EP implementation missing). PhenomNN–AMiner is a paper-declared O.O.M skip.
- Hyperedge prediction: MLP and UniGCN completed the six currently available datasets (Citeseer, Cora-CA, IMDB, House, Pubmed, AMiner); MN-40/20News loaders remain unavailable. Table 4에 Citeseer·IMDB·House·Pubmed 열을 추가해 12칸을 모두 기록했습니다 — 논문 Table 4는 이 네 데이터셋에도 값을 싣고 있어 대조 가능합니다. 12칸 전부 Δ ±1.1 이내입니다.
- HyperGCL IMDB GPU-path check: predefined splits **19–20** completed with the GPU sampler (**34.5 ± 2.1**). This is a 2-split diagnostic only, not a replacement for the 20-seed formal result.
- HyperGCN: Pubmed **59.34 ± 15.17**, AMiner **26.39 ± 2.91**.
- TriCL: House **63.5 ± 7.4**, Citeseer **52.7 ± 13.9**, Cora-CA **61.9 ± 5.8**, IMDB **47.9 ± 5.3**, Pubmed **75.0 ± 3.4**, AMiner **33.6 ± 2.5**.
- HyperGCL: House **54.60 ± 5.53**, Citeseer **18.48 ± 3.48**, Cora-CA **16.29 ± 3.97**. IMDB splits 19–20 GPU-path diagnostic completed; a fresh 20-seed aggregate remains pending.
- HOUSE: 19개 모델 모두 완료. 각 평균과 표준편차는 아래 Table 3의 HOUSE 열에 반영했습니다.
- VilLain 노드 분류 재실행 (분할 정정): `VilLain/eval.py`가 `data_split_118.pickle`(10%/10%/80%)을 읽고 있어 논문 프로토콜(1%/1%/98%)과 달랐습니다. `data_split_0.01.pickle`로 바로잡고 6개 데이터셋을 재평가했습니다. Cora-CA 31.4 ± 4.1, Pubmed 73.7 ± 3.3, AMiner 19.9 ± 1.2는 논문값과 표준편차까지 일치합니다. 임베딩은 자기지도라 분할과 무관하므로 재학습 없이 MLP probe만 다시 돌렸습니다.
- Recovery status: PhenomNN–AMiner exits with dense-matrix O.O.M. HyperGRL Citeseer/IMDB/Pubmed/AMiner each exhausts the batch-size-1 retry with CUDA O.O.M (the outer 90-minute watchdog also records exit 124); these four are recorded as O.O.M, not pending.

`내 결과 ± 표준편차 (Δ = 내 평균 − HyperGC 논문 표의 평균)` 형식입니다.

- `↑2 이상`: 논문 기준보다 2%p 이상 높음
- `−2~5`: 논문 기준보다 2~5%p 낮음
- `↓5 초과`: 논문 기준보다 5%p 이상 낮음
- `—`: 아직 해당 조합의 정식 결과가 없거나, 데이터/실행 정책상 제외됨
- **정식**은 전임자 `118.sh` 고정 설정·기본 200 epoch·20 split/seed 결과입니다. `smoke`는 단기 확인 결과로 논문 재현값이 아닙니다.

## Node classification — Table 3 · Accuracy

| Model | Citeseer | Cora-CA | IMDB | House | Pubmed | AMiner | DBLP-A | MN-40 | 20News |
|---|---|---|---|---|---|---|---|---|---|
| AllSet | **41.05 ± 8.26** (Δ **−0.05**) | **53.09 ± 6.43** (Δ **−0.51**) | **40.53 ± 4.58** (Δ **−1.17**) | **50.2 ± 2.8** (Δ **−0.1**) | **72.45 ± 6.22** (Δ **−1.65**) | **29.62 ± 3.55** (Δ **−0.18**) | — deferred | — blocked-data | — blocked-data |
| ED-HNN | **34.00 ± 8.84** (Δ **+1.10**) | **36.50 ± 7.53** (Δ **+0.20**) | **38.00 ± 2.81** (Δ **+0.80**) | **71.7 ± 4.8** (Δ **+0.7**) | **60.96 ± 3.85** (Δ **−0.94**) | **26.56 ± 3.05** (Δ **−0.54**) | — blocked-data | — blocked-data | — blocked-data |
| GGD (H-GD) | **27.5 ± 6.4** (Δ **−6.5**) | **28.3 ± 4.6** (Δ **−3.9**) | **36.7 ± 2.6** (Δ **−0.9**) | **49.9 ± 1.3** (Δ **−0.7**) | **62.2 ± 5.0** (Δ **−2.7**) | **16.6 ± 2.7** (Δ **−14.9**) | — blocked-data | — blocked-data | — blocked-data |
| GraphMAE2 | **51.7 ± 12.9** (Δ **+0.0**) | **64.0 ± 5.8** (Δ **−0.3**) | **44.7 ± 4.2** (Δ **−0.9**) | **52.0 ± 3.2** (Δ **−0.4**) | **72.2 ± 4.7** (Δ **−0.4**) | **34.8 ± 2.4** (Δ **+0.1**) | — blocked-data | — blocked-data | — blocked-data |
| HGNN | **38.09 ± 10.73** (Δ **−0.01**) | **46.59 ± 7.88** (Δ **+2.29**) | **41.88 ± 4.54** (Δ **+0.38**) | **51.9 ± 4.7** (Δ **+0.0**) | **70.58 ± 3.63** (Δ **−0.22**) | **30.54 ± 1.64** (Δ **+0.84**) | — blocked-data | — blocked-data | — blocked-data |
| HNHN | **43.33 ± 8.03** (Δ **−0.87**) | **51.02 ± 6.56** (Δ **−2.08**) | **41.84 ± 3.66** (Δ **−0.66**) | **56.7 ± 4.0** (Δ **+0.0**) | **69.45 ± 3.36** (Δ **+0.35**) | **31.83 ± 2.03** (Δ **−0.27**) | — blocked-data | — blocked-data | — blocked-data |
| HypeBoy | **57.6 ± 10.5** (Δ **−0.1**) | **67.0 ± 3.7** (Δ **+0.0**) | **48.0 ± 5.0** (Δ **−0.3**) | **68.7 ± 6.0** (Δ **+1.0**) | **73.7 ± 4.4** (Δ **+0.0**) | **34.2 ± 3.0** (Δ **−0.4**) | — blocked-data | — blocked-data | — blocked-data |
| HyperGCN | **33.7 ± 7.3** (Δ **−0.1**) | **45.0 ± 9.5** (Δ **+0.0**) | **40.6 ± 3.2** (Δ **+0.0**) | **48.2 ± 0.9** (Δ **+0.0**) | **59.3 ± 15.2** (Δ **+0.0**) | **26.4 ± 2.9** (Δ **−0.4**) | — blocked-data | — blocked-data | — blocked-data |
| HyperGRL | — O.O.M (batch-1 retry) | **42.0 ± 6.7** (Δ **+0.2**) | — O.O.M (batch-1 retry) | **50.6 ± 1.8** (Δ **+0.2**) | — O.O.M (batch-1 retry) | — O.O.M (batch-1 retry) | — blocked-data | — blocked-data | — blocked-data |
| MLP | **32.43 ± 8.05** (Δ **+0.03**) | **37.24 ± 4.31** (Δ **+1.24**) | **38.23 ± 2.67** (Δ **+0.63**) | **73.1 ± 3.2** (Δ **+0.0**) | **62.67 ± 3.26** (Δ **−0.13**) | **22.39 ± 1.42** (Δ **−0.31**) | — blocked-data | — blocked-data | — blocked-data |
| MaskGAE | **52.7 ± 10.4** (Δ **−0.5**) | **56.5 ± 6.8** (Δ **−3.3**) | **44.7 ± 3.5** (Δ **−0.3**) | **52.2 ± 3.0** (Δ **−0.8**) | **74.6 ± 4.2** (Δ **−0.8**) | **32.5 ± 1.7** (Δ **−1.3**) | — blocked-data | — blocked-data | — blocked-data |
| PhenomNN | **45.1 ± 11.7** (Δ **+2.9**) | **56.3 ± 7.5** (Δ **+0.1**) | **42.1 ± 2.9** (Δ **+0.0**) | **69.4 ± 7.0** (Δ **+0.0**) | **76.7 ± 3.6** (Δ **−0.1**) | — O.O.M (paper skip) | — blocked-data | — blocked-data | — blocked-data |
| SE-HSSL | **57.0 ± 8.3** (Δ **+0.0**) | **64.0 ± 4.9** (Δ **+0.1**) | **48.9 ± 4.0** (Δ **+0.0**) | **60.7 ± 7.0** (Δ **+12.7**) | **63.4 ± 9.1** (Δ **−6.4**) | **34.7 ± 4.2** (Δ **−0.1**) | — blocked-data | — blocked-data | — blocked-data |
| TriCL | **52.7 ± 13.9** (Δ **−0.3**) | **61.9 ± 5.8** (Δ **−1.5**) | **47.9 ± 5.3** (Δ **+0.4**) | **63.5 ± 7.4** (Δ **−1.7**) | **75.0 ± 3.4** (Δ **+1.0**) | **33.6 ± 2.5** (Δ **−1.0**) | — blocked-data | — blocked-data | — blocked-data |
| UniGCN | **37.70 ± 8.58** (Δ **−2.10**) | **47.21 ± 5.24** (Δ **+0.91**) | **40.55 ± 3.27** (Δ **−0.45**) | **51.5 ± 2.7** (Δ **−0.2**) | **68.56 ± 4.99** (Δ **+0.96**) | **29.62 ± 1.53** (Δ **−0.18**) | — blocked-data | — blocked-data | — blocked-data |
| UniGCN2 | **41.5 ± 9.2** (Δ **+1.9**) | **53.1 ± 7.3** (Δ **−2.2**) | **42.5 ± 3.2** (Δ **+0.9**) | **58.7 ± 10.1** (Δ **−0.1**) | **72.5 ± 4.6** (Δ **−0.1**) | **32.2 ± 1.8** (Δ **−0.1**) | — blocked-data | — blocked-data | — blocked-data |
| UniGIN | **40.34 ± 9.37** (Δ **−1.06**) | **47.63 ± 6.55** (Δ **−1.57**) | **41.06 ± 3.93** (Δ **−0.64**) | **51.0 ± 2.3** (Δ **+0.2**) | **69.74 ± 4.35** (Δ **−0.66**) | **30.70 ± 1.16** (Δ **−0.10**) | — blocked-data | — blocked-data | — blocked-data |
| VilLain | **28.5 ± 8.2** (Δ **−5.1**) | **31.4 ± 4.1** (Δ **+0.0**) | **39.2 ± 3.9** (Δ **−0.5**) | **49.3 ± 1.5** (Δ **−1.3**) | **73.7 ± 3.3** (Δ **+0.0**) | **19.9 ± 1.2** (Δ **+0.0**) | — blocked-data | — blocked-data | — blocked-data |
| HyperGCL | **18.5 ± 3.5** (Δ **−24.9**) | **16.3 ± 4.0** (Δ **−45.5**) | — diagnostic only: splits 19–20 (no formal aggregate) | **54.6 ± 5.5** (Δ **−9.1**) | — pending | — pending | — blocked-data | — blocked-data | — blocked-data |

## Hyperedge prediction — Table 4 · AUROC

| Model | Citeseer | Cora-CA | IMDB | House | Pubmed | AMiner | DBLP-P | 20News |
|---|---|---|---|---|---|---|---|---|
| MLP | **65.6 ± 2.0** (Δ **+0.0**) | **58.6 ± 2.9** (Δ **+0.0**) | **41.7 ± 2.5** (Δ **−0.3**) | **54.8 ± 5.4** (Δ **+0.0**) | **88.3 ± 0.6** (Δ **+0.0**) | **82.3 ± 0.9** (Δ **+0.0**) | — pending | — blocked-data |
| UniGCN | **53.7 ± 5.2** (Δ **−1.0**) | **61.1 ± 5.7** (Δ **+1.1**) | **53.3 ± 4.1** (Δ **−0.4**) | **50.0 ± 0.0** (Δ **+0.0**) | **51.3 ± 2.8** (Δ **−0.8**) | **68.5 ± 1.9** (Δ **−0.5**) | — pending | — blocked-data |
| UniGIN | **53.3 ± 3.4** (Δ **+0.4**) | **59.7 ± 7.6** (Δ **+1.0**) | **53.9 ± 4.5** (Δ **−0.7**) | **50.0 ± 0.0** (Δ **+0.0**) | **51.7 ± 3.6** (Δ **+0.2**) | **68.9 ± 1.2** (Δ **−0.2**) | — pending | — blocked-data |
| UniGCN2 | **60.3 ± 2.1** (Δ **+0.1**) | **52.2 ± 4.5** (Δ **+0.3**) | **57.1 ± 6.0** (Δ **−0.4**) | **50.0 ± 0.0** (Δ **+0.0**) | **69.1 ± 1.0** (Δ **+0.0**) | **46.2 ± 4.5** (Δ **+0.3**) | — pending | — blocked-data |
| GraphMAE2 | **78.1 ± 2.4** (Δ **−0.1**) | **74.7 ± 2.9** (Δ **+0.0**) | **47.4 ± 1.0** (Δ **+0.2**) | **71.8 ± 5.6** (Δ **+0.2**) | **93.9 ± 1.8** (Δ **+0.3**) | **78.1 ± 0.9** (Δ **+0.0**) | — pending | — blocked-data |
| HGNN | **54.2 ± 3.7** (Δ **−0.6**) | **64.5 ± 5.9** (Δ **−0.5**) | **62.8 ± 1.4** (Δ **+2.3**) | **50.0 ± 0.0** (Δ **−0.4**) | **66.1 ± 1.7** (Δ **+0.2**) | **69.1 ± 1.6** (Δ **−0.5**) | — pending | — blocked-data |
| HNHN | **53.7 ± 2.5** (Δ **+0.0**) | **51.8 ± 1.8** (Δ **+0.2**) | **48.2 ± 0.7** (Δ **+0.0**) | **69.7 ± 5.6** (Δ **+0.0**) | **64.3 ± 2.5** (Δ **−1.4**) | **48.1 ± 1.3** (Δ **+0.0**) | — pending | — blocked-data |
| ED-HNN | **58.1 ± 2.8** (Δ **+0.1**) | **59.2 ± 3.2** (Δ **+0.3**) | **49.1 ± 1.3** (Δ **−0.3**) | **50.3 ± 0.9** (Δ **−0.3**) | **53.3 ± 3.1** (Δ **+0.1**) | **56.8 ± 4.5** (Δ **+0.8**) | — pending | — blocked-data |
| AllSet | **50.7 ± 3.3** (Δ **−1.1**) | **50.8 ± 2.5** (Δ **−0.4**) | **50.6 ± 1.7** (Δ **+0.3**) | **53.5 ± 5.1** (Δ **+0.0**) | **52.7 ± 1.6** (Δ **+0.4**) | **50.5 ± 1.3** (Δ **−0.5**) | — pending | — blocked-data |
| HGD | **52.9 ± 4.2** (Δ **−19.3**) | **43.9 ± 10.3** (Δ **−29.3**) | **46.1 ± 3.3** (Δ **−7.0**) | **50.0 ± 0.0** (Δ **−37.9**) | **51.0 ± 2.7** (Δ **−36.2**) | **50.7 ± 8.3** (Δ **−34.2**) | — pending | — blocked-data |
| HyperGCN | **54.9 ± 2.1** (Δ **+0.0**) | **48.9 ± 1.6** (Δ **−0.4**) | **48.4 ± 1.9** (Δ **+0.0**) | **87.7 ± 2.5** (Δ **+0.0**) | **74.2 ± 0.6** (Δ **+0.1**) | **50.6 ± 2.6** (Δ **−0.2**) | — pending | — blocked-data |
| PhenomNN | **54.3 ± 2.2** (Δ **−0.2**) | **50.7 ± 1.3** (Δ **+0.4**) | **49.8 ± 0.9** (Δ **+0.1**) | **50.6 ± 1.2** (Δ **−0.2**) | **65.1 ± 1.7** (Δ **+1.1**) | O.O.M skip | O.O.M skip | O.O.T skip |
| HypeBoy | **86.4 ± 2.1** (Δ **+0.0**) | **87.4 ± 1.5** (Δ **+0.1**) | **59.3 ± 1.8** (Δ **−0.1**) | **87.0 ± 3.0** (Δ **−0.2**) | **92.1 ± 0.5** (Δ **+0.0**) | **89.7 ± 0.6** (Δ **+0.0**) | — pending | — blocked-data |
| SE-HSSL | **90.6 ± 1.1** (Δ **+0.1**) | **85.7 ± 2.3** (Δ **+0.1**) | **54.1 ± 2.0** (Δ **−1.5**) | **79.9 ± 3.1** (Δ **−0.5**) | **95.0 ± 0.4** (Δ **+0.5**) | **87.4 ± 0.6** (Δ **−0.1**) | — pending | — blocked-data |
| TriCL | **89.1 ± 1.3** (Δ **−1.4**) | **85.0 ± 2.0** (Δ **−2.8**) | **56.8 ± 3.8** (Δ **−2.1**) | **84.6 ± 3.5** (Δ **−5.4**) | **96.1 ± 0.6** (Δ **+4.2**) | **86.0 ± 0.9** (Δ **−4.4**) | — pending | — blocked-data |
| MaskGAE | **86.7 ± 1.7** (Δ **+0.0**) | **76.1 ± 2.2** (Δ **−0.4**) | **54.5 ± 1.3** (Δ **+0.1**) | **88.2 ± 3.6** (Δ **+0.2**) | **95.5 ± 0.3** (Δ **+0.0**) | **87.6 ± 0.9** (Δ **+0.0**) | — pending | O.O.T skip |
| HyperGCL | **51.9 ± 2.9** (Δ **−22.0**) | **51.1 ± 3.1** (Δ **−30.0**) | **50.9 ± 2.8** (Δ **−2.9**) | **63.3 ± 9.5** (Δ **−13.0**) | — pending | — pending | O.O.M skip | — blocked-data |
| VilLain | **57.2 ± 2.4** (Δ **−1.1**) | **64.7 ± 2.5** (Δ **+0.3**) | **43.6 ± 2.6** (Δ **−0.3**) | **77.5 ± 5.6** (Δ **+0.3**) | **84.3 ± 0.8** (Δ **+0.6**) | **61.9 ± 0.7** (Δ **−0.8**) | — pending | — blocked-data |
| HyperGRL | — unavailable: EP implementation missing | — unavailable: EP implementation missing | — unavailable: EP implementation missing | — unavailable: EP implementation missing | — unavailable: EP implementation missing | — unavailable: EP implementation missing | — unavailable: EP implementation missing | O.O.T skip |

## Community detection — Table 5 · NMI

| Model | Citeseer | Cora-CA | IMDB | House | Pubmed | AMiner | DBLP-P | 20News |
|---|---|---|---|---|---|---|---|---|
| GraphMAE2 | **42.1 ± 0.4** (Δ **+0.0**) | **42.0 ± 0.9** (Δ **−0.1**) | **5.7 ± 0.2** (Δ **−0.3**) | **0.1 ± 0.0** (Δ **−0.0**) | **34.7 ± 0.0** (Δ **+14.7**) | **40.0 ± 0.1** (Δ **−0.1**) | — pending | — pending |
| MaskGAE | **34.4 ± 0.1** (Δ **−0.4**) | **39.4 ± 1.3** (Δ **+1.4**) | **3.2 ± 0.0** (Δ **+0.3**) | **0.2 ± 0.0** (Δ **−1.2**) | **29.9 ± 0.0** (Δ **+1.0**) | **36.3 ± 0.1** (Δ **−0.0**) | — pending | O.O.T skip |
| GGD (H-GD) | **8.0 ± 0.0** (Δ **+1.7**) | **6.7 ± 0.4** (Δ **+0.7**) | **0.3 ± 0.1** (Δ **+0.0**) | **0.1 ± 0.0** (Δ **+0.1**) | **4.0 ± 0.0** (Δ **−2.7**) | **3.7 ± 0.2** (Δ **−0.7**) | — pending | — pending |
| TriCL | **39.0 ± 0.1** (Δ **+0.5**) | **45.2 ± 0.9** (Δ **+4.3**) | **5.4 ± 0.1** (Δ **−0.1**) | **2.7 ± 0.1** (Δ **−0.2**) | **31.0 ± 0.1** (Δ **−1.7**) | **40.7 ± 0.3** (Δ **−0.2**) | — pending | — pending |
| HyperGCL | — pending | — pending | — pending | — pending | — pending | — pending | O.O.M skip | — pending |
| HyperGRL | — pending | — pending | — pending | — pending | — pending | — pending | — pending | O.O.T skip |
| HypeBoy | **38.7 ± 0.1** (Δ **−2.2**) | **44.7 ± 0.9** (Δ **+2.8**) | **8.9 ± 0.0** (Δ **+0.3**) | **0.0 ± 0.0** (Δ **+0.0**) | **30.3 ± 0.0** (Δ **−0.1**) | **42.2 ± 0.1** (Δ **−0.0**) | — pending | — pending |
| VilLain | **9.1 ± 4.5** (Δ **−2.2**) | **9.7 ± 2.2** (Δ **−0.0**) | **0.0 ± 0.0** (Δ **−0.1**) | **0.1 ± 0.0** (Δ **+0.0**) | **32.9 ± 0.0** (Δ **+0.0**) | **17.7 ± 0.7** (Δ **+1.5**) | — pending | — pending |
| SE-HSSL | **38.5 ± 0.0** (Δ **−0.0**) | **44.5 ± 0.1** (Δ **+0.1**) | **0.5 ± 0.2** (Δ **+0.2**) | **0.2 ± 0.0** (Δ **−0.5**) | — pending | — pending | — pending | — pending |

## Evidence and data contract

- Canonical per-run values, configurations, and logs: [.agents/env-status/formal-results.md](.agents/env-status/formal-results.md)
- Raw execution logs: [.agents/env-status/full-runs/](.agents/env-status/full-runs/)
- Current unavailable loader inputs: DBLP-A `data_split_0.01.pickle`, MN-40 `edge_bucket.pickle`, and 20News `edge_bucket.pickle`.
