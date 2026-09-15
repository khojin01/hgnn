# Checker report — DGL final remediation verification

Timestamp: 2026-09-10 KST

All runs used the prescribed source-built DGL runtime exports.

## GraphMAE2 — SMOKE_PASS

The exact Drive `utils.py` is restored (SHA-256
`4b33a0d400cd76f4c153a6fb4891313c9bbd493beb93288c67939c6f094ae017`),
and `wandb==0.30.0` was available in `hgnn-dgl-src`.

```bash
PYTHONPATH=/home/dms2/hojin_workspace/hgnn/GraphMAE2 \
conda run -n hgnn-dgl-src python GraphMAE2/GraphMAE2_train.py \
  --data cora_coauth --num_seeds 1 --lr 0.0001 --mask_rate 0.5 \
  --device 0 --task node --epoch 15
```

Result: exit code 0; duration 5.2 s. DGL CUDA pretraining completed all 15
epochs (loss `3.9047 → 2.7305`) and the node linear evaluation completed.
The persisted metric is:

```text
mask:0.5_lr:0.0001_[0.4837745428085327]  48.4 ± 0.0
```

Classification: `SMOKE_PASS`. HyperGC Table 3 Cora-CA GraphMAE2 reference is
`64.3 ± 6.3`; this 15-epoch/one-seed result is executable validation only and
needs a tuned 20-split reproduction before judging performance.

## HyperGRL — FAIL_CODE (checkpoint compatibility)

After the authorized removal of obsolete scheduler `verbose=True` kwargs, the
same command completed DGL preprocessing, 15 node-level pretraining epochs,
15 hyperedge/joint epochs, and reached tuning:

```bash
conda run -n hgnn-dgl-src python HyperGRL/hyperGRL_train_our.py \
  --data cora_coauth --num_seeds 1 --device cuda:0 --epochs 15
```

It then failed at local checkpoint loading:

```text
_pickle.UnpicklingError: Weights only load failed
```

PyTorch 2.6+ defaults `torch.load` to `weights_only=True`; this checkpoint
contains `hyperedge_clique.GATClassifier`. The exact call is
`th.load('./pre_trained.model')` in `HyperGRL/hyper_model_general.py:195`.

Recommended source fix **only after confirming the local checkpoint is
trusted**: explicitly pass `weights_only=False` to that load call (or use a
safe-global allowlist if preserving restricted loading). No such change was
made by env-checker. No metric.

HyperGCL was not run. AllSet DBLP-A remains deferred as `BLOCKED_DATA`.
