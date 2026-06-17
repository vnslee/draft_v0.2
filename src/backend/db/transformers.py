"""
transformers.py — data/ JSON → 정식 스키마(research_items / entry_records) 변환기

각 JSON 파일의 1개국 레코드를 받아 catalog_item_id 단위 research_item 문서 리스트로 변환한다.
seed.py(MongoDB 적재)와 loaders.py(JSON 폴백) 양쪽에서 사용한다.

핵심 규칙:
  - value=null 또는 미수록 → is_missing=True (null ≠ 0)
  - source_tier: source_verifier 재사용 + estimated 플래그
  - 킬스위치 5개 항목은 JSON에 실데이터 거의 없음 → KILLSWITCH_MOCKUP에서 보강
"""
from __future__ import annotations

import re
from typing import Any

from core.normalizer import to_usd
from core.source_verifier import SourceTier, verify_source
from db.catalog_seed import CATALOG_ITEMS


# ── 국가명 ↔ ISO 코드 ─────────────────────────────────────────────────────────

COUNTRY_ISO_MAP: dict[str, str] = {
    "한국": "KR",
    "호주": "AU",
    "중국": "CN",
    "미국": "US",
    "캐나다": "CA",
    "독일": "DE",
    "러시아": "RU",
    "인도": "IN",
    "인도네시아": "ID",
    "멕시코": "MX",
    "영국": "GB",
    "폴란드": "PL",
    "스페인": "ES",
}

ISO_TO_NAME: dict[str, str] = {v: k for k, v in COUNTRY_ISO_MAP.items()}


def to_iso(country: str) -> str:
    """국가명(한국) 또는 ISO 코드(KR) → ISO 코드. 미매핑이면 입력 그대로."""
    if country in COUNTRY_ISO_MAP:
        return COUNTRY_ISO_MAP[country]
    if country.upper() in ISO_TO_NAME:
        return country.upper()
    return country


def to_name(country: str) -> str:
    """ISO 코드(KR) 또는 국가명 → 한국어 국가명. 미매핑이면 입력 그대로."""
    if country.upper() in ISO_TO_NAME:
        return ISO_TO_NAME[country.upper()]
    if country in COUNTRY_ISO_MAP:
        return country
    return country


# ── 카탈로그 인덱스 ───────────────────────────────────────────────────────────

_CATALOG_BY_ID: dict[str, dict] = {it["catalog_item_id"]: it for it in CATALOG_ITEMS}


def _items_in_category(category_id: str) -> list[dict]:
    return [it for it in CATALOG_ITEMS if it["category_id"] == category_id]


# ── attribute.key → catalog_item_id 매핑 ──────────────────────────────────────
# auto_finance_market.json의 dimensions.*.attributes[].key 기반

MARKET_ATTR_MAP: dict[str, str] = {
    "fin_penetration_new_owned": "MKT_001",
    "fin_penetration_owned_total": "MKT_001",   # 총계 — 신차 침투율 근사
    "fin_penetration_used_owned": "MKT_002",
    "newreg_private_share": "MKT_008",          # 개인 비율
    "newreg_commercial_share": "MKT_008",       # 법인 비율(역수)
    "consumer_pref_installment": "MKT_007",     # 할부 선호
    "consumer_pref_leasing": "MKT_007",
    "consumer_pref_pcp_balloon": "MKT_007",
    "scf_customer_assets_eur": "MKT_003",       # 시장규모 근사
    "lease_penetration_new_reg": "FIN_002",     # 리스 침투 → 캡티브 강도
    "captive_new_retail_contracts": "FIN_002",
    "captive_new_leasing_contracts": "FIN_002",
    "vwfs_country_penetration": "FIN_002",
    "vw_group_penetration": "SYS_008",          # 경쟁사 점유율(REFERENCE)
    "vwfs_new_contracts": "SYS_006",            # 경쟁사 정보(REFERENCE)
}


