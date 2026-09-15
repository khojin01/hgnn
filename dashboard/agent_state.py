"""`.agents` 원장 → 픽셀 오피스가 읽는 정규화 에이전트 상태.

세 role agent(env-builder / env-checker / clerk)와, 지금 GPU에서 돌고 있는
formal 실행(run) 하나하나를 같은 스키마로 뽑아낸다. 원장은 **읽기만** 한다.

각 에이전트에 대해 뽑는 것:
  now       — 지금 하고 있는 작업
  next      — 앞으로 해야 하는 작업
  done      — 완료한 작업
  artifacts — 완료한 작업의 결과물(파일 경로)
  blockers  — 막혀 있는 것

섹션 단위로 예외를 격리한다. 원장 하나가 깨져도 나머지는 그대로 나온다.
"""

from __future__ import annotations

import re
import subprocess
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

KST = timezone(timedelta(hours=9))

ROOT = Path(__file__).resolve().parent.parent
AGENTS = ROOT / ".agents"
ENV_STATUS = AGENTS / "env-status"
FULL_RUNS = ENV_STATUS / "full-runs"
RUN_SCRIPTS = AGENTS / "run-scripts"
CLERK = AGENTS / "clerk-reports"

# formal-results.md 에서 "끝난 것"으로 치는 상태
TERMINAL_DONE = {"formal", "operational-20seed"}
# 사람이 풀어야 움직이는 상태
BLOCKED_STATES = {"blocked-data", "blocked-source", "blocked-config", "deferred",
                  "timeout-preprocess", "blocked-env", "blocked-permission"}
# 논문이 O.O.M/O.O.T로 적어 둬서 애초에 실행하지 않는 상태
SKIPPED_STATES = {"skipped-oom", "skipped-oot", "skipped-paper"}


# ── 공통 유틸 ────────────────────────────────────────────────────────────────

def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def rel(path: Path | str) -> str:
    """저장소 루트 기준 상대 경로. 화면과 로그에 그대로 쓴다."""
    try:
        return str(Path(path).resolve().relative_to(ROOT))
    except (ValueError, OSError):
        return str(path)


def strip_md(cell: str) -> str:
    """표 셀에서 링크·강조·백틱을 벗겨 사람이 읽는 문자열만 남긴다."""
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", cell)
    text = text.replace("`", "").replace("**", "").replace("*", "")
    return text.strip()


def parse_tables(text: str) -> list[dict]:
    """Markdown을 훑어 `## 제목` 아래의 파이프 표를 모두 뽑는다.

    열 순서가 바뀌어도 되도록 헤더 이름을 키로 하는 dict 행을 돌려준다.
    """
    tables: list[dict] = []
    heading = ""
    rows: list[list[str]] = []

    def flush() -> None:
        # 헤더 + 구분선 + 최소 1행이 있어야 표로 인정한다.
        if len(rows) >= 3:
            header = [strip_md(c) for c in rows[0]]
            body = []
            for raw in rows[2:]:
                cells = [strip_md(c) for c in raw]
                cells += [""] * (len(header) - len(cells))
                body.append(dict(zip(header, cells)))
            tables.append({"heading": heading, "header": header, "rows": body})
        rows.clear()

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            flush()
            heading = stripped.lstrip("#").strip()
            continue
        if stripped.startswith("|") and stripped.endswith("|"):
            rows.append(stripped.strip("|").split("|"))
            continue
        flush()
    flush()
    return tables


def pick(row: dict, *keywords: str) -> str:
    """헤더 이름에 keyword가 들어간 첫 열의 값. 열 순서 변경에 견디기 위함."""
    for key, value in row.items():
        low = key.lower()
        if any(word in low for word in keywords):
            return value
    return ""


def task_of_heading(heading: str) -> str | None:
    low = heading.lower()
    if "table 3" in low or "node classification" in low:
        return "node"
    if "20-seed operational" in low:
        return "node-operational"
    if "table 4" in low or "hyperedge" in low:
        return "edge"
    if "table 5" in low or "community" in low:
        return "community"
    return None


TASK_LABEL = {
    "node": "노드 분류 (T3)",
    "node-operational": "노드 20-seed 운영검증",
    "edge": "하이퍼엣지 예측 (T4)",
    "community": "커뮤니티 탐지 (T5)",
}


