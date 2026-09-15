# Hyperedge Prediction env-checker report

- 점검 시각: 2026-09-12 KST
- 점검 범위: 19개 모델, 제공된 11개 데이터셋 및 우선 집계 대상 6개 데이터셋
- 원칙: 기존 정식 결과는 재실행하지 않았으며 소스, 결과 파일, 기존 traceback만 대조했다.

## 결론

현재 정식 20-seed 결과 파일이 확인된 모델은 MLP, UniGCN, UniGIN, GraphMAE2의 4개이며, 각 모델은 Citeseer, Cora-CA, IMDB, House, Pubmed, AMiner 6개를 완료했다. 따라서 우선 대상은 24/114 셀이 완료됐다. H-GD Cora-CA 결과는 1 seed smoke이므로 정식 완료로 세지 않는다.

기존 GPU 큐는 현재 실행 중이지 않다. `status.tsv`가 비어 있는 이유는 모델 프로세스가 결과를 저장한 뒤 `NameError` 또는 누락 데이터로 비정상 종료했고, 외부 실행 세션이 wrapper의 상태 기록/다음 모델 시작 전에 종료됐기 때문이다. 모델 단위 shell 전체를 하나의 `conda run`으로 감싸지 말고, 데이터셋별 명령을 독립 `setsid` 작업으로 실행해 종료 코드를 즉시 기록해야 한다.

## 데이터 공통 장애

공용 `dataset.py`는 로드시 `data/<dataset>/data_split_0.01.pickle`과 `edge_bucket.pickle`을 모두 요구한다.

| 데이터셋 | 누락/불일치 | 기존 traceback | 권장 해결 |
|---|---|---|---|
| `cora_cite` | `X.pt`, `data_split_0.01.pickle` 없음 | `FileNotFoundError: data/cora_cite/X.pt` | 원본 Drive에서 해당 파일 복구 후 shape/split 20개 검증 |
| `dblp_copub` | `data_split_0.01.pickle` 없음 | `FileNotFoundError: data/dblp_copub/data_split_0.01.pickle` | 원본 Drive에서 복구. NC 보류와 별개로 EP 실행에도 split이 필요 |
| `dblp_coauth` | `X.pt` 없음 | `FileNotFoundError: data/dblp_coauth/X.pt` | 원본 Drive에서 복구 |
| `modelnet_40` | `edge_bucket.pickle` 없음 | `FileNotFoundError: data/modelnet_40/edge_bucket.pickle` | 원본 Drive에서 원본 split 복구. 임의 생성 시 논문 Table 4와 직접 비교 금지 |
| `news` | `edge_bucket.pickle` 없음; `edge_bucket_match.pickle`만 존재 | `FileNotFoundError: data/news/edge_bucket.pickle` | Drive 원본과 hash/내용을 비교해 동일 파일이면 명시적 alias 또는 loader fallback. 검증 전 단순 rename 금지 |

재현 명령:

```bash
conda run --no-capture-output -n hgnn-pyg python MLP/MLP_train.py --data modelnet_40 --num_seeds 20 --lr 0.01 --device cuda:1 --task edge
conda run --no-capture-output -n hgnn-pyg python MLP/MLP_train.py --data news --num_seeds 20 --lr 0.001 --device cuda:1 --task edge
```

## 결과 저장 후 `NameError`

아래 모델은 edge 결과 파일을 먼저 저장하지만, `start`/`end`는 node 분기에서만 정의하고 공통 후처리에서 `end-start`를 사용한다. 따라서 정상 수치가 있어도 프로세스 종료 코드는 1이다.

- MLP, UniGCN, UniGIN: 기존 로그에서 실제 traceback 확인.
- 동일 구조로 정적 확인: UniGCN2, HGNN, HNHN, ED-HNN, AllSet, HyperGCN, PhenomNN, MaskGAE, HyperGCL.
- 예: `MLP_train.py:228 NameError: name 'end' is not defined`.
- PhenomNN은 추가로 결과 파일명이 `result_<data>_PhenomNN.txt`라 node와 edge가 같은 파일에 섞인다.
- SE-HSSL은 edge 결과를 모든 데이터셋 공통 `result_SEHSSL_edge.txt`에 누적한다.

권장 해결: 프로그램 시작에 `run_started = time.time()`을 두고 종료 시 `time.time() - run_started`를 기록하거나, 시간 기록을 node 분기 안으로 제한한다. 결과 파일은 반드시 `result_<data>_<model>_<task>.txt`로 통일한다.

