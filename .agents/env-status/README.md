# Environment and model validation status

Last updated: 2026-09-11 KST — all runnable environment groups, including the
final HyperGCL run, have smoke results; no 20-split benchmark verification.

Legend: `planned` means awaiting the relevant agent. Metrics must include the
reported statistic (normally mean ± std), seed count, and a log/result path.
`T3/T4/T5` refers to HyperGC PDF Tables 3, 4, and 5; clerk records the exact
matching cell before calling a result benchmark-verified. Any O.O.M/O.O.T cell
is recorded as `skipped` and is not run.

## Current environment status

| Environment | Requirement source | Intended models | Builder state | Checker state | Blocker / next owner |
|---|---|---|---|---|---|
| `hgnn-pyg` | `others_require.txt` (compatibility port) | AllSet, EDHNN, H-GD, Hypeboy, HyperGCN, MLP, MaskGAE, PhenomNN, TriCL, UniGCN2 | ready_for_check | CUDA/PyG import pass; AllSet/MLP smoke-pass | Python 3.10.21/Torch 2.7.0+cu128/RTX 5080; PyG 2.0.4 — env-builder/checker |
| `hgnn-dgl-src` | `graphmae2_require.txt` (isolated source-build port) | GraphMAE2, HyperGRL | ready_for_check | CUDA/GraphBolt; GraphMAE2/HyperGRL smoke-pass | DGL 2.1.0 source build, CUDA 12.8/sm120; requires `DGL_LIBRARY_PATH=/tmp/dgl-v2.1.0-build-r5` and matching `LD_LIBRARY_PATH` |
| `hgnn-legacy` | `HGNN_require.txt` (compatibility port) | HGNN, HNHN, UniGCN, UniGIN, UniGCN2 | ready_for_check | CUDA/import; HGNN/HNHN/UniGIN/UniGCN2 smoke-pass | UniGCN runner restored from user-provided Drive; runtime validation pending — env-checker |
| `hgnn-hypergcl` | `others_require.txt` baseline (compatibility port) | HyperGCL | ready_for_check | smoke-pass | Python 3.10.21/Torch 2.7.0+cu128/PyG 2.0.4; final Cora-CA bounded smoke completed — env-checker |

## Current model status

