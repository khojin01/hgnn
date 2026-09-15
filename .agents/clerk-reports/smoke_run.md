# Hypergraph experiment result matrix

`내 결과 ± 표준편차 (Δ = 내 평균 − HyperGC 논문 표의 평균)` 형식입니다.

- `↑2 이상`: 논문 기준보다 2%p 이상 높음
- `−2~5`: 논문 기준보다 2~5%p 낮음
- `↓5 초과`: 논문 기준보다 5%p 이상 낮음
- `—`: 아직 해당 조합의 정식 결과가 없거나, 데이터/실행 정책상 제외됨
- **정식**은 전임자 `118.sh` 고정 설정·기본 200 epoch·20 split/seed 결과입니다. `smoke`는 단기 확인 결과로 논문 재현값이 아닙니다.

## Node classification — Table 3 · Accuracy

| Model | Citeseer | Cora-CA | IMDB | Pubmed | AMiner | DBLP-A | MN-40 | 20News |
|---|---|---|---|---|---|---|---|---|
| AllSet | **41.05 ± 8.26** (Δ **+0.45**) | **53.09 ± 6.43** (Δ **−0.01**) | **40.53 ± 4.58** (Δ **−1.17**) | **72.45 ± 6.22** (Δ **−0.85**) | **29.62 ± 3.55** (Δ **−0.28**) | — deferred | — blocked-data | — blocked-data |
| ED-HNN | **34.00 ± 8.84** (Δ **+1.10**) | **36.50 ± 7.53** (Δ **+0.20**) | **38.00 ± 2.81** (Δ **+0.80**) | **60.96 ± 3.85** (Δ **−0.94**) | **26.56 ± 3.05** (Δ **−0.54**) | — blocked-data | — blocked-data | — blocked-data |
| GGD (H-GD) | **27.5 ± 6.4** (Δ **−0.7**) | **28.3 ± 4.6** (Δ **−0.2**) | **36.7 ± 2.6** (Δ **+0.0**) | **62.2 ± 5.0** (Δ **+0.0**) | **16.6 ± 2.7** (Δ **+0.2**) | — blocked-data | — blocked-data | — blocked-data |
| GraphMAE2 | **51.7 ± 12.9** (Δ **−0.3**) | **64.0 ± 5.8** (Δ **+0.6**) | **44.7 ± 4.2** (Δ **−0.3**) | **72.2 ± 4.7** (Δ **+4.3**) | **34.8 ± 2.4** (Δ **+0.0**) | — blocked-data | — blocked-data | — blocked-data |
| HGNN | **38.09 ± 10.73** (Δ **−0.01**) | **46.59 ± 7.88** (Δ **+2.29**) | **41.88 ± 4.54** (Δ **+0.38**) | **70.58 ± 3.63** (Δ **−0.22**) | **30.54 ± 1.64** (Δ **+0.84**) | — blocked-data | — blocked-data | — blocked-data |
| HNHN | **43.33 ± 8.03** (Δ **−0.87**) | **51.02 ± 6.56** (Δ **−2.08**) | **41.84 ± 3.66** (Δ **−0.66**) | **69.45 ± 3.36** (Δ **+0.35**) | **31.83 ± 2.03** (Δ **−0.27**) | — blocked-data | — blocked-data | — blocked-data |
| HypeBoy | **57.6 ± 10.5** (Δ **−0.1**) | **67.0 ± 3.7** (Δ **+0.0**) | **48.0 ± 5.0** (Δ **−0.3**) | **73.7 ± 4.4** (Δ **+0.0**) | **34.2 ± 3.0** (Δ **−0.4**) | — blocked-data | — blocked-data | — blocked-data |
| HyperGCN | **33.7 ± 7.3** (Δ **+0.1**) | **45.0 ± 9.5** (Δ **+13.6**) | **40.6 ± 3.2** (Δ **+0.9**) | **59.3 ± 15.2** (Δ **−14.4**) | **26.4 ± 2.9** (Δ **+6.5**) | — blocked-data | — blocked-data | — blocked-data |
| HyperGRL | — timeout-repair | **42.0 ± 6.7** (Δ **+0.2**) | — timeout-repair | — timeout-repair | — timeout-repair | — blocked-data | — blocked-data | — blocked-data |
| MLP | **32.43 ± 8.05** (Δ **+0.03**) | **37.24 ± 4.31** (Δ **+1.24**) | **38.23 ± 2.67** (Δ **+0.63**) | **62.67 ± 3.26** (Δ **−0.13**) | **22.39 ± 1.42** (Δ **−0.31**) | — blocked-data | — blocked-data | — blocked-data |
| MaskGAE | **52.7 ± 10.4** (Δ **−0.5**) | **56.5 ± 6.8** (Δ **−3.3**) | **44.7 ± 3.5** (Δ **−0.3**) | **74.6 ± 4.2** (Δ **−0.8**) | **32.5 ± 1.7** (Δ **−1.3**) | — blocked-data | — blocked-data | — blocked-data |
| PhenomNN | **45.1 ± 11.7** (Δ **+2.9**) | **56.3 ± 7.5** (Δ **+0.1**) | **42.1 ± 2.9** (Δ **+0.0**) | **76.7 ± 3.6** (Δ **−0.1**) | — O.O.M (paper skip) | — blocked-data | — blocked-data | — blocked-data |
| SE-HSSL | **57.0 ± 8.3** (Δ **+0.0**) | **64.0 ± 4.9** (Δ **+0.1**) | **48.9 ± 4.0** (Δ **+0.0**) | **63.4 ± 9.1** (Δ **−6.4**) | **34.7 ± 4.2** (Δ **−0.1**) | — blocked-data | — blocked-data | — blocked-data |
| TriCL | **52.7 ± 13.9** (Δ **−0.3**) | **61.9 ± 5.8** (Δ **−1.5**) | **47.9 ± 5.3** (Δ **+0.4**) | **75.0 ± 3.4** (Δ **+1.0**) | **33.6 ± 2.5** (Δ **−1.0**) | — blocked-data | — blocked-data | — blocked-data |
| UniGCN | **37.70 ± 8.58** (Δ **−0.50**) | **47.21 ± 5.24** (Δ **−0.89**) | **40.55 ± 3.27** (Δ **+0.05**) | **68.56 ± 4.99** (Δ **−0.34**) | **29.62 ± 1.53** (Δ **−0.28**) | — blocked-data | — blocked-data | — blocked-data |
| UniGCN2 | **41.5 ± 9.2** (Δ **+1.9**) | **53.1 ± 7.3** (Δ **−2.2**) | **42.5 ± 3.2** (Δ **+0.9**) | **72.5 ± 4.6** (Δ **−0.1**) | **32.2 ± 1.8** (Δ **−0.1**) | — blocked-data | — blocked-data | — blocked-data |
| UniGIN | **40.34 ± 9.37** (Δ **−1.06**) | **47.63 ± 6.55** (Δ **−1.57**) | **41.06 ± 3.93** (Δ **−0.64**) | **69.74 ± 4.35** (Δ **−0.66**) | **30.70 ± 1.16** (Δ **−0.10**) | — blocked-data | — blocked-data | — blocked-data |
| VilLain | **51.5 ± 2.9** (Δ **+17.9**) | **57.2 ± 1.8** (Δ **+25.8**) | **45.4 ± 1.0** (Δ **+5.7**) | **80.9 ± 0.9** (Δ **+7.2**) | **30.2 ± 0.5** (Δ **+10.3**) | — blocked-data | — blocked-data | — blocked-data |
| HyperGCL | **18.5 ± 3.5** (Δ **−24.9**) | **16.3 ± 4.0** (Δ **−45.5**) | — diagnostic only: splits 19–20 (no formal aggregate) | — pending | — pending | — blocked-data | — blocked-data | — blocked-data |

