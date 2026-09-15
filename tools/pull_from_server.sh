#!/usr/bin/env bash
# 【로컬 PC 에서 실행한다. 서버가 아니다.】
#
# 연구실 서버에서 실험 결과 원본만 받아와, 로컬에서 Obsidian 노트를 생성한다.
# git 도 클라우드도 쓰지 않는다. ssh + rsync 만 있으면 된다.
#
# 메모는 로컬 vault 에만 존재하고 서버로 가지 않으므로 덮어써질 위험이 없다.
#
# 이 서버의 sshd 는 22 가 아니라 221 포트를 쓴다.
# VSCode Remote-SSH 로 접속 중이라면 ~/.ssh/config 에 이미 항목이 있을 것이다.
# 그 별칭을 쓰면 포트를 따로 줄 필요가 없다:
#
#   SERVER=<VSCode에서 쓰는 호스트명> ~/bin/pull_from_server.sh
#
# 별칭 없이 쓸 때:
#   ~/bin/pull_from_server.sh                     # 아래 기본값 사용 (221 포트)
#   SERVER=dms2@10.198.137.172 PORT=221 ~/bin/pull_from_server.sh
#
# 최초 1회 (로컬 PC 에서):
#   scp -P 221 dms2@10.198.137.172:/home/dms2/hojin_workspace/hgnn/tools/{pull_from_server.sh,exp2vault.py} ~/bin/
#   chmod +x ~/bin/pull_from_server.sh

set -uo pipefail

SERVER="${SERVER-dms2@10.198.137.172}"
PORT="${PORT:-221}"
REMOTE="${REMOTE:-/home/dms2/hojin_workspace/hgnn}"
MIRROR="${MIRROR:-$HOME/hgnn-mirror}"     # 서버 결과의 로컬 사본
VAULT="${VAULT:-$HOME/hgnn-vault}"        # Obsidian 으로 여는 폴더
SCRIPT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/exp2vault.py"

command -v rsync >/dev/null || { echo "rsync 가 필요합니다." >&2; exit 1; }
[[ -f "$SCRIPT" ]] || { echo "exp2vault.py 가 옆에 있어야 합니다: $SCRIPT" >&2; exit 1; }

# SERVER 가 비어 있으면 REMOTE 를 로컬 경로로 본다 (서버에서 직접 돌릴 때 / 테스트용)
SRC="${SERVER:+$SERVER:}$REMOTE"
RSH=()
[[ -n "$SERVER" ]] && RSH=(-e "ssh -p $PORT")

mkdir -p "$MIRROR"

echo "== 결과 원본 받기: ${SERVER:-로컬}${SERVER:+ (포트 $PORT)} =="
# 결과와 로그만. 학습 체크포인트나 데이터 텐서는 받지 않는다.
rsync -az --delete "${RSH[@]}" "$SRC/results/" "$MIRROR/results/" || exit 1
rsync -az --delete "${RSH[@]}" "$SRC/logs/"    "$MIRROR/logs/"    || exit 1
# data/ 는 데이터셋 이름 목록으로만 쓰이므로 디렉토리 구조만 받는다
rsync -az --delete "${RSH[@]}" --include='*/' --exclude='*' \
  "$SRC/data/" "$MIRROR/data/" || exit 1
echo "   results $(ls "$MIRROR/results" | wc -l)개 · logs $(ls "$MIRROR/logs" | wc -l)개"

echo
echo "== 노트 생성 =="
python3 "$SCRIPT" --repo "$MIRROR" --vault "$VAULT" "$@" || exit 1

echo
echo "완료. Obsidian 에서 $VAULT 를 열면 됩니다."
echo "메모는 각 노트의 '## 메모' 에 쓰세요. 다시 실행해도 보존됩니다."
