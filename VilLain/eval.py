import torch
import torch.nn as nn
import numpy as np
import torch.nn.functional as F
import argparse
import random

import yaml
from tqdm import tqdm
import numpy as np
import torch
import torch.nn as nn

from torch_scatter import scatter_add, scatter

from sklearn import metrics
from torchmetrics import AveragePrecision
from torchmetrics.classification import BinaryAccuracy
import pickle
import sys
import os

import copy
from sklearn.decomposition import PCA
EMBS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'embs')

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from loader import DatasetLoader
class MLP(nn.Module) : 
    
    def __init__(self, in_dim, n_class) :
        super(MLP, self).__init__()
        self.linear1 = torch.nn.Linear(in_dim, n_class)
        self.reset_parameters()
        
    def reset_parameters(self):
        self.linear1.reset_parameters()
        
    def forward(self, x) : 
        x = self.linear1(x)
        return x
        
class MLP_HENN(nn.Module) :
    
    def __init__(self, in_dim, hidden_dim, p = 0.5) : 
        super(MLP_HENN, self).__init__() 
        
        self.classifier1 = nn.Linear(in_dim, hidden_dim)
        self.classifier2 = nn.Linear(hidden_dim, 1)
        self.dropouts = nn.Dropout(p = p)
        self.reset_parameters()

    def reset_parameters(self):
        self.classifier1.reset_parameters()
        self.classifier2.reset_parameters()
        
    def forward(self, x, target_nodes, target_ids: list) : 
        # maximum = scatter(src = x[target_nodes, :], index = target_ids, dim = 0, reduce = 'max')
        # minimum = scatter(src = x[target_nodes, :], index = target_ids, dim = 0, reduce = 'min')
        # Z = maximum - minimum
        Z = scatter(src = x[target_nodes, :], index = target_ids, dim = 0, reduce = 'sum')
        Z = (self.classifier1(Z)) # No need of Logits
        Z = torch.relu(Z)
        Z = self.dropouts(Z)
        Z = (self.classifier2(Z)) # No need of Logits
        
        return torch.sigmoid(Z).squeeze(-1) # Edge Prediction Probability
    

