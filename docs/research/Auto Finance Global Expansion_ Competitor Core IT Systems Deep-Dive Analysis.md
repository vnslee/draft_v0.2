# 오토파이낸스 글로벌 진출 — 경쟁사 코어 IT 시스템 심층 조사 (대시보드 항목 B)

## TL;DR

- **유럽은 우리 타깃(NETSOL NFS Ascent)과 정합성이 가장 높다(이식 난이도 中)**: NFS Ascent는 무기명이지만 정황상 Daimler/BMW로 추정되는 “leading German auto captive”와 2015년 체결한 12개국·$110M(NETSOL 사상 최대) 계약을 보유하고, Ikano Bank(스웨덴)·영국 스타트업 은행으로 확산 중이다. 다만 영국·독일·스페인·폴란드 주요 경쟁사 다수는 Alfa Systems, Sopra(SFP/Cassiopae), VWFS 자체구축을 써, “경쟁사가 NETSOL을 쓴다”는 부분적으로만 사실이다.
- **APAC는 Oracle DB+Java 생태계로는 정합하나 ‘Oracle ADF’ 일치는 어떤 경쟁사에서도 1차 출처로 확인되지 않았다(이식 난이도 中)**: 현대캐피탈(한국)=Cassiopae(Java/J2EE+Oracle), KB캐피탈=LG CNS 차세대(Java+Pro*C/Oracle), 인도=Nucleus FinnOne Neo(Java/SOA), 사우디 SFC=Nucleus FinnOne — 전부 Oracle DB+Java 계열이지만 ADF 프레젠테이션 프레임워크를 명시한 사례는 없다.
- **미국은 Salesforce가 코어 엔진이 아니라 고객접점(CRM/loan-lease console) 계층에서만 정합(이식 난이도 中~상)**: Toyota Financial Services가 Salesforce Automotive Cloud를 채택했으나, 미국 코어 originations/servicing/collections 시장의 사실상 표준은 defi SOLUTIONS·Shaw Systems·Alfa이며 이들과는 계층이 달라 코어 대체 시 추가 통합이 불가피하다.

## Key Findings

**1) 벤더→고객 매핑 (가장 신뢰도 높은 준공식 근거)**

- **NETSOL NFS Ascent**: NETSOL 글로벌 세일즈 디렉터는 Mercedes-Benz, BMW, Ford, Nissan, Toyota, Hyundai, Geely, Volvo를 25년간 auto captive 고객으로 명시. 유럽 실적은 ① 영국 스타트업 은행 클라우드 go-live(2022, NFS Ascent 유럽·은행권 최초), ② Ikano Bank(스웨덴, 북유럽 다국 클라우드 롤아웃), ③ 한국의 무기명 독일계 captive full-suite go-live(2024.4). 단일 최대 건은 **2015년 체결, 12개국, $110M 초과 — NETSOL 사상 최대 계약** 으로 고객은 전 PR에서 “leading German auto captive”로 무기명이다(정황상 Daimler 또는 BMW Korea 추정, 확정 불가).
- **Alfa Systems**: Toyota Financial Services, Mercedes-Benz, Daimler Truck, PACCAR, John Deere Financial, CarMax가 라이브 고객(Alfa 공식: “Our live customers…include Toyota Financial Services, Mercedes-Benz and CarMax”).  영국 본사·FTSE250·클라우드 네이티브 SaaS.
- **Sopra Banking(SBS)**: Santander, Société Générale, Mercedes-Benz, Toyota, Honda Finance Europe가 고객. Hyundai Capital America는 Cassiopae로 **2020년 5월 20일 go-live(15개월 프로젝트, 500만+ 계약 이관, 현재 200만+ 활성계약 관리)** — HCA CIO Hwanjun Yang: “Hyundai Capital America now has an advanced IT system best-optimized for its market.” 
- **Nucleus FinnOne Neo**: 인도 Cholamandalam(2006~), Tata Capital Housing, L&T Financial, DCB Bank; **사우디 Saudi Finance Company(2014년 파트너십 개시, FinnOne™ 코어, Auto·Personal·SME 전 영역, SAMA 준거·ZATCA API 연동)** — SFC CEO Bander Al-Samman가 직접 인용. 호주 Bank of Sydney는 FinnOne Neo CAS 사용.
- **defi SOLUTIONS / Shaw Systems(미국)**: captive·은행·credit union·specialty lender. **Shaw는 Roy Shaw가 1967년 창업, 8개국 300+ 고객**(“Over 300 clients in eight countries”).  defi는 Fiserv·Warburg Pincus·Bain Capital 투자, no-code SaaS.

