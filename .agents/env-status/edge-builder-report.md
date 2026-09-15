# EP env-builder report

Updated: 2026-09-13 08:50 KST

## Active execution

| GPU | PID | Queue | Current/next work | Log/status |
|---:|---:|---|---|---|
| 0 | 1897260 | `edge-hgd-six-gpu0-20260912` | H-GD, six complete datasets, 20 seeds each | `.agents/env-status/full-runs/edge-hgd-six-gpu0-20260912/` |
| 1 | 1895892 | `edge-six-resume-v2-gpu1-20260912` | UniGCN2 → HGNN → HNHN → EDHNN → AllSet → HyperGCN → MaskGAE; six datasets each | `.agents/env-status/full-runs/edge-six-resume-v2-gpu1-20260912/` |

The queues isolate every model/dataset command, record an exit state, continue
after a failure, and skip an already-written formal aggregate. MLP, UniGCN,
UniGIN, and GraphMAE2 already have six 20-seed aggregates and are not rerun.

Current execution at this update:

- GPU 0: HypeBoy Citeseer (`PID 1912684`). PhenomNN's five runnable datasets
  completed and AMiner was recorded as the paper O.O.M skip.
- GPU 1: HyperGCN Pubmed (`PID 1906289`); HyperGCN's first four datasets completed.
- H-GD, UniGCN2, HGNN, HNHN, EDHNN, and AllSet are complete on all six datasets.

## Fixes and checker verification

- Nine supervised trainers (`MLP`, `UniGCN`, `UniGIN`, `UniGCN2`, `HGNN`,
  `HNHN`, `EDHNN`, `AllSet`, `HyperGCN`) wrote their edge result and then
  crashed because node-only `end-start` timing variables were referenced.
  The timing write is now guarded by `args.task == "node"`.
- env-checker independently reran UniGCN2 edge in an isolated `/tmp` working
  directory: exit code 0, result produced, AUROC 62.23. No campaign result was
  polluted by this smoke test.
- TriCL's Drive-original source contained a complete edge branch but made it
  unreachable with `if True` and had no `--task` parser option. Added
  `--task {node,edge}`, activated the existing branch, updated `num_edges`
  after each edge-split incidence replacement, and enabled the standard result
  path. env-checker then completed an isolated Cora-CA edge smoke with exit 0
  and AUROC 84.2.
- PhenomNN now avoids node-only timing on edge runs and writes an unambiguous
  dataset/task result file. SE-HSSL refreshes `num_edges` for each edge split
  and writes dataset-specific results. HypeBoy retains its original aggregate
  output and additionally writes a dataset-specific edge result for clerk.
- VilLain's original edge trainer writes one node-embedding file per split and
  label-space size, but its evaluator was hardwired to the node branch. The
  evaluator now gathers only embeddings belonging to the same split, combines
  them with PCA, calls the existing membership-AUROC evaluator, and writes a
  dataset-specific result. env-checker validated the complete evaluator route
  in an isolated temporary directory (exit 0, diagnostic AUROC 76.4; not a
  formal result) and created `.agents/env-status/villain-edge-check.ok`.
- H-GD already supported `--task edge`; the new formal queue preserves the
  supplied `118.sh` settings and changes only the task. Its earlier Cora-CA
  one-seed result is not considered formal and does not trigger a skip.

## Google Drive source audit

The public folder is accessible without authentication through its public
HTML/download endpoints. The local H-GD, TriCL, and HyperGRL trainer hashes
exactly matched the Drive files before changes:

| File | Drive/local SHA-256 before edits |
|---|---|
| `H-GD/H-GD_train.py` | `4668dd46835a8da4d4c300abf57d5ac7f469c9e64d3dbda61eaec00c73a4b9d4` |
| `TriCL/TriCL_train.py` | `903d547525b4d06efc93c08b57d0e6982b3a3dff8202cbee9cc3c2f100c300e8` |
| `HyperGRL/HyperGRL_train.py` | `4c6db7ecf37023772a5a7bf6936e4bb04af675dd9237d5131d2b9e4fe89c378d` |

