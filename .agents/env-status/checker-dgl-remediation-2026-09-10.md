# Checker report — DGL remediation follow-up

Timestamp: 2026-09-10 KST

## HyperGRL after torch_scatter installation — FAIL_CODE

With the prescribed DGL exports, `hgnn-dgl-src` imported the new
`torch_scatter==2.1.2+pt27cu128`; a CUDA smoke returned `[4.0, 2.0]`.

```bash
conda run -n hgnn-dgl-src python HyperGRL/hyperGRL_train_our.py --data cora_coauth --num_seeds 1 --device cuda:0 --epochs 15
```

The model passed DGL import and Cora-CA preprocessing/clustering stages, then
failed before training at:

```text
HyperGRL/hyperedge_clique.py:286
TypeError: ReduceLROnPlateau.__init__() got an unexpected keyword argument 'verbose'
```

Torch 2.7 removed the legacy `verbose` scheduler keyword. This is a source API
compatibility issue, not another dependency-installation failure. No metric.

## GraphMAE2 Drive-source recovery — exact match restored

The Drive candidate
`/home/dms2/hojin_workspace/CoTeach_upload/drive_download/GraphMAE2/utils.py`
was accepted only after hashes for `GraphMAE2_train.py`, `datasets/data_proc.py`,
and the relevant model files exactly matched the workspace. `utils.py` was then
restored exactly; its post-restore SHA-256 is identical on both sides:

```text
4b33a0d400cd76f4c153a6fb4891313c9bbd493beb93288c67939c6f094ae017
```

The command must run from repository root with
`PYTHONPATH=/home/dms2/hojin_workspace/hgnn/GraphMAE2` so local runner imports
resolve while the common loader still finds `data/`.

```bash
PYTHONPATH=/home/dms2/hojin_workspace/hgnn/GraphMAE2 \
conda run -n hgnn-dgl-src python GraphMAE2/GraphMAE2_train.py \
  --data cora_coauth --num_seeds 1 --lr 0.0001 --mask_rate 0.5 \
  --device 0 --task node --epoch 15
```

Result: helper import advanced correctly, then failed with:

```text
ModuleNotFoundError: No module named 'wandb'
```

Requested builder action: install `wandb` in `hgnn-dgl-src`; this is an
environment dependency gap. Do not use `--use_cfg`, because the matching
`configs/` source folder is absent. No metric.

HyperGCL was not run. AllSet DBLP-A remains deferred as `BLOCKED_DATA`.
