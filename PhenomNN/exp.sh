for d in 'citeseer_cite' 'cora_cite' 'dblp_copub' 'cora_coauth' 'imdb' 'house' 'pubmed_cite' 'dblp_coauth' 'aminer' 'modelnet_40' 'news'
do
for lr in 0.01 0.001 0.0001
do

for lam0 in 10 #0 0.1 0.5 1 5 10 20 50 80
do

for lam1 in 10 #0 0.1 0.5 1 5 10 20 50 80
do

for alp in 0.1 #0.05 0.01 0.1 1
do

for prop_step in 8 #4 8 16
do


    python PhenomNN/PhenomNN_train.py --data $d --num_seeds 20 --lr $lr --device cuda:1 --task node --lam0 $lam0 --lam1 $lam1 --alp $alp --prop_step $prop_step --task node
done
done
done
done
done
done


