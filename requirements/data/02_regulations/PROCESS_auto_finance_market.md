# 프로세스: 자동차 금융 시장(오토 금융) 국가별 조사

> **목적** — 특정 국가에 대해 **오토 금융 시장의 4대 지표**(침투율 / 채널 비율 / 상품 구조 / 주요 플레이어)를 공식 출처로 조사·검증·산출하는 **반복 가능한 절차**를 정의한다. 어떤 국가든 이 문서를 그대로 따라 동일 품질·동일 축으로 조사하여, **국가 간 유사도 비교**가 성립하도록 한다.
>
> - 최초 적용 사례: 독일·스페인 → [`../../../reports/auto_finance_market_DE_ES_2025.md`](../../../reports/auto_finance_market_DE_ES_2025.md)
> - 정형 산출물 예: [`../../../mockup/auto_finance_market/auto_finance_market.json`](../../../mockup/auto_finance_market/auto_finance_market.json)
> - 유사도 설계 연계: [`../../simillarity/agent_similarity_design.md`](../../simillarity/agent_similarity_design.md)
> - 상위 제약: [`../global_constraints.md`](../global_constraints.md)

> 같은 폴더의 [`PROCESS_auto_finance_regulation.md`](PROCESS_auto_finance_regulation.md)는 **규제·세제**를 다루는 자매 프로세스다. 본 문서는 **시장 구조(침투율·채널·상품·플레이어)**를 다룬다. 두 프로세스는 동일한 deep-research 적대적 검증 방법론을 공유한다.

---

## 0. 입력 (Inputs)

| 입력 | 설명 | 예시 |
|---|---|---|
| **대상 국가** | 조사할 국가 (1개 이상) | 체코, 폴란드, 미국 … |
| **대상 연도** | 기준연도. "최신 갱신본" 원칙(미발행 시 직전 FY) | 2025 (캡티브·협회는 FY2024 결산이 최신일 수 있음) |

> 대상 국가는 [`../00_basic_information/countries.md`](../00_basic_information/countries.md)의 진출/진출예정 국가에서 고른다.

---

## 1. 조사 항목 (4대 축 — 고정)

국가가 바뀌어도 **항상 이 4개 축(dimension)**을 조사한다. 축이 국가 간 동일해야 유사도 비교가 성립한다.

| # | 축 (dimension) | 무엇을 찾는가 | 비고 |
|---|---|---|---|
| 1 | **침투율 (penetration)** | 신차/중고차 판매 중 금융(리스+할부+PCP) 이용 비율 | ⚠️ **정의(분모) 주의** — §2-A |
| 2 | **채널 비율 (channel_mix)** | 승용차(PV) 개인 vs 법인/플릿 vs 렌탈, 상용차(LCV/트럭) 비중 | 등록대수 기준이 일반적 |
| 3 | **상품 구조 (product_structure)** | 리스 vs 할부 vs PCP(풍선할부) vs 잔가보증 비중 | 소비자 선호 ≠ 캡티브 신규계약 — 분리 |
| 4 | **주요 플레이어 (key_players)** | 캡티브(VW FS·Santander CF 등) vs 일반 은행 점유율 | 캡티브 침투율은 내부 지표(시장점유율 아님) |

### ⚠️ 1-A. 침투율 정의 함정 (가장 중요)

"침투율"은 출처마다 **분모가 다르다.** 절대 단순 비교 금지. 반드시 `aspect`로 구분해 기록한다.

| 정의(aspect) | 분모 | 예 (독일·스페인) |
|---|---|---|
| `penetration_owned_survey` | 가계 **보유** 차량 중 금융 비율(설문) | 독일 BFACH 41% |
| `penetration_lease_newreg` | **신규등록** 대비 **리스만** | 독일 BDL 48% |
| `penetration_operlease_totalreg` | **총 등록** 대비 **운용리스만** | 스페인 AER 25.74% |
| `penetration_total_financing` | **판매대수** 대비 **전체 금융**(할부+PCP+리스) | (이상적 비교 기준 — 미확보 잦음) |

