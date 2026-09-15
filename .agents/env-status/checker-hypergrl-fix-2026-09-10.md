# Checker report — authorized HyperGRL checkpoint compatibility fix

Timestamp: 2026-09-10 KST

## Scoped diff

One line changed in `HyperGRL/hyper_model_general.py`:

```python
pretrained_model = th.load('./pre_trained.model', weights_only=False)
```

The path is the local `./pre_trained.model` produced by this same runner's
pretraining flow immediately before the load. No global deserialization policy
or external/untrusted checkpoint handling changed.

## Compile and bounded GPU run — SMOKE_PASS

```bash
python -m py_compile HyperGRL/hyper_model_general.py
export DGL_LIBRARY_PATH=/tmp/dgl-v2.1.0-build-r5
export LD_LIBRARY_PATH=/tmp/dgl-v2.1.0-build-r5:/home/dms2/miniconda/envs/hgnn-dgl-src/lib:${LD_LIBRARY_PATH:-}
conda run -n hgnn-dgl-src python HyperGRL/hyperGRL_train_our.py \
  --data cora_coauth --num_seeds 1 --device cuda:0 --epochs 15
```

Result: exit code 0. The runner completed preprocessing, node-level
pretraining, hyperedge-level pretraining/joint flow, tuning, validation, and
test evaluation.

```text
vali score: 0.43478260869565216
test score: 0.4227156276686593
42.3 ± 0.0
```

Classification: `SMOKE_PASS`. HyperGC Table 3 reports HyperGRL Cora-CA
`41.8 ± 5.8`; this Cora-CA 1-seed/15-epoch result is plausibly consistent but
is not a 20-split reproduction. HyperGCL was not run. AllSet DBLP-A remains
deferred as `BLOCKED_DATA`.
