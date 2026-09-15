# Checker report — authorized SEHSSL configuration recovery and MaskGAE smoke

Timestamp: 2026-09-10 KST

## SEHSSL configuration recovery — restored, bounded smoke TIMEOUT

The confirmed Drive configuration was restored at `SEHSSL/config.yaml`. Its
content differs from the Drive source only by one final newline; its Cora-CA
contract is unchanged:

```yaml
cora_coauth:
  batch_size: 2048
  batch_size_2: null
```

Bounded Cora-CA node command used the recovered fixed configuration with
`n_epoch=15`, GPU 0, and one split. The process entered execution but emitted
no model progress or result artifact for 90 seconds, while consuming a CPU
core and 332 MiB on GPU 0 during sample generation/preprocessing. It was then
terminated with `SIGTERM` to honor bounded-smoke scope and release the GPU.

Classification: `TIMEOUT_PREPROCESS`; no Python traceback or metric. This is
not an environment import/config failure. A future run needs a time budget or
profiling/algorithmic decision for `generate_sample` before a full SEHSSL
benchmark can be attempted.

## MaskGAE recovery handoff — FAIL_ENV

Root restored the exact Drive candidates `MaskGAE/maskgae/model.py`,
`utils.py`, and `mask.py`; all three compile.

```bash
conda run -n hgnn-pyg python MaskGAE/MaskGAE_train.py \
  --data cora_coauth --num_seeds 1 --epochs 15 --lr 0.001 --device 0 \
  --task node --alpha 0.003 --p 0.5
```

Result: failed at first import:

```text
ModuleNotFoundError: No module named 'texttable'
```

The missing import originates in the restored exact
`MaskGAE/maskgae/utils.py` (`from texttable import Texttable`). Requested
builder action: install `texttable` in `hgnn-pyg`, then hand back for this
same bounded Cora-CA command. No metric.

HyperGCL was not run. AllSet DBLP-A remains deferred as `BLOCKED_DATA`.
