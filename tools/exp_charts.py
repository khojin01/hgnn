#!/usr/bin/env python3
"""
Leaderboard 수치를 태스크별 차트(PNG)로 그려 vault/assets/ 에 넣고 Charts.md 를 만든다.

    python bin/exp_charts.py --repo ~/hgnn-mirror --vault "~/Documents/Obsidian Vault/hgnn"

파싱은 exp2vault.py 의 함수를 그대로 쓴다 (같은 디렉토리에 있어야 한다).
라이트/다크 두 벌을 그린다. 노트에는 라이트를 넣고, 다크 테마를 쓰면 -dark 파일을 쓰면 된다.
"""
import argparse
import os
import sys
from collections import defaultdict
from datetime import date

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.font_manager import findfont, FontProperties

import exp2vault as E

# dataviz 기준 팔레트 --------------------------------------------------------
# 시퀀셜: 파랑 한 색, 100 -> 700. 라이트는 밝은 쪽이 '낮음',
# 다크는 표면(#1a1a19)에 가까운 어두운 쪽이 '낮음' 이 되도록 방향을 뒤집는다.
BLUE = ["#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7",
        "#3987e5", "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b"]

THEME = {
    "light": dict(surface="#fcfcfb", ink="#0b0b0b", ink2="#52514e",
                  grid="#e5e4e0", bar="#2a78d6", empty="#f0efec",
                  ramp=BLUE, hi_ink="#ffffff", lo_ink="#0b0b0b"),
    "dark": dict(surface="#1a1a19", ink="#ffffff", ink2="#c3c2b7",
                 grid="#383835", bar="#3987e5", empty="#2a2a28",
                 ramp=BLUE[::-1], hi_ink="#0b0b0b", lo_ink="#ffffff"),
}

TASKS = [("node", "Node classification", "정확도 (%)"),
         ("edge", "Hyperedge prediction", "예측 점수"),
         ("cluster", "Community detection", "NMI")]


def pick_font():
    """한글 폰트가 있으면 쓰고, 없으면 라벨을 영어로 돌린다."""
    for name in ("Malgun Gothic", "NanumGothic", "AppleGothic", "Noto Sans CJK KR"):
        try:
            if os.path.basename(findfont(FontProperties(family=name),
                                         fallback_to_default=False)):
                return name
        except Exception:
            continue
    return None


def collect(repo):
    """exp2vault 와 같은 규칙으로 (dataset, model, task) -> 최신값 을 모은다."""
    E.REPO = repo
    datasets, models = E.known_datasets(), E.known_models()
    results_dir = os.path.join(repo, "results")
    recs = []
    for name in sorted(os.listdir(results_dir)):
        if not name.endswith(".txt"):
            continue
        path = os.path.join(results_dir, name)
        if E.is_csv_snapshot(path, datasets):
            continue
        rs, _ = E.extract_records(path, datasets, models, name.startswith("pair_"))
        recs += [r for r in rs if r["dataset"] and r["model"]]

    groups = defaultdict(list)
    for r in recs:
        groups[(r["dataset"], r["model"], r["task"])].append(r)
    # 결과 파일은 append 방식이므로 마지막 줄이 최신이다 (노트의 '최신' 과 같은 값).
    return {k: v[-1]["mean"] for k, v in groups.items()}


def grid_for(latest, task):
    keys = [k for k in latest if k[2] == task]
    ds = sorted({k[0] for k in keys})
    mdl = sorted({k[1] for k in keys})
    # 평균이 높은 모델이 위로. 데이터셋 커버리지가 다르므로 개수를 함께 보여준다.
    def mean(m):
        vals = [latest[(d, m, task)] for d in ds if (d, m, task) in latest]
        return sum(vals) / len(vals), len(vals)
    mdl.sort(key=lambda m: mean(m)[0], reverse=True)
    return ds, mdl, {m: mean(m) for m in mdl}


def style(ax, t):
    ax.set_facecolor(t["surface"])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(colors=t["ink2"], length=0, labelsize=9)


