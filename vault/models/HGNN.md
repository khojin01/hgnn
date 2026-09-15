---
type: model
datasets: 9
updated: 2026-09-15 13:09
tags: [hgnn/model]
---

<!-- AUTO:BEGIN -->
# HGNN

<span class="lgn">코드 `HGNN/` · 결과 `results/result_*_HGNN_*.txt` · 갱신 2026-09-15 13:09</span>

<div class="hg-cards"><div class="hg-card"><span class="k">NC 일치</span><span class="big">5/6</span><span class="note">|Δ| 중앙값 0.38</span></div><div class="hg-card"><span class="k">HP 일치</span><span class="big">5/6</span><span class="note">|Δ| 중앙값 0.50</span></div><div class="hg-card"><span class="k">최대 편차</span><span class="big">+2.3</span><span class="note">하이퍼엣지 예측 · IMDB</span></div></div>

## Node classification <span class="m">Table 3 · Accuracy</span>

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | <span class="v">38.1</span><span class="sd">±10.7</span> | 38.1 | <span class="d ok">−0.0</span> | |
| [[Cora-CA]] | <span class="v">46.6</span><span class="sd">±7.9</span> | 44.3 | <span class="d warn">+2.3</span> | |
| [[IMDB]] | <span class="v">41.9</span><span class="sd">±4.5</span> | 41.5 | <span class="d ok">+0.4</span> | |
| [[House]] | <span class="v">51.9</span><span class="sd">±4.7</span> | 51.9 | <span class="d ok">+0.0</span> | |
| [[Pubmed]] | <span class="v">70.6</span><span class="sd">±3.6</span> | 70.8 | <span class="d ok">−0.2</span> | |
| [[AMiner]] | <span class="v">30.5</span><span class="sd">±1.6</span> | 29.7 | <span class="d ok">+0.8</span> | |
| [[DBLP-A]] | <span class="na">—</span> | 65.0 | | blocked-data |
| [[MN-40]] | <span class="na">—</span> | 89.5 | | blocked-data |
| [[20News]] | <span class="na">—</span> | 67.1 | | blocked-data |

## Hyperedge prediction <span class="m">Table 4 · AUROC</span>

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | <span class="v">54.2</span><span class="sd">±3.7</span> | 54.8 | <span class="d ok">−0.6</span> | |
| [[Cora-CA]] | <span class="v">64.5</span><span class="sd">±5.9</span> | 65.0 | <span class="d ok">−0.5</span> | |
| [[IMDB]] | <span class="v">62.8</span><span class="sd">±1.4</span> | 60.5 | <span class="d warn">+2.3</span> | |
| [[House]] | <span class="v">50.0</span><span class="sd">±0.0</span> | 50.4 | <span class="d ok">−0.4</span> | |
| [[Pubmed]] | <span class="v">66.1</span><span class="sd">±1.7</span> | 65.9 | <span class="d ok">+0.2</span> | |
| [[AMiner]] | <span class="v">69.1</span><span class="sd">±1.6</span> | 69.6 | <span class="d ok">−0.5</span> | |
| [[DBLP-P]] | <span class="na">—</span> | 61.0 | | pending |
| [[20News]] | <span class="na">—</span> | 49.4 | | blocked-data |

<div class="hg-legend"><span>우리값 <span class="sd">±표준편차</span></span><span class="d ok">±2 이내</span><span class="d warn">2–5</span><span class="d bad">5 초과</span><span class="lim">OOM</span><span class="lgn">논문이 수치를 못 낸 칸</span><span class="na">—</span><span class="lgn">미실행·보류</span></div>

관련: [[논문 대조]] · [[Home]]
<!-- AUTO:END -->

## 메모


