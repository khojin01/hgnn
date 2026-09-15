#!/usr/bin/env python3
"""`.agents` 원장 상태 → VS Code CodexEconPixel 확장의 픽셀 오피스.

확장은 자기 워크스페이스 안에서 **실제로 돌고 있는** Codex 세션만 캐릭터로
띄운다. 이 저장소의 세 role agent(env-builder / env-checker / clerk)는 그런
세션이 아니라 Markdown 원장으로 상태를 주고받으므로, 확장 입장에서는 존재하지
않는다. 이 브릿지가 그 간극을 메운다.

## 어떻게 붙는가

이 fork의 확장에는 훅 HTTP 서버가 **없다**. `server/src/server.ts`가 저장소에
남아 있지만 `src/extension.ts`가 import하지 않고, 빌드 산출물에도 들어가지
않는다. 확장이 에이전트를 발견하는 유일한 경로는 Codex 세션 파일 감시다:

    ~/.codex/sessions/**/*.jsonl

`listActiveCodexSessions()`가 각 파일의 첫 줄을 `session_meta`로 읽어
`payload.cwd`가 워크스페이스 안이고 mtime이 10분 이내면 캐릭터로 채택한다.
그래서 브릿지는 에이전트마다 그 형식의 세션 파일을 하나씩 만들고, 원장 상태가
바뀔 때마다 거기에 레코드를 덧붙인다.

    작업 시작  → response_item / function_call     캐릭터가 타이핑
    작업 종료  → event_msg / exec_command_end      도구 아이콘 정리
    작업 없음  → event_msg / task_complete         캐릭터가 쉼

`cwd`는 `<저장소>/.pixel-office/<이름>`을 쓴다. 워크스페이스 하위 경로라서
`Watch All Sessions`를 켜지 않아도 채택되고, 확장이 경로의 마지막 조각을
캐릭터 이름표로 쓰기 때문에 이름도 제대로 나온다. 실제로 만들어지지는 않는다.

## 알아둘 것

세션 파일은 `~/.codex/sessions/` 아래에 생긴다. Codex CLI가 자기 세션을
보관하는 곳과 같은 디렉터리다 — 확장이 그 경로만 보기 때문에 선택지가 없다.
`codex resume` 목록에 섞여 보일 수 있다. 정상 종료(Ctrl-C) 시 브릿지가 자기가
만든 파일을 모두 지운다. 강제 종료로 남았다면 `--cleanup`으로 지운다.

원장 파일은 읽기만 한다. 쓰기 경로가 없다.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from agent_state import ROOT, build_state  # noqa: E402

CODEX_SESSIONS = Path.home() / ".codex" / "sessions"
# 브릿지가 만든 세션임을 표시한다. 정리할 때 이 값으로 찾는다.
ORIGINATOR = "hgnn-pixel-bridge"
# 확장이 특별 취급하는 도구 이름들. 작업 설명을 도구 이름 자리에 넣기 때문에
# 이 이름들과 겹치면 엉뚱하게 해석된다 (spawn_agent는 서브에이전트를 만든다).
RESERVED_TOOL_NAMES = {
    "shell_command", "multi_tool_use.parallel", "spawn_agent",
    "wait_agent", "send_input", "web_search",
}
# 확장은 세션을 채택할 때 파일 끝으로 건너뛴다 (adoptExternalSession의
# `fileOffset = stat.size`). 채택 시점 이전에 쓴 레코드는 절대 읽히지 않으므로,
# 상태가 안 바뀌어도 주기적으로 현재 상태를 다시 써 줘야 갓 채택된 캐릭터가
# 상태를 받는다. 이 간격이 "패널을 열고 나서 캐릭터가 살아나기까지"의 상한이다.
HEARTBEAT_S = 15.0
# 에이전트 키 → 세션 id를 항상 같은 값으로 만들기 위한 네임스페이스.
# 재시작할 때마다 새 id를 쓰면 확장에 캐릭터가 계속 쌓인다. 확장은 오래된 외부
# 에이전트를 자동으로 지우지 않는다 (`EXTERNAL_STALE_TIMEOUT_MS`가 deprecated로
# 주석 처리되어 있다). 그래서 id도 파일 경로도 재시작 간에 고정한다.
NAMESPACE = uuid.uuid5(uuid.NAMESPACE_URL, "hgnn-pixel-bridge")
# 키 → 세션 파일 경로. 재시작하면 이걸 보고 같은 파일을 이어 쓴다.
MANIFEST = Path(__file__).resolve().parent / ".pixel-bridge-sessions.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def tool_label(text: str) -> str:
    """확장은 모르는 도구 이름을 `Using <이름>`으로 그대로 보여준다.

    그래서 도구 이름 자리에 작업 설명을 통째로 넣는 게 가장 읽기 좋다.
    `shell_command`로 보내면 명령이 30자에서 잘린다. `.`과 `_`는 확장이 공백으로
    바꾸므로 미리 정리한다.
    """
    label = " ".join(text.split()).replace("_", " ").replace(".", " ")[:40]
    label = " ".join(label.split()) or "작업 중"
    return label + " " if label in RESERVED_TOOL_NAMES else label


class CodexSession:
    """확장이 읽을 수 있는 Codex 세션 파일 하나. 캐릭터 하나에 대응한다."""

    def __init__(self, key: str, name: str, existing: str | None = None,
                 dry_run: bool = False) -> None:
        self.name = name
        # 같은 에이전트는 언제 다시 띄워도 같은 세션 id를 쓴다.
        self.session_id = str(uuid.uuid5(NAMESPACE, key))
        self.cwd = str(ROOT / ".pixel-office" / name)
        self.dry_run = dry_run
        self.call_seq = 0
        self.open_call: str | None = None
        self.last_emit = 0.0

        if existing and Path(existing).is_file():
            # 이전 실행이 쓰던 파일을 이어 쓴다 → 확장의 기존 캐릭터가 그대로 산다.
            self.path = Path(existing)
            self.reused = True
            return

        self.reused = False
        stamp = datetime.now()
        directory = CODEX_SESSIONS / f"{stamp:%Y}" / f"{stamp:%m}" / f"{stamp:%d}"
        self.path = directory / f"rollout-{stamp:%Y-%m-%dT%H-%M-%S}-{self.session_id}.jsonl"

        if not dry_run:
            directory.mkdir(parents=True, exist_ok=True)
            self._append({
                "timestamp": now_iso(),
                "type": "session_meta",
                "payload": {
                    "id": self.session_id,
                    "timestamp": now_iso(),
                    "cwd": self.cwd,
                    "originator": ORIGINATOR,
                    "source": ORIGINATOR,
                },
            })

    def _append(self, record: dict) -> None:
        self.last_emit = time.monotonic()
        if self.dry_run:
            return
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    def tool_start(self, label: str) -> None:
        """캐릭터를 '작업 중'으로. 이미 열린 작업이 있으면 먼저 닫는다."""
        self.tool_end()
        self.call_seq += 1
        self.open_call = f"{self.session_id}-{self.call_seq}"
        self._append({
            "timestamp": now_iso(),
            "type": "response_item",
            "payload": {
                "type": "function_call",
                "name": tool_label(label),
                "call_id": self.open_call,
                "arguments": "{}",
            },
        })

    def tool_end(self) -> None:
        if self.open_call is None:
            return
        self._append({
            "timestamp": now_iso(),
            "type": "event_msg",
            "payload": {"type": "exec_command_end", "call_id": self.open_call},
        })
        self.open_call = None

    def idle(self, label: str) -> None:
        """작업이 없는 상태. 그래도 무슨 상태인지는 계속 보이게 한다.

        `task_complete`를 보내면 확장이 캐릭터를 waiting으로 돌리는데, 그러면
        오버레이가 상태 문구 대신 그냥 `Idle`을 띄우고(`getActivityText`의
        마지막 분기) 캐릭터가 자리를 뜬다. 대신 도구를 열었다가 바로 닫으면
        에이전트는 active로 남아 "완료된 마지막 도구의 상태"가 계속 표시된다 —
        활성 표시등은 꺼지고 자리는 지킨다. 대기 상태를 읽을 수 있게 하는 게
        이 화면의 목적이므로 이쪽을 쓴다.
        """
        self.tool_start(label)
        self.tool_end()

    def remove(self) -> None:
        if self.dry_run:
            return
        try:
            self.path.unlink()
        except OSError:
            pass


# ── 원장 상태 → 캐릭터 ──────────────────────────────────────────────────────

def short_status(role: dict, state: dict) -> str:
    """패널 말풍선에 들어갈 짧은 한 줄.

    확장의 오버레이는 `max-w-2xs whitespace-nowrap text-ellipsis`라 폭이
    고정이고 한 줄에서 잘린다. 확장을 패치하지 않는 한 늘릴 수 없으므로,
    라벨 쪽을 20자 안팎으로 줄인다. 긴 설명은 브라우저 오피스가 맡는다.
    (확장이 앞에 붙이는 `Using `까지 폭을 먹는다는 점도 감안한다.)
    """
    stats = state["stats"]
    if role["id"] == "env-checker":
        runs = state["runs"]
        if runs:
            run = runs[0]
            return f"{run['model']} {run['dataset']} {run['seed_done']}/{run['seed_total'] or 20}"
        total = stats["tasks_done"] + stats["tasks_pending"]
        return f"대기 · 정식 {stats['tasks_done']}/{total}"
    if role["id"] == "env-builder":
        blocked = len(role["blockers"])
        if role["state"] == "working":
            return f"환경 구축 {role['progress']}%"
        return f"대기 · 환경 {stats['environments']}개" + (f" · 차단 {blocked}" if blocked else "")
    if role["id"] == "clerk":
        return f"보고서 {stats['reports']} · 통합 대기"
    return role["activity"][:24]


def desired_characters(state: dict) -> dict[str, dict]:
    """지금 픽셀 오피스에 있어야 할 캐릭터 전체."""
    characters: dict[str, dict] = {}

    for role in state["roles"]:
        characters[role["id"]] = {
            "name": role["id"],
            "busy": role["state"] == "working",
            "status": short_status(role, state),
        }

    for run in state["runs"]:
        characters[run["id"]] = {
            "name": f"{run['model']}-GPU{run['gpu']}",
            "busy": True,
            "status": f"{run['dataset']} {run['seed_done']}/{run['seed_total'] or 20}",
        }
    return characters


class Bridge:
    """확장에 반영한 상태를 기억했다가, 바뀐 것만 다시 쓴다."""

    def __init__(self, verbose: bool = False, dry_run: bool = False) -> None:
        self.sessions: dict[str, CodexSession] = {}
        self.sent: dict[str, dict] = {}
        self.verbose = verbose
        self.dry_run = dry_run
        self.manifest: dict[str, str] = {}
        if not dry_run:
            try:
                self.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                self.manifest = {}

    def save_manifest(self) -> None:
        if self.dry_run:
            return
        try:
            MANIFEST.write_text(json.dumps(
                {k: str(s.path) for k, s in self.sessions.items()},
                ensure_ascii=False, indent=1), encoding="utf-8")
        except OSError:
            pass

    def log(self, action: str, key: str, detail: str = "") -> None:
        if self.verbose or self.dry_run:
            print(f"  {action:<14} {key:<26} {detail}", flush=True)

    def sync(self, state: dict) -> int:
        want = desired_characters(state)
        changes = 0

        # 사라진 캐릭터부터 정리한다 (끝난 run 등).
        for key in list(self.sessions):
            if key in want:
                continue
            self.log("세션 종료", key)
            self.sessions.pop(key).remove()
            self.sent.pop(key, None)
            self.manifest.pop(key, None)
            self.save_manifest()
            changes += 1

        for key, target in want.items():
            session = self.sessions.get(key)
            if session is None:
                session = CodexSession(key, target["name"],
                                       existing=self.manifest.get(key),
                                       dry_run=self.dry_run)
                self.sessions[key] = session
                self.sent[key] = {"status": None, "busy": None}
                self.log("세션 이어쓰기" if session.reused else "세션 생성",
                         key, session.path.name)
                self.save_manifest()
                changes += 1

            previous = self.sent[key]
            changed = (previous["status"] != target["status"]
                       or previous["busy"] != target["busy"])
            stale = time.monotonic() - session.last_emit >= HEARTBEAT_S

            if changed or stale:
                if target["busy"]:
                    session.tool_start(target["status"])
                else:
                    session.idle(target["status"])
                if changed:
                    self.log("작업 시작" if target["busy"] else "대기",
                             key, tool_label(target["status"])[:44])
                    previous.update(target)
                    changes += 1

        return changes

    def shutdown(self) -> None:
        """세션 파일은 **남긴다**.

        지우면 다음 실행이 새 파일과 새 캐릭터를 만들어 패널에 캐릭터가 쌓인다.
        확장은 오래된 외부 에이전트를 스스로 제거하지 않기 때문에(deprecated
        `EXTERNAL_STALE_TIMEOUT_MS`) 파일을 남겨 두고 이어 쓰는 쪽이 낫다.
        완전히 없애려면 `--cleanup`을 쓴다.
        """
        self.save_manifest()


def cleanup_orphans() -> int:
    """강제 종료로 남은 브릿지 세션 파일을 지운다."""
    removed = 0
    if not CODEX_SESSIONS.is_dir():
        return 0
    for path in CODEX_SESSIONS.rglob("*.jsonl"):
        try:
            with path.open("r", encoding="utf-8") as handle:
                first = handle.readline()
        except OSError:
            continue
        if ORIGINATOR not in first:
            continue
        try:
            path.unlink()
            print(f"  삭제 {path}")
            removed += 1
        except OSError:
            pass
    return removed


def main() -> int:
    parser = argparse.ArgumentParser(
        description="`.agents` 원장 상태를 VS Code 픽셀 오피스로 보낸다.")
    parser.add_argument("--interval", type=float, default=5.0,
                        help="원장을 다시 읽는 주기(초). 기본 5")
    parser.add_argument("--once", action="store_true",
                        help="한 번만 동기화하고 끝낸다 (세션 파일은 남긴다)")
    parser.add_argument("--dry-run", action="store_true",
                        help="파일을 쓰지 않고 무엇을 할지만 출력한다")
    parser.add_argument("--verbose", action="store_true",
                        help="상태 변화를 모두 출력한다")
    parser.add_argument("--cleanup", action="store_true",
                        help="남아 있는 브릿지 세션 파일만 지우고 끝낸다")
    args = parser.parse_args()

    if args.cleanup:
        count = cleanup_orphans()
        MANIFEST.unlink(missing_ok=True)
        print(f"브릿지 세션 파일 {count}개 삭제 (패널의 캐릭터는 X로 직접 닫는다)")
        return 0

    if not args.dry_run:
        print(f"세션 파일 위치: {CODEX_SESSIONS}")
        print("VS Code에서 Pixel Agents 패널이 열려 있어야 캐릭터가 보인다.")

    bridge = Bridge(verbose=args.verbose, dry_run=args.dry_run)
    try:
        while True:
            state = build_state()
            if state["errors"]:
                print(f"원장 경고: {'; '.join(state['errors'])}", file=sys.stderr)
            changes = bridge.sync(state)
            print(f"[{state['updated_kst']}] 캐릭터 {len(bridge.sessions)}개 "
                  f"(role {len(state['roles'])} · run {len(state['runs'])}) · 변경 {changes}건",
                  flush=True)
            if args.once:
                return 0
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\n종료 — 세션 파일 정리 중")
        bridge.shutdown()
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
