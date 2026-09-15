# Checker report — UniGCN2 on hgnn-legacy

Timestamp: 2026-09-10 KST

Command (Cora-CA fixed `UniGCN2/time_node.sh` setting, GPU 0):

```bash
conda run -n hgnn-legacy python UniGCN2/UniGCN2_train.py --data cora_coauth --num_seeds 1 --lr 0.001 --device cuda:0 --task node --epoch 15
```

Result: exit code 0; duration 3.7 s; CUDA training completed.

```text
Highest Train: 65.22 ± nan
Highest Valid: 34.78 ± nan
Final Train: 52.17 ± nan
Final Test: 22.33 ± nan
```

Classification: `SMOKE_PASS`; `nan` standard deviation is expected for one
seed. HyperGC Table 3 reports UniGCN2 Cora-CA `55.3 ± 5.3`; the short,
single-seed result is not performance validation. It warrants a later tuned
20-split investigation, but does not indicate an environment failure.
