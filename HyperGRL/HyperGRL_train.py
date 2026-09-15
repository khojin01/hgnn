import sys
import pickle
from sklearn.model_selection import train_test_split
import networkx as nx
import dgl
from sklearn.utils import shuffle
import torch as th
from timeit import default_timer as timer
import argparse
import torch
import torch.nn as nn
from dgl import batch
# import nxmetis
from sklearn.metrics import accuracy_score
import itertools
from tqdm import tqdm
import os.path
from os import path
import pymetis
import pandas as pd
# pd.set_option('display.max_columns', 10)
# pd.set_option('display.width', 1000)


import random
import numpy as np
from sklearn.metrics import roc_auc_score as auroc
from logreg import MLP,MLP_HENN
import copy


from sklearn import metrics
from torchmetrics import AveragePrecision
from torchmetrics.classification import BinaryAccuracy
import time


import numpy as np
import hyperedge_clique
from collections import Counter
import random
from collections import defaultdict
from itertools import combinations
from torch.utils.data import DataLoader
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

def getPretrainData(task,hyperedges, pretrain_task, cluster_number=20, pretext_classification=True):
    node_list = list(hyperedges.keys())
    if pretrain_task == 'dis2cluster':
        hyperedge_list = []
        g_hyperedge = nx.Graph()
        g_hyperedge.add_nodes_from(node_list)

        for h1 in tqdm(hyperedges):
            for h2 in hyperedges:
                if h1 != h2:
                    overlap_nodes = set(hyperedges[h1]["members"]) & set(hyperedges[h2]["members"])
                    if overlap_nodes:
                        weight = len(overlap_nodes)
                        g_hyperedge.add_edge(h1, h2, weight=weight)
        # (clique expansion
        #############################################################
        nodes = list(g_hyperedge.nodes())
        node_to_idx = {node: idx for idx, node in enumerate(nodes)}
        idx_to_node = {idx: node for node, idx in node_to_idx.items()}

        # adjacency list 만들기
        adjacency = [[] for _ in nodes]
        for u in g_hyperedge.nodes():
            u_idx = node_to_idx[u]
            for v in g_hyperedge.neighbors(u):
                v_idx = node_to_idx[v]
                adjacency[u_idx].append(v_idx)

        # 파티셔닝
        st, membership = pymetis.part_graph(cluster_number, adjacency=adjacency)

        # membership은 각 인덱스(노드)에 대해 몇 번째 파트에 속하는지 알려줌
        # 만약 원래 노드 이름이 필요하면 parts에 매핑
        parts = [[] for _ in range(cluster_number)]
        for idx, part_id in enumerate(membership):
            parts[part_id].append(idx_to_node[idx])
        #################################################################################
        if pretext_classification:
            cluster_membership = {node: membership for node, membership in enumerate(parts)}
            reversed_membership = {}
            for key in cluster_membership:  # key = 클러스터 번호
                for member in cluster_membership[key]:  # member = 노드 이름
                    if member not in reversed_membership:
                        reversed_membership[member] = key
            # with open('./g_hyperedge.p', 'wb') as fp:
            #     pickle.dump(g_hyperedge, fp)
            # with open('./reversed_membership.p', 'wb') as fp:
            #     pickle.dump(reversed_membership, fp)
            return reversed_membership, g_hyperedge
        else: # TODO: output the dict of hyperedges with distance to the centroids
            pass
    elif pretrain_task == 'dis2hyperedges':
        pass # TODO
    else:
        print('Wrong pretext_task type!')
        return True
    

