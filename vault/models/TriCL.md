---
type: model
datasets: 9
updated: 2026-09-15 13:09
tags: [hgnn/model]
---

<!-- AUTO:BEGIN -->
# TriCL

<span class="lgn">코드 `TriCL/` · 결과 `results/result_*_TriCL_*.txt` · 갱신 2026-09-15 13:09</span>

<div class="hg-cards"><div class="hg-card"><span class="k">NC 일치</span><span class="big">6/6</span><span class="note">|Δ| 중앙값 1.00</span></div><div class="hg-card"><span class="k">HP 일치</span><span class="big">1/6</span><span class="note">|Δ| 중앙값 4.20</span></div><div class="hg-card"><span class="k">최대 편차</span><span class="big">−5.4</span><span class="note">하이퍼엣지 예측 · House</span></div></div>

## Node classification <span class="m">Table 3 · Accuracy</span>

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | <span class="v">52.7</span><span class="sd">±13.9</span> | 53.0 | <span class="d ok">−0.3</span> | |
| [[Cora-CA]] | <span class="v">61.9</span><span class="sd">±5.8</span> | 63.4 | <span class="d ok">−1.5</span> | |
| [[IMDB]] | <span class="v">47.9</span><span class="sd">±5.3</span> | 47.5 | <span class="d ok">+0.4</span> | |
| [[House]] | <span class="v">63.5</span><span class="sd">±7.4</span> | 65.2 | <span class="d ok">−1.7</span> | |
| [[Pubmed]] | <span class="v">75.0</span><span class="sd">±3.4</span> | 74.0 | <span class="d ok">+1.0</span> | |
| [[AMiner]] | <span class="v">33.6</span><span class="sd">±2.5</span> | 34.6 | <span class="d ok">−1.0</span> | |
| [[DBLP-A]] | <span class="na">—</span> | 80.3 | | blocked-data |
| [[MN-40]] | <span class="na">—</span> | 93.0 | | blocked-data |
| [[20News]] | <span class="na">—</span> | 73.8 | | blocked-data |

## Hyperedge prediction <span class="m">Table 4 · AUROC</span>

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | <span class="v">89.1</span><span class="sd">±1.3</span> | 90.5 | <span class="d ok">−1.4</span> | |
| [[Cora-CA]] | <span class="v">85.0</span><span class="sd">±2.0</span> | 87.8 | <span class="d warn">−2.8</span> | |
| [[IMDB]] | <span class="v">56.8</span><span class="sd">±3.8</span> | 58.9 | <span class="d warn">−2.1</span> | |
| [[House]] | <span class="v">84.6</span><span class="sd">±3.5</span> | 90.0 | <span class="d bad">−5.4</span> | |
| [[Pubmed]] | <span class="v">96.1</span><span class="sd">±0.6</span> | 91.9 | <span class="d warn">+4.2</span> | |
| [[AMiner]] | <span class="v">86.0</span><span class="sd">±0.9</span> | 90.4 | <span class="d warn">−4.4</span> | |
| [[DBLP-P]] | <span class="na">—</span> | 94.8 | | pending |
| [[20News]] | <span class="na">—</span> | 98.2 | | blocked-data |

<div class="hg-legend"><span>우리값 <span class="sd">±표준편차</span></span><span class="d ok">±2 이내</span><span class="d warn">2–5</span><span class="d bad">5 초과</span><span class="lim">OOM</span><span class="lgn">논문이 수치를 못 낸 칸</span><span class="na">—</span><span class="lgn">미실행·보류</span></div>

관련: [[논문 대조]] · [[Home]]
<!-- AUTO:END -->

## 메모


