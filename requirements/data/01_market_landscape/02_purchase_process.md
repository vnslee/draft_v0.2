# 자동차 구매 프로세스 (Purchase Process)

> **목적** — '글로벌 진출 전략 시뮬레이션 AGENT'에서 **특정 국가가 입력되면 해당 국가의 자동차 구매 프로세스**를 제시하고, **타 국가와 프로세스 유사도를 비교·스코어링**할 수 있도록, 구매 프로세스의 **분류 체계(Taxonomy)**와 **국가별 수집 정의**, 그리고 **재사용 가능한 조사 프로세스**를 정의한다.

이 문서는 세 가지를 함께 정의한다.
1. **분류 체계** — 구매 프로세스를 어떤 축(Dimension)으로 나눌지에 대한 **표준 구분**
2. **수집 정의** — 위 분류 체계를 기준으로 **국가별로 어떤 데이터를 수집**할지
3. **조사 프로세스** — 미국 대상으로 수행한 절차를 **다른 국가에도 그대로 적용**하기 위한 재사용 가이드

> 분류 체계와 조사 프로세스는 **모든 국가에 공통 적용되는 틀**이고, 수집 데이터는 **국가별로 채워지는 값**이다. 동일 축 체계여야 국가 간 유사도 비교가 성립한다.

---

## 1. 대상

**대상 국가**별로, 그 나라 **판매량 상위 3개 제조사 그룹(OEM)**을 중심으로 자동차 구매 프로세스를 수집한다.

> 상위 3개 그룹 선정 기준은 `00_basic_information/countries.md`의 bestseller(그룹 기준)와 일치시킨다. (예: 미국 = GM / Toyota / Ford)

---

## 2. 분류 체계 (Taxonomy)

구매 프로세스는 **4개 축(Dimension)의 조합**으로 정의한다. 국가별 데이터가 확보되는 축만 채우고, **미확보 축은 비워 둔다.**

> ⚠️ **세부 속성·구분값은 국가별로 다를 수 있다.** 채널·세액공제·금융 상품 등은 국가마다 통용 제도 자체가 다르므로, 속성 예시는 **참고용**이며 실제 수집 시에는 **현지 기준**을 쓰고 `note`에 차이를 기록한다. **단, `key`(국가 공통 비교키)는 국가 간 동일하게 유지**해야 유사도 비교가 성립한다.

| 축 (Dimension) | 설명 | 속성(attribute) 예시 (key) |
|----------------|------|----------------------------|
| 온라인/디지털 구매 (online_digital) | 제조사 공식 온라인 구매 플랫폼, 디지털 리테일, 예약/주문 시스템 | `oem_digital_retail_platform`, `digital_retail_omnichannel`, `oem_online_purchase_checkout` |
| 딜러십 판매 모델 (dealership_model) | 딜러 네트워크, 직판(DTC) 여부, 협상, 재고, 판매 만족도, 시장 리더십 | `primary_sales_channel`, `market_sales_leader_oem`, `sales_satisfaction_leader_mass_market`, `incentive_level_vs_industry` |
| 금융/리스/인센티브 (financing_incentives) | 파이낸싱, 리스, 할부, 로열티·카드 프로그램, 프로모션 | `oem_loyalty_program`, `oem_cobrand_credit_card`, `ev_incentive_finder_tool` |
| EV 구매 특화 (ev_process) | EV 세액공제, 충전 인프라, EV 전용 구매 경로 | `federal_new_ev_credit_max`, `federal_ev_credit_income_cap_*`, `federal_*_sunset_date`, `oem_ev_trim_expansion`, `oem_charging_network_expansion` |

> 각 속성은 **정성(존재여부/라벨)** 또는 **정량(금액·비율·건수)** 일 수 있다. 정량 값에는 가급적 단위·기준을 `note`에 적는다.

---

## 3. 수집 정보

각 국가별로, **위 분류 체계의 각 축·속성에 대해** 아래 정보를 수집한다.

| 구분 | 항목 | 설명 |
|------|------|------|
| 식별 | 국가명 / 권역 / 상위 3개 OEM 그룹 | 국가 식별 및 대상 OEM |
| 식별 | 축 (Dimension) | 2장에서 정의한 4개 축 |
| 속성 | 비교키 (key) | **국가 공통**. 동일 key 끼리 국가 간 비교/스코어링 |
| 속성 | 라벨 (label) | 사람이 읽는 속성 이름 |
| 값 | value | 정성(존재여부/문자열) 또는 정량(숫자) |
| 신뢰성 | year / estimated / source / note | 출처·기준연도·추정여부 |
| 검증 | verification.verified / vote | 적대적 검증 통과 여부 및 표(예: '3-0', '2-1') |

> **정량 수치는 추정 금지.** 출처가 있는 값만 기재하고, 없으면 `value: null`로 비워 둔다. (누락 = 미확보)
> **반증(REFUTED) 항목은 attributes에 넣지 않고** `refuted_claims[]`에 별도 보관한다(투명성).

---

## 4. 제약 사항

1. **출처 제약(중요)**: **일반 뉴스 기사 사용 금지.** **제조사 공식 뉴스룸(예: news.gm.com / pressroom.toyota.com / media.ford.com 및 산하 브랜드)**과, **EV 세액공제 등 제도 정보는 정부 공식 자료(예: 미국 IRS)**만 사용한다. 국가별로 대응되는 공식 출처를 사전에 정의한다(아래 6-1).
2. **분류 체계(2장)는 공통 축**이며, 국가별로 통용되는 제도·채널·상품 구분값이 다를 경우 **현지 기준을 우선**하고 `note`에 차이를 기록한다. **`key`는 국가 간 동일하게 유지**한다(유사도 비교 전제).
3. **정량 데이터는 출처 명시된 경우만** 기재한다. 추정·통념으로 채우지 않는다. (누락 = 미확보)
4. 모든 속성에는 **출처·기준연도·검증 결과(vote)**를 명기한다. (기본 기준연도: 2025년)
5. **검증 통과(verified=true) 항목만 정식 수록**하고, 반증 항목은 `refuted_claims[]`로 분리한다.

