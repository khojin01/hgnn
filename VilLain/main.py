import os
import copy
import time
import math
import random
import numpy as np
import pickle as pkl
from tqdm import tqdm, trange

import torch
import torch.nn as nn
import torch.optim as optim

import utils
import model
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from loader import DatasetLoader
EPS = 1e-10

args = utils.parse_args()
EMBS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'embs')

##### GPU Settings #####
if torch.cuda.is_available():
    device = torch.device("cuda:" + args.gpu)
else:
    device = torch.device("cpu")
print('Device:\t', device, '\n')

##### Config #####
config = '{}_dim{}_nl{}_ns{}_nsg{}_lr{}'.format(args.dataset, args.dim, args.num_labels, args.num_step, args.num_step_gen,args.lr)
    
##### Random Seed #####
SEED = 0
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
data = DatasetLoader().load(args.dataset).to(device)
##### Read Data #####
if args.task=="node":
    H, labels, features = data.hyperedge_index, data.labels,data.features
    #utils.load(args.dataset)
    #labels = labels.tolist()
    #feature_dim = features.shape[1]

    V_idx, E_idx = H[0].to(device), H[1].to(device)
    V, E = torch.max(V_idx)+1, torch.max(E_idx)+1

    print('V = {}\tE = {}'.format(V,E))
    print('Sparsity = {}'.format(len(V_idx)/(V*E)))
        
    ################################################################################

    num_subspace = math.ceil(args.dim / args.num_labels)
        
    ##### Prepare Training #####
    our_model = model.model(V_idx, E_idx, V, E, num_subspace, args.num_labels, args.num_step, args.num_step_gen).to(device)
    optimizer = optim.AdamW(our_model.parameters(), lr=args.lr, weight_decay=0)

    ##### Train Model #####
        
    best_loss, best_model = 1e10, None
    pre_loss, patience = 1e10, 20
    for epoch in range(1, args.epochs+1):
        import time
        if epoch==1:
            start_time = time.time()
        if epoch==10:
            end_time = time.time()
            
    
                
        our_model.train()

        loss_local, loss_global = our_model()
        loss = loss_local + loss_global

        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(our_model.parameters(), 1.0)
        optimizer.step()

        if epoch % 10 == 0:
            print('{}\t{}\t{}'.format(epoch, loss_local.item(), loss_global.item()))
            with open('logs/{}.txt'.format(config), 'a') as f:
                f.write('Epoch {}\tLocal {}\tGlobal {}\n'.format(epoch, loss_local.item(), loss_global.item()))
        
        if loss.item() < best_loss:
            our_model.eval()
            best_loss = loss.item()
            best_model = copy.deepcopy(our_model.state_dict())

        if epoch <= 1000:
            continue

        diff = abs(loss.item() - pre_loss) / abs(pre_loss)
        if diff < 0.002:
            cnt_wait += 1
        else:
            cnt_wait = 0
                
        if cnt_wait == patience:
            break
            
        pre_loss = loss.item()


    path=f'./time/time.txt'
    with open(path, 'a+') as write_obj:
        write_obj.write(f'{args.dataset}_VilLain{args.num_labels}:{end_time-start_time}\n')

    # Process the embedding
    our_model.load_state_dict(best_model)

    embs = our_model.get_node_embeds().detach().cpu().numpy()
    

    with open(os.path.join(EMBS_DIR, '{}.pkl'.format(config)), 'wb') as f:
        pkl.dump(embs, f)

else:
    edge_splits=data.edge_splits
    for seed in range(args.num_seeds):
        edge_split=edge_splits[seed]
        data.hyperedge_index=edge_split[3]
        H, labels, features = data.hyperedge_index, data.labels,data.features
#utils.load(args.dataset)
#labels = labels.tolist()
#feature_dim = features.shape[1]

        V_idx, E_idx = H[0].to(device), H[1].to(device)
        V, E = torch.max(V_idx)+1, torch.max(E_idx)+1

        print('V = {}\tE = {}'.format(V,E))
        print('Sparsity = {}'.format(len(V_idx)/(V*E)))
            
        ################################################################################

        num_subspace = math.ceil(args.dim / args.num_labels)
            
        ##### Prepare Training #####
        our_model = model.model(V_idx, E_idx, V, E, num_subspace, args.num_labels, args.num_step, args.num_step_gen).to(device)
        optimizer = optim.AdamW(our_model.parameters(), lr=args.lr, weight_decay=0)

        ##### Train Model #####
            
        best_loss, best_model = 1e10, None
        pre_loss, patience = 1e10, 20

        for epoch in range(1, args.epochs+1):
            our_model.train()

            loss_local, loss_global = our_model()
            loss = loss_local + loss_global

            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(our_model.parameters(), 1.0)
            optimizer.step()

            if epoch % 10 == 0:
                print('{}\t{}\t{}'.format(epoch, loss_local.item(), loss_global.item()))
                with open('logs/{}.txt'.format(config), 'a') as f:
                    f.write('Epoch {}\tLocal {}\tGlobal {}\n'.format(epoch, loss_local.item(), loss_global.item()))
            
            if loss.item() < best_loss:
                our_model.eval()
                best_loss = loss.item()
                best_model = copy.deepcopy(our_model.state_dict())

            if epoch <= 1000:
                continue

            diff = abs(loss.item() - pre_loss) / abs(pre_loss)
            if diff < 0.002:
                cnt_wait += 1
            else:
                cnt_wait = 0
                    
            if cnt_wait == patience:
                break
                
            pre_loss = loss.item()


        # Process the embedding
        our_model.load_state_dict(best_model)

        embs = our_model.get_node_embeds().detach().cpu().numpy()

        with open(os.path.join(EMBS_DIR, 'edge', 'split{}_{}.pkl'.format(seed, config)), 'wb') as f:
            pkl.dump(embs, f)
