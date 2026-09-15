# Checker report — missing-entrypoint re-audit

Timestamp: 2026-09-10 KST

Scope: local files, runner scripts, README references, bytecode names, and
the nested `VilLain/.git` index. No files were restored or modified.

| Model | Expected entrypoint | Exact audit result | Status |
|---|---|---|---|
| UniGCN | `UniGCN/UniGCN_train.py` | `118.sh`, `exp_node.sh`, and `exp_edge.sh` all call this file, but it is absent. Present files are only `util.py` plus `model.cpython-39.pyc` / `util.cpython-39.pyc`; no runner, parser, or equivalent train script exists. `UniGCN2_train.py` is a distinct sibling implementation and must not be substituted as a UniGCN result. | `BLOCKED_SOURCE` |
| Hypeboy | `Hypeboy/Hypeboy_train.py` | Both `118.sh` and `time_node.sh` call this absent file. `src.py` is helper/training-function code with no CLI parser or `__main__`; `HNNs.cpython-39.pyc` is a model-class artifact, not an executable runner. | `BLOCKED_SOURCE` |
| VilLain | `VilLain/main.py`, then `emb_concat.py` / `eval.py` | All local scripts and README point to absent files. The nested Git index lists `code/main.py` and `code/emb_concat.py`, but `git show :code/main.py` and `git show :code/emb_concat.py` fail with `fatal: bad object`; `eval.py` is absent even from the index. Git history is also unusable (`bad object refs/remotes/origin/main`). There is no usable equivalent runner. | `BLOCKED_SOURCE_REPOSITORY` |

Required remedy: obtain the predecessor's complete source checkout or the
missing runner files (and VilLain evaluation script/data contract). This is
not solvable by Conda dependency changes. Do not reconstruct a runner from
bytecode or copy a sibling model without root authorization.
