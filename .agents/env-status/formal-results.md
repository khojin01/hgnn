# Formal dataset-wise results ledger

This ledger is separate from `README.md` smoke evidence. A row becomes
**formal** only when it uses the fixed configuration and completes the intended
paper split/seed protocol (normally 20), reports mean ± std, and links its log.
Single-seed or bounded runs remain smoke-only and are not formal results.

Status: `pending`, `running`, `formal`, `operational-20seed`, `skipped-oom`, `skipped-oot`,
`deferred`, `blocked-data`, `blocked-source`, `blocked-config`, or
`timeout-preprocess`. Targets are HyperGC Tables 3 (node accuracy), 4
(hyperedge AUROC), and 5 (community NMI).

## Node classification — Table 3

| Model | Dataset | Run config | Completed splits/seeds | Mean ± std | Table target | Status | Log / evidence |
|---|---|---|---:|---|---|---|---|
| AllSet | dblp_copub (DBLP-A) | fixed config | 0/20 | — | 64.9 ± 4.6 | deferred | Missing split; user deferred |
| AllSet | citeseer_cite | `118.sh`; lr=0.001, heads=8, default epoch=200 | 20/20 | 41.05 ± 8.26 | 41.1 ± 9.8 | formal | `full-runs/formal118-allset-node-gpu0-20260911/citeseer_cite.log` |
| AllSet | cora_coauth (Cora-CA) | `118.sh`; lr=0.001, heads=4, default epoch=200 | 20/20 | 53.09 ± 6.43 | 53.6 ± 8.2 | formal | `full-runs/formal118-allset-node-gpu0-20260911/cora_coauth.log` |
| AllSet | imdb | `118.sh`; lr=0.001, heads=8, default epoch=200 | 20/20 | 40.53 ± 4.58 | 41.7 ± 2.9 | formal | `full-runs/formal118-allset-node-gpu0-20260911/imdb.log` |
| AllSet | pubmed_cite | `118.sh`; lr=0.001, heads=8, default epoch=200 | 20/20 | 72.45 ± 6.22 | 74.1 ± 5.0 | formal | `full-runs/formal118-allset-node-gpu0-20260911/pubmed_cite.log` |
| AllSet | aminer | `118.sh`; lr=0.001, heads=2, default epoch=200 | 20/20 | 29.62 ± 3.55 | 29.8 ± 3.2 | formal | `full-runs/formal118-allset-node-gpu0-20260911/aminer.log` |
| EDHNN | citeseer_cite | `118.sh`; lr=0.001, restart_alpha=0.7, default epoch=200 | 20/20 | 34.00 ± 8.84 | 32.9 ± 11.6 | formal | `full-runs/formal118-edhnn-node-gpu0-20260911/citeseer_cite.log` |
| EDHNN | cora_coauth (Cora-CA) | `118.sh`; lr=0.001, restart_alpha=0.8, default epoch=200 | 20/20 | 36.50 ± 7.53 | 36.3 ± 8.7 | formal | `full-runs/formal118-edhnn-node-gpu0-20260911/cora_coauth.log` |
| EDHNN | imdb | `118.sh`; lr=0.001, restart_alpha=1, default epoch=200 | 20/20 | 38.00 ± 2.81 | 37.2 ± 2.6 | formal | `full-runs/formal118-edhnn-node-gpu0-20260911/imdb.log` |
| EDHNN | pubmed_cite | `118.sh`; lr=0.01, restart_alpha=1, default epoch=200 | 20/20 | 60.96 ± 3.85 | 61.9 ± 3.3 | formal | `full-runs/formal118-edhnn-node-gpu0-20260911/pubmed_cite.log` |
| EDHNN | aminer | `118.sh`; lr=0.01, restart_alpha=0.9, default epoch=200 | 20/20 | 26.56 ± 3.05 | 27.1 ± 2.8 | formal | `full-runs/formal118-edhnn-node-gpu0-20260911/aminer.log` |
| GraphMAE2 | cora_coauth (Cora-CA) | fixed config | 0/20 | — | 64.3 ± 6.3 | pending | smoke-only in README |
| H-GD (GGD) | cora_coauth (Cora-CA) | fixed config | 0/20 | — | 32.2 ± 6.3 | pending | smoke-only in README |
| HGNN | citeseer_cite | `118.sh`; lr=0.01, default epoch=200 | 20/20 | 38.09 ± 10.73 | 38.1 ± 10.7 | formal | `full-runs/formal118-hgnn-node-gpu1-20260911/citeseer_cite.log` |
| HGNN | cora_coauth (Cora-CA) | `118.sh`; lr=0.01, default epoch=200 | 20/20 | 46.59 ± 7.88 | 44.3 ± 8.0 | formal | `full-runs/formal118-hgnn-node-gpu1-20260911/cora_coauth.log` |
| HGNN | imdb | `118.sh`; lr=0.01, default epoch=200 | 20/20 | 41.88 ± 4.54 | 41.5 ± 2.8 | formal | `full-runs/formal118-hgnn-node-gpu1-20260911/imdb.log` |
| HGNN | pubmed_cite | `118.sh`; lr=0.001, default epoch=200 | 20/20 | 70.58 ± 3.63 | 70.8 ± 3.8 | formal | `full-runs/formal118-hgnn-node-gpu1-20260911/pubmed_cite.log` |
| HGNN | aminer | `118.sh`; lr=0.01, default epoch=200 | 20/20 | 30.54 ± 1.64 | 29.7 ± 2.0 | formal | `full-runs/formal118-hgnn-node-gpu1-20260911/aminer.log` |
| HNHN | citeseer_cite | commented `118.sh` fixed config; lr=0.01, alpha=0, beta=0, default epoch=200 | 20/20 | 43.33 ± 8.03 | 44.2 ± 7.9 | formal | `full-runs/formal118-hnhn-node-gpu1-20260911/citeseer_cite.log` |
| HNHN | cora_coauth (Cora-CA) | commented `118.sh` fixed config; lr=0.01, alpha=-0.5, beta=-1.5, default epoch=200 | 20/20 | 51.02 ± 6.56 | 53.1 ± 7.4 | formal | `full-runs/formal118-hnhn-node-gpu1-20260911/cora_coauth.log` |
| HNHN | imdb | commented `118.sh` fixed config; lr=0.001, alpha=0, beta=-1.5, default epoch=200 | 20/20 | 41.84 ± 3.66 | 42.5 ± 3.6 | formal | `full-runs/formal118-hnhn-node-gpu1-20260911/imdb.log` |
| HNHN | pubmed_cite | commented `118.sh` fixed config; lr=0.01, alpha=-3, beta=-2.5, default epoch=200 | 20/20 | 69.45 ± 3.36 | 69.1 ± 3.4 | formal | `full-runs/formal118-hnhn-node-gpu1-20260911/pubmed_cite.log` |
| HNHN | aminer | commented `118.sh` fixed config; lr=0.001, alpha=0.5, beta=0, default epoch=200 | 20/20 | 31.83 ± 2.03 | 32.1 ± 2.7 | formal | `full-runs/formal118-hnhn-node-gpu1-20260911/aminer.log` |
| Hypeboy | cora_coauth (Cora-CA) | fixed config | 0/20 | — | 67.0 ± 3.7 | pending | smoke-only in README |
| HyperGCL | cora_coauth (Cora-CA) | fixed config | 0/20 | — | 61.8 ± 3.0 | pending | smoke-only in README |
| HyperGCN | cora_coauth (Cora-CA) | fixed config | 0/20 | — | 45.0 ± 9.5 | pending | smoke-only in README |
| HyperGRL | cora_coauth (Cora-CA) | fixed config | 0/20 | — | 41.8 ± 5.8 | pending | smoke-only in README |
| MLP | citeseer_cite | `118.sh`; lr=0.01, default epoch=200 | 20/20 | 32.43 ± 8.05 | 32.4 ± 8.1 | formal | `full-runs/formal118-mlp-node-gpu0-20260911/citeseer_cite.log` |
| MLP | cora_coauth (Cora-CA) | `118.sh`; lr=0.01, default epoch=200 | 20/20 | 37.24 ± 4.31 | 36.0 ± 4.7 | formal | `full-runs/formal118-mlp-node-gpu0-20260911/cora_coauth.log` |
| MLP | imdb | `118.sh`; lr=0.01, default epoch=200 | 20/20 | 38.23 ± 2.67 | 37.6 ± 3.3 | formal | `full-runs/formal118-mlp-node-gpu0-20260911/imdb.log` |
| MLP | pubmed_cite | `118.sh`; lr=0.001, default epoch=200 | 20/20 | 62.67 ± 3.26 | 62.8 ± 3.0 | formal | `full-runs/formal118-mlp-node-gpu0-20260911/pubmed_cite.log` |
| MLP | aminer | `118.sh`; lr=0.01, default epoch=200 | 20/20 | 22.39 ± 1.42 | 22.7 ± 1.8 | formal | `full-runs/formal118-mlp-node-gpu0-20260911/aminer.log` |
| MaskGAE | cora_coauth (Cora-CA) | fixed config | 0/20 | — | 59.8 ± 4.1 | pending | smoke-only pretraining in README |
| PhenomNN | cora_coauth (Cora-CA) | fixed config | 0/20 | — | 56.2 ± 6.6 | pending | smoke-only in README |
| SEHSSL | cora_coauth (Cora-CA) | fixed config | 0/20 | — | 63.9 ± 5.0 | timeout-preprocess | 90-second bounded timeout |
| TriCL | cora_coauth (Cora-CA) | fixed config | 0/20 | — | 63.4 ± 3.9 | pending | smoke-only in README |
| UniGCN | citeseer_cite | `118.sh`; lr=0.001, default epoch=200 | 20/20 | 37.70 ± 8.58 | 39.8 ± 9.2 | formal | `full-runs/formal118-unigcn-node-gpu1-20260911/citeseer_cite.log` |
| UniGCN | cora_coauth (Cora-CA) | `118.sh`; lr=0.01, default epoch=200 | 20/20 | 47.21 ± 5.24 | 46.3 ± 6.6 | formal | `full-runs/formal118-unigcn-node-gpu1-20260911/cora_coauth.log` |
| UniGCN | imdb | `118.sh`; lr=0.01, default epoch=200 | 20/20 | 40.55 ± 3.27 | 41.0 ± 3.0 | formal | `full-runs/formal118-unigcn-node-gpu1-20260911/imdb.log` |
| UniGCN | pubmed_cite | `118.sh`; lr=0.001, default epoch=200 | 20/20 | 68.56 ± 4.99 | 67.6 ± 5.6 | formal | `full-runs/formal118-unigcn-node-gpu1-20260911/pubmed_cite.log` |
| UniGCN | aminer | `118.sh`; lr=0.001, default epoch=200 | 20/20 | 29.62 ± 1.53 | 29.8 ± 1.8 | formal | `full-runs/formal118-unigcn-node-gpu1-20260911/aminer.log` |
| UniGCN2 | cora_coauth (Cora-CA) | fixed config | 0/20 | — | 55.3 ± 5.3 | pending | smoke-only in README |
| UniGIN | citeseer_cite | `118.sh`; lr=0.01, default epoch=200 | 20/20 | 40.34 ± 9.37 | 41.4 ± 10.3 | formal | `full-runs/formal118-unigin-node-gpu1-20260911/citeseer_cite.log` |
| UniGIN | cora_coauth (Cora-CA) | `118.sh`; lr=0.01, default epoch=200 | 20/20 | 47.63 ± 6.55 | 49.2 ± 6.9 | formal | `full-runs/formal118-unigin-node-gpu1-20260911/cora_coauth.log` |
| UniGIN | imdb | `118.sh`; lr=0.01, default epoch=200 | 20/20 | 41.06 ± 3.93 | 41.7 ± 2.7 | formal | `full-runs/formal118-unigin-node-gpu1-20260911/imdb.log` |
| UniGIN | pubmed_cite | `118.sh`; lr=0.001, default epoch=200 | 20/20 | 69.74 ± 4.35 | 70.4 ± 4.9 | formal | `full-runs/formal118-unigin-node-gpu1-20260911/pubmed_cite.log` |
| UniGIN | aminer | `118.sh`; lr=0.001, default epoch=200 | 20/20 | 30.70 ± 1.16 | 30.8 ± 1.2 | formal | `full-runs/formal118-unigin-node-gpu1-20260911/aminer.log` |
| VilLain | cora_coauth (Cora-CA) | fixed config | 0/20 | — | 31.4 ± 4.1 | pending | node formal run pending |

