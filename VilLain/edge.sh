
gpu=0
dim=128
## cora_cite
num_step=4
num_step_gen=100
lr=0.001
for nl in 2 3 4 5 6 7 8
do
python VilLain/main.py --gpu $gpu --dataset cora_cite --num_step $num_step --num_step_gen $num_step_gen --lr $lr --num_labels $nl --dim $dim --task edge
done
# python VilLain/emb_concat.py --dataset $d --num_step $num_step --num_step_gen $num_step_gen --lr $lr --task edge
# python VilLain/eval.py --data $d --num_step $num_step --num_step_gen $num_step_gen --lr $lr --device $gpu --task edge

# citeseer_cite
lr=0.0001
for nl in 2 3 4 5 6 7 8
do
python VilLain/main.py --gpu $gpu --dataset citeseer_cite --num_step $num_step --num_step_gen $num_step_gen --lr $lr --num_labels $nl --dim $dim --task edge
done
# python VilLain/emb_concat.py --dataset $d --num_step $num_step --num_step_gen $num_step_gen --lr $lr --task edge
# python VilLain/eval.py --data $d --num_step $num_step --num_step_gen $num_step_gen --lr $lr --device $gpu --task edge

# cora_coauth
lr=0.001
for nl in 2 3 4 5 6 7 8
do
python VilLain/main.py --gpu $gpu --dataset cora_coauth --num_step $num_step --num_step_gen $num_step_gen --lr $lr --num_labels $nl --dim $dim --task edge
done
# python VilLain/emb_concat.py --dataset $d --num_step $num_step --num_step_gen $num_step_gen --lr $lr --task edge
# python VilLain/eval.py --data $d --num_step $num_step --num_step_gen $num_step_gen --lr $lr --device $gpu --task edge

# dblp_copub
lr=0.01
for nl in 2 3 4 5 6 7 8
do
python VilLain/main.py --gpu $gpu --dataset dblp_copub --num_step $num_step --num_step_gen $num_step_gen --lr $lr --num_labels $nl --dim $dim --task edge
done
# python VilLain/emb_concat.py --dataset $d --num_step $num_step --num_step_gen $num_step_gen --lr $lr --task edge
# python VilLain/eval.py --data $d --num_step $num_step --num_step_gen $num_step_gen --lr $lr --device $gpu --task edge


# house
lr=0.0001
for nl in 2 3 4 5 6 7 8
do
python VilLain/main.py --gpu $gpu --dataset house --num_step $num_step --num_step_gen $num_step_gen --lr $lr --num_labels $nl --dim $dim --task edge
done
# python VilLain/emb_concat.py --dataset $d --num_step $num_step --num_step_gen $num_step_gen --lr $lr --task edge
# python VilLain/eval.py --data $d --num_step $num_step --num_step_gen $num_step_gen --lr $lr --device $gpu --task edge

#imdb
lr=0.01
for nl in 2 3 4 5 6 7 8
do
python VilLain/main.py --gpu $gpu --dataset imdb --num_step $num_step --num_step_gen $num_step_gen --lr $lr --num_labels $nl --dim $dim --task edge
done
# python VilLain/emb_concat.py --dataset $d --num_step $num_step --num_step_gen $num_step_gen --lr $lr --task edge
# python VilLain/eval.py --data $d --num_step $num_step --num_step_gen $num_step_gen --lr $lr --device $gpu --task edge

# pubmed_cite
num_step_gen=10
lr=0.0001
for nl in 2 3 4 5 6 7 8
do
python VilLain/main.py --gpu $gpu --dataset pubmed_cite --num_step $num_step --num_step_gen $num_step_gen --lr $lr --num_labels $nl --dim $dim --task edge
done
# python VilLain/emb_concat.py --dataset $d --num_step $num_step --num_step_gen $num_step_gen --lr $lr --task edge
# python VilLain/eval.py --data $d --num_step $num_step --num_step_gen $num_step_gen --lr $lr --device $gpu --task edge



# aminer
num_step_gen=10
lr = 0.01

for nl in 2 3 4 5 6 7 8
do
python VilLain/main.py --gpu $gpu --dataset aminer --num_step $num_step --num_step_gen $num_step_gen --lr $lr --num_labels $nl --dim $dim --task edge
done
# python VilLain/emb_concat.py --dataset $d --num_step $num_step --num_step_gen $num_step_gen --lr $lr --task edge
# python VilLain/eval.py --data $d --num_step $num_step --num_step_gen $num_step_gen --lr $lr --device $gpu --task edge

# dblp_coauth
num_step_gen=100
lr = 0.01

for nl in 2 3 4 5 6 7 8
do
python VilLain/main.py --gpu $gpu --dataset dblp_coauth --num_step $num_step --num_step_gen $num_step_gen --lr $lr --num_labels $nl --dim $dim --task edge
done
# python VilLain/emb_concat.py --dataset $d --num_step $num_step --num_step_gen $num_step_gen --lr $lr --task edge
# python VilLain/eval.py --data $d --num_step $num_step --num_step_gen $num_step_gen --lr $lr --device $gpu --task edge

# modelnet_40
num_step_gen=100
lr = 0.001

for nl in 2 3 4 5 6 7 8
do
python VilLain/main.py --gpu $gpu --dataset modelnet_40 --num_step $num_step --num_step_gen $num_step_gen --lr $lr --num_labels $nl --dim $dim --task edge
done
# python VilLain/emb_concat.py --dataset $d --num_step $num_step --num_step_gen $num_step_gen --lr $lr --task edge
# python VilLain/eval.py --data $d --num_step $num_step --num_step_gen $num_step_gen --lr $lr --device $gpu --task edge

# news
num_step_gen=100
lr = 0.01

for nl in 2 3 4 5 6 7 8
do
python VilLain/main.py --gpu $gpu --dataset news --num_step $num_step --num_step_gen $num_step_gen --lr $lr --num_labels $nl --dim $dim --task edge
done
# python VilLain/emb_concat.py --dataset $d --num_step $num_step --num_step_gen $num_step_gen --lr $lr --task edge
# python VilLain/eval.py --data $d --num_step $num_step --num_step_gen $num_step_gen --lr $lr --device $gpu --task edge

