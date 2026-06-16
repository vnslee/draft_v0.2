# 신규 국가 진출용 오토파이낸스 에이전트 대시보드: 데이터 항목별 공식 출처 매핑 (2025년 기준)

## TL;DR

- 거시·시장·규제 대부분의 항목은 **공식·준공식 출처가 실재하고 2025년 데이터를 제공**한다(IMF WEO 2025, OICA 2025, IEA Global EV Outlook 2025, ACEA/CAAM/SIAM/KAMA, DLA Piper 2025, PwC WWTS, 각국 중앙은행/금융감독당국 등록부, OEM·캐피탈 공시).
- 그러나 **두 항목은 공식 출처가 구조적으로 취약**하다: (1) 국가 간 비교 가능한 단일 **오토파이낸스 침투율(penetration rate)** 공식 출처는 사실상 없으며 국가별로 조립해야 한다(브라질 B3/SNG, VW 캐피탈 공시 등 부분적), (2) **경쟁사 코어 IT 시스템** 정보는 공식 출처가 사실상 없고 벤더 보도자료·도입사례에만 의존한다.
- 결론: 대시보드는 거시/판매/규제/세제/EV 항목은 공식 API·DB·PDF로 자동 갱신이 가능하나, 침투율과 경쟁사 IT는 준공식·상업 출처 혼합 + 수동 검증 설계를 전제해야 한다.

## Key Findings

대시보드의 데이터 항목을 5개 카테고리로 나눠 공식 출처 존재 여부를 ‘있음/부분적/사실상 없음’으로 판정했다.

|데이터 항목        |판정    |대표 공식 출처                                     |2025  |커버리지       |접근            |
|--------------|------|---------------------------------------------|------|-----------|--------------|
|GDP 명목/실질성장률  |있음    |IMF World Economic Outlook DB (2025년 4월·10월판)|O     |글로벌(~190개국)|공개 DB/SDMX/엑셀 |
|권역 분류         |있음    |UN M49(UNSD), World Bank region              |O(상시) |글로벌        |공개 DB/엑셀      |
|연간 자동차 판매대수   |있음    |OICA, ACEA, CAAM, SIAM, KAMA                 |O     |글로벌+국가     |PDF/공개표(일부 유료)|
|판매 CAGR 시계열   |있음    |OICA·각 협회·MarkLines                          |O     |글로벌+국가     |PDF/유료DB      |
|오토파이낸스 침투율    |부분적   |국가별: B3(브라질), Experian(미국, 상업), VW 캐피탈 공시    |O(국가별)|국가별·정의 불일치 |PDF/유료/공시     |
|오토파이낸스 CAGR   |부분적   |중앙은행 여신통계(Fed G.19 등) + 협회                   |O     |국가별        |공개DB/PDF      |
|경쟁사 TOP3 식별   |있음    |금융감독당국 등록부 + 각사 재무제표                         |O     |국가별        |공개등록부/공시      |
|OEM 판매량(현대/기아)|있음    |현대차·기아 IR/사업보고서, OICA, MarkLines             |O     |글로벌        |공시/PDF/유료     |
|라이선스 유무·주체    |있음    |각국 중앙은행/금융감독당국                               |O(상시) |국가별        |공개등록부/법령      |
|대출기간·세제혜택     |있음    |법령/관보, 규제당국                                  |O     |국가별        |법령DB/PDF      |
|차량 세금         |있음    |국세청/재무부 + PwC WWTS·자동차세 가이드                  |O     |글로벌        |공개온라인/PDF     |
|개인정보보호법       |있음    |현지법 원문 + DLA Piper 2025                      |O     |160+ 관할권   |공개온라인/PDF     |
|EV 수요·충전인프라   |있음    |IEA Global EV Outlook 2025 + Data Explorer   |O     |글로벌        |공개DB/PDF      |
|외국인 대출·채권 규제  |있음    |금융감독당국/중앙은행/법령                               |O     |국가별        |법령/PDF        |
|신차/중고차 이용현황   |부분적   |중앙은행·신용정보기관·협회                               |O     |국가별        |공개DB/PDF/유료   |
|경쟁사 상품·이율·약관  |부분적   |각사 공시·약관·웹사이트                                |O     |국가별        |비정형/공시        |
|경쟁사 코어 IT 시스템 |사실상 없음|(공식 출처 없음) 벤더 보도자료·도입사례                      |△     |비정형        |비정형           |