# ── 원장 로더 ────────────────────────────────────────────────────────────────

def load_formal_results() -> list[dict]:
    """formal-results.md → 모델×데이터셋×task 단위 작업 목록."""
    tasks: list[dict] = []
    for table in parse_tables(read_text(ENV_STATUS / "formal-results.md")):
        task = task_of_heading(table["heading"])
        if task is None:
            continue
        for row in table["rows"]:
            model = pick(row, "model")
            dataset = pick(row, "dataset")
            status = pick(row, "status").lower()
            if not model or not status:
                continue
            tasks.append({
                "task": task,
                "task_label": TASK_LABEL[task],
                "model": model,
                "dataset": dataset,
                "config": pick(row, "run config", "config"),
                "seeds": pick(row, "splits", "seeds"),
                "metric": pick(row, "mean"),
                "target": pick(row, "table target", "target"),
                "status": status,
                "evidence": pick(row, "log", "evidence"),
            })
    return tasks


def load_env_status() -> dict:
    """env-status/README.md → 환경 표 / 모델 표 / 최근 이벤트 표."""
    out: dict[str, list] = {"environments": [], "models": [], "events": []}
    for table in parse_tables(read_text(ENV_STATUS / "README.md")):
        low = table["heading"].lower()
        if "current environment status" in low:
            for row in table["rows"]:
                name = pick(row, "environment")
                if not name:
                    continue
                out["environments"].append({
                    "name": name,
                    "source": pick(row, "requirement"),
                    "models": pick(row, "intended models"),
                    "builder": pick(row, "builder"),
                    "checker": pick(row, "checker"),
                    "blocker": pick(row, "blocker"),
                })
        elif "current model status" in low:
            for row in table["rows"]:
                model = pick(row, "model")
                if not model:
                    continue
                out["models"].append({
                    "order": pick(row, "order"),
                    "model": model,
                    "env": pick(row, "environment"),
                    "datasets": pick(row, "dataset"),
                    "observed": pick(row, "observed"),
                    "reference": pick(row, "benchmark", "ref"),
                    "state": pick(row, "state"),
                    "blocker": pick(row, "blocker"),
                })
        elif "recent events" in low:
            for row in table["rows"]:
                actors = pick(row, "from")
                if not actors:
                    continue
                out["events"].append({
                    "time": pick(row, "time"),
                    "actors": actors,
                    "event": pick(row, "event"),
                    "outcome": pick(row, "outcome"),
                })
    return out


def load_handoffs(events: list[dict], limit: int = 12) -> list[dict]:
    """최근 이벤트 표에서 `A → B` 형태만 골라 핸드오프 화살표로 만든다."""
    handoffs: list[dict] = []
    for event in events:
        actors = event["actors"]
        if "→" not in actors and "->" not in actors:
            continue
        parts = re.split(r"→|->", actors, maxsplit=1)
        source, target = parts[0].strip(), parts[1].strip()
        handoffs.append({
            "from": source,
            "to": target,
            "time": event["time"],
            "text": event["event"],
            "outcome": event["outcome"],
        })
    return handoffs[-limit:]


def load_clerk_reports() -> dict:
    """clerk-reports → 개별 보고서 목록, 통합 이력, 통합 대기 건수."""
    readme = read_text(CLERK / "README.md")
    pending = 0
    match = re.search(r"통합 대기 건수는\s*\*\*(\d+)건\*\*", readme)
    if match:
        pending = int(match.group(1))

    reports: list[dict] = []
    bundles: list[dict] = []
    for table in parse_tables(readme):
        low = table["heading"].lower()
        if "개별 보고서 목록" in table["heading"]:
            for row in table["rows"]:
                summary = pick(row, "요약")
                if not summary:
                    continue
                reports.append({
                    "no": pick(row, "번호"),
                    "time": pick(row, "작성"),
                    "summary": summary,
                    "status": pick(row, "상태"),
                })
        elif "통합 이력" in table["heading"] or "묶음" in low:
            for row in table["rows"]:
                target = pick(row, "대상")
                if not target:
                    continue
                bundles.append({"no": pick(row, "묶음"), "covers": target,
                                "file": pick(row, "파일")})

    files = sorted((CLERK / "개별").glob("*.md")) if (CLERK / "개별").is_dir() else []
    bundle_files = sorted((CLERK / "통합").glob("*.md")) if (CLERK / "통합").is_dir() else []
    return {
        "pending_bundle": pending,
        "reports": reports,
        "bundles": bundles,
        "report_files": [rel(f) for f in files],
        "bundle_files": [rel(f) for f in bundle_files],
    }


