# 오토파이낸스 신규 국가 진출: 13개국 공식 출처 매핑 감사 (2025 기준)

## TL;DR

- **항목 A(침투율)는 8개국에서 준공식 1차 출처(산업협회·중앙은행·거래소)가 실재하나, 정의가 4가지로 갈려 13개국을 그대로 비교하는 것은 불가능하다.** 미국(Experian/Fed G.19), 영국(FLA), 독일(Bankenfachverband), 스페인(ASNEF), 폴란드(ZPL), 호주(AFIA), 브라질(B3 SNG/Fenabrave), 한국(여신금융협회)은 출처가 풍부한 반면, 사우디·이집트는 중앙은행 ‘여신잔액·품목비중’만 있고 침투율은 없으며, 푸에르토리코는 별도 침투율 출처가 사실상 없다.
- **항목 B(경쟁사 코어 IT)는 13개국 모두 진정한 공식 1차 출처가 없다.** 최선은 벤더 공식 case study/보도자료(준공식)와 금융사 연차보고서·채용공고(간접)뿐이며, 미국·영국·인도에서만 벤더 case study가 비교적 풍부하다.
- **규제 6개 항목은 13개국 모두 1차 공식 출처(법령·규제당국)가 확정 가능하다.** 라이선스·개인정보·EV는 규제당국 웹사이트와 DLA Piper(2025)·IEA Global EV Outlook 2025로 전 국가 매핑되며, 권역 패턴은 ‘유럽·북미·APAC 선진국 풍부 / 중동·남미·푸에르토리코 빈약’으로 명확하다.

## Key Findings

### 권역별 출처 풍부도 패턴

- **풍부(Tier 1):** 미국, 영국, 독일, 호주, 한국, 폴란드 — 침투율·규제 모두 준공식 이상 출처가 존재.
- **중간(Tier 2):** 스페인, 캐나다, 브라질, 인도 — 침투율 출처는 있으나 정의·접근성에 제약(유료·회원전용·정의 상이, 또는 분모/분자가 별도 기관).
- **빈약(Tier 3):** 사우디, 이집트, 푸에르토리코 — 침투율 직접 출처 부재(여신잔액·품목비중으로 대체) 또는 별도 국가 데이터 없음(푸에르토리코는 미국 연방 데이터에 흡수).

### 항목 A: 침투율 출처와 정의 정형화

침투율의 ‘정의’가 국가별로 다음 4가지로 갈린다:

1. **금융+리스 인도대수 ÷ 총 인도대수**(브라질 B3 SNG, 영국 FLA의 신차 등록 대비 비율)
1. **금융 이용 구매자/차량 비율**(독일 Bankenfachverband 설문조사 기반, 미국 Experian)
1. **신규 여신 중 차량 비중 / 여신잔액**(사우디 SAMA, 이집트 FRA, 한국 여신금융협회 할부금융 취급액)
1. **리스/렌탈 신규계약 ‘가치(금액)’**(폴란드 ZPL — 가치 기준, 대수 아님)

따라서 13개국을 동일 분모로 비교하려면 보정이 필요하다.

### 항목 B: 경쟁사 IT 출처 신뢰도

공식 1차 출처는 사실상 없음. 신뢰도 순서: **준공식(벤더 공식 case study/보도자료, 고객명·도입연도 명시) > 기업공시(금융사 연차보고서 IT 섹션, 단편적) > 비정형(채용공고, 보도)**.

## Details

### 항목 A — 국가별 침투율 출처 매핑

**미국 (Tier 1).** Experian “State of the Automotive Finance Market Report”(분기별)가 사실상 시장 표준 — 예: 신차 리스 비중 Q4 2025 24.37%, captives 신차금융 53.96%(Q4 2025). 정의는 ‘금융/리스 이용 비율’. 공식 1차로는 연방준비제도 **G.19 Consumer Credit**(월간, 공개, motor vehicle loans 잔액 — passenger cars·SUV·픽업 포함, 보트·오토바이·RV 제외)와 미국 의회조사국(CRS) 보고서 IF13179(2026)가 있으며, 후자는 “At the end of 2025, there were 108 million open auto loans, and outstanding auto loan debt totaled $1.67 trillion”와 90일+ 연체율 “5.0% in the third quarter of 2025”를 명시한다. 신뢰도: 상업데이터(Experian, 침투율) + 공식 1차(Fed·CRS, 잔액). 모두 2025/2026 데이터 제공. CFPB는 감독·소비자보호 자료.

