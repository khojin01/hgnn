#!/bin/bash


# device=$1
python HyperGRL/HyperGRL_train.py --data cora_cite --num_seeds 1
python HyperGRL/HyperGRL_train.py --data dblp_copub --num_seeds 1
python HyperGRL/HyperGRL_train.py --data cora_coauth --num_seeds 1


python HyperGRL/HyperGRL_train.py --data house --num_seeds 1