import math
import torch
import numpy as np
import torch.nn as nn
import torch.nn.functional as F

from torch import Tensor
from torch.nn.modules.module import Module
from torch.nn import Linear
from torch.nn import Parameter
from torch_geometric.nn.conv import MessagePassing
from torch_geometric.utils import softmax
from torch_scatter import scatter_add
from torch_scatter import scatter
from typing import Optional
from torch_geometric.typing import Adj, Size, OptTensor
class HNHNConv(MessagePassing):
    def __init__(self, in_channels, hidden_channels, out_channels, heads=1, nonlinear_inbetween=True,
                 concat=True, bias=True, **kwargs):
        kwargs.setdefault('aggr', 'add')
        super(HNHNConv, self).__init__(node_dim=0, **kwargs)

        self.in_channels = in_channels
        self.hidden_channels = hidden_channels
        self.out_channels = out_channels
        self.nonlinear_inbetween = nonlinear_inbetween

        # preserve variable heads for later use (attention)
        self.heads = heads
        self.concat = True
        # self.weight = Parameter(torch.Tensor(in_channels, out_channels))
        self.weight_v2e = Linear(in_channels, hidden_channels)
        self.weight_e2v = Linear(hidden_channels, out_channels)

        self.reset_parameters()

    def reset_parameters(self):
        self.weight_v2e.reset_parameters()
        self.weight_e2v.reset_parameters()
        # glorot(self.weight_v2e)
        # glorot(self.weight_e2v)
        # zeros(self.bias)

    def forward(self, x, data):
        r"""
        Args:
            x (Tensor): Node feature matrix :math:`\mathbf{X}`
            hyperedge_index (LongTensor): The hyperedge indices, *i.e.*
                the sparse incidence matrix
                :math:`\mathbf{H} \in {\{ 0, 1 \}}^{N \times M}` mapping from
                nodes to edges.
            hyperedge_weight (Tensor, optional): Sparse hyperedge weights
                :math:`\mathbf{W} \in \mathbb{R}^M`. (default: :obj:`None`)
        """
        hyperedge_index = data.hyperedge_index
        hyperedge_weight = None
        num_nodes, num_edges = x.size(0), 0
        if hyperedge_index.numel() > 0:
            num_edges = int(hyperedge_index[1].max()) + 1

        if hyperedge_weight is None:
            hyperedge_weight = x.new_ones(num_edges)

        x = self.weight_v2e(x)

#         ipdb.set_trace()
#         x = torch.matmul(torch.diag(data.D_v_beta), x)
        x = data.D_v_beta.unsqueeze(-1) * x

        self.flow = 'source_to_target'
        out = self.propagate(hyperedge_index, x=x, norm=data.D_e_beta_inv,
                             size=(num_nodes, num_edges))
        
        if self.nonlinear_inbetween:
            out = F.relu(out)
        
        # sanity check
        out = torch.squeeze(out, dim=1)
        
        out = self.weight_e2v(out)
        
#         out = torch.matmul(torch.diag(data.D_e_alpha), out)
        out = data.D_e_alpha.unsqueeze(-1) * out

        # Use an explicitly reversed incidence for the hyperedge-to-node
        # pass.  This is equivalent to the legacy ``target_to_source`` path,
        # while remaining compatible with the installed PyG MessagePassing
        # size validation.
        self.flow = 'source_to_target'
        out = self.propagate(hyperedge_index.flip(0), x=out, norm=data.D_v_alpha_inv,
                             size=(num_edges, num_nodes))
        
        return out

    def message(self, x_j, norm_i):

        out = norm_i.view(-1, 1) * x_j

        return out

    def __repr__(self):
        return "{}({}, {}, {})".format(self.__class__.__name__, self.in_channels,
                                   self.hidden_channels, self.out_channels)

class HNHN_n(nn.Module):
    """
    """

    def __init__(self, args):
        super(HNHN_n, self).__init__()

        self.num_layers = 2
        self.dropout = 0.5
        self.MLP_hidden=128
        
        self.convs = nn.ModuleList()
        # two cases
        if self.num_layers == 1:
            self.convs.append(HNHNConv(args.num_features, self.MLP_hidden, args.num_classes,
                                       nonlinear_inbetween=args.HNHN_nonlinear_inbetween))
        else:
            self.convs.append(HNHNConv(args.num_features, self.MLP_hidden, self.MLP_hidden,
                                       nonlinear_inbetween=args.HNHN_nonlinear_inbetween))
            for _ in range(self.num_layers - 2):
                self.convs.append(HNHNConv(self.MLP_hidden, self.MLP_hidden, self.MLP_hidden,
                                           nonlinear_inbetween=args.HNHN_nonlinear_inbetween))
            self.convs.append(HNHNConv(self.MLP_hidden, self.MLP_hidden, args.num_classes,
                                       nonlinear_inbetween=args.HNHN_nonlinear_inbetween))
        self.reset_parameters()

    def reset_parameters(self):
        for conv in self.convs:
            conv.reset_parameters()

    def forward(self, data):

        x = data.features
        
        if self.num_layers == 1:
            conv = self.convs[0]
            x = conv(x, data)
            # x = F.dropout(x, p=self.dropout, training=self.training)
        else:
            for i, conv in enumerate(self.convs[:-1]):
                x = F.relu(conv(x, data))
                x = F.dropout(x, p=self.dropout, training=self.training)
            x = self.convs[-1](x, data)

        return x

class HNHN_e(nn.Module):
    """
    """

    def __init__(self, args):
        super(HNHN_e, self).__init__()

        self.num_layers = 2
        self.dropout = 0.5
        self.MLP_hidden=128
        
        self.convs = nn.ModuleList()
        # two cases
        if self.num_layers == 1:
            self.convs.append(HNHNConv(args.num_features, self.MLP_hidden, args.num_classes,
                                       nonlinear_inbetween=args.HNHN_nonlinear_inbetween))
        else:
            self.convs.append(HNHNConv(args.num_features, self.MLP_hidden, self.MLP_hidden,
                                       nonlinear_inbetween=args.HNHN_nonlinear_inbetween))
            for _ in range(self.num_layers - 1):
                self.convs.append(HNHNConv(self.MLP_hidden, self.MLP_hidden, self.MLP_hidden,
                                           nonlinear_inbetween=args.HNHN_nonlinear_inbetween))
        
        self.mlp_edge = nn.Linear(self.MLP_hidden, 1)
        self.reset_parameters()

    def reset_parameters(self):
        self.mlp_edge.reset_parameters()
        for conv in self.convs:
            conv.reset_parameters()

    def forward(self, data, v, e):

        x = data.features
        
        if self.num_layers == 1:
            conv = self.convs[0]
            x = conv(x, data)
            # x = F.dropout(x, p=self.dropout, training=self.training)
        else:
            for i, conv in enumerate(self.convs[:-1]):
                x = F.relu(conv(x, data))
                x = F.dropout(x, p=self.dropout, training=self.training)
            x = self.convs[-1](x, data)
        
        Z = scatter(src = x[v, :], index = e, dim = 0, reduce = 'sum')
        x = self.mlp_edge(Z)

        return x
