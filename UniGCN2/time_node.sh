#!/bin/bash

device=$1


# python UniGCN2/UniGCN2_train.py --data citeseer_cite --num_seeds 1 --lr 0.001 --device cuda:$device --task node --epoch 15
# python UniGCN2/UniGCN2_train.py --data cora_cite --num_seeds 1 --lr 0.01 --device cuda:$device --task node --epoch 15
python UniGCN2/UniGCN2_train.py --data dblp_copub --num_seeds 1 --lr 0.01 --device cuda:$device --task node --epoch 15
python UniGCN2/UniGCN2_train.py --data cora_coauth --num_seeds 1 --lr 0.001 --device cuda:$device --task node --epoch 15
python UniGCN2/UniGCN2_train.py --data imdb --num_seeds 1 --lr 0.01 --device cuda:$device --task node --epoch 15
python UniGCN2/UniGCN2_train.py --data house --num_seeds 1 --lr 0.01 --device cuda:$device --task node --epoch 15
python UniGCN2/UniGCN2_train.py --data pubmed_cite --num_seeds 1 --lr 0.001 --device cuda:$device --task node --epoch 15
python UniGCN2/UniGCN2_train.py --data dblp_coauth --num_seeds 1 --lr 0.001 --device cuda:$device --task node --epoch 15
python UniGCN2/UniGCN2_train.py --data aminer --num_seeds 1 --lr 0.001 --device cuda:$device --task node --epoch 15
python UniGCN2/UniGCN2_train.py --data modelnet_40 --num_seeds 1 --lr 0.001 --device cuda:$device --task node --epoch 15
python UniGCN2/UniGCN2_train.py --data news --num_seeds 1 --lr 0.001 --device cuda:$device --task node --epoch 15