**2) 경쟁사→시스템 역추적**

- **Volkswagen Financial Services**: 단일 코어 벤더가 아니라 자체+멀티벤더. DB는 Oracle Exadata Cloud@Customer로 이관(2023, 지연 60%↓·분석 50%↑), 컨테이너 VMware Tanzu(TKGI/NSX-T), 통합 MuleSoft+AWS, 문서처리 SAP 기반. → NETSOL/Alfa형 단일 코어가 아니라 자체구축 중심이라 직접 대체 난이도가 가장 높음.
- **현대캐피탈(한국)**: Cassiopae(Sopra)=“글로벌 IT 표준 플랫폼” 차세대. **HCS는 2016년 6월부터 Cassiopae 프로덕션(HCI는 2015년 6월)**, 현대캐피탈 CIO Gun Woo Kim: “This is the first successful case of applying a packaged solution to core financial business in Korea.”   2005년 레거시(LG CNS+현대오토에버 자체구축, IBM BCS 감리, 약 400억·연인원 6,000명) → Cassiopae 패키지로 교체. Java/J2EE+Oracle 스택.
- **KB캐피탈**: LG CNS 차세대(2019 완료), 채용공고상 Java+Pro*C(Oracle 임베디드 C)/Oracle DB·Oracle 인증 우대. 하나캐피탈: 하나금융티아이 “DT Rebuild”(2023.12, 17개월·약 240억). 우리금융캐피탈·신한캐피탈(리테일 오토 철수)은 1차 출처 미확인.
- **Hyundai Capital America**: Cassiopae 코어 + Oracle EBS/HCM + NetSol LeasePak Cloud(리스 관리, appsruntheworld 데이터 브로커=비정형).
- **Toyota Financial Services(미국)**: **Salesforce Automotive Cloud(2022.9 출시)의 Captive Finance·Automotive Loan and Lease Console 채택** — TFS 디지털정보책임자 Angela Baker: “Technology like Salesforce’s Automotive Cloud is exciting because it will help us build more meaningful relationships with our customers.” 

**3) 모듈별 분해**

- **NFS Ascent**: Omni POS(originations) + CMS(loan&lease/contract management) + WFS(wholesale floorplan) + DAAS(dealer/auditor).
- **Alfa Systems**: 단일 플랫폼에 originations·servicing·collections·remarketing 통합.
- **Nucleus FinnOne Neo**: CAS(Customer Acquisition=originations) + LMS(management) + Collections/Delinquency.
- **defi SOLUTIONS**: ORIGINATIONS + SERVICING + MANAGED SERVICING(collections·repossession·bankruptcy 포함).
- **Sopra SFP/Cassiopae**: Portfolio Management(onboarding·credit·risk) + wholesale/floorplan; 일부 모듈은 Salesforce 위 구축(SBS 공식).

## Details — 국가 × 경쟁사 × 모듈 × 벤더/스택 매트릭스

### 유럽 (타깃: NETSOL NFS Ascent / NFS Digital)

- **영국**: Black Horse(Lloyds, 시장 리더, Lex Autolease와 함께 모터부문)·Santander Consumer UK(Stellantis 파트너)·Close Brothers·MotoNovo가 주요 경쟁사. 개별 코어 벤더는 공개 1차 출처 부족(한계). NETSOL은 영국 스타트업 은행 클라우드 go-live(2022)와 대형 중고차 금융사 Wholesale 계약(~$4M)으로 유럽 첫 거점 확보. Alfa도 영국 본사. **정합성 中**(NETSOL 레퍼런스 존재하나 대형 경쟁사 상당수 Alfa/자체).
- **독일**: VWFS(자체+Oracle Exadata/멀티벤더), Mercedes-Benz Mobility·BMW FS(NETSOL captive 관계 추정). **정합성 中~상**(타깃 벤더 핵심 레퍼런스 본거지이나 VWFS 자체구축은 직접 대체 난이도 높음).
- **스페인**: Santander Consumer Finance(범유럽 auto 리더), VWFS España, BBVA. Santander는 SBS 고객으로 표기. 스페인 법인 단위 코어는 1차 출처 제한적(한계). **정합성 中**.
- **폴란드**: PKO Leasing, mLeasing, Santander Consumer Bank, VW Bank Polska(Softax/STX Next가 딜러 리스 신청 시스템 구축), Toyota Bank Polska, BMW FS Polska. 로컬 SI 비중 큼. **정합성 中~하**(로컬 커스텀·captive 본사 시스템 혼재).

### 북미 (타깃: Salesforce)