def heatmap(latest, task, label, mode, out, ko):
    t = THEME[mode]
    ds, mdl, _ = grid_for(latest, task)
    if not ds:
        return None
    cmap = LinearSegmentedColormap.from_list("blue", t["ramp"])

    fig, ax = plt.subplots(figsize=(1.15 * len(ds) + 3.6, 0.36 * len(mdl) + 1.9))
    fig.patch.set_facecolor(t["surface"])
    style(ax, t)

    # 색은 '열(데이터셋) 안에서의 상대 위치'. 데이터셋마다 난이도가 달라
    # 전체 공통 스케일로 칠하면 어려운 데이터셋의 열이 통째로 흐려진다.
    col_rng = {}
    for d in ds:
        vals = [latest[(d, m, task)] for m in mdl if (d, m, task) in latest]
        col_rng[d] = (min(vals), max(vals)) if vals else (0.0, 1.0)

    for i, m in enumerate(mdl):
        for j, d in enumerate(ds):
            v = latest.get((d, m, task))
            if v is None:
                ax.add_patch(plt.Rectangle((j + 0.01, i + 0.01), 0.98, 0.98,
                                           facecolor=t["empty"], edgecolor="none"))
                ax.text(j + 0.5, i + 0.5, "—", ha="center", va="center",
                        color=t["ink2"], fontsize=8)
                continue
            lo, hi = col_rng[d]
            f = 0.5 if hi == lo else (v - lo) / (hi - lo)
            # 2px 간격을 남겨 칸이 서로 붙지 않게 한다
            ax.add_patch(plt.Rectangle((j + 0.01, i + 0.01), 0.98, 0.98,
                                       facecolor=cmap(f), edgecolor="none"))
            ax.text(j + 0.5, i + 0.5, f"{v:.1f}", ha="center", va="center",
                    fontsize=8.5, color=t["hi_ink"] if f > 0.55 else t["lo_ink"])

    ax.set_xlim(0, len(ds)); ax.set_ylim(0, len(mdl))
    ax.set_xticks([j + 0.5 for j in range(len(ds))])
    ax.set_xticklabels(ds, rotation=30, ha="right")
    ax.set_yticks([i + 0.5 for i in range(len(mdl))])
    ax.set_yticklabels(mdl)
    ax.invert_yaxis()
    ax.xaxis.set_ticks_position("top")
    ax.xaxis.set_label_position("top")

    sub = ("색 = 각 열 안에서의 상대 위치 · 숫자 = 실제 값"
           if ko else "color = rank within each column · number = actual value")
    ax.set_title(f"{label}\n{sub}", color=t["ink"], fontsize=12,
                 loc="left", pad=16, linespacing=1.6)
    fig.tight_layout()
    fig.savefig(out, dpi=170, facecolor=t["surface"])
    plt.close(fig)
    return out


def ranking(latest, task, label, unit, mode, out, ko):
    t = THEME[mode]
    ds, mdl, mean = grid_for(latest, task)
    if not ds:
        return None
    mdl = list(reversed(mdl))                    # 큰 값이 위로 오도록

    fig, ax = plt.subplots(figsize=(6.8, 0.34 * len(mdl) + 1.8))
    fig.patch.set_facecolor(t["surface"])
    style(ax, t)
    ax.xaxis.grid(True, color=t["grid"], linewidth=0.8)
    ax.set_axisbelow(True)

    vals = [mean[m][0] for m in mdl]
    ax.barh(range(len(mdl)), vals, height=0.62, color=t["bar"],
            edgecolor=t["surface"], linewidth=1.2)
    for i, m in enumerate(mdl):
        ax.text(vals[i] + max(vals) * 0.012, i, f"{vals[i]:.1f}",
                va="center", fontsize=8.5, color=t["ink2"])

    ax.set_yticks(range(len(mdl)))
    ax.set_yticklabels([f"{m}  ({mean[m][1]})" for m in mdl])
    ax.set_xlim(0, max(vals) * 1.12)
    ax.set_xlabel(unit, color=t["ink2"], fontsize=9)
    sub = (f"데이터셋 {len(ds)}개 평균 · 괄호는 실제 측정된 데이터셋 수"
           if ko else f"mean over {len(ds)} datasets · (n) = datasets measured")
    ax.set_title(f"{label}\n{sub}", color=t["ink"], fontsize=12,
                 loc="left", pad=14, linespacing=1.6)
    fig.tight_layout()
    fig.savefig(out, dpi=170, facecolor=t["surface"])
    plt.close(fig)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=os.path.expanduser("~/hgnn-mirror"))
    ap.add_argument("--vault", default=os.environ.get("HGNN_VAULT", E.DEFAULT_VAULT))
    args = ap.parse_args()

    repo = os.path.expanduser(args.repo)
    vault = os.path.expanduser(args.vault)
    assets = os.path.join(vault, "assets")
    os.makedirs(assets, exist_ok=True)

    font = pick_font()
    ko = font is not None
    if ko:
        plt.rcParams["font.family"] = font
    plt.rcParams["axes.unicode_minus"] = False

    latest = collect(repo)
    today = date.today().isoformat()

    made, lines = [], ["# 차트", "", f"갱신 {today} · 값은 각 조합의 **최신** 기록", ""]
    for task, label, unit in TASKS:
        if not any(k[2] == task for k in latest):
            continue
        ds, mdl, _ = grid_for(latest, task)
        lines += [f"## {label}", "",
                  f"모델 {len(mdl)}개 × 데이터셋 {len(ds)}개", ""]
        for kind, fn in (("heatmap", heatmap), ("rank", ranking)):
            for mode in ("light", "dark"):
                name = f"{task}-{kind}-{mode}.png"
                path = os.path.join(assets, name)
                if kind == "heatmap":
                    fn(latest, task, label, mode, path, ko)
                else:
                    fn(latest, task, label, unit, mode, path, ko)
                made.append(name)
            lines += [f"![[{task}-{kind}-light.png]]", ""]
    lines += ["> 다크 테마에서는 같은 이름의 `-dark.png` 를 쓰면 된다 "
              "(예: `![[node-heatmap-dark.png]]`).", "",
              "관련: [[Leaderboard]] · [[Home]]"]

    E.write_note(os.path.join(vault, "Charts.md"), "\n".join(lines),
                 frontmatter=["type: charts", f"updated: {today}", "tags: [hgnn/overview]"])
    print(f"차트 {len(made)}장 · {assets}")
    print(f"노트: {os.path.join(vault, 'Charts.md')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