def getData(device,hyperedges, node_features, node_ids, model_to_use, cluster_membership, g_hyperedge, cluster_num, rw_feat=False, ori_feat=False):
    # method 1: clique expansion. Output: list of cliques (dgl graphs) and list of labels
    if model_to_use == 'hyperedge_clique' or model_to_use == 'hyperedge_tree':
        i = 0
        lists = []
        labels_pre = []
        labels = []
        label_set = set()
        for h in hyperedges:
            if h in list(g_hyperedge.nodes):
                label_set.add(hyperedges[h]["category"])
        num_categories = len(label_set)
        for h in tqdm(hyperedges):
            if h in list(g_hyperedge.nodes):
                vertex_embedding_list = []
                hyperedge = hyperedges[h]
                g_nx = nx.complete_graph(len(hyperedge["members"]))
                for vertex in hyperedge["members"]:
                    i += 1
                    if i % 100000 == 0:
                        print(i)
                    try:
                        if rw_feat:
                            vertex_embedding_list.append(th.tensor(node_features[node_ids.index(vertex)].tolist()))
                        if ori_feat:
                            vertex_embedding_list.append(th.tensor(node_features[vertex].tolist()))
                    except:
                        print("Missed one: ", vertex)
                node_attr_dict = dict(zip(list(range(len(hyperedge["members"]))), vertex_embedding_list))
                nx.set_node_attributes(g_nx, node_attr_dict, 'node_attr')
                # g = dgl.DGLGraph()
                # g.from_networkx(g_nx, node_attrs=['node_attr']) # For dgl < 0.5.x
                g = dgl.from_networkx(g_nx, node_attrs=['node_attr']).to(device) # For dgl 0.5.x
                lists.append(g)

                ## Use categorical labels
                labels.append(int(hyperedge["category"]))
                # labels.append(int(hyperedge["category"]))
                labels_pre.append(int(cluster_membership[h]))

        X, Y, Y_pre = lists, labels, labels_pre


        return X, Y, Y_pre, num_categories
    else:
        print('Wrong model name!')
        return