The Drive source also has no `exp_edge.sh` for H-GD, TriCL, or HyperGRL.
Therefore no missing edge runner can be restored for those models. H-GD and
TriCL are recoverable from their latent evaluators. HyperGRL contains an
unused edge evaluator but no edge training/evaluation branch, so it needs a
careful implementation/validation rather than a filename substitution.

## Data audit

The six campaign datasets (`citeseer_cite`, `cora_coauth`, `imdb`, `house`,
`pubmed_cite`, `aminer`) have the required common-loader files. The failures
outside this set are data blockers, not Conda failures. The original Drive was
checked and contains the same omissions:

- `cora_cite`: Drive also lacks `X.pt`.
- `dblp_copub`: Drive also lacks `data_split_0.01.pickle` (and remains user-deferred for AllSet).
- `dblp_coauth`: Drive also lacks `X.pt`.
- `modelnet_40`: Drive also lacks `edge_bucket.pickle`.
- `news`: Drive has only `edge_bucket_match.pickle`, exactly like local.

No missing data file was fabricated or renamed because equivalence is not yet
established. Paper-designated O.O.M/O.O.T cases remain skips.

## Follow-on queue

TriCL's six-dataset 20-seed queue is staged as PID 1897580. It waits for the
GPU-1 supervised queue to exit and then starts automatically, skipping any
formal result that may already exist.

GPU 0 also has PID 1898142 staged behind H-GD. It runs PhenomNN on the five
non-skipped datasets (AMiner is recorded as `SKIPPED_PAPER_OOM`) and then
HypeBoy on all six, preserving the supplied per-dataset settings/configuration.

Additional persistent follow-on queues:

| PID | GPU | Queue | Start condition |
|---:|---:|---|---|
| 1912638 | 0 | SE-HSSL, six datasets | after PID 1898142 (PhenomNN/HypeBoy) exits |
| 1912639 | 1 | HyperGCL, six datasets | after PID 1897580 (TriCL) exits |
| 1912647 | 1 | VilLain, six datasets | after HyperGCL exits and checker gate exists |

VilLain requires all 20 real split embeddings for each of label sizes 2–8
before evaluation. Partial embedding sets are recorded as
`FAILED_EMBEDDINGS` and are never reported as formal metrics.

### Checker follow-up corrections (2026-09-13 01:20 KST)

- SE-HSSL and VilLain now persist the complete 20-value `test_results` array
  alongside mean and standard deviation, allowing clerk/checker to audit the
  seed count instead of trusting only an aggregate.
- VilLain evaluation explicitly enumerates label sizes 2 through 8 for every
  split and raises on any missing file. A partial/stale embedding set cannot be
  evaluated as complete.
- HyperGCL queue completion/skip detection now uses the trainer's actual result
  stem, `result_<dataset>_HyperGCL_edge.txt`.
- `py_compile` for both modified trainers and `bash -n` for both affected
  queues passed before the queued models started.

### Timing-footer preservation (2026-09-13 08:50 KST)

- MaskGAE finished all six 20-seed EP runs and wrote complete 20-value arrays.
  Its old process then exited 1 only in the node-only `end-start` footer. The
  six status pairs were corrected by appending `COMPLETE_RESULT_PRESERVED`;
  none were rerun.
- HyperGCL Citeseer and Cora-CA likewise completed 20 seeds and wrote results
  before the obsolete footer raised `NameError`. Both were reclassified as
  `COMPLETE_RESULT_PRESERVED` without rerun.
- HyperGCL IMDB (`PID 1938916`) loaded the old source and is still running.
  Monitor PID 1941374 waits for it to exit and marks it complete only when the
  result exists and the log contains the final 20-seed statistics. House,
  Pubmed, and AMiner are subsequently launched from the already-patched source.
- The HyperGCL parent queue remains PID 1912639. VilLain queue PID 1912647 is
  still waiting for that parent to finish and will then start automatically.
