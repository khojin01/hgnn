#!/usr/bin/env bash
# 대시보드 스냅샷(state.json)을 다시 만든다. cron이 30분마다 호출한다.
#
#   */30 * * * * /home/dms2/hojin_workspace/hgnn/dashboard/refresh.sh
#
# cron은 대화형 셸의 PATH를 물려받지 않으므로 python3를 절대 경로로 부른다.
# 로그는 계속 자라지 않게 꼬리만 남긴다.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON=/home/dms2/miniconda/bin/python3
LOG="$ROOT/dashboard/refresh.log"
LOG_MAX_LINES=400

log() { printf '%s  %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >>"$LOG"; }

# 같은 작업이 겹쳐 도는 것을 막는다. 원장이 커지면 한 번에 몇 초 걸릴 수 있다.
exec 9>"$ROOT/dashboard/.refresh.lock"
if ! flock -n 9; then
  log "SKIP 이전 실행이 아직 돌고 있음"
  exit 0
fi

# 논문 기준값은 PDF가 바뀔 때만 다시 뽑으면 된다. 없을 때만 만든다.
if [[ ! -f "$ROOT/dashboard/paper_reference.json" ]]; then
  log "paper_reference.json 없음 — PDF에서 다시 추출"
  "$PYTHON" "$ROOT/dashboard/paper_reference.py" >>"$LOG" 2>&1 \
    || log "WARN paper_reference.py 실패 — 논문 대조 없이 진행"
fi

output=$("$PYTHON" "$ROOT/dashboard/collector.py" 2>&1)
status=$?
if (( status == 0 )); then
  # collector가 찍는 요약 중 마지막 줄(논문 대조 결과)만 남긴다.
  log "OK $(printf '%s' "$output" | tail -1 | sed 's/^ *//')"
else
  log "FAIL collector.py 종료 코드 $status"
  printf '%s\n' "$output" | tail -5 >>"$LOG"
fi

# 아티팩트용 정적 리포트도 같이 만들어 둔다. 발행은 Claude 도구가 필요하므로
# cron이 못 하지만, 파일을 최신으로 유지해 두면 발행은 한 번의 호출로 끝난다.
if (( status == 0 )); then
  report_out=$("$PYTHON" "$ROOT/dashboard/build_report.py" 2>&1)
  if (( $? == 0 )); then
    log "리포트 $(printf '%s' "$report_out" | grep -m1 '^리포트' | sed 's/^리포트 [^ ]* //') $(printf '%s' "$report_out" | grep -m1 '^대조' | sed 's/^ *//')"
  else
    log "WARN build_report.py 실패"
    printf '%s\n' "$report_out" | tail -3 >>"$LOG"
  fi
fi

# 로그 꼬리만 유지
if [[ -f "$LOG" ]] && (( $(wc -l <"$LOG") > LOG_MAX_LINES )); then
  tail -n "$LOG_MAX_LINES" "$LOG" >"$LOG.tmp" && mv "$LOG.tmp" "$LOG"
fi

exit "$status"