def load_builder_events(limit: int = 6) -> list[str]:
    """events.md 최신 섹션의 불릿. builder가 무엇을 만지고 있었는지의 산문 기록."""
    text = read_text(ENV_STATUS / "events.md")
    bullets = [re.sub(r"\s+", " ", line.strip().lstrip("- ").strip())
               for line in text.splitlines() if line.strip().startswith("- ")]
    return bullets[-limit:]


# ── 실행(run) 상태 ───────────────────────────────────────────────────────────

def run_plan(script: Path) -> dict:
    """run-script 한 개 → run_id, GPU, 계획된 데이터셋 순서."""
    text = read_text(script)
    run_id = ""
    match = re.search(r"full-runs/([A-Za-z0-9._-]+)", text)
    if match:
        run_id = match.group(1)
    datasets = re.findall(r"^\s*run_case\s+([A-Za-z0-9_]+)", text, re.M)
    gpu = ""
    gpu_match = re.search(r"cuda:(\d+)", text)
    if gpu_match:
        gpu = gpu_match.group(1)
    model_match = re.match(r"formal118-([a-z0-9]+)-([a-z]+)-gpu(\d+)", script.stem)
    return {
        "script": rel(script),
        "run_id": run_id or script.stem,
        "model": model_match.group(1) if model_match else script.stem,
        "task": model_match.group(2) if model_match else "node",
        "gpu": gpu or (model_match.group(3) if model_match else ""),
        "datasets": datasets,
    }


def run_status(run_id: str) -> dict:
    """status.tsv + 개별 로그 → 끝난 데이터셋, 실패, 지금 돌고 있는 데이터셋."""
    directory = FULL_RUNS / run_id
    finished: dict[str, str] = {}
    for line in read_text(directory / "status.tsv").splitlines():
        parts = line.split()
        if len(parts) >= 2:
            finished[parts[0]] = parts[1]

    # 종료 코드가 안 찍힌 로그 = 아직 돌고 있는 데이터셋
    current = ""
    seed_done = seed_total = 0
    if directory.is_dir():
        for log in sorted(directory.glob("*.log"), key=lambda p: p.stat().st_mtime,
                          reverse=True):
            body = read_text(log)
            if "EXIT_CODE=" in body:
                continue
            current = log.stem
            seeds = re.findall(r"(\d+)/(\d+)\s*\[", body)
            if seeds:
                seed_done, seed_total = int(seeds[-1][0]), int(seeds[-1][1])
            break

    return {
        "finished": finished,
        "ok": sum(1 for code in finished.values() if code == "0"),
        "failed": sorted(name for name, code in finished.items() if code != "0"),
        "current_dataset": current,
        "seed_done": seed_done,
        "seed_total": seed_total,
    }


def live_processes() -> list[dict]:
    """지금 떠 있는 formal/node20 실행 프로세스."""
    try:
        proc = subprocess.run(["ps", "-eo", "pid=,etimes=,etime=,args="], text=True,
                              capture_output=True, timeout=3, check=False)
    except (OSError, subprocess.SubprocessError):
        return []

    found: list[dict] = []
    for line in proc.stdout.splitlines():
        if not re.search(r"formal118-|node20-", line):
            continue
        parts = line.split(None, 3)
        if len(parts) < 4:
            continue
        pid, etimes, etime, args = parts
        match = re.search(r"(formal118-[a-z0-9]+-[a-z]+-gpu\d+-\d+|node20-[a-z0-9]+-gpu\d+-\d+)",
                          args)
        if not match:
            continue
        found.append({"pid": int(pid), "elapsed_s": int(etimes) if etimes.isdigit() else 0,
                      "elapsed": etime, "run_id": match.group(1), "args": args[:200]})
    return found


