# Checker report — UniGIN on hgnn-legacy

Timestamp: 2026-09-10 KST

Planned fixed smoke command:

```bash
conda run -n hgnn-legacy python UniGIN/UniGIN_train.py --data cora_coauth --num_seeds 1 --lr 0.01 --device cuda:0 --task node --epoch 15
```

Result: `BLOCKED_EXECUTION_AUTHORIZATION`. The server rejected the GPU command
at approval time (`Rejected("rejected by user")`). No Python process started;
there is no model metric, traceback, or environment diagnosis. Do not report
this as a UniGIN or Conda failure. Re-run only after execution permission is
available.
