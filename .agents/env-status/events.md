# Environment validation event log

Append an event for every environment build, checker run, repair request, and
benchmark comparison. Keep raw logs outside this file; link their paths here.

## 2026-09-10 KST — baseline

- Clerk created the status ledger. No environment creation, model execution, or
  performance measurement had been reported at this point.

## 2026-09-10 KST — `hgnn-pyg` hand-off, AllSet and MLP checks

- Compatibility-port `hgnn-pyg` passed CUDA/PyG runtime smoke on RTX 5080:
  Python 3.10.21 and Torch 2.7.0+cu128. The original CUDA 11 package pins are
  retained solely as provenance.
- AllSet: DBLP-A is `BLOCKED_DATA` because
  `data/dblp_copub/data_split_0.01.pickle` is absent. Its Cora-CA attempt
  reached the model then failed with legacy custom aggregation incompatibility
  under PyG 2.6.1 and typo `ValeuError` at `AllSet/model.py:274`; no metric.
  Builder changed only PyG to 2.0.4 and checker is retrying.
- MLP: Cora-CA GPU0, one seed/20 epochs, exit 0, test accuracy 32.15%. The
  `nan` standard deviation is expected for one seed. This is a smoke-pass only;
  it is provisionally compared with T3 MLP Cora-CA 36.0 ± 4.7, not a 20-split
  benchmark verification. Evidence: `checker-mlp-2026-09-10.md`.

## 2026-09-10 KST — AllSet PyG remediation result

- Builder retained Torch 2.7/cu128 and changed pure PyG from 2.6.1 to 2.0.4;
  no model code was changed.
- AllSet Cora-CA GPU0, one seed/15 epochs: exit 0 and final test accuracy
  48.38% (`nan` standard deviation is expected for one seed). This is a
  smoke-pass, preliminarily compared with T3's 53.6 ± 8.2—not a comparable
  20-split result. Evidence: `checker-allset-remediation-2026-09-10.md`.
- AllSet DBLP-A remains `BLOCKED_DATA`: its required
  `data/dblp_copub/data_split_0.01.pickle` is absent.

## 2026-09-10 KST — EDHNN smoke result and environment update

- EDHNN Cora-CA GPU0, one seed/15 epochs: exit 0 and final test accuracy
  7.56% (`nan` standard deviation expected for one seed). This proves runtime
  execution only; it is not comparable to the T3 20-split target of 36.3 ± 8.7.
  Evidence: `checker-edhnn-2026-09-10.md`. DBLP-A remains data-blocked.
- `hgnn-legacy` is ready for checker runtime tests. `hgnn-dgl` is blocked:
  its DGL GraphBolt binary does not match Torch 2.7; builder owns stack repair.

## 2026-09-10 KST — HGNN smoke result

- `hgnn-legacy` CUDA/import checks and HGNN Cora-CA GPU0 run passed: one
  seed/20 epochs, exit 0, final test accuracy 45.26% (`nan` standard deviation
  expected for one seed). The value is plausible beside T3's 44.3 ± 8.0 but is
  a smoke result, not a 20-split reproduction. Evidence:
  `checker-hgnn-2026-09-10.md`.

## 2026-09-10 KST — UniGIN and runner recovery

- UniGIN Cora-CA GPU0, one seed/15 epochs: exit 0 and final test 50.85%
  (`nan` standard deviation expected). This is a plausible smoke result beside
  T3 49.2 ± 6.9, not a 20-split reproduction. Evidence:
  `checker-unigin-remediation-2026-09-10.md`.
- User-provided Drive artifacts restored missing runners; they were not locally
  reconstructed: Hypeboy `Hypeboy_train.py`/`HNNs.py`, UniGCN
  `UniGCN_train.py`/`model.py`, and VilLain `main.py`/`emb_concat.py`/`eval.py`.
  Runtime validation for these recovered sources is pending.

## 2026-09-10 KST — recovered runner validation

