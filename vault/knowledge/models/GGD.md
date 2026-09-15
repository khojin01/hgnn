---
type: model
code_dir: H-GD
nc_done: 6
nc_agree: 2
hp_done: 6
hp_agree: 0
cd_done: 6
cd_agree: 5
max_abs_delta: 37.9
worst_cell: "하이퍼엣지 예측 House −37.9"
status: complete
updated: 2026-09-15 19:27
tags: [hgnn/model]
---

<!-- AUTO:BEGIN -->
# GGD

실행법 → [[GGD 실행]] · 코드 `H-GD/` · 결과 `results/result_*_H-GD_*.txt` · <small>갱신 2026-09-15 19:27</small>

NC 2/6 일치 · HP 0/6 일치 · CD 5/6 일치 · 최대 편차 하이퍼엣지 예측 House −37.9

## Node classification — Table 3 · Accuracy

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 27.5 <span class="sd">±6.4</span> | 34.0 | <span class="d bad">−6.5</span> |  |
| [[Cora-CA]] | 28.3 <span class="sd">±4.6</span> | 32.2 | <span class="d warn">−3.9</span> |  |
| [[IMDB]] | 36.7 <span class="sd">±2.6</span> | 37.6 | <span class="d ok">−0.9</span> |  |
| [[House]] | 49.9 <span class="sd">±1.3</span> | 50.6 | <span class="d ok">−0.7</span> |  |
| [[Pubmed]] | 62.2 <span class="sd">±5.0</span> | 64.9 | <span class="d warn">−2.7</span> |  |
| [[AMiner]] | 16.6 <span class="sd">±2.7</span> | 31.5 | <span class="d bad">−14.9</span> |  |
| [[DBLP-A]] | — | 58.8 |  | blocked-data |
| [[MN-40]] | — | 76.8 |  | blocked-data |
| [[20News]] | — | 47.5 |  | blocked-data |

## Hyperedge prediction — Table 4 · AUROC

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 52.9 <span class="sd">±4.2</span> | 72.2 | <span class="d bad">−19.3</span> |  |
| [[Cora-CA]] | 43.9 <span class="sd">±10.3</span> | 73.2 | <span class="d bad">−29.3</span> |  |
| [[IMDB]] | 46.1 <span class="sd">±3.3</span> | 53.1 | <span class="d bad">−7.0</span> |  |
| [[House]] | 50.0 <span class="sd">±0.0</span> | 87.9 | <span class="d bad">−37.9</span> |  |
| [[Pubmed]] | 51.0 <span class="sd">±2.7</span> | 87.2 | <span class="d bad">−36.2</span> |  |
| [[AMiner]] | 50.7 <span class="sd">±8.3</span> | 84.9 | <span class="d bad">−34.2</span> |  |
| [[DBLP-P]] | — | 91.6 |  | pending |
| [[20News]] | — | 87.9 |  | blocked-data |

## Community detection — Table 5 · NMI

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | 8.0 <span class="sd">±0.0</span> | 6.3 | <span class="d ok">+1.7</span> |  |
| [[Cora-CA]] | 6.7 <span class="sd">±0.4</span> | 6.0 | <span class="d ok">+0.7</span> |  |
| [[IMDB]] | 0.3 <span class="sd">±0.1</span> | 0.3 | <span class="d ok">+0.0</span> |  |
| [[House]] | 0.1 <span class="sd">±0.0</span> | 0.1 | <span class="d ok">+0.1</span> |  |
| [[Pubmed]] | 4.0 <span class="sd">±0.0</span> | 6.7 | <span class="d warn">−2.7</span> |  |
| [[AMiner]] | 3.7 <span class="sd">±0.2</span> | 4.4 | <span class="d ok">−0.7</span> |  |
| [[DBLP-P]] | — | 2.6 |  | pending |
| [[20News]] | — | 0.0 |  | pending |

표기 · 값 <span class="sd">±표준편차</span> · Δ = 우리 − 논문 · <span class="d ok">+0.3</span> ±2 이내 · <span class="d warn">+3.0</span> 2–5 · <span class="d bad">+7.0</span> 5 초과 · <span class="lim">OOM</span> 논문이 수치를 못 낸 칸 · — 미실행·보류
<!-- AUTO:END -->

## 메모


