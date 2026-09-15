
gpu=1


for nl in 2 3 4 5 6 7 8
do

python VilLain/main.py --dim 128 --num_labels $nl --dataset cora_cite --num_step 4 --num_step_gen 100 --gpu $gpu --epochs 20 --lr 0.01
python VilLain/main.py --dim 128 --num_labels $nl --dataset citeseer_cite --num_step 4 --num_step_gen 100 --gpu $gpu --epochs 20 --lr 0.0001
# python VilLain/main.py --dim 128 --num_labels $nl --dataset cora_coauth --num_step 4 --num_step_gen 100 --gpu $gpu --lr 0.001
# python VilLain/main.py --dim 128 --num_labels $nl --dataset dblp_copub --num_step 4 --num_step_gen 100 --gpu $gpu --lr 0.01

# python VilLain/main.py --dim 128 --num_labels $nl --dataset house --num_step 4 --num_step_gen 100 --gpu $gpu --lr 0.0001
# python VilLain/main.py --dim 128 --num_labels $nl --dataset imdb --num_step 4 --num_step_gen 100 --gpu $gpu --lr 0.01
# python VilLain/main.py --dim 128 --num_labels $nl --dataset pubmed_cite --num_step 4 --num_step_gen 10 --gpu $gpu --lr 0.01

# python VilLain/main.py --dim 128 --num_labels $nl --dataset aminer --num_step 4 --num_step_gen 10 --gpu $gpu --lr 0.01
# python VilLain/main.py --dim 128 --num_labels $nl --dataset dblp_coauth --num_step 4 --num_step_gen 100 --gpu $gpu --lr 0.01
# python VilLain/main.py --dim 128 --num_labels $nl --dataset modelnet_40 --num_step 4 --num_step_gen 100 --gpu $gpu --lr 0.001
# python VilLain/main.py --dim 128 --num_labels $nl --dataset news --num_step 4 --num_step_gen 100 --gpu $gpu --lr 0.01
done