**캐나다 (Tier 2).** CFLA가 DesRosiers Automotive Consultants에 의뢰해 발간하는 “Canadian Light Vehicle Market Review”가 차량금융시장 연례 분석(준공식, 산업협회). Bank of Canada·Statistics Canada는 가계부채·차량판매 매크로만 제공. 침투율 직접 수치는 회원/유료 가능성.

**영국 (Tier 1).** FLA “Motor Finance” 통계(월간, 공개, fla.org.uk/research/motor-finance-statistics). FLA 자체 표현으로 2025년 회원사가 신차/중고차 구매에 £41.1bn 지원, 민간 신차 등록의 85% 이상을 금융 지원. 정의는 ‘민간 신차 등록 대비 금융 비율’. 준공식 1차. 2025/2026 데이터 제공. Bank of England는 매크로.

**독일 (Tier 1).** Bankenfachverband(BFACH) “Konsumfinanzierung”(연례 Ipsos/YouGov 설문, 2025판 발표). 정의는 ‘금융/리스로 구매된 PKW 비율’(설문 기반). 1차 보도자료 기준 최신치: 2025년 상반기 Kfz-Kredit 신규영업 119억 유로, 약 786,000대가 신용·리스로 금융(전년 동기 대비 -3.6%). 과거 침투율 참고치(2023 조사, Statista 인용)는 신차 약 49%·중고차 약 34%. 준공식. Deutsche Bundesbank는 소비자여신 매크로만.

**스페인 (Tier 2).** ASNEF(전국금융기관협회)가 Equifax와 “Informe de Tendencias de Crédito” 분기 발간(자동차금융 demand 포함). 준공식. Banco de España는 매크로 여신만. ASNEF 자동차금융 침투율 직접 수치는 회원자료 가능성.

**폴란드 (Tier 1, 단 정의 상이).** Związek Polskiego Leasingu(ZPL, leasing.org.pl)가 분기·연간 시장 데이터 발간, 회원 32개사 + 협력기관 데이터로 시장 100% 커버 주장.  **단 ‘가치(zł) 기준’**이며 인도대수 침투율이 아님 — 2025년 차량이 전체 리스의 73.8%, 경차(승용+소형상용)금융 67.4십억 zł(+11.6%), 소비자리스 4.1% 비중. PZWLP(차량렌탈·리스협회)는 ZPL 회원. NBP는 매크로. 준공식. 정의 상이 주의.

**한국 (Tier 1).** 여신금융협회(CREFIA)가 ‘연도별 할부금융 취급액 및 실적 잔액’, ‘연도별 리스실적 요약/업종별/물건별’을 공개(crefia.or.kr, 금감원 금융통계정보시스템 기준). 정의는 ‘할부금융 취급액/잔액’(여신금액 기준, 침투율 아님). 금감원(FSS)·한국은행은 감독·매크로. 준공식+공식.

**호주 (Tier 1).** AFIA(Australian Finance Industry Association) 2025 Motor Finance Non-Bank Lenders 보고서 — “$24.4 billion of motor vehicle finance to more than 507,000 consumer and commercial customers in 2025”, 연말 활성대출 잔액 $53 billion, “MNBLs finance almost one in ten passenger vehicles across Australia through more than 1.4 million active accounts”, 딜러 기반 대출 “around 70% of motor vehicle loans originating through dealerships”(CEO Diane Tate 인용). 준공식. ABS·APRA는 매크로/건전성.

**인도 (Tier 2).** RBI(공식, 차량대출 잔액·NBFC 자산건전성·Financial Stability Report)와 SIAM(공식, 차량판매·EV — FY2025-26 승용차 46.43 Lakh 판매 등)이 1차이나 **침투율은 직접 발표하지 않음**. 침투율은 상업조사(Mordor, TraceData, Makreo 등)에서만 산출. 신뢰도: 공식 1차(분모/분자 별도) + 상업데이터(침투율).

