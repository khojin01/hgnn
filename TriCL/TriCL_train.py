import argparse
import random

import yaml
from tqdm import tqdm
import numpy as np
import torch
import torch.nn as nn
from tricl.models import HyperEncoder, TriCL
from tricl.utils import drop_features, drop_incidence, valid_node_edge_mask, hyperedge_index_masking
from sklearn.metrics import roc_auc_score as auroc
from tricl.logreg import MLP,MLP_HENN
import copy

from sklearn import metrics
from torchmetrics import AveragePrecision
from torchmetrics.classification import BinaryAccuracy

import sys
import os
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


def train(model_type, num_negs):
    features, hyperedge_index = data.features, data.hyperedge_index
    num_nodes, num_edges = data.num_nodes, data.num_edges

    model.train()
    optimizer.zero_grad(set_to_none=True)

    # Hypergraph Augmentation
    hyperedge_index1 = drop_incidence(hyperedge_index, params['drop_incidence_rate'])
    hyperedge_index2 = drop_incidence(hyperedge_index, params['drop_incidence_rate'])
    x1 = drop_features(features, params['drop_feature_rate'])
    x2 = drop_features(features, params['drop_feature_rate'])

    node_mask1, edge_mask1 = valid_node_edge_mask(hyperedge_index1, num_nodes, num_edges)
    node_mask2, edge_mask2 = valid_node_edge_mask(hyperedge_index2, num_nodes, num_edges)
    node_mask = node_mask1 & node_mask2
    edge_mask = edge_mask1 & edge_mask2

    # Encoder
    n1, e1 = model(x1, hyperedge_index1, num_nodes, num_edges)
    n2, e2 = model(x2, hyperedge_index2, num_nodes, num_edges)

    # Projection Head
    n1, n2 = model.node_projection(n1), model.node_projection(n2)
    e1, e2 = model.edge_projection(e1), model.edge_projection(e2)

    loss_n = model.node_level_loss(n1, n2, params['tau_n'], batch_size=params['batch_size_1'], num_negs=num_negs)
    if model_type in ['tricl_ng', 'tricl']:
        loss_g = model.group_level_loss(e1[edge_mask], e2[edge_mask], params['tau_g'], batch_size=params['batch_size_1'], num_negs=num_negs)
    else:
        loss_g = 0

    if model_type in ['tricl']:
        masked_index1 = hyperedge_index_masking(hyperedge_index, num_nodes, num_edges, None, edge_mask1)
        masked_index2 = hyperedge_index_masking(hyperedge_index, num_nodes, num_edges, None, edge_mask2)
        loss_m1 = model.membership_level_loss(n1, e2[edge_mask2], masked_index2, params['tau_m'], batch_size=params['batch_size_2'])
        loss_m2 = model.membership_level_loss(n2, e1[edge_mask1], masked_index1, params['tau_m'], batch_size=params['batch_size_2'])
        loss_m = (loss_m1 + loss_m2) * 0.5
    else:
        loss_m = 0
    loss = loss_n + params['w_g'] * loss_g + params['w_m'] * loss_m
    loss.backward()
    optimizer.step()
    return loss.item()

def NC_evaluator_linear(z,classifier, idx, label):
    with torch.no_grad():
        classifier.eval()
        pred=torch.argmax(classifier(z),dim=1)
        acc=torch.sum((pred==label)[idx])/len(idx)
    return acc.item()
def accuracy(logits: list, labels: list):
    average_precision = AveragePrecision(task="binary")
    auc_roc = metrics.roc_auc_score(labels, logits)
    labels=torch.from_numpy(labels)
    labels=labels.type(torch.int32)
    ap = average_precision(torch.from_numpy(logits), labels)
    binary_acc= BinaryAccuracy()
    acc=binary_acc(torch.from_numpy(logits), labels)
    #eval 기록
    return auc_roc,ap,acc
def HE_evaluator(z,classifier, vidx, eidx,label):
    with torch.no_grad():
        classifier.eval()
        pred=classifier(z,vidx,eidx).to('cpu').detach().squeeze(-1).numpy()
        auroc,ap,acc=accuracy(pred,label)
    return auroc,ap,acc
