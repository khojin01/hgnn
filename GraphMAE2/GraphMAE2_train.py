import logging
import numpy as np
from tqdm import tqdm
import torch
import scipy.sparse as sp
import torch.nn as nn
from utils import (
    build_args,
    create_optimizer,
    set_random_seed,
    TBLogger,
    get_current_lr,
    load_best_configs,
)
from datasets.data_proc import load_small_dataset
from models import build_model
import sys
import os
import random
import numpy as np
from sklearn.metrics import roc_auc_score as auroc
from models.logreg import MLP,MLP_HENN
import copy

from sklearn import metrics
from torchmetrics import AveragePrecision
from torchmetrics.classification import BinaryAccuracy

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


def pretrain(model, graph, feat, optimizer, max_epoch):

    target_nodes = torch.arange(feat.shape[0], device=feat.device, dtype=torch.long)
    epoch_iter = tqdm(range(max_epoch))
    for epoch in tqdm(range(max_epoch)):
        import time
        if epoch==1:
            start=time.time()
        if epoch==10:
            end=time.time()
        model.train()

        loss = model(graph, feat, targets=target_nodes)

        loss_dict = {"loss": loss.item()}
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        epoch_iter.set_description(f"# Epoch {epoch}: train_loss: {loss.item():.4f}")
    path=f'./time/time.txt'
    with open(path, 'a+') as write_obj:
        write_obj.write(f'{args.data}_{args.method}:{end-start}\n')

    return model
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
        

def main(args):
    device = args.device if args.device >= 0 else "cpu"
    dataset_name = args.data
    max_epoch = args.epoch
    num_hidden = 128
    num_layers = 2
    encoder_type = "gcn"
    decoder_type = "gcn"
    replace_rate = args.replace_rate

    loss_fn = args.loss_fn

    lr = args.lr
    weight_decay = 0.000001


    data = DatasetLoader().load(args.data).to(args.device)
    args.num_features=data.features.shape[1]
    args.num_classes=data.labels.max().item()+1
    args.method="GraphMAE2"

    
    
    fix_seed(0)
    accs = []
    print(data.name)
    print(args)
    if args.task=="node": #node
        graph, (num_features, num_classes) = load_small_dataset(data,args)
        node_splits = data.data_splits
        model = build_model(args)
        model.to(device)
        optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=1e-6)
        x=graph.ndata["feat"]
        model = pretrain(model, graph, x, optimizer, max_epoch)
        
        with torch.no_grad():
            model.eval() 
            embeds=model.embed(graph,x)   
        # Table 5(커뮤니티 탐지)용. 경로를 주면 노드 임베딩을 저장만 한다. 안 주면 원래 동작 그대로다.
        if getattr(args, "save_emb", None):
            import pickle as _pickle, os as _os
            _os.makedirs(_os.path.dirname(args.save_emb), exist_ok=True)
            with open(args.save_emb, "wb") as _f:
                _pickle.dump(embeds.detach().cpu().numpy(), _f)
            print("saved embeddings:", args.save_emb)

        valid_results, test_results, epoch_results = node_prediction_linear_eval(args,node_splits,embeds,data)


    elif args.task=="edge":
        valid_results,test_results=[],[]
        edge_splits = data.edge_splits
        for seed in range(args.num_seeds):
            edge_split=edge_splits[seed]
            data.hyperedge_index=edge_split[3]
            graph, (num_features, num_classes) = load_small_dataset(data,args)

            model = build_model(args)
            model.to(device)
            optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=1e-6)
            x=graph.ndata["feat"]
            model = pretrain(model, graph, x, optimizer, max_epoch)
            
            with torch.no_grad():
                model.eval() 
                embeds=model.embed(graph,x)   
            valid_result, test_result, _ = edge_prediction_linear_eval(args,edge_split,embeds,data)
            valid_results.append(valid_result[0])
            test_results.append(test_result[0])

            
    v_acc_mean=np.mean(np.array(valid_results))
    v_acc_std=np.std(np.array(valid_results))


    t_acc_mean=np.mean(np.array(test_results))
    t_acc_std=np.std(np.array(test_results))

    path=f'./results/result_{args.data}_{args.method}_{args.task}.txt'
    with open(path, 'a+') as write_obj:
        write_obj.write(f'mask:{args.mask_rate}_lr:{args.lr}_{test_results}  {t_acc_mean*100:.1f} ± {t_acc_std*100:.1f}\n')
    path=f'./result_small.txt'
    with open(path, 'a+') as write_obj:
        write_obj.write(f'{args.data},{args.method},{t_acc_mean*100:.1f} ± {t_acc_std*100:.1f}\n')
    

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    args = build_args()
    if args.use_cfg:
        args = load_best_configs(args)
    print(args)
    main(args)
