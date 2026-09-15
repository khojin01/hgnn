gpu=1

dim=128


num_step=4
num_step_gen=10
for d in "cora_cite" "citeseer_cite" "cora_coauth" "dblp_copub" "house" "imdb" "pubmed_cite" "aminer" "dblp_coauth" "modelnet_40" "news"
do
for nl in 2 3 4 5 6 7 8
do
for lr in 0.01 0.001 0.0001
do
    python VilLain/main.py --gpu $gpu --dataset $d --num_step $num_step --num_step_gen $num_step_gen --lr $lr --num_labels $nl --dim $dim
    python VilLain/emb_concat.py --dataset $d --num_step $num_step --num_step_gen $num_step_gen --lr $lr
    python VilLain/eval.py --data $d --num_step $num_step --num_step_gen $num_step_gen --lr $lr --device $gpu
done
done
done
python VilLain/emb_concat.py --dataset $d --num_step $num_step --num_step_gen $num_step_gen
num_step_gen=100
for d in "citeseer_cite" "dblp_copub" "cora_coauth" #"house" "imdb" "pubmed_cite" "aminer" "dblp_coauth" "modelnet_40" "news" "cora_cite" 
do
# for nl in 2 3 4 5 6 7 8
# do
for lr in 0.01 0.001 0.0001
do
    # python VilLain/main.py --gpu $gpu --dataset $d --num_step $num_step --num_step_gen $num_step_gen --lr $lr --num_labels $nl --dim $dim
    # python VilLain/emb_concat.py --dataset $d --num_step $num_step --num_step_gen $num_step_gen --lr $lr
    python VilLain/eval.py --data $d --num_step $num_step --num_step_gen $num_step_gen --lr $lr --device $gpu
done
done
# done
gpu=1
dim=128
## cora_cite
num_step=4
num_step_gen=100
lr=0.001
for nl in 2 3 4 5 6 7 8
do
python VilLain/main.py --gpu $gpu --dataset cora_cite --num_step $num_step --num_step_gen $num_step_gen --lr $lr --num_labels $nl --dim $dim --task edge
done
python VilLain/emb_concat.py --dataset $d --num_step $num_step --num_step_gen $num_step_gen --lr $lr --task edge
python VilLain/eval.py --data $d --num_step $num_step --num_step_gen $num_step_gen --lr $lr --device $gpu --task edge

# citeseer_cite
