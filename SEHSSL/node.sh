
python SEHSSL/SEHSSL_train.py --task node --device 1 --num_seeds 1 --dataset cora_cite --num_layers 1 --hid_dim 128 --proj_dim 512 --drop_incidence_rate_1 0.1 --drop_incidence_rate_2 0.2 --drop_feature_rate_1 0.1 --drop_feature_rate_2 0.2 --tau 0.5 --tau_n 0.5 --tau_g 0.5 --tau_m 1 --w_g 1.2 --w_m 0.18 --n_epoch 200 --lr 0.0005 --weight_decay 0.1 --n_ratio  0.45 --e_ratio  0.45 --lr_lr 0.005 --lr_num_epochs 50 --lambda_n 0.0002 --lambda_g 0.0035 --beta 0.62 --K 1 --d 10  

 
 
python SEHSSL/SEHSSL_train.py --task node --device 1 --num_seeds 1 --dataset citeseer_cite  --num_layers 1 --hid_dim 128 --proj_dim 256 --drop_incidence_rate_1 0.1 --drop_incidence_rate_2 0.2 --drop_feature_rate_1 0.1 --drop_feature_rate_2 0.2 --tau 0.35 --tau_n 0.5 --tau_g 0.5 --tau_m 1 --w_g 1 --w_m 0.18 --n_epoch 200 --lr 0.0005 --weight_decay 0.2 --n_ratio  0.45 --e_ratio  0.45 --lr_lr 0.005 --lr_num_epochs 60 --lambda_n 0.00002 --lambda_g 0.00075 --beta 0.65 --K 4 --d 10 


python SEHSSL/SEHSSL_train.py --task node --device 1 --num_seeds 1 --dataset dblp_copub --drop_incidence_rate_1 0.3 --drop_incidence_rate_2 0.3 --drop_feature_rate_1 0.3 --drop_feature_rate_2 0.3 --tau_n 0.8 --tau_g 0.6 --tau_m 0.7 --w_g 2 --w_m 1 --lr 0.001 --hid_dim 128 --proj_dim 128 --weight_decay 1.0e-06 --num_layers 2 --n_epoch 200  

python SEHSSL/SEHSSL_train.py --task node --device 1 --num_seeds 1 --dataset cora_coauth  --num_layers 1 --hid_dim 128 --proj_dim 512 --drop_incidence_rate_1 0.05 --drop_incidence_rate_2 0.1 --drop_feature_rate_1 0.05 --drop_feature_rate_2 0.1 --tau 0.5 --tau_n 0.5 --tau_g 0.5 --tau_m 1 --w_g 1 --w_m 0 --n_epoch 200 --lr 0.0005 --weight_decay 0.05 --n_ratio  0.45 --e_ratio  0.45 --lr_lr 0.005 --lr_num_epochs 78 --lambda_n 0.0003 --lambda_g 0.00001 --beta 0.65 --K 4 --d 10 

python SEHSSL/SEHSSL_train.py --task node --device 1 --num_seeds 1 --dataset imdb --drop_incidence_rate_1 0.6 --drop_incidence_rate_2 0.6 --drop_feature_rate_1 0.7 --drop_feature_rate_2 0.7 --tau_n 0.1 --tau_g 0.3 --tau_m 0.9 --w_g 4 --w_m 0.5 --lr 0.001 --hid_dim 128 --proj_dim 128 --weight_decay 1.0e-06 --num_layers 2 --n_epoch 200  

python SEHSSL/SEHSSL_train.py --task node --device 1 --num_seeds 1 --dataset house --drop_incidence_rate_1 0.7 --drop_incidence_rate_2 0.7 --drop_feature_rate_1 0.5 --drop_feature_rate_2 0.5 --tau_n 0.3 --tau_g 0.9 --tau_m 0.8 --w_g 0.25 --w_m 2 --lr 0.001 --hid_dim 128 --proj_dim 128 --weight_decay 1.0e-06 --num_layers 2 --n_epoch 200 



python SEHSSL/SEHSSL_train.py --task node --device 1 --num_seeds 1 --dataset pubmed_cite  --num_layers 1 --hid_dim 128 --proj_dim 512 --drop_incidence_rate_1 0.1 --drop_incidence_rate_2 0.2 --drop_feature_rate_1 0.1 --drop_feature_rate_2 0.2 --tau 0.5 --tau_n 0.5 --tau_g 0.5 --tau_m 1 --w_g 1 --w_m 0.1 --n_epoch 200 --lr 3.55e-04 --weight_decay 4.5e-5 --lr_lr 0.03 --lr_wd 0.0 --lr_num_epochs 65 --lambda_n 0.0015 --lambda_g 0.0055 --beta 0.65 --K 2 --d 10 
 

 
python SEHSSL/SEHSSL_train.py --task node --device 1 --num_seeds 1 --dataset dblp_coauth  --num_layers 2 --hid_dim 128 --proj_dim 512 --drop_incidence_rate_1 0.1 --drop_incidence_rate_2 0.2 --drop_feature_rate_1 0.1 --drop_feature_rate_2 0.2 --tau 0.5 --tau_n 0.5 --tau_g 0.5 --tau_m 1 --w_g 1 --w_m 0.18 --n_epoch 200 --lr 3.6e-04 --weight_decay 0.01 --n_ratio  0.45 --e_ratio  0.45 --lr_lr 0.015 --lr_num_epochs 350 --lambda_n 0.0012 --lambda_g 0.003 --beta 0.65 --K 1 --d 10 
 
python SEHSSL/SEHSSL_train.py --task node --device 1 --num_seeds 1 --dataset aminer --drop_incidence_rate_1 0.5 --drop_incidence_rate_2 0.5 --drop_feature_rate_1 0.2 --drop_feature_rate_2 0.2 --tau_n 0.6 --tau_g 0.7 --tau_m 1.0 --w_g 1 --w_m 0.0625 --lr 0.0005 --hid_dim 128 --proj_dim 128 --weight_decay 1.0e-06 --num_layers 2 --n_epoch 200  

python SEHSSL/SEHSSL_train.py --task node --device 1 --num_seeds 1 --dataset modelnet_40  --num_layers 1 --hid_dim 128 --proj_dim 512 --drop_incidence_rate_1 0.05 --drop_incidence_rate_2 0.1 --drop_feature_rate_1 0.05 --drop_feature_rate_2 0.1 --tau 0.5 --tau_n 0.5 --tau_g 0.5 --tau_m 1 --w_g 1 --w_m 0.01 --n_epoch 200 --lr 0.0005 --weight_decay 0.18 --n_ratio  0.45 --e_ratio  0.45 --lr_lr 0.018 --lr_num_epochs 70 --lambda_n 0.0017 --lambda_g 0.025 --beta 0.5 --K 1 --d 10  

python SEHSSL/SEHSSL_train.py --task node --device 1 --num_seeds 1 --dataset news  --num_layers 1 --hid_dim 128 --proj_dim 512 --drop_incidence_rate_1 0.05 --drop_incidence_rate_2 0.1 --drop_feature_rate_1 0.05 --drop_feature_rate_2 0.1 --tau 1 --tau_n 0.5 --tau_g 0.5 --tau_m 1 --w_g 1 --w_m 0.01 --n_epoch 200 --lr 3.0e-04 --weight_decay 0 --lr_lr 0.018 --lr_num_epochs 100 --lambda_n 0.0005 --lambda_g 0.0001 --beta 0.6 --K 1 --d 10 
 