재현 명령:

```bash
conda run --no-capture-output -n hgnn-pyg python MLP/MLP_train.py --data citeseer_cite --num_seeds 1 --lr 0.01 --device cuda:1 --task edge
```

예상: 결과 출력/저장 후 `NameError: name 'end' is not defined`.

## 19개 모델 지원 및 저장 점검

| 모델 | `--task edge` 실행 가능성 | 20-seed 저장 | 현재 판정 및 env-builder 조치 |
|---|---:|---:|---|
| AllSet | 지원 | 지원 | edge 분기 존재. `end/start` 후처리 수정 후 실행 |
| ED-HNN | 지원 | 지원 | edge 분기 존재. `end/start` 후처리 수정 후 실행 |
| H-GD | 지원 | 지원 | **edge 분기 존재**. Cora-CA 1-seed smoke 54.3만 존재; 정식 20-seed 명령 추가 필요 |
| GraphMAE2 | 지원 | 지원 | 6개 우선 데이터셋 정식 완료. 누락 데이터만 복구 후 나머지 실행 |
| HGNN | 지원 | 지원 | edge 분기 존재. `end/start` 후처리 수정 후 실행 |
| HNHN | 지원 | 지원 | edge 분기 존재. `end/start` 후처리 수정 후 실행 |
| HypeBoy | 지원 | 20개 hard-coded | `task=edge` 분기 존재하고 `edge_bucket`을 직접 사용. dataset별 실행 스크립트와 표준 결과명 필요 |
| HyperGCN | 지원 | 지원 | edge 분기 존재. `end/start` 후처리 수정 후 실행 |
| HyperGCL | 지원 | 지원 | edge 분기 존재. GPU sampler 경로 사용 가능. `end/start` 후처리 수정; 가장 늦게 실행 권장 |
| HyperGRL | **미지원** | 미지원 | parser에 `--task`가 없고 `if True`, `args.task='node'`로 강제. 현재 코드는 node label hyperedge classification이며 membership EP가 아님 |
| MLP | 지원 | 완료 6/6 | 6개 결과 보존. `end/start`만 수정; 완료분 재실행 금지 |
| MaskGAE | 지원 | 지원 | edge 분기 존재. `end/start` 후처리 수정 후 실행 |
| PhenomNN | 지원 | 지원 | edge 분기 존재. dense incidence/adjacency로 대형 데이터 OOM 위험. 시간 변수와 task별 파일명 수정 |
| SE-HSSL | 지원 | 지원 | edge 분기 존재. `--num_seeds 20` 필요. 전처리 시간/메모리 주의; dataset별 결과명으로 수정 |
| TriCL | **도달 불가** | 현재 불가 | parser에 `--task`가 없고 `if True`, `args.task='node'`. edge 구현 자체는 존재하므로 분기를 복구하고 결과 path 주석 해제 |
| UniGCN | 지원 | 완료 6/6 | 6개 결과 보존. `end/start`만 수정; 완료분 재실행 금지 |
| UniGCN2 | 지원 | 지원 | edge 분기 존재. `end/start` 후처리 수정 후 실행 |
| UniGIN | 지원 | 완료 6/6 | 6개 결과 보존. `end/start`만 수정; 완료분 재실행 금지 |
| VilLain | 임베딩만 지원 | 평가 불가 | `main.py`는 split별 edge embedding을 저장하지만 `eval.py`가 `if True`로 node만 실행하고 edge evaluator가 주석 처리됨. `edge.sh`의 merge/eval 호출도 전부 주석 |

## 모델별 핵심 재현/수정 지침

### H-GD

기존 오판과 달리 `H-GD_train.py`의 `else`가 edge 학습/평가를 수행한다.

```bash
conda run --no-capture-output -n hgnn-pyg python H-GD/H-GD_train.py --data cora_coauth --task edge --num_seeds 1 --epochs 1 --device cuda:1
```

기존 smoke 결과: `results/result_cora_coauth_HGD_edge.txt`, 1 seed 54.3. 정식 실행에는 `--num_seeds 20 --epochs 200`과 논문/118 설정을 사용한다.

### TriCL

현재 `TriCL_train.py`는 `--task` parser가 없고 `if True: #node`이며 내부에서 `args.task="node"`를 대입한다. 아래 명령은 `unrecognized arguments: --task edge`가 예상된다.

