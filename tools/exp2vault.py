#!/usr/bin/env python3
"""
실험 결과(results/, logs/)를 Obsidian vault의 마크다운 노트로 변환한다.

사용법:
    python tools/exp2vault.py                 # 기본 vault 경로에 생성
    python tools/exp2vault.py --vault ~/foo   # 다른 vault 경로
    python tools/exp2vault.py --dry-run       # 쓰지 않고 요약만 출력
    python tools/exp2vault.py --report        # 파싱 실패한 줄을 모두 출력

노트의 <!-- AUTO:BEGIN --> ~ <!-- AUTO:END --> 사이만 덮어쓴다.
그 바깥에 직접 쓴 메모는 재실행해도 보존된다.
"""
import argparse
import os
import re
import sys
from collections import defaultdict
from datetime import date

# results/ · logs/ · data/ 가 있는 곳. --repo 로 바꿀 수 있어서
# 서버에서 받아온 사본을 대상으로 로컬 PC 에서 돌릴 수도 있다.
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_VAULT = os.path.expanduser("~/hojin_workspace/vault")

AUTO_BEGIN = "<!-- AUTO:BEGIN -->"
AUTO_END = "<!-- AUTO:END -->"

TASK_SUFFIXES = ("node", "edge", "time")
TASK_LABEL = {
    "node": "Node classification",
    "edge": "Hyperedge prediction",
    "cluster": "Community detection",
    "time": "실행 시간",
    "pair": "Pairwise 비교 (태스크 미상)",
    "unknown": "미분류",
}

# 줄 끝 "30.2 ± 3.1" / "32.2 ± nan"
SUM_RE = re.compile(r"([-\d.]+)\s*±\s*(nan|[-\d.]+)\s*$")
# "data:cora_coauth, NMI: 9.45"
NMI_RE = re.compile(r"^data:\s*(\S+?)\s*,\s*NMI:\s*([-\d.]+)\s*$")
# "cora_coauth=> 5.5749"  (단일 값, 시간)
VAL_RE = re.compile(r"^\s*([^=]+?)\s*=>\s*([-\d.]+)\s*$")
# "houselr0.0001_51.9 ± 0.0"
LR_RE = re.compile(r"^(\S+?)lr([-\d.]+)_")
# "0.001=> ..." 앞의 태그
TAG_RE = re.compile(r"^\s*([^=\[]+?)\s*=>")
# 날짜만 바뀐 것은 '변경'으로 치지 않는다. 그러지 않으면 매일 전체 노트가 diff 에 잡힌다.
VOLATILE_RE = re.compile(r"(updated: |갱신 )\d{4}-\d{2}-\d{2}")


def _ignoring_date(s):
    return VOLATILE_RE.sub(r"\1<DATE>", s)


# --------------------------------------------------------------------------
# 이름 해석
# --------------------------------------------------------------------------
def known_datasets():
    """data/ 디렉토리를 권위 있는 데이터셋 목록으로 삼는다. 긴 이름 우선."""
    d = os.path.join(REPO, "data")
    if not os.path.isdir(d):
        return []
    names = [n for n in os.listdir(d) if os.path.isdir(os.path.join(d, n))]
    return sorted(names, key=len, reverse=True)


def known_models():
    """레포 최상위 디렉토리 + 결과에서 관찰된 이름."""
    seen = {"AllSet", "EDHNN", "GraphMAE2", "HGD", "HGNN", "HNHN", "Hypeboy",
            "HyperGCL", "Hyper_GCN", "HyperGRL", "MaskGAE", "MLP", "PhenomNN",
            "SEHSSL", "TriCL", "UniGCN", "UniGCN2", "UniGIN", "VilLain"}
    for n in os.listdir(REPO):
        if os.path.isdir(os.path.join(REPO, n)) and not n.startswith((".", "_")):
            seen.add(n.replace("-", ""))
    return sorted(seen, key=len, reverse=True)


