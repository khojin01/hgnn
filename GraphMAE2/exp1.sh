for d in 'citeseer_cite' 'cora_cite' 'dblp_copub' 'cora_coauth' 'imdb' 'house' 'pubmed_cite' 'dblp_coauth' 'aminer' 'modelnet_40' 'news'
do
for lr in  0.01 0.001 0.0001
do
for mask in 0.25 0.5 0.75
do

    python GraphMAE2/GraphMAE2_train.py --data $d --num_seeds 20 --lr $lr --mask_rate $mask --device 1 --task edge
done
done
done