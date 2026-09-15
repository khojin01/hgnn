---
type: model
datasets: 9
updated: 2026-09-15 13:09
tags: [hgnn/model]
---

<!-- AUTO:BEGIN -->
# HyperGCN

<span class="lgn">코드 `HyperGCN/` · 결과 `results/result_*_HyperGCN_*.txt` · 갱신 2026-09-15 13:09</span>

<div class="hg-cards"><div class="hg-card"><span class="k">NC 일치</span><span class="big">6/6</span><span class="note">|Δ| 중앙값 0.00</span></div><div class="hg-card"><span class="k">HP 일치</span><span class="big">6/6</span><span class="note">|Δ| 중앙값 0.10</span></div><div class="hg-card"><span class="k">최대 편차</span><span class="big">−0.4</span><span class="note">노드 분류 · AMiner</span></div></div>

## Node classification <span class="m">Table 3 · Accuracy</span>

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | <span class="v">33.7</span><span class="sd">±7.3</span> | 33.8 | <span class="d ok">−0.1</span> | |
| [[Cora-CA]] | <span class="v">45.0</span><span class="sd">±9.5</span> | 45.0 | <span class="d ok">+0.0</span> | |
| [[IMDB]] | <span class="v">40.6</span><span class="sd">±3.2</span> | 40.6 | <span class="d ok">+0.0</span> | |
| [[House]] | <span class="v">48.2</span><span class="sd">±0.9</span> | 48.2 | <span class="d ok">+0.0</span> | |
| [[Pubmed]] | <span class="v">59.3</span><span class="sd">±15.2</span> | 59.3 | <span class="d ok">+0.0</span> | |
| [[AMiner]] | <span class="v">26.4</span><span class="sd">±2.9</span> | 26.8 | <span class="d ok">−0.4</span> | |
| [[DBLP-A]] | <span class="na">—</span> | 64.3 | | blocked-data |
| [[MN-40]] | <span class="na">—</span> | 57.8 | | blocked-data |
| [[20News]] | <span class="na">—</span> | 71.7 | | blocked-data |

## Hyperedge prediction <span class="m">Table 4 · AUROC</span>

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | <span class="v">54.9</span><span class="sd">±2.1</span> | 54.9 | <span class="d ok">+0.0</span> | |
| [[Cora-CA]] | <span class="v">48.9</span><span class="sd">±1.6</span> | 49.3 | <span class="d ok">−0.4</span> | |
| [[IMDB]] | <span class="v">48.4</span><span class="sd">±1.9</span> | 48.4 | <span class="d ok">+0.0</span> | |
| [[House]] | <span class="v">87.7</span><span class="sd">±2.5</span> | 87.7 | <span class="d ok">+0.0</span> | |
| [[Pubmed]] | <span class="v">74.2</span><span class="sd">±0.6</span> | 74.1 | <span class="d ok">+0.1</span> | |
| [[AMiner]] | <span class="v">50.6</span><span class="sd">±2.6</span> | 50.8 | <span class="d ok">−0.2</span> | |
| [[DBLP-P]] | <span class="na">—</span> | 53.9 | | pending |
| [[20News]] | <span class="na">—</span> | 55.6 | | blocked-data |

<div class="hg-legend"><span>우리값 <span class="sd">±표준편차</span></span><span class="d ok">±2 이내</span><span class="d warn">2–5</span><span class="d bad">5 초과</span><span class="lim">OOM</span><span class="lgn">논문이 수치를 못 낸 칸</span><span class="na">—</span><span class="lgn">미실행·보류</span></div>

관련: [[논문 대조]] · [[Home]]
<!-- AUTO:END -->

## 메모


