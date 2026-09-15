

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


class UniGCNIIConv(nn.Module):
    def __init__(self, args, in_features, out_features):
        super().__init__()
        self.W = nn.Linear(in_features, out_features, bias=False)
        self.args = args

    def reset_parameters(self):
        self.W.reset_parameters()
        
    def forward(self, X, vertex, edges, alpha, beta, X0):
        N = X.shape[0]
        degE = self.args.UniGNN_degE
        degV = self.args.UniGNN_degV

        Xve = X[vertex] # [nnz, C]
        Xe = scatter(Xve, edges, dim=0, reduce='mean') # [E, C], reduce is 'mean' here as default
        
        Xe = Xe * degE 

        Xev = Xe[edges] # [nnz, C]
        Xv = scatter(Xev, vertex, dim=0, reduce='sum', dim_size=N) # [N, C]
        
        Xv = Xv * degV
        
        X = Xv 

        if self.args.UniGNN_use_norm:
            X = normalize_l2(X)

        Xi = (1-alpha) * X + alpha * X0
        X = (1-beta) * Xi + beta * self.W(Xi)


        return X

class UniGCN2_n(nn.Module):
    def __init__(self, args, V, E):
        """UniGNNII

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
        self.V = V 
        self.E = E 
        self.act = nn.ReLU() # Default relu
        self.dropout = nn.Dropout(0.5) # 0.2 is chosen for GCNII

        self.nfeat=args.num_features
        self.nhid=128
        self.nclass=args.num_classes
        self.nlayer=2


        self.convs = torch.nn.ModuleList()
        self.convs.append(torch.nn.Linear(self.nfeat, self.nhid))
        for _ in range(self.nlayer):
            self.convs.append(UniGCNIIConv(args, self.nhid, self.nhid))
        self.convs.append(torch.nn.Linear(self.nhid, self.nclass))
        self.reg_params = list(self.convs[1:-1].parameters())
        self.non_reg_params = list(self.convs[0:1].parameters())+list(self.convs[-1:].parameters())
        
    def reset_parameters(self):
        for conv in self.convs:
            conv.reset_parameters()
        
    def forward(self, data):
        x = data.features
        V, E = self.V, self.E 
        lamda, alpha = 0.5, 0.1 
        x = self.dropout(x)
        x = F.relu(self.convs[0](x))
        x0 = x 
        for i,con in enumerate(self.convs[1:-1]):
            x = self.dropout(x)
            beta = math.log(lamda/(i+1)+1)
            x = F.relu(con(x, V, E, alpha, beta, x0))
        x = self.dropout(x)
        x = self.convs[-1](x)
        return x


class UniGCN2_e(nn.Module):
    def __init__(self, args, V, E):
        """UniGNNII

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
        self.V = V 
        self.E = E 
        self.act = nn.ReLU() # Default relu
        self.dropout = nn.Dropout(0.5) # 0.2 is chosen for GCNII

        self.nfeat=args.num_features
        self.nhid=128
        self.nclass=args.num_classes
        self.nlayer=2


        self.convs = torch.nn.ModuleList()
        self.convs.append(torch.nn.Linear(self.nfeat, self.nhid))
        for _ in range(self.nlayer):
            self.convs.append(UniGCNIIConv(args, self.nhid, self.nhid))
        self.convs.append(torch.nn.Linear(self.nhid, self.nhid))
        self.reg_params = list(self.convs[1:-1].parameters())
        self.non_reg_params = list(self.convs[0:1].parameters())+list(self.convs[-1:].parameters())
        self.mlp_edge = nn.Linear(self.nhid, 1)
        
    def reset_parameters(self):
        self.mlp_edge.reset_parameters()
        for conv in self.convs:
            conv.reset_parameters()
        
    def forward(self, data,v,e):
        x = data.features
        V, E = self.V, self.E 
        lamda, alpha = 0.5, 0.1 
        x = self.dropout(x)
        x = F.relu(self.convs[0](x))
        x0 = x 
        for i,con in enumerate(self.convs[1:-1]):
            x = self.dropout(x)
            beta = math.log(lamda/(i+1)+1)
            x = F.relu(con(x, V, E, alpha, beta, x0))
        x = self.dropout(x)
        x = self.convs[-1](x)
        Z = scatter(src = x[v, :], index = e, dim = 0, reduce = 'sum')
        x = self.mlp_edge(Z)      
        return x
