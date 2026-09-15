import numpy as np
import torch
import argparse
import warnings
import pickle

from tqdm import tqdm
from HNNs import *
from src import *
import yaml
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from loader import DatasetLoader

if __name__ == "__main__" : 
    
    warnings.filterwarnings("ignore")
    
    parser = argparse.ArgumentParser('Proposed Method.')
    parser.add_argument('-data', '--data', type=str, default='cora_cite')            
    parser.add_argument('-task', '--task', type=str, default='finetuning')
    parser.add_argument('-epoch', '--epoch', type=int, default=200)
    parser.add_argument('--num_seeds', type=int, default=20,
                        help='Number of predefined data splits to evaluate (default: 20).')
    parser.add_argument('-p_x', '--p_x', type=float, default=0.4)
    parser.add_argument('-p_e', '--p_e', type=float, default=0.9)
    parser.add_argument('-device', '--device', type=str, default='cuda:1')
    args = parser.parse_args()
    
    ## Related information
    params=yaml.safe_load(open('./Hypeboy/config.yaml'))[args.data]
    data_name = args.data
    task_name = args.task
    ssl_epoch = params['epoch']
    device = args.device
    p_x = params['p_x']
    p_e = params['p_e']
    data = DatasetLoader().load(args.data).to(args.device)
    ## Loading data
    X = data.features
    H = data.hyperedge_index    
    Y = data.labels
    n_class = int(torch.unique(Y).shape[0])
    with open('./data/{0}/edge_bucket.pickle'.format(data_name), "rb") as f : 
        edge_buckets = pickle.load(f)
    data_splits = data.data_splits
        
    results = []
    fix_seed(0)
    
    if task_name == 'finetuning' : 
        
        required_tools = related_tool(X, H, data_name, device)
            
        encoder = HyperEncoder(in_dim = X.shape[1], edge_dim = 128, node_dim = 128, num_layers=2,
                                   drop_p = 0.5, cached = False).to(device)
        decoder = HyperDecoder(in_dim = 128, edge_dim = X.shape[1], node_dim = X.shape[1], drop_p = 0.5,
                                  num_layers=2, cached = False, device = device).to(device)

        head1 = key_query_mapper(hidden_dim = 128).to(device)
        head2 = key_query_mapper(hidden_dim = 128).to(device) 

        parameters = HypeBoy(X, encoder, decoder, head1, head2, device, required_tools, 
                        lr1 = 0.001, lr2 = 0.001, epoch1 = 300, epoch2 = ssl_epoch, 
                         prob_x1 = 0.5, prob_x2 = p_x, prob_e1 = 0.2, prob_e2 = p_e)
            
        for splits in tqdm(range(20)) : 

            train_idx, valid_idx, test_idx = data_splits[splits]
            encoder.load_state_dict(parameters)
            encoder.train()
            GNN = end2endNN(encoder = encoder, hidden_dim = 128, n_class = n_class).to(device)
            
            valid_acc, test_acc = train_FineTuning(GNN, X, H, Y, train_idx, valid_idx, test_idx, 
                                                   lr = 1e-3, w_decay = 1e-6, epochs = 200)
            
            results.append(test_acc)
        
    elif task_name == 'node' : # Linear evaluation with node classification
                                    
        required_tools = related_tool(X, H, data_name, device)
            
        encoder = HyperEncoder(in_dim = X.shape[1], edge_dim = 128, node_dim = 128, num_layers=2,
                                   drop_p = 0.5, cached = False).to(device)
        decoder = HyperDecoder(in_dim = 128, edge_dim = X.shape[1], node_dim = X.shape[1], drop_p = 0.5,
                                  num_layers=2, cached = False, device = device).to(device)

        head1 = key_query_mapper(hidden_dim = 128).to(device)
        head2 = key_query_mapper(hidden_dim = 128).to(device) 
        import time
        start=time.time()
        parameters = HypeBoy(X, encoder, decoder, head1, head2, device, required_tools, 
                        lr1 = 0.001, lr2 = 0.001, epoch1 = 300, epoch2 = ssl_epoch, 
                         prob_x1 = 0.5, prob_x2 = p_x, prob_e1 = 0.2, prob_e2 = p_e)
        end=time.time()
        time=end-start
        path=f'./results/result_Hypeboy_time.txt'
        with open(path, 'a+') as write_obj:
            write_obj.write(f'{data_name}=> {time}\n')
        for splits in tqdm(range(args.num_seeds)) : 

            train_idx, valid_idx, test_idx = data_splits[splits]
            encoder.load_state_dict(parameters)
            classifier = MLP(in_dim = 128, hidden_dim = 128, n_class = n_class).to(device)
            valid_acc, test_acc = train_MLP(classifier, encoder, X, Y, H, train_idx, valid_idx, test_idx, 
              lr = 1e-3, epochs = 200, w_decay = 1e-6, device = device)
            
            results.append(test_acc)
        
    elif task_name == 'edge' : # Linear evaluation with hyperedge prediction
        
        for splits in tqdm(range(20)) : 
            
            c_buckets = edge_buckets[splits]
            curH = c_buckets[3].to(device)
            required_tools = related_tool(X, curH, data_name, device)
            
            encoder = HyperEncoder(in_dim = X.shape[1], edge_dim = 128, node_dim = 128, num_layers=2,
                                   drop_p = 0.5, cached = False).to(device)
            decoder = HyperDecoder(in_dim = 128, edge_dim = X.shape[1], node_dim = X.shape[1], drop_p = 0.5,
                                      num_layers=2, cached = False, device = device).to(device)

            head1 = key_query_mapper(hidden_dim = 128).to(device)
            head2 = key_query_mapper(hidden_dim = 128).to(device) 

            parameters = HypeBoy(X, encoder, decoder, head1, head2, device, required_tools, 
                            lr1 = 0.001, lr2 = 0.001, epoch1 = 300, epoch2 = ssl_epoch, 
                             prob_x1 = 0.5, prob_x2 = p_x, prob_e1 = 0.2, prob_e2 = p_e)
            
            encoder.load_state_dict(parameters)
            
            with torch.no_grad() : 
                encoder.eval()
                Z = encoder(X, curH, X.shape[0], int(torch.max(curH[1]) + 1))
            
            mlp_model = MLP_HENN(in_dim = Z.shape[1], hidden_dim = 128).to(device)
            
            valid_acc, test_acc = train_HE_predictor(model = mlp_model, X = Z, edge_buckets = c_buckets, 
                                                     lr = 1e-3, epochs = 200, device = device, seed = splits)
            results.append(test_acc)
        
    else : 
        raise TypeError("Wrong task name is given. It should be given one of [finetuning, linear_node, linear_edge]")
    
    print("Data: {0} / Task: {1} / Avg. Perf: {2} / Std. Perf: {3}".format(data_name, task_name, np.mean(results), np.std(results)))
    
    path=f"./results/pair_{args.data}.txt"
    with open(path, 'a+') as write_obj:
        write_obj.write(f'Hypeboy => {results},{np.mean(results)*100:.1f} ± {np.std(results)*100:.1f}\n')

    path=f'./results/result_Hypeboy_{args.task}.txt'
    with open(path, 'a+') as write_obj:
        write_obj.write(f'{data_name}=> {results},{np.mean(results)*100:.1f} ± {np.std(results)*100:.1f}\n')
    path=f'./results/result_{data_name}_Hypeboy_{args.task}.txt'
    with open(path, 'a+') as write_obj:
        write_obj.write(f'{results},{np.mean(results)*100:.1f} ± {np.std(results)*100:.1f}\n')
    args.method="Hypeboy"
    path=f'./result_small.txt'
    with open(path, 'a+') as write_obj:
        write_obj.write(f'{args.data},{args.method},{np.mean(results)*100:.1f} ± {np.std(results)*100:.1f}\n')
