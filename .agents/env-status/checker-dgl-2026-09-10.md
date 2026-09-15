# Checker report — DGL environment / GraphMAE2 / HyperGRL

Timestamp: 2026-09-10 KST

All commands below exported the required source-built DGL runtime paths:

```bash
export DGL_LIBRARY_PATH=/tmp/dgl-v2.1.0-build-r5
export LD_LIBRARY_PATH=/tmp/dgl-v2.1.0-build-r5:/home/dms2/miniconda/envs/hgnn-dgl-src/lib:${LD_LIBRARY_PATH:-}
```

## DGL preflight — PASS

`hgnn-dgl-src` imported Torch `2.7.0+cu128`, DGL `2.1.0`, and
`dgl.graphbolt`; CUDA was available on RTX 5080. The shell emitted a harmless
`libtinfo.so.6: no version information available` warning, plus torchdata's
deprecation warning.

## GraphMAE2 — BLOCKED_SOURCE

Attempted fixed Cora-CA node command:

```bash
conda run -n hgnn-dgl-src python GraphMAE2/GraphMAE2_train.py --data cora_coauth --num_seeds 1 --lr 0.0001 --mask_rate 0.5 --device 0 --task node --epoch 15
```

It failed immediately with:

```text
ModuleNotFoundError: No module named 'utils'
```

The same result occurred from `cwd=GraphMAE2`. `GraphMAE2_train.py` imports
`build_args`, `create_optimizer`, `set_random_seed`, `TBLogger`,
`get_current_lr`, and `load_best_configs` from `utils`, but no
`GraphMAE2/utils.py` (or matching shared helper) exists in this checkout.
This is a recovered-source omission, not a DGL/Conda failure. No metric.

## HyperGRL — FAIL_ENV

Attempted bounded Cora-CA node command:

```bash
conda run -n hgnn-dgl-src python HyperGRL/hyperGRL_train_our.py --data cora_coauth --num_seeds 1 --device cuda:0 --epochs 15
```

It imported DGL successfully, then exited at local `HyperGRL/logreg.py` with:

```text
ModuleNotFoundError: No module named 'torch_scatter'
```

Requested builder action: install a Torch 2.7/CUDA 12.8/RTX 5080 compatible
`torch_scatter` into `hgnn-dgl-src`, then hand the environment back for the
same command. This is an environment dependency gap. No metric.

HyperGCL was not run. AllSet DBLP-A remains deferred as `BLOCKED_DATA`.
