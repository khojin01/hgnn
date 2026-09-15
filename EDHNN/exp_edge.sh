#!/bin/bash

device=$1


python EDHNN/EDHNN_train.py --data citeseer_cite --num_seeds 20 --restart_alpha 0.7 --lr 0.001 --device cuda:$device --task edge 
python EDHNN/EDHNN_train.py --data cora_cite --num_seeds 20 --restart_alpha 1.0 --lr 0.01 --device cuda:$device --task edge 
python EDHNN/EDHNN_train.py --data dblp_copub --num_seeds 20 --restart_alpha 0.9 --lr 0.01 --device cuda:$device --task edge 
python EDHNN/EDHNN_train.py --data cora_coauth --num_seeds 20 --restart_alpha 0.8 --lr 0.001 --device cuda:$device --task edge 
python EDHNN/EDHNN_train.py --data imdb --num_seeds 20 --restart_alpha 1.0 --lr 0.001 --device cuda:$device --task edge 
python EDHNN/EDHNN_train.py --data house --num_seeds 20 --restart_alpha 1.0 --lr 0.01 --device cuda:$device --task edge 
python EDHNN/EDHNN_train.py --data pubmed_cite --num_seeds 20 --restart_alpha 1.0 --lr 0.01 --device cuda:$device --task edge 
python EDHNN/EDHNN_train.py --data dblp_coauth --num_seeds 20 --restart_alpha 0.9 --lr 0.001 --device cuda:$device --task edge 
python EDHNN/EDHNN_train.py --data aminer --num_seeds 20 --restart_alpha 0.9 --lr 0.01 --device cuda:$device --task edge 
python EDHNN/EDHNN_train.py --data modelnet_40 --num_seeds 20 --restart_alpha 1.0 --lr 0.01 --device cuda:$device --task edge 
python EDHNN/EDHNN_train.py --data news --num_seeds 20 --restart_alpha 0.9 --lr 0.001 --device cuda:$device --task edge
