import argparse
import random
import yaml
from tqdm import tqdm
import numpy as np
import pickle
import torch
import torch.nn as nn
from torch_scatter import scatter_add
from collections import defaultdict
from contrast_loss import cca_loss
from tricl_encoder import HyperEncoder, TriCL
from utils import fix_seed,drop_features, drop_incidence, valid_node_edge_mask, hyperedge_index_masking
from utils import search_k_hop_edge,clique_expansion,save_samples,load_samples
from evaluation import node_classification_eval
from fairaug import orth_proj,balance_hyperedges
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from loader import DatasetLoader

import copy

from torch_scatter import scatter_add, scatter

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
    
class MILNCELoss(nn.Module):
  
    def __init__(self,node_dim,edge_dim,d,tau,beta,batch_size,device,mean=True):
        super(MILNCELoss,self).__init__()
        
        self.d=d
        self.tau=tau 
        self.mean=mean
        self.batch_size=batch_size
        self.beta=torch.tensor(beta).to(device)
        self.disc=nn.Bilinear(node_dim,edge_dim,1).to(device) 
        self.device=device
    
    def f(self,x,tau):
        return torch.exp(x/tau)
    
    def Listwise_loss(self,n,e,hop_hyperedge,hop_hypernode):
        
        score_list=defaultdict(None) 
        for k in hop_hypernode.keys():
            score_list[k]=torch.zeros((hop_hypernode[k].shape[0],k)).to(self.device)
            
        losses=[]

        for k in hop_hypernode.keys():

            num_samples = len(hop_hypernode[k])
            num_batches = (num_samples - 1) // self.batch_size + 1
            indices = torch.arange(0, num_samples)

            for i in range(num_batches):
                
                ids = indices[i * self.batch_size: (i + 1) * self.batch_size] 
                node_idx=hop_hypernode[k][ids]
                anchor=n[node_idx,:] 
                
                anchor=torch.repeat_interleave(anchor.unsqueeze(1),self.d,dim=1)
                
                for j in range(k):
                    
                    contrast_edges_j=hop_hyperedge[k][ids,j]
                    contrast_obj=e[contrast_edges_j,:] # # [batch_size,sample_size,edge_dim]
                    hop_score=self.f(torch.sigmoid(self.disc(anchor,contrast_obj).squeeze()),self.tau).sum(dim=1) 
                    
                    score_list[k][ids,j]=hop_score
                        
        for k in hop_hypernode.keys():
            
            loss_k=torch.zeros(hop_hyperedge[k].shape[0]).to(self.device)
            for j in range(k-1):
                loss_k+=-torch.log(torch.min(score_list[k][:,j]/score_list[k][:,j:].sum(dim=1),self.beta))
            loss_k=loss_k/(k-1)
            losses.append(loss_k)
        
        return torch.cat(losses)
    
    def forward(self,n,e,hop_hyperedge,hop_hypernode):
        
        loss=self.Listwise_loss(n,e,hop_hyperedge,hop_hypernode)
        
        return loss.mean() if self.mean else loss.sum()    
    
def train(model,contrast_model,data,params,hop_hyperedge,hop_hypernode,optimizer,model_type,projection=False):
    
    features, hyperedge_index = data.features, data.hyperedge_index
    num_nodes, num_edges = data.num_nodes, data.num_edges

    model.train()
    optimizer.zero_grad(set_to_none=True)

    # Hypergraph Augmentation
    hyperedge_index1 = drop_incidence(hyperedge_index, args.drop_incidence_rate_1)
    hyperedge_index2 = drop_incidence(hyperedge_index, args.drop_incidence_rate_2)
    x1 = drop_features(features, args.drop_feature_rate_1)
    x2 = drop_features(features, args.drop_feature_rate_2)

    node_mask1, edge_mask1 = valid_node_edge_mask(hyperedge_index1, num_nodes, num_edges)
    node_mask2, edge_mask2 = valid_node_edge_mask(hyperedge_index2, num_nodes, num_edges)
    node_mask = node_mask1 & node_mask2
    edge_mask = edge_mask1 & edge_mask2

    # Encoder
    n1, e1 = model(x1, hyperedge_index1, num_nodes, num_edges)
    n2, e2 = model(x2, hyperedge_index2, num_nodes, num_edges)
    n, e = model(features, hyperedge_index, num_nodes, num_edges)
    
    #n1, n2 = model.node_projection(n1), model.node_projection(n2)
    #e1, e2 = model.edge_projection(e1), model.edge_projection(e2)
    if projection:
        n, e = model.node_projection(n), model.edge_projection(e)
    
    if model_type in ['hssl','hssl_ng','hssl_n']:
        loss_n=cca_loss(n1,n2,num_nodes,args.lambda_n,args.device)
    else:
        loss_n=0
    
    if model_type in ['hssl','hssl_ng']:
        loss_g=cca_loss(e1,e2,num_edges,args.lambda_g,args.device)
    else:
        loss_g=0
    
    if model_type in ['hssl']:
        loss_m=contrast_model(n,e,hop_hyperedge,hop_hypernode)
    else:
        loss_m = 0
    
    loss = loss_n + args.w_g * loss_g + args.w_m * loss_m

    #print(loss_n.item(),loss_g.item(),loss_m.item())
    #print(loss_n.item(),loss_g.item())
    
    loss.backward()
    optimizer.step()
    
    return loss