## Details

### 1. 국가별 기본 데이터

**GDP 명목 및 실질 성장률 — 판정: 있음.** 기본 출처로 전제한 **IMF World Economic Outlook(WEO) Database**는 2025년 4월판과 10월판이 모두 발간되어 있으며, 명목 GDP(NGDPD), 실질 GDP 성장률 등을 1980년부터 당해 및 향후 2년 전망까지 제공한다. 2025년 4월판은 “A Critical Juncture amid Policy Shifts” 부제로 발간되었고, 데이터는 SDMX 포맷과 엑셀로 다운로드 가능한 완전 공개 DB다(imf.org/en/publications/weo/weo-database/2025/april). 보완적으로 World Bank Global Economic Prospects도 존재한다. 다만 WEO 수치는 2025년 내에도 4월→7월 업데이트→10월로 수정되므로(예: 2025년 글로벌 성장률 전망이 4월 대비 7월 29일 업데이트에서 3.0%로 상향) 대시보드는 판본·발표일을 명시해야 한다.

**권역 분류 기준 — 판정: 있음.** UN Statistics Division의 **M49 표준(Standard Country or Area Codes for Statistical Use)**이 공식 분류로, 세계를 5개 대륙 권역(아프리카 002, 아메리카 019, 아시아 142, 유럽 150, 오세아니아 009)과 22개 소권역으로 나누고 249개 국가·지역에 3자리 코드와 ISO 코드를 부여한다(unstats.un.org/unsd/methodology/m49/). 별도로 **World Bank 6대 운영 권역**(East Asia & Pacific, Europe & Central Asia, Latin America & Caribbean, Middle East & North Africa, South Asia, Sub-Saharan Africa)이 있다. 사용자가 요청한 북미/남미/아태/유럽/중동 권역 구분은 M49 또는 World Bank 분류를 베이스로 커스터마이징하면 된다. 둘 다 공개 다운로드 가능.

### 2. 시장 정보

**연간 자동차 판매대수 — 판정: 있음.** **OICA(국제자동차공업협회)**가 글로벌 표준으로 sales-statistics 페이지에서 연도별 판매·생산을 제공하며 2025년 데이터까지 포함한다. OICA 발표(Shailesh Chandra 회장, 2026년 4월 29일 베이징 모터쇼)에 따르면 “global vehicle sales increased to 99.8 million units in 2025 from 95.3 million units in 2024, posting a growth of 4.7 per cent” — 즉 2025년 글로벌 판매 9,980만 대(+4.7%)다. 국가별로는 **ACEA(유럽), CAAM(중국), SIAM(인도, 회계연도 기준), KAMA(한국)**가 각각 공식 협회 데이터를 발표하며 모두 2025년 자료를 제공한다. CAAM은 2026년 1월 14일 발표에서 2025년 중국 신차 판매가 9.4% 증가한 3,444만 대(생산 3,453.1만 대, +10.4%), NEV 1,649만 대(점유율 47.9%)라고 공표했다. 단 OICA·각 협회 데이터는 무료 PDF/표가 기본이나 일부 상세 시계열은 유료(MarkLines 등)다. 주의: 인도 SIAM은 회계연도(4월–3월) 기준이고 일부 OEM(BMW, Mercedes, JLR 등) 제외 도매(wholesale) 기준이라 정의 차이가 있다.

**판매 CAGR 산출용 시계열 — 판정: 있음.** OICA가 2005년 이후 연도별 시계열을 제공하고, MarkLines는 글로벌 판매의 99% 커버리지로 국가·모델별 월간/연간 데이터를 제공한다(유료 구독).  CAGR은 이 시계열로 직접 산출 가능.

**오토파이낸스/리스 침투율 — 판정: 부분적 (핵심 취약점).** 조사 결과 **국가 간 비교 가능한 단일 공식 침투율 출처는 사실상 존재하지 않는다.** 중앙은행(미국 Fed G.19, 브라질 BCB)은 침투율이 아니라 **여신 잔액·신규 취급액**만 공표한다. 실재하는 출처는 국가별로 조립해야 하며 정의도 제각각이다:

