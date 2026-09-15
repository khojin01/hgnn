import torch

from torch_scatter import scatter_add
from torch_scatter import scatter
import numpy as np

def generate_norm_HNHN(data, args):
    """
    :param H: hypergraph incidence matrix H
    :param variable_weight: whether the weight of hyperedge is variable
    :return: G
    """
#     H = data.incident_mat
    alpha = args.HNHN_alpha
    beta = args.HNHN_beta

    weight = torch.ones(data.num_edges).to(args.device)
    Dn = scatter_add(weight[data.hyperedge_index[1]], data.hyperedge_index[0], dim=0, dim_size=data.num_nodes)
    De = scatter_add(torch.ones(data.hyperedge_index.shape[1]).to(args.device), data.hyperedge_index[1], dim=0, dim_size=data.num_edges)

    DV=Dn.cpu().detach().numpy()
    DE=De.cpu().detach().numpy()
    H = torch.sparse_coo_tensor(data.hyperedge_index, \
    data.hyperedge_index.new_ones((data.hyperedge_index.shape[1],)), (data.num_nodes, data.num_edges)).to_dense().cpu().detach().numpy()

    D_e_alpha = DE ** alpha
    D_v_alpha = np.zeros(data.num_nodes)

    for i in range(data.num_nodes):
        # which edges this node is in
        he_list = np.where(H[i] == 1)[0]
        D_v_alpha[i] = np.sum(DE[he_list] ** alpha)

    D_v_beta = DV ** beta
    D_e_beta = np.zeros(data.num_edges)
    for i in range(data.num_edges):
        # which nodes are in this hyperedge
        node_list = np.where(H[:, i] == 1)[0]
        D_e_beta[i] = np.sum(DV[node_list] ** beta)

    D_v_alpha_inv = 1.0 / D_v_alpha
    D_v_alpha_inv[D_v_alpha_inv == float("inf")] = 0

    D_e_beta_inv = 1.0 / D_e_beta
    D_e_beta_inv[D_e_beta_inv == float("inf")] = 0

    data.D_e_alpha = torch.from_numpy(D_e_alpha).float().to(args.device)
    data.D_v_alpha_inv = torch.from_numpy(D_v_alpha_inv).float().to(args.device)
    data.D_v_beta = torch.from_numpy(D_v_beta).float().to(args.device)
    data.D_e_beta_inv = torch.from_numpy(D_e_beta_inv).float().to(args.device)

    return data

