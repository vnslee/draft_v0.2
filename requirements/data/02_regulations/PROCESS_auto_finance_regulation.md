# 프로세스: 자동차 금융 규제·세제 국가별 조사

> **목적** — 특정 국가에 대해 **자동차 금융 상품별 운영 조건 규제 + 세제 혜택**을 공식 출처로 조사·검증·산출하는 **반복 가능한 절차**를 정의한다. 어떤 국가든 이 문서를 그대로 따라 동일 품질로 조사할 수 있게 한다.
>
> - 최초 적용 사례: 미국·인도 → [`auto_finance_regulation_US_IN_2025-2026.md`](auto_finance_regulation_US_IN_2025-2026.md)
> - 정형 산출물 예: [`../mockup/regulations/auto_finance_regulation.json`](../mockup/regulations/auto_finance_regulation.json)
> - 상위 제약: [`../requirements/data/global_constraints.md`](../requirements/data/global_constraints.md)

---

## 0. 입력 (Inputs)

| 입력 | 설명 | 예시 |
|---|---|---|
| **대상 국가** | 조사할 국가 (1개 이상) | 독일, 영국, 인도네시아 … |
| **대상 연도** | 기준연도. "최신 갱신본" 원칙 | 2025/2026 중 최신 |
| **금융 상품** | 조사 대상 상품 유형 | 오토론(할부) / 리스 / 장기렌트 / EV 대출 |

> 대상 국가는 [`../requirements/data/00_basic_information/countries.md`](../requirements/data/00_basic_information/countries.md)의 진출/진출예정 국가에서 고른다.

---

## 1. 조사 항목 (4대 항목 — 고정)

국가가 바뀌어도 **항상 이 4개 항목**을 상품별로 조사한다.

| # | 항목 | 무엇을 찾는가 |
|---|---|---|
| 1 | **최소/최대 대출(약정) 기간** | 법령상 기간 상한/하한이 있는가 (없으면 "없음"도 결론) |
| 2 | **대출 금액·LTV 한도** | LTV 상한, 최소/최대 대출금액, (캡이 아닌) 공시규제 적용 한도 구분 |
| 3 | **금리·수수료 상한 등 운영 조건** | 이자율 상한(usury), 수수료 캡, **중도상환수수료** 규제, 공시 의무 |
| 4 | **상품별 세제 혜택** | 대출이자 소득공제, 차량 구매 관련 세제(GST/판매세), EV 세액공제 등 **금융상품 연계 세제** |

> **상품 유형 구분**: 오토론(closed-end credit)·리스·장기렌트는 적용 법령이 다를 수 있다(예: 미국은 대출=Reg Z / 리스=Reg M). 상품별로 나눠 기록한다.

---

## 2. 출처 원칙 (반드시 준수 — global_constraints)

1. **공식 출처만** 사용한다. 뉴스·블로그·비교사이트(예: bankbazaar, cleartax, 핀테크 마케팅 페이지) **금지**.
   - 규제 당국 / 중앙은행 / 금융감독기구 / 세무당국 / 정부 공보(법령·관보)
2. **지어내기 금지** — 공식 출처로 확인 못 한 항목은 **"공식 자료에서 확인 불가"**로 명시(누락 = 미확보). 추정·통념으로 채우지 않는다.
3. 모든 항목에 **출처(기관명·문서명·조항/번호)·기준연도**를 명기한다.
4. **연방/중앙 vs 지방/주(state) 구분** — 금리 상한 등은 주·지역별로 다를 수 있으므로 분리해 기록하고, 검증한 주/지역을 명시한다(미검증 지역은 미확보로).
5. **검증 통과분만 수록** — 적대적 검증(아래 3단계)을 통과(CONFIRMED)한 claim만 본문에. 반증(REFUTED)은 기각 사유와 함께 별도 표에.

### 국가별 공식 출처 매핑 (시작점 — 확장 가능)

| 국가 | 운영 규제(기간·금액·금리·수수료) | 세제 |
|---|---|---|
| **미국** | Federal Reserve, CFPB(Reg Z/Reg M·TILA), NCUA, 주(state) usury법 | IRS |
| **인도** | RBI(Master Directions·Notifications) | Income Tax Dept/CBDT, GST Council, PIB(재무부) |
| **EU/유로존** | ECB, EBA, 각국 중앙은행, EU Consumer Credit Directive(2023/2225) 국내법 | 각국 세무당국, EU VAT Directive |
| **영국** | FCA(CONC sourcebook), Bank of England | HMRC |
| **독일** | BaFin, Bundesbank, BGB(소비자신용 §491~) | Bundesfinanzministerium |
| **호주** | ASIC, APRA, National Consumer Credit Protection Act | ATO |
| **캐나다** | FCAC, OSFI, 주(province)별 소비자보호법 | CRA |
| **일본** | 金融庁(FSA), 割賦販売法/貸金業法 | 国税庁(NTA) |
| **인도네시아** | OJK(금융감독청), Bank Indonesia | DJP(국세청) |
| **멕시코** | CNBV, Banxico, CONDUSEF | SAT |
| **폴란드** | KNF, NBP, EU CCD 국내법 | 재무부 |
| **러시아** | Bank of Russia(ЦБ РФ) | ФНС(연방세무청) |
| **중국** | PBOC, 国家金融监督管理总局(NFRA) | 国家税务总局 |
| **한국** | 금융위원회·금융감독원, 여신전문금융업법, RBI 대응 | 국세청, 기획재정부 |

