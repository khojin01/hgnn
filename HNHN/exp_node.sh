#!/bin/bash

device=$1

for d in 'citeseer_cite' 'cora_cite' 'dblp_copub' 'cora_coauth' 'imdb' 'house' 'pubmed_cite' 'dblp_coauth' 'aminer' 'modelnet_40' 'news'
do
for a in -3 -2.5 -2.0 -1.5 -1.0 -0.5 0 0.5 
do
for b in -2.5 -2.0 -1.5 -1.0 -0.5 0 0.5 1.0 
do
for lr in 0.05 0.01 0.005 0.001 0.0005 0.0001
do

    python HNHN/HNHN_train.py --data $d --num_seeds 20 --lr $lr --HNHN_alpha $a --HNHN_beta $b --device cuda:$device --task node
done
done
done
done