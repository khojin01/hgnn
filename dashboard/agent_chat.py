"""픽셀 오피스 NPC 대화 — 에이전트에게 자기 담당 업무를 물어본다.

캐릭터를 클릭하고 질문하면, 그 role의 프로토콜 문서와 현재 원장 상태를
컨텍스트로 붙여 `codex exec`를 돌린다. 답은 그 담당자의 관점에서 나온다.

**읽기 전용이다.** 세 겹으로 막는다:

1. `-s read-only`   — codex 샌드박스가 쓰기 명령 자체를 거부한다
2. `--ephemeral`    — 세션 파일을 남기지 않는다. 질문할 때마다 픽셀 오피스에
                      유령 캐릭터가 생기는 걸 막는다
3. 프롬프트 명시     — 조사와 답변만 하고 아무것도 바꾸지 말라고 지시한다

작업 지시(`plan` → `execute`)는 두 단계다. 먼저 읽기 전용으로 **무엇을 할지와
정확한 명령어**를 받아 사람이 보고, 승인해야 비로소 쓰기 권한으로 실행한다.
지시와 실행은 `dashboard/orders.log`에 전부 남는다.
"""

from __future__ import annotations

import shutil
import subprocess
from datetime import datetime
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from agent_state import AGENTS, KST, ROOT, build_state  # noqa: E402

# 물어볼 수 있는 에이전트와 그 프로토콜 문서. 여기 없는 이름은 거부한다.
ROLE_FILES = {
    "env-builder": AGENTS / "env-builder.md",
    "env-checker": AGENTS / "env-checker.md",
    "clerk": AGENTS / "clerk.md",
}
QUESTION_MAX_CHARS = 2000
TIMEOUT_S = 240
# 실행은 파일을 고치고 명령을 돌리므로 더 오래 걸린다.
EXECUTE_TIMEOUT_S = 900
# 지시와 실행 기록. 무엇을 시켰고 무엇이 돌았는지 되짚을 수 있어야 한다.
ORDER_LOG = Path(__file__).resolve().parent / "orders.log"


def find_codex() -> str | None:
    """codex 실행 파일을 찾는다.

    서버가 로그인 셸이 아닌 곳에서 뜨면 `~/.local/bin`이 PATH에 없을 수 있다.
    PATH → 사용자 bin → ChatGPT 확장 번들 순으로 내려간다.
    """
    found = shutil.which("codex")
    if found:
        return found
    local = Path.home() / ".local" / "bin" / "codex"
    if local.exists():
        return str(local)
    bundled = sorted((Path.home() / ".vscode-server" / "extensions").glob(
        "openai.chatgpt-*/bin/*/codex"))
    return str(bundled[-1]) if bundled else None


class ChatError(RuntimeError):
    """질문을 처리할 수 없다. 사용자에게 그대로 보여줄 메시지를 담는다."""


def _bullets(items: list[dict], limit: int) -> str:
    if not items:
        return "  (없음)"
    lines = []
    for item in items[:limit]:
        detail = f" — {item['detail']}" if item.get("detail") else ""
        path = f" [{item['path']}]" if item.get("path") else ""
        lines.append(f"  - {item['label']}{detail}{path}")
    if len(items) > limit:
        lines.append(f"  - … 외 {len(items) - limit}건")
    return "\n".join(lines)


