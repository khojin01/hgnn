# Checker report — MaskGAE and SEHSSL recovery audit

Timestamp: 2026-09-10 KST

Scope: current checkout, local user-provided Drive download at
`/home/dms2/hojin_workspace/CoTeach_upload/drive_download/`, runner imports,
and available local Git metadata. No file was restored or edited.

## MaskGAE — confirmed exact-source candidates; still BLOCKED_SOURCE

Current `MaskGAE/MaskGAE_train.py` imports:

```python
from maskgae.utils import tab_printer, get_dataset
from maskgae.model import MaskGAE, DegreeDecoder, EdgeDecoder, GNNEncoder
from maskgae.mask import MaskEdge, MaskPath
```

The local checkout lacks all three corresponding source files:

| Missing local file | Exact Drive candidate |
|---|---|
| `MaskGAE/maskgae/model.py` | `.../drive_download/MaskGAE/maskgae/model.py` |
| `MaskGAE/maskgae/utils.py` | `.../drive_download/MaskGAE/maskgae/utils.py` |
| `MaskGAE/maskgae/mask.py` | `.../drive_download/MaskGAE/maskgae/mask.py` |

Provenance evidence:

- Local and Drive `MaskGAE_train.py` hashes are identical:
  `4fddf843b1b969799ed0653c784fc399c5a08f95c2d10994e0d5efe482b66fbc`.
- Existing local/Drive `maskgae/logreg.py` and `loss.py` hashes are identical.
- Drive candidates compile and expose exactly the runner's required APIs:
  `MaskGAE`, `DegreeDecoder`, `EdgeDecoder`, `GNNEncoder`, `get_dataset`,
  `tab_printer`, plus `MaskEdge`/`MaskPath` in the corresponding mask module.
- Matching `.pyc` filenames are already present locally, corroborating the
  same missing source names but not used as a recovery source.

Status: candidate provenance is sufficient for an authorized exact-file
restore; no similarly named substitute is proposed.

## SEHSSL — confirmed exact-source candidate; still BLOCKED_CONFIG

`SEHSSL/SEHSSL_train.py:377` unconditionally reads
`SEHSSL/config.yaml` and accesses the selected dataset's `batch_size`. The
local checkout lacks this configuration. The Drive candidate is:

```text
/home/dms2/hojin_workspace/CoTeach_upload/drive_download/SEHSSL/config.yaml
```

It contains the required Cora-CA entry:

```yaml
cora_coauth:
  batch_size: 2048
  batch_size_2: null
```

Provenance evidence:

- Local and Drive `SEHSSL_train.py` hashes are identical:
  `054d6b13fcc75c3f615fa7974cf22e87a9f5641ae9b40609494cb62168746fe3`.
- All eight present helper modules (`contrast_loss`, `evaluation`, `fairaug`,
  `layers`, `logreg`, `sample_generator`, `tricl_encoder`, `utils`) have
  identical local/Drive SHA-256 hashes.
- The Drive folder's shell scripts and README share the same model layout.

Status: candidate provenance is sufficient for an authorized exact-file
restore; no inferred configuration values are needed.

## Required next decision

Root/user authorization is required before copying the three MaskGAE sources
and/or SEHSSL `config.yaml` into this checkout. After restoration, env-checker
will compile then run Cora-CA GPU smoke tests under the mapped PyG environment.
