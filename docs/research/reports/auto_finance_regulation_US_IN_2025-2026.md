# 자동차 금융 규제·세제 조사 보고서 — 미국·인도 (2025~2026)

> **조사 목적** — '글로벌 진출 전략 시뮬레이션 AGENT'용. 자동차 금융 상품별 **운영 조건 규제**(최소/최대 대출 기간, 대출 금액·LTV, 수수료·금리 상한 등)와 **상품별 세제 혜택**을 국가·공식 출처 기준으로 조사한다.
>
> - **대상 국가**: 미국(US), 인도(IN)
> - **대상 연도**: 2025/2026 중 최신 갱신본 (항목별 기준연도 별도 표기)
> - **조사일**: 2026-06-13
> - **조사 방법**: deep-research workflow (fan-out 검색 → 공식 1차 출처 fetch → claim별 3표 적대적 검증 → 종합)
> - **검증 결과**: 미국 25개 claim 통과 / 0 기각, 인도 13개 통과 / 2 기각
> - **정형 산출물**: [`mockup/regulations/auto_finance_regulation.json`](../mockup/regulations/auto_finance_regulation.json)

## 출처 원칙 (global_constraints 준수)

- 출처는 **국가 기관·규제기관·공식 법령만** 사용한다. 뉴스·블로그·비교사이트(bankbazaar, cleartax 등) 배제.
  - 미국: Federal Reserve, CFPB, NCUA, IRS, 주(state) 법령(NY·CA)
  - 인도: RBI, Income Tax Department, GST Council, PIB(재무부·중공업부·도로교통부)
- **지어내기 금지** — 미확보 항목은 "공식 자료에서 확인 불가"로 명시(누락 = 미확보).
- 모든 항목에 **출처·기준연도** 명기. 적대적 검증(CONFIRMED) 통과 항목만 수록, 반증(REFUTED)은 기각 사유와 함께 별도 기록.

---

# 1. 미국 (United States)

## 1-0. 규제 체계 개요

미국 연방 자동차 금융 규제는 **금리·기간·수수료 '캡'이 아니라 '정보공시(disclosure)' 중심**이다.

- **오토론(closed-end credit)**: Truth in Lending Act(TILA, 15 U.S.C. 1601 et seq.) → **Regulation Z**(12 CFR Part 1026)
- **소비자 리스**: Consumer Leasing Act → **Regulation M**(12 CFR 1013)
- **감독기관**: CFPB (단, Dodd-Frank §1029로 대부분의 **독립 딜러**는 권한 제외 → FTC 분담)
- **금리/수수료 상한**: 연방이 아닌 **주(state) usury법** 및 **NCUA**(연방신용조합)에서 규율
- **특례**: 현역 군인은 Military Lending Act §987로 별도 **36% MAPR 상한**

> **출처**: CFPB Supervisory Highlights — Auto Finance (Special Edition), Federal Register 2024-24093 (2024.10.18); Reg Z 12 CFR 1026.1(b)
> **인용**: *"The origination of automobile loans is governed by the Truth in Lending Act (TILA) as implemented by Regulation Z ... 12 C.F.R. Part 1026."* / Reg Z 목적: *"to promote the informed use of consumer credit by requiring disclosures ... does not generally govern charges for consumer credit."*

## 1-1. 최소/최대 대출 기간 규제

| 결과 | 내용 |
|---|---|
| **연방** | 법령상 최소/최대 대출 기간 한도 **없음**. 기간은 대주(lender)·주법 영역. |

- **출처**: TILA / Regulation Z (12 CFR Part 1026), 2025

## 1-2. 대출 금액·LTV 한도 규제

| 결과 | 내용 |
|---|---|
| **연방 LTV·금액 캡** | **없음** |
| **Reg Z / Reg M 적용 한도** | 2026년 **$73,400 이하** 소비자 신용·리스 거래에 공시규제 적용 (2025년 $71,900 → CPI-W 2.1% 인상). **대출금액 캡이 아니라 공시규제 적용선**. |

- **출처**: Fed/CFPB joint final rules, CFPB newsroom(2025.12.15); Federal Register 2025-22814(Reg Z)·2025-22813(Reg M)
- **인용**: *"Regulation Z and Regulation M generally will apply to consumer credit transactions and consumer leases of $73,400 or less in 2026."*
- **비고**: 한도 초과 거래는 일반적으로 공시규제 면제(모기지·사학자금은 금액 무관 적용). 자동차 대출 전용 LTV·min/max 금액 연방 상한 없음.