**브라질 (Tier 2, 단 정의 명확).** B3(거래소)의 **Sistema Nacional de Gravames(SNG)**가 차량금융 등록 기반 침투율 발간 — B3 공식 페이지가 정의를 명시: “penetração de financiamentos sobre vendas de veículos (fontes: Fenabrave e Fenauto)“이며 여신잔액은 “fonte: Banco Central do Brasil”. 2025년 730만대 금융( 신차 260만대 = 판매의 50% 이상). **가장 명시적인 ‘금융대수÷판매대수’ 정의(B3 1차 + Fenabrave/BCB 결합).** 단 중고차 총판매 공식 데이터 부재로 중고차 침투율은 미산출.  

**푸에르토리코 (Tier 3).** 별도 침투율 공식 출처 사실상 부재. 미국 연방 데이터(Fed G.19)에 주(state)별로 분리되지 않고 흡수. OCIF(금융기관감독청)는 리스기관 보고서식(Consolidated Reports on Condition and Income – Leasing Institutions)은 있으나 침투율 통계는 아님. 은행(Popular Auto, FirstBank, 신용조합 등) 개별 상품 공시만. 빈약.

**사우디 (Tier 3).** SAMA(중앙은행)가 “Annual Performance of Finance Companies Sector and Real Estate Refinance” 보고서(PDF, sama.gov.sa)에서 ‘Auto’를 별도 품목으로 분리 — 2023판 표 “Classifications of Financing Portfolio by Activity” 기준 Auto 21.2십억 SAR(총 포트폴리오 84.7십억 SAR). SAMA 데이터 기반 보도(Arab News, 2025.9, SAMA 인용)로는 2025년 2분기 금융사 총여신 99.37십억 SAR 중 auto 약 25.93십억 SAR(2위 품목), 소매 비중 약 77%. 접근: PDF + Monthly Statistics/Open Data Portal/API. **단 여신잔액일 뿐 침투율(금융차량÷판매)은 SAMA가 발표하지 않음.** 공식 1차(잔액 한정).

**이집트 (Tier 3).** FRA(Financial Regulatory Authority, fra.gov.eg)가 소비자금융 통계 발간 — 2025년 1~11월 자동차/차량이 전체 소비자금융의 17.7%(전기·전자제품 19.6% 다음), 소비자금융 잔액 96.3십억 EGP(2025), 비은행 금융 총 1.4조 EGP. CBE(중앙은행)는 매크로. **품목별 비중은 있으나 침투율 아님.** 공식 1차(비중·잔액 한정).

### 침투율 정형화(비교 가능성) 판정

- **직접 비교 가능 그룹(금융대수÷판매대수에 가까움):** 브라질(B3 SNG), 영국(FLA, 신차 등록 대비), 호주(AFIA, 승용차 10대 중 1대 — 단 비은행 한정).
- **설문 기반 구매자/차량 비율:** 독일, 미국(Experian). → 인도대수 기준 환산 보정 필요.
- **여신금액/잔액 기준(분모가 대수 아님):** 한국, 사우디, 이집트, 폴란드(가치). → 평균 차량가·평균 대출액으로 대수 환산 보정 필요, 오차 큼.
- **공통 분모 제안:** OICA/SIAM/Fenabrave 등 ‘신차 판매대수’를 공통 분모로 고정하고, 각국 금융/리스 ‘계약 대수’를 분자로 통일. 대수가 없는 국가(한국·사우디·이집트·폴란드)는 평균 금융액으로 대수 추정하는 보정계수를 적용. EU·미국은 신차/중고차 구분이 명시되므로 신차 기준으로 우선 통일 권장. 호주는 비은행만 커버하므로 은행 포함 총량으로 보정 필요.

### 항목 B — 경쟁사 코어 IT 출처

**벤더 공식 case study(준공식, 가장 신뢰):**