- UniGCN Cora-CA GPU0, one seed/15 epochs: smoke-pass at 40.31%, compared
  preliminarily with T3 46.3 ± 6.6. Hypeboy's bounded recovered runner also
  smoke-passed Cora-CA at 63.19%, versus T3 67.0 ± 3.7. Evidence for both:
  `checker-restored-runners-2026-09-10.md`.
- VilLain reached CUDA/data execution then failed in code, not environment:
  it calls `load_state_dict(None)` because a checkpoint is assigned only after
  epoch >1000, and retains hard-coded cowbean embedding paths. No metric.

## 2026-09-10 KST — VilLain authorization and DGL source build

- User authorized a minimal VilLain fix only: initialize `best_model` for a
  pre-1000-epoch smoke, and make the former `/home/cowbean/.../embs` path
  repository-relative at `VilLain/embs`. Post-fix GPU result is pending.
- Builder created isolated `hgnn-dgl-src` with CUDA 12.8.2/nvcc 12.8.93,
  CMake, and Ninja. DGL 2.1 configuration for Torch 2.7+cu128/sm120 and root
  CUDA compilation succeed. Nested GraphBolt/Torch CMake fails because the
  Torch header probe still selects `/usr/include/cuda.h` (CUDA 12.0) rather
  than Conda CUDA 12.8. No model code has changed.

## 2026-09-10 KST — VilLain post-fix smoke result

- The authorized minimal VilLain patch compiled and preserved original full-run
  behavior. Cora-CA CUDA 10-epoch train → concat → eval completed, generated
  repo-local embeddings, and reported community-detection NMI 9.45. Record as
  `smoke-pass` only: the short configuration is not a Table 5 reproduction
  (T5 VilLain Cora-CA reference 9.73). Evidence:
  `checker-villain-fix-2026-09-10.md`.

## 2026-09-10 KST — DGL source remediation accepted

- Isolated `hgnn-dgl-src` now provides DGL 2.1.0 compiled for Torch 2.7,
  CUDA 12.8, and RTX 5080 (`sm_120`). `import dgl.graphbolt` and a CUDA graph
  `copy_u_sum` operation passed on `cuda:0` (sum 4.0).
- Runtime must set `DGL_LIBRARY_PATH=/tmp/dgl-v2.1.0-build-r5` and include that
  directory plus the environment library directory in `LD_LIBRARY_PATH`.
  GraphMAE2 bounded GPU smoke is running; HyperGRL follows it. HyperGCL remains
  deferred as the final model.

## 2026-09-10 KST — GraphMAE2 and HyperGRL smoke results

- GraphMAE2 Cora-CA GPU, one seed/15 epochs: exit 0, final accuracy 48.4 ±
  0.0. It is an end-to-end smoke-pass, not a Table 3 reproduction (reference
  64.3 ± 6.3). Evidence: `checker-dgl-final-2026-09-10.md`.
- HyperGRL initially reached the local pre-trained checkpoint and failed only
  on Torch's `weights_only` default. An authorized scoped `weights_only=False`
  checkpoint-load patch completed the Cora-CA full DGL GPU flow: one seed/15
  epochs, exit 0, final 42.3 ± 0.0. This is plausibly near T3 41.8 ± 5.8 but
  remains a smoke-pass. Evidence: `checker-hypergrl-fix-2026-09-10.md`.

## 2026-09-10 KST — PhenomNN and source-recovery work started

- PhenomNN scheduler compatibility remediation is active after Torch 2.7
  rejected the legacy `ReduceLROnPlateau(verbose=...)` call; GPU validation is
  pending.
- MaskGAE and SEHSSL Drive recovery audits are active. Missing source/config
  must be restored only when provenance confirms it matches this repository;
  similarly named candidates are explicitly not treated as recovered sources.

## 2026-09-10 KST — HNHN, DGL, UniGIN, and HyperGCL status

