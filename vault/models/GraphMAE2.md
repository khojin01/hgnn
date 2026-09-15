---
type: model
datasets: 9
updated: 2026-09-15 13:09
tags: [hgnn/model]
---

<!-- AUTO:BEGIN -->
# GraphMAE2

<span class="lgn">코드 `GraphMAE2/` · 결과 `results/result_*_GraphMAE2_*.txt` · 갱신 2026-09-15 13:09</span>

<div class="hg-cards"><div class="hg-card"><span class="k">NC 일치</span><span class="big">6/6</span><span class="note">|Δ| 중앙값 0.40</span></div><div class="hg-card"><span class="k">HP 일치</span><span class="big">6/6</span><span class="note">|Δ| 중앙값 0.20</span></div><div class="hg-card"><span class="k">최대 편차</span><span class="big">−0.9</span><span class="note">노드 분류 · IMDB</span></div></div>

## Node classification <span class="m">Table 3 · Accuracy</span>

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | <span class="v">51.7</span><span class="sd">±12.9</span> | 51.7 | <span class="d ok">+0.0</span> | |
| [[Cora-CA]] | <span class="v">64.0</span><span class="sd">±5.8</span> | 64.3 | <span class="d ok">−0.3</span> | |
| [[IMDB]] | <span class="v">44.7</span><span class="sd">±4.2</span> | 45.6 | <span class="d ok">−0.9</span> | |
| [[House]] | <span class="v">52.0</span><span class="sd">±3.2</span> | 52.4 | <span class="d ok">−0.4</span> | |
| [[Pubmed]] | <span class="v">72.2</span><span class="sd">±4.7</span> | 72.6 | <span class="d ok">−0.4</span> | |
| [[AMiner]] | <span class="v">34.8</span><span class="sd">±2.4</span> | 34.7 | <span class="d ok">+0.1</span> | |
| [[DBLP-A]] | <span class="na">—</span> | 77.2 | | blocked-data |
| [[MN-40]] | <span class="na">—</span> | 90.6 | | blocked-data |
| [[20News]] | <span class="na">—</span> | 71.8 | | blocked-data |

## Hyperedge prediction <span class="m">Table 4 · AUROC</span>

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | <span class="v">78.1</span><span class="sd">±2.4</span> | 78.2 | <span class="d ok">−0.1</span> | |
| [[Cora-CA]] | <span class="v">74.7</span><span class="sd">±2.9</span> | 74.7 | <span class="d ok">+0.0</span> | |
| [[IMDB]] | <span class="v">47.4</span><span class="sd">±1.0</span> | 47.2 | <span class="d ok">+0.2</span> | |
| [[House]] | <span class="v">71.8</span><span class="sd">±5.6</span> | 71.6 | <span class="d ok">+0.2</span> | |
| [[Pubmed]] | <span class="v">93.9</span><span class="sd">±1.8</span> | 93.6 | <span class="d ok">+0.3</span> | |
| [[AMiner]] | <span class="v">78.1</span><span class="sd">±0.9</span> | 78.1 | <span class="d ok">+0.0</span> | |
| [[DBLP-P]] | <span class="na">—</span> | 92.7 | | pending |
| [[20News]] | <span class="na">—</span> | 87.0 | | blocked-data |

<div class="hg-legend"><span>우리값 <span class="sd">±표준편차</span></span><span class="d ok">±2 이내</span><span class="d warn">2–5</span><span class="d bad">5 초과</span><span class="lim">OOM</span><span class="lgn">논문이 수치를 못 낸 칸</span><span class="na">—</span><span class="lgn">미실행·보류</span></div>

관련: [[논문 대조]] · [[Home]]
<!-- AUTO:END -->

## 메모


