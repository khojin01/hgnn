#!/bin/bash

device=$1

for d in 'citeseer_cite' 'cora_cite' 'dblp_copub' 'cora_coauth' 'imdb' 'house' 'pubmed_cite' 'dblp_coauth' 'aminer' 'modelnet_40' 'news'
do
for lr in 0.01 0.001 0.0001
do
    for rs in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0
    do
    python EDHNN/EDHNN_train.py --data $d --num_seeds 20 --lr $lr --restart_alpha $rs --device cuda:$device --task node
done
done
done