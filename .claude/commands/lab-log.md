---
description: 오늘의 실험 일지 초안을 만든다 (status.tsv · results · 원장 변화를 모아 lab/일지/YYYY-MM-DD.md 에)
allowed-tools: Bash(git *), Bash(ls *), Bash(cat *), Bash(tail *), Bash(find *), Bash(grep *), Bash(date *), Read, Write, Edit, Glob, Grep
---

## 할 일

1. 오늘 날짜(KST)로 `vault/lab/일지/YYYY-MM-DD.md` 가 있으면 읽고, 없으면 `_템플릿.md` 로 만든다.
2. 마지막 일지 이후 바뀐 것을 모은다.
   - `.agents/env-status/full-runs/*/status.tsv` 에 새로 붙은 줄 (실행 · 데이터셋 · 상태)
   - `results/` 에서 수정 시각이 마지막 일지보다 늦은 파일
   - `.agents/clerk-reports/experiment_now.md` 의 "Latest formal completions" 항목 변화
   - `git log --since=<마지막 일지 날짜>` 의 커밋 (vault 자동 커밋 제외)
3. 일지에 **한 일 / 결과 / 판단** 을 채운다. 수치는 결과 파일 경로와 함께. 판단은 근거가 있는 것만 — 없으면 "미확인" 이라고 쓴다.
4. `다음 할 일` 에서 끝난 항목을 체크하고, 새로 생긴 일을 위에 추가한다. `질문` 에 답이 생겼으면 근거와 함께 닫는다.
5. 새로 안 함정이 있으면 해당 `protocols/<모델> 실행.md` 의 **함정과 판단** 에 한 줄 추가한다.

## 하지 말 것

- `knowledge/` 와 AUTO 구간을 편집하지 않는다.
- 수치를 추정하지 않는다. 파일에 있는 값만 옮긴다.
- 일지를 길게 쓰지 않는다. 다음 세션의 클로드가 1분 안에 읽을 분량.
