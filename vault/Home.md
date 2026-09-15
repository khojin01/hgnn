---
type: home
updated: 2026-09-15 15:36
tags: [hgnn/home]
---

<!-- AUTO:BEGIN -->
# HGNN 연구 노트북

<small>dms2 의 `vault/` · 클로드가 실험할 때 읽고 쓰는 곳 · 사람은 관제 아티팩트를 본다 · 갱신 2026-09-15 15:36</small>

## 실험 전에

- [[실행 규약]] — 정식 실행 정의 · 분할 · 환경 · 스크립트 규약 · 돌리지 말 것
- [[다음 할 일]] · [[질문]] — 무엇을 왜 하는지
- `protocols/<모델> 실행` — 그 모델의 정식 명령과 함정

## 실험 후에

- `lab/일지/오늘.md` 에 무엇·왜·결과·판단 (템플릿 `_템플릿.md`, 명령 `/lab-log`)
- 새로 안 함정은 해당 `protocols/` 노트의 **함정과 판단** 에

## 사실 (자동 생성 · 손대지 않는다)

- [[논문 대조]] — HyperGC Table 3·4·5 vs 우리 정식 결과
- [[에이전트]] — clerk / env-builder / env-checker
- `knowledge/models/` [[AllSet]] · [[ED-HNN]] · [[GGD]] · [[GraphMAE2]] · [[HGNN]] · [[HNHN]] · [[HypeBoy]] · [[HyperGCL]] · [[HyperGCN]] · [[HyperGRL]] · [[MLP]] · [[MaskGAE]] · [[PhenomNN]] · [[SE-HSSL]] · [[TriCL]] · [[UniGCN]] · [[UniGCN2]] · [[UniGIN]] · [[VilLain]]

## 최근 일지

- [[2026-09-15]]

## 갱신 흐름

| 무엇 | 누가 | 주기 |
|---|---|---|
| 원장·Δ | clerk → `collector.py` | 10분 · 5분 |
| knowledge/ · protocols/ AUTO 구간 · `live.json` | `tools/vault_build.py` | 1분 (내용 바뀔 때만 커밋) |
| lab/ · protocols 의 함정과 판단 | 클로드 (실험할 때) | 그때그때 |
| 로컬 옵시디언 | `hgnn_sync.ps1` git pull | 1분 |
| 관제 아티팩트 | Claude 세션 (온디맨드 · 루프) | 요청 시 · 5분 |
<!-- AUTO:END -->

## 메모


