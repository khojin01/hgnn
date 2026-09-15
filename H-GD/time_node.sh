#!/bin/bash

device=$1

# python H-GD/H-GD_train.py --data citeseer_cite --num_seeds 1 --lr 0.0001 --device cuda:$device --task node --epochs 15 --p_e 0.3 --p_x 0.2 
# python H-GD/H-GD_train.py --data cora_cite --num_seeds 1 --lr 0.0001 --device cuda:$device --task node --epochs 15 --p_e 0.1 --p_x 0.3 
# python H-GD/H-GD_train.py --data dblp_copub --num_seeds 1 --lr 0.0001 --device cuda:$device --task node --epochs 15 --p_e 0.2 --p_x 0.2 
# python H-GD/H-GD_train.py --data cora_coauth --num_seeds 1 --lr 0.0001 --device cuda:$device --task node --epochs 15 --p_e 0.1 --p_x 0.1 
# python H-GD/H-GD_train.py --data imdb --num_seeds 1 --lr 0.001 --device cuda:$device --task node --epochs 15 --p_e 0.2 --p_x 0.1 
# python H-GD/H-GD_train.py --data house --num_seeds 1 --lr 0.0001 --device cuda:$device --task node --epochs 15 --p_e 0.2 --p_x 0.3 
# python H-GD/H-GD_train.py --data pubmed_cite --num_seeds 1 --lr 0.0001 --device cuda:$device --task node --epochs 15 --p_e 0.4 --p_x 0.4 
# python H-GD/H-GD_train.py --data aminer --num_seeds 1 --lr 0.0001 --device cuda:$device --task node --epochs 15 --p_e 0.2 --p_x 0.2 
# python H-GD/H-GD_train.py --data modelnet_40 --num_seeds 1 --lr 0.0001 --device cuda:$device --task node --epochs 15 --p_e 0.2 --p_x 0.2 

python H-GD/H-GD_train.py --data dblp_coauth --num_seeds 1 --lr 0.0001 --device cuda:$device --task node --epochs 15 --p_e 0.2 --p_x 0.2 
python H-GD/H-GD_train.py --data news --num_seeds 1 --lr 0.0001 --device cuda:$device --task node --epochs 15 --p_e 0.2 --p_x 0.2 