def live_runs() -> list[dict]:
    """살아 있는 실행 = 픽셀 오피스의 run 캐릭터."""
    plans = {}
    if RUN_SCRIPTS.is_dir():
        for script in sorted(RUN_SCRIPTS.glob("*.sh")):
            plan = run_plan(script)
            plans[plan["run_id"]] = plan

    runs: list[dict] = []
    seen: set[str] = set()
    for proc in live_processes():
        run_id = proc["run_id"]
        if run_id in seen:
            continue
        seen.add(run_id)
        plan = plans.get(run_id, {"model": run_id, "task": "node", "gpu": "",
                                  "datasets": [], "script": ""})
        status = run_status(run_id)
        total = len(plan["datasets"]) or (len(status["finished"]) + 1)
        done = len(status["finished"])
        runs.append({
            "id": f"run:{run_id}",
            "kind": "run",
            "run_id": run_id,
            "model": plan["model"].upper() if len(plan["model"]) <= 4 else plan["model"],
            "task": plan["task"],
            "gpu": plan["gpu"],
            "pid": proc["pid"],
            "elapsed": proc["elapsed"],
            "dataset": status["current_dataset"] or "(시작 중)",
            "seed_done": status["seed_done"],
            "seed_total": status["seed_total"],
            "dataset_done": done,
            "dataset_total": total,
            "progress": min(100, round(done * 100 / total)) if total else 0,
            "failed": status["failed"],
            "log": rel(FULL_RUNS / run_id / f"{status['current_dataset']}.log")
                   if status["current_dataset"] else rel(FULL_RUNS / run_id),
            "script": plan.get("script", ""),
        })
    return runs


def completed_runs() -> list[dict]:
    """status.tsv가 있는 모든 실행 = env-checker가 끝낸 결과물."""
    out: list[dict] = []
    if not FULL_RUNS.is_dir():
        return out
    for directory in sorted(FULL_RUNS.iterdir()):
        if not directory.is_dir() or not (directory / "status.tsv").is_file():
            continue
        status = run_status(directory.name)
        out.append({
            "run_id": directory.name,
            "ok": status["ok"],
            "total": len(status["finished"]),
            "failed": status["failed"],
            "path": rel(directory),
            "mtime": directory.stat().st_mtime,
        })
    out.sort(key=lambda item: item["mtime"], reverse=True)
    return out


# ── role agent 조립 ─────────────────────────────────────────────────────────

def build_builder(env_status: dict, tasks: list[dict]) -> dict:
    """env-builder: Conda 환경을 만들고 호환성 문제를 고친다."""
    envs = env_status["environments"]
    ready = [e for e in envs if "ready" in e["builder"].lower()]
    building = [e for e in envs if "building" in e["builder"].lower()]

    # 모델 표에서 환경/코드 문제로 넘어온 항목 = builder가 볼 차례인 것
    env_blocked = [m for m in env_status["models"]
                   if re.search(r"env-builder|builder", m["blocker"], re.I)]
    open_env_issues = [t for t in tasks
                       if t["status"] in {"blocked-env", "blocked-config", "timeout-preprocess"}]

    now = []
    if building:
        now = [{"label": f"{e['name']} 환경 구축 중", "detail": e["blocker"]} for e in building]
    elif env_blocked:
        now = [{"label": f"{m['model']} 환경 이슈 대기", "detail": m["blocker"]}
               for m in env_blocked[:3]]
    else:
        now = [{"label": "checker 피드백 감시", "detail":
                f"환경 {len(ready)}개 모두 ready_for_check — 새 환경/코드 오류 발생 시 착수"}]

    next_items = [{"label": f"{t['model']} {t['dataset']} 환경 문제 해소",
                   "detail": f"{t['status']} — {t['evidence']}"}
                  for t in open_env_issues[:6]]
    if not next_items:
        next_items = [{"label": "대기 — 새 환경 요청 없음",
                       "detail": "checker가 FAIL_ENV를 올리면 그때 착수"}]

    done = [{"label": f"{e['name']} 구성 완료",
             "detail": f"{e['models']} · {e['blocker']}"} for e in ready]

    artifacts = [{"label": path.name, "path": rel(path)}
                 for path in sorted(ENV_STATUS.glob("*builder*.md"))]
    artifacts += [{"label": path.name, "path": rel(path)}
                  for path in sorted(ENV_STATUS.glob("dgl-source-build*.md"))]

    return {
        "id": "env-builder",
        "kind": "role",
        "name": "env-builder",
        "role": "환경 구축 · 호환성 수정",
        "desk": "환경실",
        "state": "working" if building else ("waiting" if not env_blocked else "blocked"),
        "activity": now[0]["label"],
        "progress": round(len(ready) * 100 / len(envs)) if envs else 0,
        "now": now,
        "next": next_items,
        "done": done,
        "artifacts": artifacts,
        "blockers": [{"label": e["name"], "detail": e["blocker"]}
                     for e in envs if "blocked" in e["blocker"].lower()],
        "notes": load_builder_events(4),
    }


