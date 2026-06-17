"""
loaders.py — 데이터 접근 계층

MongoDB 연결 시: motor(async) 기반으로 DB에서 읽음
MongoDB 미연결 시: data/ 폴더 JSON 파일에서 읽음 (개발/오프라인 폴백)

함수 시그니처와 반환 타입은 고정 — 절대 변경 금지.
DB 전환 시 이 파일의 본문만 교체한다.
"""
from __future__ import annotations

import json
import os
from functools import lru_cache
from typing import Any

_HERE = os.path.dirname(os.path.abspath(__file__))
_DATA_DIR = os.path.normpath(os.path.join(_HERE, "..", "..", "..", "data"))


# ── JSON 폴백 헬퍼 ────────────────────────────────────────────────────────────

def _read(rel: str) -> Any:
    with open(os.path.join(_DATA_DIR, rel), encoding="utf-8") as f:
        return json.load(f)


@lru_cache(maxsize=None)
def _json_countries() -> dict[str, dict]:
    raw = _read("countries/countries.json")
    return {c["name"]: c for c in raw.get("countries", [])}


@lru_cache(maxsize=None)
def _json_markets() -> dict[str, dict]:
    raw = _read("auto_finance_market/auto_finance_market.json")
    return {m["country"]: m for m in raw.get("markets", [])}


@lru_cache(maxsize=None)
def _json_segments() -> dict[str, dict]:
    raw = _read("customer_segment/customer_segment.json")
    return {s["country"]: s for s in raw.get("segments", [])}


@lru_cache(maxsize=None)
def _json_processes() -> dict[str, dict]:
    raw = _read("purchase_process/purchase_process.json")
    return {p["country"]: p for p in raw.get("processes", [])}


@lru_cache(maxsize=None)
def _json_regulations() -> dict[str, dict]:
    raw = _read("regulations/auto_finance_regulation.json")
    return {r["country"]: r for r in raw.get("regulations", [])}


@lru_cache(maxsize=None)
def _json_licenses() -> dict[str, dict]:
    raw = _read("regulations/capital_license.json")
    return {l["country"]: l for l in raw.get("licenses", [])}


@lru_cache(maxsize=None)
def _json_baseline() -> dict:
    raw = _read("baseline/entry_baseline.json")
    baselines = {b["country"]: b for b in raw.get("baselines", [])}
    return {"baselines": baselines, "multiplier_table": raw.get("multiplier_table", {})}


def _by_id(data: dict[str, dict], country_id: str) -> dict | None:
    """국가명 또는 ISO 코드로 검색."""
    result = data.get(country_id)
    if result is None:
        result = next((v for v in data.values() if v.get("country_code") == country_id), None)
    return result


# ── DB 접근 헬퍼 ──────────────────────────────────────────────────────────────

def _get_db():
    try:
        from db.connection import get_db
        return get_db()
    except Exception:
        return None


# ── 국가 ──────────────────────────────────────────────────────────────────────

async def load_countries_async() -> dict[str, dict]:
    db = _get_db()
    if db is not None:
        docs = await db.countries.find({}, {"_id": 0}).to_list(None)
        if docs:
            return {c["name"]: c for c in docs}
    return _json_countries()


def load_countries() -> dict[str, dict]:
    """동기 인터페이스 — JSON 폴백 전용 (라우터·에이전트 초기화 시 사용)."""
    return _json_countries()


def load_country(country_name: str) -> dict | None:
    return load_countries().get(country_name)


def entered_countries() -> list[str]:
    return [n for n, c in load_countries().items() if c.get("entry_status") == "진출"]


def candidate_countries() -> list[str]:
    return [n for n, c in load_countries().items() if c.get("entry_status") == "진출예정"]


# ── 베이스라인 (JSON 폴백 소스 — load_entry_record/load_multiplier_table가 사용) ──

def load_baseline() -> dict:
    return _json_baseline()


# ── 카탈로그 (정식 스키마) ────────────────────────────────────────────────────

async def load_catalog_categories() -> list[dict]:
    db = _get_db()
    if db is not None:
        docs = await db.catalog_categories.find({}, {"_id": 0}).to_list(None)
        if docs:
            return docs
    from db.catalog_seed import CATALOG_CATEGORIES
    return [dict(c) for c in CATALOG_CATEGORIES]