def split_name(stem, datasets):
    """'result_cora_coauth_Hyper_GCN_node' -> ('cora_coauth', 'Hyper_GCN', 'node')

    데이터셋명과 모델명 둘 다 '_' 를 포함할 수 있으므로
    task 는 접미사로, dataset 은 알려진 목록의 최장 접두사로 자른다.
    파일명에 데이터셋이 없으면 dataset=None 을 돌려주고, 줄에서 찾는다.
    """
    rest = stem
    for pre in ("result_", "pair_"):
        if rest.startswith(pre):
            rest = rest[len(pre):]
            break

    task = None
    for suf in TASK_SUFFIXES:
        if rest.endswith("_" + suf):
            task, rest = suf, rest[: -(len(suf) + 1)]
            break

    for ds in datasets:
        if rest == ds:
            return ds, None, task
        if rest.startswith(ds + "_"):
            return ds, rest[len(ds) + 1:], task
    return None, (rest or None), task


# --------------------------------------------------------------------------
# 결과 파일 -> 레코드
# --------------------------------------------------------------------------
def logical_lines(path):
    """tensor([...]) 가 여러 줄에 걸쳐도 요약값이 나올 때까지 이어붙인다."""
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            raw = f.read()
    except OSError:
        return
    buf = ""
    for line in raw.splitlines():
        s = line.strip()
        if not s:
            continue
        buf = (buf + " " + s).strip() if buf else s
        if SUM_RE.search(buf) or NMI_RE.match(buf) or VAL_RE.match(buf):
            yield buf
            buf = ""
        elif len(buf) > 50000:
            buf = ""
    if buf:
        yield buf


def extract_records(path, datasets, models, is_pair=False):
    """한 결과 파일에서 (dataset, model, task, metric, mean, std, tag) 레코드를 뽑는다.

    파일명에 없는 정보는 줄의 태그에서 찾는다. 반환: (records, failed_lines)
    """
    stem = os.path.basename(path)[:-4]
    ds_f, model_f, task_f = split_name(stem, datasets)

    # 'result_cluster_VilLain_node.txt' 처럼 태스크가 모델명 앞에 붙은 파일이 있다.
    # 떼어내지 않으면 'cluster_VilLain' 이 별개 모델로 갈라진다.
    if model_f:
        for pre in ("cluster", "node", "edge", "time"):
            if model_f.startswith(pre + "_") and model_f[len(pre) + 1:] in models:
                model_f, task_f = model_f[len(pre) + 1:], pre
                break

    recs, failed = [], []

    for line in logical_lines(path):
        ds, model, task = ds_f, model_f, task_f
        metric, mean, std, tag = "score", None, None, None

        m = NMI_RE.match(line)
        if m:
            ds, task, metric = m.group(1), "cluster", "NMI"
            mean = float(m.group(2))
            recs.append(dict(dataset=ds, model=model, task=task, metric=metric,
                             mean=mean, std=std, tag=tag))
            continue

        m = LR_RE.match(line)
        if m and m.group(1) in datasets:
            ds, tag = m.group(1), f"lr{m.group(2)}"

        s = SUM_RE.search(line)
        if s:
            try:
                mean = float(s.group(1))
            except ValueError:
                failed.append((stem, line[:120]))
                continue
            std = None if s.group(2) == "nan" else float(s.group(2))
            if tag is None:
                t = TAG_RE.match(line)
                if t:
                    tag = t.group(1).strip()
        else:
            v = VAL_RE.match(line)
            if not v:
                failed.append((stem, line[:120]))
                continue
            tag, mean = v.group(1).strip(), float(v.group(2))
            metric, task = "seconds", task or "time"

        # 태그가 데이터셋명·모델명이면 신원 정보이므로 설정 태그에서 비운다.
        # 그 외(예: '0.001', 'lr0.0001')는 하이퍼파라미터이므로 그대로 둔다.
        if tag:
            if tag in datasets:
                ds, tag = tag, None
            elif tag in models:
                model, tag = tag, None
                if is_pair:
                    task = "pair"

        recs.append(dict(dataset=ds, model=model, task=task or "unknown",
                         metric=metric, mean=mean, std=std, tag=tag))
    return recs, failed


def is_csv_snapshot(path, datasets):
    """'cora_coauth,MLP,32.2 ± nan' 형태가 대부분이면 스냅샷 파일로 본다."""
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            lines = [l.strip() for l in f if l.strip()][:30]
    except OSError:
        return False
    if not lines:
        return False
    hit = sum(1 for l in lines
              if len(l.split(",")) >= 3 and l.split(",")[0].strip() in datasets)
    return hit >= max(2, len(lines) * 0.6)