| Order | Model | Environment | Check command / fixed configuration | Datasets | Observed performance | Benchmark ref. | State | Blocker / next owner |
|---:|---|---|---|---|---|---|---|---|
| 1 | AllSet | `hgnn-pyg` | Cora-CA GPU0; 1 seed, 15 epochs | DBLP-A explicitly deferred; Cora-CA completed | Cora-CA test accuracy 48.38%; std `nan` expected for 1 seed | T3: DBLP-A 64.9 ± 4.6; Cora-CA 53.6 ± 8.2 | smoke-pass | DBLP-A deferred by user; Cora-CA preliminary only — checker |
| 2 | EDHNN | `hgnn-pyg` | Cora-CA GPU0; 1 seed, 15 epochs | DBLP-A blocked; Cora-CA completed | Cora-CA test accuracy 7.56%; std `nan` expected for 1 seed | T3 node Cora-CA: 36.3 ± 8.7 | smoke-pass | Execution only; do not call metric regression until tuned 20-split run — checker |
| 3 | GraphMAE2 | `hgnn-dgl-src` | Cora-CA GPU0; 1 seed, 15 epochs | cora_coauth | final accuracy 48.4 ± 0.0 | T3 node Cora-CA: 64.3 ± 6.3 | smoke-pass | End-to-end pass; configuration not a Table 3 reproduction |
| 4 | H-GD | `hgnn-pyg` | Cora-CA GPU0; 1 seed, 15 epochs | node and hyperedge prediction completed | node 30.23%; edge AUROC 54.30%; std 0.00 | T3/T4 GGD Cora-CA: 32.2 ± 6.3 / 73.2 ± 4.0 | smoke-pass | Environment is ready; fixed-script datasets still have missing files — data owner/checker |
| 5 | HGNN | `hgnn-legacy` | Cora-CA GPU0; 1 seed, 20 epochs | cora_coauth | test accuracy 45.26%; std `nan` expected for 1 seed | T3 node Cora-CA: 44.3 ± 8.0 | smoke-pass | Plausible, but not 20-split comparable — checker |
| 6 | HNHN | `hgnn-legacy` | Cora-CA GPU0; 1 seed, 15 epochs | cora_coauth | test accuracy 48.51%; std `nan` expected for 1 seed | T3 node Cora-CA: 53.1 ± 7.4 | smoke-pass | Preliminary only; no environment repair required — checker |
| 7 | Hypeboy | `hgnn-pyg` | Cora-CA GPU0; bounded recovered runner | cora_coauth | test accuracy 63.19% | T3 node Cora-CA: 67.0 ± 3.7 | smoke-pass | Recovered Drive runner executes; preliminary configuration — checker |
| 8 | HyperGCN | `hgnn-pyg` | Cora-CA GPU0; 1 seed, 20 epochs | DBLP-A blocked; Cora-CA completed | Cora-CA final test accuracy 24.77%; std `nan` expected for 1 seed | T3 node Cora-CA: 45.0 ± 9.5 | smoke-pass | DBLP-A split missing; Cora-CA is preliminary only — checker |
| 9 | HyperGRL | `hgnn-dgl-src` | Cora-CA GPU0; 1 seed, 15 epochs full flow | cora_coauth | final accuracy 42.3 ± 0.0 | T3 node Cora-CA: 41.8 ± 5.8 | smoke-pass | Scoped `weights_only=False` checkpoint-load compatibility patch; plausible, not 20-split comparable |
| 10 | MLP | `hgnn-pyg` | Cora-CA GPU0; 1 seed, 20 epochs | cora_coauth | test accuracy 32.15%; std `nan` expected for 1 seed | T3 node Cora-CA: 36.0 ± 4.7 | smoke-pass | Configuration differs from Table 3 and has insufficient seeds; run 20 splits for benchmark check — checker |
| 11 | MaskGAE | `hgnn-pyg` | Cora-CA GPU0; 1 seed, 15 epochs | cora_coauth | pretraining completed; no metric because eval period 30 > smoke 15 epochs | T3/T4/T5 | smoke-pass | `texttable==1.7.0` installed; execution passes, extend epochs for evaluation — checker |
| 12 | PhenomNN | `hgnn-pyg` | Cora-CA GPU0; 1 seed, 15 epochs | cora_coauth | test accuracy 49.06%; std `nan` expected for 1 seed | T3 node Cora-CA: 56.2 ± 6.6 | smoke-pass | Scoped scheduler fix works; not a 20-split benchmark — checker |
| 13 | SEHSSL | `hgnn-pyg` | bounded Cora-CA node run | cora_coauth preprocessing | no metric | T3 node Cora-CA: 63.9 ± 5.0 | timeout-preprocess | Provenance-matched config restored; stopped after 90s with no model output/traceback to honor bound, not an environment failure |
| 14 | TriCL | `hgnn-pyg` | Cora-CA GPU0; 1 seed, 15 epochs | cora_coauth completed | Cora-CA test accuracy 60.10%; std 0.00 | T3 node Cora-CA: 63.4 ± 3.9 | smoke-pass | Fixed active datasets lack files; Cora-CA preliminary only — checker |
| 15 | VilLain | `hgnn-pyg` | Cora-CA CUDA; 10 epochs; train → concat → eval | cora_coauth | cluster NMI 9.45 | T5 community Cora-CA: 9.73 | smoke-pass | Minimal authorized patch preserves full-run behavior; short configuration is not a Table 5 reproduction |
| 16 | UniGCN | `hgnn-legacy` | Cora-CA GPU0; 1 seed, 15 epochs | cora_coauth | test accuracy 40.31%; std `nan` expected for 1 seed | T3 node Cora-CA: 46.3 ± 6.6 | smoke-pass | Recovered Drive runner executes; preliminary only — checker |
| 17 | UniGCN2 | `hgnn-legacy` | Cora-CA GPU0; 1 seed, 15 epochs | cora_coauth completed | Cora-CA final test accuracy 22.33%; std `nan` expected for 1 seed | T3 node Cora-CA: 55.3 ± 5.3 | smoke-pass | Preliminary only; run 20 splits for benchmark check — checker |
| 18 | UniGIN | `hgnn-legacy` | Cora-CA GPU0; 1 seed, 15 epochs | cora_coauth | test accuracy 50.85%; std `nan` expected for 1 seed | T3 node Cora-CA: 49.2 ± 6.9 | smoke-pass | Plausible smoke result only; not 20-split comparable |
| 19 (last) | HyperGCL | `hgnn-hypergcl` | Cora-CA GPU0; 1 seed bounded smoke | cora_coauth; O.O.M/O.O.T cells remain skipped | final accuracy 11.4 ± `nan`; 14.88 s | T3 node Cora-CA: 61.8 ± 3.0 | smoke-pass | Final-order run completed; smoke only, not benchmark-pass |

