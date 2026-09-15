#!/bin/bash

device=$1


python MaskGAE/MaskGAE_train.py --data citeseer_cite --num_seeds 20 --p 0.5 --alpha 0.002 --lr 0.0001 --device $device --task edge 
python MaskGAE/MaskGAE_train.py --data cora_cite --num_seeds 20 --p 0.75 --alpha 0.003 --lr 0.001 --device $device --task edge 
python MaskGAE/MaskGAE_train.py --data dblp_copub --num_seeds 20 --p 0.75 --alpha 0.003 --lr 0.001 --device $device --task edge 
python MaskGAE/MaskGAE_train.py --data cora_coauth --num_seeds 20 --p 0.5 --alpha 0.003 --lr 0.001 --device $device --task edge 
python MaskGAE/MaskGAE_train.py --data imdb --num_seeds 20 --p 0.25 --alpha 0.001 --lr 0.001 --device $device --task edge 
python MaskGAE/MaskGAE_train.py --data house --num_seeds 20 --p 0.5 --alpha 0.003 --lr 0.01 --device $device --task edge 
python MaskGAE/MaskGAE_train.py --data pubmed_cite --num_seeds 20 --p 0.75 --alpha 0.002 --lr 0.01 --device $device --task edge 
python MaskGAE/MaskGAE_train.py --data dblp_coauth --num_seeds 20 --p 0.75 --alpha 0.001 --lr 0.001 --device $device --task edge 
python MaskGAE/MaskGAE_train.py --data aminer --num_seeds 20 --p 0.75 --alpha 0.001 --lr 0.002 --device $device --task edge 
python MaskGAE/MaskGAE_train.py --data modelnet_40 --num_seeds 20 --p 0.5 --alpha 0.002 --lr 0.01 --device $device --task edge 
python MaskGAE/MaskGAE_train.py --data news --num_seeds 20 --p 0.75 --alpha 0.003 --lr 0.01 --device $device --task edge