## 20-seed operational validation (not Table 3 reproduction)

These runs used the shortened 20-epoch `time_node.sh` settings. They completed
20 seeds and prove end-to-end operation, but the formal campaign uses `118.sh`
and the default 200-epoch configuration; do not treat these values as Table 3
reproductions.

| Model | Dataset | Run config | Completed splits/seeds | Mean ± std | Table 3 target | Status | Log / evidence |
|---|---|---|---:|---|---|---|---|
| HGNN | cora_coauth (Cora-CA) | `time_node.sh`; 20 epochs | 20/20 | 43.80 ± 6.44 | 44.3 ± 8.0 | operational-20seed | `full-runs/node20-hgnn-gpu1-20260911/` |
| HGNN | imdb | `time_node.sh`; 20 epochs | 20/20 | 40.53 ± 4.80 | 41.5 ± 2.8 | operational-20seed | `full-runs/node20-hgnn-gpu1-20260911/` |
| HGNN | pubmed_cite | `time_node.sh`; 20 epochs | 20/20 | 66.93 ± 5.11 | 70.8 ± 3.8 | operational-20seed | `full-runs/node20-hgnn-gpu1-20260911/` |
| HGNN | aminer | `time_node.sh`; 20 epochs | 20/20 | 28.84 ± 2.25 | 29.7 ± 2.0 | operational-20seed | `full-runs/node20-hgnn-gpu1-20260911/` |
| MLP | cora_coauth (Cora-CA) | `time_node.sh`; 20 epochs | 20/20 | 35.39 ± 4.66 | 36.0 ± 4.7 | operational-20seed | `full-runs/node20-mlp-gpu0-20260911/` |
| MLP | imdb | `time_node.sh`; 20 epochs | 20/20 | 38.57 ± 2.74 | 37.6 ± 3.3 | operational-20seed | `full-runs/node20-mlp-gpu0-20260911/` |
| MLP | pubmed_cite | `time_node.sh`; 20 epochs | 20/20 | 49.78 ± 7.26 | 62.8 ± 3.0 | operational-20seed | `full-runs/node20-mlp-gpu0-20260911/` |
| MLP | aminer | `time_node.sh`; 20 epochs | 20/20 | 22.90 ± 1.64 | 22.7 ± 1.8 | operational-20seed | `full-runs/node20-mlp-gpu0-20260911/` |