## Dataset performance ledger

No completed measurements yet. Add one row per model/dataset/task after a run.

Formal 20-split/seed results and Table 3–5 skip/defer status are maintained in
[the formal dataset-wise ledger](formal-results.md). The table below is smoke
evidence only. A dark visual view of the same formal ledger is available in
[results-dashboard.html](results-dashboard.html).

| Model | Task | Dataset | Command/config | Metric (mean ± std; seeds) | HyperGC table/cell/value | Comparison | Evidence | Status |
|---|---|---|---|---|---|---|---|---|
| MLP | node | cora_coauth (Cora-CA) | GPU0; 1 seed; 20 epochs | 32.15% (std `nan`, expected for one seed) | T3 / MLP Cora-CA / 36.0 ± 4.7 | provisional, plausibly consistent; not 20-split comparable | `.agents/env-status/checker-mlp-2026-09-10.md` | smoke-pass |
| AllSet | node | cora_coauth (Cora-CA) | GPU0; 1 seed; 15 epochs | 48.38% (std `nan`, expected for one seed) | T3 / AllSet Cora-CA / 53.6 ± 8.2 | preliminary; configuration and seed count are not comparable | `.agents/env-status/checker-allset-remediation-2026-09-10.md` | smoke-pass |
| EDHNN | node | cora_coauth (Cora-CA) | GPU0; 1 seed; 15 epochs | 7.56% (std `nan`, expected for one seed) | T3 / ED-HNN Cora-CA / 36.3 ± 8.7 | execution smoke only; configuration and seed count are not comparable | `.agents/env-status/checker-edhnn-2026-09-10.md` | smoke-pass |
| HGNN | node | cora_coauth (Cora-CA) | GPU0; 1 seed; 20 epochs | 45.26% (std `nan`, expected for one seed) | T3 / HGNN Cora-CA / 44.3 ± 8.0 | plausible smoke result; not 20-split comparable | `.agents/env-status/checker-hgnn-2026-09-10.md` | smoke-pass |
| HNHN | node | cora_coauth (Cora-CA) | GPU0; 1 seed; 15 epochs | 48.51% (std `nan`, expected for one seed) | T3 / HNHN Cora-CA / 53.1 ± 7.4 | preliminary; configuration and seed count are not comparable | `.agents/env-status/checker-hnhn-2026-09-10.md` | smoke-pass |
| H-GD (GGD) | node | cora_coauth (Cora-CA) | GPU0; 1 seed; 15 epochs; p_e=0.1, p_x=0.1 | 30.23% (std 0.00) | T3 / GGD Cora-CA / 32.2 ± 6.3 | -1.97%p; preliminary, not 20-split comparable | `.agents/env-status/checker-h-gd-cora-coauth-2026-09-10.log` | smoke-pass |
| HyperGCN | node | cora_coauth (Cora-CA) | GPU0; 1 seed; 20 epochs | 24.77% (std `nan`, expected for one seed) | T3 / HyperGCN Cora-CA / 45.0 ± 9.5 | -20.23%p; preliminary, not 20-split comparable | `.agents/env-status/checker-hypergcn-cora-coauth-2026-09-10.log` | smoke-pass |
| PhenomNN | node | cora_coauth (Cora-CA) | GPU0; 1 seed; 15 epochs | no metric; scheduler constructor rejected `verbose` | T3 / PhenomNN Cora-CA / 56.2 ± 6.6 | execution blocked before training | `.agents/env-status/checker-phenomnn-cora-coauth-2026-09-10.log` | failed-code |
| TriCL | node | cora_coauth (Cora-CA) | GPU0; 1 seed; 15 epochs | 60.10% (std 0.00) | T3 / TriCL Cora-CA / 63.4 ± 3.9 | -3.30%p; preliminary, not 20-split comparable | `.agents/env-status/checker-tricl-cora-coauth-2026-09-10.log` | smoke-pass |
| SEHSSL | node | cora_coauth (Cora-CA) | GPU0; 1 seed; 15 epochs | no metric; `SEHSSL/config.yaml` missing | T3 / SE-HSSL Cora-CA / 63.9 ± 5.0 | execution blocked before data/model setup | `.agents/env-status/checker-sehssl-cora-coauth-2026-09-10.log` | failed-code |
| UniGCN2 | node | cora_coauth (Cora-CA) | GPU0; 1 seed; 15 epochs | 22.33% (std `nan`, expected for one seed) | T3 / UniGCN2 Cora-CA / 55.3 ± 5.3 | -32.97%p; preliminary, not 20-split comparable | `.agents/env-status/checker-unigcn2-cora-coauth-2026-09-10.log` | smoke-pass |
| H-GD (GGD) | hyperedge prediction | cora_coauth (Cora-CA) | GPU0; 1 seed; 15 epochs; p_e=0.1, p_x=0.1 | AUROC 54.30% (std 0.00) | T4 / GGD Cora-CA / 73.2 ± 4.0 | -18.90%p; preliminary, not 20-split comparable | `.agents/env-status/checker-h-gd-edge-cora-coauth-2026-09-10.log` | smoke-pass |
| UniGIN | node | cora_coauth (Cora-CA) | GPU0; 1 seed; 15 epochs | 50.85% (std `nan`, expected for one seed) | T3 / UniGIN Cora-CA / 49.2 ± 6.9 | plausible smoke result; not 20-split comparable | `.agents/env-status/checker-unigin-remediation-2026-09-10.md` | smoke-pass |
| UniGCN | node | cora_coauth (Cora-CA) | GPU0; 1 seed; 15 epochs | 40.31% (std `nan`, expected for one seed) | T3 / UniGCN Cora-CA / 46.3 ± 6.6 | preliminary; not 20-split comparable | `.agents/env-status/checker-restored-runners-2026-09-10.md` | smoke-pass |
| Hypeboy | node | cora_coauth (Cora-CA) | GPU0; bounded recovered runner | 63.19% | T3 / HypeBoy Cora-CA / 67.0 ± 3.7 | preliminary configuration; not benchmark comparable | `.agents/env-status/checker-restored-runners-2026-09-10.md` | smoke-pass |
| VilLain | community detection | cora_coauth (Cora-CA) | CUDA; 10 epochs; train → concat → eval | NMI 9.45 | T5 / VilLain Cora-CA / 9.73 | smoke-pass; short configuration is not a Table 5 reproduction | `.agents/env-status/checker-villain-fix-2026-09-10.md` | smoke-pass |
| PhenomNN | node | cora_coauth (Cora-CA) | GPU0; 1 seed; 15 epochs | 49.06% (std `nan`, expected for one seed) | T3 / PhenomNN Cora-CA / 56.2 ± 6.6 | smoke-pass; not 20-split comparable | `.agents/env-status/checker-phenomnn-remediation-2026-09-10.md` | smoke-pass |
| MaskGAE | node | cora_coauth (Cora-CA) | GPU0; 1 seed; 15 epochs | pretraining completed; no evaluation metric (`eval_period=30`) | T3 / MaskGAE Cora-CA / 59.8 ± 4.1 | runtime smoke only; increase epoch count for comparison | `.agents/env-status/checker-maskgae-final-2026-09-10.md` | smoke-pass |
| HyperGCL | node | cora_coauth (Cora-CA) | GPU0; 1 seed bounded smoke | 11.4% (std `nan`, expected for one seed); 14.88 s | T3 / HyperGCL Cora-CA / 61.8 ± 3.0 | smoke-pass only; not benchmark-pass | `.agents/env-status/checker-hypergcl-2026-09-10.md` | smoke-pass |
| GraphMAE2 | node | cora_coauth (Cora-CA) | GPU0; 1 seed; 15 epochs | 48.4 ± 0.0 | T3 / GraphMAE2 Cora-CA / 64.3 ± 6.3 | smoke-pass; not a Table 3 reproduction | `.agents/env-status/checker-dgl-final-2026-09-10.md` | smoke-pass |
| HyperGRL | node | cora_coauth (Cora-CA) | GPU0; 1 seed; 15 epochs full flow | 42.3 ± 0.0 | T3 / HyperGRL Cora-CA / 41.8 ± 5.8 | plausible smoke result; not 20-split comparable | `.agents/env-status/checker-hypergrl-fix-2026-09-10.md` | smoke-pass |

