#!/usr/bin/env python3
"""커뮤니티 탐지(Table 5) 평가 — 저장된 노드 임베딩을 k-means 로 군집하고 NMI 를 잰다.

    python3 tools/cluster_eval.py --model-dir VilLain --data house \
        --emb VilLain/embs/house_dim128_ns4_nsg100_lr0.0001_merged.pkl

모델 코드는 건드리지 않는다. 각 모델이 이미 저장해 둔 임베딩과 저장소 공용 로더의
레이블만 읽는다. 군집 수는 레이블의 고유값 수다 (논문과 같은 방식).

정식 실행 규약이 20 seed 를 요구하므로 k-means 를 seed 0..19 로 20번 돌리고
`[v1, ..., v20], 평균 ± 표준편차` 형식으로 적는다. 원장 파서가 읽는 형식이다.

    results/result_<data>_<모델디렉터리>_cluster.txt

VilLain/eval.py 의 `--task cluster` 는 seed 42 한 번만 돌려 표준편차가 없고
파일명도 데이터셋을 담지 않는다. 그래서 그 경로 대신 이 도구를 쓴다.
"""
from __future__ import annotations

import argparse
import os
import pickle
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-dir", required=True, help="모델 디렉터리 이름 (결과 파일 이름에도 쓰인다)")
    ap.add_argument("--data", required=True, help="원시 데이터셋 이름 (citeseer_cite 등)")
    ap.add_argument("--emb", required=True, help="노드 임베딩 pickle 경로")
    ap.add_argument("--seeds", type=int, default=20)
    ap.add_argument("--out-name", default=None, help="결과 파일의 모델 표기 (기본: --model-dir)")
    a = ap.parse_args()

    import numpy as np
    import torch
    from sklearn.cluster import KMeans
    from sklearn.metrics import normalized_mutual_info_score

    mdir = ROOT / a.model_dir
    sys.path.insert(0, str(mdir))
    os.chdir(ROOT)                      # 로더가 data/<이름> 상대경로를 쓴다
    from loader import DatasetLoader    # 각 모델 디렉터리의 공용 로더

    data = DatasetLoader().load(a.data)
    labels = data.labels.detach().cpu().numpy()

    with open(a.emb, "rb") as f:
        z = pickle.load(f)
    if isinstance(z, torch.Tensor):
        z = z.detach().cpu().numpy()
    z = np.asarray(z)
    if z.shape[0] != labels.shape[0]:
        raise SystemExit("임베딩 %d행 vs 레이블 %d개 — 맞지 않는다" % (z.shape[0], labels.shape[0]))

    k = int(np.unique(labels).size)
    scores = []
    for s in range(a.seeds):
        pred = KMeans(n_clusters=k, random_state=s, n_init=10).fit_predict(z)
        scores.append(normalized_mutual_info_score(labels, pred) * 100)

    mean, std = float(np.mean(scores)), float(np.std(scores))
    name = a.out_name or a.model_dir
    out = ROOT / "results" / ("result_%s_%s_cluster.txt" % (a.data, name))
    out.parent.mkdir(exist_ok=True)
    body = "%s => [%s],%.1f ± %.1f\n" % (name, ", ".join("%.4f" % v for v in scores), mean, std)
    with out.open("a", encoding="utf-8") as f:
        f.write(body)
    print("%s · %s · k=%d · NMI %.2f ± %.2f → %s" % (name, a.data, k, mean, std, out.name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
