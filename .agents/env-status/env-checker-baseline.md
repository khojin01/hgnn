# env-checker baseline inventory

Updated: 2026-09-10 (pre-environment inspection)

## Current state

No Conda environment handoff has been received; no model has been executed.
This report deliberately contains no claimed runtime results.

| Status | Models |
|---|---|
| Awaiting environment | AllSet, EDHNN, GraphMAE2, H-GD, HGNN, HNHN, HyperGCN, HyperGRL, MLP, MaskGAE, PhenomNN, SEHSSL, TriCL, UniGCN2, UniGIN, HyperGCL(last) |
| Source/entrypoint contract blocker | UniGCN, Hypeboy, VilLain |

## Datasets and fixed node-smoke coverage

The workspace contains the paper's 11 node datasets under `data/`:
`citeseer_cite`, `cora_cite`, `dblp_copub` (DBLP-A), `cora_coauth`
(Cora-CA), `imdb`, `house`, `pubmed_cite`, `dblp_coauth` (DBLP-P), `aminer`,
`modelnet_40` (MN-40), and `news` (20News).  The normal first enabled
fixed-parameter smoke dataset is `dblp_copub`; `time_node.sh` provides all
11 fixed commands for most baselines.  It is a 1-seed/15-epoch executable
test, not a paper reproduction.

## Node-classification paper references (HyperGC Table 3)

Values are accuracy percentages in this dataset order:
`Citeseer, Cora, DBLP-A, Cora-CA, IMDB, House, Pubmed, DBLP-P, AMiner, MN-40, 20News`.
Use mean ± standard deviation from the paper only for the final 20-split run.

| Model | Table 3 target |
|---|---|
| MLP | 32.4, 29.4, 56.6, 36.0, 37.6, 73.1, 62.8, 74.6, 22.7, 88.5, 73.3 |
| HGNN | 38.1, 45.1, 65.0, 44.3, 41.5, 51.9, 70.8, 84.0, 29.7, 89.5, 67.1 |
| UniGIN | 41.4, 45.5, 63.1, 49.2, 41.7, 50.8, 70.4, 83.5, 30.8, 87.1, 68.1 |
| UniGCN2 | 39.6, 43.9, 58.7, 55.3, 41.6, 58.8, 72.6, 86.1, 32.3, 79.7, 76.8 |
| AllSet | 41.1, 49.0, 64.9, 53.6, 41.7, 50.3, 74.1, 85.6, 29.8, 89.4, 77.2 |
| ED-HNN | 32.9, 29.3, 58.3, 36.3, 37.2, 71.0, 61.9, 85.1, 27.1, 73.0, 75.7 |
| PhenomNN | 42.2, 55.8, 70.3, 56.2, 42.1, 69.4, 76.8, O.O.M, O.O.M, 94.0, O.O.T |
| GraphMAE2 | 51.7, 61.0, 77.2, 64.3, 45.6, 52.4, 72.6, 87.4, 34.7, 90.6, 71.8 |
| MaskGAE | 53.2, 55.8, 78.2, 59.8, 45.0, 53.0, 75.4, 86.9, 33.8, 91.0, O.O.T |
| TriCL | 53.0, 61.5, 80.3, 63.4, 47.5, 65.2, 74.0, 87.6, 34.6, 93.0, 73.8 |
| HyperGCL (run last) | 43.4, 54.8, 69.5, 61.8, 48.4, 63.7, 71.0, O.O.M, 30.4, 94.6, 74.0 |
| HyperGRL | 35.1, 37.0, 41.1, 41.8, 35.7, 50.4, 50.2, 78.7, 28.0, 89.4, O.O.T |
| HypeBoy | 57.7, 61.9, 81.2, 67.0, 48.3, 67.7, 73.7, 87.9, 34.6, 89.2, 75.7 |
| VilLain | 33.6, 47.1, 40.4, 31.4, 39.7, 50.6, 73.7, 69.0, 19.9, 69.7, 74.3 |
| SE-HSSL | 57.0, 62.5, 77.1, 63.9, 48.9, 48.0, 69.8, 83.6, 34.8, 85.8, 75.8 |

`H-GD` is the checkout's name for the paper's GGD baseline; its exact Table 3
row is GGD and should be transcribed into its individual runtime report before
final reproduction.

## Table 4/5 exclusions to enforce

- Table 4 (hyperedge prediction): PhenomNN skips DBLP-P and AMiner (O.O.M),
  and 20News (O.O.T); MaskGAE and HyperGRL skip 20News (O.O.T).
- Table 5 (community detection): MaskGAE and HyperGRL skip 20News (O.O.T);
  HyperGCL skips DBLP-P (O.O.M).
- Any other O.O.M/O.O.T explicitly shown in the paper's corresponding row is
  a `SKIPPED_PAPER` result, not a failed run.

## Preflight findings for env-builder

- `others_require.txt` locks Torch 1.11.0 with PyG 2.0.4 and compiled
  extensions targeting `pt111cu113`/unqualified builds; package channel and
  CUDA wheel compatibility must be logged.
- `graphmae2_require.txt` locks Torch 1.13.1 / CUDA 11.7 and DGL 0.9.1;
  both generic `dgl` and `dgl-cu117` are listed, a potential duplicate-package
  conflict that must be resolved and recorded by the builder.
- `HGNN_require.txt` locks Torch 1.11.0 / PyG 2.0.3; use it for the special
  HGNN/HNHN/Uni family as directed by the prior maintainer.