- HNHN Cora-CA GPU0, one seed/15 epochs: exit 0, final test 48.51%; `nan`
  standard deviation is expected for a single seed. It is a smoke-pass and
  preliminary relative to T3 53.1 ± 7.4. Evidence: `checker-hnhn-2026-09-10.md`.
- GraphMAE2 and HyperGRL are terminal `BLOCKED_ENV`: DGL 2.1 GraphBolt ships
  libraries only for Torch 2.0–2.2 and hard-loads an exact versioned `.so`;
  Torch 2.7 is unsupported. The server lacks CMake and has nvcc 12.0, while a
  native RTX 5080 source build requires newer CUDA (at least 12.8).
- UniGIN is `BLOCKED_PERMISSION`: the user rejected its GPU smoke command at
  the approval step. This is neither an environment nor model failure and must
  not be retried without authorization.
- `hgnn-hypergcl` is prepared (Python 3.10.21, Torch 2.7.0+cu128, PyG 2.0.4,
  RTX 5080 CUDA smoke pass) but remains deferred until the non-HyperGCL queue
  is terminal and GPU execution is authorized.

## 2026-09-10 KST — authorization and remediation update

- User authorized the UniGIN GPU smoke. Its previous `BLOCKED_PERMISSION`
  status is superseded; checker execution is pending.
- User explicitly deferred AllSet DBLP-A. The absent split remains evidence,
  but this dataset must not be retried in the current run.
- GraphMAE2/HyperGRL DGL remediation is active. The prior GraphBolt/Torch 2.7
  and local toolchain findings remain the current technical evidence until a
  builder update proves a compatible stack.

## 2026-09-10 KST — H-GD runtime check

- `hgnn-pyg` import checks passed for H-GD: Torch 2.7.0+cu128, PyG 2.0.4,
  torch_scatter 2.1.2+pt27cu128, and torchmetrics 1.7.4.
- Fixed-script datasets `dblp_coauth`, `news`, and `cora_cite` are
  `BLOCKED_DATA` because respectively `X.pt`, `edge_bucket.pickle`, and `X.pt`
  are missing.
- H-GD Cora-CA GPU0, one seed/15 epochs, exit 0: test accuracy 30.23% (std
  0.00). This is -1.97%p from Table 3 GGD's 32.2 ± 6.3 and remains a smoke-pass,
  not a 20-split reproduction. Evidence:
  `checker-h-gd-cora-coauth-2026-09-10.log`.

## 2026-09-12 KST — VilLain 노드 분류 분할 정정

- `VilLain/eval.py`가 노드 분할을 `data_split_118.pickle`(train 10% / valid 10% /
  test 80%)에서 직접 읽고 있었다. 저장소에서 공용 로더 `dataset.py`를 거치지 않고
  분할 파일을 여는 유일한 코드였고, 나머지 18개 모델은 모두
  `data_split_0.01.pickle`(1% / 1% / 98%)을 쓴다.
- HyperGC 논문 4장이 프로토콜을 못 박는다: "we randomly split nodes into training,
  validation, and test sets with ratios of 1%, 1%, and 98%, respectively, and report
  the average and standard deviation of accuracy over 20 random splits."
- 레이블을 10배 더 받은 탓에 Table 3 대비가 성립하지 않았다. 정정 전 기록은
  Cora-CA +25.8, Citeseer +17.9, AMiner +10.3 %p로 논문을 크게 웃돌았다.
- `eval.py`를 `--split` 인자로 바꾸고 기본값을 `0.01`로 두었다. 다른 분할로 실험하려면
  명시해야 한다. 백업: `VilLain/eval.py.bak-20260912-170535`.
- 6개 데이터셋을 재평가했다(GPU 1, 20 split). VilLain은 자기지도라 임베딩이 분할과
  무관하므로 재학습 없이 `VilLain/embs/*_merged.pkl`을 재사용하고 MLP probe만 다시
  돌렸다. 소요 약 3분.