## Hyperedge prediction — Table 4 · AUROC

| Model | Cora-CA | DBLP-P | AMiner | 20News |
|---|---|---|---|---|
| GGD (H-GD) | 54.30 ± 0.00 smoke (Δ −18.90) | — pending | — pending | — pending |
| PhenomNN | — pending | O.O.M skip | O.O.M skip | O.O.T skip |
| MaskGAE | — pending | — pending | — pending | O.O.T skip |
| HyperGRL | — pending | — pending | — pending | O.O.T skip |

## Community detection — Table 5 · NMI

| Model | Cora-CA | DBLP-P | 20News |
|---|---|---|---|
| VilLain | 9.45 smoke (Δ −0.28) | — pending | — pending |
| HyperGCL | — pending | O.O.M skip | — pending |
| MaskGAE | — pending | — pending | O.O.T skip |
| HyperGRL | — pending | — pending | O.O.T skip |

## Evidence and data contract

- Canonical per-run values, configurations, and logs: [.agents/env-status/formal-results.md](.agents/env-status/formal-results.md)
- Raw execution logs: [.agents/env-status/full-runs/](.agents/env-status/full-runs/)
- Current unavailable loader inputs: DBLP-A `data_split_0.01.pickle`, MN-40 `edge_bucket.pickle`, and 20News `edge_bucket.pickle`.
