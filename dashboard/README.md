# HGNN task dashboard

`smoke_run.md`를 5분마다 스냅샷으로 집계하여 Node classification, Edge prediction,
Community detection 탭으로 보여준다. 서버는 `GET /api/state`와 외부 자동화용
`POST /api/webhook`을 제공한다.

```bash
python3 dashboard/collector.py
python3 dashboard/server.py --port 8765
```

## 자동 갱신 (1분마다)

`state.json`은 `collector.py`가 만들고, 화면은 그걸 10초마다 다시 읽는다.
`collector.py`는 혼자 돌지 않는다. 원장을 쓰는 단계가 먼저 끝나야 하므로
`tools/refresh_all.sh`가 파이프라인 전체를 한 줄로 이어서 돌린다. cron이 1분마다 부른다.

```
* * * * * /home/dms2/hojin_workspace/hgnn/tools/refresh_all.sh
```

`refresh_all.sh`가 순서대로 하는 일 (전부 합쳐 0.3초쯤):

1. `clerk_refresh.py` — `results/` · `full-runs/` → `experiment_now.md` (원장)
2. `collector.py` — 원장 → `state.json`, 그리고 논문 기준값 대조
3. `build_report.py` — `state.json` → `hypergc-report.html`
4. `vault_build.py` — `state.json` · 서버 상태 → `vault/` 노트 · `live.json`
5. `git` — 내용이 바뀐 노트만 커밋·푸시

그 밖에:

- `flock`으로 겹쳐 도는 것을 막고, 앞 단계가 실패하면 뒤 단계를 돌리지 않는다
- `paper_reference.json`이 없을 때만 PDF에서 논문 기준값을 다시 뽑는다
- 결과를 `dashboard/pipeline.log`에 한 줄씩 남기고, 400줄만 유지한다

cron은 대화형 셸의 PATH를 물려받지 않으므로 `python3`를 절대 경로로 부른다.

### 확인과 조작

```bash
tail -f dashboard/pipeline.log    # 갱신 이력
tools/refresh_all.sh              # 즉시 한 번 갱신
crontab -l                        # 등록 상태
```

로그는 이런 모양이다.

```
2026-09-12 21:24:57  OK 논문 대조: 120/120 일치 · 불일치 0
2026-09-12 21:30:01  SKIP 이전 실행이 아직 돌고 있음
```

`불일치`가 0이 아니면 원장의 Δ가 논문값과 어긋난 것이다. 화면의 **기준값 불일치**
섹션에 어느 칸인지 나온다.

### 자동화되지 않는 것

- **아티팩트**는 발행에 Claude 도구가 필요해 cron이 못 한다. 갱신이 필요하면 요청한다.
- **논문 기준값**은 `paper_reference.json`이 이미 있으면 다시 뽑지 않는다.
  `HyperGC.pdf`가 바뀌면 `python3 dashboard/paper_reference.py`를 직접 돌린다.
- **대시보드 서버**(`server.py`)는 이 스크립트가 관리하지 않는다. 죽으면 다시 띄운다:
  `setsid nohup python3 dashboard/server.py > /tmp/clerk-dashboard.log 2>&1 &`

### 아티팩트 자동 갱신 — 어디까지 되나

발행에는 Claude의 Artifact 도구가 필요하다. 그래서 작업을 둘로 나눴다.

| 단계 | 누가 | 비용 | 지속성 |
|---|---|---|---|
| 원장 · `state.json` · 리포트 · 노트 생성 | cron → `refresh_all.sh` | 없음 | 재부팅 후에도 유지 |
| 아티팩트 발행 | Claude 세션 | 매 실행마다 토큰 | **세션이 살아 있는 동안만** |

앞 단계는 `refresh_all.sh`가 1분마다 한다. 그래서 **디스크의 리포트 HTML은 항상
최신**이고, 발행은 한 번의 도구 호출로 끝난다.

발행 자동화의 한계:

- `CronCreate`로 건 예약은 **세션 전용**이다. Claude를 닫으면 사라지고, 7일 후
  자동 만료된다.
- 클라우드 예약(`/schedule`)은 오래 살지만 **클라우드에서 돌기 때문에 이 서버의
  파일을 읽지 못한다.** 로컬에서 만든 HTML을 발행할 방법이 없다.
- 아티팩트 페이지가 스스로 갱신할 수도 없다. 샌드박스가 `localhost:8765`로
  나가는 요청을 막는다.

그래서 실용적인 운영 방식은 이렇다.

```bash
# 언제든 최신 리포트를 발행하고 싶을 때 — 파일은 이미 최신이다
#   Claude에게: "아티팩트 갱신해줘"
```

**대시보드는 이 제약과 무관하다.** 브라우저가 `/api/state`를 10초마다 다시 읽으므로,
탭만 열어두면 30분 안에 새 결과가 올라온다. 공유 스냅샷이 필요할 때만 발행하면 된다.

### 구성 파일 (갱신 경로)

```
.agents/clerk-reports/experiment_now.md   원장 (clerk가 갱신)
        ↓  collector.py  (+ paper_reference.json 로 논문 대조)
dashboard/state.json                      대시보드가 읽는 스냅샷
        ↓  build_report.py (+ report_template.html)
dashboard/hypergc-report.html             아티팩트로 발행할 정적 리포트
```
