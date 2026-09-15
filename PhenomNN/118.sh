#!/bin/bash

device=$1

python PhenomNN/PhenomNN_train.py --data citeseer_cite --num_seeds 20 --lr 0.01 --device cuda:$device --task node --lam0 10 --lam1 1 --alp 1 --prop_step 16 --task node
python PhenomNN/PhenomNN_train.py --data cora_cite --num_seeds 20 --lr 0.01 --device cuda:$device --task node --lam0 80 --lam1 20 --alp 1 --prop_step 16 --task node
python PhenomNN/PhenomNN_train.py --data dblp_copub --num_seeds 20 --lr 0.01 --device cuda:$device --task node --lam0 0.5 --lam1 20 --alp 1 --prop_step 8 --task node
python PhenomNN/PhenomNN_train.py --data cora_coauth --num_seeds 20 --lr 0.01 --device cuda:$device --task node --lam0 20 --lam1 10 --alp 0.1 --prop_step 8 --task node



python PhenomNN/PhenomNN_train.py --data imdb --num_seeds 20 --lr 0.01 --device cuda:$device --task node --lam0 0 --lam1 5 --alp 0.01 --prop_step 8 --task node
python PhenomNN/PhenomNN_train.py --data house --num_seeds 20 --lr 0.01 --device cuda:$device --task node --lam0 0.01 --lam1 10 --alp 1 --prop_step 8 --task node
python PhenomNN/PhenomNN_train.py --data pubmed_cite --num_seeds 20 --lr 0.01 --device cuda:$device --task node --lam0 10 --lam1 5 --alp 1 --prop_step 16 --task node

python PhenomNN/PhenomNN_train.py --data modelnet_40 --num_seeds 20 --lr 0.01 --device cuda:$device --task node --lam0 10 --lam1 10 --alp 0.1 --prop_step 8 --task node