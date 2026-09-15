# env-builder status

Updated: 2026-09-10 (Asia/Seoul)

## Server compatibility assessment

- OS: Ubuntu 24.04 kernel `7.0.0-28-generic`.
- Conda: `25.9.1` at `/home/dms2/miniconda`.
- GPUs: 2 x NVIDIA GeForce RTX 5080, driver `595.84`, driver CUDA capability
  `13.2`, 16 GB each.
- The supplied package sets pin Torch 1.11.0 CUDA 11.3 and Torch 1.13.1 CUDA
  11.7.  Those binaries predate RTX 5080/Blackwell (`sm_120`) and cannot be
  used for GPU execution here.  They remain reproducibility references, not
  viable GPU installations on this server.

## Proposed environments

| Environment | Requirement provenance | State | Next action |
| --- | --- | --- | --- |
| `hgnn-pyg` | `others_require.txt` (Torch 1.11 / PyG 2.0.4) | planned | Install a Blackwell-capable Torch/CUDA build and matching PyG extensions; smoke-test PyG models. |
| `hgnn-dgl` | `graphmae2_require.txt` (Torch 1.13 / DGL 0.9.1) | planned | Install a Blackwell-capable Torch build and compatible DGL; smoke-test GraphMAE2/HyperGRL. |
| `hgnn-legacy` | `HGNN_require.txt` (Torch 1.11 / PyG 2.0.3) | blocked-by-hardware until modern-port test | These models were explicitly reported to require this family. Their original binary cannot execute on RTX 5080. Test them only after modern PyG baseline works; otherwise require an older GPU/node. |
| `hgnn-hypergcl` | `others_require.txt` | deferred | Build/check last, per request. |

## Model mapping from source imports

- PyG: AllSet, EDHNN, H-GD, HGNN, HNHN, Hypeboy, HyperGCN, HyperGCL, MLP,
  MaskGAE, PhenomNN, SEHSSL, TriCL, UniGCN, UniGCN2, UniGIN, VilLain.
- DGL: GraphMAE2 and HyperGRL.
- Local datasets are present under `data/` (including `aminer`, `dblp_*`,
  `cora_*`, `citeseer_cite`, `house`, `imdb`, `modelnet_40`, `news`, and
  `pubmed_cite`), so no data download has yet been identified.

## Open issues / decisions

1. Creating Conda environments under `/home/dms2/miniconda/envs` and fetching
   Conda/PyPI wheels requires network and filesystem approval.  Awaiting it.
2. A modern GPU stack is a compatibility port relative to the three historic
   lockfiles.  The checker must distinguish package/API failures from metric
   differences; Table 3--5 verification belongs to the checker/clerk log.
3. `Hypeboy/time_node.sh` references `Hypeboy_train.py`, but the file listing
   contains `Hypeboy/src.py` and no `Hypeboy_train.py`; this is a model-runner
   issue, not an environment issue.

## Handoff format for env-checker

Append a dated entry to `.agents/env-status/env-checker.md` containing:
environment, command, model/dataset, result, full error traceback (if any),
and whether CPU import succeeded.  env-builder will then record the diagnosis
and environment-only remedy here.

## Final compatibility checkpoint — 2026-09-11

All four runtime environments now pass their GPU import checks on the RTX 5080:

| Environment | Verified stack | Builder remediation record |
| --- | --- | --- |
| `hgnn-pyg` | Torch 2.7.0+cu128, PyG 2.0.4, CUDA available | PyG extension compatibility; `texttable==1.7.0` for MaskGAE; Torch 2.7 scheduler compatibility fixes only where required. |
| `hgnn-dgl-src` | Torch 2.7.0+cu128, DGL 2.1.0, `torch_scatter 2.1.2+pt27cu128`, wandb 0.30.0, CUDA available | Isolated DGL CUDA 12.8/sm120 source build; runtime requires the documented DGL library-path exports. |
| `hgnn-legacy` | Torch 2.7.0+cu128, PyG 2.0.3, CUDA available | Legacy PyG model compatibility port. |
| `hgnn-hypergcl` | Torch 2.7.0+cu128, PyG 2.0.4, CUDA available | Built and validated last as requested. |

No reproducible environment blocker remains in the checker matrix.  Keep
AllSet DBLP-A deferred, retain all HyperGC Table 3/4/5 O.O.M/O.O.T skips, and
treat SEHSSL's bounded preprocessing timeout as a workload/data-runtime state
rather than an environment failure.  Model metrics remain smoke results until
their prescribed multi-split configurations are run.
