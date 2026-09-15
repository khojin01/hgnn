# Checker report — HyperGCL final-order smoke validation

Timestamp: 2026-09-10 KST

HyperGCL was executed only after the remaining eligible models reached their
documented terminal states. Cora-CA is not an O.O.M/O.O.T exception in the
HyperGC tables.

## Environment preflight

`hgnn-hypergcl` imported Torch `2.7.0+cu128`, PyG `2.0.4`, compiled
`torch_scatter`/`torch_sparse`, and CUDA on RTX 5080.

## Command and result

```bash
conda run -n hgnn-hypergcl python HyperGCL/HyperGCL_train.py \
  --task node --epochs 15 --num_seeds 1 --data cora_coauth --cuda 0
```

Result: exit code 0. The runner persisted its result rather than returning the
usual stdout summary:

```text
results/result_cora_coauth_HyperGCL_node.txt
lr0.001glr0.001a_l0.1=> tensor([11.4432]),11.4 ± nan
```

`time/time.txt` additionally records GPU execution time `14.8835` seconds and
accuracy `11.4432` for `cora_coauth_HyperGCL`.

Classification: `SMOKE_PASS` for environment/model execution. The `nan`
standard deviation is expected at one seed. HyperGC Table 3's HyperGCL
Cora-CA target is `61.8 ± 3.0`; this short, default-hyperparameter smoke is
far below that reference and is **not** a performance reproduction. Before a
benchmark conclusion, run the intended tuned hyperparameters and 20 splits.

No PDF-designated O.O.M/O.O.T pair was run. AllSet DBLP-A remains deferred as
`BLOCKED_DATA`.