def parse_csv_snapshot(path):
    """'cora_coauth,MLP,32.2 ± nan' 형태의 스냅샷 파일."""
    rows = []
    if not os.path.exists(path):
        return rows
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            parts = [p.strip() for p in line.strip().split(",")]
            if len(parts) < 3:
                continue
            m = SUM_RE.search(parts[-1])
            if not m:
                continue
            try:
                mean = float(m.group(1))
            except ValueError:
                continue
            rows.append(dict(dataset=parts[0], model=parts[1], mean=mean,
                             std=None if m.group(2) == "nan" else float(m.group(2))))
    return rows



# --------------------------------------------------------------------------
# 노트 쓰기
# --------------------------------------------------------------------------
def fmt(mean, std, metric="score"):
    if mean is None:
        return "—"
    if metric == "seconds":
        return f"{mean:.1f}s"
    if std is None:
        return f"{mean:.1f}"
    return f"{mean:.1f} ± {std:.1f}"


def write_note(path, body, frontmatter=None, dry_run=False):
    """frontmatter(항상 1행부터) + AUTO 블록을 교체하고, 그 뒤 사용자 메모는 보존한다.

    Obsidian 은 YAML frontmatter 가 파일 맨 앞에 있어야 인식하므로
    AUTO 마커 바깥에 둔다.
    """
    fm = f"---\n" + "\n".join(frontmatter) + "\n---\n\n" if frontmatter else ""
    block = f"{AUTO_BEGIN}\n{body}\n{AUTO_END}"
    old = None
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            old = f.read()
        tail = old
        if tail.startswith("---\n"):                 # 기존 frontmatter 제거
            end = tail.find("\n---\n", 4)
            if end != -1:
                tail = tail[end + 5:]
        if AUTO_BEGIN in tail and AUTO_END in tail:
            # 본문이 마커 문자열을 담고 있어도 블록이 조기 종료되지 않도록 마지막 END 기준
            new = fm + block + tail.rsplit(AUTO_END, 1)[1]
        else:
            new = fm + block + "\n\n" + tail.lstrip()
    else:
        new = fm + block + "\n\n## 메모\n\n\n"
    # 실제 내용이 같고 날짜만 다르면 쓰지 않는다 (기존 updated: 값을 유지)
    if old is not None and _ignoring_date(old) == _ignoring_date(new):
        return False
    if not dry_run:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(new)
    return True


def slug(*parts):
    return "-".join(str(p) for p in parts if p)


