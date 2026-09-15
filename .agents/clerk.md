# Clerk protocol — hypergraph environment validation

This file is the durable hand-off contract for the three-agent workflow. The
single source of current state is `.agents/env-status/README.md`; append-only
events belong in `.agents/env-status/events.md`.

## 사용자용 보고서 및 smoke 원장

Clerk는 내부 상태 갱신과 별도로, 사용자에게 전달할 보고서를 반드시 한글로
작성한다. 경로와 용도는 다음과 같다.

| 산출물 | 경로 | 갱신 시점 |
|---|---|---|
| 개별 보고서 | `.agents/clerk-reports/개별/` | 모든 의미 있는 hand-off 또는 상태 변경 직후 |
| 5건 통합 보고서 | `.agents/clerk-reports/통합/` | 개별 보고서가 새로 5건 쌓일 때 |
| 보고서 목록/묶음 상태 | `.agents/clerk-reports/README.md` | 개별/통합 보고서 작성 때마다 |
| 모델×데이터셋 결과 매트릭스 | `.agents/clerk-reports/experiment_now.md` | **각 정식 실행 종료·결과 확정 직후** |

> **2026-09-13 정책 변경 (사용자 지시).** smoke 결과는 결과 매트릭스에 기록하지
> 않는다. 단일 seed·짧은 epoch 값은 논문 재현값이 아니다. 정식(`118.sh` 고정
> 설정 · 기본 200 epoch · 20 split/seed) 결과만 표에 올리고, 실행 가능성 확인은
> 로그로만 남기며 매트릭스에는 `— pending`을 둔다. 아래 smoke 관련 지시는
> 이 문단이 우선한다. `smoke_run.md`는 과거 기록으로만 보존한다.

- 개별 보고서는 `YYYYMMDD-HHMM-순번-요약.md`로 이름 붙이고, 제목·본문·상태를
  한글로 쓴다. 원본 로그와 내부 증거 파일은 경로를 링크로 남긴다.
- 개별 보고서에는 최소한 `발생한 문제`, `조치 내용`, `현재 상태`, `다음 담당자`를
  포함한다. 현재 상태는 반드시 `해결됨`, `진행 중`, `해결 불가`, `문제 없음` 중 하나로
  표기한다. `해결 불가`에는 근거와 재검토 조건을 함께 적는다.
- **모든 개별 보고서의 마지막 섹션**은 `전체 모델 task 현황` 표로 끝낸다. 표는 작성
  시점의 `.agents/env-status/README.md`에 있는 전체 모델을 행으로, 아래 세 task를
  열로 하여 누락 없이 표시한다: `노드 분류 (Table 3)`, `하이퍼엣지 예측 (Table 4)`,
  `커뮤니티 탐지 (Table 5)`. 기호는 `O (됨)`=해당 task의 성공 실행 증거가 있음,
  `X (안됨)`=실행 불가·차단·미지원, `△ (해결중)`=미실행·조사·환경/데이터/권한 해결
  대기 중을 뜻한다. 각 셀에는 짧은 근거를 괄호 안에 덧붙인다. 이 표 다음에는 어떤
  본문이나 부록도 추가하지 않는다.
- 통합 보고서는 시간순으로 새 개별 보고서 정확히 5건을 대상으로 작성한다. 파일명은
  `묶음-0001-첫보고서일자-마지막보고서일자.md` 형식을 쓴다. 원본 5건은 삭제하거나
  덮어쓰지 말고, 통합 보고서에 대상 파일 목록과 각 건의 **문제 / 해결됨 / 진행 중 /
  해결 불가** 분류를 표로 정리한다.
- 이미 통합한 보고서는 다음 묶음의 수에 다시 세지 않는다. `README.md`에 마지막 통합
  묶음과 다음 묶음의 대기 건수를 기록한다.
- `.agents/clerk-reports/smoke_run.md`는 저장소 루트의 `smoke_run.md`와 **동일한
  모델×데이터셋 매트릭스 형식**을 유지한다. 태스크별(Table 3 노드 분류 정확도,
  Table 4 엣지 예측 AUROC, Table 5 커뮤니티 탐지 NMI)로 표를 나누고, 행은 모델,
  열은 데이터셋으로 둔다. 결과 셀은 반드시 `내 결과 ± 표준편차 (Δ = 내 평균 −
  HyperGC 논문 평균)`을 사용한다. 정식 결과·smoke·실행 중·대기·데이터 차단·보류·
  O.O.M/O.O.T를 셀 안에서 명확히 구분하고, 결과가 확정될 때마다 해당 셀과 원본
  `smoke_run.md`를 함께 갱신한다. 로그·명령·종료 코드 등 세부 증거는 내부
  `.agents/env-status/` 원장에 보존한다; 매트릭스에는 링크만 둔다.

## Roles and hand-offs

1. `env-builder` creates or repairs the named Conda environment, records the
   exact environment name, Python/CUDA/PyTorch stack, installation command,
   and any unresolved conflict. It then marks the environment `ready_for_check`.
2. `env-checker` runs a minimal smoke test first, followed by the fixed
   configuration in the model's `time_node.sh` (or the documented equivalent).
   It reports command, GPU/device, dataset, exit status, log path, metric and
   failure traceback. A failure must identify the builder action requested.
3. `clerk` updates the current table and appends a dated event after each
   hand-off. It also writes the Korean user report and, for every **formal**
   run, appends `experiment_now.md` with the HyperGC-paper delta. Smoke runs
   are no longer recorded in the result matrix (2026-09-13 user directive):
   keep them in logs only. Match the delta reference to the task's own table —
   Table 3 for node, Table 4 for hyperedge, Table 5 for community. The same
   model differs between tables (GGD Cora-CA: T3 32.2, T4 73.2), so mixing
   them flips the sign. Verify against `dashboard/paper_reference.json`.
   Do not treat a process exit of zero as benchmark
   validation: record performance separately against the applicable HyperGC
   Table 3/4/5.

## Status vocabulary

- `planned`: not yet built/checked
- `building`: environment work in progress
- `ready_for_check`: builder completed an install; checker has not accepted it
- `running`: a check is executing
- `smoke-pass`: imports and a short run succeeded
- `benchmark-pass`: reported metric is plausibly consistent with the cited table
- `failed`: command failed; retain concise error and the requested builder fix
- `blocked`: cannot proceed without a decision/resource
- `skipped`: HyperGC reports O.O.M/O.O.T; record the exact table cell/reason

## Required report format

```
timestamp (KST):
agent: env-builder | env-checker
environment/model:
command:
datasets:
result: status + metric(s), or error summary
evidence: log path / output location
next action + owner:
```

HyperGCL is scheduled only after every other eligible model/dataset has a
terminal status. Never overwrite prior evidence; correct it in a new event.