async def load_catalog_items(category_id: str | None = None) -> list[dict]:
    db = _get_db()
    if db is not None:
        query = {"category_id": category_id} if category_id else {}
        docs = await db.catalog_items.find(query, {"_id": 0}).to_list(None)
        if docs:
            return docs
    from db.catalog_seed import CATALOG_ITEMS
    items = [dict(i) for i in CATALOG_ITEMS]
    if category_id:
        items = [i for i in items if i["category_id"] == category_id]
    return items


async def load_catalog_item(catalog_item_id: str) -> dict | None:
    db = _get_db()
    if db is not None:
        doc = await db.catalog_items.find_one({"catalog_item_id": catalog_item_id}, {"_id": 0})
        if doc:
            return doc
    from db.catalog_seed import CATALOG_ITEMS
    return next((dict(i) for i in CATALOG_ITEMS if i["catalog_item_id"] == catalog_item_id), None)


# ── research_items (정식 스키마, catalog_item_id 단위) ────────────────────────

async def load_research_items(
    country_id: str,
    category_id: str | None = None,
    snapshot_kind: str = "CURRENT",
) -> dict[str, dict]:
    """
    국가의 research_items를 catalog_item_id 키 dict로 반환.
    country_id: ISO 코드(KR) 또는 한국어명(한국) 모두 수용.
    미수록 항목은 is_missing=True 문서로 채워 항목 수 고정.
    """
    from db.transformers import to_iso

    iso = to_iso(country_id)

    db = _get_db()
    if db is not None:
        result = await _db_research_items(db, iso, category_id, snapshot_kind)
        if result:
            return result
    return _json_fallback_research_items(iso, category_id)


async def _db_research_items(db, iso: str, category_id: str | None, snapshot_kind: str) -> dict[str, dict]:
    # 최신 snapshot 조회
    snap = await db.research_snapshots.find_one(
        {"country_id": iso, "data_kind": snapshot_kind},
        sort=[("survey_date", -1)],
    )
    if not snap:
        return {}
    items = await db.research_items.find({"snapshot_id": snap["snapshot_id"]}, {"_id": 0}).to_list(None)
    by_id = {it["catalog_item_id"]: it for it in items}
    if category_id:
        cat_ids = {i["catalog_item_id"] for i in await load_catalog_items(category_id)}
        by_id = {k: v for k, v in by_id.items() if k in cat_ids}
    return by_id


@lru_cache(maxsize=128)
def _json_fallback_research_items(iso: str, category_id: str | None) -> dict[str, dict]:
    """JSON을 transformers로 on-the-fly 변환. (iso, category_id) 캐싱."""
    from db import transformers as T
    from db.catalog_seed import CATALOG_ITEMS

    snapshot_id = f"json_{iso}"
    by_id: dict[str, dict] = {}

    def _absorb(items: list[dict]) -> None:
        for it in items:
            cid = it["catalog_item_id"]
            # 실데이터(미확보 아님)가 기존 미확보를 덮어씀
            existing = by_id.get(cid)
            if existing is None or (existing.get("is_missing") and not it.get("is_missing")):
                by_id[cid] = it

    # 각 JSON 소스 변환
    market = _by_id(_json_markets(), iso)
    if market:
        _absorb(T.transform_market_data(market, snapshot_id))
    seg = _by_id(_json_segments(), iso)
    if seg:
        _absorb(T.transform_segment_data(seg, snapshot_id))
    reg = _by_id(_json_regulations(), iso)
    if reg:
        _absorb(T.transform_regulation_data(reg, snapshot_id))
    lic = _by_id(_json_licenses(), iso)
    if lic:
        _absorb(T.transform_license_data(lic, snapshot_id))
    proc = _by_id(_json_processes(), iso)
    if proc:
        _absorb(T.transform_purchase_process(proc, snapshot_id))

    # 킬스위치 목업 보강 (REGULATORY)
    ks_items = T._apply_killswitch_mockup(
        [by_id[c] for c in ("REG_001", "REG_002", "REG_003", "REG_004", "REG_005") if c in by_id],
        iso, snapshot_id,
    )
    for it in ks_items:
        by_id[it["catalog_item_id"]] = it

    # 모든 카탈로그 항목을 is_missing으로 채움
    for ci in CATALOG_ITEMS:
        cid = ci["catalog_item_id"]
        if cid not in by_id:
            by_id[cid] = T._missing_item(snapshot_id, cid)

    # 카테고리 필터
    if category_id:
        cat_ids = {ci["catalog_item_id"] for ci in CATALOG_ITEMS if ci["category_id"] == category_id}
        by_id = {k: v for k, v in by_id.items() if k in cat_ids}
    return by_id