> 신규 국가 조사 시: 확보한 침투율 수치가 **어느 분모인지** 먼저 확인하고 위 aspect 중 하나로 태깅한다. 다른 분모를 같은 칸에 섞지 않는다. 가능하면 `penetration_total_financing`(판매 대비 전체 금융)을 표준 비교축으로 확보 시도한다.

---

## 2. 출처 원칙 (반드시 준수 — global_constraints)

1. **공식 1차 출처만** 사용한다. 뉴스·블로그·비교사이트·시장조사 유료보고서 요약 **금지**.
   - 정부 통계청·자동차청 / 중앙은행·금융감독 / 자동차·리스·소비자금융 **협회** / 은행·캡티브 **IR(연차·반기보고서)** / Leaseurope·ECB 등 범유럽 기관.
2. **지어내기 금지** — 공식 출처로 확인 못 한 항목은 `value: null` + `status: "공식 자료에서 확인 불가"`로 명시(누락=미확보).
3. 모든 항목에 **출처(기관명·문서명·페이지/조항)·기준연도·verbatim 인용(quote)**을 명기한다.
4. **정의/분모 명시** — 침투율·채널은 분모가 다를 수 있으므로 `aspect`와 `note`에 정의를 분리 기록한다.
5. **검증 통과분만 수록** — 적대적 검증(§3)을 통과(CONFIRMED)한 claim만 본문/attributes에. 반증(REFUTED)은 `refuted_claims[]`에 사유와 함께 분리.

### 국가별 공식 출처 매핑 (시작점 — 확장 가능)

| 국가 | 정부·등록 통계 | 협회(침투율·채널·상품) | 캡티브·은행 IR |
|---|---|---|---|
| **독일** | KBA(자동차청), Destatis, Bundesbank | BFACH(Bankenfachverband), BDL(리스협회), VDA | VWFS AG, BMW Group FS, Mercedes-Benz Mobility, Santander CF |
| **스페인** | DGT, INE, Banco de España | ANFAC, AER(렌팅), ASNEF(소비자금융), AELR | Santander CF, VWFS, BBVA, CaixaBank |
| **체코** | Ministerstvo dopravy/SDA(등록), ČSÚ, ČNB(중앙은행) | ČLFA(체코 리스·금융협회), AutoSAP | VWFS(ŠkoFIN), Moneta, Santander CF |
| **폴란드** | CEPiK/PZPM(등록), GUS, NBP, KNF | ZPL(리스협회 — Leaseurope 회원), ZBP, PZWLP(렌탈) | VWFS, Santander CF Polska, mBank |
| **미국** | BEA, Federal Reserve(G.19 소비자신용), FRED | — (협회 분산: NADA 딜러) | Ally, GM Financial, Ford Credit, Toyota FS |
| **EU/유로존 공통** | Eurostat | Leaseurope(범유럽 리스 통계), ACEA(등록) | ECB(은행 통계) |

> ⚠️ 위 매핑은 **시작점**이다. 실제 조사 시 해당 기관 공식 사이트에서 최신 문서를 확인하고, 표에 없어도 공식이면 사용한다. 국가마다 협회 커버리지가 다르다(예: 스페인은 운용리스=AER가 강하지만 할부 전체는 ASNEF, 미국은 단일 협회 침투율이 약해 Fed G.19·캡티브 IR로 대체).

---

## 3. 실행 방법 (deep-research 적대적 검증 워크플로우)

독일·스페인 조사에 쓴 것과 동일한 구조. 국가만 바꿔 재실행한다.

```
[1] Scope  — 질문을 5개 탐색각도로 분해(아래 §3-1). 출처 제약(공식 기관) 명시.
[2] Search — 각도별 병렬 WebSearch. 공식 정부·협회·IR 도메인으로 한정(뉴스·블로그 제외).
[3] Fetch  — URL 중복 제거 후 상위 출처를 WebFetch. 각 claim에 verbatim 인용 + 문서·페이지·연도 첨부.
             못 찾으면 claim 미생성(지어내기 금지).
[4] Verify — claim마다 독립 검증관 3인이 "기본 refuted=true, 공식 출처로 확인될 때만 confirm".
             refute 2표 이상 → 기각. 검증관은 출처가 공식인지·인용이 실제인지·최신본인지·분모 정의가 맞는지 점검.
[5] 종합   — CONFIRMED만 수록, REFUTED는 기각 사유 기록, 미확보는 "공식 자료에서 확인 불가".
```

