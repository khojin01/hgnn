# Checker report — HNHN on hgnn-legacy

Timestamp: 2026-09-10 KST

Command (Cora-CA fixed `HNHN/time_node.sh` configuration, GPU 0):

```bash
conda run -n hgnn-legacy python HNHN/HNHN_train.py --data cora_coauth --num_seeds 1 --lr 0.01 --HNHN_alpha -0.5 --HNHN_beta -1.5 --device cuda:0 --task node --epoch 15
```

Result: exit code 0; duration 8.6 s; CUDA training completed.

```text
Highest Train: 100.00 ± nan
Highest Valid: 65.22 ± nan
Final Train: 100.00 ± nan
Final Test: 48.51 ± nan
```

Classification: `SMOKE_PASS`; `nan` standard deviation is expected at one
seed. This is executable validation, not a 20-split paper reproduction. No
environment repair requested.