- **미국**: 코어 표준=defi SOLUTIONS·Shaw Systems(1967~, 300+고객)·Alfa(Toyota·Mercedes·CarMax). Salesforce는 Automotive Cloud(captive finance)로 TFS 등 CRM/engagement 계층. **정합성 中~상**: Salesforce 기반 솔루션은 고객접점·loan/lease console에 정합하나 경쟁사 코어 계약·채권 엔진(defi/Shaw/Alfa)과 계층이 달라 코어 대체 시 추가 통합 필요.
- **캐나다**: Hyundai Capital Canada(현대 글로벌 표준 Cassiopae 후보), TD Auto Finance, Ford Credit Canada. 1차 출처 제한적(한계). **정합성 中**.

### APAC (타깃: 한국 사용 코어 = Oracle ADF/Java)

- **한국**: 현대캐피탈=Cassiopae(Java/J2EE+Oracle), KB캐피탈=LG CNS 차세대(Java+Pro*C/Oracle), 하나캐피탈=하나금융티아이 DT Rebuild, 무기명 독일계 captive=NETSOL NFS Ascent(2024). 전부 Oracle DB+Java 계열이나 **‘Oracle ADF’ 명시 사례 없음**. **정합성 中~상**(Oracle/Java 생태계 공통, ADF 일치 미확인).
- **호주**: Angle Auto Finance(독립 1위, Cerberus 소유, “새 시스템 구축”), Pepper Money, Toyota Finance. **Alfa가 2025년 9월 15일 ANZ용 ‘Alfa Start’ 프리컨피그 SaaS 출시(단일 인스턴스 AUD·NZD·USD, PPSR·SSO·ISO 20022 통합, originations~collections 전 라이프사이클)** 로 비은행/captive 코어에서 선점 강화. **정합성 中**.
- **인도**: Nucleus FinnOne Neo(Java/SOA, Cholamandalam·Tata·L&T 다수), TCS BaNCS, Toyota Financial Services India. Oracle DB+Java 계열로 한국 타깃과 기술 정합성 최상. **정합성 상**.

### 남미 (권역 솔루션 미지정 — 근접도 평가)

- **브라질**: 은행계(Itaú·Bradesco·Santander·Banco do Brasil·Caixa) + captive(Banco Mercedes-Benz·Banco Volkswagen·Banco Stellantis·Banco Toyota·Banco Honda) + 독립(Rodobens). captive는 글로벌 본사 시스템(VWFS=자체, Mercedes/Toyota=Alfa·Sopra) 추종 가능성. 브라질 로컬 코어 벤더는 1차 출처 부족(한계). **근접: 유럽 NETSOL(captive 관계) 또는 미국 Salesforce(engagement).**
- **푸에르토리코**: 미국 시스템 생태계(defi/Shaw/Salesforce) 영향권, 1차 출처 거의 없음(한계). **근접: 미국 Salesforce.**

### 중동 (권역 솔루션 미지정 — 근접도 평가)

- **사우디아라비아**: Saudi Finance Company=Nucleus FinnOne(2014~, Auto/Personal/SME, SAMA/ZATCA, Java/SOA). Abdul Latif Jameel(Toyota captive)·Al Rajhi·SNB 코어는 1차 출처 미확인. NETSOL “Atheeb NetSol” JV는 사이버보안/컨설팅 위주로 auto 코어 go-live 없음. **근접: APAC Nucleus 계열(Java/Oracle)이 한국 Oracle/Java 타깃과 정합.**
- **이집트**: Contact Financial/ContactCars, valU(EFG Hermes), GB Auto/Drive 모두 코어 시스템 벤더 1차 출처 전무(완전한 정보 공백). **근접 솔루션 판단 불가 — 추가 현장 실사 필수.**

## 기술 스택·아키텍처 요약

- **NFS Ascent**: Java/J2EE, Oracle DB, 분산·클러스터 배포, on-prem+AWS 클라우드(SaaS 구독 전환 중), API-first 마켓플레이스(AppexNow/Flex).
- **Alfa Systems**: 클라우드 네이티브 SaaS(Alfa Cloud), 단일 플랫폼, ML 의사결정, ISO 20022, 오픈소스(OIN 가입).
- **Sopra SFP/Cassiopae**: Java/J2EE, Oracle SOA/Linux, 클라우드+on-prem, 일부 Portfolio Management은 Salesforce 위 구축.
- **Nucleus FinnOne Neo**: Java, SOA, 600+ API,  OS/DB 독립, 클라우드+on-prem, AI 플랫폼 내장.
- **defi SOLUTIONS**: SaaS, no-code, 컨테이너화/클라우드 네이티브 지향.
- **VWFS(자체)**: Oracle Exadata Cloud@Customer + VMware Tanzu + MuleSoft/AWS + SAP 문서.
- **한국 캐피탈**: Oracle DB + Java/Pro*C(현대=Cassiopae, KB=LG CNS). ‘Oracle ADF’ 명시 사례 없음.

