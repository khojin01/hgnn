import torch
import numpy as np
import math
def clique_expansion(data):
    edge_index=data.hyperedge_index
    device = edge_index.device
    nodes, hyperedges = edge_index

    # 고유한 hyperedge id 찾기
    unique_hyperedges = torch.unique(hyperedges)
    num_hyperedges = unique_hyperedges.size(0)

    # hyperedge별 몇 개씩 있는지 count
    counts = torch.bincount(hyperedges, minlength=hyperedges.max().item() + 1)

    # hyperedge별로 노드 모으기
    sorted_hyperedges, perm = hyperedges.sort()
    sorted_nodes = nodes[perm]

    # hyperedge별로 split
    node_groups = torch.split(sorted_nodes, counts[counts != 0].tolist())

    # clique 확장
    src_list = []
    tgt_list = []
    hyperedge_list = []

    valid_hyperedges = unique_hyperedges[counts[unique_hyperedges] > 1]

    for group, he_id in zip(node_groups, valid_hyperedges):
        if group.numel() < 2:
            continue
        comb = torch.combinations(group, r=2)  # 모든 (i,j) 쌍
        src_list.append(comb[:, 0])
        tgt_list.append(comb[:, 1])
        hyperedge_list.append(he_id.repeat(comb.size(0)))

        # 반대 방향도 추가 (undirected)
        src_list.append(comb[:, 1])
        tgt_list.append(comb[:, 0])
        hyperedge_list.append(he_id.repeat(comb.size(0)))

    src_nodes = torch.cat(src_list)
    tgt_nodes = torch.cat(tgt_list)
    hyperedge_ids = torch.cat(hyperedge_list)

    data.edge_index = torch.stack([src_nodes, tgt_nodes, hyperedge_ids], dim=0)

    return data

def augment_edge(data, pe):
    expanded_edge_index=data.edge_index
    device = expanded_edge_index.device
    src_nodes, tgt_nodes, hyperedge_ids = expanded_edge_index

    unique_hyperedges = torch.unique(hyperedge_ids)
    num_hyperedges = unique_hyperedges.size(0)

    num_keep = math.ceil(num_hyperedges * (1 - pe))

    perm = torch.randperm(num_hyperedges, device=device)[:num_keep]
    selected_hyperedges = unique_hyperedges[perm]

    # 선택된 hyperedge에 해당하는 edge만 남기기
    mask = (hyperedge_ids.unsqueeze(1) == selected_hyperedges.unsqueeze(0)).any(dim=1)

    new_src_nodes = src_nodes[mask]
    new_tgt_nodes = tgt_nodes[mask]
    new_hyperedge_ids = hyperedge_ids[mask]

    subsampled_edge_index = torch.stack([new_src_nodes, new_tgt_nodes, new_hyperedge_ids], dim=0)

    values = torch.ones(new_src_nodes.size(0), device=device)

    adj = torch.sparse_coo_tensor(
        indices=subsampled_edge_index[:2],
        values=values,
        size=(data.num_nodes, data.num_nodes),
        device=device
    )

    return adj
    
def augment_feature(X, p, device) :
    
    return X * (((torch.rand(X.shape) > p).float()).to(device))