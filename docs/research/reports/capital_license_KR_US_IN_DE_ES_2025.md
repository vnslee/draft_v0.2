# 캐피탈 진출 라이선스 조사 보고서 — 한국·미국·인도·독일·스페인 (2025)

> **조사 목적** — '글로벌 진출 전략 시뮬레이션 AGENT'용. 캐피탈사(여신전문금융회사 — **여신·대출업 + 리스·할부금융 + 팩토링·기업금융**, 예금수취 없는 비은행 여신금융)가 각국에 진출할 때 필요한 **금융 라이선스/인가**를 조사한다.
>
> - **대상 국가**: 한국(KR), 미국(US), 인도(IN), 독일(DE), 스페인(ES)
> - **대상 연도**: 2025년 기준 (항목별 기준연도 별도 표기)
> - **조사일**: 2026-06-13
> - **조사 방법**: 공식기관 도메인 한정 검색(`allowed_domains`) → 1차 출처(감독기관·중앙은행·법령 DB) fetch → 교차확인
> - **정형 산출물**: [`mockup/regulations/capital_license.json`](../mockup/regulations/capital_license.json)
> - **조사 프로세스 문서**: [`reports/process_license_research_methodology.md`](process_license_research_methodology.md)

## 출처 원칙 (사용자 지시 엄수)

- **검색·인용 모두 공식 기관 도메인만** 사용. 로펌 블로그·컨설팅 요약·위키피디아 등 2차 자료는 보조로도 배제.
  - 한국: 국가법령정보센터(law.go.kr), 금융위원회(fsc.go.kr), 금융감독원(fss.or.kr)
  - 미국: CFPB(consumerfinance.gov), 주 감독청(예: California DFPI, dfpi.ca.gov)
  - 인도: Reserve Bank of India(rbi.org.in / rbidocs.rbi.org.in)
  - 독일: BaFin(bafin.de), Deutsche Bundesbank
  - 스페인: Banco de España(bde.es), BOE(boe.es), EUR-Lex
- **지어내기 금지** — 미확보 항목은 "공식 자료에서 확인 불가"로 명시(누락 = 미확보).
- 모든 항목에 **근거 법령·발급기관·출처 URL·기준연도** 명기.

## 핵심 요약 비교

| 국가 | 라이선스 형태 | 발급/감독 기관 | 최소 자본금(여신·리스 기준) | 근거 법령 |
|---|---|---|---|---|
| 🇰🇷 한국 | 등록(리스·할부·신기술)/허가(카드) | 금융위원회·금융감독원 | 신기술금융 100억원 등 (업종별) | 여신전문금융업법 |
| 🇺🇸 미국 | 주별 lender license + 연방감독 | 주 금융감독청 + CFPB | (캘리포니아) 순자산 $25,000 + 보증보험 $25,000 | 주 Financing Law + 연방 SAFE Act |
| 🇮🇳 인도 | NBFC 등록 (Certificate of Registration) | Reserve Bank of India | NOF ₹10 crore | RBI Act 1934 §45-IA |
| 🇩🇪 독일 | BaFin 인가(Erlaubnis) | BaFin + Deutsche Bundesbank | 대출업 €5,000,000 / 리스·팩토링 면제 | KWG (독일은행법) |
| 🇪🇸 스페인 | EFC 인가 | 경제부 재무총국 + Banco de España | €5,000,000 | Ley 5/2015 + RD 309/2020 |

---

# 1. 한국 (Korea)

## 1-0. 규제 체계 개요

여신전문금융업 = **신용카드업 + 시설대여업(리스) + 할부금융업 + 신기술사업금융업**. 신용카드업만 **허가제**, 나머지 여신업(리스·할부·신기술)은 **등록제**. 모두 **예금수취 불가**.

- **발급기관**: 금융위원회(허가·등록), 금융감독원(감독·검사)
- **근거 법령**: 「여신전문금융업법」 제3조(허가 등)·제5조(자본금), 동법 시행령, 여신전문금융업감독규정

