

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



class GraphConvolution(nn.Module):

    def __init__(self, in_features, out_features, residual=False, variant=False, incidence_v=100, incidence_e=50,
                 init_dist=None, args=None):
        super(GraphConvolution, self).__init__()
        self.variant = variant
        self.args = args
        if self.variant:
            self.in_features = 2 * in_features
        else:
            self.in_features = in_features
        self.lam4=0
        
        self.lam0=args.lam0
        self.lam1=args.lam1
        self.alpha=args.alp if args.alp !=0 else 1/(1+args.lam4+args.lam0+args.lam1)
        self.num_steps=args.prop_step
        self.out_features = out_features
        self.residual = residual
        self.notresidual=args.notresidual
        self.twoHgamma=args.twoHgamma
        # self.weight = Parameter(torch.FloatTensor(self.in_features, self.out_features))
        self.adj = None
        self.normalize_type=args.normalize_type#in ["edge","none","full","node"]
        if args.H:
            H = {}
            for t in ["beta","gamma1","gamma2"]:

                if args.notresidual:
                    H[t] = torch.rand(in_features, in_features)
                    bound = 4/in_features # normal
                    nn.init.normal_(H[t], 0, bound)
                    H[t] = nn.Parameter(H[t])
                else:


                    H[t] = torch.rand(in_features, in_features)
                    bound =1/in_features # normal
                    nn.init.normal_(H[t], 0, bound)
                    H[t] = H[t] + torch.eye(in_features)
                
                
                    H[t] = nn.Parameter(H[t])
                
            self.H = nn.ParameterDict(H)

        else:
            self.H=None
       

        self.init_attn=None
        self.reset_parameters()

    def reset_parameters(self):
       pass
    
    def forward(self, X, A, D):
        A_beta, A_gamma = A           # (N, N)
        D_beta, D_gamma, I = D        # (N, N), all dense tensors

        H = self.H                    # dictionary of projection matrices
        Y = Y0 = X                    # initial features

        epsilon = 1e-6
        diagD = False

        if H is not None:
            Q_tild = self.lam0 * D_beta + self.lam1 * D_gamma + I
            diagD = True

            L_gamma = D_gamma - A_gamma
            H_1 = H["beta"]
            H_2 = H["gamma1"]
            H_3 = H["gamma2"]
        else:
            Q_tild = self.lam0 * D_beta + self.lam1 * D_gamma + I

        for k in range(self.num_steps):
            Q_inv = torch.inverse(Q_tild + epsilon * torch.eye(Q_tild.size(0), device=Q_tild.device))

            if H is not None:
                if diagD:
                    if self.twoHgamma:
                        Y_hat = (
                            self.lam0 * (A_beta @ Y @ (H_1 + H_1.T) - D_beta @ Y @ H_1 @ H_1.T)
                            + Y0
                            + (self.lam1 / 2)
                            * (
                                L_gamma @ Y
                                + A_gamma @ Y @ (H_2 + H_2.T)
                                - D_gamma @ Y @ H_2 @ H_2.T
                                + A_gamma @ Y @ (H_3 + H_3.T)
                                - D_gamma @ Y @ H_3 @ H_3.T
                            )
                        )
                    else:
                        if self.args.HisI:
                            Y_hat = self.lam0 * (2 * A_beta @ Y - D_beta @ Y) + Y0 + self.lam1 * A_gamma @ Y
                        else:
                            Y_hat = (
                                self.lam0 * (A_beta @ Y @ (H_1 + H_1.T) - D_beta @ Y @ H_1 @ H_1.T)
                                + Y0
                                + self.lam1 * (L_gamma @ Y + A_gamma @ Y @ (H_2 + H_2.T) - D_gamma @ Y @ H_2 @ H_2.T)
                            )
            else:
                Y_hat = self.lam0 * A_beta @ Y + Y0 + self.lam1 * A_gamma @ Y

            Y = (1 - self.alpha) * Y + self.alpha * Q_inv @ Y_hat

        return Y
        


