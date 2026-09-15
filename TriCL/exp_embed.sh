!/bin/bash

device=$1

# python TriCL/TriCL_train.py --data citeseer_cite --device 1 --num_seeds 20
# python TriCL/TriCL_train.py --data cora_cite --device 1 --num_seeds 20
# python TriCL/TriCL_train.py --data dblp_copub --device 1 --num_seeds 20
# python TriCL/TriCL_train.py --data cora_coauth --device 1 --num_seeds 20
# python TriCL/TriCL_train.py --data imdb --device 1 --num_seeds 20
# python TriCL/TriCL_train.py --data house --device 1 --num_seeds 20
# python TriCL/TriCL_train.py --data pubmed_cite --device 1 --num_seeds 20
# python TriCL/TriCL_train.py --data dblp_coauth --device 1 --num_seeds 20
python TriCL/TriCL_train.py --data aminer --device 1 --num_seeds 20
# python TriCL/TriCL_train.py --data modelnet_40 --device 1 --num_seeds 20
# python TriCL/TriCL_train.py --data news --device 1 --num_seeds 20
