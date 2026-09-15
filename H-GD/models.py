import numpy as np
import scipy.sparse as sp
import torch
import torch.nn as nn
import time

class GCN(nn.Module):
    def __init__(self, in_ft, out_ft, act, bias=True):
        super(GCN, self).__init__()
        self.fc = nn.Linear(in_ft, out_ft, bias=False)
        self.act = nn.PReLU() if act == 'prelu' else act
        
        if bias:
            self.bias = nn.Parameter(torch.FloatTensor(out_ft))
            self.bias.data.fill_(0.0)
        else:
            self.register_parameter('bias', None)

        for m in self.modules():
            self.weights_init(m)

    def weights_init(self, m):
        if isinstance(m, nn.Linear):
            torch.nn.init.xavier_uniform_(m.weight.data)
            if m.bias is not None:
                m.bias.data.fill_(0.0)

    # Shape of seq: (batch, nodes, features)
    def forward(self, seq, adj, sparse=False):
        seq_fts = self.fc(seq)
        if sparse:
            out = torch.spmm(adj, torch.squeeze(seq_fts, 0))
        else:
            out = torch.bmm(adj, seq_fts)
        if self.bias is not None:
            out += self.bias
        
        return self.act(out)

class GCN_m(nn.Module):
    def __init__(self, in_ft, out_ft, act, k, bias=True):
        self.act = nn.PReLU() if act == 'prelu' else act
        self.conv = [GCN(in_ft, out_ft)]
        for _ in range(0, k):
            self.conv.append(GCN(out_ft, out_ft))
        self.conv = nn.ModuleList(self.conv)


class GGD(nn.Module):
    def __init__(self, n_in, n_h, activation):
        super(GGD, self).__init__()
        self.gcn = GCN(n_in, n_h, activation)
        self.lin = nn.Linear(n_h, n_h)

    def forward(self, seq1, seq2, adj, sparse):
        h_1 = self.gcn(seq1, adj, sparse)
        h_2 = self.gcn(seq2, adj, sparse)
        sc_1 = ((self.lin(h_1.squeeze(0))).sum(1)).unsqueeze(0)
        sc_2 = ((self.lin(h_2.squeeze(0))).sum(1)).unsqueeze(0)

        logits = torch.cat((sc_1, sc_2), 1)
        return logits

    # Detach the return variables
    def embed(self, seq, adj, sparse):
        h_1 = self.gcn(seq, adj, sparse)
        h_2 = h_1.clone()
        for i in range(5):
            h_2 = adj @ h_2

        return h_1.detach(), h_2.detach()