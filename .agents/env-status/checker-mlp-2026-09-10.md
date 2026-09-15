# Checker report — MLP on hgnn-pyg

Timestamp: 2026-09-10 KST

Command (Cora-CA fixed entry in `MLP/time_node.sh`, using allocated GPU 0):

```bash
conda run -n hgnn-pyg python MLP/MLP_train.py --data cora_coauth --num_seeds 1 --lr 0.01 --task node --epoch 20 --device cuda:0
```

Result: exit code 0; CUDA training completed. Output:

```text
Highest Train: 100.00 ± nan
Highest Valid: 43.48 ± nan
Final Train: 100.00 ± nan
Final Test: 32.15 ± nan
```

The `nan` standard deviations are expected warnings for `num_seeds=1` with
PyTorch's default unbiased standard deviation; this is not a numerical crash.
HyperGC Table 3 reports MLP Cora-CA accuracy `36.0 ± 4.7` over 20 splits. The
single 20-epoch smoke result is plausibly within that reference variation but
is not benchmark verification.

Classification: `SMOKE_PASS`; no environment repair requested.