### 3-1. 탐색 각도 (5개 — 4축 + 범유럽/거시 보강)

| # | 탐색 각도 | 대응 축 |
|---|---|---|
| 1 | 협회·범유럽 통계 (Leaseurope/ACEA + 거시) | 전체 맥락 |
| 2 | 대상국 정부·협회 통계 — 침투율·채널 | penetration + channel_mix |
| 3 | (2국 동시 조사 시) 비교국 정부·협회 통계 | penetration + channel_mix |
| 4 | 캡티브 플레이어 점유율 — IR/연차보고서 | key_players + product_structure |
| 5 | 상품 구조 — PCP/풍선할부/잔가보증·감독기관 | product_structure |

### 3-2. 재실행 방법 (실무)

범용 `deep-research` 스킬에 아래 args 템플릿을 채워 실행한다. (1국이면 각도 3 생략 가능)

**deep-research args 템플릿** (`<국가>`·`<기관>`만 치환):

```
<국가>의 오토(자동차) 금융 시장에 대한 <연도> 기준 상세 조사. 다음 4개 지표를 다룰 것:
(1) 침투율(Penetration) — 신차/중고차 판매 중 금융(리스+할부+PCP) 이용 비율. 분모 정의를 반드시 명시.
(2) 채널 비율 — 승용차(PV) 개인 vs 플릿/법인 vs 상용차(LCV/트럭) 비중.
(3) 상품 구조 — 리스 vs 할부 vs PCP(풍선할부) vs 잔가보증 비중. 소비자 선호와 캡티브 신규계약을 분리.
(4) 주요 플레이어 — 캡티브(VW FS, Santander CF 등) vs 일반 은행 점유율.

[제약 — 매우 중요]
- 출처는 반드시 공식 자료만: 정부 통계(<자동차청/통계청/중앙은행>), 협회(<리스·소비자금융·자동차 협회>),
  은행·캡티브 IR(연차·반기보고서), Leaseurope/ECB 등. 뉴스·블로그·비교사이트 금지.
- 데이터가 없으면 지어내지 말고 "공식 자료에서 확인 불가"로 명시.
- 모든 항목에 출처(기관명·문서명·페이지·연도)·기준연도·verbatim 인용 명기.
- 침투율·채널은 분모(보유 vs 신규등록 vs 판매, 운용리스만 vs 전체금융)를 구분해 기록.

[산출물] 국가별로 위 4개 축을 표로 정리하고, 각 수치마다 공식 출처를 명시한 cited report.
```

> 실행 팁: 워크플로우가 백그라운드에서 중단되면 `Workflow({scriptPath, resumeFromRunId, args})`로 **args를 함께 넣어** 재개한다(args 누락 시 즉시 종료됨). 캐시된 검색·페치·검증은 재사용된다.

---

## 4. 산출물 (Outputs) — 2종

조사 1건당 아래 2개를 만든다.

### 4-1. 원본 보고서 (사람이 읽는 cited report) → `reports/`

- 파일명: `auto_finance_market_<국가코드들>_<연도>.md` (예: `auto_finance_market_CZ_2025.md`)
- 구조(독일·스페인 보고서와 동일):
  1. 헤더(목적·방법·출처제약·정형 산출물 링크)
  2. **⚠️ 침투율 정의 주의**(분모 표) — 가장 먼저
  3. 출처 원칙
  4. 국가별 → `시장 개요` → `4대 축`(표 + verbatim 인용 + 출처)
  5. **기각된 claim(REFUTED)** 표 — 미수록 사유
  6. **미확보 항목(Open Gaps)** 목록
  7. **출처 목록**(1차 공식 출처 URL 표)

