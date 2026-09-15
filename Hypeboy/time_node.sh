#!/bin/bash

device=$1

for d in 'dblp_copub' 'cora_coauth' 'imdb' 'house' 'pubmed_cite' 'dblp_coauth' 'aminer' 'modelnet_40' 'news' 'citeseer_cite' 'cora_cite' 
do 
python Hypeboy/Hypeboy_train.py --data $d --task node --device cuda:$device
done