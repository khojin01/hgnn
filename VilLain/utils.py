import os
import math
import pickle as pkl
import numpy as np
import argparse
from tqdm import tqdm, trange
import torch

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
        
def parse_args():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--dataset", default='cora_cite', type=str, help='dataset')
    parser.add_argument("--gpu", default='1', type=str, help='gpu number')
    
    parser.add_argument("--batch_size", default=50000, type=int, help='batch size')
    parser.add_argument("--epochs", default=5000, type=int, help='number of epochs')
    parser.add_argument("--lr", default=1e-2, type=float, help='learning rate')
    parser.add_argument("--num_seeds", default=20, type=int, help='splits')
    parser.add_argument("--dim", default=128, type=int, help='embedding dimension')
    parser.add_argument("--num_labels", default=2, type=int, help='number of labels')
    parser.add_argument("--tau", default=1.0, type=float, help='softmax temperature')
    
    parser.add_argument("--num_step", default=4, type=int, help='number of steps')
    parser.add_argument("--task", default="node", type=str)
    parser.add_argument("--num_step_gen", default=100, type=int, help='number of steps (generation)')
    
    return parser.parse_args()

def generate_batches(data_size, batch_size, shuffle=True):
    data = np.arange(data_size)
    
    if shuffle:
        np.random.shuffle(data)
    
    batch_num = math.ceil(data_size / batch_size)
    batches = np.split(np.arange(batch_num * batch_size), batch_num)
    batches[-1] = batches[-1][:(data_size - batch_size * (batch_num - 1))]
    
    for i, batch in enumerate(batches):
        batches[i] = [data[j] for j in batch]
        
    return batches