async def load_research_item(country_id: str, catalog_item_id: str) -> dict | None:
    items = await load_research_items(country_id)
    return items.get(catalog_item_id)


# ── entry_records (정식 스키마) ───────────────────────────────────────────────

async def load_entry_record(country_id: str) -> dict | None:
    """country_id(ISO 또는 한국어명)로 entry_records 조회. JSON 폴백 포함."""
    from db.transformers import to_iso, to_name, transform_entry_record

    iso = to_iso(country_id)
    db = _get_db()
    if db is not None:
        doc = await db.entry_records.find_one({"country_id": iso}, {"_id": 0})
        if doc:
            return doc
    # JSON 폴백: entry_baseline.json baselines에서 변환
    baselines = load_baseline()["baselines"]
    name = to_name(iso)
    raw = baselines.get(name) or next(
        (b for b in baselines.values() if b.get("country_code") == iso), None
    )
    return transform_entry_record(raw) if raw else None


async def load_multiplier_table() -> dict:
    db = _get_db()
    if db is not None:
        doc = await db.baseline_multipliers.find_one({"_id": "default"})
        if doc:
            return doc.get("table", {})
    return load_baseline().get("multiplier_table", {})


# ── 룰셋 ─────────────────────────────────────────────────────────────────────

_DEFAULT_RULESET = {
    "id": "default",
    "name": "기본 룰셋 v1",
    "version": 1,
    "locked": False,
    "weights": {"market": 0.25, "regulation": 0.25, "environment": 0.20, "system": 0.30},
    "thresholds": {"entry": 60.0, "system_gate": 50.0},
    "killswitch_enabled": True,
}

_memory_rulesets: dict[str, dict] = {"default": dict(_DEFAULT_RULESET)}


async def load_ruleset(ruleset_id: str = "default") -> dict | None:
    db = _get_db()
    if db is not None:
        doc = await db.rulesets.find_one({"id": ruleset_id}, {"_id": 0})
        return doc
    return _memory_rulesets.get(ruleset_id)


async def list_rulesets() -> list[dict]:
    db = _get_db()
    if db is not None:
        docs = await db.rulesets.find({}, {"_id": 0}).to_list(None)
        return docs
    return list(_memory_rulesets.values())


async def save_ruleset(ruleset: dict) -> None:
    db = _get_db()
    if db is not None:
        await db.rulesets.replace_one({"id": ruleset["id"]}, ruleset, upsert=True)
    else:
        _memory_rulesets[ruleset["id"]] = dict(ruleset)


# ── 분석 작업 저장소 ──────────────────────────────────────────────────────────

_memory_analyses: dict[str, dict] = {}
_memory_results: dict[str, dict] = {}


async def save_analysis(analysis: dict) -> None:
    db = _get_db()
    if db is not None:
        await db.analyses.replace_one({"id": analysis["id"]}, analysis, upsert=True)
    else:
        _memory_analyses[analysis["id"]] = analysis


async def get_analysis(analysis_id: str) -> dict | None:
    db = _get_db()
    if db is not None:
        return await db.analyses.find_one({"id": analysis_id}, {"_id": 0})
    return _memory_analyses.get(analysis_id)


async def save_result(result: dict) -> None:
    db = _get_db()
    if db is not None:
        await db.results.replace_one({"id": result["id"]}, result, upsert=True)
    else:
        _memory_results[result["id"]] = result


async def get_result(result_id: str) -> dict | None:
    db = _get_db()
    if db is not None:
        return await db.results.find_one({"id": result_id}, {"_id": 0})
    return _memory_results.get(result_id)


async def list_results(limit: int = 20) -> list[dict]:
    db = _get_db()
    if db is not None:
        return await db.results.find({}, {"_id": 0}).sort("created_at", -1).limit(limit).to_list(None)
    results = sorted(_memory_results.values(), key=lambda r: r.get("created_at", ""), reverse=True)
    return results[:limit]
