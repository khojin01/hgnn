#!/bin/bash

device=$1

for d in 'news'
do
for px in 0.3
do
for pe in 0.3
do
for lr in 0.01 0.001 0.0001
do
    python H-GD/H-GD_train.py --data $d --num_seeds 20 --device cuda:$device --task node --p_x $px --p_e $pe --lr $lr
done
done
done
done