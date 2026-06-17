"""
catalog_seed.py — 카탈로그 마스터 데이터 (코드 상수)

02_데이터카테고리정의서.md의 항목들에 catalog_item_id를 부여한 정식 카탈로그.
seed.py가 이 모듈을 import해 MongoDB에 적재하고, loaders.py가 JSON 폴백 소스로 사용한다.

설계 원칙:
  - similarity_type: CONTINUOUS(연속) / CATEGORICAL(범주) / BINARY(이진) / REFERENCE(참고)
  - data_type: NUMBER / PERCENT / TEXT / CODE / DATE / MULTI / RANGE
  - is_killswitch=True인 항목은 killswitch_rule 필수 (operator/threshold/field)
  - REFERENCE 항목은 점수에 미반영 (보고서 정보용)
"""
from __future__ import annotations


# ── 카테고리 마스터 (4개) ──────────────────────────────────────────────────────

CATALOG_CATEGORIES: list[dict] = [
    {
        "category_id": "MARKET",
        "name": "시장",
        "name_en": "Market",
        "default_weight": 0.25,
        "is_gate": False,
        "gate_threshold": None,
    },
    {
        "category_id": "REGULATORY",
        "name": "규제",
        "name_en": "Regulatory",
        "default_weight": 0.25,
        "is_gate": False,
        "gate_threshold": None,
    },
    {
        "category_id": "FINANCIAL",
        "name": "환경/금융",
        "name_en": "Financial Landscape",
        "default_weight": 0.20,
        "is_gate": False,
        "gate_threshold": None,
    },
    {
        "category_id": "SYSTEM",
        "name": "시스템",
        "name_en": "Systems & Competitors",
        "default_weight": 0.30,
        "is_gate": True,
        "gate_threshold": 50.0,
    },
]


def _item(
    cid: str,
    category: str,
    sub: str,
    name: str,
    name_en: str,
    sim_type: str,
    data_type: str,
    weight: float = 1.0,
    is_killswitch: bool = False,
    killswitch_rule: dict | None = None,
) -> dict:
    return {
        "catalog_item_id": cid,
        "category_id": category,
        "sub_category": sub,
        "name": name,
        "name_en": name_en,
        "similarity_type": sim_type,
        "data_type": data_type,
        "default_item_weight": weight,
        "is_killswitch": is_killswitch,
        "killswitch_rule": killswitch_rule,
    }


# ── 카탈로그 항목 (74개) ───────────────────────────────────────────────────────

