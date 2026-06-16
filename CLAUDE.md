# 오토금융 해외진출 진단 콘솔 — 프로젝트 가이드

## 프로젝트 한 줄 요약

오토금융 캐피탈사의 신규 국가 진출 의사결정을 지원하는 AI 에이전트 대시보드.
진출국 실적을 기준점으로 삼아 미진출 국가의 진출 난이도·비용을 유사도 기반으로 추정한다.

---

## 디렉토리 구조

```
/workshop
├── src/
│   ├── frontend/          # React + Vite (포트 5173)
│   ├── backend/           # FastAPI (포트 8000)
│   └── similarity_agent/  # 유사도 엔진 (loaders.py 등)
│
├── data/                  # 목업 JSON (실 DB 교체 전까지 loaders.py가 여기서 읽음)
│   ├── countries/
│   ├── regulations/
│   ├── baseline/
│   ├── purchase_process/
│   ├── customer_segment/
│   └── auto_finance_market/
│
├── docs/
│   ├── design/            # 설계 문서 (01~04, 화면요구사항, 프로토타입컨텍스트)
│   ├── impl/              # 구현 명세 (이 폴더 — 아키텍처/API/DB/에이전트/프론트/배포)
│   ├── research/          # 리서치 자료
│   └── dev/               # 개발 노트 (BUGFIX, README 등)
│
├── requirements/          # 요구사항 문서
├── archive/               # 백업·임시 파일
└── CLAUDE.md              # 이 파일
```

---

## 기술 스택 (확정)

| 영역 | 스택 |
|---|---|
| 프론트엔드 | React 18 + Vite + TypeScript, Zustand(상태관리), TailwindCSS |
| 백엔드 | Python 3.11+, FastAPI, uvicorn |
| 실시간 통신 | WebSocket (분석 진행률 스트리밍) |
| DB | MongoDB Atlas (mongoose 스키마는 `docs/impl/03_db_schema.md` 참조) |
| LLM | Claude API — Haiku 4.5(에이전트 병렬 분석) / Sonnet 4.6(Summary·보고서 생성) |
| Claude SDK | `anthropic` Python SDK, `tool_use` + 멀티턴 |

---

## 핵심 설계 원칙

1. **점수는 규칙, 근거는 LLM** — 유사도 점수는 코드로 결정적 산출. LLM은 근거 문장만 생성.
2. **출처 검증은 코드** — 도메인 화이트리스트를 코드 레벨에서 강제. 프롬프트에 맡기지 않음.
3. **null ≠ 0** — 미확보 데이터는 마스킹. 보고서에 "비교 불가"로 명시. 절대 0점 처리 금지.
4. **룰셋 불변** — 보고서가 참조한 가중치 룰셋은 잠금. 변경 시 새 버전 생성.
5. **loaders.py가 유일한 데이터 접근점** — DB 전환 시 loaders.py 내부만 교체.

---

## 에이전트 구조 (5-Agent)

```
Phase 1 (병렬):  MarketAgent | RegulationAgent | EnvironmentAgent | SystemAgent
Phase 2 (순차):  SummaryAgent (4개 결과 취합 → 최종 판정 + 보고서 데이터)
```

WebSocket `/ws/analysis/{analysis_id}` 로 프론트에 실시간 진행률 스트리밍.

---

## 관련 문서

- **아키텍처**: `docs/impl/01_architecture.md`
- **API 명세**: `docs/impl/02_api_spec.md`
- **DB 스키마**: `docs/impl/03_db_schema.md`
- **에이전트 설계**: `docs/impl/04_agent_design.md`
- **프론트엔드 명세**: `docs/impl/05_frontend_spec.md`
- **배포 가이드**: `docs/impl/06_deployment.md`
- **설계 원문**: `docs/design/01_설계문서.md` ~ `04_화면설계흐름.md`
