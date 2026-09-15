# hgnn — 하이퍼그래프 벤치마크 재현 (HyperGC, KDD ’26)

이 레포에서 실험을 돌리는 Claude Code 는 `vault/` 를 연구 노트북으로 쓴다.
사람은 노트를 직접 보지 않고 Claude 아티팩트(관제)로 본다. 그러니 노트는 **다음 세션의 클로드가 읽기 좋게** 쓴다.

## 실험 전에 반드시 읽는다

1. `vault/protocols/실행 규약.md` — 정식 실행 정의, 분할 계약, 환경, 스크립트 규약, 돌리지 말 것
2. `vault/lab/다음 할 일.md` · `vault/lab/질문.md` — 지금 무엇을 왜 하는지
3. 돌릴 모델의 `vault/protocols/<모델> 실행.md` — 정식 명령과 **함정과 판단**
4. 필요하면 `vault/knowledge/models/<모델>.md` — 지금까지의 결과와 논문 Δ

전부 읽지 않는다. 모델 하나를 돌리면 그 모델의 노트 두 개면 된다.

## 실험 후에 반드시 쓴다

- `vault/lab/일지/YYYY-MM-DD.md` — 무엇을·왜·결과·판단. 템플릿 `_템플릿.md`. 같은 날이면 이어 쓴다. `/lab-log` 로 초안을 만들 수 있다.
- 새로 안 함정은 `vault/protocols/<모델> 실행.md` 의 **함정과 판단** 아래에. 실패 원인·고친 것·다시 가지 말 길.
- `다음 할 일` 은 체크하고, 새 항목은 위에. `질문` 은 답을 찾으면 근거 경로와 함께 닫는다.

## 손대지 않는 것

- `vault/knowledge/` 전체와 모든 노트의 `AUTO:BEGIN ~ AUTO:END` 구간 — `tools/vault_build.py` 가 1분마다 덮어쓴다.
- 결과 수치를 노트에 직접 적지 않는다. `results/*.txt` 에 남기면 clerk → collector → vault_build 가 올린다.
  올라오지 않으면 `dashboard/pipeline.log` 를 본다.
- 정식 결과 파일(`results/result_<dataset>_<Dir>_<task>.txt`)을 지우거나 덮어쓰지 않는다. 재실행은 새 run_id 로.

## 실행 규칙 요약

- 정식 = `<모델>/118.sh` 고정 설정 · 200 epoch · 20 seed. 그 외는 smoke 이며 원장에 올리지 않는다.
- 노드 분류 분할 `data_split_0.01.pickle` (1/1/98). `data_split_118.pickle` 은 Table 3 대비 불가.
- 실행 스크립트는 `.agents/run-scripts/` 에 두고 `run_id`, `status.tsv`, `timeout 24h`, `SKIP_EXISTING` 규약을 따른다.
- 논문이 O.O.M / O.O.T 로 보고한 칸은 돌리지 않는다 (`실행 규약.md` 목록).
- GPU 2장(RTX 5080 16GB). 다른 실행이 돌고 있으면 `nvidia-smi` 로 확인하고 빈 GPU 를 쓴다.

## 에이전트

- `clerk` — 결과 원장 `.agents/clerk-reports/experiment_now.md` 관리. cron 파이프라인 `tools/refresh_all.sh` 가 1분마다 갱신한다.
- `env-builder` / `env-checker` — 환경 구축·검증. 정의서 `.agents/*.md`. 정식 실행 전 게이트 `*-check.ok`.

## 볼트 구조

```
vault/
  CLAUDE.md · Home.md
  knowledge/   논문 대조 · models/ · datasets/ · 에이전트   ← 자동, 읽기만
  protocols/   실행 규약 · <모델> 실행                    ← AUTO + 함정과 판단(쓴다)
  lab/         일지/ · 다음 할 일 · 질문                   ← 클로드가 쓴다
```

로컬 PC 의 옵시디언은 이 `vault/` 를 git 으로 미러한다. 거기 `papers/` 는 사람의 공부 기록이라 이 레포에 없다.

## 관제 아티팩트에서 오는 편집

사용자는 관제 아티팩트(연구 노트 탭)에서 `lab/다음 할 일.md` 의 체크리스트와 `lab/일지/<날짜>.md` 를 직접 고칠 수 있다.
그 편집은 아티팩트 DB 의 `notes/todo` · `notes/journal` 에 쌓이고, 관제 갱신 루프가 `tools/note_write.py` 로 파일에 반영한다.
`note_write.py` 는 stdin 으로 JSON 을 받아 파일만 쓴다. 할 일 목록은 통째로 교체되므로, 항목을 지우거나 순서를 바꾸는 편집은 사용자가 한 것이다.
