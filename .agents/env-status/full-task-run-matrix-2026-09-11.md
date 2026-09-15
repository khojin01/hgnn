# Formal task run matrix

Updated: 2026-09-11 KST.  This is the execution contract for the full
dataset-wise campaign.  It is deliberately separate from the bounded
one-seed smoke reports.  A `READY` entry uses the model's supplied fixed
configuration from `118.sh` (or a model-specific full runner), keeps its
`--num_seeds 20`, and writes a per-run log. `time_node.sh` runs are retained
as operational validation only: their 15/20-epoch timing bounds are not
Table-result reproduction settings.

## Data and split contract

The standard trainers load `H.pt`, `X.pt`, `Y.pt`, and
`data_split_0.01.pickle`.  At campaign start, the data preflight found:

| Dataset | Campaign disposition |
|---|---|
| `citeseer_cite`, `cora_coauth`, `imdb`, `aminer` | `READY_DATA`: all six common-loader files are present |
| `cora_cite` | `BLOCKED_DATA`: missing `X.pt`, `data_split_0.01.pickle`, and `data_split_118.pickle` |
| `dblp_copub` (DBLP-A) | `BLOCKED_DATA` for generic trainers: missing `data_split_0.01.pickle`; **AllSet is additionally explicitly DEFERRED by user** |
| `house` | `BLOCKED_DATA`: missing `H.pt`, `X.pt`, `Y.pt` |
| `pubmed_cite` | `READY_DATA`: all six common-loader files are present |
| `dblp_coauth` (DBLP-P) | `BLOCKED_DATA`: missing full `X.pt` and `edge_bucket.pickle` |
| `modelnet_40` | `BLOCKED_DATA`: missing `edge_bucket.pickle` |
| `news` | `BLOCKED_DATA`: missing `edge_bucket.pickle` (only `edge_bucket_match.pickle` exists) |

No missing input is attributed to a Conda environment. DBLP-A has the 118
split but lacks the generic 0.01 split, so it is still data-blocked for these
trainers.

## Task support and policy

| Family/models | Node (T3) | Hyperedge prediction (T4) | Community detection (T5) | Execution rule |
|---|---|---|---|---|
| Supervised: MLP, HGNN, HNHN, UniGCN, UniGCN2, UniGIN, AllSet, EDHNN, HyperGCN, PhenomNN | implemented (`node`) | implemented (`edge`) | no dedicated community evaluator | run node/edge only; community is N/A rather than a failure |
| H-GD (GGD) | implemented | implemented | no dedicated community evaluator | run node/edge only |
| GraphMAE2, MaskGAE, TriCL, HyperGCL, HyperGRL, HypeBoy, VilLain, SE-HSSL | implemented or model-specific node probe | model-specific pretext/evaluation route | model-specific clustering evaluator | run only where the checkout exposes a complete evaluator; otherwise record `BLOCKED_RUNNER`, never invent a metric |

The code audit directly confirms `node`/`edge` branches in the supervised
trainers, H-GD, GraphMAE2 and MaskGAE.  The remaining self-supervised models
need their supplied multi-stage runners: HypeBoy ignores the usual seed
switch in its node branch; VilLain is train → concatenate embeddings →
cluster-eval; SE-HSSL blocks in preprocessing before a metric.  They are not
placed into unattended generic batches.

### Mandatory paper skips

`SKIPPED_PAPER` means no command is launched.

| Model | T3 node skips | T4 edge skips | T5 community skips |
|---|---|---|---|
| PhenomNN | DBLP-P, AMiner = O.O.M; 20News = O.O.T | DBLP-P, AMiner = O.O.M; 20News = O.O.T | N/A |
| MaskGAE | 20News = O.O.T | 20News = O.O.T | 20News = O.O.T |
| HyperGCL | DBLP-P = O.O.M | — | DBLP-P = O.O.M |
| HyperGRL | 20News = O.O.T | 20News = O.O.T | 20News = O.O.T |

## First GPU-safe node batches

| Run ID | Model/env | GPU | Datasets | Status |
|---|---|---:|---|---|
| `node20-mlp-gpu0-20260911` | MLP / `hgnn-pyg` | 0 | `time_node` 20-epoch operational sweep; Cora-CA, IMDB, Pubmed, AMiner ran; DBLP-A/MN-40/20News logged blocked | complete; non-formal |
| `node20-hgnn-gpu1-20260911` | HGNN / `hgnn-legacy` | 1 | `time_node` 20-epoch operational sweep; Cora-CA, IMDB, Pubmed, AMiner ran; DBLP-A/MN-40/20News logged blocked | complete; non-formal |

Each child dataset command is limited to 30 minutes, runs sequentially on its
assigned GPU, and continues to the next dataset if it fails.  Its log records
the full command, exit code, and metric/no-metric evidence.  Results are
added to `formal-results.md` only after the 20-seed aggregate appears.