> **출처**: [여신전문금융업법 — 국가법령정보센터](https://www.law.go.kr/법령/여신전문금융업법)
> **인용(제2조 정의, 법령 원문 확인)**: *"'여신전문금융업'이란 신용카드업, 시설대여업, 할부금융업 또는 신기술사업금융업을 말한다."* / *"'신용카드업자'란 제3조제1항에 따라 신용카드업의 허가를 받거나 등록을 한 자를 말한다."*

## 1-1. 업종별 라이선스 구분 (허가 vs 등록)

| 업종 | 구분 | 비고 |
|---|---|---|
| 신용카드업 | **허가** | 제3조제1항 |
| 시설대여업(리스) | **등록** | — |
| 할부금융업 | **등록** | — |
| 신기술사업금융업 | **등록** | — |

## 1-2. 자본금 요건

| 업종 | 최소 자본금(자기자본) | 출처/비고 |
|---|---|---|
| 신기술사업금융업 | **100억원 이상** | 2024년 시행령 개정으로 200억원→100억원 완화 |
| 시설대여업·할부금융업 | 시행령에서 규정 (정확 금액 미확보) | 법제처 사이트 자동조회 차단으로 제5조 본문 캡처 미확보 |

- **출처(자본금 완화)**: [금융위 보도자료 — 여신전문금융업법 시행령 개정안 국무회의 통과](https://www.fsc.go.kr/no010101/72364)
- **인용**: *"자본금 요건 완화 : 200 → 100억원 이상"* (신기술사업금융업)
- **자기자본 정의(제2조19호, 법령 원문 확인)**: *"'자기자본'이란 납입자본금·자본잉여금 및 이익잉여금 등의 합계액으로서 대통령령으로 정하는 것을 말한다."*

> ⚠️ **미확보**: 시설대여·할부금융 업종별 자본금 정확 금액은 law.go.kr이 조문 본문을 JS 렌더링하고 자동조회를 차단해 제5조 원문 화면을 확보하지 못함. 정의·허가/등록 구분은 법령 원문에서 직접 확인, 신기술금융 100억원은 FSC 보도자료로 검증.

---

# 2. 미국 (United States)

## 2-0. 규제 체계 개요

미국은 **단일 연방 캐피탈/여신 라이선스가 없다.** 진출하는 **주(州)마다 개별 lender license**를 취득해야 하며, 연방 차원에서는 CFPB가 비은행 소비자금융을 감독한다(이중 구조).

- **발급기관**: 각 주 금융감독청 (예: California DFPI) — 신청은 NMLS(전국 멀티주 라이선싱 시스템) 경유
- **연방 감독기관**: CFPB (Consumer Financial Protection Bureau)
- **근거 법령**: 주법(예: California Financing Law) + 연방 SAFE Act([12 CFR Part 1007·1008](https://www.consumerfinance.gov/compliance/supervision-examinations/secure-and-fair-enforcement-for-mortgage-licensing-safe-act-examination-procedures/))

> **출처(연방 감독)**: [CFPB — Institutions subject to CFPB supervisory authority](https://www.consumerfinance.gov/compliance/supervision-examinations/institutions/)
> **인용**: *"Congress authorized the CFPB to supervise nonbank financial companies where it has reasonable cause to believe that the company is posing risk to consumers."*

## 2-1. 대표 사례 — California Finance Lenders License (CFLL)

| 항목 | 내용 |
|---|---|
| **라이선스** | Finance Lenders License (소비자·상업 대출 모두 커버) / Finance Broker License |
| **발급기관** | Department of Financial Protection and Innovation (DFPI) |
| **근거 법령** | California Financing Law |
| **자본금/요건** | 최소 순자산 **$25,000** + 보증보험(surety bond) **$25,000** |
| **신청** | NMLS 시스템 경유 |

- **출처**: [DFPI — About California Financing Law](https://dfpi.ca.gov/regulated-industries/california-financing-law/about-california-financing-law/)
- **인용**: *"The law requires applicants to have and maintain a minimum net worth of at least $25,000 and to obtain and maintain a $25,000 surety bond."* / *"A finance lender is ... 'any person who is engaged in the business of making consumer loans or making commercial loans.'"*

> ⚠️ **미확보**: 캘리포니아는 대표 사례일 뿐, 미국은 50개 주(+준주)마다 lender license 요건(자본·보증보험·금리상한)이 상이. 타 주는 진출 결정 시 개별 조사 필요.

---

# 3. 인도 (India)

## 3-0. 규제 체계 개요

비은행 여신금융은 **NBFC(Non-Banking Financial Company)**로 RBI에 **등록(Certificate of Registration)**해야 한다. 여신·리스·할부는 **NBFC-ICC**(Investment and Credit Company), 팩토링은 **NBFC-Factor**.

- **발급/감독기관**: Reserve Bank of India (RBI)
- **근거 법령**: Reserve Bank of India Act, 1934 **제45-IA조**, NBFC Master Directions
- **전제**: Companies Act(1956/2013)에 따라 회사로 설립 후 RBI 등록

> **출처**: [RBI — NBFC FAQs](https://www.rbi.org.in/commonman/Upload/English/FAQs/PDFs/ALLNBFC23042025.pdf), [RBI — Master Direction (PDF)](https://rbidocs.rbi.org.in/rdocs/notification/PDFs/45MD01092016B52D6E12D49F411DB63F67F2344A4E09.PDF)
> **인용**: *"A Non-Banking Financial Company (NBFC) is a company registered under the Companies Act ... engaged in the business of loans and advances, acquisition of shares/stocks/bonds/debentures/securities."*

## 3-1. 자본금 요건 (Net Owned Fund, NOF)

| 구분 | NOF 요건 | 비고 |
|---|---|---|
| **NBFC-ICC** 신규 | **₹10 crore (2억 루피)** | 신규 등록 기준 |
| NBFC-ICC 기존 (글라이드패스) | ₹2cr → **₹5cr (2025.3.31)** → **₹10cr (2027.3.31)** | 단계적 상향 |
| NBFC-Factor | ₹5cr → ₹7cr (2025.3.31) → ₹10cr (2027.3.31) | — |

- **출처**: [RBI — Minimum NOF for commencement of business of NBFC (PDF)](https://rbidocs.rbi.org.in/rdocs/Notification/PDFs/26156.PDF)
- **인용(NOF 정의)**: *"Net owned funds ... is the aggregate of paid-up capital and free reserves, netted by ... accumulated balance of loss, deferred revenue expenditure and other intangible assets ..."*
- **비고**: 기한 내 NOF 미달 시 등록(Certificate of Registration) 유지 불가.

> ⚠️ **출처 접근 한계**: RBI 사이트는 봇 차단(403/CAPTCHA)이 강해 직접 fetch 불가. NOF 글라이드패스·법조항(§45-IA)·정의는 RBI 공식 인덱싱 페이지 검색결과(rbi.org.in 도메인 한정)로 확보·교차확인.

---

# 4. 독일 (Germany)

## 4-0. 규제 체계 개요

KWG(Kreditwesengesetz, 독일은행법)에 따라 **BaFin 인가(Erlaubnis)**가 필요. 업종별로 대출업(Kreditgeschäft), 금융리스(Finanzierungsleasing), 팩토링(Factoring)으로 구분.

- **발급/감독기관**: BaFin (Bundesanstalt für Finanzdienstleistungsaufsicht) + Deutsche Bundesbank 공동
- **근거 법령**: KWG
  - 대출업: § 1 Abs. 1 Satz 2 Nr. 2, § 32
  - 금융리스: § 32 Abs. 1 Satz 1 i.V.m. § 1 Abs. 1a Satz 2 **Nr. 10** KWG
  - 팩토링: § 32 Abs. 1 Satz 1 i.V.m. § 1 Abs. 1a Satz 2 **Nr. 9** KWG

## 4-1. 자본금 요건

| 업종 | 최소 자본 | 출처/비고 |
|---|---|---|
| 대출업 (CRR-Kreditinstitut, 예금+대출) | **€5,000,000** (§ 33 KWG, Anfangskapital ≥ 5 Mio.) | EZB와 공동 심사 |
| 금융리스·팩토링 | **법정 최소자본 없음** | § 2 Abs. 7a KWG로 자기자본·유동성 요건 면제 → 회사법상 자본금만 충족 |

- **출처(리스·팩토링)**: [BaFin — Finanzierungsleasing & Factoring](https://www.bafin.de/DE/unternehmen-maerkte/erlaubnis-registrierung/leasing-factoring/leasing-factoring.html)
- **인용**: *"Gemäß § 2 Absatz 7a KWG ... verlangt das Gesetz kein Mindestkapital. ... Eigenkapital- und Liquiditätsanforderungen für Kreditgeschäfte gelten nicht."*
- **출처(대출업)**: [BaFin — Bankgeschäfte](https://www.bafin.de/DE/unternehmen-maerkte/erlaubnis-registrierung/bankgeschaefte/bankgeschaefte.html)
- **인용**: *"Nach § 31 KWG ist ein Anfangskapital von mindestens 5 Mio. Euro erforderlich."*

## 4-2. 인가 절차

| 항목 | 내용 |
|---|---|
| **신청** | AnzV 양식으로 BaFin 제출(1부) + Deutsche Bundesbank 동시 제출 + BA 14/15 전자사본 |
| **수수료(리스·팩토링)** | **€4,646** |
| **추가 요건** | BAIT/DORA 증빙, 적격 경영진(대출업은 최소 2인) |

- **인용**: *"Gebühr: 4.646 Euro"* (리스·팩토링 인가)

---

# 5. 스페인 (Spain)

## 5-0. 규제 체계 개요

비은행 전문여신기관은 **EFC(Establecimiento Financiero de Crédito)**로 인가받는다. 소비자·모기지 대출, 보증, **리스, 팩토링**, 카드를 영위하되 **예금수취 불가**(따라서 예금보험기금 가입 의무 없음).

- **발급기관**: 경제부 재무총국(Secretaría General del Tesoro y Financiación Internacional)
- **사전심사·감독**: Banco de España (+ 자금세탁방지위원회 집행국 SEPBLAC 보고)
- **근거 법령**: **Ley 5/2015**(2015.4.27, 기업금융 촉진법) Título II, **Real Decreto 309/2020**(2020.2.11)

> **출처**: [Banco de España — Other institutions supervised / Activity licence](https://www.bde.es/wbe/en/punto-informacion/contenidos/autorizaciones-acreditaciones/autorizacion-inicio-actividad/otras_entidades_88e9fa956071281.html), [BOE — Real Decreto 309/2020](https://www.boe.es/buscar/doc.php?id=BOE-A-2020-2613)
> **인용**: *"Specialised lending institutions (EFC) are non-deposit-taking credit entities that arrange loans, guarantees, leasing, and factoring."*

## 5-1. 자본금·형태 요건

| 항목 | 내용 |
|---|---|
| **최소 자본** | **€5,000,000** (전액 현금 납입, 기명주식) |
| **회사 형태** | sociedad anónima (주식회사), 존속기간 무기한 |

- **인용**: *"A minimum capital of 5 million euros is required, entirely paid in cash and represented by registered shares."* (Banco de España / BOE)

## 5-2. 인가 절차·소요기간

| 항목 | 내용 |
|---|---|
| **신청** | 재무총국에 제출, Banco de España·SEPBLAC 사전 보고서 |
| **소요기간** | 접수(또는 서류보완 완료) 후 원칙 **3개월** 내, 최대 **12개월** 내 결정 |

- **인용**: *"The authorization request must be resolved within three months ... and in any case within twelve months of reception."*

---

## 미확보·후속 조사 항목 (open_gaps)

- **한국**: 시설대여업·할부금융업 업종별 자본금 정확 금액(제5조 본문). law.go.kr 자동조회 차단 → HWP/PDF 직접 다운로드 또는 감독규정 별표 확인 필요.
- **미국**: 캘리포니아 외 49개 주(+준주)별 lender license 요건(자본·보증보험·금리상한). 진출 주 확정 후 개별 조사.
- **인도**: RBI 원문 PDF 직접 fetch 불가(봇 차단). NOF·법조항은 공식 검색결과로 확보했으나, 최종 인용 시 RBI Master Direction PDF 원문 대조 권장.
- **공통**: 외국법인의 **지점(branch) vs 현지법인(subsidiary)** 설립 시 추가 요건(상호주의·최소 출자·본국 감독당국 동의)은 본 조사 범위 외 — 진출형태 확정 후 별도 조사.