## Hyperedge prediction — Table 4

| Model | Dataset | Run config | Completed splits/seeds | Mean ± std | Table target | Status | Log / evidence |
|---|---|---|---:|---|---|---|---|
| H-GD (GGD) | cora_coauth (Cora-CA) | fixed config | 0/20 | — | 73.2 ± 4.0 AUROC | pending | smoke-only in README |
| PhenomNN | dblp_copub (DBLP-P) | fixed config | 0/20 | — | O.O.M | skipped-oom | HyperGC Table 4 |
| PhenomNN | aminer | fixed config | 0/20 | — | O.O.M | skipped-oom | HyperGC Table 4 |
| PhenomNN | news (20News) | fixed config | 0/20 | — | O.O.T | skipped-oot | HyperGC Table 4 |
| MaskGAE | news (20News) | fixed config | 0/20 | — | O.O.T | skipped-oot | HyperGC Table 4 |
| HyperGRL | news (20News) | fixed config | 0/20 | — | O.O.T | skipped-oot | HyperGC Table 4 |

## Community detection — Table 5

| Model | Dataset | Run config | Completed splits/seeds | Mean ± std | Table target | Status | Log / evidence |
|---|---|---|---:|---|---|---|---|
| VilLain | cora_coauth (Cora-CA) | fixed config | 0/20 | — | 9.73 NMI | pending | 10-epoch smoke-only in README |
| HyperGCL | dblp_copub (DBLP-P) | fixed config | 0/20 | — | O.O.M | skipped-oom | HyperGC Table 5 |
| MaskGAE | news (20News) | fixed config | 0/20 | — | O.O.T | skipped-oot | HyperGC Table 5 |
| HyperGRL | news (20News) | fixed config | 0/20 | — | O.O.T | skipped-oot | HyperGC Table 5 |

## Update rule

For a completed formal run, replace the matching row with exact config,
completed splits/seeds, mean ± std, Table cell, and log path. Keep failed or
smoke-only attempts in `README.md`, not this ledger.

## Dataset-level blocked-data evidence

These are shared-loader failures, observed in both 20-seed MLP and HGNN
campaign commands; they are not environment failures.

| Dataset | Exact missing path | Evidence |
|---|---|---|
| DBLP-A (`dblp_copub`) | `data/dblp_copub/data_split_0.01.pickle` | `full-runs/node20-{mlp-gpu0,hgnn-gpu1}-20260911/dblp_copub.log` |
| MN-40 (`modelnet_40`) | `data/modelnet_40/edge_bucket.pickle` | `full-runs/node20-{mlp-gpu0,hgnn-gpu1}-20260911/modelnet_40.log` |
| 20News (`news`) | `data/news/edge_bucket.pickle` (only `edge_bucket_match.pickle` exists) | `full-runs/node20-{mlp-gpu0,hgnn-gpu1}-20260911/news.log` |