# ── 킬스위치 목업 (정의서 기반 추정) ──────────────────────────────────────────
# JSON에 실데이터 없는 킬스위치 5개를 국가별로 보강. 전부 추정값(TIER3).
# value_normalized 인코딩: BINARY는 통과조건 충족 여부를 raw 값으로 저장,
#   - REG_001: 외국인 지분 한도(%) — 100이면 통과
#   - REG_002/003: "OK" 또는 "RESTRICTED"
#   - REG_004: "NONE" 또는 "MANDATORY"
#   - REG_005: 금리 상한(%) — None이면 상한 없음(통과)

KILLSWITCH_MOCKUP: dict[str, dict[str, Any]] = {
    "KR": {"REG_001": 100, "REG_002": "OK", "REG_003": "OK", "REG_004": "NONE", "REG_005": 20},
    "US": {"REG_001": 100, "REG_002": "OK", "REG_003": "OK", "REG_004": "NONE", "REG_005": 36},
    "DE": {"REG_001": 100, "REG_002": "OK", "REG_003": "OK", "REG_004": "MANDATORY", "REG_005": None},
    "ES": {"REG_001": 100, "REG_002": "OK", "REG_003": "OK", "REG_004": "MANDATORY", "REG_005": None},
    "IN": {"REG_001": 100, "REG_002": "RESTRICTED", "REG_003": "OK", "REG_004": "MANDATORY", "REG_005": None},
    "CN": {"REG_001": 51, "REG_002": "RESTRICTED", "REG_003": "RESTRICTED", "REG_004": "MANDATORY", "REG_005": 24},
    "RU": {"REG_001": 100, "REG_002": "RESTRICTED", "REG_003": "RESTRICTED", "REG_004": "MANDATORY", "REG_005": None},
    "AU": {"REG_001": 100, "REG_002": "OK", "REG_003": "OK", "REG_004": "NONE", "REG_005": None},
    "CA": {"REG_001": 100, "REG_002": "OK", "REG_003": "OK", "REG_004": "NONE", "REG_005": 60},
    "MX": {"REG_001": 100, "REG_002": "OK", "REG_003": "OK", "REG_004": "NONE", "REG_005": None},
    "ID": {"REG_001": 85, "REG_002": "OK", "REG_003": "OK", "REG_004": "MANDATORY", "REG_005": None},
    "GB": {"REG_001": 100, "REG_002": "OK", "REG_003": "OK", "REG_004": "NONE", "REG_005": None},
    "PL": {"REG_001": 100, "REG_002": "OK", "REG_003": "OK", "REG_004": "MANDATORY", "REG_005": None},
}


# ── source_tier / confidence_grade 결정 ───────────────────────────────────────

def _resolve_source_tier(source_url: str | None, estimated: bool, country_iso: str | None = None) -> str:
    if not source_url or source_url in ("MOCKUP", "추정"):
        return SourceTier.TIER3.value if estimated else SourceTier.BLOCKED.value
    if source_url.startswith("http"):
        tier = verify_source(source_url, country_iso)
        return tier.value
    # URL이 아닌 문서명 등 → estimated 여부로 판정
    return SourceTier.TIER3.value if estimated else SourceTier.TIER2.value


def _resolve_confidence_grade(source_tier: str) -> str:
    return {
        "TIER1": "OFFICIAL",
        "TIER2": "SEMI_OFFICIAL",
        "TIER3": "ESTIMATED",
        "BLOCKED": "ESTIMATED",
    }.get(source_tier, "ESTIMATED")


# ── value 정규화 ──────────────────────────────────────────────────────────────

def _normalize_value(raw: Any, data_type: str) -> Any:
    """data_type에 맞춰 value_normalized 산출. 실패 시 None."""
    if raw is None:
        return None
    if data_type == "PERCENT":
        num = _coerce_number(raw)
        if num is None:
            return None
        return num / 100.0 if num > 1.0 else num
    if data_type == "NUMBER":
        return _coerce_number(raw)
    # TEXT / CODE / MULTI / RANGE / DATE → 원본 보존
    return raw


def _coerce_number(raw: Any) -> float | None:
    if isinstance(raw, (int, float)):
        return float(raw)
    if isinstance(raw, str):
        m = re.search(r"-?\d+(?:[.,]\d+)?", raw.replace(",", ""))
        if m:
            try:
                return float(m.group())
            except ValueError:
                return None
    return None