> ⚠️ 위 매핑은 **시작점**이다. 실제 조사 시 해당 기관 공식 사이트에서 최신 문서를 확인하고, 표에 없는 기관이라도 공식이면 사용한다. RBI rbidocs PDF처럼 직접 fetch가 403/CAPTCHA로 막히면 **공식 notification 페이지·관보로 교차 확인**한다.

---

## 3. 실행 방법 (deep-research 적대적 검증 워크플로우)

미국·인도 조사에 쓴 것과 동일한 구조. 국가만 바꿔 재실행한다.

```
[1] Fetch  — 4대 항목 × 상품별로, 공식 출처를 WebSearch로 찾고 실제 페이지를 WebFetch.
             각 claim에 verbatim 인용 + 문서번호/조항/연도 첨부. 못 찾으면 claim 미생성(지어내기 금지).
[2] Verify — claim마다 독립 검증관 3인이 "기본 refuted=true, 공식 출처로 확인될 때만 confirm".
             refute 2표 이상 → 기각. 검증관은 출처가 공식인지·인용이 실제인지·최신본인지 점검.
[3] 종합   — CONFIRMED만 수록, REFUTED는 기각 사유 기록, 미확보는 "공식 자료에서 확인 불가".
```

### 재실행 방법 (실무)

이 저장소에는 인도 조사용 워크플로우 스크립트가 보존되어 있다. 다른 국가에 재사용하려면:

1. 스크립트의 `ITEMS[].q`(검색 질의)와 출처 매핑을 **대상 국가 기관명**으로 바꾼다(2번 표 참조).
2. `Workflow` 도구로 실행 → 백그라운드 완료 후 결과(JSON)를 받는다.
3. 또는 범용 `deep-research` 스킬에 아래 args 템플릿을 채워 실행한다.

**deep-research args 템플릿** (`<국가>`·`<기관>`만 치환):

```
<국가>의 자동차 금융(auto finance) 상품별 정부·공식 기관 규제 및 세제 혜택을 <연도> 최신 공식 자료 기준으로 조사한다.

[조사 항목 — 금융 상품별(오토론/할부, 리스, 장기렌트, EV 대출)]
1. 최소/최대 대출(약정) 기간 규제 — 법령상 한도가 있는가
2. 대출 금액 한도 (LTV 한도, 최소/최대 대출금액) 규제
3. 수수료·금리 상한 등 운영 조건 규제 (이자율 상한, 수수료 캡, 중도상환수수료 규제)
4. 상품별 세제 혜택 여부 (이자 소득공제, 차량 구매 관련 세제, EV 세액공제 등)

[제약 — 매우 중요]
- 출처는 반드시 <국가>의 국가 기관/규제기관/공식 법령만 사용 (예: <중앙은행/금융감독기구>, <세무당국>, <관보/법령>). 뉴스·블로그·비교사이트 금지.
- 데이터가 없으면 지어내지 말고 "공식 자료에서 확인 불가"로 명시.
- 모든 항목에 출처(기관명·문서명·조항·연도)와 기준연도(최신 갱신본) 명기.
- 연방/중앙 규제와 지방/주(state)별 규제(특히 금리 상한)를 구분.

[산출물] 국가별·상품별로 위 4개 항목을 표로 정리하고, 각 항목마다 공식 출처를 명시한 cited report.
```

---

## 4. 산출물 (Outputs) — 2종

조사 1건당 아래 2개를 만든다.

### 4-1. 원본 보고서 (사람이 읽는 cited report) → `reports/`

- 파일명: `auto_finance_regulation_<국가코드들>_<연도>.md` (예: `auto_finance_regulation_DE_UK_2026.md`)
- 구조(미국·인도 보고서와 동일):
  1. 헤더(목적·대상·조사일·검증 결과·정형 산출물 링크)
  2. 출처 원칙
  3. 국가별 → `규제 체계 개요` → `1~4 항목`(표 + verbatim 인용 + 출처)
  4. **기각된 claim(REFUTED)** 표 — 미수록 사유
  5. **미확보 항목(Open Gaps)** 목록
  6. **출처 목록**(1차 공식 출처 URL 표)

### 4-2. 정형 산출물 (AGENT가 쓰는 JSON 초안) → `mockup/regulations/`

- 파일명: `auto_finance_regulation.json` (국가들을 `regulations[]` 배열에 누적)
- 신뢰성 메타 구조(프로젝트 공통):
  ```json
  { "value": ..., "year": 2026, "estimated": false,
    "source": "기관·문서·조항", "doc_ref": "URL/번호", "quote": "verbatim", "note": "..." }
  ```
  - `estimated`: 공식 출처 확정=`false`, 추정/미확정=`true`
  - 미확보: `"value": null, "status": "공식 자료에서 확인 불가"`
  - 검증·기각·미확보 사유는 `meta.verification` / `meta.open_gaps`에 기록

---

## 5. 체크리스트 (조사 1건 완료 기준)

- [ ] 4대 항목을 **상품별로** 모두 다뤘다(없으면 "없음"/"확인 불가"도 결론으로 기재).
- [ ] 모든 수록 항목에 **공식 출처 + 기준연도 + verbatim 인용**이 있다.
- [ ] 연방/중앙 vs 지방/주를 **구분**했고, 검증한 지역을 명시했다.
- [ ] **적대적 검증(3표)** 통과분만 본문에, 기각분은 사유와 함께 별도 표에 있다.
- [ ] **미확보 항목**을 "공식 자료에서 확인 불가"로 명시했다(지어내기 0건).
- [ ] `reports/`에 원본 md, `mockup/regulations/`에 JSON 초안 — 2종을 모두 생성했다.
```