def build_checker(tasks: list[dict], runs: list[dict], runs_done: list[dict]) -> dict:
    """env-checker: 모델을 실제로 돌리고 metric을 뽑는다."""
    done_tasks = [t for t in tasks if t["status"] in TERMINAL_DONE]
    pending = [t for t in tasks if t["status"] in {"pending", "running"}]
    blocked = [t for t in tasks if t["status"] in BLOCKED_STATES]
    skipped = [t for t in tasks if t["status"] in SKIPPED_STATES]
    runnable = len(done_tasks) + len(pending)

    if runs:
        now = [{"label": f"{r['model']} / {r['dataset']} (GPU{r['gpu']})",
                "detail": f"seed {r['seed_done']}/{r['seed_total'] or 20} · "
                          f"데이터셋 {r['dataset_done']}/{r['dataset_total']} · {r['elapsed']} 경과",
                "path": r["log"]} for r in runs]
        state, activity = "working", f"{len(runs)}개 실행 진행 중"
    else:
        now = [{"label": "실행 대기", "detail":
                f"정식 완료 {len(done_tasks)}건 · 남은 실행 대상 {len(pending)}건"}]
        state, activity = "idle", "다음 배치 대기"

    next_items = [{"label": f"{t['model']} · {t['dataset']}",
                   "detail": f"{t['task_label']} · 목표 {t['target']} · {t['status']}"}
                  for t in pending[:12]]

    done = [{"label": f"{t['model']} · {t['dataset']}",
             "detail": f"{t['task_label']} · {t['metric']} (목표 {t['target']}) · {t['seeds']}",
             "path": t["evidence"]} for t in done_tasks]

    artifacts = [{"label": f"{r['run_id']} — 성공 {r['ok']}/{r['total']}", "path": r["path"]}
                 for r in runs_done[:12]]

    return {
        "id": "env-checker",
        "kind": "role",
        "name": "env-checker",
        "role": "모델 실행 · 성능 검증",
        "desk": "실행실",
        "state": state,
        "activity": activity,
        "progress": round(len(done_tasks) * 100 / runnable) if runnable else 0,
        "now": now,
        "next": next_items,
        "done": done,
        "artifacts": artifacts,
        "blockers": [{"label": f"{t['model']} · {t['dataset']}",
                      "detail": f"{t['status']} — {t['evidence']}"} for t in blocked],
        "notes": [f"논문 O.O.M/O.O.T로 실행하지 않는 칸 {len(skipped)}건"],
    }