# --------------------------------------------------------------------------
def main():
    global REPO
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", default=os.environ.get("HGNN_VAULT", DEFAULT_VAULT))
    ap.add_argument("--repo", default=os.environ.get("HGNN_REPO", REPO),
                    help="results/ · logs/ · data/ 가 있는 디렉토리")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--report", action="store_true", help="파싱 실패한 줄을 출력")
    args = ap.parse_args()

    REPO = os.path.expanduser(args.repo)
    vault = os.path.expanduser(args.vault)
    datasets, models = known_datasets(), known_models()
    if not datasets:
        print(f"data/ 를 찾을 수 없습니다: {REPO}/data", file=sys.stderr)
        return 1

    results_dir = os.path.join(REPO, "results")
    today = date.today().isoformat()

    # ---- 1. 모든 결과 파일에서 레코드 추출 ----
    all_recs, all_failed, snapshot_files = [], [], []
    for name in sorted(os.listdir(results_dir)):
        if not name.endswith(".txt"):
            continue
        path = os.path.join(results_dir, name)
        # 'dataset,model,값 ± std' CSV 스냅샷은 Leaderboard 에서 따로 다룬다
        if is_csv_snapshot(path, datasets):
            snapshot_files.append(name)
            continue
        is_pair = name.startswith("pair_")
        recs, failed = extract_records(path, datasets, models, is_pair)
        if not recs:
            snapshot_files.append(name)
            continue
        keep = [r for r in recs if r["dataset"] and r["model"]]
        for r in keep:
            r["src"] = f"results/{name}"
        if len(keep) < len(recs):
            all_failed += [(name, "데이터셋/모델 미확인")] * (len(recs) - len(keep))
        all_recs += keep
        all_failed += failed

    # ---- 2. (dataset, model, task, metric) 으로 묶기 ----
    groups = defaultdict(list)
    for r in all_recs:
        groups[(r["dataset"], r["model"], r["task"], r["metric"])].append(r)

    runs = []
    for (ds, model, task, metric), rs in groups.items():
        best = min(rs, key=lambda e: e["mean"]) if metric == "seconds" \
            else max(rs, key=lambda e: e["mean"])
        runs.append(dict(dataset=ds, model=model, task=task, metric=metric,
                         entries=rs, latest=rs[-1], best=best,
                         srcs=sorted({r["src"] for r in rs})))

    # ---- 3. (조합별 run 노트는 만들지 않는다) ----
    # 조합 230개를 각각 노트로 만들면 그래프 뷰가 run 노트로 뒤덮여 읽을 수 없다.
    # 수치는 데이터셋 노트와 모델 노트의 표에 그대로 들어가고,
    # 그래프에는 데이터셋 ↔ 모델 연결만 남긴다.
    changed = 0

    # ---- 4. 데이터셋 노트 ----
    by_ds = defaultdict(list)
    for r in runs:
        by_ds[r["dataset"]].append(r)

    for ds, rs in sorted(by_ds.items()):
        front = [f"type: dataset", f"models: {len({r['model'] for r in rs})}",
                 f"updated: {today}", "tags: [hgnn/dataset]"]
        lines = [f"# {ds}", "",
                 f"모델 {len({r['model'] for r in rs})}개 · 조합 {len(rs)}건 · 갱신 {today}", ""]
        for task in ("node", "edge", "cluster", "pair", "time", "unknown"):
            sub = [r for r in rs if r["task"] == task]
            if not sub:
                continue
            lines += [f"## {TASK_LABEL[task]}", "",
                      "| 모델 | 최신 | 최고 | 기록 |", "|---|---:|---:|---:|"]
            rev = (task == "time")
            for r in sorted(sub, key=lambda x: x["latest"]["mean"], reverse=not rev):
                lines.append(
                    f"| [[{r['model']}]] "
                    f"| {fmt(r['latest']['mean'], r['latest']['std'], r['metric'])} "
                    f"| {fmt(r['best']['mean'], r['best']['std'], r['metric'])} "
                    f"| {len(r['entries'])} |")
            lines.append("")
        lines.append("전체: [[Leaderboard]]")
        if write_note(os.path.join(vault, "datasets", f"{ds}.md"),
                      "\n".join(lines), frontmatter=front, dry_run=args.dry_run):
            changed += 1

    # ---- 4b. 모델 노트 ----
    # 그래프 뷰에서 데이터셋 뿐 아니라 모델로도 묶이도록 허브 노트를 둔다.
    # run 노트가 [[dataset]] · [[model]] 을 모두 가리키므로 모델–run–데이터셋 으로 이어진다.
    by_model = defaultdict(list)
    for r in runs:
        by_model[r["model"]].append(r)

    for model, rs in sorted(by_model.items()):
        covered = sorted({r["dataset"] for r in rs})
        srcs = sorted({s for r in rs for s in r["srcs"]})
        front = [f"type: model", f"datasets: {len(covered)}",
                 f"updated: {today}", "tags: [hgnn/model]"]
        lines = [f"# {model}", "",
                 f"데이터셋 {len(covered)}개 · 조합 {len(rs)}건 · 갱신 {today}", ""]
        for task in ("node", "edge", "cluster", "pair", "time", "unknown"):
            sub = [r for r in rs if r["task"] == task]
            if not sub:
                continue
            lines += [f"## {TASK_LABEL[task]}", "",
                      "| 데이터셋 | 최신 | 최고 | 기록 |", "|---|---:|---:|---:|"]
            rev = (task == "time")
            for r in sorted(sub, key=lambda x: x["latest"]["mean"], reverse=not rev):
                lines.append(
                    f"| [[{r['dataset']}]] "
                    f"| {fmt(r['latest']['mean'], r['latest']['std'], r['metric'])} "
                    f"| {fmt(r['best']['mean'], r['best']['std'], r['metric'])} "
                    f"| {len(r['entries'])} |")
            lines.append("")
        lines += ["## 원본 파일", ""]
        lines += [f"- `{s}`" for s in srcs]
        lines += ["", "전체: [[Leaderboard]]"]
        if write_note(os.path.join(vault, "models", f"{model}.md"),
                      "\n".join(lines), frontmatter=front, dry_run=args.dry_run):
            changed += 1

    # ---- 5. 리더보드 ----
    lines = ["# Leaderboard", "",
             f"갱신 {today} · 조합 {len(runs)}건 · 레코드 {len(all_recs)}건", ""]
    for task in ("node", "edge", "cluster"):
        sub = [r for r in runs if r["task"] == task]
        if not sub:
            continue
        ds_list = sorted({r["dataset"] for r in sub})
        grid = {(r["dataset"], r["model"]): r["latest"] for r in sub}
        lines += [f"## {TASK_LABEL[task]}", "",
                  "| 모델 | " + " | ".join(ds_list) + " |",
                  "|---|" + "---:|" * len(ds_list)]
        for m in sorted({r["model"] for r in sub}):
            cells = [fmt(grid[(d, m)]["mean"], grid[(d, m)]["std"])
                     if (d, m) in grid else "—" for d in ds_list]
            lines.append(f"| [[{m}]] | " + " | ".join(cells) + " |")
        lines.append("")

    for snap, note in (("result_small.txt", "small split"),
                       ("results/result_118.txt", "1:1:8 split")):
        rows = parse_csv_snapshot(os.path.join(REPO, snap))
        if not rows:
            continue
        lines += [f"## 스냅샷 — {note}", "",
                  f"원본 `{snap}` · {len(rows)}행. 같은 조합이 여러 번 나타날 수 있다.", "",
                  "| 데이터셋 | 모델 | 값 |", "|---|---|---:|"]
        lines += [f"| {r['dataset']} | {r['model']} | {fmt(r['mean'], r['std'])} |"
                  for r in rows]
        lines.append("")

    if write_note(os.path.join(vault, "Leaderboard.md"), "\n".join(lines),
                  frontmatter=["type: overview", f"updated: {today}", "tags: [hgnn/overview]"],
                  dry_run=args.dry_run):
        changed += 1

    # ---- 6. (스윕 노트는 만들지 않는다) ----
    # logs/ 의 'dataset_dim128_nl2_...' 는 VilLain main.py 의 사전학습 로그뿐이고,
    # 표에 남는 Local/Global 손실은 results/ 의 다운스트림 점수와 연결되지 않는다.
    # 2026-09-15 에 노트 생성을 중단했다. 원본 로그는 서버에 그대로 있다.

    # ---- 7. 파싱 현황 (빠진 것을 숨기지 않는다) ----
    lines = ["# 파싱 현황", "", f"갱신 {today}", "",
             f"- 결과 파일에서 추출한 레코드: **{len(all_recs)}건**",
             f"- (데이터셋 × 모델 × 태스크) 조합: **{len(runs)}개**",
             f"- 해석하지 못한 줄: **{len(all_failed)}건**", ""]
    if snapshot_files:
        lines += ["## 레코드가 없는 파일", "",
                  "CSV 스냅샷이거나 형식이 다른 파일. Leaderboard 하단에서 따로 다룬다.", ""]
        lines += [f"- `results/{n}`" for n in snapshot_files] + [""]
    lines += ["## 노트로 만들지 않는 것", "",
              "`logs/` 의 학습 로그는 노트로 만들지 않는다. VilLain 사전학습의 Local/Global 손실이 "
              "`results/` 의 다운스트림 점수와 연결되지 않아 표로 두어도 읽을 것이 없었다. "
              "원본은 서버의 `logs/` 에 그대로 있다.", ""]
    if all_failed:
        lines += ["## 해석하지 못한 줄", "",
                  "형식이 새로 추가되었을 수 있다. `tools/exp2vault.py` 의 정규식을 확인할 것.", "",
                  "| 파일 | 줄 |", "|---|---|"]
        for f, l in all_failed[:80]:
            lines.append(f"| `{f}` | `{l.replace('|', '\\|')}` |")
        if len(all_failed) > 80:
            lines.append(f"| … | 외 {len(all_failed) - 80}건 |")
        lines.append("")
    lines += ["## 주의", "",
              "- `pair` 태스크는 원본 파일에 태스크 표기가 없어 node/edge 를 구분하지 못한다. 수동 확인 필요.",
              "- `node` 는 분류 정확도, `edge` 는 하이퍼엣지 예측 점수, `cluster` 는 NMI 로 가정했다.",
              "- 결과 파일은 append 방식이라 '최신' 은 파일의 마지막 기록을 뜻한다."]
    if write_note(os.path.join(vault, "파싱 현황.md"), "\n".join(lines),
                  frontmatter=["type: status", f"updated: {today}", "tags: [hgnn/overview]"],
                  dry_run=args.dry_run):
        changed += 1

    # ---- 8. 홈 노트 ----
    home = ["# HGNN 실험 노트", "", f"갱신 {today}", "",
            "## 데이터셋", ""]
    home += [f"- [[{ds}]] — 조합 {len(rs)}건" for ds, rs in sorted(by_ds.items())]
    home += ["", "## 모델", ""]
    home += [f"- [[{m}]] — 데이터셋 {len({r['dataset'] for r in rs})}개"
             for m, rs in sorted(by_model.items())]
    home += ["", "## 전체", "", "- [[Leaderboard]] — 데이터셋 × 모델 표"]
    if os.path.exists(os.path.join(vault, "Charts.md")):
        home += ["- [[Charts]] — 태스크별 히트맵·순위 차트"]
    home += ["- [[파싱 현황]] — 무엇이 반영되고 무엇이 빠졌는지", "",
             "## 갱신 방법", ""]
    # 결과 원본 옆에 tools/ 가 있으면 서버의 레포, 없으면 로컬 PC 가 받아온 사본이다.
    on_server = os.path.isdir(os.path.join(REPO, "tools"))
    if on_server:
        home += ["```bash", "cd ~/hojin_workspace/hgnn", "python tools/exp2vault.py", "```",
                 "", "또는 Claude Code 에서 `/exp-log`."]
    else:
        home += ["서버에서 결과 원본을 다시 받아 이 노트를 새로 만든다.", "",
                 "```powershell",
                 'powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\\bin\\pull_hgnn.ps1"',
                 "```",
                 "", "macOS·Linux 는 `pull_from_server.sh` (rsync 사용)."]
    home += ["",
             "> 각 노트에서 자동 생성 구간(AUTO:BEGIN ~ AUTO:END 주석 사이)만 덮어쓴다.",
             "> 그 **아래 `## 메모`** 에 쓴 내용은 재실행해도 보존된다.", "",
             "## 동기화", ""]
    if on_server:
        home += ["이 vault 는 **서버에서 확인하는 용도**다. 로컬 PC 의 Obsidian vault 와는 별개다.", ""]
    else:
        home += ["이 vault 는 **로컬 PC 용**이다. 서버의 `~/hojin_workspace/vault` 와는 별개다.", ""]
    home += ["| | 하는 일 |", "|---|---|",
             "| 서버 | 실험 → `/exp-log` → 서버 vault 갱신 |",
             "| 로컬 PC | `results/`·`logs/` 원본만 받아 → 자기 쪽에서 노트 생성 |", "",
             "메모는 로컬 PC 의 vault 에만 존재하고 서버로 오지 않는다. 덮어쓸 일이 구조적으로 없다."]
    if write_note(os.path.join(vault, "Home.md"), "\n".join(home),
                  frontmatter=["type: home", f"updated: {today}", "tags: [hgnn/overview]"],
                  dry_run=args.dry_run):
        changed += 1

    verb = "변경될 노트" if args.dry_run else "갱신된 노트"
    print(f"{verb}: {changed}개")
    print(f"  레코드 {len(all_recs)} · 조합 {len(runs)} · "
          f"데이터셋 {len(by_ds)} · 모델 {len(by_model)}")
    print(f"  해석 실패 {len(all_failed)}건" + ("  (--report 로 확인)" if all_failed else ""))
    print(f"  vault: {vault}")
    if args.report and all_failed:
        print("\n해석하지 못한 줄:")
        for f, l in all_failed:
            print(f"  [{f}] {l}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