```bash
conda run --no-capture-output -n hgnn-pyg python TriCL/TriCL_train.py --data cora_coauth --task edge --num_seeds 1 --device 1
```

수정 권고: parser choices `node,edge`; `if args.task == "node"`; edge 결과를 `results/result_<data>_TriCL_edge.txt`로 저장. edge 분기의 `params['epochs']` 존재 여부도 각 config에서 검증한다.

env-builder의 1차 분기 복구 후 격리 smoke에서 추가 오류가 확인됐다. Cora-CA 원본 `data.num_edges`는 1072지만 `edge_splits[0][3]`의 최대 hyperedge id는 1207이다. split graph를 대입한 뒤 `data.num_edges`를 다시 계산하지 않아 `valid_node_edge_mask`의 `scatter_add(..., dim_size=1072)`에 1207 인덱스가 들어가 CUDA device-side assert가 발생한다. 각 seed 시작 시 아래 갱신이 필요하다.

```python
data.hyperedge_index = edge_split[3].to(args.device)
data.num_edges = int(data.hyperedge_index[1].max()) + 1
```

실패 로그: `/tmp/hgnn-tricl-edge-check.uzmg0T/run.log`.

### HyperGRL

```bash
conda run --no-capture-output -n hgnn-dgl-src python HyperGRL/HyperGRL_train.py --data cora_coauth --task edge --num_seeds 1 --device cuda:1
```

현재는 `unrecognized arguments: --task edge`. 단순히 `if True`만 바꾸면 안 된다. 현재 HyperGRL의 `getData`는 node labels로 hyperedge graph classification을 구성하므로, 공용 `edge_splits`의 node-hyperedge membership AUROC 평가기를 연결해야 한다. 원본 Drive에서 edge 구현/스크립트를 먼저 찾고, 없으면 다른 self-supervised 모델과 동일한 `MLP_HENN` 평가 프로토콜을 이식한다.

### VilLain

`VilLain/main.py --task edge`는 20개 split embedding을 만들 수 있으나, `VilLain/eval.py --task edge`는 현재도 node branch로 들어가 merge된 node embedding을 요구한다. `edge.sh` 역시 `emb_concat.py`와 `eval.py` 호출이 주석이다. 원본 Drive에서 완성된 edge 평가판을 우선 복구하고, 없으면 split별 embedding을 해당 split의 `edge_splits`와 `MLP_HENN`에 전달해 AUROC를 20개 집계한다.

### HypeBoy

edge 구현은 정상적으로 존재하지만 별도 formal runner가 없다. `edge_bucket` 20개를 hard-code하여 `--num_seeds`를 무시하고, 모든 데이터셋을 `result_Hypeboy_edge.txt`에 합친다. dataset별 20-split 결과가 구분되도록 표준 저장명을 추가한다.

## 큐 재구성 권고

1. 원본 Drive에서 5개 누락/불일치 데이터 파일과 HyperGRL/TriCL/VilLain 원본 edge 코드를 먼저 조사한다.
2. 결과가 이미 존재하는 MLP, UniGCN, UniGIN, GraphMAE2의 우선 6개 셀은 skip한다.
3. 데이터셋별 독립 명령으로 실행하고 각 명령 직후 `model, dataset, exit_code, result_path, seed_count`를 TSV에 기록한다.
4. 파일 존재만으로 완료 판정하지 말고 결과 배열 길이가 정확히 20인지 검사한다.
5. 빠른 모델부터 UniGCN2, HGNN, HNHN, ED-HNN, AllSet, HyperGCN 순으로 실행하고, self-supervised/고비용 모델을 H-GD, MaskGAE, HypeBoy, PhenomNN, SE-HSSL, TriCL, VilLain, HyperGRL, HyperGCL 순으로 후속 실행한다.

## 확인된 정식 결과 파일

- MLP: 6개 (`citeseer_cite`, `cora_coauth`, `imdb`, `house`, `pubmed_cite`, `aminer`)
- UniGCN: 6개
- UniGIN: 6개
- GraphMAE2: 6개
- H-GD: Cora-CA 1개 파일은 1-seed smoke이므로 정식 결과가 아님

## env-builder 수정 재검증