class phenomnn(nn.Module):
    def __init__(self, nfeat, nlayers, nhidden, nclass, dropout, variant, incidence_v=100, incidence_e=50,
                 init_dist=None, args=None):
        super(phenomnn, self).__init__()
        self.convs = nn.ModuleList()
        for _ in range(1):
            self.convs.append(GraphConvolution(nhidden, nhidden, variant=variant,args=args))
        self.fcs = nn.ModuleList()
        self.fcs.append(nn.Linear(nfeat, nhidden))
        self.fcs.append(nn.Linear(nhidden, nclass))
        self.in_features = nfeat
        self.out_features = nclass
        self.hiddendim = nhidden
        self.nhiddenlayer = nlayers

        self.params1 = list(self.convs.parameters())
        self.params2 = list(self.fcs.parameters())
        self.act_fn = nn.ReLU()
        self.dropout = dropout
    def reset_parameters(self):
        for conv in self.convs:
            conv.reset_parameters()
        for layer in self.fcs:
            layer.reset_parameters()

    def forward(self, input, adj, D):
        _layers = []
        x = F.dropout(input, self.dropout, training=self.training)
        layer_inner = self.act_fn(self.fcs[0](x))
        # layer_inner = input
        _layers.append(layer_inner)
        for i, con in enumerate(self.convs):
            layer_inner = F.dropout(layer_inner, self.dropout, training=self.training)
            layer_inner = self.act_fn(con(layer_inner, A=adj, D=D))
        layer_inner = F.dropout(layer_inner, self.dropout, training=self.training)
        layer_inner = self.fcs[-1](layer_inner)
        self.adj = con.adj  # 保存看看学的结果
        return layer_inner  # F.log_softmax(layer_inner, dim=1)

    def get_outdim(self):
        return self.out_features




class PhenomNN_n(nn.Module):
    """
       The model architecture likes:
       All options are configurable.
    """

    def __init__(self,
                 nfeat,
                 nclass,
                 inputlayer=None,
                 outputlayer=None,
                 args=None,
                 ):
        super(PhenomNN_n, self).__init__()
        self.dropout = 0.5
        self.nbaselayer = 2
        self.args = args

        self.nhid=128
        self.nhidlayer=2


        self.BASEBLOCK = phenomnn

        self.midlayer = nn.ModuleList()

        for i in range(self.nhidlayer):
            
            gcb = self.BASEBLOCK(nfeat=nfeat,
                                     nlayers=self.nbaselayer,
                                     nhidden=self.nhid,
                                     nclass=nclass,
                                     dropout=self.dropout,
                                     variant=args.phenomNN_variant,
                                     args=args,
                                     )

            
            self.midlayer.append(gcb)
        self.params1 = self.midlayer[0].params1
        self.params2 = self.midlayer[0].params2
        self.reset_parameters()

    def reset_parameters(self):
        for layer in self.midlayer:
            layer.reset_parameters()

    def forward(self, data):
        fea=data.features
        G=data.G
        adj=data.H
        out = self.midlayer[0](input=fea, adj=adj, D=G)
        return out



class PhenomNN_e(nn.Module):
    """
       The model architecture likes:
       All options are configurable.
    """

    def __init__(self,
                 nfeat,
                 inputlayer=None,
                 outputlayer=None,
                 args=None,
                 ):
        super(PhenomNN_e, self).__init__()
        self.dropout = 0.5
        self.nbaselayer = 2
        self.args = args

        self.nhid=128
        self.nhidlayer=2


        self.BASEBLOCK = phenomnn

        self.midlayer = nn.ModuleList()

        for i in range(self.nhidlayer):
            
            gcb = self.BASEBLOCK(nfeat=nfeat,
                                     nlayers=self.nbaselayer,
                                     nhidden=self.nhid,
                                     nclass=self.nhid,
                                     dropout=self.dropout,
                                     variant=args.phenomNN_variant,
                                     args=args,
                                     )

            
            self.midlayer.append(gcb)
        self.params1 = self.midlayer[0].params1
        self.params2 = self.midlayer[0].params2
        self.mlp_edge = nn.Linear(self.nhid, 1)
        self.reset_parameters()

    def reset_parameters(self):
        self.mlp_edge.reset_parameters()
        for layer in self.midlayer:
            layer.reset_parameters()

    def forward(self, data,v,e):
        fea=data.features
        G=data.G
        adj=data.H
        out = self.midlayer[0](input=fea, adj=adj, D=G)
        Z = scatter(src = out[v, :], index = e, dim = 0, reduce = 'sum')
        x = self.mlp_edge(Z)


        return x