## 1-3. 금리·수수료 상한·중도상환 등 운영 조건 규제

| 구분 | 결과 | 출처 |
|---|---|---|
| **연방 금리·수수료 상한** | 없음 (TILA/Reg Z는 정확한 **공시만** 의무화) | Reg Z 12 CFR 1026.18, 1026.17 |
| **연방 중도상환수수료** | 금지·상한 없음. Reg Z 1026.18은 "중도상환수수료/환급 **적용 여부 공시**"만 의무화 | Reg Z 12 CFR 1026.18; 1026.17(c)(1) |
| **NCUA(연방신용조합)** | 법정 상한 **15%**, NCUA가 한시 **18%**로 상향(**2027.9.10까지**, 이후 15% 복귀). Payday alternative loan은 28%까지 | NCUA(2026); Federal Credit Union Act 12 U.S.C. 1757(5)(A)(vi)(I) |
| **뉴욕(NY)** | 기본 법정이율 6%, 민사 usury 상한 **16%** | NY GOL §5-501; Banking Law §14-a |
| **캘리포니아(CA)** | Rees-Levering 자동차판매금융법: 선이자 구간별 상한(잔액 $225까지 월 1.5%, $900까지 월 1⅙%≈1.167%, $2,500까지 월 5/6%≈0.833%, 또는 전체 잔액 월 1% 중 큰 값, 최소 $25) + **중도상환수수료 금지** | CA Civil Code §2982 §2982(j)(1)·(l)(1) |

- **인용(연방)**: *"Reg Z does not generally govern (cap) the charges for consumer credit; it requires disclosure of APR, finance charge, amount financed, total of payments."*
- **인용(중도상환)**: *"Reg Z 1026.18 requires a definitive statement of whether a prepayment penalty applies — but does NOT prohibit or cap it."* (CFPB 검사에서 중도상환수수료 부정확 공시로 오토론 originator 적발 사례 — 공시 위반 차원)
- **인용(NCUA)**: *"The Federal Credit Union Act generally limits federal credit unions to a 15-percent interest rate ceiling on loans; the current 18% ceiling is extended to September 10, 2027."*
- **인용(NY)**: GOL §5-501(1) *"shall be six per centum per annum unless a different rate is prescribed in ... section fourteen-a of the banking law"* (민사 상한 16%)
- **인용(CA)**: §2982(l)(1) *"the buyer may pay at any time before maturity the entire indebtedness ... without penalty."*
- **⚠️ 주별 상이**: usury/금융수수료 상한은 주마다 다름. **NY·CA 2개 주만 검증**, 나머지 48개 주 미확보.

## 1-4. 상품별 세제 혜택

| 혜택 | 내용 | 출처 |
|---|---|---|
| **신규 자동차 대출이자 소득공제 (신설)** | 연 최대 **$10,000**, 과세연도 **2025~2028 한시**. 요건: 2024.12.31 이후 발생 대출, **신차·개인용도**, **미국 내 최종조립**(VIN/라벨 확인). 표준공제자도 가능. MAGI $100,000(부부합산 $200,000) 초과 시 단계적 축소. Schedule 1-A 신청. | IRS/Treasury guidance; OBBB Public Law 119-21(2025.7.4); Federal Register 2025-24154(2026.1.2 게재, 의견수렴 2026.2.2까지) |
| **EV/클린차량 세액공제 (종료)** | **§30D(신차)·§25E(중고)·§45W(상용)** 모두 **2025.9.30 이후 취득분부터 폐지**. (종료 전 §45W 상한: GVWR 14,000lbs 미만 $7,500 / 이상 $40,000) | IRS FAQ for Public Law 119-21(OBBB); IRS Commercial Clean Vehicle Credit; OBBB §70503 |

- **인용(공제 신설)**: *"$10,000 annual deduction limit on interest paid on vehicle loans incurred after Dec. 31, 2024, to purchase new made-in-America vehicles for personal use."*
- **인용(EV 종료)**: §30D *"The credit will not be allowed for any vehicle acquired after September 30, 2025"* (동일하게 §25E·§45W). 'Acquired' = 서면 구속계약 + 지급일.
- **비고**: 최종규칙(2025-24154)은 의견수렴(2026.2.2 마감) 후 요건 변경 가능.

---

