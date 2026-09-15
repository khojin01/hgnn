import sys
import os
import torch
import random
import numpy as np
from texttable import Texttable
import torch_geometric.transforms as T
from torch_geometric.data import Data
from torch_geometric.utils import index_to_mask
import itertools
    
def get_dataset(data,transform=None) -> Data:
    node_ids, edge_ids = data.hyperedge_index
    unique_edges = torch.unique(edge_ids)

    src_list = []
    target_list = []

    for e in unique_edges:
        nodes_in_edge = node_ids[edge_ids == e]
        if len(nodes_in_edge) > 1:
            for u, v in itertools.combinations(nodes_in_edge.tolist(), 2):
                src_list.extend([u, v])
                target_list.extend([v, u])
    edge_index=torch.tensor([src_list,target_list])

    data = Data(x=data.features,edge_index=edge_index,y=data.labels)
    data = transform(data)
    return data
    
def tab_printer(args):
    """Function to print the logs in a nice tabular format.

    Note
    ----
    Package `Texttable` is required.
    Run `pip install Texttable` if was not installed.

    Parameters
    ----------
    args: Parameters used for the model.
    """
    args = vars(args)
    keys = sorted(args.keys())
    t = Texttable()
    t.add_rows([["Parameter", "Value"]] + [[k, str(args[k])] for k in keys if not k.startswith('__')])
    return t.draw()