- **미국**: Experian “State of the Automotive Finance Market Report”가 분기별로 신차/중고차 금융 비중을 제공한다. Q4 2025판(2026년 3월 5일 발표)에 따르면 신차 금융 비중은 전년 41.20%에서 42.20%로 상승, 중고차는 57.80%이며, 총 시장 점유율은 은행 29.29%·캐피탈(captives) 27.55%·신협 19.56%다. 단 Experian은 정부·협회가 아닌 상업적 데이터 기업이다 — “A FTSE 100 Index company listed on the London Stock Exchange (EXPN), we have a team of 25,200 people across 33 countries”(Experian plc). 비록 Fed G.19가 일부 입력값(finance company 신차론 조건)으로 Experian을 인용할 만큼 사실상의 벤치마크이지만 ‘공식’은 아니다.
- **유럽**: Eurofinas(Facts & Figures, Annual Statistical Enquiry)·Leaseurope가 차량금융 볼륨·상품믹스를 제공하나  **등록대수 대비 침투율 비율은 직접 공표하지 않는다.** 2025년은 Biannual(반기) 통계만 공개 수준(예: 2025년 상반기 신규 소비자금융 중 29%가 차량 관련).
- **브라질**: **B3(브라질 거래소)의 SNG(국가차량담보등록시스템)**가 “penetração de financiamentos sobre vendas de veículos(차량 판매 대비 금융 침투율)“를 Fenabrave/Fenauto 판매 데이터와 BCB 여신 포트폴리오를 결합해 월간 공표한다 — 조사된 출처 중 가장 ‘공식’에 가까운 침투율 데이터다(2025년 신차 약 50% 이상 금융).
- **OEM 캐피탈 공시**: Volkswagen Financial Services는 연차보고서에서 침투율을 명시적으로 정의·공표한다. Volkswagen Group Annual Report 2025: “The ratio of leased and financed vehicles to Group deliveries (penetration rate) increased to 37.2 (34.1)% in the Financial Services Division’s markets in the reporting year.” 단 자사 인도분 한정이라 시장 전체 침투율은 아니다(독일 단독으로는 인도분의 약 70%, EV는 82%로 공시).

결론: 대시보드는 침투율을 단일 글로벌 소스로 채울 수 없고, 국가별 출처(중앙은행+협회+거래소+캐피탈 공시)를 조합하고 **정의 불일치를 명시**해야 한다.

**오토파이낸스 성장률(CAGR) — 판정: 부분적.** 미국 Fed G.19의 모터비클론 잔액 시계열(분기별 “Motor Vehicle Loans” memo item), 유럽 Eurofinas 신규취급 시계열 등으로 잔액·취급액 기준 CAGR은 산출 가능하나, ‘침투율 CAGR’은 위 침투율 한계를 그대로 승계한다.

**국가별 주요 경쟁사 TOP 3 식별 — 판정: 있음.** 두 공식 출처 조합으로 확인 가능: (1) **금융감독당국 등록부**(영국 FCA Financial Services Register, UAE 중앙은행 Finance Companies Regulation, 스리랑카·인도 RBI 등록 NBFC, 미국은 주별 sales finance 라이선스 + CFPB Larger Participant Rule)로 인가·등록 주체 식별, (2) **각사 재무제표/연차보고서**로 규모 순위. 토요타 파이낸스(TMCC가 3월 결산 기준 SEC에 분기·연차 보고), 폭스바겐 파이낸스(VW Group Annual Report 2025 Financial Services 섹션, 2025년 말 총 계약 3,000만 건)는 모두 공시로 확인된다.

**OEM 판매량(현대/기아) — 판정: 있음.** 현대차는 IR(분기실적·CEO Investor Day·사업보고서)에서 상세 공시를 제공한다. Hyundai Motor 2025 Annual & Q4 Business Results(2026년 1월 29일): “the company sold 4,138,389 vehicles worldwide, nearly unchanged from 2024” — 즉 2025년 글로벌 4,138,389대, 전동화 차량 약 23%(961,812대, +27% YoY). 기아도 동일 구조의 IR을 운영한다. 보완으로 OICA·MarkLines가 OEM별 글로벌 판매를 집계한다. 모두 2025년 자료 존재.

### 3. 규제

