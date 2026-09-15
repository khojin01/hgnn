# Checker report — AllSet on hgnn-pyg

Timestamp: 2026-09-10 KST

## Environment import preflight — PASS

Command:

```bash
conda run -n hgnn-pyg python -c "import sys, torch, torch_geometric, torch_scatter, torch_sparse, torch_cluster, torch_spline_conv, pyg_lib; ..."
```

Observed: Python 3.10.21; `torch=2.7.0+cu128`; CUDA 12.8 available on
`NVIDIA GeForce RTX 5080`; `torch_geometric=2.6.1`; all requested compiled PyG
extensions imported. Duration: 8.7 s (including the first model command).

## Fixed-script first enabled command — BLOCKED_DATA

Command (the first uncommented `AllSet/time_node.sh` entry, with allocated GPU
0 substituted):

```bash
conda run -n hgnn-pyg python AllSet/AllSet_train.py --data dblp_copub --num_seeds 1 --lr 0.001 --heads 2 --device cuda:0 --task node --epoch 15
```

Exit: 127 from `conda run` because the child process raised:

```text
FileNotFoundError: data/dblp_copub/data_split_0.01.pickle
```

`dataset.py` unconditionally loads `H.pt`, `X.pt`, `Y.pt`,
`data_split_0.01.pickle`, and `edge_bucket.pickle`. The chosen dataset has all
but the 0.01 split. This is a data-contract failure, not an environment fix.
No metric was produced.

## Next valid fixed-script command — FAIL_ENV_COMPAT / code-path incompatibility

`cora_coauth` has the required generic files. Command:

```bash
conda run -n hgnn-pyg python AllSet/AllSet_train.py --data cora_coauth --num_seeds 1 --lr 0.001 --heads 4 --device cuda:0 --task node --epoch 15
```

Exit: 127 from `conda run`; duration: 5.5 s; no metric. The run loaded the
data and entered `model(data)`, then failed at:

```text
AllSet/model.py:274 in aggregate
    raise ValeuError("aggr was not passed!")
NameError: name 'ValeuError' is not defined. Did you mean: 'ValueError'?
```

The error occurs below PyG 2.6.1's `MessagePassing.propagate` call because the
legacy model's custom `aggregate` receives no `aggr`. The misspelled exception
is source-level, but the entered branch is consistent with a PyG API behavior
change versus the lockfile's PyG 2.0.4. Do not patch `AllSet/model.py` without
root authorization.

## Requested env-builder action

Assess whether a Torch-2.7/RTX-5080-compatible PyG release or compatibility
setting can preserve the legacy custom aggregation contract. If none exists,
record this as a necessary modern-source port rather than an installation
failure. Preserve the successful CUDA/PyG import evidence above.

## Clerk fields

Model: AllSet; task: node; datasets: DBLP-A then Cora-CA; result:
`BLOCKED_DATA`, then `FAIL_ENV_COMPAT`; metric: none; Table 3 targets: 64.9
(DBLP-A), 53.6 (Cora-CA); evidence: this report.
