---
type: model
datasets: 9
updated: 2026-09-15 13:09
tags: [hgnn/model]
---

<!-- AUTO:BEGIN -->
# HyperGCL

<span class="lgn">코드 `HyperGCL/` · 결과 `results/result_*_HyperGCL_*.txt` · 갱신 2026-09-15 13:09</span>

<div class="hg-cards"><div class="hg-card"><span class="k">NC 일치</span><span class="big">0/3</span><span class="note">|Δ| 중앙값 24.90</span></div><div class="hg-card"><span class="k">HP 일치</span><span class="big">0/4</span><span class="note">|Δ| 중앙값 22.00</span></div><div class="hg-card"><span class="k">최대 편차</span><span class="big">−45.5</span><span class="note">노드 분류 · Cora-CA</span></div></div>

## Node classification <span class="m">Table 3 · Accuracy</span>

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | <span class="v">18.5</span><span class="sd">±3.5</span> | 43.4 | <span class="d bad">−24.9</span> | |
| [[Cora-CA]] | <span class="v">16.3</span><span class="sd">±4.0</span> | 61.8 | <span class="d bad">−45.5</span> | |
| [[IMDB]] | <span class="na">—</span> | 48.4 | | diagnostic only: splits 19–20 (no formal aggregate) |
| [[House]] | <span class="v">54.6</span><span class="sd">±5.5</span> | 63.7 | <span class="d bad">−9.1</span> | |
| [[Pubmed]] | <span class="na">—</span> | 71.0 | | pending |
| [[AMiner]] | <span class="na">—</span> | 30.4 | | pending |
| [[DBLP-A]] | <span class="na">—</span> | 69.5 | | blocked-data |
| [[MN-40]] | <span class="na">—</span> | 94.6 | | blocked-data |
| [[20News]] | <span class="na">—</span> | 74.0 | | blocked-data |

## Hyperedge prediction <span class="m">Table 4 · AUROC</span>

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | <span class="v">51.9</span><span class="sd">±2.9</span> | 73.9 | <span class="d bad">−22.0</span> | |
| [[Cora-CA]] | <span class="v">51.1</span><span class="sd">±3.1</span> | 81.1 | <span class="d bad">−30.0</span> | |
| [[IMDB]] | <span class="v">50.9</span><span class="sd">±2.8</span> | 53.8 | <span class="d warn">−2.9</span> | |
| [[House]] | <span class="v">63.3</span><span class="sd">±9.5</span> | 76.3 | <span class="d bad">−13.0</span> | |
| [[Pubmed]] | <span class="na">—</span> | 89.6 | | pending |
| [[AMiner]] | <span class="na">—</span> | 82.1 | | pending |
| [[DBLP-P]] | <span class="lim">OOM</span> | 83.6 | | O.O.M skip |
| [[20News]] | <span class="na">—</span> | 76.3 | | blocked-data |

## Community detection <span class="m">Table 5 · NMI</span>

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Cora-CA]] | <span class="na">—</span> | 30.6 | | pending |
| [[DBLP-P]] | <span class="lim">OOM</span> | — | | O.O.M skip |
| [[20News]] | <span class="na">—</span> | 38.2 | | pending |

<div class="hg-legend"><span>우리값 <span class="sd">±표준편차</span></span><span class="d ok">±2 이내</span><span class="d warn">2–5</span><span class="d bad">5 초과</span><span class="lim">OOM</span><span class="lgn">논문이 수치를 못 낸 칸</span><span class="na">—</span><span class="lgn">미실행·보류</span></div>

관련: [[논문 대조]] · [[Home]]
<!-- AUTO:END -->

## 메모