**오토파이낸스 라이선스 유무·주체 — 판정: 있음.** 각국 중앙은행/금융감독당국이 공식 등록부를 운영한다: 영국 FCA Financial Services Register(공개 검색),  UAE 중앙은행 Finance Companies Regulation, 스리랑카 중앙은행 Licensed Finance Companies, 인도 RBI NBFC 등록, 미국은 주(state) 단위 sales finance license + 연방 CFPB의 Automobile Financing Larger Participant Rule(2015년 6월 30일 최종규칙, 2025년 임계값 재검토 ANPR 진행, 의견제출 마감 2025년 9월 22일). 상시 갱신.

**금융 상품별 최소/최대 대출기간·세제혜택 — 판정: 있음.** 법령·관보 및 규제당국 고시가 1차 출처. 보완적으로 PwC·법무법인 가이드. 단 상품별 최소/최대 기간은 국가별 법령이 산재해 통합DB는 없고 국가별 수집 필요.

**차량 보유/구매 세금 — 판정: 있음.** 1차 출처는 각국 국세청/재무부/관세청. 통합 검토용으로 **PwC Worldwide Tax Summaries(145~150여 개 관할권, 무료 온라인, 현지 PwC 전문가 갱신)**와 PwC Global Automotive Tax Guide(차량 특화)가 사실상의 표준 정리본이다. 계산식·납부시점까지 포함.

**개인정보보호법 — 판정: 있음.** 1차 출처는 현지 개인정보보호법 원문(예: EU GDPR, 중국 PIPL, 인도 DPDP Act 2023).  통합 정리본으로 **DLA Piper Data Protection Laws of the World(2025년 14판, 160+ 관할권, 무료 온라인)**가 개인정보 정의·보유·해외이전 등을 관할권별로 제공한다. 2025년 갱신 확인.

**친환경차(EV) 수요·충전 인프라 — 판정: 있음.** **IEA Global EV Outlook 2025**(2025년 5월 14일 발간)와 부속 Global EV Data Explorer/Policy Explorer가 판매·재고·충전소·정책을 국가별로 제공한다(Licence: CC BY 4.0 공개). Executive Summary: “Electric car sales exceeded 17 million globally in 2024, reaching a sales share of more than 20%… In 2025, sales of electric cars are expected to surpass 20 million, accounting for over a quarter of cars sold worldwide.” 후속 **Global EV Outlook 2026**도 발간되어 실적을 확정했다: “Electric car sales grew by 20% globally to exceed 20 million in 2025, meaning one-quarter of all new cars sold were electric”(중국 EV가 전체 신차의 약 55%).

**외국인 대출 가능 여부·채권 규제 — 판정: 있음.** 금융감독당국/중앙은행 규정 및 법령이 1차 출처. 국가별 외환·여신 규제로 산재하나 공식 출처는 존재.

### 4. 오토파이낸스 상세

**금융 침투율 — (위 2번과 동일, 부분적).**

**신차/중고차(은행/여신사) 이용 현황 — 판정: 부분적.** 미국은 Experian(신차 vs 중고차 금융 비중, 은행/캐피탈/신협 점유율 분기 공표) + Fed G.19. 중앙은행·신용정보기관·협회가 국가별로 존재하나 신차/중고차 분해 + 은행/여신사 분해를 동시에 공표하는 곳은 제한적이다. 미국 NAF Association/AFSA 공동 Non-Prime Automotive Financing Survey도 준공식 보완 출처(유료).

**주요 경쟁사 TOP3 및 로컬 회사 — 판정: 있음.** 금융감독당국 등록부 + 재무제표(위 참조). 로컬 회사도 등록부로 식별 가능.

**경쟁사 취급 상품·이율·딜러십·계약방식 — 판정: 부분적.** 각사 공시·약관·웹사이트가 1차 출처지만 비정형이고 표준화되어 있지 않다. 최소-최대 이율은 각사 공시/약관 또는 규제당국 고시로 부분 확인.