- 수정 후 검증 시각: 2026-09-12 KST
- 격리 경로: `/tmp/hgnn-edge-check.qJdXu0` (운영 결과 미변경)
- 명령: `python UniGCN2/UniGCN2_train.py --data citeseer_cite --num_seeds 1 --lr 0.001 --device cuda:1 --task edge`
- 결과: `EXIT_CODE=0`, `result_citeseer_cite_UniGCN2_edge.txt` 생성, test AUROC 62.23.
- 판정: edge 결과 저장 후 `end/start NameError`는 제거됐다. 1 seed의 표준편차가 `nan`인 경고는 정상이며 정식 20-seed에서는 발생하지 않는다.

### TriCL 2차 수정 검증

- 격리 경로: `/tmp/hgnn-tricl-edge-check2.Ia74vH` (운영 결과 미변경)
- 명령: `python TriCL/TriCL_train.py --data cora_coauth --task edge --num_seeds 1 --epoch 1 --device 1`
- 실제 동작: edge branch는 config의 200 pretrain epochs와 1,000-epoch membership evaluator를 수행했다 (`--epoch 1`은 현재 edge branch에서 사용되지 않음).
- 결과: `EXIT_CODE=0`, `results/result_cora_coauth_TriCL_edge.txt` 생성, 1-seed AUROC 84.2.
- 판정: task 분기, split별 `num_edges` 갱신, 평가 및 표준 결과 저장까지 정상. 정식 20-seed 실행 가능 상태다.

### VilLain edge evaluator 복구 검증

- 검증 시각: 2026-09-13 01:15 KST
- 격리 경로: `/tmp/hgnn-villain-edge-check.gRKkun`
- 명령: `python VilLain/eval.py --data cora_coauth --num_seeds 1 --task edge --device 1 --num_step 4 --num_step_gen 10 --lr 0.001`
- 방법: 운영 edge embedding이 아직 없으므로 기존 node embedding 하나를 임시 `split0_...` 이름으로 연결했다. 이는 파일 발견, split별 PCA, 기존 membership predictor, AUROC 집계, 표준 결과 저장 경로만 검증하기 위한 것으로 수치 재현 검증이 아니다.
- 결과: `EXIT_CODE=0`, 1-split AUROC 76.4, 격리된 `results/result_cora_coauth_VilLain_edge.txt` 생성.
- gate: `.agents/env-status/villain-edge-check.ok` 생성. 정식 실행은 반드시 `main.py --task edge`가 생성한 split별 실제 임베딩을 사용해야 한다.

## 2026-09-13 정식 큐 독립 감사

### 완료 및 형식 검증

아래 모델의 6개 우선 데이터셋 결과는 각 파일의 최종 배열이 정확히 20개이고, trainer의 edge evaluator가 `roc_auc_score`를 반환하며, 경로가 `results/result_<dataset>_<model>_edge.txt`임을 확인했다.

- UniGCN2: 6/6, 모두 20 AUROC.
- HGNN: 6/6, 모두 20 AUROC.
- HNHN: 6/6, 모두 20 AUROC.
- ED-HNN: 6/6, 모두 20 AUROC.
- AllSet: 6/6, 모두 20 AUROC.
- H-GD: 6/6, 최종 정식 line은 모두 20 AUROC. Cora-CA 파일의 과거 1-seed smoke line은 최종 line이 아니므로 collector는 반드시 마지막 20-value line을 읽어야 한다.
- PhenomNN: Citeseer, Cora-CA, IMDB, House 4/5(non-OOM target)가 완료됐고 각 20 AUROC 및 표준 task 경로를 확인했다. Pubmed는 진행 중이며 AMiner는 논문 O.O.M skip이다.
- HyperGCN: Citeseer, Cora-CA, IMDB, House 4/6 완료, 각 20 AUROC. Pubmed 진행 중, 이후 AMiner 예정.

감사 시점의 실행 상태:

- GPU 0: PhenomNN Pubmed 19/20 이후 HypeBoy 6개 예정.
- GPU 1: HyperGCN Pubmed 15/20 이후 AMiner, MaskGAE 6개 예정.
- TriCL 6개 큐는 GPU 1 감독모델 큐 종료를 기다린다.

### metric 확인