# 2. 인도 (India)

## 2-0. 규제 체계 개요

RBI는 자동차 대출의 기간·LTV·금리를 **'캡'으로 직접 규제하기보다 건전성(risk weight)·공정관행(중도상환·공시) 틀**로 규율한다. 자동차 대출 전용 기간/LTV 상한은 RBI가 별도로 정하지 않고 **은행·NBFC의 board-approved 신용정책에 위임**. 세제는 소득세법(§80EEB)·GST Council 소관.

> 적대적 검증관 3인 모두 "RBI는 자동차 대출 전용 LTV 상한을 두지 않으며 대주 자체 신용정책에 위임"이 정확하다고 확인.

## 2-1. 최소/최대 대출 기간 규제

| 결과 | 내용 |
|---|---|
| **확인 불가** | RBI가 자동차 대출 전용 최소/최대 기간 상한을 규정한 공식 자료를 **확인하지 못함(미확보)**. 기간은 대주 자체 정책. |

## 2-2. 대출 금액·LTV 한도 규제

| 결과 | 내용 | 출처 |
|---|---|---|
| **자동차 대출 LTV 상한 부재** | RBI는 자동차/차량 대출 전용 LTV·대출금액 상한을 별도로 정하지 않음 — 대주(은행·NBFC)의 board-approved 신용정책에 위임 | 적대적 검증(3인) 합의 (RBI Master Circular on Housing Finance 대비 확인) |

- **비고**: 후보 자료의 '주택대출 LTV 표(20락=90%)'는 RBI가 **30락 기준**으로 갱신해 수치 오류로 **기각** → 자동차 대출과 무관해 미수록. '자동차 대출 LTV 상한 부재'만 확정.

## 2-3. 금리·수수료 상한·중도상환 등 운영 조건 규제

| 구분 | 결과 | 출처 |
|---|---|---|
| **금리 상한** | **확인 불가**(RBI는 캡 대신 EBLR 연동·공정관행 틀). 미확보 | — |
| **중도상환(foreclosure)수수료 금지** | **변동금리 대출**의 중도상환수수료 금지 — **개인(비사업목적)·MSE(사업목적)** 대상. 부분/전액·상환재원 불문, **최소 lock-in 없음**. 2026.1.1 이후 sanction/renew된 모든 대출 적용 | RBI(Pre-payment Charges on Loans) Directions, 2025; RBI/2025-26/64; DoR.MCS.REC.38/01.01.001/2025-26(2025.7.2) |
| **중도상환 부가 보호** | 소급부과 금지, 기존 면제분 부과 금지, 대주측 요구 중도상환 시 부과 금지. 적용/면제 여부는 sanction letter·loan agreement·**Key Facts Statement(KFS)**에 사전 공시, 미공시분 회수 불가 | 동상 |
| **건전성 우대** | 소비자신용 risk weight 125% 상향(2023) 시 **차량대출 명시 제외**(은행·NBFC 공통) → 통상(낮은) risk weight 유지 | RBI/2023-24/85, DOR.STR.REC.57/21.06.001/2023-24(2023.11.16) |
| **top-up 취급** | 차량 등 가치하락 동산 담보 top-up 대출은 신용평가·건전성한도·익스포저상 **무담보** 취급 | 동상 |

- **인용(중도상환 금지)**: *"No pre-payment charges shall be levied on floating-rate loans to: Individuals (for purposes other than business), and MSEs (for business purposes) ... regardless of the source of repayment, whether partial or full, and with no minimum lock-in period."*
- **인용(부가 보호)**: *"Pre-payment charges cannot be levied retrospectively or where the charges were previously waived. No charges shall be imposed if the pre-payment is initiated at the instance of the lending institution. ... must disclose ... in: Sanction letters, Loan agreements, and Key Facts Statements (KFS)."*
- **인용(건전성)**: *"...consumer credit exposure ... including personal loans, but excluding housing loans, education loans, vehicle loans and loans secured by gold ... increased by 25 percentage points to 125%."*
- **적용기관**: 상업은행(Payments Bank 제외)·협동조합은행·NBFC·AIFI. 이중/특수금리(고정+변동) 대출은 중도상환 시점에 변동금리면 면제 적용.

## 2-4. 상품별 세제 혜택

