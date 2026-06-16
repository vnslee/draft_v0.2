# 캐피탈 진출 라이선스 조사 프로세스 (재사용 가이드)

> 다른 국가에서도 **동일한 방식**으로 캐피탈(여신전문금융) 진출 라이선스 정보를 조사하기 위한 표준 프로세스. 본 문서대로 따르면 [`capital_license_KR_US_IN_DE_ES_2025.md`](capital_license_KR_US_IN_DE_ES_2025.md) / [`mockup/regulations/capital_license.json`](../mockup/regulations/capital_license.json)와 동일한 품질·형식의 결과를 산출할 수 있다.

---

## 0. 핵심 원칙 (반드시 준수)

1. **1차 자료만** — 검색·인용 **모두** 공식 기관 도메인만 사용. 로펌 블로그·컨설팅 요약·위키피디아는 보조로도 배제.
2. **지어내기 금지** — 확인 못 한 항목은 `null` + `status: "공식 자료에서 확인 불가"`. 누락 = 미확보로 명시.
3. **출처·연도 명기** — 모든 사실에 발급기관·근거법령·출처 URL·기준연도를 단다.
4. **사업범위 먼저 고정** — "캐피탈"은 모호하므로 범위를 먼저 정의: 여신·대출업 + 리스·할부금융 + 팩토링·기업금융 (예금수취 없는 비은행). 은행업·지급결제·전자화폐는 제외.

---

## 1. 조사할 5개 항목 (국가 공통 스키마)

| 항목 | 키 | 내용 |
|---|---|---|
| 라이선스 명칭 | `license` | 인가/등록의 정확한 명칭 (영문 + 현지어) |
| 발급·감독 기관 | `authority` | 인가 주체 + 감독기관 (중앙은행/금융감독청) |
| 근거 법령 | `legal_basis` | 정확한 법령명 + 조항 번호 |
| 자본금 요건 | `capital_requirement` | 최소 자본금/순자산/NOF (업종별로 다르면 분리) |
| 발급 절차 | `procedure` | 신청 경로·제출서류·소요기간 |

각 필드는 `{value, year, estimated, source, doc_ref?, quote?, note?}` 객체로 기록 (기존 mockup JSON 스키마 준수).

---

## 2. 공식 출처 도메인 맵 (국가별 진입점)

조사할 국가의 감독기관을 먼저 식별하고 `allowed_domains`로 검색을 제한한다.

| 국가 | 감독기관 | 공식 도메인 | 라이선스 키워드 |
|---|---|---|---|
| 한국 | 금융위·금감원 / 법제처 | `fsc.go.kr`, `fss.or.kr`, `law.go.kr` | 여신전문금융업, 시설대여, 할부금융 |
| 미국 | 주 감독청 + CFPB | `dfpi.ca.gov`(주별 상이), `consumerfinance.gov`, `nmlsconsumeraccess.org` | finance lender license, NBFC |
| 인도 | RBI | `rbi.org.in`, `rbidocs.rbi.org.in` | NBFC, net owned fund, §45-IA |
| 독일 | BaFin + Bundesbank | `bafin.de` | Erlaubnis, KWG, Finanzierungsleasing, Factoring |
| 스페인 | Banco de España / BOE | `bde.es`, `boe.es` | establecimiento financiero de crédito (EFC) |
| **(EU 공통)** | EUR-Lex | `eur-lex.europa.eu` | CRR, CRD, 면허 passporting |

> **신규 국가 진입점 찾기**: ① 중앙은행/금융감독청 공식 사이트 → ② "비은행 여신/lending/leasing/factoring license" 검색 → ③ 근거 법령 DB(공식 관보)에서 조항 확인.

---

## 3. 단계별 실행

### 3-1. 사업범위·항목 확정
- 사용자에게 사업범위(여신/리스/팩토링)와 결과물 형식을 먼저 확인.
- 5개 조사항목(§1)을 국가별로 동일하게 적용.

