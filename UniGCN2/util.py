
import torch
import torch_sparse
from torch_scatter import scatter

import numpy as np
import scipy.sparse as sp

def generate_norm_UniGCN2(data,args):
    H = torch.sparse_coo_tensor(data.hyperedge_index, \
    data.hyperedge_index.new_ones((data.hyperedge_index.shape[1],)), (data.num_nodes, data.num_edges)).to_dense().cpu().detach().numpy()
    data.hyperedge_index=sp.csr_matrix(H)
    (row, col), value = torch_sparse.from_scipy(data.hyperedge_index)
    V, E = row.to(args.device), col.to(args.device)
    degV=data.Dn.reshape(-1,1).to(args.device)
    degE = scatter(degV[V], E, dim=0, reduce='mean')
    degV = degV.pow(-0.5)
    degV[torch.isinf(degV)] = 1
    args.UniGNN_degV = degV.to(args.device)
    args.UniGNN_degE = degE.to(args.device)

    data.V=V
    data.E=E
    return data,args