def build_prompt(agent: str, question: str) -> str:
    """role 프로토콜 + 현재 원장 상태 + 질문을 하나의 프롬프트로 엮는다."""
    state = build_state()
    role = next((r for r in state["roles"] if r["id"] == agent), None)
    if role is None:
        raise ChatError(f"원장에서 `{agent}` 상태를 찾지 못했다.")

    protocol = ""
    role_file = ROLE_FILES[agent]
    try:
        protocol = role_file.read_text(encoding="utf-8")
    except OSError:
        protocol = "(프로토콜 문서를 읽지 못했다)"

    return f"""너는 이 저장소의 `{agent}` 에이전트다. 아래는 네 역할 정의와, 지금
원장에 기록된 네 상태다. 이 역할의 담당자로서 질문에 답하라.

규칙:
- **아무것도 바꾸지 마라.** 조사하고 답만 한다. 파일 수정·명령 실행·설치 금지.
- 한국어로 답한다. 서론 없이 답부터 쓴다.
- 근거가 되는 원장 파일 경로를 함께 밝힌다. 필요하면 저장소 파일을 직접 읽어라.
- 원장에 없는 내용은 지어내지 말고 "원장에 기록이 없다"고 말한다.
- 길어도 20줄을 넘기지 마라.

=== 내 역할 정의 ({role_file.relative_to(ROOT)}) ===
{protocol}

=== 지금 내 상태 (원장에서 추출) ===
상태: {role['state']} · 진행률 {role['progress']}% · {role['activity']}

지금 하는 일:
{_bullets(role['now'], 5)}

앞으로 할 일 ({len(role['next'])}건):
{_bullets(role['next'], 12)}

완료한 일 ({len(role['done'])}건):
{_bullets(role['done'], 12)}

차단된 것 ({len(role['blockers'])}건):
{_bullets(role['blockers'], 8)}

결과물 ({len(role['artifacts'])}건):
{_bullets(role['artifacts'], 8)}

=== 더 볼 수 있는 원장 ===
- .agents/env-status/README.md — 환경/모델 현황, 최근 이벤트
- .agents/env-status/formal-results.md — 모델×데이터셋 정식 결과
- .agents/env-status/events.md — 핸드오프 기록 원문
- .agents/clerk-reports/개별/ — 한글 운영 보고서
- .agents/env-status/full-runs/ — 실행 로그

=== 질문 ===
{question}
"""


def _validate(agent: str, text: str, what: str) -> str:
    if agent not in ROLE_FILES:
        raise ChatError(f"알 수 없는 에이전트: {agent}")
    text = text.strip()
    if not text:
        raise ChatError(f"{what}이(가) 비어 있다.")
    if len(text) > QUESTION_MAX_CHARS:
        raise ChatError(f"{what}이(가) 너무 길다 ({len(text)}자 / 최대 {QUESTION_MAX_CHARS}자).")
    return text


def _log_order(agent: str, kind: str, body: str) -> None:
    stamp = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")
    try:
        with ORDER_LOG.open("a", encoding="utf-8") as handle:
            handle.write(f"\n=== {stamp} KST · {agent} · {kind} ===\n{body.strip()}\n")
    except OSError:
        pass


def _run_codex(prompt: str, sandbox: str, timeout: int) -> str:
    """codex를 한 번 돌리고 마지막 메시지를 돌려준다."""
    with tempfile.NamedTemporaryFile("w+", suffix=".md", delete=False,
                                     encoding="utf-8") as answer_file:
        answer_path = Path(answer_file.name)

    codex = find_codex()
    if codex is None:
        raise ChatError(
            "`codex`를 찾지 못했다. PATH에 올린다: mkdir -p ~/.local/bin && "
            "ln -sf ~/.vscode-server/extensions/openai.chatgpt-*/bin/linux-x86_64/codex "
            "~/.local/bin/codex")

    command = [
        codex, "exec",
        "--ephemeral",              # 세션 파일을 남기지 않는다 (유령 캐릭터 방지)
        "-s", sandbox,              # read-only 또는 workspace-write
        "--skip-git-repo-check",    # 이 저장소는 git repo가 아니다
        "-C", str(ROOT),
        "-o", str(answer_path),     # 마지막 메시지만 이 파일에 쓴다
        "-",                        # 프롬프트는 stdin으로
    ]
    try:
        completed = subprocess.run(
            command, input=prompt, text=True, capture_output=True,
            timeout=timeout, check=False,
        )
    except OSError as exc:
        answer_path.unlink(missing_ok=True)
        raise ChatError(f"codex 실행 실패 ({codex}): {exc}") from None
    except subprocess.TimeoutExpired:
        answer_path.unlink(missing_ok=True)
        raise ChatError(f"{timeout}초 안에 끝나지 않았다. 범위를 줄여서 다시 시도한다.") from None

    try:
        answer = answer_path.read_text(encoding="utf-8").strip()
    except OSError:
        answer = ""
    finally:
        answer_path.unlink(missing_ok=True)

    if not answer:
        tail = (completed.stderr or completed.stdout or "").strip().splitlines()
        raise ChatError("답을 받지 못했다. " + (" / ".join(tail[-3:]) if tail else
                                              f"종료 코드 {completed.returncode}"))
    return answer


