"""Formal HyperGRL hyperedge-prediction runner.

The original HyperGRL script only exercised its node-classification branch.
This runner trains the same HyperGRL clique encoder on each official node
split, extracts one learned embedding per original node, and evaluates the
repository's official 20-seed incidence splits with ``MLP_HENN``.
"""
from __future__ import annotations

import argparse
import copy
import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import DataLoader
import dgl

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT))

from loader import DatasetLoader
from hyperedge_clique import HyperScorerGeneral
from hyperGRL_train_our import (
    edge_prediction_linear_eval,
    getData,
    getPretrainData,
    fix_seed,
)


def build_hyperedges(data):
    rows, cols = data.hyperedge_index[0].cpu(), data.hyperedge_index[1].cpu()
    incidences = defaultdict(list)
    for node, hedge in zip(rows.tolist(), cols.tolist()):
        incidences[int(hedge)].append(int(node))
    neighbors = defaultdict(set)
    for members in incidences.values():
        for u, v in combinations(members, 2):
            neighbors[u].add(v)
            neighbors[v].add(u)
    return {
        node: {"members": list(members), "category": int(data.labels[node].item())}
        for node, members in neighbors.items()
    }


@torch.no_grad()
def extract_embeddings(scorer, graphs, device, batch_size):
    scorer._model.eval()
    outputs = []
    for start in range(0, len(graphs), batch_size):
        bg = dgl.batch(graphs[start:start + batch_size]).to(device)
        outputs.append(scorer._model.encode(bg).detach())
    return torch.cat(outputs, dim=0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', required=True)
    parser.add_argument('--num_seeds', type=int, default=20)
    parser.add_argument('--epochs', type=int, default=200)
    parser.add_argument('--lr', type=float, default=0.001)
    parser.add_argument('--device', default='cuda:0')
    parser.add_argument('--cluster_num', type=int, default=10)
    parser.add_argument('--hidden_dim', type=int, default=128)
    parser.add_argument('--batch_size', type=int, default=64)
    parser.add_argument('--n_negative', type=int, default=8)
    parser.add_argument('--edge_epochs', type=int, default=1000,
                        help='linear EP probe epochs (use a small value only for smoke tests)')
    args = parser.parse_args()
    args.method = 'HyperGRL'

    device = torch.device(args.device if torch.cuda.is_available() else 'cpu')
    data = DatasetLoader().load(args.data).to(device)
    hyperedges = build_hyperedges(data)
    node_order = list(hyperedges)
    membership, g_hyperedge = getPretrainData(
        'edge', hyperedges, 'dis2cluster', cluster_number=args.cluster_num,
        pretext_classification=True)
    X, Y, Y_pre, num_categories = getData(
        str(device), hyperedges, data.features, list(range(data.num_nodes)),
        'hyperedge_clique', membership, g_hyperedge, args.cluster_num,
        ori_feat=True, rw_feat=False)

    scores = []
    for seed in range(args.num_seeds):
        fix_seed(seed)
        train_idx, valid_idx, _ = data.data_splits[seed]
        X_train = [X[int(i)] for i in train_idx]
        X_val = [X[int(i)] for i in valid_idx]
        y_train = [Y[int(i)] for i in train_idx]
        y_val = [Y[int(i)] for i in valid_idx]
        yp_train = [Y_pre[int(i)] for i in train_idx]
        yp_val = [Y_pre[int(i)] for i in valid_idx]
        counts = np.bincount(y_train, minlength=num_categories)
        weights = [1 - (c / max(1, counts.sum())) for c in counts]
        pre_counts = np.bincount(yp_train, minlength=args.cluster_num)
        pre_weights = [1 - (c / max(1, pre_counts.sum())) for c in pre_counts]
        scorer = HyperScorerGeneral(
            input_dim=data.features.shape[1],
            hidden_size=args.hidden_dim, num_class=num_categories,
            n_epochs=args.epochs, weight_tune=weights, cluster_num=args.cluster_num,
            weight_pre=pre_weights, n_negative=args.n_negative, lr=args.lr,
            device=str(device), batch_size=args.batch_size, dname=args.data,
            num_nodes=data.num_nodes)
        scorer.train(
            dname=args.data, g_list_train=X_train, labels_train_tune=y_train,
            labels_train_pre=yp_train, g_list_validation=X_val,
            labels_validation_tune=y_val, labels_validation_pre=yp_val,
            eval_metric=None, alpha=1, train_mode='pretrain',
            pretrain_node=True, pretrain_he=True, joint=False)
        embeds = extract_embeddings(scorer, X, device, args.batch_size)
        full = torch.zeros((data.num_nodes, embeds.shape[1]), device=device)
        full[torch.tensor(node_order, device=device)] = embeds
        split = data.edge_splits[seed]
        _, test_result, _ = edge_prediction_linear_eval(args, split, full, data)
        scores.append(float(test_result[0]))
        print(f'seed={seed} auroc={scores[-1]:.6f}', flush=True)

    result = np.asarray(scores, dtype=float)
    out = Path(f'results/result_{args.data}_HyperGRL_edge.txt')
    out.parent.mkdir(exist_ok=True)
    with out.open('a') as handle:
        handle.write(f'{result.tolist()} => {result.mean() * 100:.1f} ± {result.std() * 100:.1f}\n')
    print(f'Final Test AUROC: {result.mean() * 100:.1f} ± {result.std() * 100:.1f}')


if __name__ == '__main__':
    main()
