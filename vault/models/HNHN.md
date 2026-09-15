---
type: model
datasets: 9
updated: 2026-09-15 13:09
tags: [hgnn/model]
---

<!-- AUTO:BEGIN -->
# HNHN

<span class="lgn">코드 `HNHN/` · 결과 `results/result_*_HNHN_*.txt` · 갱신 2026-09-15 13:09</span>

<div class="hg-cards"><div class="hg-card"><span class="k">NC 일치</span><span class="big">5/6</span><span class="note">|Δ| 중앙값 0.66</span></div><div class="hg-card"><span class="k">HP 일치</span><span class="big">6/6</span><span class="note">|Δ| 중앙값 0.00</span></div><div class="hg-card"><span class="k">최대 편차</span><span class="big">−2.1</span><span class="note">노드 분류 · Cora-CA</span></div></div>

## Node classification <span class="m">Table 3 · Accuracy</span>

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | <span class="v">43.3</span><span class="sd">±8.0</span> | 44.2 | <span class="d ok">−0.9</span> | |
| [[Cora-CA]] | <span class="v">51.0</span><span class="sd">±6.6</span> | 53.1 | <span class="d warn">−2.1</span> | |
| [[IMDB]] | <span class="v">41.8</span><span class="sd">±3.7</span> | 42.5 | <span class="d ok">−0.7</span> | |
| [[House]] | <span class="v">56.7</span><span class="sd">±4.0</span> | 56.7 | <span class="d ok">+0.0</span> | |
| [[Pubmed]] | <span class="v">69.5</span><span class="sd">±3.4</span> | 69.1 | <span class="d ok">+0.3</span> | |
| [[AMiner]] | <span class="v">31.8</span><span class="sd">±2.0</span> | 32.1 | <span class="d ok">−0.3</span> | |
| [[DBLP-A]] | <span class="na">—</span> | 69.0 | | blocked-data |
| [[MN-40]] | <span class="na">—</span> | 89.2 | | blocked-data |
| [[20News]] | <span class="na">—</span> | 74.4 | | blocked-data |

## Hyperedge prediction <span class="m">Table 4 · AUROC</span>

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | <span class="v">53.7</span><span class="sd">±2.5</span> | 53.7 | <span class="d ok">+0.0</span> | |
| [[Cora-CA]] | <span class="v">51.8</span><span class="sd">±1.8</span> | 51.6 | <span class="d ok">+0.2</span> | |
| [[IMDB]] | <span class="v">48.2</span><span class="sd">±0.7</span> | 48.2 | <span class="d ok">+0.0</span> | |
| [[House]] | <span class="v">69.7</span><span class="sd">±5.6</span> | 69.7 | <span class="d ok">+0.0</span> | |
| [[Pubmed]] | <span class="v">64.3</span><span class="sd">±2.5</span> | 65.7 | <span class="d ok">−1.4</span> | |
| [[AMiner]] | <span class="v">48.1</span><span class="sd">±1.3</span> | 48.1 | <span class="d ok">+0.0</span> | |
| [[DBLP-P]] | <span class="na">—</span> | 51.2 | | pending |
| [[20News]] | <span class="na">—</span> | 56.0 | | blocked-data |

<div class="hg-legend"><span>우리값 <span class="sd">±표준편차</span></span><span class="d ok">±2 이내</span><span class="d warn">2–5</span><span class="d bad">5 초과</span><span class="lim">OOM</span><span class="lgn">논문이 수치를 못 낸 칸</span><span class="na">—</span><span class="lgn">미실행·보류</span></div>

관련: [[논문 대조]] · [[Home]]
<!-- AUTO:END -->

## 메모