def ask(agent: str, question: str) -> dict:
    """에이전트에게 물어본다. 읽기 전용."""
    question = _validate(agent, question, "질문")
    answer = _run_codex(build_prompt(agent, question), "read-only", TIMEOUT_S)
    return {"agent": agent, "question": question, "answer": answer}


# ── 작업 지시 ───────────────────────────────────────────────────────────────

_ORDER_RULES = """공통 규칙:
- `.agents/` 원장은 **덮어쓰지 마라.** 기존 증거는 보존하고 새 항목을 덧붙인다
  (`clerk.md`의 "Never overwrite prior evidence; correct it in a new event").
- 30분 넘게 걸릴 GPU 학습은 직접 붙잡고 있지 마라. `.agents/run-scripts/`의
  기존 스크립트 방식대로 로그를 남기는 백그라운드 실행으로 띄우고, 시작했다는
  사실과 로그 경로를 보고한 뒤 끝낸다.
- 데이터가 없거나 논문이 O.O.M/O.O.T로 적어 둔 조합은 실행하지 말고 그대로 보고한다.
- 한국어로 보고한다."""


def build_plan_prompt(agent: str, order: str) -> str:
    """실행 전 계획. 아무것도 바꾸지 않고 '무엇을 할지'만 받는다."""
    return build_prompt(agent, f"""아래는 사용자가 너에게 내린 작업 지시다.

    {order}

지금은 **계획만** 세운다. 파일을 고치거나 명령을 실행하지 마라. 다음을 답하라:

1. **할 일** — 무엇을 왜 하는지 3줄 이내.
2. **실행할 명령** — 실제로 돌릴 셸 명령을 ```sh 블록에 그대로. 없으면 "없음".
3. **바꿀 파일** — 수정/생성할 파일 경로 목록. 없으면 "없음".
4. **위험 요소** — 되돌리기 어려운 것, 오래 걸리는 것, 확인이 필요한 것.
5. **지시가 불명확하거나 원장 근거와 충돌하면** 그 점을 먼저 지적하라.

{_ORDER_RULES}""")


def plan(agent: str, order: str) -> dict:
    """지시를 받아 실행 계획을 만든다. 읽기 전용이라 안전하다."""
    order = _validate(agent, order, "지시")
    text = _run_codex(build_plan_prompt(agent, order), "read-only", TIMEOUT_S)
    _log_order(agent, "계획 요청", f"지시: {order}\n\n{text}")
    return {"agent": agent, "order": order, "plan": text}


def execute(agent: str, order: str, approved_plan: str) -> dict:
    """사람이 승인한 계획을 실제로 실행한다. 워크스페이스 쓰기 권한이 열린다."""
    order = _validate(agent, order, "지시")
    if not approved_plan.strip():
        raise ChatError("승인된 계획이 없다. 계획을 먼저 받아야 한다.")

    prompt = build_prompt(agent, f"""아래는 사용자가 내린 작업 지시와, 사용자가
**승인한** 실행 계획이다. 계획대로 실행하라.

=== 지시 ===
{order}

=== 승인된 계획 ===
{approved_plan}

실행 규칙:
- 승인된 계획의 범위를 벗어나지 마라. 계획에 없던 파일을 고치거나 명령을
  돌리지 마라. 범위를 벗어나야 한다면 실행을 멈추고 그 이유를 보고하라.
- 끝나면 **실제로 실행한 명령, 바꾼 파일, 결과**를 보고하라. 실패도 그대로 적는다.

{_ORDER_RULES}""")

    text = _run_codex(prompt, "workspace-write", EXECUTE_TIMEOUT_S)
    _log_order(agent, "실행", f"지시: {order}\n\n{text}")
    return {"agent": agent, "order": order, "result": text}


if __name__ == "__main__":  # 수동 확인용: python3 dashboard/agent_chat.py env-checker "질문"
    if len(sys.argv) < 3:
        print("사용법: python3 dashboard/agent_chat.py <agent> <질문>", file=sys.stderr)
        raise SystemExit(2)
    try:
        print(ask(sys.argv[1], " ".join(sys.argv[2:]))["answer"])
    except ChatError as exc:
        print(f"오류: {exc}", file=sys.stderr)
        raise SystemExit(1) from None
