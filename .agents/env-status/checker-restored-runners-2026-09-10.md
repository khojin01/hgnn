# Checker report — restored UniGCN, Hypeboy, and VilLain runners

Timestamp: 2026-09-10 KST

## Recovery verification

The restored files compile successfully with `python -m py_compile` and their
names now satisfy the existing runner scripts:

- `Hypeboy/Hypeboy_train.py`, `Hypeboy/HNNs.py`
- `UniGCN/UniGCN_train.py`, `UniGCN/model.py`
- `VilLain/main.py`, `VilLain/emb_concat.py`, `VilLain/eval.py`

No recovered file was modified by env-checker.

## UniGCN — SMOKE_PASS

Environment: `hgnn-legacy` (Torch 2.7.0+cu128, PyG 2.0.3, RTX 5080).

```bash
conda run -n hgnn-legacy python UniGCN/UniGCN_train.py --data cora_coauth --num_seeds 1 --lr 0.01 --device cuda:0 --task node --epoch 15
```

Result: exit code 0; duration 3.5 s; GPU training completed.

```text
Highest Train: 100.00 ± nan
Highest Valid: 43.48 ± nan
Final Train: 91.30 ± nan
Final Test: 40.31 ± nan
```

`nan` standard deviation is expected at one seed. This establishes a working
runner/environment, not paper-performance reproduction.

## Hypeboy — SMOKE_PASS

Environment: `hgnn-pyg` (modern CUDA Torch + legacy-compatible PyG 2.0.4).
The runner ignores its CLI `--epoch` for the main HypeBoy procedure and instead
uses YAML-configured 300/200-stage training; it completed inside the imposed
60-second bound.

```bash
timeout 60s conda run -n hgnn-pyg python Hypeboy/Hypeboy_train.py --data cora_coauth --task node --device cuda:0 --epoch 15
```

Result: exit code 0; duration 9.0 s.

```text
Data: cora_coauth / Task: node / Avg. Perf: 0.6319385170936584 / Std. Perf: 0.0
```

Recorded accuracy: 63.19%. HyperGC Table 3 HypeBoy Cora-CA reference is
`67.0 ± 3.7`; this one-split smoke is plausible but not benchmark validation.

## VilLain — FAIL_CODE (bounded smoke)

Environment: `hgnn-pyg`.

```bash
conda run -n hgnn-pyg python VilLain/main.py --dataset cora_coauth --gpu 0 --epochs 10 --lr 0.001 --num_labels 2 --dim 128 --num_step 4 --num_step_gen 10 --task node
```

The program selected `cuda:0`, loaded Cora-CA (`V=2388`, `E=1072`), and ran
through epoch 10, then exited 127 through `conda run` because:

```text
TypeError: Expected state_dict to be dict-like, got <class 'NoneType'>.
```

Cause: `main.py` initializes `best_model=None` and deliberately skips its
checkpoint-selection branch until `epoch > 1000`, then unconditionally calls
`our_model.load_state_dict(best_model)`. A bounded (or script's 20-epoch)
node smoke therefore cannot complete. Even after that code-path is fixed, the
runner and `emb_concat.py` write/read hard-coded `/home/cowbean/Compet_exp/
VilLain/embs` paths rather than this workspace. This is a restored-source
issue, not a Conda dependency failure. Do not patch without root authorization.

## Preserved exclusions

AllSet DBLP-A (`dblp_copub`) remains `BLOCKED_DATA` because
`data/dblp_copub/data_split_0.01.pickle` is absent. HyperGCL was not run.