---

## 5. 산출물 생성 프로세스

- 조사한 구매 프로세스 정보를 **JSON 초안**으로 생성한다.
- **산출물 경로**: `mockup/purchase_process/` 폴더에 생성한다. (폴더가 없으면 생성)
- **원본 보고서(서술형)**는 `reports/` 폴더에 마크다운으로 보관한다.
- JSON 구조는 **초안 수준**으로 둔다 (DB 스키마/저장 유형 확정 전).
- **미확보 데이터는 채워넣지 않는다** (누락 = 미확보).
- 신뢰성 정보가 필요한 데이터 필드는 **`{ value, year, estimated, source, note? }`** 메타 구조로 저장한다.
    - `estimated`: 추정치/미확정이면 `true`, 확정 실측치(검증 통과)면 `false`
    - 각 속성에 **`verification: { verified, vote }`**를 함께 둔다.
- 각 **축(dimension) 단위로 `complete`** 플래그로 수집 완성 여부를 표기한다.
- 각 속성에 **국가 공통 `key`**를 부여한다(유사도 비교 단위).

---

## 6. 조사 프로세스 (재사용 가이드 — 타 국가 적용)

미국을 대상으로 수행한 절차를, **다른 국가에도 그대로 적용**할 수 있도록 일반화한다. (실제 미국 1회차는 deep-research 워크플로우로 수행: 5개 탐색각도 → 23개 출처 → 67개 주장 추출 → 25개 검증 → 23개 확인/2개 폐기)

### 6-1. 사전 정의 (국가 진입 시 1회)

1. **상위 3개 OEM 그룹 확정** — `countries.md` bestseller(그룹 기준)에서 가져온다.
2. **공식 출처 화이트리스트 작성** — 해당 국가/OEM의 **공식 뉴스룸 도메인**과 **정부 공식 제도 출처**를 미리 정의한다.
   - 제조사 예: GM `news.gm.com`, Chevrolet `media.chevrolet.com`, Cadillac `media.cadillac.com`, Toyota `pressroom.toyota.com`, Ford `media.ford.com`.
   - 정부/제도 예(미국 EV): IRS `irs.gov`. → **다른 국가는 그 나라의 EV 보조금·세제 담당 정부기관 공식 사이트로 대체**한다.

### 6-2. 탐색 각도 (5개 — 4개 축 + EV 보강)

| # | 탐색 각도 | 대응 축 |
|---|-----------|---------|
| 1 | online/digital retail | online_digital |
| 2 | dealership sales model | dealership_model |
| 3 | financing / lease / incentives | financing_incentives |
| 4 | EV purchase tax credit & charging | ev_process |
| 5 | EV-specific buying path & cross-brand digital (보강) | ev_process + online_digital |

### 6-3. 실행 단계

1. **Scope** — 위 5개 탐색 각도로 질문을 분해한다(상위 3개 OEM 그룹 명시, 출처 제약 명시).
2. **Search** — 각도별 병렬 검색. **공식 뉴스룸/정부 도메인으로 한정**(일반 뉴스 제외).
3. **Fetch** — URL 중복 제거 후 상위 출처를 가져와 **검증 가능한(falsifiable) 주장**을 추출한다.
4. **Verify** — 주장별 **3표 적대적 검증**(2/3 이상 반박 시 폐기). `vote`(예: '3-0', '2-1') 기록.
5. **Synthesize** — 의미 중복 병합, 신뢰도순 정렬, **출처 URL과 함께** 종합. 검증 통과 항목만 수록.

### 6-4. 출력 규칙

- 모든 주장은 **공식 출처 URL**로 인용한다. URL 없는 주장은 수록하지 않는다.
- 검증 통과 항목 → `dimensions.*.attributes[]` (verified=true).
- 반증 항목 → `refuted_claims[]` (투명성, 본문 미반영).
- 출처 화이트리스트 밖(일반 뉴스 등)에서 나온 주장 → **폐기**.
- 특정 OEM에서 검증 통과 주장이 하나도 없으면 → **`open_gaps`에 공백 명시**(미국 Ford 사례 참조).

### 6-5. 유사도 비교/스코어링 (DB 적재 후)

- 비교 단위: **동일 dimension · 동일 attribute.key**.
- 점수 = (속성 존재여부 일치) + (정량 value 근접도) + (정성 라벨/제도 유형 일치)의 조합으로 산출 권장.
- **`value: null`(미확보)는 비교에서 제외하거나 별도 패널티**로 처리(국가별 데이터 완성도 차이 보정).
- **`basis`/출처/시점이 다른 정량값은 직접 비교하지 않는다**(분모 상이). 같은 `key`라도 `note`의 기준 차이를 확인한다.

---

## 7. 참고 — 미국 1회차 산출물

| 산출물 | 경로 |
|--------|------|
| 원본 보고서(서술형) | `reports/2025_us_car_buying_process.md` |
| 구조화 데이터(JSON 초안) | `mockup/purchase_process/purchase_process.json` |

> 미국 결과 요약: GM 2025 판매 1위(+6%), Toyota SmartPath 누적 100만 고객, GM Rewards Mastercard(2025.5), 연방 EV 세액공제 2025.9.30 종료. **Ford는 검증 통과 1차 출처를 확보하지 못해 공백**으로 남김.