- 결과: Cora-CA 31.4 ± 4.1, Pubmed 73.7 ± 3.3, AMiner 19.9 ± 1.2는 논문값과
  표준편차까지 일치한다. IMDB 39.2(Δ −0.5), House 49.3(Δ −1.3), Citeseer 28.5(Δ −5.1).
  Citeseer만 차이가 남아 있어 추가 확인이 필요하다.
- `experiment_now.md`의 VilLain 노드 행을 교체하고 머리말에 분할 계약을 명시했다.
  다음 담당자: 모델 코드가 분할 파일을 직접 열면 `data_split_0.01.pickle`인지 확인한다.

## 2026-09-12 KST — Table 3/4 기준값 정정 (Δ 29칸 + Table target 18칸)

- `experiment_now.md`의 Δ 29칸이 다른 모델 행의 논문값을 기준으로 계산돼 있었다.
  HyperGCN 6칸은 전부 VilLain 행 기준이어서, 실제로는 거의 완전히 재현됐는데도
  ±14 %p 어긋난 것처럼 적혀 있었다. 반대로 GGD AMiner는 −14.9 %p 미달이
  +0.2 %p로 가려져 있었다.
- `formal-results.md`의 `Table target` 열 18칸도 논문과 달랐다. 절반은 표준편차만
  어긋난 경우다(예: HGNN Citeseer 38.1 ± 8.7 → 38.1 ± 10.7).
- 측정값은 건드리지 않고 기준값만 HyperGC.pdf에서 다시 계산해 넣었다.
  백업: `experiment_now.md.bak-20260912-154333`, `formal-results.md.bak-20260912-155852`.
- 논문값은 `dashboard/paper_reference.py`가 PDF에서 기계적으로 추출해
  `dashboard/paper_reference.json`에 보관한다. 손으로 옮긴 값은 없다.
  `python3 dashboard/collector.py`가 매 갱신마다 전 칸을 대조하고 불일치를 보고한다.

## 2026-09-12 KST — Table 4 열 보강 (하이퍼엣지 예측 8칸)

- MLP·UniGCN이 6개 데이터셋(Citeseer, Cora-CA, IMDB, House, Pubmed, AMiner)의
  하이퍼엣지 예측을 끝냈는데, `experiment_now.md`의 Table 4 표에는 Cora-CA·AMiner
  열만 있어 8칸이 기록되지 못하고 있었다. 원시 결과는
  `results/result_<dataset>_<model>_edge.txt`에 모두 있었다.
- 원장 메모는 "Table 4 records the paper-comparable Cora-CA and AMiner cells"였지만,
  HyperGC 논문 Table 4는 Citeseer·IMDB·House·Pubmed에도 값을 싣는다
  (`dashboard/paper_reference.json`의 T4 참조). 네 칸 모두 대조 가능하다.
- 표를 T3와 같은 열 순서(Citeseer · Cora-CA · IMDB · House · Pubmed · AMiner ·
  DBLP-P · 20News)로 넓히고 8칸을 채웠다. 측정값은 원시 결과에서 읽고 Δ는 PDF에서
  계산했다. 기존 셀은 그대로 옮겼다. 백업: `experiment_now.md.bak-20260912-185602`.
- 결과: 12칸 전부 Δ ±1.1 이내. MLP는 Citeseer·Cora-CA·House·Pubmed·AMiner 다섯 칸이
  소수점까지 일치한다. UniGCN은 Citeseer −1.0, Pubmed −0.8이 최대 편차다.
- 다음 담당자: 표에 열이 없어 기록하지 못하는 결과가 생기면 열을 먼저 넓힌다.
  논문에 값이 있는 조합인지는 `dashboard/paper_reference.json`으로 확인할 수 있다.

## 2026-09-13 KST — 사용자 지시: smoke 기록 중단 + EP 기준표 오류 정정

### 사용자 지시 (정책 변경)

- **smoke 결과를 결과 매트릭스에 더 이상 기록하지 않는다.** 단일 seed·짧은 epoch
  결과는 논문 재현값이 아니므로 표에 올리지 않는다. 정식(`118.sh` 고정 설정 ·
  기본 200 epoch · 20 split/seed) 결과만 기록한다. 실행 가능성 확인은 로그로만
  남기고 매트릭스에는 `— pending`을 둔다.
