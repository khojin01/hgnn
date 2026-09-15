#!/bin/bash

device=$1

# python HNHN/HNHN_train.py --data citeseer_cite --num_seeds 1 --lr 0.01 --HNHN_alpha 0 --HNHN_beta 0 --device cuda:$device --task node --epoch 15
# python HNHN/HNHN_train.py --data cora_cite --num_seeds 1 --lr 0.01 --HNHN_alpha -1 --HNHN_beta 0 --device cuda:$device --task node --epoch 15
python HNHN/HNHN_train.py --data dblp_copub --num_seeds 1 --lr 0.001 --HNHN_alpha -2 --HNHN_beta -0.5 --device cuda:$device --task node --epoch 15
python HNHN/HNHN_train.py --data cora_coauth --num_seeds 1 --lr 0.01 --HNHN_alpha -0.5 --HNHN_beta -1.5 --device cuda:$device --task node --epoch 15

python HNHN/HNHN_train.py --data imdb --num_seeds 1 --lr 0.001 --HNHN_alpha 0 --HNHN_beta -1.5 --device cuda:$device --task node --epoch 15
python HNHN/HNHN_train.py --data house --num_seeds 1 --lr 0.001 --HNHN_alpha -2 --HNHN_beta -1 --device cuda:$device --task node --epoch 15
python HNHN/HNHN_train.py --data pubmed_cite --num_seeds 1 --lr 0.01 --HNHN_alpha -3 --HNHN_beta -2.5 --device cuda:$device --task node --epoch 15
python HNHN/HNHN_train.py --data dblp_coauth --num_seeds 1 --lr 0.001 --HNHN_alpha 0 --HNHN_beta -1 --device cuda:$device --task node --epoch 15

python HNHN/HNHN_train.py --data aminer --num_seeds 1 --lr 0.001 --HNHN_alpha 0.5 --HNHN_beta 0 --device cuda:$device --task node --epoch 15
python HNHN/HNHN_train.py --data model_40 --num_seeds 1 --lr 0.01 --HNHN_alpha -3 --HNHN_beta -1 --device cuda:$device --task node --epoch 15
python HNHN/HNHN_train.py --data news --num_seeds 1 --lr 0.001 --HNHN_alpha 0 --HNHN_beta -2.5 --device cuda:$device --task node --epoch 15