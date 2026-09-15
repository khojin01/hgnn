# Checker report — AllSet remediation verification

Timestamp: 2026-09-10 KST

Builder changed only the pure-Python package to `torch-geometric==2.0.4`, while
retaining RTX-compatible Torch `2.7.0+cu128` and the compiled PyG extensions.

Preflight command:

```bash
conda run -n hgnn-pyg python -c "import torch, torch_geometric, torch_scatter; print(torch.__version__, torch_geometric.__version__, torch.cuda.is_available())"
```

Observed: `2.7.0+cu128 2.0.4 True`.

Recheck command:

```bash
conda run -n hgnn-pyg python AllSet/AllSet_train.py --data cora_coauth --num_seeds 1 --lr 0.001 --heads 4 --device cuda:0 --task node --epoch 15
```

Result: exit code 0; duration 7.4 s; GPU node run completed.

```text
Highest Train: 100.00 ± nan
Highest Valid: 65.22 ± nan
Final Train: 100.00 ± nan
Final Test: 48.38 ± nan
```

The `nan` standard deviations are expected for one seed. HyperGC Table 3
reports AllSet Cora-CA `53.6 ± 8.2` over 20 splits; this is an executable
smoke-pass result, not final reproduction. The first script entry (`dblp_copub`)
remains `BLOCKED_DATA` because its `data_split_0.01.pickle` is absent.

Classification: `SMOKE_PASS` after environment remediation. No source code
was edited.
