import sys
import os
import argparse
import random
import torch
import torch_sparse
from torch_scatter import scatter
import numpy as np
import scipy.sparse as sp
from tqdm import tqdm
from model import *
from util import *
from sklearn.metrics import roc_auc_score as auroc

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from loader import DatasetLoader
def fix_seed(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    random.seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = True
class Logger(object):
    """ Adapted from https://github.com/snap-stanford/ogb/ """

    def __init__(self, runs, info=None):
        self.info = info
        self.results = [[] for _ in range(runs)]

    def add_result(self, run, result):
        assert len(result) == 3
        assert run >= 0 and run < len(self.results)
        self.results[run].append(result)

    def print_statistics(self, run=None):
        if run is not None:
            result = 100 * torch.tensor(self.results[run])
            argmax = result[:, 1].argmax().item()
            print(f'Run {run + 1:02d}:')
            print(f'Highest Train: {result[:, 0].max():.2f}')
            print(f'Highest Valid: {result[:, 1].max():.2f}')
            print(f'  Final Train: {result[argmax, 0]:.2f}')
            print(f'   Final Test: {result[argmax, 2]:.2f}')
        else:
            result = 100 * torch.tensor(self.results)

            best_results = []
            for r in result:
                train1 = r[:, 0].max().item()
                valid = r[:, 1].max().item()
                train2 = r[r[:, 1].argmax(), 0].item()
                test = r[r[:, 1].argmax(), 2].item()
                best_results.append((train1, valid, train2, test))

            best_result = torch.tensor(best_results)

            print(f'All runs:')
            r = best_result[:, 0]
            print(f'Highest Train: {r.mean():.2f} ± {r.std():.2f}')
            r = best_result[:, 1]
            print(f'Highest Valid: {r.mean():.2f} ± {r.std():.2f}')
            r = best_result[:, 2]
            print(f'  Final Train: {r.mean():.2f} ± {r.std():.2f}')
            r = best_result[:, 3]
            print(f'   Final Test: {r.mean():.2f} ± {r.std():.2f}')

            return best_result[:, 1], best_result[:, 3]


@torch.no_grad()
def evaluate_n(model, data, split_idx, eval_func, result=None):
    if result is not None:
        out = result
    else:
        model.eval()
        out = model(data)
        out = F.log_softmax(out, dim=1)

    train_acc = eval_func(
        data.labels[split_idx[0]], out[split_idx[0]])
    valid_acc = eval_func(
        data.labels[split_idx[1]], out[split_idx[1]])
    test_acc = eval_func(
        data.labels[split_idx[2]], out[split_idx[2]])

#     Also keep track of losses
    train_loss = F.nll_loss(
        out[split_idx[0]], data.labels[split_idx[0]])
    valid_loss = F.nll_loss(
        out[split_idx[1]], data.labels[split_idx[1]])
    test_loss = F.nll_loss(
        out[split_idx[2]], data.labels[split_idx[2]])
    return train_acc, valid_acc, test_acc, train_loss, valid_loss, test_loss, out

@torch.no_grad()
def evaluate_e(model, train_data, valid_data, test_data, eval_func_e):
    train_auroc,train_loss = eval_func_e(model,train_data)
    valid_auroc,valid_loss = eval_func_e(model,valid_data)
    test_auroc,test_loss = eval_func_e(model,test_data)
    return train_auroc, valid_auroc, test_auroc, train_loss, valid_loss, test_loss


def eval_acc_node(y_true, y_pred):
    acc_list = []
    y_true = y_true.detach().cpu().numpy()
    y_pred = y_pred.argmax(dim=-1, keepdim=False).detach().cpu().numpy()

#     ipdb.set_trace()
#     for i in range(y_true.shape[1]):
    is_labeled = y_true == y_true
    correct = y_true[is_labeled] == y_pred[is_labeled]
    acc_list.append(float(np.sum(correct))/len(correct))

    return sum(acc_list)/len(acc_list)

def eval_acc_edge(model, data_split):
    v=data_split[0]
    e=torch.tensor(data_split[1]).to(args.device)
    label=data_split[2]

    with torch.no_grad():
        model.eval()
        out=model(data,v,e)
        pred=torch.sigmoid(out).squeeze(-1).detach().cpu().numpy()

    y_true = label.detach().cpu().numpy()
    score=auroc(y_true,pred)
    loss=F.binary_cross_entropy(torch.tensor(pred), label)

    return score,loss


   
if __name__ == '__main__':
    parser = argparse.ArgumentParser('HGNN model')
    parser.add_argument('--data', type=str, default='cora_cite', 
        choices=['citeseer_cite','cora_cite','pubmed_cite','cora_coauth','dblp_copub','dblp_coauth','aminer','imdb','modelnet_40','news','house'])
    parser.add_argument('--UniGNN_use-norm', action="store_true", help='use norm in the final layer')
    parser.add_argument('--UniGNN_degV', default = 0)
    parser.add_argument('--UniGNN_degE', default = 0)
    parser.add_argument('--num_seeds', type=int, default=20)
    parser.add_argument('--lr',default=0.001, type=float)
    parser.add_argument('--device', type=str, default='cuda:0')
    parser.add_argument('--task', type=str)
    
    parser.add_argument('--epoch', type=int, default=200)

    args = parser.parse_args()
    
    data = DatasetLoader().load(args.data).to(args.device)
    args.num_features=data.features.shape[1]
    args.num_classes=data.labels.max().item()+1
    args.method="UniGIN"
    node_splits = data.data_splits
    edge_splits = data.edge_splits

    fix_seed(0)
    accs = []
    logger = Logger(args.num_seeds, args)
    print(data.name)
    print(args)
    data,args=generate_norm_UniGIN(data,args)
    for seed in tqdm(range(args.num_seeds)):
        
        num_nodes, num_edges = data.num_nodes, data.num_edges
        if args.task=="edge":
            data.hyperedge_index = edge_splits[seed][3].to(args.device)
            data.num_edges = data.hyperedge_index[1].max()+1
            data,args=generate_norm_UniGIN(data,args)

            train_data,valid_data,test_data=edge_splits[seed][0],edge_splits[seed][1],edge_splits[seed][2]

            criterion = nn.BCELoss()
            eval_func = eval_acc_edge
            model=UniGIN_e(args, V=data.V, E=data.E).to(args.device)
            optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=1e-6)
            best_val = float('-inf')

            train_v=train_data[0]
            train_e=torch.tensor(train_data[1]).to(args.device)
            train_label = train_data[2].to(args.device)
        

            for epoch in range(args.epoch):
                model.train()
                optimizer.zero_grad()
                out = model(data,train_v,train_e)
                if out.size(-1) != 1:
                    assert False
                out = torch.sigmoid(out).squeeze(-1)
                loss=criterion(out,train_label)
                loss.backward()
                optimizer.step()

                result = evaluate_e(model, train_data, valid_data, test_data, eval_func)
                logger.add_result(seed, result[:3])

        elif args.task=="node":           

            train_idx,valid_idx,test_idx=node_splits[seed]
            criterion = nn.NLLLoss()
            eval_func = eval_acc_node
            model=UniGIN_n(args, V=data.V, E=data.E).to(args.device)
            optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=1e-6)
            best_val = float('-inf')
            import time

            for epoch in range(args.epoch):
                if epoch==1:
                    start=time.time()
                if epoch==10:
                    end=time.time()
                model.train()
                optimizer.zero_grad()
                out = model(data)
                if out.size(-1) != args.num_classes:
                    assert False
                out = F.log_softmax(out, dim=1)
                loss = criterion(out[train_idx], data.labels[train_idx])
                loss.backward()
                optimizer.step()
                result = evaluate_n(model, data, node_splits[seed], eval_func)
                logger.add_result(seed, result[:3])

    best_val, best_test = logger.print_statistics()
    path=f'./results/result_{args.data}_{args.method}_{args.task}.txt'
    with open(path, 'a+') as write_obj:
        write_obj.write(f'{args.lr}=> {best_test},{best_test.mean():.1f} ± {best_test.std():.1f}\n')

    if args.task == "node":
        path=f'./time/time.txt'
        with open(path, 'a+') as write_obj:
            write_obj.write(f'{args.data}_{args.method}:{end-start} acc:({best_test.mean()})\n')

    path=f'./result_small.txt'
    with open(path, 'a+') as write_obj:
        write_obj.write(f'{args.data},{args.method},{best_test.mean():.1f} ± {best_test.std():.1f}\n')
