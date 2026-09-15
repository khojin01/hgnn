---
type: overview
updated: 2026-09-15 15:02
tags: [hgnn/overview]
cssclasses: [hg-wide, wide-page]
---

<!-- AUTO:BEGIN -->
# 차트

<small>clerk 원장의 정식 결과 · 막대에 마우스를 올리면 값이 보인다 · 갱신 2026-09-15 15:02</small>

## Node classification — Accuracy · 데이터셋 6개 평균

```chart
type: bar
labels: [HypeBoy, PhenomNN, TriCL, SE-HSSL, GraphMAE2, MaskGAE, UniGCN2, HNHN, AllSet, UniGIN, HGNN, HyperGRL, UniGCN, ED-HNN, MLP, HyperGCN, VilLain, GGD, HyperGCL]
series:
  - title: 우리
    data: [58.2, 57.9, 55.8, 54.8, 53.2, 52.2, 50.1, 49.0, 47.8, 46.7, 46.6, 46.3, 45.9, 44.6, 44.3, 42.2, 40.3, 36.9, 29.8]
  - title: 논문
    data: [58.2, 57.3, 56.3, 53.7, 53.6, 53.4, 50.0, 49.6, 48.4, 47.4, 46.1, 46.1, 46.0, 44.4, 44.1, 42.3, 41.5, 41.8, 56.3]
tension: 0.2
width: 100%
labelColors: false
fill: false
beginAtZero: false
legend: true
stacked: false
height: 320px
```

> [!note]- 데이터셋별 히트맵 (PNG)
> ![[node-heatmap-light.png]]
>
> 다크 테마에서는 같은 이름의 `-dark.png` 를 쓰면 된다.

## Hyperedge prediction — AUROC · 데이터셋 6개 평균

```chart
type: bar
labels: [HypeBoy, TriCL, SE-HSSL, MaskGAE, GraphMAE2, MLP, VilLain, HGNN, HyperGCN, UniGCN, UniGIN, HNHN, UniGCN2, ED-HNN, HyperGCL, PhenomNN, AllSet, GGD]
series:
  - title: 우리
    data: [83.6, 82.9, 82.1, 81.4, 74.0, 65.2, 64.9, 61.1, 60.8, 56.3, 56.2, 56.0, 55.8, 54.5, 54.3, 54.1, 51.5, 49.1]
  - title: 논문
    data: [83.7, 84.9, 82.4, 81.5, 73.9, 65.3, 65.0, 61.0, 60.9, 56.6, 56.1, 56.2, 55.8, 54.4, 71.3, 53.9, 51.7, 76.4]
tension: 0.2
width: 100%
labelColors: false
fill: false
beginAtZero: false
legend: true
stacked: false
height: 320px
```

> [!note]- 데이터셋별 히트맵 (PNG)
> ![[edge-heatmap-light.png]]
>
> 다크 테마에서는 같은 이름의 `-dark.png` 를 쓰면 된다.

관련: [[논문 대조]] · [[모델 비교]] · [[Home]]
<!-- AUTO:END -->

## 메모


