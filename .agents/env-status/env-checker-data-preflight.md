# env-checker data preflight correction

Updated: 2026-09-10 KST

This report supersedes the generic data-completeness sentence in
`env-checker-baseline.md`. Dataset directories exist, but the common
`H.pt`/`X.pt`/`Y.pt`/split-file contract is incomplete:

| Dataset | Missing generic inputs | Checker action |
|---|---|---|
| `cora_cite` | `X.pt`, `data_split_118.pickle`, `data_split_0.01.pickle` | `BLOCKED_DATA` unless its runner proves an alternate source |
| `house` | `H.pt`, `X.pt`, `Y.pt` | `BLOCKED_DATA` unless its runner proves an alternate source |
| `dblp_coauth` | full `X.pt`, `edge_bucket.pickle` | `BLOCKED_DATA` unless its runner proves an alternate source |
| `dblp_copub` | `data_split_0.01.pickle` | `BLOCKED_DATA` for standard trainers (the 118 split exists) |
| `pubmed_cite` | `Y.pt` | `BLOCKED_DATA` unless its runner proves an alternate source |
| `modelnet_40` | `edge_bucket.pickle` | `BLOCKED_DATA` unless its runner proves an alternate source |
| `news` | `edge_bucket.pickle` | `BLOCKED_DATA` (only `edge_bucket_match.pickle` exists) |

The complete generic-loader datasets are `citeseer_cite`, `cora_coauth`,
`imdb`, and `aminer`. A missing dataset file is not an environment-installation
error.

Hypeboy's `118.sh` contains pasted historical result text while calling the
missing `Hypeboy_train.py`; that text is not runtime evidence.