**경쟁사 코어 시스템/IT 솔루션 — 판정: 사실상 없음 (핵심 취약점).** 이 항목의 **공식 출처는 존재하지 않는다.** 확인 가능한 정보는 모두 (1) IT 벤더(Alfa Systems, NETSOL, FIS Asset Finance, Nucleus Software FinnOne Neo, SBS 등)의 보도자료·도입사례·고객 인용, (2) 채용공고, (3) LinkedIn/컨퍼런스(AFSA Vehicle Finance Conference) 등 비정형 소스다. 예컨대 Alfa Systems는 CarMax Auto Finance·Siemens Financial Services·Novuna 등을 사례로 공개하나, 이는 마케팅 자료이지 금융사 측 공식 공시가 아니다. enlyft 같은 기술스택 추정 서비스가 있으나 추정치다. 대시보드는 이 항목을 ‘추정·비정형’으로 명시하고 수동 검증을 전제해야 한다.

## Recommendations

1. **즉시 자동화 가능한 항목(공개 API/DB)을 1차 통합하라**: IMF WEO(SDMX), UN M49, IEA Global EV Data Explorer, 미국 Fed G.19(Data Download Program), FCA 등록부. 이들은 무료·구조화·2025 데이터 제공으로 대시보드 백본으로 적합하다.
1. **PDF/표 기반 준자동 항목**: OICA·ACEA·CAAM·SIAM·KAMA 판매, 현대/기아 IR, DLA Piper·PwC 정리본. 분기/연간 파싱 파이프라인 구축. 발표 주기·판본 메타데이터를 반드시 기록(특히 IMF WEO 4월/10월, Experian 분기).
1. **침투율은 ‘국가별 조립 + 정의 태깅’ 방식으로 설계하라**: 단일 글로벌 소스가 없으므로 미국=Experian, 브라질=B3/SNG+Fenabrave, 유럽=Eurofinas/Leaseurope, 캐피탈=VW(37.2%)/Toyota 공시를 매핑하고, 각 셀에 정의(인도대수 대비 vs 구매자 비율 vs 상품믹스)를 라벨링. 비교 시 동일 정의만 비교.
1. **경쟁사 IT 시스템은 별도 ‘저신뢰·비정형’ 트랙으로 분리하라**: 벤더 보도자료·도입사례·채용공고를 수집하되 출처를 명시하고 신뢰도 등급(추정)을 부여. 공식 데이터로 취급 금지.
1. **국가별 라이선스·세금·대출기간은 진출 후보국이 정해질 때 심층 1차 법령 수집을 트리거하라**: 통합 DB가 없으므로 PwC WWTS/DLA Piper로 1차 스크리닝 후 현지 법령·규제당국으로 확정.

**임계값/판단 변경 기준**: (a) 어떤 항목이라도 출처가 상업 단일 소스(Experian, MarkLines)에만 의존하면 ‘부분적’으로 강등하고 대체 공식 소스 탐색. (b) 침투율 정의가 국가 간 불일치하면 비교 차트에서 제외. (c) 경쟁사 IT 정보가 단일 벤더 자료에만 근거하면 대시보드 노출 보류.

## Caveats

- **상업 vs 공식 구분**: Experian, MarkLines, Mordor/Grand View 등은 권위 있으나 정부·협회가 아닌 상업 소스다. 사용자 정의상 ‘공식’에 미달하므로 본 보고서는 이를 ‘준공식/상업’으로 표기했다. Experian은 FTSE 100 상장사(LSE: EXPN, 33개국 25,200명)다.
- **정의 불일치**: ‘침투율’은 (1) 금융·리스 인도대수 ÷ 총 인도대수(VW, 브라질 B3), (2) 금융 이용 구매자 비율(미국 Experian의 신차 80%대 금융), (3) 금융 상품믹스 점유(Eurofinas)로 정의가 달라 직접 비교 불가.
- **회계연도·집계 기준 차이**: 인도 SIAM(4–3월, 일부 OEM 제외 도매), 토요타(3월 결산) 등 기준 상이.
- **전망치 주의**: IMF WEO 전망, VW 2026 가이던스, IEA STEPS 시나리오 등은 전망(forecast)이며 실적과 구분 필요. IEA EV 2025판의 2025년 수치는 당초 전망이었고 2026판이 이를 실적으로 확정했다.
- **중동·일부 신흥국 커버리지**: 침투율·신차/중고차 분해·경쟁사 IT는 중동·아프리카·일부 아태 신흥국에서 공식 출처가 더욱 희박하다. 권역별로는 북미·유럽이 가장 풍부하고, 중동·신흥 아태가 가장 빈약하다.