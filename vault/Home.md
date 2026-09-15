---
type: home
updated: 2026-09-15 14:20
tags: [hgnn/overview]
cssclasses: [hg-home]
---

<!-- AUTO:BEGIN -->
# HGNN 실험 노트

<span class="lgn">dms2 가 만들고 GitHub 를 거쳐 여기로 온다 · 갱신 2026-09-15 14:20</span>

## 지금

- [[대시보드]] — 실행 중 실험 · GPU · 최근 실행 · 자동화 프로세스 · 커밋 (1분 갱신)
- [[에이전트]] — clerk / env-builder / env-checker 의 역할과 활성 상태

## 결과

- [[논문 대조]] — HyperGC Table 3·4·5 vs 우리 정식 결과, Δ 배지

- [[Charts]] — 태스크별 순위 차트 (호버로 값 확인)
- [[모델 비교]] — 모델 19개를 일치율·편차로 정렬·필터 (Bases)
- [[데이터셋 비교]] — 데이터셋별 1위 모델 (Bases)

## 모델

- [[AllSet]]
- [[ED-HNN]]
- [[GGD]]
- [[GraphMAE2]]
- [[HGNN]]
- [[HNHN]]
- [[HypeBoy]]
- [[HyperGCL]]
- [[HyperGCN]]
- [[HyperGRL]]
- [[MLP]]
- [[MaskGAE]]
- [[PhenomNN]]
- [[SE-HSSL]]
- [[TriCL]]
- [[UniGCN]]
- [[UniGCN2]]
- [[UniGIN]]
- [[VilLain]]

## 데이터셋

- [[Citeseer]]
- [[Cora-CA]]
- [[IMDB]]
- [[House]]
- [[Pubmed]]
- [[AMiner]]
- [[DBLP-A]]
- [[MN-40]]
- [[20News]]
- [[DBLP-P]]

## 어떻게 갱신되나

| 무엇 | 누가 | 경로 |
|---|---|---|
| 원장·Δ | clerk (10분 루프) → `collector.py` (5분) | `experiment_now.md` → `state.json` |
| 이 노트들 | `tools/vault_build.py` (cron 1분) | `vault/` |
| 로컬 PC 로 | 서버가 변경 시 git push → PC 가 1분마다 pull · 대시보드.md 는 ssh 로 직접 | `hgnn_sync.ps1` |

> 각 노트의 자동 생성 구간(AUTO 주석 사이)만 덮어쓴다. **`## 메모`** 는 보존된다.
<!-- AUTO:END -->

## 메모