def edge_prediction_linear_eval(args,edge_split,embeds,data):
    lr=0.001
    max_epoch=1000
    h_dim=512

    classifier=MLP_HENN(in_dim=embeds.shape[1],hidden_dim=h_dim).to(embeds.device)
    optimizer=torch.optim.AdamW(classifier.parameters(),lr=lr,weight_decay=0.0)
    criterion=nn.BCELoss()
    train_vidx = torch.tensor(edge_split[0][0]).to(embeds.device)
    train_eidx = torch.tensor(edge_split[0][1]).to(embeds.device)
    train_label = edge_split[0][2].float().to(embeds.device)
    
    valid_vidx = torch.tensor(edge_split[1][0]).to(embeds.device)
    valid_eidx = torch.tensor(edge_split[1][1]).to(embeds.device)
    valid_label = edge_split[1][2].float().cpu().detach().numpy()
    
    test_vidx = torch.tensor(edge_split[2][0]).to(embeds.device)
    test_eidx = torch.tensor(edge_split[2][1]).to(embeds.device)
    test_label = edge_split[2][2].float().cpu().detach().numpy()

    valid_score=0
    best_epoch=0


    embeds=embeds.detach()
    for epoch in tqdm(range(1, max_epoch + 1)):
        classifier.train()
        optimizer.zero_grad(set_to_none=True)
        pred=classifier(embeds,train_vidx,train_eidx)
        
        loss = criterion(pred, train_label)
        loss.backward()
        optimizer.step()

        if (epoch + 1) % 10 == 0:
            cur_score=HE_evaluator(z=embeds,classifier=classifier, vidx=valid_vidx, eidx=valid_eidx,label=valid_label)
            
            path=f'./logs/log_{args.method}_{data.name}.txt'
            with open(path, 'a+') as write_obj:
                write_obj.write(f'{args.data}{epoch}=> auroc: {cur_score[0]}, ap: {cur_score[1]}, acc: {cur_score[2]}\n')
            if epoch<=10:
                cur_score=list(cur_score)
                cur_score[0]=0
            if cur_score[0]>valid_score:
                valid_score=cur_score[0]
                param=copy.deepcopy(classifier.state_dict())
                best_epoch=epoch
                valid_results=cur_score
    classifier.load_state_dict(param)
    test_results=HE_evaluator(z=embeds, classifier=classifier, vidx=test_vidx, eidx=test_eidx,label=test_label)

    return valid_results, test_results, best_epoch

def node_prediction_linear_eval(args,node_splits,embeds,data):

    lr=0.001
    max_epoch=1000
    valid_results, test_results, best_epochs=[],[],[]
    for train_idx, valid_idx, test_idx in tqdm(node_splits[:args.num_seeds]):
        classifier = MLP(in_dim=embeds.shape[1],n_class =args.num_classes).to(embeds.device)
        optimizer=torch.optim.AdamW(classifier.parameters(),lr=lr,weight_decay=0.0)
        criterion=nn.CrossEntropyLoss()
        valid_score=0
        best_epoch=0        
        embeds=embeds.detach()
        for epoch in range(1, max_epoch + 1):
            classifier.train()
            optimizer.zero_grad(set_to_none=True)
            pred=classifier(embeds)[train_idx,:]
            y=data.labels
            loss = criterion(pred, y[train_idx])
            loss.backward()
            optimizer.step()

            if (epoch + 1) % 1 == 0:
                cur_score=NC_evaluator_linear(z=embeds, classifier=classifier, idx=valid_idx, label=y)
                
                path=f'./logs/log_{args.method}_{data.name}.txt'
                with open(path, 'a+') as write_obj:
                    write_obj.write(f'{data.name}{epoch}=>  val_acc: {cur_score}\n')
                if epoch<=10:
                    cur_score==0
                if cur_score>valid_score:
                    valid_score=cur_score
                    param=copy.deepcopy(classifier.state_dict())
                    best_epoch=epoch
                    valid_result=cur_score
        classifier.load_state_dict(param)
        test_result=NC_evaluator_linear(z=embeds, classifier=classifier, idx=test_idx, label=y)


        valid_results.append(valid_result)
        test_results.append(test_result)
        best_epochs.append(best_epoch)

    return valid_results, test_results, best_epochs



