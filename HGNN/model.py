

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
def glorot(tensor):
    if tensor is not None:
        stdv = math.sqrt(6.0 / (tensor.size(-2) + tensor.size(-1)))
        tensor.data.uniform_(-stdv, stdv)


def zeros(tensor):
    if tensor is not None:
        tensor.data.fill_(0)

class HypergraphConv(MessagePassing):

    def __init__(self, in_channels, out_channels, symdegnorm=False, use_attention=False, heads=1,
                 concat=True, negative_slope=0.2, dropout=0, bias=True,
                 **kwargs):
        kwargs.setdefault('aggr', 'add')
        super(HypergraphConv, self).__init__(node_dim=0, **kwargs)

        self.in_channels = in_channels
        self.out_channels = out_channels
        self.use_attention = use_attention
        self.symdegnorm = symdegnorm

        if self.use_attention:
            self.heads = heads
            self.concat = concat
            self.negative_slope = negative_slope
            self.dropout = dropout
            self.weight = Parameter(
                torch.Tensor(in_channels, heads * out_channels))
            self.att = Parameter(torch.Tensor(1, heads, 2 * out_channels))
        else:
            self.heads = 1
            self.concat = True
            self.weight = Parameter(torch.Tensor(in_channels, out_channels))

        if bias and concat:
            self.bias = Parameter(torch.Tensor(heads * out_channels))
        elif bias and not concat:
            self.bias = Parameter(torch.Tensor(out_channels))
        else:
            self.register_parameter('bias', None)

        self.reset_parameters()

    def reset_parameters(self):

        glorot(self.weight)
        if self.use_attention:
            glorot(self.att)
        zeros(self.bias)

    def forward(self, x: Tensor, hyperedge_index: Tensor,
                hyperedge_weight: Optional[Tensor] = None) -> Tensor:
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
        num_nodes, num_edges = x.size(0), 0
        if hyperedge_index.numel() > 0:
            num_edges = int(hyperedge_index[1].max()) + 1

        if hyperedge_weight is None:
            hyperedge_weight = x.new_ones(num_edges)

        x = torch.matmul(x, self.weight)

        alpha = None
        
        D = scatter_add(hyperedge_weight[hyperedge_index[1]],
                        hyperedge_index[0], dim=0, dim_size=num_nodes)
        D = 1.0 / D**(0.5)
        D[D == float("inf")] = 0

        B = scatter_add(x.new_ones(hyperedge_index.size(1)),
                        hyperedge_index[1], dim=0, dim_size=num_edges)
        B = 1.0 / B
        B[B == float("inf")] = 0

        x = D.unsqueeze(-1)*x
        self.flow = 'source_to_target'
        out = self.propagate(hyperedge_index, x=x, norm=B, alpha=alpha,
                                size=(num_nodes, num_edges))
        # PyG's current MessagePassing implementation validates ``size`` in
        # source-to-target order.  Explicitly reverse the incidence pairs for
        # the hyperedge-to-node pass instead of changing ``flow``; the former
        # was accepted by the original PyG version but now causes a 341/1290
        # dimension mismatch on House.
        self.flow = 'source_to_target'
        out = self.propagate(hyperedge_index.flip(0), x=out, norm=D, alpha=alpha,
                                size=(num_edges, num_nodes))

        if self.concat is True:
            out = out.view(-1, self.heads * self.out_channels)
        else:
            out = out.mean(dim=1)

        if self.bias is not None:
            out = out + self.bias

        return out
        
class HGNN_n(nn.Module):

    def __init__(self, args):
        super(HGNN_n, self).__init__()

        self.num_layers = 2
        self.dropout = 0.5 
        self.MLP_hidden=128
        self.symdegnorm=False
        self.out_channels=args.num_classes



#         Note that add dropout to attention is default in the original paper
        self.convs = nn.ModuleList()
        self.convs.append(HypergraphConv(args.num_features,
                                         self.MLP_hidden, self.symdegnorm))
        for _ in range(self.num_layers-2):
            self.convs.append(HypergraphConv(
                self.MLP_hidden, self.MLP_hidden, self.symdegnorm))
        # Output heads is set to 1 as default
        self.convs.append(HypergraphConv(
            self.MLP_hidden, self.out_channels, self.symdegnorm))

        self.reset_parameters()

    def reset_parameters(self):
        for conv in self.convs:
            conv.reset_parameters()

    def forward(self, data):

        x = data.features
        edge_index = data.hyperedge_index

        for i, conv in enumerate(self.convs[:-1]):
            x = F.elu(conv(x, edge_index))
            x = F.dropout(x, p=self.dropout, training=self.training)

#         x = F.dropout(x, p=self.dropout, training=self.training)
        x = self.convs[-1](x, edge_index)

        return x

        
class HGNN_e(nn.Module):

    def __init__(self, args):
        super(HGNN_e, self).__init__()

        self.num_layers = 2
        self.dropout = 0.5 
        self.MLP_hidden=128
        self.symdegnorm=False



#         Note that add dropout to attention is default in the original paper
        self.convs = nn.ModuleList()
        self.convs.append(HypergraphConv(args.num_features,
                                         self.MLP_hidden, self.symdegnorm))
        for _ in range(self.num_layers-1):
            self.convs.append(HypergraphConv(
                self.MLP_hidden, self.MLP_hidden, self.symdegnorm))
        self.mlp_edge = nn.Linear(self.MLP_hidden, 1)

        self.reset_parameters()

    def reset_parameters(self):
        self.mlp_edge.reset_parameters()
        for conv in self.convs:
            conv.reset_parameters()

    def forward(self, data, v, e):

        x = data.features
        edge_index = data.hyperedge_index

        for i, conv in enumerate(self.convs[:-1]):
            x = F.elu(conv(x, edge_index))
            x = F.dropout(x, p=self.dropout, training=self.training)

        x = self.convs[-1](x, edge_index)
        Z = scatter(src = x[v, :], index = e, dim = 0, reduce = 'sum')
        x = self.mlp_edge(Z)

        return x
