import logging
import random
import torch
import dgl
from sklearn.preprocessing import StandardScaler
import itertools



def load_small_dataset(data,args):

   
    # graph = dataset[0]
    # graph = graph.remove_self_loop()
    # graph = graph.add_self_loop()
    # num_features = graph.ndata["feat"].shape[1]
    # num_classes = dataset.num_classes
    data=clique_expansion(data)

    num_nodes = data.hyperedge_index[0].max()+1
    num_edges = data.hyperedge_index[1].max()+1
    num_features = data.features.size(1)
    num_classes = torch.unique(data.labels).size(0)

    src = data.src.to(args.device)
    dst = data.dst.to(args.device)



    # 4. 그래프 생성
    graph = dgl.graph((src, dst), num_nodes=num_nodes)
    graph = graph.remove_self_loop().add_self_loop()
    # 5. feature, label 부여
    graph.ndata['feat'] = data.features
    graph.ndata['label'] = data.labels

    
    return graph, (num_features, num_classes)

def preprocess(graph):
    # make bidirected
    feat = graph.ndata["feat"]
    src, dst = graph.all_edges()
    # graph.add_edges(dst, src)
    graph = dgl.to_bidirected(graph)

    # add self-loop
    graph = graph.remove_self_loop().add_self_loop()
    # graph.create_formats_()
    return graph


def scale_feats(x):
    logging.info("### scaling features ###")
    scaler = StandardScaler()
    feats = x.numpy()
    scaler.fit(feats)
    feats = torch.from_numpy(scaler.transform(feats)).float()
    return feats


def clique_expansion(data):
    """
    Args:
        node_edge_tensor: LongTensor of shape (2, N), where
                          node_edge_tensor[0] = node indices,
                          node_edge_tensor[1] = corresponding hyperedge indices.
    Returns:
        src: LongTensor of shape (E,)
        target: LongTensor of shape (E,)
    """
    node_ids, edge_ids = data.hyperedge_index
    unique_edges = torch.unique(edge_ids)

    src_list = []
    target_list = []

    for e in unique_edges:
        nodes_in_edge = node_ids[edge_ids == e]
        if len(nodes_in_edge) > 1:
            for u, v in itertools.combinations(nodes_in_edge.tolist(), 2):
                src_list.extend([u, v])
                target_list.extend([v, u])  # add both directions

    data.src = torch.tensor(src_list, dtype=torch.long)
    data.dst = torch.tensor(target_list, dtype=torch.long)

    return data