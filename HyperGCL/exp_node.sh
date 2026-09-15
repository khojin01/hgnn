#!/bin/bash

device=$1

for d in 'citeseer_cite' 'cora_cite' 'dblp_copub' 'cora_coauth' 'imdb' 'house' 'pubmed_cite' 'dblp_coauth' 'aminer' 'modelnet_40' 'news'
do
for lr in 0.001 0.01 0.001 0.0001
do

    python HyperGCL/HyperGCL_train.py --data $d --num_seeds 1 --lr $lr --a_l $a_l --cuda $device --task node
done
done






for d in 'citeseer_cite' 'cora_cite' 'dblp_copub' 'cora_coauth' 'imdb' 'house' 'pubmed_cite' 'dblp_coauth' 'aminer' 'modelnet_40' 'news'
do
for a_l in 0.5 1 2
do

    python HyperGCL/HyperGCL_train.py --data $d --num_seeds 1 --lr $lr --a_l $a_l --cuda $device --task node
done
done
