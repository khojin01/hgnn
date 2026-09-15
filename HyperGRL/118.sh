#!/bin/bash


device=$1


# python HyperGRL/hyperGRL_train_our.py --data citeseer_cite  --num_seeds 20 --device cuda:1
# python HyperGRL/hyperGRL_train_our.py --data cora_cite  --num_seeds 20 --device cuda:1

# python HyperGRL/hyperGRL_train_our.py --data dblp_copub --device cuda:1 --num_seeds 20
# python HyperGRL/hyperGRL_train_our.py --data cora_coauth --device cuda:1 --num_seeds 20
# python HyperGRL/hyperGRL_train_our.py --data imdb --device cuda:1 --num_seeds 20
python HyperGRL/hyperGRL_train_our.py --data house --device cuda:1 --num_seeds 20
python HyperGRL/hyperGRL_train_our.py --data pubmed_cite --device cuda:1 --num_seeds 20
python HyperGRL/hyperGRL_train_our.py --data dblp_coauth --device cuda:1 --num_seeds 20
python HyperGRL/hyperGRL_train_our.py --data aminer --device cuda:1 --num_seeds 20
python HyperGRL/hyperGRL_train_our.py --data modelnet_40 --device cuda:1 --num_seeds 20
python HyperGRL/hyperGRL_train_our.py --data news --device cuda:1 --num_seeds 20