- 감독 모델과 PhenomNN의 `eval_acc_edge`는 sigmoid prediction에 `sklearn.metrics.roc_auc_score`를 적용한다.
- H-GD/TriCL/GraphMAE2/MaskGAE/SE-HSSL/VilLain의 공통 membership predictor도 반환 tuple의 index 0인 AUROC를 집계한다.
- HypeBoy의 `HE_evaluator`는 직접 `roc_auc_score(labels, pred)`를 반환한다. 변수명이 `test_acc`여도 실제 지표는 AUROC다.

### 01:16 KST 증분 확인

- PhenomNN Pubmed 완료: `EXIT_CODE=0`, 최종 배열 20개, AUROC `65.1 ± 1.7`, 표준 경로 `results/result_pubmed_cite_PhenomNN_edge.txt`.
- PhenomNN 우선 대상은 논문 O.O.M인 AMiner를 제외한 5/5가 모두 완료됐다.
- HypeBoy Citeseer 정식 20-split 실행이 GPU 0에서 시작됐다. 소스상 집계 지표는 AUROC이며, 완료 후 배열 길이와 표준 파일을 다시 확인해야 한다.

### 01:19 KST 증분 확인

- HypeBoy Citeseer 완료: `EXIT_CODE=0`, 정확히 20개 split AUROC, `86.4 ± 2.1`, 표준 경로 `results/result_citeseer_cite_Hypeboy_edge.txt`.
- 출력 배열과 `np.mean`/`np.std`를 재계산 가능한 형식으로 보존한다. 다음 Cora-CA 실행이 정상 시작됐다.

### VilLain/SE-HSSL 결과 감사 보완 재검증

- VilLain은 각 split마다 정확한 `nl2..8` 7개 경로를 요구하도록 수정됐다.
- `/tmp/hgnn-villain-edge-check2.SCEDRY`에서 7개 임시 링크를 사용한 1-split 검증이 `EXIT_CODE=0`으로 통과했다.
- 표준 파일에 `split_results=[0.7637858301784748]`가 함께 저장되어 split 개수를 감사할 수 있다. 값은 임시 embedding 진단값이며 정식 결과가 아니다.
- SE-HSSL도 표준 dataset/task 파일에 `split_results` 배열과 평균·표준편차를 함께 저장하도록 정적 확인했다.
- HyperGCL 후속 큐가 기대하는 결과 stem도 잘못된 `AllDeepSets`에서 trainer의 실제 method인 `HyperGCL`로 교정됐고 `bash -n`을 통과했다.

### 01:21 KST HypeBoy 증분 확인

- Cora-CA 완료: `EXIT_CODE=0`, 20개 AUROC, `87.4 ± 1.5`, 표준 dataset/task 파일 정상.
- HypeBoy는 현재 2/6 완료(Citeseer, Cora-CA)했고 IMDB가 실행 중이다.

### 08:50 KST MaskGAE / HyperGCL 결과 보존 감사

- MaskGAE는 Citeseer, Cora-CA, IMDB, House, Pubmed, AMiner 6/6 결과 파일의 split 배열이 각각 정확히 20개임을 독립 확인했다.
- MaskGAE AUROC: Citeseer `86.7 ± 1.7`, Cora-CA `76.1 ± 2.2`, IMDB `54.5 ± 1.3`, House `88.2 ± 3.6`, Pubmed `95.5 ± 0.3`, AMiner `87.6 ± 0.9`.
- 이 6개 실행의 과거 `FAILED`는 결과 저장 이후 timing 변수 `end`를 참조하면서 발생한 `NameError`였다. 결과 배열 자체는 완전하며 재실행할 필요가 없다. 현재 소스는 timing 기록을 node task에서만 수행하도록 수정됐다.
- HyperGCL Citeseer와 Cora-CA 결과 파일의 `tensor([...])`에 각각 정확히 20개 split AUROC가 있음을 확인했다. 결과는 Citeseer `51.9 ± 2.9`, Cora-CA `51.1 ± 3.1`이다.
- HyperGCL 두 실행의 과거 `FAILED`도 결과 저장 이후 동일한 timing `NameError` 때문이며, status에는 `COMPLETE_RESULT_PRESERVED`가 후속 기록됐다. 현재 소스는 수정 완료 상태다.
- HyperGCL IMDB는 PID 1938916에서 실행 중이다. 독립 로그 감사 시 완전 종료된 outer seed는 2/20이고, 세 번째 seed는 epoch 141/200(70.5%)였다. 환산 전체 진행률은 약 `13.5%`이며, 현재 속도가 유지되면 IMDB 완료까지 약 3시간 20분이 남는다.
