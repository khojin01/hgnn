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

## 사람과 이어지는 길 — 세 갈래

사람은 노트를 직접 보지 않는다. 아래 세 경로로 본다. **서버는 파일까지만 만들고, claude.ai 에 올리는 일은 세션만 할 수 있다.**

| 경로 | 무엇 | 누가 움직이나 |
|---|---|---|
| 아티팩트 2개 | 관제(HGNN MAIN) · 논문 대조(dms2) | 서버가 파일 생성 → **세션이 둘 다 발행** |
| 디스코드 | 알림(실행 시작·완료·실패) · 조회 · `@지시` | 서버가 직접 (`tools/discord_bot.py`) |
| 옵시디언 | 로컬 PC 가 git 으로 `vault/` 미러 | 서버가 커밋·푸시, 로컬이 pull |

### 아티팩트는 두 개다 — 하나만 올리면 다른 하나가 조용히 낡는다

- **HGNN MAIN (관제)** `CmR71CY6fS8EVtFD8Ce3pY` — 실행 상태·에이전트·연구 노트·지시·커밋
- **HyperGC 재현 대조(dms2)** `McC9c6qoLCw13GmFBqvZkb` — Table 3·4·5 셀 단위 Δ

로컬에서 `python bin/hgnn_build.py --out-dir <디렉터리>` 가 두 HTML 을 한 번에 받는다. 그다음 각자의 URL 로 발행한다.
2026-09-15 에 관제만 올리고 대조를 빼먹어 이틀 낡은 표가 걸려 있었다.

### 지시가 들어오는 길

- **디스코드 `@지시 <내용>`** → `tools/inbox.py` 가 `dashboard/inbox.jsonl` 에 쌓는다. 설정의 `owner` 가 보낸 것만 바로 수행 대상이다.
- **관제 페이지 지시함** → 아티팩트 DB 에 쌓이고, 페이지가 스스로 재발행해 세션을 깨운다. 세션이 그것을 읽어 같은 지시함으로 옮긴다.

**지시함이 유일한 기록이다.** 처리한 것은 `tools/inbox.py done <id>` 로 닫는다. 닫지 않으면 계속 미처리로 남아 다음 세션이 다시 본다.
어느 경로든 글은 파일에 적힐 뿐이고, 실행·중지 판단은 세션이 프로토콜을 읽고 한다. 채팅 글이 셸 명령이 되는 구조는 없다.

### 노트 편집이 돌아오는 길

관제 페이지 연구 노트 탭에서 사람이 `lab/다음 할 일.md` 와 `lab/일지/<날짜>.md` 를 직접 고칠 수 있다.
편집은 아티팩트 DB 의 `notes/todo` · `notes/journal` 에 쌓이고, 세션이 `tools/note_write.py` 로 파일에 반영한다 (stdin JSON, 파일만 쓴다).
할 일 목록은 통째로 교체되므로 항목이 사라졌다면 사람이 지운 것이다.

### 디스코드

`tools/discord_bot.py` 하나가 알림·조회·지시를 다 맡는다. `refresh_all.sh` 가 매분 `notify` 로 상태 변화를 웹훅에 올리고
`ensure-bot` 으로 조회 루프를 살려 둔다. 설정은 `.discord.json` (웹훅 · 토큰 · 채널 · owner · 보고 채널, 저장소에 안 들어간다).
부르는 말은 설정의 `commands` 로 바꾼다. 진행 보고는 `discord_bot.py report` 로 `#order` 채널에 보낸다.
알림은 표준 라이브러리만 쓰고 조회 루프만 `~/.venvs/discord` 의 discord.py 를 쓴다.

### 세션이 깨어나는 법

로컬에서 `bin/hgnn_watch.sh` 를 배경으로 돌리면 30초마다 지시함과 `tools/pulse.py` 의 상태 한 줄을 본다.
미처리 지시가 있거나 상태가 바뀌면 그 줄을 찍고 끝난다 — 그 종료가 곧 알림이다. 조용하면 토큰을 쓰지 않는다.
깨어나면 할 일은 셋이다: 지시 처리 → `inbox.py done`, 결과가 바뀌었으면 아티팩트 **둘 다** 발행, 필요하면 `#order` 에 보고.