- 이에 따라 `clerk.md`의 smoke 관련 조항(§사용자용 보고서 및 smoke 원장,
  §Roles and hand-offs 3항)은 더 이상 유효하지 않다. `clerk`는 해당 절차를
  중단하고 프로토콜 문서를 갱신한다.

### 이번에 정정한 것

- `experiment_now.md`에서 smoke 수치 2건을 제거했다.
  - Table 4 `GGD (H-GD)` 행 전체 삭제: Cora-CA smoke 54.30 한 칸만 있었고,
    같은 표의 `HGD` 행이 6개 데이터셋 정식 20-seed 결과를 갖는다. 중복이었다.
  - Table 5 `VilLain` Cora-CA: smoke NMI 9.45 → `— pending`.
- Table 4 `HGD` 행의 Δ 6칸이 **Table 3(노드 분류) 기준값**으로 계산돼 있었다.
  하이퍼엣지 예측 표인데 노드 분류 값을 뺀 것이다. 정정 결과:

  | 데이터셋 | 내 결과 | 잘못된 기준 (T3) | 올바른 기준 (T4) | Δ 정정 |
  |---|---|---|---|---|
  | Citeseer | 52.9 | 34.0 | 72.2 | +18.9 → −19.3 |
  | Cora-CA | 43.9 | 32.2 | 73.2 | +11.7 → −29.3 |
  | IMDB | 46.1 | 37.6 | 53.1 | +8.5 → −7.0 |
  | House | 50.0 | 50.6 | 87.9 | −0.6 → −37.9 |
  | Pubmed | 51.0 | 64.9 | 87.2 | −13.9 → −36.2 |
  | AMiner | 50.7 | 31.5 | 84.9 | +19.2 → −34.2 |

  부호가 뒤집혀 있었다. H-GD의 하이퍼엣지 예측은 논문보다 크게 미달인데
  원장은 "논문 초과"로 적고 있었다.

### 실행·작성 담당 에이전트에게 (env-checker / clerk)

1. **task별 기준표를 반드시 맞춘다.** 노드 분류는 Table 3, 하이퍼엣지 예측은
   Table 4, 커뮤니티 탐지는 Table 5다. 같은 모델·같은 데이터셋이어도 표마다
   값이 다르다(예: GGD Cora-CA는 T3 32.2, T4 73.2). 표를 섞으면 부호까지 뒤집힌다.
2. **모델 이름을 한 표기로 통일한다.** 같은 모델이 `HGD` / `GGD (H-GD)` /
   `H-GD (GGD)`로 섞여 적혀 표 안에 중복 행이 생겼고, 자동 대조가 이름을 못 찾아
   검증을 건너뛰었다. 논문 표기(`GGD`)를 기준으로 쓴다.
3. **결과가 있는데 표에 열이 없으면 열을 먼저 넓힌다.** Table 4의 Citeseer ·
   IMDB · House · Pubmed 8칸이 원시 결과는 있는데 열이 없어 누락됐던 적이 있다.
4. Δ를 직접 계산해 적기보다, 기준값을 `dashboard/paper_reference.json`에서
   확인한다. 이 파일은 `dashboard/paper_reference.py`가 `HyperGC.pdf`에서
   기계적으로 뽑은 것이다(T3·T4 19개 모델, T5 9개 모델).
5. `python3 dashboard/collector.py`가 매 갱신마다 전 칸을 대조하고
   `불일치 N` · `미대조 N행`을 출력한다. 0이 아니면 원장이 틀렸다는 뜻이다.
   cron이 30분마다 돌리며 `dashboard/refresh.log`에 남는다.

백업: `experiment_now.md.bak-20260913-010337`(Δ 정정),
`experiment_now.md.bak-20260913-011*`(smoke 제거).
