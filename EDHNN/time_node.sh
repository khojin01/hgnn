#!/bin/bash

device=$1

python EDHNN/EDHNN_train.py --data citeseer_cite --lr 0.001 --restart_alpha 0.7 --device cuda:$device --task node --num_seeds 1 --epoch 15
python EDHNN/EDHNN_train.py --data cora_cite --lr 0.01 --restart_alpha 1 --device cuda:$device --task node --num_seeds 1 --epoch 15
python EDHNN/EDHNN_train.py --data dblp_copub --lr 0.01 --restart_alpha 0.9 --device cuda:$device --task node --num_seeds 1 --epoch 15
python EDHNN/EDHNN_train.py --data cora_coauth --lr 0.001 --restart_alpha 0.8 --device cuda:$device --task node --num_seeds 1 --epoch 15

python EDHNN/EDHNN_train.py --data imdb --lr 0.001 --restart_alpha 1 --device cuda:$device --task node --num_seeds 1 --epoch 15
python EDHNN/EDHNN_train.py --data house --lr 0.01 --restart_alpha 1 --device cuda:$device --task node --num_seeds 1 --epoch 15
python EDHNN/EDHNN_train.py --data pubmed_cite --lr 0.01 --restart_alpha 1 --device cuda:$device --task node --num_seeds 1 --epoch 15
python EDHNN/EDHNN_train.py --data dblp_coauth --lr 0.001 --restart_alpha 0.9 --device cuda:$device --task node --num_seeds 1 --epoch 15
python EDHNN/EDHNN_train.py --data aminer --lr 0.01 --restart_alpha 0.9 --device cuda:$device --task node --num_seeds 1 --epoch 15
python EDHNN/EDHNN_train.py --data modelnet_40 --lr 0.01 --restart_alpha 1 --device cuda:$device --task node --num_seeds 1 --epoch 15
python EDHNN/EDHNN_train.py --data news --lr 0.001 --restart_alpha 0.9 --device cuda:$device --task node --num_seeds 1 --epoch 15
