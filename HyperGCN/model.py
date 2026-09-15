import math
import torch
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
import util
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


class HyperGCN_e(nn.Module):
    def __init__(self, V, X, args):
        """
        d: initial node-feature dimension
        h: number of hidden units
        c: number of classes
        """
        super(HyperGCN_e, self).__init__()
        dropout=0.5
        num_layers=2
        d, l = args.num_features, num_layers
        device = args.device  # and torch.device.is_available()
        self.MLP_hidden=128

        h = [d]
        for i in range(l):
            power = l - i + 2
            
            h.append(self.MLP_hidden)

        reapproximate = True

        self.layers = nn.ModuleList([util.HyperGraphConvolution(
            h[i], h[i+1], reapproximate, device) for i in range(l)])
        self.do, self.l = dropout, num_layers
        self.m = args.HyperGCN_mediators
        self.mlp_edge = nn.Linear(self.MLP_hidden, 1)

        self.reset_parameters()

    def reset_parameters(self):
        self.mlp_edge.reset_parameters()
        for layer in self.layers:
            layer.reset_parameters()

    def forward(self, data, v, e):
        """
        an l-layer GCN
        """
        do, l, m = self.do, self.l, self.m
        H = data.features
        E = data.hypergraph

        for i, hidden in enumerate(self.layers):
            H = F.relu(hidden(E, H, m))
            if i < l - 1:
                V = H
                H = F.dropout(H, do, training=self.training)

        Z = scatter(src = H[v, :], index = e, dim = 0, reduce = 'sum')
        x = self.mlp_edge(Z)


        return x


class HyperGCN_n(nn.Module):
    def __init__(self, V, E, X, args):
        """
        d: initial node-feature dimension
        h: number of hidden units
        c: number of classes
        """
        super(HyperGCN_n, self).__init__()
        dropout=0.5
        num_layers=2
        d, l, c = args.num_features, num_layers, args.num_classes
        device = args.device  # and torch.device.is_available()

        h = [d]
        for i in range(l-1):
            power = l - i + 2
            
            h.append(2**power)
        h.append(c)

        reapproximate = True
        structure = E

        self.layers = nn.ModuleList([util.HyperGraphConvolution(
            h[i], h[i+1], reapproximate, device) for i in range(l)])
        self.do, self.l = dropout, num_layers
        self.structure, self.m = structure, args.HyperGCN_mediators
        self.reset_parameters()

    def reset_parameters(self):
        for layer in self.layers:
            layer.reset_parameters()

    def forward(self, data):
        """
        an l-layer GCN
        """
        do, l, m = self.do, self.l, self.m
        H = data.features

        for i, hidden in enumerate(self.layers):
            H = F.relu(hidden(self.structure, H, m))
            if i < l - 1:
                V = H
                H = F.dropout(H, do, training=self.training)

        return H