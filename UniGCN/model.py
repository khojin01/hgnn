

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

# v1: X -> XW -> AXW -> norm
class UniGCNConv(nn.Module):

    def __init__(self, args, in_channels, out_channels, negative_slope=0.2):
        super().__init__()
        self.W = nn.Linear(in_channels, out_channels, bias=False)        
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.negative_slope = negative_slope
        self.dropout = 0.5
        self.args = args 
    
    def reset_parameters(self):
        self.W.reset_parameters()

    def __repr__(self):
        return '{}({}, {}, heads={})'.format(self.__class__.__name__,
                                             self.in_channels,
                                             self.out_channels, 1)

    def forward(self, X, vertex, edges):
        N = X.shape[0]
        degE = self.args.UniGNN_degE
        degV = self.args.UniGNN_degV
        
        # v1: X -> XW -> AXW -> norm
        
        X = self.W(X)

        Xve = X[vertex] # [nnz, C]
        Xe = scatter(Xve, edges, dim=0, reduce='sum') # [E, C]
        
        Xe = Xe * degE 

        Xev = Xe[edges] # [nnz, C]
        Xv = scatter(Xev, vertex, dim=0, reduce='sum', dim_size=N) # [N, C]
        
        Xv = Xv * degV

        X = Xv 
        
        if self.args.UniGNN_use_norm:
            X = normalize_l2(X)

        # NOTE: skip concat here?

        return X

class UniGCN_e(nn.Module):
    def __init__(self, args, V, E):
        """UniGNN

        Args:
            args   (NamedTuple): global args
            nfeat  (int): dimension of features
            nhid   (int): dimension of hidden features, note that actually it\'s #nhid x #nhead
            nclass (int): number of classes
            nlayer (int): number of hidden layers
            nhead  (int): number of conv heads
            V (torch.long): V is the row index for the sparse incident matrix H, |V| x |E|
            E (torch.long): E is the col index for the sparse incident matrix H, |V| x |E|
        """
        super().__init__()
        self.nfeat=args.num_features
        self.nhid=128
        self.nlayer=2


        self.conv_out = UniGCNConv(args, self.nhid, self.nhid)
        self.convs = nn.ModuleList(
            [ UniGCNConv(args, self.nfeat, self.nhid)] +
            [UniGCNConv(args, self.nhid, self.nhid) for _ in range(self.nlayer-1)]
        )
        self.V = V 
        self.E = E 
        self.act = nn.ReLU()
        self.input_drop = nn.Dropout(0.5)
        self.dropout = nn.Dropout(0.5)
        self.mlp_edge = nn.Linear(self.nhid, 1)
        self.reset_parameters()

    def reset_parameters(self):
        self.mlp_edge.reset_parameters()
        for conv in self.convs:
            conv.reset_parameters()
            
    def forward(self, data, v, e):
        V, E = self.V, self.E 
        X=data.features
        X = self.input_drop(X)
        for conv in self.convs:
            X = conv(X, V, E)
            X = self.act(X)
            X = self.dropout(X)

        X = self.conv_out(X, V, E)
        Z = scatter(src = X[v, :], index = e, dim = 0, reduce = 'sum')
        X = self.mlp_edge(Z)      
        return X

class UniGCN_n(nn.Module):
    def __init__(self, args, V, E):
        """UniGNN

        Args:
            args   (NamedTuple): global args
            nfeat  (int): dimension of features
            nhid   (int): dimension of hidden features, note that actually it\'s #nhid x #nhead
            nclass (int): number of classes
            nlayer (int): number of hidden layers
            nhead  (int): number of conv heads
            V (torch.long): V is the row index for the sparse incident matrix H, |V| x |E|
            E (torch.long): E is the col index for the sparse incident matrix H, |V| x |E|
        """
        super().__init__()
        self.nfeat=args.num_features
        self.nhid=128
        self.nclass=args.num_classes
        self.nlayer=2


        self.conv_out = UniGCNConv(args, self.nhid, self.nclass)
        self.convs = nn.ModuleList(
            [ UniGCNConv(args, self.nfeat, self.nhid)] +
            [UniGCNConv(args, self.nhid, self.nhid) for _ in range(self.nlayer-2)]
        )
        self.V = V 
        self.E = E 
        self.act = nn.ReLU()
        self.input_drop = nn.Dropout(0.5)
        self.dropout = nn.Dropout(0.5)
        self.reset_parameters()

    def reset_parameters(self):
        for conv in self.convs:
            conv.reset_parameters()
            
    def forward(self, data):
        V, E = self.V, self.E 
        X=data.features
        X = self.input_drop(X)
        for conv in self.convs:
            X = conv(X, V, E)
            X = self.act(X)
            X = self.dropout(X)

        X = self.conv_out(X, V, E)      
        return X