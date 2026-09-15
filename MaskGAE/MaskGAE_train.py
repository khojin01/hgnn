import argparse
import numpy as np
import random
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch_geometric.transforms as T
from tqdm.auto import tqdm
import sys
import os
import copy
# custom modules
from maskgae.utils import tab_printer, get_dataset
from maskgae.model import MaskGAE, DegreeDecoder, EdgeDecoder, GNNEncoder
from maskgae.mask import MaskEdge, MaskPath
from maskgae.logreg import MLP,MLP_HENN


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
    optimizer=torch.optim.AdamW(classifier.parameters(),lr=lr,weight_decay=1e-6)
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
        classifier = MLP(in_dim=embeds.shape[1],n_class =data.num_classes).to(embeds.device)
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

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", nargs="?", default="imdb", help="Datasets. (default: Cora)")
    parser.add_argument("--mask", nargs="?", default="Path", help="Masking stractegy, `Path`, `Edge` or `None` (default: Path)")

    parser.add_argument("--layer", nargs="?", default="gcn", help="GNN layer, (default: gcn)")
    parser.add_argument("--encoder_activation", nargs="?", default="elu", help="Activation function for GNN encoder, (default: elu)")
    parser.add_argument('--encoder_channels', type=int, default=128, help='Channels of GNN encoder layers. (default: 128)')
    parser.add_argument('--hidden_channels', type=int, default=128, help='Channels of hidden representation. (default: 64)')
    parser.add_argument('--decoder_channels', type=int, default=128, help='Channels of decoder layers. (default: 128)')
    parser.add_argument('--encoder_layers', type=int, default=2, help='Number of layers for encoder. (default: 2)')
    parser.add_argument('--decoder_layers', type=int, default=2, help='Number of layers for decoders. (default: 2)')
    parser.add_argument('--encoder_dropout', type=float, default=0.5, help='Dropout probability of encoder. (default: 0.8)')
    parser.add_argument('--decoder_dropout', type=float, default=0.5, help='Dropout probability of decoder. (default: 0.2)')
    parser.add_argument('--alpha', type=float, default=0., help='loss weight for degree prediction. (default: 0.)')

    parser.add_argument('--lr', type=float, default=0.01, help='Learning rate for training. (default: 0.01)')
    parser.add_argument('--weight_decay', type=float, default=1e-6, help='weight_decay for link prediction training. (default: 5e-5)')
    parser.add_argument('--grad_norm', type=float, default=1.0, help='grad_norm for training. (default: 1.0.)')
    parser.add_argument('--batch_size', type=int, default=2**16, help='Number of batch size for link prediction training. (default: 2**16)')

    parser.add_argument("--start", nargs="?", default="node", help="Which Type to sample starting nodes for random walks, (default: node)")
    parser.add_argument('--p', type=float, default=0.7, help='Mask ratio or sample ratio for MaskEdge/MaskPath')

    parser.add_argument('--bn', action='store_true', help='Whether to use batch normalization for GNN encoder. (default: False)')
    parser.add_argument('--l2_normalize', action='store_true', help='Whether to use l2 normalize output embedding. (default: False)')
    parser.add_argument('--nodeclas_weight_decay', type=float, default=1e-6, help='weight_decay for node classification training. (default: 1e-3)')

    parser.add_argument('--epochs', type=int, default=200, help='Number of training epochs. (default: 500)')
    parser.add_argument('--num_seeds', type=int, default=20, help='Number of runs. (default: 20)')
    parser.add_argument('--eval_period', type=int, default=30, help='(default: 30)')
    parser.add_argument("--device", type=int, default=0)
    parser.add_argument('--full_data', action='store_true', help='Whether to use full data for pretraining. (default: False)')
    parser.add_argument("--task", type=str, default="node")
    args = parser.parse_args()

    data = DatasetLoader().load(args.data).to(args.device)
    data.num_features=data.features.shape[1]
    data.num_classes=data.labels.max().item()+1
    args.method="MaskGAE"
    fix_seed(0)
    accs = []
    print(data.name)
    print(args)

    args.device = f"cuda:{args.device}" if torch.cuda.is_available() else "cpu"
    transform = T.Compose([
    T.ToUndirected(),
    T.ToDevice(args.device)])

    if args.mask == 'Path':
        mask = MaskPath(p=args.p, 
                    num_nodes=data.num_nodes, 
                    start=args.start,
                    walk_length=args.encoder_layers+1)
    elif args.mask == 'Edge':
        mask = MaskEdge(p=args.p)



    if args.task=="node": #node
        graph_data = get_dataset(data,transform=transform)
        node_splits = data.data_splits
        encoder = GNNEncoder(data.num_features, args.encoder_channels, args.hidden_channels,
                     num_layers=args.encoder_layers, dropout=args.encoder_dropout,
                     bn=args.bn, layer=args.layer, activation=args.encoder_activation)

        edge_decoder = EdgeDecoder(args.hidden_channels, args.decoder_channels,
                                num_layers=args.decoder_layers, dropout=args.decoder_dropout)

        degree_decoder = DegreeDecoder(args.hidden_channels, args.decoder_channels,
                                    num_layers=args.decoder_layers, dropout=args.decoder_dropout)


        model = MaskGAE(encoder, edge_decoder, degree_decoder, mask).to(args.device)
        graph_data=graph_data.to(args.device)
        optimizer = torch.optim.Adam(model.parameters(),
                                 lr=args.lr,
                                 weight_decay=args.weight_decay)
    
        import time
        for epoch in tqdm(range(1, 1 + args.epochs)):
            
            if epoch==1:
                start=time.time()
            if epoch==10:
                end=time.time()
            loss = model.train_step(graph_data, optimizer,
                                    alpha=args.alpha, 
                                    batch_size=args.batch_size)
        
        with torch.no_grad():
            model.eval()
            embeds=model.encoder.get_embedding(graph_data.x,graph_data.edge_index)

        valid_results, test_results, epoch_results = node_prediction_linear_eval(args,node_splits,embeds,data)

    else:
        valid_results,test_results=[],[]
        edge_splits = data.edge_splits
        for seed in range(args.num_seeds):
            edge_split=edge_splits[seed]
            data.hyperedge_index=edge_split[3]
            graph_data = get_dataset(data,transform=transform)
            encoder = GNNEncoder(data.num_features, args.encoder_channels, args.hidden_channels,
                     num_layers=args.encoder_layers, dropout=args.encoder_dropout,
                     bn=args.bn, layer=args.layer, activation=args.encoder_activation)

            edge_decoder = EdgeDecoder(args.hidden_channels, args.decoder_channels,
                                    num_layers=args.decoder_layers, dropout=args.decoder_dropout)

            degree_decoder = DegreeDecoder(args.hidden_channels, args.decoder_channels,
                                        num_layers=args.decoder_layers, dropout=args.decoder_dropout)


            model = MaskGAE(encoder, edge_decoder, degree_decoder, mask).to(args.device)
            graph_data=graph_data.to(args.device)
            optimizer = torch.optim.Adam(model.parameters(),
                                    lr=args.lr,
                                    weight_decay=args.weight_decay)
            for epoch in tqdm(range(1, 1 + args.epochs)):

                loss = model.train_step(graph_data, optimizer,
                                        alpha=args.alpha, 
                                        batch_size=args.batch_size)
            with torch.no_grad():
                model.eval()
                embeds=model.encoder.get_embedding(graph_data.x,graph_data.edge_index)
            valid_result, test_result, _ = edge_prediction_linear_eval(args,edge_split,embeds,data)
            valid_results.append(valid_result[0])
            test_results.append(test_result[0])

    v_acc_mean=np.mean(np.array(valid_results))
    v_acc_std=np.std(np.array(valid_results))


    t_acc_mean=np.mean(np.array(test_results))
    t_acc_std=np.std(np.array(test_results))

    path=f'./results/result_{args.data}_{args.method}_{args.task}.txt'
    with open(path, 'a+') as write_obj:
        write_obj.write(f'mask:{args.p}_lr:{args.lr}_lw{args.alpha} = {test_results} => {t_acc_mean*100:.1f} ± {t_acc_std*100:.1f}\n')

    # ``start``/``end`` are only populated by the node-classification path.
    # Edge prediction has already written its metric above, so do not turn a
    # successful 20-seed run into a failed process while writing optional timing.
    if args.task == 'node':
        path=f'./time/time.txt'
        with open(path, 'a+') as write_obj:
            write_obj.write(f'{args.data}_{args.method}:{end-start} acc:({t_acc_mean})\n')
        
    path=f'./results/result_118.txt'
    with open(path, 'a+') as write_obj:
        write_obj.write(f'{args.data},{args.method},{t_acc_mean*100:.1f} ± {t_acc_std*100:.1f}\n')

    path=f'./result_small.txt'
    with open(path, 'a+') as write_obj:
        write_obj.write(f'{args.data},{args.method},{t_acc_mean*100:.1f} ± {t_acc_std*100:.1f}\n')