# Fair variant
def FairHSSL_Training(model,contrast_model,data,args,hop_hyperedge,hop_hypernode,optimizer,model_type,projection=False):
    
    params=model.params

    features, hyperedge_index = data.x, data.hyperedge_index
    orth_features = orth_proj(features,data.sens_idx) 
    num_nodes, num_edges = data.num_nodes, data.num_hyperedges
    
    if hasattr(data,'sens_idx'):
        node_groups = features[:,data.sens_idx] 
        balanced_hyperedge_index = balance_hyperedges(hyperedge_index, node_groups, dname=args.dname) 
        
    for epoch in tqdm(range(1, 200 + 1)):
    
        model.train()
        optimizer.zero_grad(set_to_none=True)
        
        if params['edge_aug'] == 'aos':
            hyperedge_index1=drop_incidence(hyperedge_index, args.drop_incidence_rate_1)
            hyperedge_index2 = drop_incidence(balanced_hyperedge_index, args.drop_incidence_rate_2)
        else:
            hyperedge_index1 = drop_incidence(hyperedge_index, args.drop_incidence_rate_1)
            hyperedge_index2 = drop_incidence(hyperedge_index, args.drop_incidence_rate_2)
        
        # Feature Augmentation
        if args.feat_aug == 'orth_proj':
            x1 =  drop_features(features, args.drop_feature_rate_1) 
            x2 = drop_features(orth_features, args.drop_feature_rate_2)
        else:
            x1 = drop_features(features, args.drop_feature_rate_1)
            x2 = drop_features(features, args.drop_feature_rate_2)

        node_mask1, edge_mask1 = valid_node_edge_mask(hyperedge_index1, num_nodes, num_edges)
        node_mask2, edge_mask2 = valid_node_edge_mask(hyperedge_index2, num_nodes, num_edges)

        # Encoder
        n1, e1 = model(x1, hyperedge_index1, num_nodes, num_edges)
        n2, e2 = model(x2, hyperedge_index2, num_nodes, num_edges)
        n, e = model(features, hyperedge_index, num_nodes, num_edges)
        
        if model_type in ['hssl','hssl_ng','hssl_n']:
            loss_n=cca_loss(n1,n2,num_nodes,args.lambda_n,args.device)
        else:
            loss_n=0
        
        if model_type in ['hssl','hssl_ng']:
            loss_g=cca_loss(e1,e2,num_edges,args.lambda_g,args.device)
        else:
            loss_g=0
        
        if model_type in ['hssl']:
            loss_m=contrast_model(n,e,hop_hyperedge,hop_hypernode)
        else:
            loss_m = 0
        
        loss = loss_n + args.w_g * loss_g + args.w_m * loss_m
        
        loss.backward()
        optimizer.step()

def generate_sample(data,args,seed=0,edge_split=-1):
    
    # clique expansion: node-node adjacency matrix
    clique_index=clique_expansion(data.hyperedge_index)
    hyperedge_index=data.hyperedge_index
    
    neighbor_list=search_k_hop_edge(data,clique_index,hyperedge_index,'cpu',K=args.K)

    np.random.seed(seed)

    sample_list=defaultdict(list)
    for v_i in range(len(neighbor_list)):
        for k in range(len(neighbor_list[v_i])):
            sample_list[v_i].append(np.random.choice(neighbor_list[v_i][k].numpy(),args.d).tolist())
    
    hop_hypernode=dict() 
    hop_hyperedge=dict()

    k_hop_n=np.array(list(map(len,sample_list.values()))) 

    for k in range(args.K+1):
        ids=np.where(k_hop_n==(k+1))[0]
        if len(ids):
            hop_hypernode[k+1]=ids # {2:[...],3:[...]}: ndarray
            
    for k in hop_hypernode.keys():
        hop_hyperedge[k]=torch.tensor([sample_list[i] for i in hop_hypernode[k]])
    
    # if save:
    #     save_samples({'node':hop_hypernode,'edge':hop_hyperedge},data.name,params['K'])
    
    return hop_hypernode,hop_hyperedge