# ── research_item 생성 헬퍼 ───────────────────────────────────────────────────

_item_counter = {"n": 0}


def _next_item_id(snapshot_id: str, catalog_item_id: str) -> str:
    _item_counter["n"] += 1
    return f"{snapshot_id}_{catalog_item_id}_{_item_counter['n']}"


def make_research_item(
    snapshot_id: str,
    catalog_item_id: str,
    value_raw: Any = None,
    value_normalized: Any = None,
    source_name: str | None = None,
    source_url: str | None = None,
    estimated: bool = True,
    evidence: str | None = None,
    condition: str | None = None,
    country_iso: str | None = None,
) -> dict:
    is_missing = value_normalized is None and value_raw is None
    source_tier = _resolve_source_tier(source_url, estimated, country_iso)
    confidence_grade = _resolve_confidence_grade(source_tier)
    return {
        "item_id": _next_item_id(snapshot_id, catalog_item_id),
        "snapshot_id": snapshot_id,
        "catalog_item_id": catalog_item_id,
        "value_raw": str(value_raw) if value_raw is not None else None,
        "value_normalized": value_normalized,
        "is_missing": is_missing,
        "source_name": source_name,
        "source_url": source_url,
        "source_tier": source_tier,
        "is_official": source_tier == "TIER1",
        "official_gap_flag": source_tier in ("TIER2", "TIER3", "BLOCKED"),
        "confidence_grade": confidence_grade,
        "evidence": evidence,
        "condition": condition,
    }


def _missing_item(snapshot_id: str, catalog_item_id: str) -> dict:
    return {
        "item_id": _next_item_id(snapshot_id, catalog_item_id),
        "snapshot_id": snapshot_id,
        "catalog_item_id": catalog_item_id,
        "value_raw": None,
        "value_normalized": None,
        "is_missing": True,
        "source_name": None,
        "source_url": None,
        "source_tier": "BLOCKED",
        "is_official": False,
        "official_gap_flag": True,
        "confidence_grade": "ESTIMATED",
        "evidence": None,
        "condition": None,
    }


def _missing_items_for_category(category_id: str, snapshot_id: str) -> list[dict]:
    return [_missing_item(snapshot_id, it["catalog_item_id"]) for it in _items_in_category(category_id)]


def _merge_fill_missing(items: list[dict], category_id: str, snapshot_id: str) -> list[dict]:
    """변환된 items에 없는 카테고리 항목을 is_missing으로 채워 항목 수를 고정."""
    present = {i["catalog_item_id"] for i in items}
    for it in _items_in_category(category_id):
        if it["catalog_item_id"] not in present:
            items.append(_missing_item(snapshot_id, it["catalog_item_id"]))
    return items


# ── 킬스위치 보강 ─────────────────────────────────────────────────────────────

def _apply_killswitch_mockup(items: list[dict], country_iso: str, snapshot_id: str) -> list[dict]:
    """REG_001~005 항목을 KILLSWITCH_MOCKUP 값으로 교체(있으면). 실데이터 우선."""
    mockup = KILLSWITCH_MOCKUP.get(country_iso, {})
    by_id = {i["catalog_item_id"]: i for i in items}
    for cid, val in mockup.items():
        existing = by_id.get(cid)
        # 실데이터가 이미 있고 미확보가 아니면 보존
        if existing and not existing.get("is_missing"):
            continue
        ci = _CATALOG_BY_ID[cid]
        # 킬스위치 BINARY 항목은 정규화하지 않고 원본 스케일 유지
        # (killswitch_rule.threshold가 원본 스케일 — 예: 외국인지분 100%, 금리상한 15%)
        normalized = val
        new_item = make_research_item(
            snapshot_id=snapshot_id,
            catalog_item_id=cid,
            value_raw=val,
            value_normalized=normalized,
            source_name="정의서 기반 추정",
            source_url="추정",
            estimated=True,
            evidence="정의서 기반 추정값 (실측 교체 필요)",
            country_iso=country_iso,
        )
        by_id[cid] = new_item
    return list(by_id.values())


