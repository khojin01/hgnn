#!/usr/bin/env bash
# vault/ 노트를 다시 만들고, 내용이 바뀐 것만 커밋·푸시한다. cron 이 1분마다 부른다.
#
#   * * * * * /home/dms2/hojin_workspace/hgnn/tools/vault_sync.sh
#
# - 대시보드.md 는 매분 바뀌므로 .gitignore 에 있다. 로컬 PC 가 ssh 로 직접 받아간다.
# - 나머지 노트는 vault_build.py 가 '날짜만 바뀐 경우' 를 스스로 건너뛰므로,
#   여기까지 왔을 때 diff 가 있으면 실제로 값이 바뀐 것이다.
# - origin 이 없으면 커밋만 하고 push 는 건너뛴다 (GitHub 연결 전에도 동작).
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON=/home/dms2/miniconda/bin/python3
LOG="$ROOT/vault/.sync.log"
LOG_MAX=300

log() { printf '%s  %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >>"$LOG"; }

mkdir -p "$ROOT/vault"
exec 9>"$ROOT/vault/.sync.lock"
if ! flock -n 9; then
  log "SKIP 이전 실행이 아직 돌고 있음"
  exit 0
fi

# 1. 노트 생성 (차트는 5분에 한 번만 — matplotlib 이 무겁다)
if (( $(date +%M) % 5 == 0 )); then
  out=$("$PYTHON" "$ROOT/tools/vault_build.py" 2>&1)
else
  out=$("$PYTHON" "$ROOT/tools/vault_build.py" --no-charts 2>&1)
fi
status=$?
if (( status != 0 )); then
  log "FAIL vault_build.py 종료 코드 $status"
  printf '%s\n' "$out" | tail -5 >>"$LOG"
  exit "$status"
fi

# 2. git — 저장소가 아니면 여기서 끝
cd "$ROOT" || exit 1
[[ -d .git ]] || { log "OK $out (git 아님)"; exit 0; }

git add -A >/dev/null 2>&1
if git diff --cached --quiet; then
  log "OK $out · 커밋할 변경 없음"
  exit 0
fi

# 바뀐 파일을 커밋 메시지에 요약한다. 결과가 바뀌면 어떤 모델·데이터셋인지 보이게.
changed=$(git diff --cached --name-only | sed 's#^vault/##' | head -6 | tr '\n' ' ')
n=$(git diff --cached --name-only | wc -l)
msg="vault: $changed"
(( n > 6 )) && msg="$msg… ($n files)"
git commit -q -m "$msg" && log "COMMIT $(git rev-parse --short HEAD) $msg" || { log "FAIL commit"; exit 1; }

if git remote get-url origin >/dev/null 2>&1; then
  if git push -q origin HEAD 2>>"$LOG"; then
    log "PUSH ok"
  else
    log "WARN push 실패 (다음 분에 재시도)"
  fi
fi

if [[ -f "$LOG" ]] && (( $(wc -l <"$LOG") > LOG_MAX )); then
  tail -n "$LOG_MAX" "$LOG" >"$LOG.tmp" && mv "$LOG.tmp" "$LOG"
fi
exit 0
