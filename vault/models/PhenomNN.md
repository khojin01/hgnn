---
type: model
datasets: 9
updated: 2026-09-15 13:09
tags: [hgnn/model]
---

<!-- AUTO:BEGIN -->
# PhenomNN

<span class="lgn">코드 `PhenomNN/` · 결과 `results/result_*_PhenomNN_*.txt` · 갱신 2026-09-15 13:09</span>

<div class="hg-cards"><div class="hg-card"><span class="k">NC 일치</span><span class="big">4/5</span><span class="note">|Δ| 중앙값 0.10</span></div><div class="hg-card"><span class="k">HP 일치</span><span class="big">5/5</span><span class="note">|Δ| 중앙값 0.20</span></div><div class="hg-card"><span class="k">최대 편차</span><span class="big">+2.9</span><span class="note">노드 분류 · Citeseer</span></div></div>

## Node classification <span class="m">Table 3 · Accuracy</span>

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | <span class="v">45.1</span><span class="sd">±11.7</span> | 42.2 | <span class="d warn">+2.9</span> | |
| [[Cora-CA]] | <span class="v">56.3</span><span class="sd">±7.5</span> | 56.2 | <span class="d ok">+0.1</span> | |
| [[IMDB]] | <span class="v">42.1</span><span class="sd">±2.9</span> | 42.1 | <span class="d ok">+0.0</span> | |
| [[House]] | <span class="v">69.4</span><span class="sd">±7.0</span> | 69.4 | <span class="d ok">+0.0</span> | |
| [[Pubmed]] | <span class="v">76.7</span><span class="sd">±3.6</span> | 76.8 | <span class="d ok">−0.1</span> | |
| [[AMiner]] | <span class="lim">OOM</span> | — | | O.O.M (paper skip) |
| [[DBLP-A]] | <span class="na">—</span> | 70.3 | | blocked-data |
| [[MN-40]] | <span class="na">—</span> | 94.0 | | blocked-data |
| [[20News]] | <span class="na">—</span> | — | | blocked-data |

## Hyperedge prediction <span class="m">Table 4 · AUROC</span>

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | <span class="v">54.3</span><span class="sd">±2.2</span> | 54.5 | <span class="d ok">−0.2</span> | |
| [[Cora-CA]] | <span class="v">50.7</span><span class="sd">±1.3</span> | 50.3 | <span class="d ok">+0.4</span> | |
| [[IMDB]] | <span class="v">49.8</span><span class="sd">±0.9</span> | 49.7 | <span class="d ok">+0.1</span> | |
| [[House]] | <span class="v">50.6</span><span class="sd">±1.2</span> | 50.8 | <span class="d ok">−0.2</span> | |
| [[Pubmed]] | <span class="v">65.1</span><span class="sd">±1.7</span> | 64.0 | <span class="d ok">+1.1</span> | |
| [[AMiner]] | <span class="lim">OOM</span> | — | | O.O.M skip |
| [[DBLP-P]] | <span class="lim">OOM</span> | — | | O.O.M skip |
| [[20News]] | <span class="lim">OOT</span> | — | | O.O.T skip |

<div class="hg-legend"><span>우리값 <span class="sd">±표준편차</span></span><span class="d ok">±2 이내</span><span class="d warn">2–5</span><span class="d bad">5 초과</span><span class="lim">OOM</span><span class="lgn">논문이 수치를 못 낸 칸</span><span class="na">—</span><span class="lgn">미실행·보류</span></div>

관련: [[논문 대조]] · [[Home]]
<!-- AUTO:END -->

## 메모


