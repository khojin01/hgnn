#!/usr/bin/env bash
# 실험 파이프라인 한 바퀴. cron 이 1분마다 부른다.
#
#   * * * * * /home/dms2/hojin_workspace/hgnn/tools/refresh_all.sh
#
# 순서가 곧 의존 관계다. 예전에는 이 네 단계가 각자 다른 주기로 돌아
# collector 가 clerk 보다 먼저 도는 경우가 있었다. 이제 한 줄로 이어서 돈다.
#
#   1 clerk_refresh.py  results/ · full-runs → .agents/clerk-reports/experiment_now.md (원장)
#   2 collector.py      원장 → dashboard/state.json (+ 논문 기준값 대조)
#   3 build_report.py   state.json → dashboard/hypergc-report.html
#   4 vault_build.py    state.json · 서버 상태 → vault/ 노트 · dashboard/live.json
#   5 git               내용이 바뀐 노트만 커밋·푸시
#
# 네 단계를 합쳐 0.3초쯤 걸린다. flock 으로 겹침을 막고, 앞 단계가 실패하면 멈춘다.
# 로그는 dashboard/pipeline.log 꼬리만 남긴다.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON=/home/dms2/miniconda/bin/python3
LOG="$ROOT/dashboard/pipeline.log"
LOG_MAX=400

log() { printf '%s  %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >>"$LOG"; }
trim() { [[ -f "$LOG" ]] && (( $(wc -l <"$LOG") > LOG_MAX )) && { tail -n "$LOG_MAX" "$LOG" >"$LOG.tmp" && mv "$LOG.tmp" "$LOG"; }; return 0; }

mkdir -p "$ROOT/dashboard"
exec 9>"$ROOT/dashboard/.pipeline.lock"
if ! flock -n 9; then
  log "SKIP 이전 실행이 아직 돌고 있음"
  exit 0
fi

run() {  # run <이름> <스크립트> [인자…] — 출력은 $OUT, 실패하면 스크립트를 멈춘다
  local name="$1"; shift
  local status
  OUT=$("$PYTHON" "$@" 2>&1); status=$?
  if (( status != 0 )); then
    log "FAIL $name 종료 코드 $status"
    echo "$OUT" | tail -5 >>"$LOG"
    trim
    exit "$status"
  fi
}

# 논문 기준값은 PDF 가 바뀔 때만 다시 뽑으면 된다. 없을 때만 만든다.
[[ -f "$ROOT/dashboard/paper_reference.json" ]] || \
  "$PYTHON" "$ROOT/dashboard/paper_reference.py" >>"$LOG" 2>&1 || log "WARN paper_reference.py 실패 — 논문 대조 없이 진행"

run clerk_refresh "$ROOT/.agents/run-scripts/clerk_refresh.py"
run collector     "$ROOT/dashboard/collector.py"
collect=$(printf '%s' "$OUT" | tail -1 | sed 's/^ *//')
run build_report  "$ROOT/dashboard/build_report.py"
run vault_build   "$ROOT/tools/vault_build.py"
build=$OUT

# 사용 설명서는 .claude/ 가 원본이다. 옵시디언은 vault/ 만 보므로 바뀌었을 때만 복사한다.
# (사본을 두 군데서 고치면 어긋난다 — 고칠 때는 .claude/ 쪽을 고친다.)
cp -u "$ROOT/.claude/사용 설명서.md" "$ROOT/vault/사용 설명서.md" 2>/dev/null || true

# 디스코드 — .discord.json 이 있을 때만 움직인다. 없으면 두 줄 다 조용히 지나간다.
"$PYTHON" "$ROOT/tools/discord_bot.py" notify >/dev/null 2>>"$LOG"
"$PYTHON" "$ROOT/tools/discord_bot.py" ensure-bot >/dev/null 2>>"$LOG"

# git — 저장소가 아니면 여기서 끝.
# vault_build.py 가 '날짜만 바뀐 경우' 를 스스로 건너뛰므로, diff 가 있으면 실제로 값이 바뀐 것이다.
cd "$ROOT" || exit 1
[[ -d .git ]] || { log "OK $collect · $build (git 아님)"; trim; exit 0; }

git add -A >/dev/null 2>&1
if git diff --cached --quiet; then
  log "OK $collect · $build · 커밋할 변경 없음"
  trim; exit 0
fi

changed=$(git diff --cached --name-only | sed 's#^vault/##' | head -6 | tr '\n' ' ')
n=$(git diff --cached --name-only | wc -l)
msg="vault: $changed"
(( n > 6 )) && msg="$msg… ($n files)"
if git commit -q -m "$msg"; then
  log "COMMIT $(git rev-parse --short HEAD) $msg"
else
  log "FAIL commit"; trim; exit 1
fi

if git remote get-url origin >/dev/null 2>&1; then
  git push -q origin HEAD 2>>"$LOG" && log "PUSH ok" || log "WARN push 실패 (다음 분에 재시도)"
fi
trim
exit 0
