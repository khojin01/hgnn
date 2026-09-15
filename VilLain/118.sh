gpu=1



python VilLain/eval.py --data cora_cite --num_step 4 --num_step_gen 100 --device $gpu --lr 0.01
python VilLain/eval.py --data citeseer_cite --num_step 4 --num_step_gen 100 --device $gpu --lr 0.0001
python VilLain/eval.py --data cora_coauth --num_step 4 --num_step_gen 100 --device $gpu --lr 0.001
python VilLain/eval.py --data dblp_copub --num_step 4 --num_step_gen 100 --device $gpu --lr 0.01

python VilLain/eval.py --data house --num_step 4 --num_step_gen 100 --device $gpu --lr 0.0001
python VilLain/eval.py --data imdb --num_step 4 --num_step_gen 100 --device $gpu --lr 0.01
python VilLain/eval.py --data pubmed_cite --num_step 4 --num_step_gen 10 --device $gpu --lr 0.01

python VilLain/eval.py --data aminer --num_step 4 --num_step_gen 10 --device $gpu --lr 0.01
python VilLain/eval.py --data dblp_coauth --num_step 4 --num_step_gen 100 --device $gpu --lr 0.01
python VilLain/eval.py --data modelnet_40 --num_step 4 --num_step_gen 100 --device $gpu --lr 0.001
python VilLain/eval.py --data news --num_step 4 --num_step_gen 100 --device $gpu --lr 0.01
