
import torch
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
from torch_scatter import scatter_add, scatter
class MLP_model_n(nn.Module):
    """ adapted from https://github.com/CUAI/CorrectAndSmooth/blob/master/gen_models.py """

    def __init__(self, args):
        super(MLP_model_n, self).__init__()
        in_channels = args.num_features
        hidden_channels = 128
        out_channels = args.num_classes
        num_layers = 2
        dropout = 0.5

        self.lins = nn.ModuleList()
        self.normalizations = nn.ModuleList()

        self.normalizations.append(nn.Identity())
        self.lins.append(nn.Linear(in_channels, hidden_channels))
        self.normalizations.append(nn.Identity())
        for _ in range(num_layers - 2):
            self.lins.append(
                nn.Linear(hidden_channels, hidden_channels))
            self.normalizations.append(nn.Identity())
        self.lins.append(nn.Linear(hidden_channels, out_channels))
        

        self.dropout = dropout

        self.reset_parameters()

    def reset_parameters(self):
        for lin in self.lins:
            lin.reset_parameters()
        for normalization in self.normalizations:
            if normalization.__class__.__name__ != 'Identity':
                normalization.reset_parameters()

    def forward(self, data):
        x = data.features
        x = self.normalizations[0](x)
        for i, lin in enumerate(self.lins[:-1]):
            x = lin(x)
            x = F.relu(x, inplace=True)
            x = self.normalizations[i+1](x)
            x = F.dropout(x, p=self.dropout, training=self.training)
        x = self.lins[-1](x)
        return x

class MLP_model_e(nn.Module):
    """ adapted from https://github.com/CUAI/CorrectAndSmooth/blob/master/gen_models.py """

    def __init__(self, args):
        super(MLP_model_e, self).__init__()
        in_channels = args.num_features
        hidden_channels = 128
        out_channels = 1
        num_layers = 2
        dropout = 0.5

        self.lins = nn.ModuleList()
        self.normalizations = nn.ModuleList()

        self.normalizations.append(nn.Identity())
        self.lins.append(nn.Linear(in_channels, hidden_channels))
        self.normalizations.append(nn.Identity())
        for _ in range(num_layers - 2):
            self.lins.append(
                nn.Linear(hidden_channels, hidden_channels))
            self.normalizations.append(nn.Identity())
        self.lins.append(nn.Linear(hidden_channels, out_channels))
        

        self.dropout = dropout

        self.reset_parameters()

    def reset_parameters(self):
        for lin in self.lins:
            lin.reset_parameters()
        for normalization in self.normalizations:
            if normalization.__class__.__name__ != 'Identity':
                normalization.reset_parameters()

    def forward(self, X,v,e):
        Z = scatter(src = X[v, :], index = e, dim = 0, reduce = 'sum')
        
        x = self.normalizations[0](Z)
        for i, lin in enumerate(self.lins[:-1]):
            x = lin(x)
            x = F.relu(x, inplace=True)
            x = self.normalizations[i+1](x)
            x = F.dropout(x, p=self.dropout, training=self.training)
        x = self.lins[-1](x)
        return x