- **Alfa Systems:** 미국 CarMax Auto Finance(2017 계약,  2021.10 라이브), 미국 ‘Alfa Start’(US auto 전용 preconfigured SaaS), 영국 United Trust Bank·HTB·Paragon, 범유럽 Siemens Financial Services(v5 라이브, TCS·Simmons & Simmons 협업). 자동차·자산금융 전문(1990~).
- **Nucleus Software FinnOne Neo:** 인도 Cholamandalam(2006~),  Bussan Auto Finance India(Mitsui & Co./Yamaha JV, FinnOne mCollect), Sai Point Finance(4일 라이브), Esskay Fincorp, 필리핀 EastWest Bank, UAE Deem Finance, 베트남 MB Bank 등 200+ 은행/50개국, 인도 내 대출 US$500bn 관리. 인도·중동·동남아 강세.
- 과제 명시 기타 벤더(FIS, SBS, Sopra Banking, TCS BaNCS, Temenos): 벤더 사이트·보도자료에 단편 case study 존재.

**간접 출처:** Deloitte 등 컨설팅사의 ‘자동차 captive finance’ 익명화 case study(코어시스템 클라우드 마이그레이션 150개 앱, 북미 loan origination 현대화 등) — 고객명 비공개.

**판정:** 13개국 모두 정부/규제당국이 금융사 코어시스템을 공시하는 제도는 없음. 따라서 ‘공식 1차 출처 부재’를 명확히 하고, 벤더 case study(준공식)와 연차보고서·채용공고(비정형)로만 추정 가능. 커버리지: 미국·영국·인도 풍부 / 독일·호주·동남아 중간 / 사우디·이집트·푸에르토리코·폴란드·브라질 희박.

### 규제 6개 항목 — 국가별 1차 공식 출처

**1. 라이선스/감독주체:** 영국 FCA, 독일 BaFin, 스페인 Banco de España, 폴란드 KNF, 미국 주별+CFPB, 캐나다 주별, 한국 금융위/금감원, 호주 ASIC(신용)+APRA(건전성), 인도 RBI(NBFC), 브라질 BCB, 푸에르토리코 OCIF(Ley Núm. 4 de 1985 근거),  사우디 SAMA, 이집트 FRA(Consumer Finance Law No. 18 of 2020 — FRA가 모든 비은행 소비자금융 감독). 전 국가 규제당국 웹사이트·법령원문으로 1차 확정 가능.

**2. 대출기간/금리상한/세제:** 각국 규제당국 고시·법령. 미국은 주별 usury, 한국은 대부업법·여전법, 푸에르토리코는 84개월 등 상품별 상한이 은행 공시에 명시. 이집트 자동차대출 연 25% 상한은 **FRA 1차 공시가 아니라 TraceData Research(상업) 기술**(“As of 2023, the maximum allowable rate stood at 25% annually for auto loans”)이므로 상업출처로 표기하고 FRA 원문 별도 확인 필요. 1차 출처는 법령·관보.

**3. 차량세금:** PwC Worldwide Tax Summaries + 각국 국세청/관세청(예: 한국 자동차세·개별소비세). 1차 확정 가능.

**4. 개인정보:** DLA Piper “Data Protection Laws of the World” 2025판(dlapiperdataprotection.com)이 13개국 모두 커버(준공식 정리), 1차 출처는 각국 법령: 영국/독일/스페인/폴란드 GDPR+현지법, 미국 주별(20개주 포괄법, ’26.1 Indiana·Kentucky·Rhode Island 발효)+연방, 캐나다 PIPEDA, 한국 PIPA, 호주 Privacy Act(개정 1차분 진행중), 인도 DPDP Act 2023(+DPDP Rules 2025, 2025.11.13 MeitY 고시·단계적 시행, 핵심조항 2027.5 예정), 브라질 LGPD, 사우디 PDPL(2021 제정·2023.9 시행·2024.9 준수, Transfer Regulations 포함), 이집트 PDPL, 푸에르토리코(미국 연방+현지법). 해외이전: 사우디(조건부 허용, 국가안보·핵심이익 침해 불가)·인도(중앙정부 지정 제한 가능)는 조건부.

**5. 외국인 대출/채권추심:** 각국 금융·소비자보호 법령. 이집트는 FRA가 채권추심·현금화 규제 명시(위반자 블랙리스트 제도, Egyptian Federation of Consumer Finance Entities 운영). 1차 출처 확정 가능.