### 3-2. 공식 도메인 한정 검색 (병렬)
- `WebSearch`에 `allowed_domains: [공식도메인]`을 걸어 국가별 동시 검색.
- 한 번에 5개국 병렬 실행 → 라이선스 명칭·근거법령·기관·1차 출처 URL 확보.

```
WebSearch(query="<라이선스 키워드>", allowed_domains=["<감독기관 도메인>"])
```

### 3-3. 1차 출처 직접 fetch (정확한 수치·조항·인용)
- 검색으로 찾은 공식 페이지를 `WebFetch`로 열어 **자본금 금액·조항 번호·절차·원문 인용**을 추출.
- 리다이렉트(302/301)는 안내된 redirect URL로 재요청.

### 3-4. 접근 차단 우회 (봇 차단·JS 렌더링)
일부 공식 사이트는 자동 fetch를 막는다. 처리 순서:
1. **WebFetch 실패(403/404/CAPTCHA)** → `curl -A "<브라우저 UA>"`로 재시도 (예: 법령 HTML).
2. **여전히 차단**(RBI = Akamai 봇월, CAPTCHA) → 공식 도메인 한정 **검색결과 스니펫**(검색엔진이 인덱싱한 공식 페이지 내용)으로 교차확인하고, `note`에 "원문 직접대조 미완"을 남긴다.
3. **JS 렌더링**(law.go.kr 조문 본문) → curl로 받은 HTML을 `python3`로 태그 제거·키워드 추출. 그래도 조문 본문이 비면 미확보로 표기.

> ⚠️ 우회는 **공식 도메인 한정**으로만. 2차 자료로 빠지지 않는다. 차단으로 못 얻은 값은 반드시 `미확보`로 남긴다(추정 금지).

### 3-5. 산출물 3종 생성
1. **보고서** `reports/capital_license_<국가코드들>_<연도>.md` — 핵심요약표 + 국가별 섹션(라이선스/기관/법령/자본금/절차) + 원문 인용 + open_gaps.
2. **시드 JSON** `mockup/regulations/capital_license.json` — 기존 `auto_finance_regulation.json` 스키마(`meta` + `licenses[]`, `{value,year,estimated,source,...}`) 준수. 새 국가는 `licenses[]`에 객체 추가.
3. **프로세스 문서**(본 문서) 갱신 — 새 국가 도메인 맵 추가.

---

## 4. 국가별 라이선스 구조 빠른 참조 (조사된 5개국)

조사 시 "이 나라는 어떤 유형인가"를 빠르게 가늠하는 데 사용.

- **단일 인가형** (독일·스페인): 중앙 감독기관이 단일 라이선스 발급. 자본금 €5M 수준(EU CRR 영향). 리스·팩토링은 경감 가능(독일 §2 Abs.7a KWG).
- **등록형** (한국·인도): 회사 설립 후 감독기관 등록. 업종별 자본금/NOF 차등. 한국=금융위 등록, 인도=RBI NBFC 등록.
- **주별 분산형** (미국): 연방 단일 라이선스 없음 → 진출 주마다 lender license + 연방 CFPB 감독. 자본요건이 주마다 상이.

> 신규 국가 조사 시 위 3유형 중 어디에 가까운지 먼저 판별하면 어떤 기관·법령을 찾을지 빠르게 좁혀진다.

---

## 5. 체크리스트 (국가 1개 완료 기준)

- [ ] 라이선스 정확 명칭(영문+현지어) 확보
- [ ] 발급기관 + 감독기관 구분 확보
- [ ] 근거 법령 + 조항 번호 확보 (공식 법령 DB)
- [ ] 자본금/NOF/순자산 요건 (업종별 분리) — 공식 출처 인용
- [ ] 발급 절차·소요기간 (확보 못 하면 미확보 명시)
- [ ] 모든 사실에 출처 URL + 기준연도
- [ ] 차단/미확보 항목을 `open_gaps`에 기록
- [ ] JSON `licenses[]`에 객체 추가 + 보고서 섹션 추가