# ── 메인 변환 함수들 ──────────────────────────────────────────────────────────

def transform_market_data(raw: dict, snapshot_id: str) -> list[dict]:
    """auto_finance_market.json 1개국 → MARKET + 일부 FINANCIAL/SYSTEM research_items"""
    items: list[dict] = []
    country_iso = raw.get("country_code") or to_iso(raw.get("country", ""))
    seen: set[str] = set()

    dimensions = raw.get("dimensions", {})
    for dim_name, dim in dimensions.items():
        for attr in dim.get("attributes", []):
            key = attr.get("key")
            cid = MARKET_ATTR_MAP.get(key)
            if not cid or cid in seen:
                continue
            ci = _CATALOG_BY_ID.get(cid)
            if not ci:
                continue
            val_obj = attr.get("value", {})
            raw_val = val_obj.get("value") if isinstance(val_obj, dict) else val_obj
            estimated = val_obj.get("estimated", True) if isinstance(val_obj, dict) else True
            source = val_obj.get("source") if isinstance(val_obj, dict) else None
            normalized = _normalize_value(raw_val, ci["data_type"])
            items.append(make_research_item(
                snapshot_id=snapshot_id,
                catalog_item_id=cid,
                value_raw=raw_val,
                value_normalized=normalized,
                source_name=source,
                source_url=source,
                estimated=estimated,
                evidence=attr.get("label"),
                country_iso=country_iso,
            ))
            seen.add(cid)

    _merge_fill_missing(items, "MARKET", snapshot_id)
    return items


def transform_segment_data(raw: dict, snapshot_id: str) -> list[dict]:
    """customer_segment.json 1개국 → MKT_007/MKT_008 등 일부 보강"""
    items: list[dict] = []
    country_iso = raw.get("country_code") or to_iso(raw.get("country", ""))

    auto_finance = raw.get("auto_finance", {})
    # 채널 items에서 캡티브/은행 비중 추출 → FIN_005 근거
    channel = auto_finance.get("channel", {})
    channel_items = channel.get("items", []) if isinstance(channel, dict) else []
    if channel_items:
        labels = ", ".join(str(i.get("name")) for i in channel_items if isinstance(i, dict))
        items.append(make_research_item(
            snapshot_id=snapshot_id,
            catalog_item_id="FIN_005",
            value_raw=labels,
            value_normalized=labels,
            source_name=channel.get("basis"),
            estimated=True,
            evidence="고객 세그먼트 채널 구조",
            country_iso=country_iso,
        ))
    return items  # 카테고리 채우기는 호출측에서 통합


def transform_regulation_data(raw: dict, snapshot_id: str) -> list[dict]:
    """auto_finance_regulation.json 1개국 → REGULATORY/FINANCIAL 일부"""
    items: list[dict] = []
    country_iso = raw.get("country_code") or to_iso(raw.get("country", ""))

    # 금리 상한 → FIN_001(평균금리 근사) + REG_005(킬스위치)
    auto_loan = raw.get("products", {}).get("auto_loan", {})
    rate_fee = auto_loan.get("rate_fee_prepay", {})
    rate_node = None
    for k, v in rate_fee.items():
        if "rate_cap" in k and isinstance(v, dict):
            rate_node = v
            break
    if rate_node:
        raw_val = rate_node.get("value")
        num = _coerce_number(raw_val)
        if num is not None:
            items.append(make_research_item(
                snapshot_id=snapshot_id,
                catalog_item_id="FIN_001",
                value_raw=raw_val,
                value_normalized=num / 100.0 if num > 1.0 else num,
                source_name=rate_node.get("source"),
                source_url=rate_node.get("source"),
                estimated=rate_node.get("estimated", True),
                evidence="금리 상한 기반 평균금리 근사",
                country_iso=country_iso,
            ))

    # 개인정보 프레임워크 → REG_014
    framework = raw.get("regulatory_framework", {})
    if isinstance(framework, dict) and framework.get("value"):
        items.append(make_research_item(
            snapshot_id=snapshot_id,
            catalog_item_id="REG_014",
            value_raw=framework.get("value"),
            value_normalized=framework.get("value"),
            source_name=framework.get("source"),
            source_url=framework.get("source"),
            estimated=framework.get("estimated", True),
            evidence="규제 프레임워크",
            country_iso=country_iso,
        ))
    return items


