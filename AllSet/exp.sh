#!/bin/bash

device=$1

for d in 'citeseer_cite' 'cora_cite' 'dblp_copub' 'cora_coauth' 'imdb' 'house' 'pubmed_cite' 'dblp_coauth' 'aminer' 'modelnet_40' 'news'
do
    for lr in 0.05 0.01 0.005 0.001 0.0005 0.0001
    do
        for h in 1 2 4 8
        do
        python AllSet/AllSet_train.py --data $d --num_seeds 20 --lr $lr --heads $h --device cuda:$device --task node
        done
    done
done


