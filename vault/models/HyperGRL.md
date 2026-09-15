---
type: model
datasets: 9
updated: 2026-09-15 13:09
tags: [hgnn/model]
---

<!-- AUTO:BEGIN -->
# HyperGRL

<span class="lgn">코드 `HyperGRL/` · 결과 `results/result_*_HyperGRL_*.txt` · 갱신 2026-09-15 13:09</span>

<div class="hg-cards"><div class="hg-card"><span class="k">NC 일치</span><span class="big">2/2</span><span class="note">|Δ| 중앙값 0.20</span></div><div class="hg-card"><span class="k">HP 일치</span><span class="big">0/0</span><span class="note">정식 결과 없음</span></div><div class="hg-card"><span class="k">최대 편차</span><span class="big">+0.2</span><span class="note">노드 분류 · Cora-CA</span></div></div>

## Node classification <span class="m">Table 3 · Accuracy</span>

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | <span class="lim">OOM</span> | 35.1 | | O.O.M (batch-1 retry) |
| [[Cora-CA]] | <span class="v">42.0</span><span class="sd">±6.7</span> | 41.8 | <span class="d ok">+0.2</span> | |
| [[IMDB]] | <span class="lim">OOM</span> | 35.7 | | O.O.M (batch-1 retry) |
| [[House]] | <span class="v">50.6</span><span class="sd">±1.8</span> | 50.4 | <span class="d ok">+0.2</span> | |
| [[Pubmed]] | <span class="lim">OOM</span> | 50.2 | | O.O.M (batch-1 retry) |
| [[AMiner]] | <span class="lim">OOM</span> | 28.0 | | O.O.M (batch-1 retry) |
| [[DBLP-A]] | <span class="na">—</span> | 41.1 | | blocked-data |
| [[MN-40]] | <span class="na">—</span> | 89.4 | | blocked-data |
| [[20News]] | <span class="na">—</span> | — | | blocked-data |

## Hyperedge prediction <span class="m">Table 4 · AUROC</span>

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Citeseer]] | <span class="na">—</span> | 83.2 | | unavailable: EP implementation missing |
| [[Cora-CA]] | <span class="na">—</span> | 80.0 | | unavailable: EP implementation missing |
| [[IMDB]] | <span class="na">—</span> | 54.7 | | unavailable: EP implementation missing |
| [[House]] | <span class="na">—</span> | 88.2 | | unavailable: EP implementation missing |
| [[Pubmed]] | <span class="na">—</span> | 78.3 | | unavailable: EP implementation missing |
| [[AMiner]] | <span class="na">—</span> | 81.5 | | unavailable: EP implementation missing |
| [[DBLP-P]] | <span class="na">—</span> | 88.2 | | unavailable: EP implementation missing |
| [[20News]] | <span class="lim">OOT</span> | — | | O.O.T skip |

## Community detection <span class="m">Table 5 · NMI</span>

| 데이터셋 | 우리 | 논문 | Δ | 비고 |
|---|---:|---:|---:|---|
| [[Cora-CA]] | <span class="na">—</span> | 34.5 | | pending |
| [[DBLP-P]] | <span class="na">—</span> | 57.4 | | pending |
| [[20News]] | <span class="lim">OOT</span> | — | | O.O.T skip |

<div class="hg-legend"><span>우리값 <span class="sd">±표준편차</span></span><span class="d ok">±2 이내</span><span class="d warn">2–5</span><span class="d bad">5 초과</span><span class="lim">OOM</span><span class="lgn">논문이 수치를 못 낸 칸</span><span class="na">—</span><span class="lgn">미실행·보류</span></div>

관련: [[논문 대조]] · [[Home]]
<!-- AUTO:END -->

## 메모


