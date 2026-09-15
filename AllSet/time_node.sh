#!/bin/bash

device=$1

# python AllSet/AllSet_train.py --data citeseer_cite --num_seeds 20 --lr 0.001 --heads 8 --device cuda:$device --task node --num_seeds 1 --epoch 15
# python AllSet/AllSet_train.py --data cora_cite --num_seeds 20 --lr 0.001 --heads 2 --device cuda:$device --task node --num_seeds 1 --epoch 15
python AllSet/AllSet_train.py --data dblp_copub --num_seeds 20 --lr 0.001 --heads 2 --device cuda:$device --task node --num_seeds 1 --epoch 15
python AllSet/AllSet_train.py --data cora_coauth --num_seeds 20 --lr 0.001 --heads 4 --device cuda:$device --task node --num_seeds 1 --epoch 15

python AllSet/AllSet_train.py --data imdb --num_seeds 20 --lr 0.001 --heads 8 --device cuda:$device --task node --num_seeds 1 --epoch 15
python AllSet/AllSet_train.py --data house --num_seeds 20 --lr 0.0001 --heads 8 --device cuda:$device --task node --num_seeds 1 --epoch 15
python AllSet/AllSet_train.py --data pubmed_cite --num_seeds 20 --lr 0.001 --heads 8 --device cuda:$device --task node --num_seeds 1 --epoch 15
python AllSet/AllSet_train.py --data dblp_coauth --num_seeds 20 --lr 0.001 --heads 1 --device cuda:$device --task node --num_seeds 1 --epoch 15
python AllSet/AllSet_train.py --data aminer --num_seeds 20 --lr 0.001 --heads 2 --device cuda:$device --task node --num_seeds 1 --epoch 15
python AllSet/AllSet_train.py --data modelnet_40 --num_seeds 20 --lr 0.001 --heads 2 --device cuda:$device --task node --num_seeds 1 --epoch 15
python AllSet/AllSet_train.py --data news --num_seeds 20 --lr 0.001 --heads 8 --device cuda:$device --task node --num_seeds 1 --epoch 15