def transform_license_data(raw: dict, snapshot_id: str) -> list[dict]:
    """capital_license.json 1개국 → REG_006(라이선스), REG_007(자본금), REG_008(처리기간)"""
    items: list[dict] = []
    country_iso = raw.get("country_code") or to_iso(raw.get("country", ""))

    # REG_006: 라이선스 종류
    lic = raw.get("license", {})
    if isinstance(lic, dict) and lic.get("value"):
        items.append(make_research_item(
            snapshot_id=snapshot_id,
            catalog_item_id="REG_006",
            value_raw=lic.get("value"),
            value_normalized=lic.get("value"),
            source_name=lic.get("source"),
            source_url=lic.get("source"),
            estimated=lic.get("estimated", True),
            evidence="라이선스 종류",
            country_iso=country_iso,
        ))

    # REG_007: 최저자본금 — capital_requirement 하위 첫 수치 추출
    cap_req = raw.get("capital_requirement", {})
    cap_val, cap_src = _extract_capital(cap_req)
    if cap_val is not None:
        items.append(make_research_item(
            snapshot_id=snapshot_id,
            catalog_item_id="REG_007",
            value_raw=cap_val,
            value_normalized=_coerce_number(cap_val),
            source_name=cap_src,
            source_url=cap_src,
            estimated=True,
            evidence="최저자본금 요건",
            country_iso=country_iso,
        ))

    # REG_008: 인허가 처리기간 — procedure에서 일수 추출
    proc = raw.get("procedure", {})
    if isinstance(proc, dict) and proc.get("value"):
        days = _coerce_number(proc.get("value"))
        items.append(make_research_item(
            snapshot_id=snapshot_id,
            catalog_item_id="REG_008",
            value_raw=proc.get("value"),
            value_normalized=days,
            source_name=proc.get("source"),
            source_url=proc.get("source"),
            estimated=proc.get("estimated", True),
            evidence="인허가 절차",
            country_iso=country_iso,
        ))
    return items


def _extract_capital(cap_req: dict) -> tuple[Any, str | None]:
    """capital_requirement의 국가별 상이한 하위 구조에서 첫 수치값+출처 추출."""
    if not isinstance(cap_req, dict):
        return None, None
    for k, v in cap_req.items():
        if isinstance(v, dict):
            val = v.get("value")
            if val is not None and _coerce_number(val) is not None:
                return val, v.get("source")
    return None, None


def transform_purchase_process(raw: dict, snapshot_id: str) -> list[dict]:
    """purchase_process.json 1개국 → MKT_014(구매프로세스 REFERENCE) 등"""
    items: list[dict] = []
    country_iso = raw.get("country_code") or to_iso(raw.get("country", ""))
    note = raw.get("note")
    if note:
        items.append(make_research_item(
            snapshot_id=snapshot_id,
            catalog_item_id="MKT_014",
            value_raw=note,
            value_normalized=note,
            source_name="purchase_process",
            estimated=True,
            evidence="구매 프로세스 개요",
            country_iso=country_iso,
        ))
    return items


# ── entry_baseline → entry_records ────────────────────────────────────────────

def transform_entry_record(raw: dict) -> dict:
    """entry_baseline.json baselines[] 1건 → entry_records 문서"""
    country_iso = raw.get("country_code") or to_iso(raw.get("country", ""))
    duration = raw.get("duration_months", {})
    cost = raw.get("cost_usd", {})
    months = duration.get("value") if isinstance(duration, dict) else None
    cost_usd = cost.get("value") if isinstance(cost, dict) else None
    return {
        "entry_id": f"entry_{country_iso}",
        "country_id": country_iso,
        "prep_period_days": int(months * 30) if months else None,
        "prep_cost_usd": cost_usd,
        "cost_breakdown": None,   # JSON에 분해 데이터 없음 — 추후 실측
        "system_info": None,
        "scope": raw.get("scope"),
        "note": raw.get("note"),
        "estimated": True,
    }