def fix_seed(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    random.seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = True

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
    parser.add_argument('--data', type=str, default='cora_cite')
    
    parser.add_argument('--num_seeds', type=int, default=20)
    parser.add_argument('--task', type=str, default="node")
    parser.add_argument('--device', type=int, default=1)
    parser.add_argument("--lr", default=0.01, type=float, help='lr')
    parser.add_argument("--num_step", default=4, type=int, help='k (training)')
    parser.add_argument("--num_step_gen", default=10, type=int, help='k (inference)')
    parser.add_argument("--split", default="0.01", type=str,
                        help="node split file suffix: data/<data>/data_split_<split>.pickle "
                             "(default 0.01 = paper's 1%/1%/98%)")
    args = parser.parse_args()
    
    data = DatasetLoader().load(args.data).to(args.device)
    args.method="VilLain"
    args.num_features=data.features.shape[1]
    args.num_classes=data.labels.max().item()+1

    fix_seed(0)
    accs = []
    print(data.name)
    print(args)


    if args.task in ("node", "cluster"):
        # HyperGC 논문 4장: "we randomly split nodes into training, validation,
        # and test sets with ratios of 1%, 1%, and 98%" — 그 분할이
        # `data_split_0.01.pickle`이고, 저장소의 공용 로더 `dataset.py`도 이걸 읽는다.
        # 이 파일은 한때 `data_split_118.pickle`(10%/10%/80%)을 읽고 있었다. VilLain만
        # 레이블을 10배 더 받아 Table 3 대비가 성립하지 않았다(Cora-CA +25.8%p).
        # 다른 분할로 실험하려면 --split 으로 명시한다. 기본값은 논문 프로토콜이다.
        with open('data/{0}/data_split_{1}.pickle'.format(args.data, args.split), "rb") as f :
            data.data_splits = pickle.load(f)

        node_splits = data.data_splits
        
        embeds_path = os.path.join(EMBS_DIR, f"{args.data}_dim128_ns{args.num_step}_nsg{args.num_step_gen}_lr{args.lr}_merged.pkl")
        with open(embeds_path, "rb") as f:
            embeds = pickle.load(f)
            
        embeds=torch.from_numpy(embeds).to(args.device)
        # Clustering is a separate task.  The previous unconditional branch
        # exited here even for ``--task node``, which made the implemented
        # 20-split linear accuracy evaluator below unreachable.
        if args.task == "cluster":
            from sklearn.cluster import KMeans
            from sklearn.metrics import normalized_mutual_info_score
            node_embeddings=embeds.detach().cpu()
            true_labels = data.labels
            num_classes = len(torch.unique(true_labels))  
            kmeans = KMeans(n_clusters=num_classes, random_state=42, n_init=10)
            pred_labels = kmeans.fit_predict(node_embeddings.numpy())  
            nmi_score = normalized_mutual_info_score(true_labels.detach().cpu().numpy(), pred_labels)
            print(f'data:{args.data}, NMI: {nmi_score*100:.2f}\n')    
            path=f'./results/result_cluster_{args.method}_{args.task}.txt'
            with open(path, 'a+') as write_obj:
                write_obj.write(f'data:{args.data}, NMI: {nmi_score*100:.2f}\n')
            raise SystemExit(0)
                
            
            
        valid_results, test_results, epoch_results = node_prediction_linear_eval(args,node_splits,embeds,data)
    else: # edge: consume the split-specific embeddings written by main.py
        valid_results, test_results = [], []
        edge_splits = data.edge_splits
        for seed in range(args.num_seeds):
            embed_files = [
                os.path.join(
                    EMBS_DIR,
                    'edge',
                    f'split{seed}_{args.data}_dim128_nl{num_labels}_ns{args.num_step}_nsg{args.num_step_gen}_lr{args.lr}.pkl',
                )
                for num_labels in range(2, 9)
            ]
            missing_files = [path for path in embed_files if not os.path.isfile(path)]
            if missing_files:
                raise FileNotFoundError(
                    f'VilLain split {seed} requires exactly nl2..8 embeddings; '
                    f'missing: {missing_files}'
                )

            split_embeds = []
            for embed_file in embed_files:
                with open(embed_file, 'rb') as f:
                    split_embeds.append(pickle.load(f)[:, :128])
            merged = np.concatenate(split_embeds, axis=1)
            n_components = min(128, merged.shape[0], merged.shape[1])
            merged = PCA(n_components=n_components).fit_transform(merged)
            embeds = torch.from_numpy(merged).float().to(args.device)

            edge_split = edge_splits[seed]
            valid_result, test_result, _ = edge_prediction_linear_eval(
                args, edge_split, embeds, data
            )
            valid_results.append(valid_result[0])
            test_results.append(test_result[0])
    v_acc_mean=np.mean(np.array(valid_results))
    v_acc_std=np.std(np.array(valid_results))


    t_acc_mean=np.mean(np.array(test_results))
    t_acc_std=np.std(np.array(test_results))
    config = 'lr{}'.format(args.lr)
    path = (f'./results/result_{args.data}_{args.method}_edge.txt'
            if args.task == 'edge' else f'./results/result_{args.method}_{args.task}.txt')
    with open(path, 'a+') as write_obj:
        split_results = [float(value) for value in test_results]
        write_obj.write(
            f'{args.data}{config}_{split_results},'
            f'{t_acc_mean*100:.1f} ± {t_acc_std*100:.1f}\n'
        )
    print(f"{t_acc_mean*100:.1f} ± {t_acc_std*100:.1f}")
    args.method="VilLain"
    path=f'./results/result_118.txt'
    with open(path, 'a+') as write_obj:
        write_obj.write(f'{args.data},{args.method},{t_acc_mean*100:.1f} ± {t_acc_std*100:.1f}\n')
