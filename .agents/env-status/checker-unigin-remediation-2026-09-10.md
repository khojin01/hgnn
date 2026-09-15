# Checker report — UniGIN on hgnn-legacy

Timestamp: 2026-09-10 KST

The prior authorization block is cleared. Command (Cora-CA fixed
`UniGIN/time_node.sh` setting, GPU 0):

```bash
conda run -n hgnn-legacy python UniGIN/UniGIN_train.py --data cora_coauth --num_seeds 1 --lr 0.01 --device cuda:0 --task node --epoch 15
```

Result: exit code 0; duration 3.5 s; CUDA node training completed.

```text
Highest Train: 100.00 ± nan
Highest Valid: 52.17 ± nan
Final Train: 100.00 ± nan
Final Test: 50.85 ± nan
```

Classification: `SMOKE_PASS`. The `nan` standard deviation is expected for a
one-seed smoke run. HyperGC Table 3's UniGIN Cora-CA reference is
`49.2 ± 6.9`; this is plausible but does not replace a 20-split reproduction.
No environment repair requested.

AllSet DBLP-A remains explicitly deferred as `BLOCKED_DATA`: its first fixed
command cannot start because `data/dblp_copub/data_split_0.01.pickle` is
absent. This UniGIN result does not alter that status.