### 4-2. 정형 산출물 (AGENT·유사도 엔진이 쓰는 JSON 초안) → `mockup/auto_finance_market/`

- 파일명: `auto_finance_market.json` (국가들을 `markets[]` 배열에 **누적**)
- 구조: `markets[] → country/country_code/region → dimensions{penetration, channel_mix, product_structure, key_players} → attributes[]`
- 각 attribute 필수 필드(유사도 비교 전제):
  ```json
  {
    "key": "국가 공통 비교키 (1:1 매칭)",
    "aspect": "유사도 비교 그룹 — 분모/정의가 같은 것끼리만 비교 (가장 중요)",
    "metric_type": "ratio_pct | eur | count (정규화 힌트)",
    "label": "사람이 읽는 이름",
    "value": { "value": ..., "year": 2024, "estimated": false,
               "source": "기관·문서·페이지", "doc_ref": "URL", "quote": "verbatim", "note": "...", "status": "..." },
    "verification": { "verified": true, "vote": "3-0" }
  }
  ```
  - `estimated`: 공식 출처 확정=`false`, 추정/미확정=`true`
  - 미확보: `"value": null, "status": "공식 자료에서 확인 불가"`, `verification.verified=false`
  - 각 dimension에 `complete`(수집 완성 여부) 플래그
  - 검증·기각·미확보 사유는 `meta.verification` / `meta.open_gaps` / `refuted_claims[]`에 기록
  - 국가별 수치가 아닌 범유럽 배경치는 `context_reference`에 분리(비교 대상 제외)

> **유사도 비교 핵심**: 두 국가를 비교할 때 **동일 `aspect`끼리만** 짝짓는다. `metric_type`에 따라 비율(소수 통일)·통화(기준통화 환산)·건수를 정규화한 뒤 근접도를 계산한다. `value:null`(미확보)은 비교에서 제외하거나 패널티 처리하고 `coverage`(확보율)를 함께 보고한다. (상세: [유사도 설계문서](../../simillarity/agent_similarity_design.md) §4~6)

---

## 5. 체크리스트 (조사 1건 완료 기준)

- [ ] 4대 축(침투율·채널·상품·플레이어)을 모두 다뤘다(없으면 "확인 불가"도 결론으로 기재).
- [ ] 침투율 수치마다 **분모(aspect)**를 명시했고, 다른 분모를 한 칸에 섞지 않았다.
- [ ] 모든 수록 항목에 **공식 출처 + 기준연도 + verbatim 인용**이 있다.
- [ ] 상품 구조에서 **소비자 선호 ≠ 캡티브 신규계약**을 분리했다.
- [ ] 캡티브 침투율을 **시장점유율과 혼동하지 않고** note에 구분했다.
- [ ] **적대적 검증(3표)** 통과분만 본문/attributes에, 기각분은 `refuted_claims[]`에 사유와 함께.
- [ ] **미확보 항목**을 "공식 자료에서 확인 불가"로 명시했다(지어내기 0건).
- [ ] 각 attribute에 **`key`·`aspect`·`metric_type`**을 부여했다(유사도 비교 전제).
- [ ] `reports/`에 원본 md, `mockup/auto_finance_market/`에 JSON 초안 — 2종을 모두 생성했다.

---

## 6. 참고 — 독일·스페인 1회차 산출물

| 산출물 | 경로 |
|---|---|
| 원본 보고서(서술형) | [`reports/auto_finance_market_DE_ES_2025.md`](../../../reports/auto_finance_market_DE_ES_2025.md) |
| 구조화 데이터(JSON 초안) | [`mockup/auto_finance_market/auto_finance_market.json`](../../../mockup/auto_finance_market/auto_finance_market.json) |

> 독일·스페인 결과 요약: 5개 탐색각도 → 24개 공식 출처 → 82개 주장 → 25개 검증 → 19개 CONFIRMED / 6개 REFUTED → 9개 핵심. 독일=법인 우위·리스 선호(캡티브), 스페인=렌탈 급성장·할부 우세(캡티브). 스페인 전체 금융 침투율은 미확보(2차 과제).