| 혜택 | 내용 | 출처 |
|---|---|---|
| **EV 대출이자 소득공제 (§80EEB)** | EV 구매 대출이자 추가공제 **최대 Rs 1.5 lakh** (Finance Act 2019 도입, AY 2020-21~ 적용) | PIB/중공업부 Year Ender 2019, Release ID 1597099; Income Tax Act §80EEB |
| **EV GST** | 전기차 GST **5%**(종전 12%→5%, 2019.8.1~ 현행 유지). 충전기/충전소 18%→5% | PIB/재무부(36th GST Council), Release ID 1580536(2019.7.27) |
| **차량 구매 GST (56th GST Council)** | 소형차 28%→**18%**, 중·대형차(>1500cc 또는 >4000mm) **40%**(cess 폐지, full ITC). **2025.9.22 시행** | PIB/재무부 Release ID 2163560(2025.9.3); PIB/도로교통부 Release ID 2165916(2025.9.12) |
| **리스 GST (legacy, 참고)** | 2017.7.1 이전 구매·리스 차량 리스에 적용 GST율의 **65%**(cess 포함) — 22nd GST Council, 2017.7.1부터 **3년 한시** | PIB/재무부(22nd GST Council), Release ID 1505912(2017.10.12) |

- **인용(§80EEB)**: *"Government has extended an additional income tax deduction of Rs 1.5 Lakh on interest paid on loans to the buyers of Electric Vehicle to buy EVs is provided."*
- **인용(EV GST)**: *"The GST rate on all electric vehicles be reduced from 12% to 5%. ... effective from 1st August, 2019."*
- **인용(소형/대형차)**: *"The GST rate on all small cars has been reduced from 28% to 18% (Petrol/LPG/CNG ≤1200cc & ≤4000mm; Diesel ≤1500cc & ≤4000mm). Mid-size and large cars (>1500cc or >4000mm) = 40%. Effective 22nd September 2025."*
- **인용(리스 legacy)**: *"Leasing of vehicles purchased and leased prior to 1st July, 2017 would attract GST at a rate equal to 65% of the applicable GST rate (including Compensation Cess). ... for a period of three years with effect from 1st July, 2017."*
- **비고**: 리스 legacy 규정은 한시(3년) 경과분 — 현행 리스 GST율 자체는 별도 미검증(미확보).

## 2-5. 장기렌트 (long-term rental)

- **확인 불가**: 인도 장기렌트 전용 금융·세제 규제를 공식 자료에서 확인하지 못함(미확보).

---

# 3. 기각된 claim (REFUTED) — 미수록 사유 기록

| 국가 | 기각된 claim | 기각 사유 |
|---|---|---|
| 인도 | 주택대출 LTV 표(상한 Rs 20 lakh=90%, 20~75 lakh=80%, 75 lakh 초과=75%) | RBI가 90% 구간 기준을 **Rs 20 lakh → 30 lakh로 갱신**(DBR.BP.BC.44/08.12.015/2015-16, 2024.4 Master Circular). 인용한 2014-15 회람의 수치가 현행과 불일치(수치 오류). + 자동차 대출과 무관. |
| 인도 | SFB·RRB·협동조합은행·NBFC-ML의 중도상환수수료 면제 "MSE 한정, 차주당 총 Rs 50 lakh" | 실제 규정(Pre-payment Directions §5)은 **'대출 sanctioned amount/limit Rs 50 lakh 이하'**(개별 facility 기준)이고 **개인(사업목적)도 포함**. "aggregate per borrower"·"MSE only"는 공식문 미포함(왜곡). |

> ⚠️ 단, 인도 LTV 기각 claim의 **"RBI는 자동차 대출 전용 LTV 상한을 두지 않는다"는 일반 명제는 검증관 3인이 정확하다고 확인** → 본문 2-2에 반영.

---

# 4. 미확보 항목 (Open Gaps)

- **미국 주별**: NY·CA 외 48개 주의 usury/금리 상한·중도상환 규제 미확보.
- **미국 리스/렌트**: Reg M(12 CFR 1013) 리스 전용 운영규정(잔가·주행거리·조기종료), 장기렌트 전용 규제 미검증.
- **인도 기간**: 자동차 대출 전용 최소/최대 기간 상한 — 공식 자료에서 확인 불가.
- **인도 금리**: 자동차 대출 금리 상한 — 공식 자료에서 확인 불가(RBI는 캡 미운영).
- **인도 침투율/평균금리**: 신차/중고차 금융 침투율·평균 금리 미확보.
- **양국 장기렌트**: 장기렌트 전용 금융·세제 규제 미확보.

