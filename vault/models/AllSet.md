---
type: model
datasets: 9
updated: 2026-09-15 13:09
tags: [hgnn/model]
---

<!-- AUTO:BEGIN -->
# AllSet

<span class="lgn">코드 `AllSet/` · 결과 `results/result_*_AllSet_*.txt` · 갱신 2026-09-15 13:09</span>

<div class="hg-cards"><div class="hg-card"><span class="k">NC 일치</span><span class="big">6/6</span><span class="note">|Δ| 중앙값 0.51</span></div><div class="hg-card"><span class="k">HP 일치</span><span class="big">6/6</span><span class="note">|Δ| 중앙값 0.40</span></div><div class="hg-card"><span class="k">최대 편차</span><span class="big">−1.6</span><span class="note">노드 분류 · Pubmed</span></div></div>

## Node classification <span class="m">Table 3 · Accuracy</span>

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | <span class="v">41.0</span><span class="sd">±8.3</span> | 41.1 | <span class="d ok">−0.1</span> | |
| [[Cora-CA]] | <span class="v">53.1</span><span class="sd">±6.4</span> | 53.6 | <span class="d ok">−0.5</span> | |
| [[IMDB]] | <span class="v">40.5</span><span class="sd">±4.6</span> | 41.7 | <span class="d ok">−1.2</span> | |
| [[House]] | <span class="v">50.2</span><span class="sd">±2.8</span> | 50.3 | <span class="d ok">−0.1</span> | |
| [[Pubmed]] | <span class="v">72.5</span><span class="sd">±6.2</span> | 74.1 | <span class="d ok">−1.6</span> | |
| [[AMiner]] | <span class="v">29.6</span><span class="sd">±3.5</span> | 29.8 | <span class="d ok">−0.2</span> | |
| [[DBLP-A]] | <span class="na">—</span> | 64.9 | | deferred |
| [[MN-40]] | <span class="na">—</span> | 89.4 | | blocked-data |
| [[20News]] | <span class="na">—</span> | 77.2 | | blocked-data |

## Hyperedge prediction <span class="m">Table 4 · AUROC</span>

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | <span class="v">50.7</span><span class="sd">±3.3</span> | 51.8 | <span class="d ok">−1.1</span> | |
| [[Cora-CA]] | <span class="v">50.8</span><span class="sd">±2.5</span> | 51.2 | <span class="d ok">−0.4</span> | |
| [[IMDB]] | <span class="v">50.6</span><span class="sd">±1.7</span> | 50.3 | <span class="d ok">+0.3</span> | |
| [[House]] | <span class="v">53.5</span><span class="sd">±5.1</span> | 53.5 | <span class="d ok">+0.0</span> | |
| [[Pubmed]] | <span class="v">52.7</span><span class="sd">±1.6</span> | 52.3 | <span class="d ok">+0.4</span> | |
| [[AMiner]] | <span class="v">50.5</span><span class="sd">±1.3</span> | 51.0 | <span class="d ok">−0.5</span> | |
| [[DBLP-P]] | <span class="na">—</span> | 53.2 | | pending |
| [[20News]] | <span class="na">—</span> | 50.1 | | blocked-data |

<div class="hg-legend"><span>우리값 <span class="sd">±표준편차</span></span><span class="d ok">±2 이내</span><span class="d warn">2–5</span><span class="d bad">5 초과</span><span class="lim">OOM</span><span class="lgn">논문이 수치를 못 낸 칸</span><span class="na">—</span><span class="lgn">미실행·보류</span></div>

관련: [[논문 대조]] · [[Home]]
<!-- AUTO:END -->

## 메모


