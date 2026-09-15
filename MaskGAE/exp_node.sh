#!/bin/bash

device=$1

for d in 'citeseer_cite' 'cora_cite' 'dblp_copub' 'cora_coauth' 'imdb' 'house' 'pubmed_cite' 'dblp_coauth' 'aminer' 'modelnet_40' 'news'
do
for lr in 0.01 0.001 0.0001
do
for alpha in 0.001 0.002 0.003
do
for mask in 0.25 0.5 0.75
do
    python MaskGAE/MaskGAE_train.py --data $d --num_seeds 20 --lr $lr --device $device --task node --alpha $alpha --p $mask
done
done
done
done