---

# 5. 출처 목록 (1차 공식 출처)

### 미국
| 기관 | 문서 | URL |
|---|---|---|
| CFPB | Truth in Lending Act 개요 | https://files.consumerfinance.gov/f/201503_cfpb_truth-in-lending-act.pdf |
| CFPB | Reg Z §1026.18 (closed-end disclosure) | https://www.consumerfinance.gov/rules-policy/regulations/1026/18/ |
| CFPB | Reg Z §1026.17 (general disclosure) | https://www.consumerfinance.gov/rules-policy/regulations/1026/17/ |
| CFPB | Auto loan TILA disclosure 안내 | https://www.consumerfinance.gov/ask-cfpb/what-is-a-truth-in-lending-disclosure-for-an-auto-loan-en-787/ |
| CFPB/Fed | 2026 달러 한도($73,400) 발표 | https://www.consumerfinance.gov/about-us/newsroom/agencies-announce-dollar-thresholds-for-applicability-of-truth-in-lending-and-consumer-leasing-rules-for-consumer-credit-and-lease-transactions-2025/ |
| Federal Register | CFPB Supervisory Highlights — Auto Finance | https://www.federalregister.gov/documents/2024/10/18/2024-24093/supervisory-highlights-special-edition-auto-finance |
| eCFR | Reg Z 12 CFR Part 226/1026 | https://www.ecfr.gov/current/title-12/chapter-II/subchapter-A/part-226 |
| NCUA | Loan Interest Rate Ceiling 연장(18%) | https://ncua.gov/newsroom/press-release/2026/ncua-board-extends-loan-interest-rate-ceiling |
| NY 법령 | GOL §5-501 | https://law.justia.com/codes/new-york/gob/article-5/title-5/5-501/ |
| CA 법령 | Civil Code §2982 (Rees-Levering) | https://leginfo.legislature.ca.gov/faces/codes_displayText.xhtml?division=3.&chapter=2b.&part=4.&lawCode=CIV&title=14. |
| IRS | OBBB(P.L.119-21) §25C/25D/25E/30D/45W FAQ | https://www.irs.gov/newsroom/faqs-for-modification-of-sections-25c-25d-25e-30c-30d-45l-45w-and-179d-under-public-law-119-21-139-stat-72-july-4-2025-commonly-known-as-the-one-big-beautiful-bill-obbb |
| IRS | 자동차 대출이자 공제 신설 안내 | https://www.irs.gov/newsroom/treasury-irs-provide-guidance-on-the-new-deduction-for-car-loan-interest-under-the-one-big-beautiful-bill |
| IRS | Commercial Clean Vehicle Credit(§45W) | https://www.irs.gov/credits-deductions/commercial-clean-vehicle-credit |

### 인도
| 기관 | 문서 | URL |
|---|---|---|
| RBI | Pre-payment Charges on Loans Directions, 2025 (RBI/2025-26/64) | https://www.rbi.org.in/scripts/NotificationUser.aspx?Id=12878&Mode=0 |
| RBI | 소비자신용 risk weight 규제(RBI/2023-24/85, 2023.11.16) | https://rbidocs.rbi.org.in/rdocs/notification/PDFs/REGULATORYMEASURES8785E7886A044B678FB8AF2C6C051807.PDF |
| PIB/중공업부 | Year Ender 2019 (§80EEB EV 대출이자 공제) | https://www.pib.gov.in/PressReleseDetailm.aspx?PRID=1597099 |
| PIB/재무부 | 36th GST Council — EV GST 5% | https://pib.gov.in/PressReleasePage.aspx?PRID=1580536 |
| PIB/재무부 | 56th GST Council FAQ — 소형/대형차 GST | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2163560 |
| PIB/도로교통부 | GST Rationalisation — 대형차 40% flat | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2165916 |
| PIB/재무부 | 22nd GST Council — 리스 GST 65%(legacy) | https://www.pib.gov.in/PressReleasePage.aspx?PRID=1505912 |
| Income Tax Dept | Finance Act 2019 (§80EEB 신설) | https://incometaxindia.gov.in/Acts/Finance%20Acts/2019_2/102120000000074073.htm |

> ⚠️ 일부 RBI rbidocs PDF는 직접 fetch 시 HTTP 403/CAPTCHA로 차단되어 공식 notification 페이지·미러로 교차 확인했다.