if __name__ == '__main__':
    parser = argparse.ArgumentParser('tricl unsupervised learning.')
    parser.add_argument('--data', type=str, default='cora_coauth')
    parser.add_argument("--save-emb", dest="save_emb", type=str, default=None)
    parser.add_argument('--model_type', type=str, default='tricl', choices=['tricl_n', 'tricl_ng', 'tricl'])
    parser.add_argument('--num_seeds', type=int, default=20)
    parser.add_argument('--epoch', type=int, default=200)
    parser.add_argument('--device', type=int, default=0)
    parser.add_argument('--task', type=str, default='node', choices=['node', 'edge'])
    args = parser.parse_args()

    params = yaml.safe_load(open('./TriCL/config.yaml'))[args.data]
    print(params)

    data = DatasetLoader().load(args.data).to(args.device)
    args.method="TriCL"
    args.num_features=data.features.shape[1]
    args.num_classes=data.labels.max().item()+1

    fix_seed(0)
    accs = []
    print(data.name)
    print(args)

    if args.task == "node":
        node_splits = data.data_splits
        encoder = HyperEncoder(data.features.shape[1], params['hid_dim'], params['hid_dim'], params['num_layers'])
        model = TriCL(encoder, params['proj_dim']).to(args.device)
        optimizer = torch.optim.AdamW(model.parameters(), lr=params['lr'], weight_decay=params['weight_decay'])
        import time
        for epoch in tqdm(range(1, args.epoch + 1)):
            
            if epoch==1:
                start=time.time()
            if epoch==10:
                end=time.time()
            loss = train(args.model_type, num_negs=None)

        path=f'./time/time.txt'
        with open(path, 'a+') as write_obj:
            write_obj.write(f'{args.data}_{args.method}:{end-start}\n')
        
        with torch.no_grad():
            model.eval() 
            embeds,_=model(data.features,data.hyperedge_index)
        # Table 5(커뮤니티 탐지)용. 경로를 주면 노드 임베딩을 저장만 한다. 안 주면 원래 동작 그대로다.
        if getattr(args, "save_emb", None):
            import pickle as _pickle, os as _os
            _os.makedirs(_os.path.dirname(args.save_emb), exist_ok=True)
            with open(args.save_emb, "wb") as _f:
                _pickle.dump(embeds.detach().cpu().numpy(), _f)
            print("saved embeddings:", args.save_emb)

        valid_results, test_results, epoch_results = node_prediction_linear_eval(args,node_splits,embeds,data)
    else: #edge
        valid_results,test_results=[],[]
        edge_splits=data.edge_splits
        for seed in range(args.num_seeds):
            edge_split=edge_splits[seed]
            data.hyperedge_index=edge_split[3].to(args.device)
            data.num_edges = int(data.hyperedge_index[1].max().item()) + 1
            encoder=HyperEncoder(data.features.shape[1],params['hid_dim'],params['hid_dim'],params['num_layers'])
            model=TriCL(encoder,params['proj_dim']).to(args.device)
            optimizer = torch.optim.AdamW(model.parameters(), lr=params['lr'], weight_decay=params['weight_decay'])

            for epoch in tqdm(range(1, params['epochs'] + 1)):
                loss = train(args.model_type, num_negs=None)
            with torch.no_grad():
                model.eval() 
                embeds,_=model(data.features,data.hyperedge_index)
            valid_result, test_result, _ = edge_prediction_linear_eval(args,edge_split,embeds,data)
            valid_results.append(valid_result[0])
            test_results.append(test_result[0])
    v_acc_mean=np.mean(np.array(valid_results))
    v_acc_std=np.std(np.array(valid_results))


    t_acc_mean=np.mean(np.array(test_results))
    t_acc_std=np.std(np.array(test_results))
    print(f"{args.data} : {t_acc_mean*100:.1f} ± {t_acc_std*100:.1f}")
    
    path=f"./results/pair_{args.data}.txt"
    with open(path, 'a+') as write_obj:
        write_obj.write(f'TriCL=> {test_results} {t_acc_mean*100:.1f} ± {t_acc_std*100:.1f}\n')

    path=f'./results/result_{args.data}_{args.method}_{args.task}.txt'
    with open(path, 'a+') as write_obj:
        write_obj.write(f'{test_results}  {t_acc_mean*100:.1f} ± {t_acc_std*100:.1f}\n')
    
    path=f'./result_small.txt'
    with open(path, 'a+') as write_obj:
        write_obj.write(f'{args.data},{args.method},{t_acc_mean*100:.1f} ± {t_acc_std*100:.1f}\n')

    
