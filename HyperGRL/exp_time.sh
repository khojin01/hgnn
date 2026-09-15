#!/bin/bash


device=$1


# python HyperGRL/hyperGRL_train_our.py --data citeseer_cite --num_seeds 1 --device cuda:$device --epochs 20
# python HyperGRL/hyperGRL_train_our.py --data cora_cite --num_seeds 1 --device cuda:$device --epochs 20

python HyperGRL/hyperGRL_train_our.py --data dblp_copub --device cuda:$device --num_seeds 20 --epochs 15
python HyperGRL/hyperGRL_train_our.py --data cora_coauth --device cuda:$device --num_seeds 20 --epochs 15
python HyperGRL/hyperGRL_train_our.py --data imdb --device cuda:$device --num_seeds 20 --epochs 15
python HyperGRL/hyperGRL_train_our.py --data house --device cuda:$device --num_seeds 20 --epochs 15
python HyperGRL/hyperGRL_train_our.py --data pubmed_cite --device cuda:$device --num_seeds 20 --epochs 15
python HyperGRL/hyperGRL_train_our.py --data dblp_coauth --device cuda:$device --num_seeds 20 --epochs 15
python HyperGRL/hyperGRL_train_our.py --data aminer --device cuda:$device --num_seeds 20 --epochs 15
python HyperGRL/hyperGRL_train_our.py --data modelnet_40 --device cuda:$device --num_seeds 20 --epochs 15
# python HyperGRL/hyperGRL_train_our.py --data news --device cuda:$device --num_seeds 20 --epochs 15

