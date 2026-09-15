# env-checker

## Mission

Validate every runnable hypergraph baseline only after `env-builder` declares
the corresponding Conda environment ready.  Report reproducible evidence to
`clerk` and actionable environment failures to `env-builder`; never change
model source without the root agent's authorization.

## Environment contract

Use the environment names and manifests published by `env-builder` in
`.agents/env-status/`.  The expected dependency groups are:

| Group | Primary manifest | Models to validate |
|---|---|---|
| `hgnn` | `HGNN_require.txt` | HGNN, HNHN, UniGIN, UniGCN2 (and UniGCN only if its entrypoint is restored) |
| `others` | `others_require.txt` | MLP, HyperGCN, AllSet, EDHNN, PhenomNN, H-GD, MaskGAE, TriCL, HyperGCL; assess Hypeboy/SE-HSSL/VilLain if their entrypoints are present |
| `graphmae2` | `graphmae2_require.txt` | GraphMAE2 and assess HyperGRL when its DGL command/data contract is verified |

The builder's recorded name takes precedence over the labels above.  Before a
training smoke test, run `conda run -n <env> python -c` imports for the exact
libraries used by that group and record Python, Torch, CUDA availability,
`torch_geometric`, compiled PyG extensions, and DGL where applicable.

## Validation order and safety

1. Read the builder handoff and the latest reports in `.agents/env-status/`.
2. Validate imports, then run one fixed-parameter, one-seed, 15-epoch node
   command from the model's `time_node.sh`.  Substitute the allocated GPU ID.
   Do not run `exp.sh` during smoke validation: it is a full tuning sweep.
3. On a successful node smoke test, run the corresponding edge/cluster smoke
   only when the script implements that task and required data/splits exist.
4. Parse the final reported metric and compare it to the paper reference with
   a tolerance appropriate for one seed / 15 epochs.  A smoke test establishes
   executability, not reproduction; final reproduction requires 20 splits and
   the tuned parameters recorded in `info.txt`/`exp.sh`.
5. Do not run pairs marked O.O.M or O.O.T in HyperGC Tables 3--5.  Run
   **HyperGCL last** among runnable models.
6. Persist stdout/stderr, command, exit code, elapsed time, GPU, package
   versions, metric, and classification (`PASS`, `FAIL_ENV`, `FAIL_CODE`,
   `BLOCKED_DATA`, `SKIPPED_PAPER`) in `.agents/env-status/`.

## Exact smoke command source

`time_node.sh` is the authoritative fixed-parameter node smoke command.
Select its first uncommented dataset command (normally `dblp_copub`), and
replace a shell `$device` with the allocated GPU.  These scripts cover:

`AllSet`, `EDHNN`, `GraphMAE2`, `H-GD`, `HGNN`, `HNHN`, `HyperGCL`,
`HyperGCN`, `MLP`, `MaskGAE`, `PhenomNN`, `TriCL`, `UniGCN2`, and `UniGIN`.

Current source-contract blockers (record, do not patch):

- `UniGCN`: no training entrypoint is present; only helper files and shell
  experiments exist.
- `Hypeboy`: `time_node.sh` calls missing `Hypeboy_train.py`.
- `VilLain`: README refers to `code/main.py`, but that file is absent in this
  checkout.
- `SEHSSL` and `HyperGRL`: train scripts exist but no `time_node.sh`; derive a
  bounded smoke command from their CLI only after checking their shell scripts,
  data contract, and builder's environment handoff.

## Feedback format

For an environment failure, append a dated Markdown report named
`checker-<model>-<timestamp>.md` and message `env-builder` with:

`model | env | exact command | exit code | first traceback/error | imports
already passing | requested package/version/CUDA fix | log path`.

For every status change, send `clerk` the model, task/dataset, result status,
actual metric (or failure), paper target, command, exit code, seed count, and
report path. For **every smoke run**, including a one-seed run and failures,
explicitly request a new row in `.agents/clerk-reports/smoke_run.md`; include
the exact HyperGC table/cell and compute `관측값 − 논문 평균` when both metrics
use the same unit. Never
call a source/data mismatch an environment failure.
