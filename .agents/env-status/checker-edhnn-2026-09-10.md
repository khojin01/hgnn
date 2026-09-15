# Checker report — EDHNN on hgnn-pyg

Timestamp: 2026-09-10 KST

The first uncommented DBLP-A command requires its missing
`data_split_0.01.pickle`, so this used the next fixed `time_node.sh`
configuration with complete generic input files.

```bash
conda run -n hgnn-pyg python EDHNN/EDHNN_train.py --data cora_coauth --num_seeds 1 --lr 0.001 --restart_alpha 0.8 --device cuda:0 --task node --epoch 15
```

Result: exit code 0; duration 3.6 s; CUDA run completed.

```text
Highest Train: 26.09 ± nan
Highest Valid: 17.39 ± nan
Final Train: 21.74 ± nan
Final Test: 7.56 ± nan
```

Classification: `SMOKE_PASS` for execution. `nan` standard deviation is the
expected one-seed warning. HyperGC Table 3's ED-HNN Cora-CA reference is
`36.3 ± 8.7`; 7.56% is not a reproduction-quality result, but this short
smoke must not be judged as a benchmark run. Confirm tuned/full-epoch settings
and 20-split behavior before calling a performance regression.
