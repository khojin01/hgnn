#!/bin/bash

device=$1

# python GraphMAE2/GraphMAE2_train.py --data citeseer_cite --num_seeds 1 --lr 0.0001 --mask_rate 0.5 --device $device --task node --epoch 15
# python GraphMAE2/GraphMAE2_train.py --data cora_cite --num_seeds 1 --lr 0.001 --mask_rate 0.25 --device $device --task node --epoch 15
python GraphMAE2/GraphMAE2_train.py --data dblp_copub --num_seeds 1 --lr 0.001 --mask_rate 0.75 --device $device --task node --epoch 15
python GraphMAE2/GraphMAE2_train.py --data cora_coauth --num_seeds 1 --lr 0.0001 --mask_rate 0.5 --device $device --task node --epoch 15


python GraphMAE2/GraphMAE2_train.py --data imdb --num_seeds 1 --lr 0.001 --mask_rate 0.75 --device $device --task node --epoch 15
python GraphMAE2/GraphMAE2_train.py --data house --num_seeds 1 --lr 0.0001 --mask_rate 0.5 --device $device --task node --epoch 15
python GraphMAE2/GraphMAE2_train.py --data pubmed_cite --num_seeds 1 --lr 0.01 --mask_rate 0.5 --device $device --task node --epoch 15
python GraphMAE2/GraphMAE2_train.py --data dblp_coauth --num_seeds 1 --lr 0.001 --mask_rate 0.5 --device $device --task node --epoch 15

python GraphMAE2/GraphMAE2_train.py --data aminer --num_seeds 1 --lr 0.0001 --mask_rate 0.5 --device $device --task node --epoch 15
python GraphMAE2/GraphMAE2_train.py --data modelnet_40 --num_seeds 1 --lr 0.001 --mask_rate 0.25 --device $device --task node --epoch 15

python GraphMAE2/GraphMAE2_train.py --data news --num_seeds 1 --lr 0.001 --mask_rate 0.5 --device $device --task node --epoch 15



python GraphMAE2/GraphMAE2_train.py --data pubmed_cite --num_seeds 20 --lr 0.01 --mask_rate 0.5 --device 0 --task edge --epoch 200