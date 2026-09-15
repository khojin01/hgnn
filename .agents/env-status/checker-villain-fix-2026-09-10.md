# Checker report — authorized VilLain source fix and verification

Timestamp: 2026-09-10 KST

## Scoped source diff

Only `VilLain/main.py`, `VilLain/emb_concat.py`, and `VilLain/eval.py` changed.

1. `main.py` now updates `best_model` whenever loss improves, before the
   existing `epoch <= 1000` early-stopping skip. Therefore a bounded run has a
   valid checkpoint. The skip remains in place, preserving the original
   full-run early-stopping schedule.
2. Added a repository-relative `EMBS_DIR` in all three runners:
   `os.path.join(os.path.dirname(os.path.abspath(__file__)), 'embs')`.
   Replaced every `/home/cowbean/Compet_exp/VilLain/embs` read/write path with
   this directory, including edge-output paths.

No model architecture, optimizer, hyperparameter, dataset, or unrelated model
code changed. `rg` confirms no old absolute embedding path remains in these
three files.

## Compile and bounded GPU smoke — PASS

```bash
python -m py_compile VilLain/main.py VilLain/emb_concat.py VilLain/eval.py
conda run -n hgnn-pyg python VilLain/main.py --dataset cora_coauth --gpu 0 --epochs 10 --lr 0.001 --num_labels 2 --dim 128 --num_step 4 --num_step_gen 10 --task node
```

Result: exit code 0; duration 5.8 s. The program used `cuda:0`, loaded
Cora-CA (`V=2388`, `E=1072`), completed epoch 10, and wrote:

```text
VilLain/embs/cora_coauth_dim128_nl2_ns4_nsg10_lr0.001.pkl
```

## Embedding pipeline verification — PASS

```bash
conda run -n hgnn-pyg python VilLain/emb_concat.py --dataset cora_coauth --task node --dim 128 --num_step 4 --num_step_gen 10 --lr 0.001
conda run -n hgnn-pyg python VilLain/eval.py --data cora_coauth --task node --device 0 --num_seeds 1 --num_step 4 --num_step_gen 10 --lr 0.001
```

Result: exit code 0; duration 8.2 s. Concatenation created the merged
repository-relative embedding, with shape `(2388, 128)`. Evaluation completed
and reported Cora-CA clustering `NMI: 9.45`.

Classification: `SMOKE_PASS`. This 10-epoch, one-configuration result is not
a Table 5 reproduction. HyperGCL was not run. AllSet DBLP-A remains deferred
as `BLOCKED_DATA` because `data/dblp_copub/data_split_0.01.pickle` is absent.
