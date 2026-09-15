# env-checker runtime reports

This is append-only checker evidence. Individual reports contain the full
context and are linked below.

## 2026-09-10 KST — hgnn-pyg / AllSet

- Environment: `hgnn-pyg`, Python 3.10.21, Torch 2.7.0+cu128, PyG 2.6.1;
  CUDA 12.8 / RTX 5080 available. PyG compiled extensions imported.
- Result: `FAIL_ENV_COMPAT` after a data preflight failure and a subsequent
  model/API compatibility failure. No metric was produced.
- Evidence: `checker-allset-2026-09-10.md`.
- Next owner: `env-builder` to evaluate an API-compatible PyG/Torch stack or
  explicitly classify this as a required source port; `env-checker` must not
  alter source without authorization.