## Recommendations

1. **유럽(NETSOL) — 단계 1**: 독일·영국을 우선 진입로로. NETSOL의 Mercedes/BMW captive 레퍼런스와 영국 클라우드 go-live를 세일즈 레버리지로 활용. VWFS(자체)·Alfa 고객(스페인 일부)·로컬 SI(폴란드)는 직접 대체 대신 병행/단계 이행. **변경 임계점: 경쟁사가 Alfa/Sopra 멀티이어 계약을 보유하면 진입을 코어 리프레시 사이클(통상 7~10년)에 맞춰 타이밍 조정.**
1. **APAC(Oracle/Java) — 단계 1(병행)**: 인도(Nucleus, Java·Oracle)가 기술 정합성 최상 → 1순위 진입. 한국은 자사 코어가 이미 Oracle/Java라 현지 Oracle 인증·Java 인재풀 확보 용이. 호주는 Alfa “Alfa Start” 선점 중이므로 신규 비은행(Angle류)·captive 타깃. **변경 임계점: 타깃 솔루션이 실제 ‘Oracle ADF’라면 현지 경쟁사·인재풀에 ADF 부재 → 진입 전 ADF→일반 Java/Spring 추상화 가능 여부를 반드시 점검.**
1. **미국(Salesforce) — 단계 2**: Salesforce는 engagement/loan-lease console 레이어로 포지셔닝하고 코어 계약·채권 엔진은 defi/Shaw/Alfa 통합 또는 자체 코어로 보완. TFS Automotive Cloud 사례를 정합 근거로 활용. **변경 임계점: 코어 servicing 정확도(penny-accurate)·대량 배치에서 Salesforce 단독이 부족하면 별도 코어 엔진 채택.**
1. **남미·중동 — 단계 3(기회주의적)**: 브라질은 captive 본사 시스템 추종 가능성이 높아 NETSOL(유럽 권역) 레버리지. 사우디는 Nucleus(Java/Oracle)가 현지 표준에 가까워 APAC 권역 솔루션과 정합. **이집트는 정보 공백이 커 진입 전 현지 1차 실사(연차보고서·FRA 등록정보·채용공고) 완료를 선행 조건으로 둘 것.**

## Caveats

- **출처 신뢰도 등급**: 벤더 공식 case study/PR=준공식(NETSOL·Alfa·Sopra·Nucleus·Salesforce 인용), 기업 IR/공시=기업공시(KB캐피탈 보도, VW 연차보고서, SFC-Nucleus PR), 채용공고·기술기사=비정형(N-System/랜더스 JobKorea, etnews, appsruntheworld). appsruntheworld는 데이터 브로커로 비정형 처리.
- **‘Oracle ADF’ 정합성 검증 한계**: 한국·인도·사우디 경쟁사 전부 Oracle DB+Java이나 ‘Oracle ADF’ 프레젠테이션 프레임워크를 명시한 1차 출처는 없음. Cassiopae·NFS Ascent·FinnOne 모두 Java/J2EE(ADF 아님). 자사 타깃이 진정한 ADF 기반이라면 시장 표준과의 미세한 기술 격차가 현지 인재·SI 파트너 확보에 영향을 줄 수 있음.
- **고객명 익명 처리**: 한국·12개국 $110M 계약의 고객은 NETSOL PR 전반에서 “leading German auto captive”로 무기명. NETSOL 매출 집중도(Daimler/BMW)로 Mercedes 또는 BMW Korea 추정되나 1차 출처로 확정되지 않음.
- **정보 공백 국가/기업**: 이집트(전 경쟁사 코어), 우리금융캐피탈·신한캐피탈, 캐나다·푸에르토리코·브라질 로컬 코어, 사우디 ALJ·Al Rajhi·SNB 코어는 1차 출처 미확보. 진입 의사결정 전 추가 실사 권고.
- **미래·마케팅 언어 주의**: 벤더 PR의 “100% implementation success rate”·“unrivalled”·“gold standard” 등은 마케팅 표현으로 사실로 단정하지 않음. ANZ “Alfa Start”·Salesforce Automotive Cloud 등 일부 기능은 출시·채택 발표 단계로, 실제 경쟁사 운영 규모는 별도 검증 필요.