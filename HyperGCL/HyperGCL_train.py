#!/usr/bin/env python
# coding: utf-8

import os
import time
# import math
import torch
# import pickle
import argparse
import random
import numpy as np
import os.path as osp



from collections import defaultdict, Counter
import scipy.sparse as sp
import torch_sparse
import torch.nn as nn
import torch.nn.functional as F
import matplotlib.pyplot as plt
import copy
from tqdm import tqdm

from layers import *
from models import *
from collections import defaultdict
from torch_geometric.utils import dropout_adj, degree, to_undirected, k_hop_subgraph
from torch_geometric.data import Data
from generator import *
from sampling import negative_sampling

from sklearn.metrics import roc_auc_score as auroc
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from loader import DatasetLoader

def fix_seed(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    random.seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = True

class Logger(object):
    """ Adapted from https://github.com/snap-stanford/ogb/ """

    def __init__(self, runs, info=None):
        self.info = info
        self.results = [[] for _ in range(runs)]

    def add_result(self, run, result):
        assert len(result) == 3
        assert run >= 0 and run < len(self.results)
        self.results[run].append(result)

    def print_statistics(self, run=None):
        if run is not None:
            result = 100 * torch.tensor(self.results[run])
            argmax = result[:, 1].argmax().item()
            print(f'Run {run + 1:02d}:')
            print(f'Highest Train: {result[:, 0].max():.2f}')
            print(f'Highest Valid: {result[:, 1].max():.2f}')
            print(f'  Final Train: {result[argmax, 0]:.2f}')
            print(f'   Final Test: {result[argmax, 2]:.2f}')
        else:
            result = 100 * torch.tensor(self.results)

            best_results = []
            for r in result:
                train1 = r[:, 0].max().item()
                valid = r[:, 1].max().item()
                train2 = r[r[:, 1].argmax(), 0].item()
                test = r[r[:, 1].argmax(), 2].item()
                best_results.append((train1, valid, train2, test))

            best_result = torch.tensor(best_results)

            print(f'All runs:')
            r = best_result[:, 0]
            print(f'Highest Train: {r.mean():.2f} ± {r.std():.2f}')
            r = best_result[:, 1]
            print(f'Highest Valid: {r.mean():.2f} ± {r.std():.2f}')
            r = best_result[:, 2]
            print(f'  Final Train: {r.mean():.2f} ± {r.std():.2f}')
            r = best_result[:, 3]
            print(f'   Final Test: {r.mean():.2f} ± {r.std():.2f}')

            return best_result[:, 1], best_result[:, 3]

@torch.no_grad()
def evaluate_n(model, data, split_idx, eval_func, result=None):
    if result is not None:
        out = result
    else:
        model.eval()
        out = model(data)
        out = F.log_softmax(out, dim=1)

    train_acc = eval_func(
        data.labels[split_idx[0]], out[split_idx[0]])
    valid_acc = eval_func(
        data.labels[split_idx[1]], out[split_idx[1]])
    test_acc = eval_func(
        data.labels[split_idx[2]], out[split_idx[2]])

#     Also keep track of losses
    train_loss = F.nll_loss(
        out[split_idx[0]], data.labels[split_idx[0]])
    valid_loss = F.nll_loss(
        out[split_idx[1]], data.labels[split_idx[1]])
    test_loss = F.nll_loss(
        out[split_idx[2]], data.labels[split_idx[2]])
    return train_acc, valid_acc, test_acc, train_loss, valid_loss, test_loss, out

@torch.no_grad()
def evaluate_e(model, train_data, valid_data, test_data, eval_func_e):
    train_auroc,train_loss = eval_func_e(model,train_data)
    valid_auroc,valid_loss = eval_func_e(model,valid_data)
    test_auroc,test_loss = eval_func_e(model,test_data)
    return train_auroc, valid_auroc, test_auroc, train_loss, valid_loss, test_loss


def eval_acc_node(y_true, y_pred):
    acc_list = []
    y_true = y_true.detach().cpu().numpy()
    y_pred = y_pred.argmax(dim=-1, keepdim=False).detach().cpu().numpy()

#     ipdb.set_trace()
#     for i in range(y_true.shape[1]):
    is_labeled = y_true == y_true
    correct = y_true[is_labeled] == y_pred[is_labeled]
    acc_list.append(float(np.sum(correct))/len(correct))

    return sum(acc_list)/len(acc_list)

def eval_acc_edge(model, data_split):
    v=data_split[0]
    e=torch.tensor(data_split[1]).to(args.device)
    label=data_split[2]

    with torch.no_grad():
        model.eval()
        out=model(data,v,e)
        pred=torch.sigmoid(out).squeeze(-1).detach().cpu().numpy()

    y_true = label.detach().cpu().numpy()
    score=auroc(y_true,pred)
    loss=F.binary_cross_entropy(torch.tensor(pred), label)

    return score,loss

    return valid_results, test_results, best_epochs


def permute_edges(data, aug_ratio, permute_self_edge):
    node_num, _ = data.features.size()
    _, edge_num = data.hyperedge_index.size()
    if not permute_self_edge:
        permute_num = int((edge_num-node_num) * aug_ratio)
    else:
        permute_num = int(edge_num * aug_ratio)
    edge_index = data.hyperedge_index
    device = edge_index.device
    if args.add_e:
        idx_add = torch.stack((
            torch.randint(node_num, (permute_num,), device=device),
            torch.randint(int(data.num_edges), (permute_num,), device=device),
        ), dim=0)
    if permute_self_edge:
        keep_idx = torch.randperm(edge_num, device=device)[:edge_num - permute_num]
        edge_after_remove = edge_index[:, keep_idx]
    # else:
    #     edge2remove_index = np.where(edge_index[1] < data.num_hyperedges[0].item())[0]
    #     edge2keep_index = np.where(edge_index[1] >= data.num_hyperedges[0].item())[0]
    #     edge_remove_index = np.random.choice(edge2remove_index, permute_num, replace=False)
    #     edge_keep_index = list(set(list(range(edge_num)))-set(edge_remove_index))
    #     edge_after_remove = edge_index[:, edge_keep_index]
    else:
        edge2remove_index = torch.nonzero(edge_index[1] < data.num_edges, as_tuple=False).flatten()
        edge2keep_index = torch.nonzero(edge_index[1] >= data.num_edges, as_tuple=False).flatten()
        keep_count = edge2remove_index.numel() - permute_num
        keep_idx = edge2remove_index[torch.randperm(edge2remove_index.numel(), device=device)[:keep_count]]
        edge_after_remove1 = edge_index[:, keep_idx]
        edge_after_remove2 = edge_index[:, edge2keep_index]
    if args.add_e:
        edge_index = torch.cat((edge_after_remove, idx_add), dim=1)
    else:
        # edge_index = edge_after_remove
        edge_index = torch.cat((edge_after_remove1, edge_after_remove2), dim=1)
    data.hyperedge_index = edge_index
    return data


def permute_hyperedges(data, aug_ratio):
    
    node_num, _ = data.x.size()
    _, edge_num = data.edge_index.size()
    hyperedge_num = int(data.num_hyperedges[0].item())
    permute_num = int(hyperedge_num * aug_ratio)
    index = defaultdict(list)
    edge_index = data.edge_index.cpu().numpy()
    # time1 = time.time()
    # for i, he in enumerate(edge_index[1]):
    #     index[he].append(i)
    # time2 = time.time()

    # edge2keep_index = np.where(edge_index[1] >= data.num_hyperedges[0].item())[0]
    # edge_keep_index = np.random.choice(hyperedge_num, hyperedge_num-permute_num, replace=False)
    # edge_keep_index_all = []
    # for keep_index in edge_keep_index:
    #     edge_keep_index_all.extend(he_index[keep_index])
    # edge_keep_index_all = np.concatenate((edge_keep_index_all, edge2keep_index))
    # edge_after_remove = edge_index[:, edge_keep_index_all]
    # edge_index = edge_after_remove
    edge_remove_index = np.random.choice(hyperedge_num, permute_num, replace=False)
    edge_remove_index_all = []
    for remove_index in edge_remove_index:
        edge_remove_index_all.extend(he_index[remove_index])
    edge_keep_index = list(set(list(range(edge_num)))-set(edge_remove_index_all))
    edge_after_remove = edge_index[:, edge_keep_index]
    edge_index = edge_after_remove
    
    data.edge_index = torch.tensor(edge_index)
    return data


def adapt(data, aug_ratio, aug):

    node_num, _ = data.x.size()
    _, edge_num = data.edge_index.size()
    hyperedge_num = int(data.num_hyperedges[0].item())
    permute_num = int(hyperedge_num * aug_ratio)
    index = defaultdict(list)
    edge_index = data.edge_index.cpu().numpy()
    for i, he in enumerate(edge_index[1]):
        index[he].append(i)
    # edge
    drop_weights = degree_drop_weights(data.edge_index, hyperedge_num)
    edge_index_1 = drop_edge_weighted(data.edge_index, drop_weights, p=aug_ratio, threshold=0.7, h=hyperedge_num, index=index)
    
    # feature
    edge_index_ = data.edge_index
    node_deg = degree(edge_index_[0])
    feature_weights = feature_drop_weights(data.x, node_c=node_deg)
    x_1 = drop_feature_weighted(data.x, feature_weights, aug_ratio, threshold=0.7)
    if aug=="adapt_edge":
        data.edge_index = edge_index_1
    elif aug=="adapt_feat":
        data.x = x_1
    else:
        data.edge_index = edge_index_1
        data.x = x_1
    return data

def drop_feature_weighted(x, w, p: float, threshold: float = 0.7):
    w = w / w.mean() * p
    
    w = w.where(w < threshold, torch.ones_like(w) * threshold)
    drop_prob = w
    drop_mask = torch.bernoulli(drop_prob).to(torch.bool)

    x = x.clone()
    x[:, drop_mask] = 0.

    return x

def degree_drop_weights(edge_index, h):
    edge_index_ = edge_index
    deg = degree(edge_index_[1])[:h]
    # deg_col = deg[edge_index[1]].to(torch.float32)
    deg_col = deg
    s_col = torch.log(deg_col)
    # weights = (s_col.max() - s_col+1e-9) / (s_col.max() - s_col.mean()+1e-9)
    weights = (s_col - s_col.min()+1e-9) / (s_col.mean() - s_col.min()+1e-9)
    return weights

def feature_drop_weights(x, node_c):
    x = torch.abs(x).to(torch.float32)
    w = x.t() @ node_c
    w = w.log()
    s = (w - w.min()) / (w.mean() - w.min())
    return s

def drop_edge_weighted(edge_index, edge_weights, p: float, h, index, threshold: float = 1.):
    _, edge_num = edge_index.size()
    edge_weights = (edge_weights+1e-9) / (edge_weights.mean()+1e-9) * p
    edge_weights = edge_weights.where(edge_weights < threshold, torch.ones_like(edge_weights) * threshold)
    # keep probability
    sel_mask = torch.bernoulli(edge_weights).to(torch.bool)
    edge_remove_index = np.array(list(range(h)))[sel_mask.cpu().numpy()]
    edge_remove_index_all = []
    for remove_index in edge_remove_index:
        edge_remove_index_all.extend(index[remove_index])
    edge_keep_index = list(set(list(range(edge_num)))-set(edge_remove_index_all))
    edge_after_remove = edge_index[:, edge_keep_index]
    edge_index = edge_after_remove
    return edge_index

def mask_nodes(data, aug_ratio):

    node_num, feat_dim = data.x.size()
    mask_num = int(node_num * aug_ratio)

    token = data.x.mean(dim=0)
    zero_v = torch.zeros_like(token)
    idx_mask = np.random.choice(node_num, mask_num, replace=False)
    data.x[idx_mask] = token

    return data

def aug(data, args):
    data_aug = copy.deepcopy(data)
    if args.aug=="mask":
        data_aug = mask_nodes(data_aug, args.aug_ratio)
    elif args.aug=="edge":
        data_aug = permute_edges(data_aug, args.aug_ratio, args.permute_self_edge)
    elif args.aug=="hyperedge":
        data_aug = permute_hyperedges(data_aug, args.aug_ratio)
    elif "adapt" in args.aug:
        data_aug = adapt(data_aug, args.aug_ratio, args.aug)
    else:
        raise ValueError(f'not supported augmentation')
    return data_aug

def sim(z1: torch.Tensor, z2: torch.Tensor):
        z1 = F.normalize(z1)
        z2 = F.normalize(z2)
        return torch.mm(z1, z2.t())

def semi_loss(z1: torch.Tensor, z2: torch.Tensor, T):
    f = lambda x: torch.exp(x / T)
    refl_sim = f(sim(z1, z1))
    between_sim = f(sim(z1, z2))
    return -torch.log(between_sim.diag() / (refl_sim.sum(1) + between_sim.sum(1) - refl_sim.diag()))

def whole_batched_semi_loss(z1: torch.Tensor, z2: torch.Tensor, batch_size: int, T):
    # Space complexity: O(BN) (semi_loss: O(N^2))
    device = z1.device
    num_nodes = z1.size(0)
    num_batches = (num_nodes - 1) // batch_size + 1
    f = lambda x: torch.exp(x / T)
    indices = torch.arange(0, num_nodes).to(device)
    losses = []
    for i in range(num_batches):
        mask = indices[i * batch_size:(i + 1) * batch_size]
        refl_sim = f(sim(z1[mask], z1))  # [B, N]
        between_sim = f(sim(z1[mask], z2))  # [B, N]

        losses.append(-torch.log(between_sim[:, i * batch_size:(i + 1) * batch_size].diag()
                                    / (refl_sim.sum(1) + between_sim.sum(1)
                                    - refl_sim[:, i * batch_size:(i + 1) * batch_size].diag())))

def batched_semi_loss(z1: torch.Tensor, z2: torch.Tensor, batch_size: int, T):
    # Space complexity: O(BN) (semi_loss: O(N^2))
    device = z1.device
    num_nodes = z1.size(0)
    num_batches = (num_nodes - 1) // batch_size + 1
    f = lambda x: torch.exp(x / T)
    indices = np.arange(0, num_nodes)
    np.random.shuffle(indices)
    i = 0
    mask = indices[i * batch_size:(i + 1) * batch_size]
    refl_sim = f(sim(z1[mask], z1))  # [B, N]
    between_sim = f(sim(z1[mask], z2))  # [B, N]
    loss = -torch.log(between_sim[:, i * batch_size:(i + 1) * batch_size].diag()
                                / (refl_sim.sum(1) + between_sim.sum(1)
                                - refl_sim[:, i * batch_size:(i + 1) * batch_size].diag()))

    return loss

def com_semi_loss(z1: torch.Tensor, z2: torch.Tensor, T, com_nodes1, com_nodes2):
    f = lambda x: torch.exp(x / T)
    refl_sim = f(sim(z1, z1))
    between_sim = f(sim(z1, z2))
    return -torch.log(between_sim[com_nodes1,com_nodes2] / (refl_sim.sum(1)[com_nodes1] + between_sim.sum(1)[com_nodes1] - refl_sim.diag()[com_nodes1]))

def contrastive_loss_node(x1, x2, args):
    T = args.t
    # if args.dname in ["yelp", "coauthor_dblp", "walmart-trips-100"]:
    #     batch_size=1024
    # else:
    #     batch_size = None
    batch_size = None
    if batch_size is None:
        l1 = semi_loss(x1, x2, T)
        l2 = semi_loss(x2, x1, T)
    else:
        l1 = batched_semi_loss(x1, x2, batch_size, T)
        l2 = batched_semi_loss(x2, x1, batch_size, T)
    ret = (l1 + l2) * 0.5
    ret = ret.mean()
    
    return ret

def semi_loss_JSD(z1: torch.Tensor, z2: torch.Tensor):
    # f = lambda x: torch.exp(x / T)

    refl_sim = sim(z1, z1)
    between_sim = sim(z1, z2)
    N = refl_sim.shape[0]
    pos_score = (np.log(2) - F.softplus(- between_sim.diag())).mean()
    neg_score_1 = (F.softplus(- refl_sim) + refl_sim - np.log(2))
    neg_score_1 = torch.sum(neg_score_1) - torch.sum(neg_score_1.diag())
    neg_score_2 = torch.sum(F.softplus(- between_sim) + between_sim - np.log(2))
    neg_score = (neg_score_1+neg_score_2)/(N*(2*N-1))
    return neg_score-pos_score


def contrastive_loss_node_JSD(x1, x2, args, com_nodes=None):
    T = args.t
    # if args.dname in ["yelp", "coauthor_dblp", "walmart-trips-100"]:
    #     batch_size=1024
    # else:
    #     batch_size = None
    batch_size = None
    if com_nodes is None:
        if batch_size is None:
            l1 = semi_loss_JSD(x1, x2)
            l2 = semi_loss_JSD(x2, x1)
        else:
            l1 = batched_semi_loss(x1, x2, batch_size, T)
            l2 = batched_semi_loss(x2, x1, batch_size, T)
    else:
        l1 = com_semi_loss(x1, x2, T, com_nodes[0], com_nodes[1])
        l2 = com_semi_loss(x2, x1, T, com_nodes[1], com_nodes[0])
    ret = (l1 + l2) * 0.5
    return ret

def semi_loss_TM(z1: torch.Tensor, z2: torch.Tensor):
    # f = lambda x: torch.exp(x / T)
    z1 = F.normalize(z1)
    z2 = F.normalize(z2)
    eps = 1.0
    N = z1.shape[0]
    pdist = nn.PairwiseDistance(p=2)
    pos_score = pdist(z1, z2).mean()
    neg_score_1 = torch.cdist(z1, z1, p=2)
    neg_score_2 = torch.cdist(z1, z2, p=2)
    neg_score_1 = torch.sum(neg_score_1) - torch.sum(neg_score_1.diag())
    neg_score_2 = torch.sum(neg_score_2)
    neg_score = (neg_score_1+neg_score_2)/(N*(2*N-1))
    return torch.max(pos_score-neg_score+eps, 0)[0]

def contrastive_loss_node_TM(x1, x2, args, com_nodes=None):
    T = args.t
    # if args.dname in ["yelp", "coauthor_dblp", "walmart-trips-100"]:
    #     batch_size=1024
    # else:
    #     batch_size = None
    batch_size = None
    if com_nodes is None:
        if batch_size is None:
            l1 = semi_loss_TM(x1, x2)
            l2 = semi_loss_TM(x2, x1)
        else:
            l1 = batched_semi_loss(x1, x2, batch_size, T)
            l2 = batched_semi_loss(x2, x1, batch_size, T)
    else:
        l1 = com_semi_loss(x1, x2, T, com_nodes[0], com_nodes[1])
        l2 = com_semi_loss(x2, x1, T, com_nodes[1], com_nodes[0])
    ret = (l1 + l2) * 0.5
    return ret

def sim_d(z1: torch.Tensor, z2: torch.Tensor):
        # z1 = F.normalize(z1)
        # z2 = F.normalize(z2)
        return torch.sqrt(torch.sum(torch.pow(z1-z2,2),1))

def calculate_distance(z1: torch.Tensor, z2: torch.Tensor):
    num_nodes = z1.size(0)
    refl_sim = 0
    for i in range(num_nodes):
        refl_sim += (torch.sum(sim_d(z1[i:i+1], z1)) - torch.squeeze(sim_d(z1[i:i+1], z1[i:i+1])))/(num_nodes-1)
    refl_sim = refl_sim/(num_nodes)
    between_sim = torch.sum(sim_d(z1, z2))/num_nodes
    print(refl_sim, between_sim)

def create_hypersubgraph(data, args):
    
    sub_size = args.sub_size
    node_size = int(data.n_x[0].item())
    hyperedge_size = int(data.num_hyperedges[0].item())
    sample_nodes = np.random.permutation(node_size)[:sub_size]
    sample_nodes = list(np.sort(sample_nodes))
    edge_index = data.edge_index
    device = edge_index.device
    sub_nodes, sub_edge_index, mapping, _ = k_hop_subgraph(sample_nodes, 1, edge_index, relabel_nodes=False, flow='target_to_source')
    sub_nodes, sorted_idx = torch.sort(sub_nodes)
    # relabel
    node_idx = torch.zeros(2*node_size+hyperedge_size, dtype=torch.long, device=device)
    node_idx[sub_nodes] = torch.arange(sub_nodes.size(0), device=device)
    sub_edge_index = node_idx[sub_edge_index]
    x = data.x[sample_nodes]
    data_sub = Data(x=x, edge_index=sub_edge_index)
    data_sub.n_x = torch.tensor([sub_size])
    data_sub.num_hyperedges = torch.tensor([sub_nodes.size(0) - 2*sub_size])
    data_sub.norm = 0
    data_sub.totedges = torch.tensor(sub_nodes.size(0) - sub_size)
    data_sub.num_ori_edge = sub_edge_index.shape[1] - sub_size
    data_sub.sub_nodes = sub_nodes
    data_sub.y = data.y[sample_nodes]
    return data_sub

def expand_edge_index(data, edge_th=0):
    '''
    args:
        num_nodes: regular nodes. i.e. x.shape[0]
        num_edges: number of hyperedges. not the star expansion edges.

    this function will expand each n2he relations, [[n_1, n_2, n_3], 
                                                    [e_7, e_7, e_7]]
    to :
        [[n_1,   n_1,   n_2,   n_2,   n_3,   n_3],
         [e_7_2, e_7_3, e_7_1, e_7_3, e_7_1, e_7_2]]

    and each he2n relations:   [[e_7, e_7, e_7],
                                [n_1, n_2, n_3]]
    to :
        [[e_7_1, e_7_2, e_7_3],
         [n_1,   n_2,   n_3]]

    and repeated for every hyperedge.
    '''
    edge_index = data.hyperedge_index
    num_nodes = data.num_nodes
    num_edges = data.num_edges

    expanded_n2he_index = []
#     n2he_with_same_heid = []

#     expanded_he2n_index = []
#     he2n_with_same_heid = []

    # start edge_id from the largest node_id + 1.
    cur_he_id = num_nodes
    # keep an mapping of new_edge_id to original edge_id for edge_size query.
    new_edge_id_2_original_edge_id = {}

    # do the expansion for all annotated he_id in the original edge_index
#     ipdb.set_trace()
    for he_idx in range(num_nodes, num_edges + num_nodes):
        # find all nodes within the same hyperedge.
        selected_he = edge_index[:, edge_index[1] == he_idx]
        size_of_he = selected_he.shape[1]

#         Trim a hyperedge if its size>edge_th
        if edge_th > 0:
            if size_of_he > edge_th:
                continue

        if size_of_he == 1:
            # there is only one node in this hyperedge -> self-loop node. add to graph.
            #             n2he_with_same_heid.append(selected_he)

            new_n2he = selected_he.clone()
            new_n2he[1] = cur_he_id
            expanded_n2he_index.append(new_n2he)

            # ====
#             new_he2n_same_heid = torch.flip(selected_he, dims = [0])
#             he2n_with_same_heid.append(new_he2n_same_heid)

#             new_he2n = torch.flip(selected_he, dims = [0])
#             new_he2n[0] = cur_he_id
#             expanded_he2n_index.append(new_he2n)

            cur_he_id += 1
            continue

        # -------------------------------
#         # new_n2he_same_heid uses same he id for all nodes.
#         new_n2he_same_heid = selected_he.repeat_interleave(size_of_he - 1, dim = 1)
#         n2he_with_same_heid.append(new_n2he_same_heid)

        # for new_n2he mapping. connect the nodes to all repeated he first.
        # then remove those connection that corresponding to the node itself.
        new_n2he = selected_he.repeat_interleave(size_of_he, dim=1)

        # new_edge_ids start from the he_id from previous iteration (cur_he_id).
        new_edge_ids = torch.LongTensor(
            np.arange(cur_he_id, cur_he_id + size_of_he)).repeat(size_of_he)
        new_n2he[1] = new_edge_ids

        # build a mapping between node and it's corresponding edge.
        # e.g. {n_1: e_7_1, n_2: e_7_2}
        tmp_node_id_2_he_id_dict = {}
        for idx in range(size_of_he):
            new_edge_id_2_original_edge_id[cur_he_id] = he_idx
            cur_node_id = selected_he[0][idx].item()
            tmp_node_id_2_he_id_dict[cur_node_id] = cur_he_id
            cur_he_id += 1

        # create n2he by deleting the self-product edge.
        new_he_select_mask = torch.BoolTensor([True] * new_n2he.shape[1])
        for col_idx in range(new_n2he.shape[1]):
            tmp_node_id, tmp_edge_id = new_n2he[0, col_idx].item(
            ), new_n2he[1, col_idx].item()
            if tmp_node_id_2_he_id_dict[tmp_node_id] == tmp_edge_id:
                new_he_select_mask[col_idx] = False
        new_n2he = new_n2he[:, new_he_select_mask]
        expanded_n2he_index.append(new_n2he)


#         # ---------------------------
#         # create he2n from mapping.
#         new_he2n = np.array([[he_id, node_id] for node_id, he_id in tmp_node_id_2_he_id_dict.items()])
#         new_he2n = torch.from_numpy(new_he2n.T).to(device = edge_index.device)
#         expanded_he2n_index.append(new_he2n)

#         # create he2n with same heid as input edge_index.
#         new_he2n_same_heid = torch.zeros_like(new_he2n, device = edge_index.device)
#         new_he2n_same_heid[1] = new_he2n[1]
#         new_he2n_same_heid[0] = torch.ones_like(new_he2n[0]) * he_idx
#         he2n_with_same_heid.append(new_he2n_same_heid)

    new_edge_index = torch.cat(expanded_n2he_index, dim=1)
#     new_he2n_index = torch.cat(expanded_he2n_index, dim = 1)
#     new_edge_index = torch.cat([new_n2he_index, new_he2n_index], dim = 1)
    # sort the new_edge_index by first row. (node_ids)
    new_order = new_edge_index[0].argsort()
    data.hyperedge_index = new_edge_index[:, new_order]

    return data

def Add_Self_Loops(data):
    # update so we dont jump on some indices
    # Assume edge_index = [V;E]. If not, use ExtractV2E()
    edge_index = data.hyperedge_index
    data.num_ori_edge = edge_index.shape[1]
    # expanded to list
    num_nodes = data.num_nodes
    # num_hyperedges = data.num_hyperedges[0]
    num_hyperedges = edge_index[1].max() + 1 - num_nodes

    if not ((data.num_nodes + data.num_edges - 1) == data.hyperedge_index[1].max().item()):
        print('num_hyperedges seems not match! 2')
    #     return
    # dict
    skip_node_lst = []
    hyperedge_appear_fre = Counter(edge_index[1].detach().cpu().numpy())
    # for edge in hyperedge_appear_fre:
    #     if hyperedge_appear_fre[edge] == 1:
    #         # ensure V
    #         skip_node = edge_index[0][torch.where(
    #             edge_index[1] == edge)[0].item()]
    #         skip_node_lst.append(skip_node.item())
    
    new_edge_idx = edge_index[1].max() + 1
    new_edges = torch.zeros(
        (2, num_nodes - len(skip_node_lst)), dtype=edge_index.dtype)
    tmp_count = 0
    for i in range(num_nodes):
        if i not in skip_node_lst:
            new_edges[0][tmp_count] = i
            new_edges[1][tmp_count] = new_edge_idx
            new_edge_idx += 1
            tmp_count += 1
    new_edges=new_edges.to(edge_index.device)
    data.totedges = num_hyperedges + num_nodes - len(skip_node_lst)
    edge_index = torch.cat((edge_index, new_edges), dim=1)
    # Sort along w.r.t. nodes

    # _, sorted_idx = torch.sort(edge_index[0])
    # data.edge_index = edge_index[:, sorted_idx].type(torch.LongTensor)
    data.hyperedge_index = edge_index.type(torch.LongTensor).to(edge_index.device)
    return data


def norm_contruction(data, option='all_one', TYPE='V2E'):
    if TYPE == 'V2E':
        if option == 'all_one':
            data.norm = torch.ones_like(data.hyperedge_index[0])

        elif option == 'deg_half_sym':
            edge_weight = torch.ones_like(data.hyperedge_index[0])
            cidx = data.hyperedge_index[1].min()
            Vdeg = scatter_add(edge_weight, data.hyperedge_index[0], dim=0)
            HEdeg = scatter_add(edge_weight, data.hyperedge_index[1]-cidx, dim=0)
            V_norm = Vdeg**(-1/2)
            E_norm = HEdeg**(-1/2)
            data.norm = V_norm[data.hyperedge_index[0]] * \
                E_norm[data.hyperedge_index[1]-cidx]

    elif TYPE == 'V2V':
        data.hyperedge_index, data.norm = gcn_norm(
            data.hyperedge_index, data.norm, add_self_loops=True)
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', default='cora_cite')
    # Table 5(커뮤니티 탐지)용 — 경로를 주면 첫 seed 학습이 끝난 뒤 노드 표현을 저장하고 멈춘다.
    parser.add_argument('--save-emb', dest='save_emb', type=str, default=None)
    # method in ['SetGNN','CEGCN','CEGAT','HyperGCN','HGNN','HCHA']
    parser.add_argument('--method', default='AllDeepSets')
    parser.add_argument('--epochs', default=200, type=int)
    # Number of runs for each split (test fix, only shuffle train/val)
    parser.add_argument('--num_seeds', default=20, type=int)
    parser.add_argument('--seed_start', default=0, type=int,
                        help='first predefined split to run; permits safe resume without repeating finished splits')
    parser.add_argument('--cuda', default=1, choices=[-1, 0, 1, 2, 3], type=int)
    parser.add_argument('--dropout', default=0.5, type=float)
    parser.add_argument('--lr', default=0.001, type=float)
    parser.add_argument('--weight_decay', default=1e-6, type=float)
    # How many layers of full NLConvs
    parser.add_argument('--All_num_layers', default=2, type=int)
    parser.add_argument('--MLP_num_layers', default=2,
                        type=int)  # How many layers of encoder
    parser.add_argument('--MLP_hidden', default=128,
                        type=int)  # Encoder hidden units
    parser.add_argument('--Classifier_num_layers', default=2,
                        type=int)  # How many layers of decoder
    parser.add_argument('--Classifier_hidden', default=128,
                        type=int)  # Decoder hidden units
    parser.add_argument('--display_step', type=int, default=-1)
    parser.add_argument('--aggregate', default='add', choices=['sum', 'mean'])
    # ['all_one','deg_half_sym']
    parser.add_argument('--normtype', default='all_one')
    parser.add_argument('--add_self_loop', action='store_false')
    # NormLayer for MLP. ['bn','ln','None']
    parser.add_argument('--normalization', default='ln')
    parser.add_argument('--deepset_input_norm', default = True)
    parser.add_argument('--GPR', action='store_false')  # skip all but last dec
    # skip all but last dec
    parser.add_argument('--LearnMask', action='store_false')
    parser.add_argument('--num_features', default=0, type=int)  # Placeholder
    parser.add_argument('--num_classes', default=0, type=int)  # Placeholder
    # Choose std for synthetic feature noise
    parser.add_argument('--feature_noise', default='1', type=str)
    # whether the he contain self node or not
    parser.add_argument('--exclude_self', action='store_true')
    parser.add_argument('--PMA', action='store_true')
    #     Args for HyperGCN
    #     Args for Attentions: GAT and SetGNN
    parser.add_argument('--heads', default=2, type=int)  # Placeholder
    parser.add_argument('--output_heads', default=2, type=int)  # Placeholder
    #     Args for HNHN
    #     Args for contrastive learning
    parser.add_argument('--t', type=float, default = 0.3)
    parser.add_argument('--p_lr', type=float, default = 0)
    parser.add_argument('--p_epochs', type=int, default = 300)
    parser.add_argument('--aug_ratio', type=float, default = 0.3)
    parser.add_argument('--p_hidden', type=int, default = -1)
    parser.add_argument('--p_layer', type=int, default = -1)
    parser.add_argument('--aug', type=str, default = "edge", help='mask|edge|hyperedge|adapt|adapt_feat|adapt_edge')
    parser.add_argument('--negative_sampling_method', choices=['gpu', 'sparse', 'dense'], default='gpu',
                        help='negative sampler for VHG-AE reconstruction; gpu avoids NumPy/CPU synchronization')
    parser.add_argument('--add_e', action='store_true', default = False)
    parser.add_argument('--permute_self_edge', action='store_true', default = False)
    parser.add_argument('--linear', action='store_true', default = False)
    parser.add_argument('--sub_size', type=int, default = 16384)
    parser.add_argument('--m_l', type=float, default = 0)
    parser.add_argument('--a_l', type=float, default = 0.1)
    parser.add_argument('--seed', type=int, default = 123)
    parser.add_argument('--g_lr', type=float, default = 1e-3)
    parser.add_argument('--g_l', type=float, default = 1)
    parser.add_argument('--step', type=int, default = 1)
    parser.add_argument('--hard', type=int, default = 1)
    parser.add_argument('--deg', type=int, default = 0)
    parser.add_argument('--mode', type=str, default = "InfoNCE")
    parser.add_argument('--task', type=str, default = "edge")
    parser.set_defaults(PMA=False)  # True: Use PMA. False: Use Deepsets.
    parser.set_defaults(add_self_loop=True)
    parser.set_defaults(exclude_self=False)
    parser.set_defaults(GPR=False)
    parser.set_defaults(LearnMask=False)
    
    #     Use the line below for .py file
    args = parser.parse_args()
    device=torch.device('cuda:'+str(args.cuda)
                              if torch.cuda.is_available() else 'cpu')
    args.device=device
    data = DatasetLoader().load(args.data).to(device)
    args.method="HyperGCL"
    args.num_features=data.features.shape[1]
    args.num_classes=data.labels.max().item()+1
    node_splits = data.data_splits
    edge_splits = data.edge_splits
    available_splits = len(node_splits) if args.task == 'node' else len(edge_splits)
    if args.seed_start < 0 or args.seed_start + args.num_seeds > available_splits:
        raise ValueError(
            f'Invalid split window [{args.seed_start}, {args.seed_start + args.num_seeds}); '
            f'{available_splits} predefined splits are available.')
    fix_seed(0)
    accs = []
    logger = Logger(args.num_seeds, args)
    print(data.name)
    print(args)
    data = Add_Self_Loops(data)
    data = norm_contruction(data, option=args.normtype)
    for local_seed, seed in enumerate(tqdm(range(args.seed_start, args.seed_start + args.num_seeds))):
        if args.task=="node": #node
            eval_func = eval_acc_node
            train_idx,valid_idx,test_idx=node_splits[seed]
            

            model = SetGNN_n(args).to(device)
            optimizer = torch.optim.Adam(model.parameters(),
                                    lr=args.lr,
                                    weight_decay=args.weight_decay)
            criterion = nn.NLLLoss()
            contrastive_loss = contrastive_loss_node
            encoder, decoder = vhgae_encoder(args).to(device), vhgae_decoder(args).to(device)
            encoder.reset_parameters()
            view_generator = vhgae(encoder, decoder, args).to(device)
            optimizer_g = torch.optim.Adam(view_generator.parameters(), lr=args.g_lr, weight_decay=0)
            best_val = float('-inf')
            import time
            for epoch in tqdm(range(args.epochs)):
                
                if epoch==1:
                    start=time.time()
                if epoch==10:
                    end=time.time()

                data_sub = copy.deepcopy(data)
                view_generator.train()
                model.train()
                data_aug1 = data_sub
                # generator update
                for sth in range(args.step):
                    optimizer_g.zero_grad()
                    out = model.forward_cl(data_aug1)
                    data_2 = copy.deepcopy(data_sub).to(device)
                    data_2.edge_index_neg = negative_sampling(
                        data_2.hyperedge_index,
                        num_nodes=[int(data_2.num_nodes), int(data_2.totedges.item())],
                        method=args.negative_sampling_method)
                    loss_vhgae, data_aug2, aug_weight, drop = view_generator.generate(data_2)
                    aug_weight_attn = aug_weight
                    out_aug = model.forward_cl(copy.deepcopy(data_sub).to(device), aug_weight_attn)
                    loss_cl = contrastive_loss(out, out_aug, args)
                    # loss_cl = contrastive_loss_node(out, out_aug, args)
                    if epoch==0:
                        g_l=args.g_l
                    loss_generator = loss_vhgae-g_l*loss_cl 
                    loss_generator.backward()
                    optimizer_g.step()
                model.train()
                optimizer.zero_grad()
                
                data_sub = data_sub.to(device)
                data_aug1 = aug(data_sub, args).to(device)
                # data_aug1 = data_sub
                if args.m_l:
                    out = model.forward_cl(data_aug1)
                    data_aug2 = aug(data_sub, args).to(device)
                    out_aug = model.forward_cl(data_aug2)
                    loss_cl_nat = contrastive_loss_node(out, out_aug, args)
                model.train()
                view_generator.eval()
                out = model.forward_cl(copy.deepcopy(data_aug1))
                data_2 = copy.deepcopy(data_sub).to(device)
                with torch.no_grad():
                    _, data_aug2, aug_weight, drop = view_generator.generate_only(data_2)
                aug_weight_attn = aug_weight
                out_aug = model.forward_cl(copy.deepcopy(data_sub).to(device), aug_weight_attn)
                loss_cl = contrastive_loss(out, out_aug, args)
                if args.linear:
                    out = model.forward_finetune(data)
                else:
                    out = model(data)
                out = F.log_softmax(out, dim=1)
                loss = criterion(out[train_idx], data.labels[train_idx])
                loss += args.a_l*loss_cl
                # #         Training part
                if args.m_l:
                    loss += args.m_l*loss_cl_nat
                loss.backward()
                optimizer.step()

                result = evaluate_n(model, data, node_splits[seed], eval_func)
                logger.add_result(local_seed, result[:3])
            
            if getattr(args, "save_emb", None):
                import pickle as _pickle, os as _os
                model.eval()
                with torch.no_grad():
                    _z = model.forward_cl(copy.deepcopy(data).to(device))
                _os.makedirs(_os.path.dirname(args.save_emb), exist_ok=True)
                with open(args.save_emb, "wb") as _f:
                    _pickle.dump(_z[:data.features.shape[0]].detach().cpu().numpy(), _f)
                print("saved embeddings:", args.save_emb, _z.shape)
                raise SystemExit(0)


        else:
            data.hyperedge_index = edge_splits[seed][3].to(args.device)
            data.num_edges = data.hyperedge_index[1].max().item()+1
            data = Add_Self_Loops(data)
            data = norm_contruction(data, option=args.normtype)
            train_data,valid_data,test_data=edge_splits[seed][0],edge_splits[seed][1],edge_splits[seed][2]

            criterion = nn.BCELoss()
            eval_func = eval_acc_edge

            model = SetGNN_e(args).to(device)
            optimizer = torch.optim.Adam(model.parameters(),
                                    lr=args.lr,
                                    weight_decay=args.weight_decay)
            
            contrastive_loss = contrastive_loss_node
            model.reset_parameters()
            encoder, decoder = vhgae_encoder(args).to(device), vhgae_decoder(args).to(device)
            encoder.reset_parameters()
            view_generator = vhgae(encoder, decoder, args).to(device)
            optimizer_g = torch.optim.Adam(view_generator.parameters(), lr=args.g_lr, weight_decay=0)
            best_val = float('-inf')

            train_v=train_data[0]
            train_e=torch.tensor(train_data[1]).to(args.device)
            train_label = train_data[2].to(args.device)


            for epoch in tqdm(range(args.epochs)):
                data_sub = copy.deepcopy(data)
                view_generator.train()
                model.train()
                data_aug1 = data_sub
                # generator update
                for sth in range(args.step):
                    optimizer_g.zero_grad()
                    out = model.forward_cl(data_aug1)
                    data_2 = copy.deepcopy(data_sub).to(device)
                    data_2.edge_index_neg = negative_sampling(
                        data_2.hyperedge_index,
                        num_nodes=[int(data_2.num_nodes), int(data_2.totedges.item())],
                        method=args.negative_sampling_method)
                    loss_vhgae, data_aug2, aug_weight, drop = view_generator.generate(data_2)
                    aug_weight_attn = aug_weight
                    out_aug = model.forward_cl(copy.deepcopy(data_sub).to(device), aug_weight_attn)
                    loss_cl = contrastive_loss(out, out_aug, args)
                    # loss_cl = contrastive_loss_node(out, out_aug, args)
                    if epoch==0:
                        g_l=args.g_l
                    loss_generator = loss_vhgae-g_l*loss_cl 
                    loss_generator.backward()
                    optimizer_g.step()
                model.train()
                optimizer.zero_grad()
                cidx = data_sub.hyperedge_index[1].min()
                data_sub.hyperedge_index[1] -= cidx
                data_sub = data_sub.to(device)
                data_aug1 = aug(data_sub, args).to(device)
                # data_aug1 = data_sub
                if args.m_l:
                    out = model.forward_cl(data_aug1)
                    data_aug2 = aug(data_sub, args).to(device)
                    out_aug = model.forward_cl(data_aug2)
                    loss_cl_nat = contrastive_loss_node(out, out_aug, args)
                model.train()
                view_generator.eval()
                out = model.forward_cl(copy.deepcopy(data_aug1))
                data_2 = copy.deepcopy(data_sub).to(device)
                with torch.no_grad():
                    _, data_aug2, aug_weight, drop = view_generator.generate_only(data_2)
                aug_weight_attn = aug_weight
                out_aug = model.forward_cl(copy.deepcopy(data_sub).to(device), aug_weight_attn)
                loss_cl = contrastive_loss(out, out_aug, args)
                if args.linear:
                    out = model.forward_finetune(data)
                else:
                    out = model(data,train_v,train_e)
                if out.size(-1) != 1:
                    assert False
                out = torch.sigmoid(out).squeeze(-1)
                loss = criterion(out, train_label)
                loss += args.a_l*loss_cl
                # #         Training part
                if args.m_l:
                    loss += args.m_l*loss_cl_nat
                loss.backward()
                optimizer.step()

                result = evaluate_e(model, train_data, valid_data, test_data, eval_func)
                logger.add_result(local_seed, result[:3])
        

    best_val, best_test = logger.print_statistics()
    path=f'./results/result_{args.data}_{args.method}_{args.task}.txt'
    with open(path, 'a+') as write_obj:
        write_obj.write(
            f'splits[{args.seed_start}:{args.seed_start + args.num_seeds}] '
            f'lr{args.lr}glr{args.g_lr}a_l{args.a_l}=> '
            f'{best_test},{best_test.mean():.1f} ± {best_test.std():.1f}\n')
    # ``start``/``end`` are only populated by the node-classification path.
    # Edge prediction has already written its metric above, so skip the
    # optional timing write instead of exiting with NameError after success.
    if args.task == 'node':
        path=f'./time/time.txt'
        with open(path, 'a+') as write_obj:
            write_obj.write(f'{args.data}_{args.method}:{end-start} acc:({best_test.mean()})\n')

    
    path=f'./result_small.txt'
    with open(path, 'a+') as write_obj:
        write_obj.write(f'{args.data},{args.method},{best_test.mean():.1f} ± {best_test.std():.1f}\n')