if __name__ == '__main__':
    
    # Training settings
    parser = argparse.ArgumentParser()
    # Training parameter
    parser.add_argument('--alpha', type=float, default=1, help='alpha for joint training')
    parser.add_argument('--beta', type=float, default=1, help='beta for joint training')
    parser.add_argument('--cluster_num', type=int, default=10, help='number of clusters when using dis2cluster')
    parser.add_argument('--device', type=str,default="cuda:1")
    parser.add_argument('--epochs', type=int, default=15,
                        help='Number of epochs to train.')
    parser.add_argument('--num_seeds', type=int, default=1,
                        help='Number of epochs to train.')
    parser.add_argument('--lr', type=float, default=0.001,
                        help='Learning rate.')
    parser.add_argument('--n_negative', type=int, default=8,
                        help='number of negative examples in node-level self-supervised training.')
    parser.add_argument('--data', default="cora_cite")
    parser.add_argument('--theta',type=float,default=0.1)

    parser.add_argument('--hidden_dim', type=int, default=128,
                        help='Number of hidden units.')
    parser.add_argument("--train_mode", default="pretrain_n_e", help="The training mode. 'separate', 'joint', 'pretrain_n', "
                                                                "'pretrain_e', 'pretrain_n_e'")

    args = parser.parse_args()

    data = DatasetLoader().load(args.data).to(args.device)
    args.method="HyperGRL"
    args.num_features=data.features.shape[1]
    args.num_classes=data.labels.max().item()+1

    rows,cols=data.hyperedge_index[0],data.hyperedge_index[1]
    hyperedge_dict = defaultdict(list)
    for node, hedge in zip(rows, cols):
        hyperedge_dict[int(hedge)].append(int(node))

    # clique 확장
    edge_dict = defaultdict(set)
    for nodes in hyperedge_dict.values():
        for u, v in combinations(nodes, 2):
            edge_dict[u].add(v)
            edge_dict[v].add(u)
    hyperedges={}

    for k,v in edge_dict.items():
        hyperedges[k]={'members':list(v), 'category':data.labels[k].item()}
    node_id = list(range(data.num_nodes))
    fix_seed(0)
    print(data.name)
    print(args)
    result=[]
    if True: #node
        node_splits = data.data_splits
        args.task="node"
        model_to_use='hyperedge_clique'
        membership, g_hyperedge = getPretrainData(args.task,hyperedges, 'dis2cluster', cluster_number=args.cluster_num,pretext_classification=True)
        X, Y, Y_pre, num_categories = getData(args.device,hyperedges, data.features, node_id, model_to_use, membership, g_hyperedge,args.cluster_num, ori_feat=True, rw_feat=False)
        X_t_v, X_test, Y_t_v, Y_test, Y_pre_t_v, Y_pre_test = train_test_split(X, Y, Y_pre, train_size=args.theta, test_size=round(1-args.theta,1))
        X_train, X_vali, Y_train, Y_vali, Y_pre_train, Y_pre_vali = train_test_split(X_t_v, Y_t_v, Y_pre_t_v,
                                                                                    train_size=0.1, test_size=0.8)
        print("get data")
        for seed in range(args.num_seeds):
            

            Y_train_counter = Counter(Y_train)
            print('Hyperedge classification training data statistics:', Y_train_counter)
            weights_tune_loss = []
            for i in range(num_categories):
                weights_tune_loss.append(Y_train_counter[i])
            weights_tune_loss = [1 - (weight / sum(weights_tune_loss)) for weight in weights_tune_loss]

            Y_train_counter = Counter(Y_pre_train)
            print('Self-training clustering statistics:', Y_train_counter)
            weights_pre_loss = []
            for i in range(len(Y_train_counter)):
                weights_pre_loss.append(Y_train_counter[i])
            weights_pre_loss = [1 - (weight / sum(weights_pre_loss)) for weight in weights_pre_loss]

            if model_to_use == 'hyperedge_clique':
                scorer = hyperedge_clique.HyperScorerGeneral(input_dim=args.num_features, hidden_size=args.hidden_dim, num_class=num_categories,
                                                        n_epochs=args.epochs, weight_tune=weights_tune_loss,
                                                        cluster_num=args.cluster_num, weight_pre=weights_pre_loss,
                                                        n_negative=args.n_negative, lr=args.lr, device=args.device)


            # Train graph scorer
            print("Training graph scorer")
            start_train_clustrer = timer()
            if model_to_use == 'hyperedge_clique' or model_to_use == 'hyperedge_tree':
                scorer.train(args.data, g_list_train=X_train, labels_train_tune=Y_train, labels_train_pre=Y_pre_train, g_list_validation=X_vali,
                        labels_validation_tune=Y_vali, labels_validation_pre=Y_pre_vali, eval_metric=accuracy_score, alpha=1,
                        train_mode='pretrain', pretrain_node=True, pretrain_he=True, joint=False)

            print('FINISHED training graph scorer in', round(timer() - start_train_clustrer, 2), 'seconds')
            batch_size=500
            num_batches=data.num_nodes//batch_size+1
            total_node=[]
            # for batch in tqdm(range(num_batches)):
            #     if (batch+1)*batch_size>=data.num_nodes:
            #         Y=X[batch*batch_size:]
            #     else:
            #         Y=X[batch*batch_size:(batch+1)*batch_size]
            #     _ , embed = scorer.predict_labels(Y)
            #     node_i=embed.tolist()
            #     total_node+=node_i
            # # path=f"./HyperGRL/embeds/HyperGRL_{args.data}"
            # th.save(th.tensor(total_node),path)
            # print(f"저장! 전체노드:{data.num_nodes}, 임베딩된 노드{th.tensor(total_node).shape}")
            # Performance on validation set:
            start_test_performance = timer()
            predicted_labels = scorer.predict_labels(X_vali)
            Y_vali = np.array(Y_vali)
            vali_label_list = []
            predict_label_list = []
            for i in range(Y_vali.shape[0]):
                if len(np.where(predicted_labels[i] == 1)[0]) > 0:
                    predict_label_list.append(np.where(predicted_labels[i] == 1)[0][0])
                else:
                    predict_label_list.append(-1)
                vali_label_list.append(Y_vali[i])

            validation_score = accuracy_score(vali_label_list, predict_label_list)
            print('vali score: ', validation_score)
            print("FINISHED computing performance on validation set in", round(timer() - start_test_performance, 4), 'seconds')

            # Performance on test set:
            start_test_performance = timer()
            predicted_labels = scorer.predict_labels(X_test)
            Y_test = np.array(Y_test)
            test_label_list = []
            predict_label_list = []
            for i in range(Y_test.shape[0]):
                if len(np.where(predicted_labels[i] == 1)[0]) > 0:
                    predict_label_list.append(np.where(predicted_labels[i] == 1)[0][0])
                else:
                    predict_label_list.append(-1)
                test_label_list.append(Y_test[i])
            test_score = accuracy_score(test_label_list, predict_label_list)
            naive_score = accuracy_score(test_label_list, np.zeros(len(predict_label_list)).tolist())
            print('test score: ', test_score)
            print('naive score: ', naive_score)
            print("FINISHED computing performance on test set in", round(timer() - start_test_performance, 4), 'seconds')

            result.append(test_score)
        

            
        path=f'./results/result_{args.data}_HyperGRL_node.txt'
        test=np.array(result)
        print(f'{test.mean()*100:.1f} ± {test.std()*100:.1f}')
        with open(path, 'a+') as write_obj:
            write_obj.write(f'{test},{test.mean()*100:.1f} ± {test.std()*100:.1f}\n')