def build_clerk(clerk: dict, tasks: list[dict], env_status: dict) -> dict:
    """clerk: 원장을 갱신하고 한글 보고서를 쓴다."""
    reports = clerk["reports"]
    pending_bundle = clerk["pending_bundle"]

    now = [{"label": f"통합 보고서 대기 {pending_bundle}/5건",
            "detail": "개별 보고서가 5건 쌓이면 다음 묶음을 작성한다"}]
    next_items = [{"label": "새 실행 종료 시 원장 반영",
                   "detail": "formal-results.md · smoke_run.md · events.md 동시 갱신"}]
    if pending_bundle >= 5:
        next_items.insert(0, {"label": "통합 보고서 작성",
                              "detail": f"대기 {pending_bundle}건 — 묶음 기준 충족"})
    unposted = [t for t in tasks if t["status"] in TERMINAL_DONE and not t["evidence"]]
    if unposted:
        next_items.insert(0, {"label": f"증거 경로 없는 정식 결과 {len(unposted)}건 보완",
                              "detail": "로그 경로를 원장에 링크"})

    done = [{"label": f"#{r['no']} {r['summary']}", "detail": f"{r['time']} · {r['status']}"}
            for r in reports]
    artifacts = [{"label": Path(p).name, "path": p} for p in clerk["bundle_files"]]
    artifacts += [{"label": Path(p).name, "path": p} for p in clerk["report_files"]]
    artifacts += [{"label": "formal-results.md", "path": rel(ENV_STATUS / "formal-results.md")},
                  {"label": "smoke_run.md", "path": rel(CLERK / "smoke_run.md")}]

    # clerk의 진행률은 문제 해소율이 아니라 "기록 반영률"이다. 끝난 작업 중
    # 증거 경로까지 원장에 링크된 비율을 쓴다.
    finished = [t for t in tasks if t["status"] in TERMINAL_DONE]
    linked = [t for t in finished if t["evidence"]]
    return {
        "id": "clerk",
        "kind": "role",
        "name": "clerk",
        "role": "결과 기록 · 통합 보고",
        "desk": "기록실",
        "state": "working" if pending_bundle >= 5 else "idle",
        "activity": f"개별 보고서 {len(reports)}건 · 통합 대기 {pending_bundle}건",
        "progress": round(len(linked) * 100 / len(finished)) if finished else 0,
        "now": now,
        "next": next_items,
        "done": done,
        "artifacts": artifacts,
        "blockers": [{"label": f"#{r['no']} {r['summary']}", "detail": r["status"]}
                     for r in reports if r["status"] == "해결 불가"],
        "notes": [f"최근 이벤트 {len(env_status['events'])}건 기록됨"],
    }


# ── 최종 상태 ────────────────────────────────────────────────────────────────

def build_state() -> dict:
    """픽셀 오피스가 소비하는 전체 상태. 섹션별로 예외를 격리한다."""
    errors: list[str] = []

    def safe(label, fn, fallback):
        try:
            return fn()
        except Exception as exc:  # 원장 하나가 깨져도 화면은 살린다
            errors.append(f"{label}: {type(exc).__name__} {exc}")
            return fallback

    env_status = safe("env-status/README.md", load_env_status,
                      {"environments": [], "models": [], "events": []})
    tasks = safe("formal-results.md", load_formal_results, [])
    clerk = safe("clerk-reports", load_clerk_reports,
                 {"pending_bundle": 0, "reports": [], "bundles": [],
                  "report_files": [], "bundle_files": []})
    runs = safe("live runs", live_runs, [])
    runs_done = safe("full-runs", completed_runs, [])
    handoffs = safe("handoffs", lambda: load_handoffs(env_status["events"]), [])

    roles = []
    for label, builder in (("env-builder", lambda: build_builder(env_status, tasks)),
                           ("env-checker", lambda: build_checker(tasks, runs, runs_done)),
                           ("clerk", lambda: build_clerk(clerk, tasks, env_status))):
        role = safe(label, builder, None)
        if role:
            roles.append(role)

    done_tasks = [t for t in tasks if t["status"] in TERMINAL_DONE]
    pending = [t for t in tasks if t["status"] in {"pending", "running"}]
    blocked = [t for t in tasks if t["status"] in BLOCKED_STATES]

    now = datetime.now(KST)
    return {
        "updated": time.time(),
        "updated_kst": now.strftime("%Y-%m-%d %H:%M:%S KST"),
        "roles": roles,
        "runs": runs,
        "handoffs": handoffs,
        "events": env_status["events"][-8:],
        "stats": {
            "models": len(env_status["models"]),
            "environments": len(env_status["environments"]),
            "tasks_done": len(done_tasks),
            "tasks_pending": len(pending),
            "tasks_blocked": len(blocked),
            "runs_live": len(runs),
            "runs_recorded": len(runs_done),
            "reports": len(clerk["reports"]),
        },
        "errors": errors,
    }


if __name__ == "__main__":  # 원장 파싱 결과를 눈으로 확인할 때 쓴다
    import json
    print(json.dumps(build_state(), ensure_ascii=False, indent=2))