## Recent events

| Time (KST) | From → to | Event | Outcome / next action |
|---|---|---|---|
| 2026-09-10 | clerk | Initial baseline created from the three requirement files and available run scripts. | Current environment and result reports are maintained below. |
| 2026-09-10 | env-builder → env-checker | `hgnn-pyg` CUDA/PyG hand-off passed. | Python 3.10.21, Torch 2.7.0+cu128, RTX 5080; original CUDA 11 pins remain non-viable. |
| 2026-09-10 | env-checker → env-builder | AllSet initial check. | DBLP-A missing split; Cora-CA legacy aggregation path incompatible with PyG 2.6.1 and typo `ValeuError` at `AllSet/model.py:274`. |
| 2026-09-10 | env-checker → clerk | MLP Cora-CA end-to-end smoke check. | Exit 0, 32.15% test accuracy with 1 seed/20 epochs; provisional against T3 36.0 ± 4.7. |
| 2026-09-10 | env-builder → env-checker | AllSet environment remediation. | Retained Torch 2.7/cu128; changed PyG 2.6.1 → 2.0.4 only. |
| 2026-09-10 | env-checker → clerk | AllSet Cora-CA remediation check. | Exit 0, 48.38% test accuracy with 1 seed/15 epochs; preliminary against T3 53.6 ± 8.2. DBLP-A remains `BLOCKED_DATA`. |
| 2026-09-10 | env-checker → clerk | EDHNN Cora-CA smoke check. | Exit 0, 7.56% test accuracy with 1 seed/15 epochs; executable only, not comparable to T3 36.3 ± 8.7. DBLP-A remains data-blocked. |
| 2026-09-10 | env-builder → clerk | Environment update. | `hgnn-legacy` is runtime-ready; `hgnn-dgl` remains blocked by GraphBolt/Torch 2.7 binary mismatch. |
| 2026-09-10 | env-checker → clerk | HGNN Cora-CA smoke check. | CUDA/import and model run passed; exit 0, 45.26% test accuracy with 1 seed/20 epochs, plausibly aligned with T3 44.3 ± 8.0. |
| 2026-09-10 | env-checker → clerk | HNHN Cora-CA smoke check. | Exit 0, 48.51% with 1 seed/15 epochs; preliminary against T3 53.1 ± 7.4. |
| 2026-09-10 | env-checker → clerk | H-GD Cora-CA smoke check. | `hgnn-pyg` imports passed; Cora-CA exit 0, 30.23% with 1 seed/15 epochs, -1.97%p versus T3 GGD 32.2 ± 6.3. `dblp_coauth`, `news`, and `cora_cite` are data-blocked by missing files. |
| 2026-09-10 | env-checker → clerk | HyperGCN Cora-CA smoke check. | `hgnn-pyg` imports and Cora-CA GPU0 run passed; exit 0, final test 24.77% with 1 seed/20 epochs, -20.23%p versus T3 45.0 ± 9.5. DBLP-A is data-blocked by its missing split. |
| 2026-09-10 | env-checker → clerk | PhenomNN Cora-CA smoke check. | Imports passed, but Torch 2.7 rejects `ReduceLROnPlateau(verbose=...)` before training. No metric; environment downgrade is not applied because `hgnn-pyg` is shared. |
| 2026-09-10 | env-checker → clerk | MaskGAE/TriCL preflight and Cora-CA smoke. | MaskGAE source lacks `maskgae/model.py` and `maskgae/utils.py`; TriCL imports and Cora-CA GPU0 smoke passed, 60.10% with one seed/15 epochs (-3.30%p from T3). |
| 2026-09-10 | env-checker → clerk | SEHSSL Cora-CA smoke preflight. | The CLI and dependencies are present, but the required `SEHSSL/config.yaml` is absent before data/model setup. No metric; source/config restoration required. |
| 2026-09-10 | env-checker → clerk | UniGCN2 Cora-CA smoke check. | `hgnn-legacy` imports and GPU0 run passed; final test 22.33% with one seed/15 epochs, -32.97%p versus T3 55.3 ± 5.3. |
| 2026-09-10 | env-checker → clerk | H-GD Cora-CA hyperedge smoke check. | GPU0 run passed; test AUROC 54.30% with one seed/15 epochs, -18.90%p versus T4 GGD 73.2 ± 4.0. |
| 2026-09-10 | env-builder → clerk | DGL terminal assessment. | GraphMAE2/HyperGRL GPU execution `BLOCKED_ENV`: DGL GraphBolt supports only Torch 2.0–2.2; source build requires missing CMake and CUDA ≥12.8. |
| 2026-09-10 | user → env-checker | UniGIN GPU smoke authorization rejected. | `BLOCKED_PERMISSION`, not a technical failure; no retry. |
| 2026-09-10 | env-builder → env-checker | `hgnn-hypergcl` prepared. | CUDA smoke passed; execution remains deferred by HyperGCL-last policy. |
| 2026-09-10 | user → env-checker | UniGIN GPU smoke authorized. | Replaces prior approval block; checker may execute. |
| 2026-09-10 | user → clerk | AllSet DBLP-A deferred; DGL remediation active. | Do not run the missing-split AllSet case; builder continues GraphMAE2/HyperGRL environment repair. |
| 2026-09-10 | env-checker → clerk | UniGIN Cora-CA smoke check. | Exit 0, 50.85% with 1 seed/15 epochs; plausible vs T3 49.2 ± 6.9, but not benchmark comparable. |
| 2026-09-10 | user → checker | Runners restored from user-provided Drive. | Hypeboy, UniGCN, and VilLain files were recovered rather than locally reconstructed; runtime checks pending. |
| 2026-09-10 | env-checker → clerk | Recovered runner validation. | UniGCN 40.31% and Hypeboy 63.19% Cora-CA smoke-pass; VilLain hits checkpoint/path code defects, not an environment failure. |
| 2026-09-10 | user → builder/checker | VilLain minimal source fix authorized. | Scope: pre-1000-epoch `best_model` initialization and repo-relative embedding path only; record subsequent smoke result. |
| 2026-09-10 | env-builder → clerk | DGL source-build remediation. | `hgnn-dgl-src` has CUDA 12.8.2, nvcc 12.8.93, CMake, Ninja; root CUDA objects compile, blocked by GraphBolt/Torch probe selecting system CUDA 12.0 header. |
| 2026-09-10 | env-checker → clerk | VilLain authorized-fix smoke check. | CUDA 10-epoch train→concat→eval passed; repo-local embedding output and NMI 9.45. This is provisional, not a Table 5 reproduction. |
| 2026-09-10 | env-builder → env-checker | DGL source remediation accepted. | DGL 2.1.0 source build with CUDA 12.8/sm120 passed `dgl.graphbolt` import and RTX 5080 `copy_u_sum` CUDA operation (sum 4.0); GraphMAE2 then HyperGRL smoke runs started. |
| 2026-09-10 | env-checker → clerk | DGL model validation completed. | GraphMAE2 48.4 ± 0.0; HyperGRL 42.3 ± 0.0 after scoped checkpoint-load compatibility patch. Both are Cora-CA 1-seed/15-epoch smoke results. |
| 2026-09-10 | env-builder/checker → clerk | PhenomNN remediation and MaskGAE/SEHSSL Drive audit started. | Track only provenance-confirmed restored files; similarly named candidates remain unverified. HyperGCL stays last. |
| 2026-09-10 | env-builder → clerk | PhenomNN fix and Drive audit evidence. | Minimal scheduler change compiled; SEHSSL config is a matching-source candidate but un-restored; MaskGAE required modules have no Drive copy. |
| 2026-09-10 | env-checker → clerk | PhenomNN remediation check. | Cora-CA exit 0, 49.06% with 1 seed/15 epochs; smoke-pass only. |
| 2026-09-10 | user → builder/checker | MaskGAE audit correction and source restoration. | Exact original modules found in nested Drive folder, restored, and `py_compile` passed; runtime validation pending. |
| 2026-09-10 | env-checker → clerk | SEHSSL and MaskGAE recovery smoke. | SEHSSL config restored but preprocessing timed out at 90s without model output; MaskGAE passed after `texttable` install, with eval unavailable inside 15-epoch smoke. |
| 2026-09-10 | user → env-checker | HyperGCL execution authorized. | Final model moved from deferred to running; O.O.M/O.O.T skip policy remains in force. |
| 2026-09-10 | env-checker → clerk | HyperGCL final-order Cora-CA smoke. | Exit 0, 11.4% with 1 seed, 14.88 s; smoke-pass only against T3 61.8 ± 3.0. |
| 2026-09-11 | clerk | Formal-results ledger created. | Table 3/4/5 formal rows are separated from smoke evidence; no 20-split formal result has been recorded yet. |

See [clerk protocol](../clerk.md) for the update contract and
[event log](events.md) for append-only detail.
