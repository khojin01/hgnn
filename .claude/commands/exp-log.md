---
description: 서버의 실험 결과를 vault 노트로 갱신한다 (로컬 PC 는 pull_from_server.sh 로 따로 가져감)
allowed-tools: Bash(python tools/exp2vault.py:*), Bash(python3 tools/exp2vault.py:*), Read, Edit, Glob, Grep
---

## 할 일

1. `python3 tools/exp2vault.py --report` 를 실행한다.
   - `$ARGUMENTS` 에 `--vault` 등이 있으면 그대로 전달한다.

2. **"해석 실패" 가 0이 아니면 반드시 보고한다.**
   결과 파일에 새 형식이 생겼다는 뜻이므로, 실패한 줄을 보여주고
   `tools/exp2vault.py` 의 정규식을 고칠지 물어본다.

3. "갱신된 노트" 가 0이 아니면, 어떤 조합의 수치가 바뀌었는지 확인해 보고한다.
   - 갱신된 노트 이름으로 `vault/runs/<dataset>-<model>-<task>.md` 를 읽어
     frontmatter 의 `value` / `best` 를 확인한다.

4. 보고는 짧게.
   - 무엇이 바뀌었는지 (데이터셋 / 모델 / 태스크, 값)
   - 눈에 띄는 것 한두 줄 (처음으로 1위, 분산이 비정상적으로 큼, 값이 떨어짐 등)
   - 바뀐 게 없으면 "변경 없음" 한 줄로 끝낸다. 억지로 관찰을 지어내지 않는다.

## 하지 말 것

- **자동 생성 구간(AUTO:BEGIN ~ AUTO:END 주석 사이)을 직접 편집하지 않는다.** 다음 실행 때 덮어쓰인다.
  해석이나 메모는 그 블록 **아래 `## 메모`** 섹션에만 쓴다.
- 결과 수치를 추정하거나 보간하지 않는다. 파일에 있는 값만 옮긴다.
- 사용자가 요청하지 않으면 `## 메모` 에 자동으로 쓰지 않는다. 쓸지 먼저 물어본다.

## 구조

- 이 서버의 `~/hojin_workspace/vault` 는 **서버에서 확인용**이다. git 을 쓰지 않는다.
- 사용자의 로컬 PC 는 `tools/pull_from_server.sh` 로 `results/`·`logs/` 원본만 rsync 해 가서
  자기 쪽에서 노트를 생성한다. **사용자의 메모는 로컬 PC 에만 있고 서버로 오지 않는다.**
  따라서 이 서버에서 vault 를 고쳐도 사용자 메모에 영향이 없다.
- `pair` 태스크는 원본에 태스크 표기가 없어 node/edge 구분이 안 된 항목이다. 수치를 인용할 때 주의한다.
- `node`=분류 정확도, `edge`=하이퍼엣지 예측 점수, `cluster`=NMI, `time`=초 로 가정하고 있다.
