# Checker report — HGNN on hgnn-legacy

Timestamp: 2026-09-10 KST

Preflight: `hgnn-legacy` imported Torch 2.7.0+cu128, PyG 2.0.3,
`torch_scatter`, and `torch_sparse`; CUDA was available on RTX 5080.

Command (Cora-CA fixed `HGNN/time_node.sh` setting with GPU 0 substituted):

```bash
conda run -n hgnn-legacy python HGNN/HGNN_train.py --data cora_coauth --num_seeds 1 --lr 0.01 --device cuda:0 --task node --epoch 20
```

Result: exit code 0; duration 7.7 s; CUDA node training completed.

```text
Highest Train: 100.00 ± nan
Highest Valid: 56.52 ± nan
Final Train: 95.65 ± nan
Final Test: 45.26 ± nan
```

Classification: `SMOKE_PASS`. `nan` standard deviations are expected with one
seed. HyperGC Table 3 HGNN Cora-CA target is `44.3 ± 8.0`; this individual
smoke result is plausible but is not a 20-split reproduction.