CATALOG_ITEMS: list[dict] = [
    # ── MARKET: 1-1 시장 일반 ──────────────────────────────────────────────────
    _item("MKT_001", "MARKET", "1-1", "금융 침투율(신차)", "Finance penetration (new)", "CONTINUOUS", "PERCENT", 1.5),
    _item("MKT_002", "MARKET", "1-1", "금융 침투율(중고차)", "Finance penetration (used)", "CONTINUOUS", "PERCENT", 1.2),
    _item("MKT_003", "MARKET", "1-1", "오토금융 시장규모", "Auto finance market size", "CONTINUOUS", "NUMBER"),
    _item("MKT_004", "MARKET", "1-1", "자동차 판매대수(연간)", "Annual vehicle sales", "CONTINUOUS", "NUMBER"),
    _item("MKT_005", "MARKET", "1-1", "신차/중고차 비율", "New/used ratio", "CONTINUOUS", "PERCENT"),
    _item("MKT_006", "MARKET", "1-1", "평균 차량가격", "Average vehicle price", "CONTINUOUS", "NUMBER"),
    _item("MKT_007", "MARKET", "1-1", "구매 패턴(현금:할부:리스)", "Purchase pattern", "CONTINUOUS", "PERCENT"),
    _item("MKT_008", "MARKET", "1-1", "고객 세그먼트(개인:법인 비율)", "Customer segment ratio", "CONTINUOUS", "PERCENT"),
    _item("MKT_009", "MARKET", "1-1", "평균 구매주기", "Average purchase cycle", "CONTINUOUS", "NUMBER"),
    _item("MKT_010", "MARKET", "1-1", "브랜드 Top10", "Top10 brands", "CATEGORICAL", "MULTI"),
    _item("MKT_011", "MARKET", "1-1", "차종 Top10", "Top10 models", "CATEGORICAL", "MULTI"),
    _item("MKT_012", "MARKET", "1-1", "OEM 순위", "OEM ranking", "CATEGORICAL", "MULTI"),
    _item("MKT_013", "MARKET", "1-1", "오토금융 성장률(CAGR)", "Auto finance CAGR", "REFERENCE", "PERCENT"),
    _item("MKT_014", "MARKET", "1-1", "구매 프로세스", "Purchase process", "REFERENCE", "TEXT"),
    _item("MKT_015", "MARKET", "1-1", "고객 세그먼트(기타 특성)", "Customer segment (other)", "REFERENCE", "MULTI"),
    # ── MARKET: 1-2 딜러 채널 구조 ─────────────────────────────────────────────
    _item("MKT_016", "MARKET", "1-2", "신차 채널 비중", "New car channel mix", "CONTINUOUS", "PERCENT"),
    _item("MKT_017", "MARKET", "1-2", "중고차 채널 비중", "Used car channel mix", "CONTINUOUS", "PERCENT"),
    _item("MKT_018", "MARKET", "1-2", "딜러 집중도", "Dealer concentration", "CONTINUOUS", "PERCENT"),
    _item("MKT_019", "MARKET", "1-2", "딜러 금융취급 관행(F&I)", "Dealer F&I practice", "CATEGORICAL", "CODE"),
    _item("MKT_020", "MARKET", "1-2", "딜러 유형 구조", "Dealer type structure", "CATEGORICAL", "CODE"),
    _item("MKT_021", "MARKET", "1-2", "멀티브랜드 여부", "Multi-brand", "CATEGORICAL", "CODE"),
    _item("MKT_022", "MARKET", "1-2", "디지털 딜러 성숙도", "Digital dealer maturity", "CATEGORICAL", "CODE"),
    _item("MKT_023", "MARKET", "1-2", "딜러-금융사 정산 구조", "Dealer-financier settlement", "REFERENCE", "TEXT"),

    # ── REGULATORY: 킬스위치 5개 (선두 배치) ───────────────────────────────────
    _item("REG_001", "REGULATORY", "2-1", "외국인 지분 한도", "Foreign ownership limit", "BINARY", "PERCENT",
          weight=1.0, is_killswitch=True,
          killswitch_rule={"operator": "LT", "threshold": 100, "field": "value_normalized",
                           "block_message": "외국인 100% 지분 불가"}),
    _item("REG_002", "REGULATORY", "2-2", "외환 송금 규제", "FX remittance restriction", "BINARY", "CODE",
          weight=1.0, is_killswitch=True,
          killswitch_rule={"operator": "EQ", "threshold": "RESTRICTED", "field": "value_normalized",
                           "block_message": "외환 송금 제한으로 자금회수 불가"}),
    _item("REG_003", "REGULATORY", "2-2", "배당 송금 제한", "Dividend remittance restriction", "BINARY", "CODE",
          weight=1.0, is_killswitch=True,
          killswitch_rule={"operator": "EQ", "threshold": "RESTRICTED", "field": "value_normalized",
                           "block_message": "배당 송금 제한으로 본사 회수 불가"}),
    _item("REG_004", "REGULATORY", "2-3", "데이터 현지화 의무", "Data localization", "BINARY", "CODE",
          weight=1.0, is_killswitch=True,
          killswitch_rule={"operator": "EQ", "threshold": "MANDATORY", "field": "value_normalized",
                           "block_message": "데이터 현지화 의무로 시스템 구축비 급증"}),
    _item("REG_005", "REGULATORY", "2-2", "금리 상한(우수라)", "Interest rate cap", "BINARY", "PERCENT",
          weight=1.0, is_killswitch=True,
          killswitch_rule={"operator": "LTE", "threshold": 15, "field": "value_normalized",
                           "block_message": "금리 상한이 수익성 임계치 이하"}),
    # ── REGULATORY: 2-1 인허가 ─────────────────────────────────────────────────
    _item("REG_006", "REGULATORY", "2-1", "라이선스 종류", "License type", "CATEGORICAL", "TEXT"),
    _item("REG_007", "REGULATORY", "2-1", "최저자본금", "Minimum capital", "CONTINUOUS", "NUMBER", 1.3),
    _item("REG_008", "REGULATORY", "2-1", "인허가 처리기간", "License processing period", "CONTINUOUS", "NUMBER"),
    _item("REG_009", "REGULATORY", "2-1", "현지 법인형태 요건", "Local entity requirement", "CATEGORICAL", "CODE"),
    _item("REG_010", "REGULATORY", "2-1", "소관 규제기관", "Regulatory authority", "REFERENCE", "TEXT"),
    # ── REGULATORY: 2-2 정책/세금 ──────────────────────────────────────────────
    _item("REG_011", "REGULATORY", "2-2", "법인세율", "Corporate tax rate", "CONTINUOUS", "PERCENT"),
    _item("REG_012", "REGULATORY", "2-2", "이자소득 원천징수", "Interest withholding tax", "CONTINUOUS", "PERCENT"),
    _item("REG_013", "REGULATORY", "2-2", "배당 송금 원천징수", "Dividend withholding tax", "CONTINUOUS", "PERCENT"),
    # ── REGULATORY: 2-3 정보보호 ───────────────────────────────────────────────
    _item("REG_014", "REGULATORY", "2-3", "개인정보보호법", "Data protection law", "CATEGORICAL", "TEXT"),
    _item("REG_015", "REGULATORY", "2-3", "국외이전 제한", "Cross-border transfer limit", "CATEGORICAL", "TEXT"),
    # ── REGULATORY: 2-4 리스크/건전성 ──────────────────────────────────────────
    _item("REG_016", "REGULATORY", "2-4", "충당금 적립 기준", "Provisioning standard", "CATEGORICAL", "TEXT"),
    _item("REG_017", "REGULATORY", "2-4", "연체 분류 기준", "Delinquency classification", "CONTINUOUS", "NUMBER"),
    _item("REG_018", "REGULATORY", "2-4", "신용정보 조회(CB) 인프라", "Credit bureau infra", "CATEGORICAL", "TEXT"),
    # ── REGULATORY: 2-5 채권추심/회수 ──────────────────────────────────────────
    _item("REG_019", "REGULATORY", "2-5", "추심 규제", "Collection regulation", "CATEGORICAL", "TEXT"),
    _item("REG_020", "REGULATORY", "2-5", "차량회수(repossession) 절차", "Repossession process", "CATEGORICAL", "TEXT"),
    _item("REG_021", "REGULATORY", "2-5", "법적 회수 소요기간", "Legal recovery period", "CONTINUOUS", "NUMBER"),
    # ── REGULATORY: 2-6 의무보험 ───────────────────────────────────────────────
    _item("REG_022", "REGULATORY", "2-6", "자동차 의무보험", "Mandatory auto insurance", "CATEGORICAL", "CODE"),
    _item("REG_023", "REGULATORY", "2-6", "신용생명보험 가능 여부", "Credit life insurance", "CATEGORICAL", "CODE"),
    _item("REG_024", "REGULATORY", "2-6", "보험 끼워팔기 규제", "Insurance bundling regulation", "CATEGORICAL", "TEXT"),

    # ── FINANCIAL: 3 환경/금융 ─────────────────────────────────────────────────
    _item("FIN_001", "FINANCIAL", "3", "평균 금리", "Average interest rate", "CONTINUOUS", "PERCENT", 1.5),
    _item("FIN_002", "FINANCIAL", "3", "캡티브 강도", "Captive intensity", "CONTINUOUS", "PERCENT", 1.3),
    _item("FIN_003", "FINANCIAL", "3", "평균 대출기간", "Average loan term", "CONTINUOUS", "NUMBER"),
    _item("FIN_004", "FINANCIAL", "3", "평균 LTV(선수금)", "Average LTV", "CONTINUOUS", "PERCENT", 1.3),
    _item("FIN_005", "FINANCIAL", "3", "캡티브/논캡티브 구분", "Captive/non-captive", "CATEGORICAL", "CODE"),
    _item("FIN_006", "FINANCIAL", "3", "금융사 순위", "Financier ranking", "CATEGORICAL", "MULTI"),
    _item("FIN_007", "FINANCIAL", "3", "상품판매 현황", "Product sales status", "REFERENCE", "TEXT"),
    _item("FIN_008", "FINANCIAL", "3", "펀딩 구조", "Funding structure", "REFERENCE", "TEXT"),
    _item("FIN_009", "FINANCIAL", "3", "해당국 특징", "Country characteristics", "REFERENCE", "TEXT"),

    # ── SYSTEM: 4-1 시스템 환경 ────────────────────────────────────────────────
    _item("SYS_001", "SYSTEM", "4-1", "주요 솔루션사", "Major solution vendors", "CATEGORICAL", "MULTI"),
    _item("SYS_002", "SYSTEM", "4-1", "솔루션 유형", "Solution type", "CATEGORICAL", "CODE"),
    _item("SYS_003", "SYSTEM", "4-1", "코어시스템 벤더 락인", "Core system vendor lock-in", "CATEGORICAL", "CODE"),
    _item("SYS_004", "SYSTEM", "4-1", "디지털 채널 성숙도", "Digital channel maturity", "CATEGORICAL", "CODE"),
    _item("SYS_005", "SYSTEM", "4-1", "결제·정산 인프라", "Payment/settlement infra", "CATEGORICAL", "TEXT"),
    # ── SYSTEM: 4-2 경쟁사 (전부 REFERENCE) ────────────────────────────────────
    _item("SYS_006", "SYSTEM", "4-2", "경쟁사 리스트", "Competitor list", "REFERENCE", "MULTI"),
    _item("SYS_007", "SYSTEM", "4-2", "경쟁사 금리 현황", "Competitor rates", "REFERENCE", "RANGE"),
    _item("SYS_008", "SYSTEM", "4-2", "경쟁사 시장 점유율", "Competitor market share", "REFERENCE", "PERCENT"),
    _item("SYS_009", "SYSTEM", "4-2", "경쟁사 진출 형태", "Competitor entry mode", "REFERENCE", "CODE"),
    _item("SYS_010", "SYSTEM", "4-2", "경쟁사 사용 시스템", "Competitor systems", "REFERENCE", "TEXT"),
    _item("SYS_011", "SYSTEM", "4-2", "경쟁사 업력", "Competitor tenure", "REFERENCE", "NUMBER"),
    _item("SYS_012", "SYSTEM", "4-2", "경쟁사 딜러망 규모", "Competitor dealer network", "REFERENCE", "NUMBER"),
    _item("SYS_013", "SYSTEM", "4-2", "경쟁사 직원수", "Competitor headcount", "REFERENCE", "NUMBER"),
]


# ── 기본 룰셋 ─────────────────────────────────────────────────────────────────

DEFAULT_RULESET: dict = {
    "_id": "default",
    "id": "default",
    "ruleset_id": "default",
    "name": "기본 룰셋 v1",
    "version": 1,
    "is_default": True,
    "locked": False,
    "weights": {
        "market": 0.25,
        "regulation": 0.25,
        "environment": 0.20,
        "system": 0.30,
    },
    "thresholds": {
        "entry": 60.0,
        "system_gate": 50.0,
    },
    "killswitch_enabled": True,
}


def category_of(catalog_item_id: str) -> str | None:
    """catalog_item_id → category_id 역참조."""
    for it in CATALOG_ITEMS:
        if it["catalog_item_id"] == catalog_item_id:
            return it["category_id"]
    return None
