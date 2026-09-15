---
type: model
datasets: 9
updated: 2026-09-15 13:09
tags: [hgnn/model]
---

<!-- AUTO:BEGIN -->
# SE-HSSL

<span class="lgn">코드 `SEHSSL/` · 결과 `results/result_*_SEHSSL_*.txt` · 갱신 2026-09-15 13:09</span>

<div class="hg-cards"><div class="hg-card"><span class="k">NC 일치</span><span class="big">4/6</span><span class="note">|Δ| 중앙값 0.10</span></div><div class="hg-card"><span class="k">HP 일치</span><span class="big">6/6</span><span class="note">|Δ| 중앙값 0.50</span></div><div class="hg-card"><span class="k">최대 편차</span><span class="big">+12.7</span><span class="note">노드 분류 · House</span></div></div>

## Node classification <span class="m">Table 3 · Accuracy</span>

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | <span class="v">57.0</span><span class="sd">±8.3</span> | 57.0 | <span class="d ok">+0.0</span> | |
| [[Cora-CA]] | <span class="v">64.0</span><span class="sd">±4.9</span> | 63.9 | <span class="d ok">+0.1</span> | |
| [[IMDB]] | <span class="v">48.9</span><span class="sd">±4.0</span> | 48.9 | <span class="d ok">+0.0</span> | |
| [[House]] | <span class="v">60.7</span><span class="sd">±7.0</span> | 48.0 | <span class="d bad">+12.7</span> | |
| [[Pubmed]] | <span class="v">63.4</span><span class="sd">±9.1</span> | 69.8 | <span class="d bad">−6.4</span> | |
| [[AMiner]] | <span class="v">34.7</span><span class="sd">±4.2</span> | 34.8 | <span class="d ok">−0.1</span> | |
| [[DBLP-A]] | <span class="na">—</span> | 77.1 | | blocked-data |
| [[MN-40]] | <span class="na">—</span> | 85.8 | | blocked-data |
| [[20News]] | <span class="na">—</span> | 75.8 | | blocked-data |

## Hyperedge prediction <span class="m">Table 4 · AUROC</span>

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | <span class="v">90.6</span><span class="sd">±1.1</span> | 90.5 | <span class="d ok">+0.1</span> | |
| [[Cora-CA]] | <span class="v">85.7</span><span class="sd">±2.3</span> | 85.6 | <span class="d ok">+0.1</span> | |
| [[IMDB]] | <span class="v">54.1</span><span class="sd">±2.0</span> | 55.6 | <span class="d ok">−1.5</span> | |
| [[House]] | <span class="v">79.9</span><span class="sd">±3.1</span> | 80.4 | <span class="d ok">−0.5</span> | |
| [[Pubmed]] | <span class="v">95.0</span><span class="sd">±0.4</span> | 94.5 | <span class="d ok">+0.5</span> | |
| [[AMiner]] | <span class="v">87.4</span><span class="sd">±0.6</span> | 87.5 | <span class="d ok">−0.1</span> | |
| [[DBLP-P]] | <span class="na">—</span> | 94.0 | | pending |
| [[20News]] | <span class="na">—</span> | 95.2 | | blocked-data |

<div class="hg-legend"><span>우리값 <span class="sd">±표준편차</span></span><span class="d ok">±2 이내</span><span class="d warn">2–5</span><span class="d bad">5 초과</span><span class="lim">OOM</span><span class="lgn">논문이 수치를 못 낸 칸</span><span class="na">—</span><span class="lgn">미실행·보류</span></div>

관련: [[논문 대조]] · [[Home]]
<!-- AUTO:END -->

## 메모