**6. EV:** IEA “Global EV Outlook 2025”(2025.5 발간, iea.org) + Global EV Data Explorer/Policy Explorer(공개, CC BY 4.0)가 13개국 대부분 커버. 단 데이터 출처가 EV Volumes·국가제출·ACEA·OICA 등 혼합. 각국 EV 인센티브는 정부 1차: 영국 VED(2025.4부터 EV 1년차 £10·이후 £195), 폴란드 NaszEauto(기후환경부·NFOŚiGW, KPO 재원), 사우디 Vision 2030(2030년 EV 30% 목표), 이집트 FRA EV 규정 (2023, 세제·우대금리), 캐나다 iZEV(2025.1 일시중단) 등.

## Recommendations

1. **즉시(Phase 1):** 침투율은 미국(Experian)·영국(FLA)·독일(Bankenfachverband)·브라질(B3 SNG)·호주(AFIA)·폴란드(ZPL)·한국(여신금융협회) 7개국을 ‘준공식 1차’로 채택해 대시보드 1차 버전 구축. 정의 메타데이터(분모·분자·신차/중고차·은행포함 여부)를 셀마다 태깅.
1. **보정(Phase 2):** 사우디·이집트·인도·한국·폴란드는 ‘여신잔액/가치/품목비중’을 평균 금융액으로 대수 환산하는 보정계수 적용. 공통 분모는 신차 판매대수(OICA/현지 협회)로 고정. 호주는 비은행 한정이므로 은행 포함 총량으로 환산.
1. **항목 B:** 공식 1차 출처 부재를 대시보드에 명시(신뢰도 등급 ‘준공식’이 최고치). 벤더 case study(Alfa·Nucleus 등)를 국가×벤더 매트릭스로 수집하고, 금융사 연차보고서·채용공고로 보강. 단편적·마케팅 편향을 명시.
1. **규제:** DLA Piper 2025 + IEA EV Outlook 2025 + PwC Tax Summaries를 표준 레퍼런스로 고정하고, 각 셀에 법령 원문/규제당국 URL을 1차 출처로 병기. 이집트 25% 금리상한 등 상업출처 의존 항목은 별도 ‘미검증’ 플래그.
1. **임계값(재평가 기준):** 침투율 정의 불일치 보정 오차가 ±10%p를 초과하면 해당 국가를 ’비교 불가(정성 분석만)’로 강등. 푸에르토리코는 별도 데이터 부재로 미국 본토 대리지표 사용을 기본값으로. 특정 국가 협회가 무료 1차 데이터를 신규 공개하면 신뢰도 등급을 ‘상업’에서 ‘준공식 1차’로 승격.

## Caveats

- 사우디·이집트 침투율은 중앙은행/FRA ‘여신잔액·품목비중’으로 대체한 것이며 진정한 침투율(금융차량÷판매대수)이 아니다. SAMA는 침투율을 발표하지 않음을 서브에이전트가 확인했다.
- ASNEF·CFLA·ZPL 등 일부 협회 데이터는 상세 수치가 회원전용·유료일 수 있어 공개 접근성은 제한적이다.
- 항목 B 벤더 case study는 마케팅 목적이므로 도입 범위·운영 현황이 과장될 수 있다.
- 일부 상업 시장조사(Ken Research, Mordor, IMARC 등)는 ‘in future’ 등 미래 추정·예측을 과거 사실처럼 서술하는 경향이 있어 1차 출처로 채택하지 않았다.
- Experian은 영국 상장 상업기관으로 엄밀히는 ‘공식 1차’가 아닌 ‘상업데이터’이나 미국 시장의 사실상 표준으로 준공식 취급했다.
- 사우디 Q2 2025 auto 25.93십억 SAR·총 99.37십억 SAR 수치는 SAMA 데이터를 인용한 보도(Arab News)로 확인된 것으로, SAMA 1차 표(Monthly Statistical Bulletin/Open Data Portal)에서 직접 추출 검증은 미완이다(해당 페이지 접근 오류).