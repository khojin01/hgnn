#!/bin/bash

device=$1

python Hypeboy/Hypeboy_train.py --data citeseer_cite --task node --device cuda:0
python Hypeboy/Hypeboy_train.py --data cora_cite --task node --device cuda:0
python Hypeboy/Hypeboy_train.py --data dblp_copub --task node --device cuda:0
python Hypeboy/Hypeboy_train.py --data cora_coauth --task node --device cuda:0

python Hypeboy/Hypeboy_train.py --data imdb --task node --device cuda:0
python Hypeboy/Hypeboy_train.py --data house --task node --device cuda:0
python Hypeboy/Hypeboy_train.py --data pubmed_cite --task node --device cuda:0
python Hypeboy/Hypeboy_train.py --data dblp_coauth --task node --device cuda:0

python Hypeboy/Hypeboy_train.py --data aminer --task node --device cuda:0
python Hypeboy/Hypeboy_train.py --data modelnet_40 --task node --device cuda:0
python Hypeboy/Hypeboy_train.py --data news --task node --device cuda:0



Data: citeseer_cite / Task: node / Avg. Perf: 70.2 ± 0.1
Data: cora_cite / Task: node / Avg. Perf: 75.4 ± 0.2
Data: dblp_copub / Task: node / Avg. Perf: 84.3 ± 0.0
Data: cora_coauth / Task: node / Avg. Perf: 74.6 ± 0.0
Data: imdb / Task: node / Avg. Perf: 53.1 ± 0.0
Data: house / Task: node / Avg. Perf: 74.5 ± 0.1
Data: pubmed_cite / Task: node / Avg. Perf: 79.7 ± 0.1
Data: aminer / Task: node / Avg. Perf: 44.8 ± 0.0
Data: modelnet_40 / Task: node / Avg. Perf: 79.7 ± 0.0
Data: news / Task: node / Avg. Perf: 88.9 ± 0.0

0.88940589427948 / Std. Perf: 0.001148727822368653