from sklearn import metrics
from torchmetrics import AveragePrecision
from torchmetrics.classification import BinaryAccuracy

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
    max_epoch=500
    h_dim=256

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
            
            if cur_score[0]>valid_score:
                valid_score=cur_score[0]
                param=copy.deepcopy(classifier.state_dict())
                best_epoch=epoch
                valid_results=cur_score
    classifier.load_state_dict(param)
    test_results=HE_evaluator(z=embeds, classifier=classifier, vidx=test_vidx, eidx=test_eidx,label=test_label)

    return valid_results, test_results, best_epoch

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser('SE-HSSL unsupervised learning.')
    parser.add_argument('--dataset', type=str,default="cora_cite")
    parser.add_argument('--model_type', type=str, default='hssl', choices=['hssl'])
    parser.add_argument('--is_fair',type=bool,default=False)
    
    parser.add_argument('--task', type=str, default='edge', choices=['edge','node','cluster'])
    parser.add_argument('--sample_seed', type=str, default=0, choices=['spcl'])
    parser.add_argument('--verbose_iter', type=int, default=50) 
    parser.add_argument('--num_seeds', type=int, default=2)
    parser.add_argument('--num_layers',type=int,default=2)#
    parser.add_argument('--hid_dim',type=int,default=128)#
    parser.add_argument('--proj_dim',type=int,default=128)#
    parser.add_argument('--drop_incidence_rate_1',type=float,default=0.05)
    parser.add_argument('--drop_incidence_rate_2',type=float,default=0.1)
    parser.add_argument('--drop_feature_rate_1',type=float,default=0.05)
    parser.add_argument('--drop_feature_rate_2',type=float,default=0.1)
    parser.add_argument('--tau',type=float,default=0.5)
    parser.add_argument('--tau_n',type=float,default=0.5)
    parser.add_argument('--tau_g',type=float,default=0.5)
    parser.add_argument('--tau_m',type=float,default=1)
    parser.add_argument('--w_g',type=float,default=1)
    parser.add_argument('--w_m',type=float,default=0.01)
    parser.add_argument('--n_epoch',type=int,default=200)#
    parser.add_argument('--lr',type=float,default=0.001)
    parser.add_argument('--weight_decay',type=float,default=0.00001)
    
    parser.add_argument('--lr_lr',type=float,default=0.001)
    parser.add_argument('--lr_wd',type=float,default=0.00001)

    parser.add_argument('--n_ratio',type=float,default=0.45)
    parser.add_argument('--e_ratio',type=float,default=0.45)
    parser.add_argument('--lr_num_epochs',type=int,default=200)#
    parser.add_argument('--lambda_n',type=float,default=0.0017)
    parser.add_argument('--lambda_g',type=float,default=0.025)
    parser.add_argument('--beta',type=float,default=0.5)
    parser.add_argument('--K',type=int,default=1)
    parser.add_argument('--d',type=int,default=10)
    parser.add_argument('--device',type=int,default=1)


        
    args = parser.parse_args()
    args.lr_lr=args.lr
    args.lr_wd=args.weight_decay
    print(args)
    params = yaml.safe_load(open('SEHSSL/config.yaml'))[args.dataset]
    
    data = DatasetLoader().load(args.dataset).to(args.device)

    #sample_dict=load_samples(data.name,params['K'])
    #hop_hypernode,hop_hyperedge=sample_dict['node'],sample_dict['edge']
    # sample_dict=load_samples(args.dataset,params['K'])
    # hop_hypernode,hop_hyperedge=sample_dict['node'],sample_dict['edge']
    
    accs = []

        
    fix_seed(0)
    args.method="SEHSSL"
    if args.task=="node":
        
        hop_hypernode,hop_hyperedge=generate_sample(data,args,seed=args.sample_seed)
        encoder = HyperEncoder(data.features.shape[1], args.hid_dim, args.hid_dim, args.num_layers)
        model = TriCL(encoder, args.proj_dim).to(args.device)
        
        contrast_model=MILNCELoss(args.hid_dim,args.hid_dim,args.d,args.tau,args.beta,params['batch_size'],args.device,mean=False)
        
        optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)

        if args.is_fair:
            FairHSSL_Training(model,contrast_model,data,args,hop_hyperedge,hop_hypernode,optimizer,
                                args.model_type,projection=False)
        else:
            for epoch in tqdm(range(1, args.n_epoch + 1)):
                import time
                print(epoch)
                if epoch==1:
                    start_time = time.time()
                if epoch==10:
                    end_time = time.time()
                    
                
                loss = train(model,contrast_model,data,args,hop_hyperedge,hop_hypernode,optimizer,
                            args.model_type,projection=False)
                
            path=f'./time/time.txt'
            with open(path, 'a+') as write_obj:
                write_obj.write(f'{args.dataset}_{args.method}:{end_time-start_time}\n')
                
        with torch.no_grad():
            model.eval()
            z,_ = model(data.features, data.hyperedge_index) 

        # if True:
        #     from sklearn.cluster import KMeans
        #     from sklearn.metrics import normalized_mutual_info_score
        #     node_embeddings=z.detach().cpu()
        #     true_labels = data.labels
        #     num_classes = len(torch.unique(true_labels))  
        #     kmeans = KMeans(n_clusters=num_classes, random_state=42, n_init=10)
        #     pred_labels = kmeans.fit_predict(node_embeddings.numpy())  
        #     nmi_score = normalized_mutual_info_score(true_labels.detach().cpu().numpy(), pred_labels)
        #     print(f'data:{args.dataset}, NMI: {nmi_score*100:.2f}\n')    
        #     path=f'./results/result_{args.dataset}_{args.method}_{args.task}.txt'
        #     with open(path, 'a+') as write_obj:
        #         write_obj.write(f'data:{args.dataset}, NMI: {nmi_score*100:.2f}\n')
        
            
        acc = node_classification_eval(model,data,num_splits=args.num_seeds,lr=args.lr_lr,max_epoch=200,
                                        lr_weight=args.lr_wd)

        accs.append(acc)
        acc_mean, acc_std = np.mean(acc, axis=0), np.std(acc, axis=0)

        accs = np.array(accs).reshape(-1, 3)
        accs_mean = list(np.mean(accs, axis=0))
        accs_std = list(np.std(accs, axis=0))
        print(f'[Final] dataset: {args.dataset}, test_acc: {accs_mean[2]:.2f}+-{accs_std[2]:.2f}')

        
            

        path=f'./results/result_{args.dataset}_{args.method}_{args.task}.txt'
        with open(path, 'a+') as write_obj:
            write_obj.write(f'{accs_mean[2]:.1f} ± {accs_std[2]:.1f}\n')
        
        path=f'./results/result_118.txt'
        with open(path, 'a+') as write_obj:
            write_obj.write(f'{args.dataset},{args.method},{accs_mean[2]:.1f} ± {accs_std[2]:.1f}\n')

    else:
        valid_results,test_results=[],[]
        edge_splits=data.edge_splits
        for seed in range(args.num_seeds):
            edge_split=edge_splits[seed]
            data.hyperedge_index=edge_split[3].to(args.device)
            data.num_edges = int(data.hyperedge_index[1].max().item()) + 1
            
            hop_hypernode,hop_hyperedge=generate_sample(data,args,seed=args.sample_seed,edge_split=seed)
            encoder = HyperEncoder(data.features.shape[1], args.hid_dim, args.hid_dim, args.num_layers)
            model = TriCL(encoder, args.proj_dim).to(args.device)
            
            contrast_model=MILNCELoss(args.hid_dim,args.hid_dim,args.d,args.tau,args.beta,params['batch_size'],args.device,mean=False)
            
            optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)

            if args.is_fair:
                FairHSSL_Training(model,contrast_model,data,args,hop_hyperedge,hop_hypernode,optimizer,
                                    args.model_type,projection=False)
            else:
                for epoch in tqdm(range(1, 200 + 1)):
                    loss = train(model,contrast_model,data,args,hop_hyperedge,hop_hypernode,optimizer,
                                args.model_type,projection=False)
                

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
        print(f"{args.dataset} : {t_acc_mean*100:.1f} ± {t_acc_std*100:.1f}")

        path=f'./results/result_{args.dataset}_{args.method}_{args.task}.txt'
        with open(path, 'a+') as write_obj:
            split_results = [float(value) for value in test_results]
            write_obj.write(
                f'{args.dataset},{split_results},'
                f'{t_acc_mean*100:.1f} ± {t_acc_std*100:.1f}\n'
            )
