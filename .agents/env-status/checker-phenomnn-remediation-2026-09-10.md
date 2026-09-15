# Checker report — PhenomNN scheduler compatibility verification

Timestamp: 2026-09-10 KST

Builder removed only obsolete `verbose=False` from PhenomNN's
`ReduceLROnPlateau` call. The supplied exact command ran successfully:

```bash
conda run -n hgnn-pyg python PhenomNN/PhenomNN_train.py \
  --data cora_coauth --num_seeds 1 --lr 0.01 --device cuda:0 --task node \
  --lam0 20 --lam1 10 --alp 0.1 --prop_step 8 --epoch 15
```

Result: exit code 0; duration 5.5 s; CUDA node training completed.

```text
Highest Train: 100.00 ± nan
Highest Valid: 47.83 ± nan
Final Train: 100.00 ± nan
Final Test: 49.06 ± nan
```

Classification: `SMOKE_PASS`. The `nan` standard deviation is expected for
one seed. HyperGC Table 3's PhenomNN Cora-CA target is `56.2 ± 6.6`; the
short, one-seed result is not a benchmark reproduction.
