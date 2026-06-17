"""
정식 스키마 마이그레이션 테스트 — catalog_seed / transformers / research_items 로더
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import asyncio
import pytest

import db.connection as _conn
_conn._db = None
_conn._client = None

from db.catalog_seed import CATALOG_CATEGORIES, CATALOG_ITEMS
from db import transformers as T
from db import loaders as L


# ── catalog_seed ──────────────────────────────────────────────────────────────

class TestCatalogSeed:
    def test_four_categories(self):
        ids = {c["category_id"] for c in CATALOG_CATEGORIES}
        assert ids == {"MARKET", "REGULATORY", "FINANCIAL", "SYSTEM"}

    def test_no_duplicate_catalog_ids(self):
        ids = [i["catalog_item_id"] for i in CATALOG_ITEMS]
        assert len(ids) == len(set(ids))

    def test_killswitch_items_have_rules(self):
        ks = [i for i in CATALOG_ITEMS if i["is_killswitch"]]
        assert len(ks) == 5
        for i in ks:
            assert i["killswitch_rule"], f"{i['catalog_item_id']} 룰 없음"
            assert "operator" in i["killswitch_rule"]
            assert "threshold" in i["killswitch_rule"]

    def test_all_similarity_types_valid(self):
        valid = {"CONTINUOUS", "CATEGORICAL", "BINARY", "REFERENCE"}
        for i in CATALOG_ITEMS:
            assert i["similarity_type"] in valid

    def test_system_category_is_gate(self):
        system = next(c for c in CATALOG_CATEGORIES if c["category_id"] == "SYSTEM")
        assert system["is_gate"] is True
        assert system["gate_threshold"] == 50.0


# ── ISO 매핑 ──────────────────────────────────────────────────────────────────

class TestIsoMapping:
    def test_to_iso_from_name(self):
        assert T.to_iso("한국") == "KR"
        assert T.to_iso("독일") == "DE"

    def test_to_iso_passthrough(self):
        assert T.to_iso("KR") == "KR"
        assert T.to_iso("DE") == "DE"

    def test_to_name_from_iso(self):
        assert T.to_name("KR") == "한국"
        assert T.to_name("DE") == "독일"


# ── 시장 변환 ─────────────────────────────────────────────────────────────────

class TestMarketTransformer:
    def _de_market(self):
        import json
        path = os.path.join(os.path.dirname(__file__), "..", "..", "..",
                            "data", "auto_finance_market", "auto_finance_market.json")
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        return next(m for m in d["markets"] if m["country_code"] == "DE")

    def test_de_penetration_maps_to_mkt001(self):
        items = T.transform_market_data(self._de_market(), "DE_test")
        by_id = {i["catalog_item_id"]: i for i in items}
        assert "MKT_001" in by_id
        assert not by_id["MKT_001"]["is_missing"]
        assert by_id["MKT_001"]["value_normalized"] is not None

    def test_percent_normalized_to_0_1(self):
        items = T.transform_market_data(self._de_market(), "DE_test")
        by_id = {i["catalog_item_id"]: i for i in items}
        v = by_id["MKT_001"]["value_normalized"]
        assert 0.0 <= v <= 1.0

    def test_market_catalog_filled(self):
        # 변환 결과는 MARKET 카탈로그 전체를 포함 (없는 건 is_missing)
        items = T.transform_market_data(self._de_market(), "DE_test")
        market_ids = {i["catalog_item_id"] for i in CATALOG_ITEMS if i["category_id"] == "MARKET"}
        present = {i["catalog_item_id"] for i in items}
        assert market_ids.issubset(present)


# ── 킬스위치 목업 ─────────────────────────────────────────────────────────────

class TestKillswitchMockup:
    def test_china_foreign_ownership_below_100(self):
        items = T._apply_killswitch_mockup([], "CN", "CN_test")
        by_id = {i["catalog_item_id"]: i for i in items}
        # 중국 외국인지분 51% — 원본 스케일 유지 (정규화 안 함)
        assert by_id["REG_001"]["value_normalized"] == 51

    def test_killswitch_mockup_tier3(self):
        items = T._apply_killswitch_mockup([], "KR", "KR_test")
        for i in items:
            assert i["source_tier"] == "TIER3"
            assert "추정" in (i["evidence"] or "")


# ── research_items 로더 (JSON 폴백) ──────────────────────────────────────────

class TestResearchItemsLoader:
    def test_returns_dict(self):
        result = asyncio.get_event_loop().run_until_complete(
            L.load_research_items("DE", "MARKET")
        )
        assert isinstance(result, dict)
        assert len(result) > 0

    def test_known_country_has_data(self):
        result = asyncio.get_event_loop().run_until_complete(
            L.load_research_items("DE", "MARKET")
        )
        scored = [v for v in result.values() if not v["is_missing"]]
        assert len(scored) > 0

    def test_missing_items_included(self):
        # 멕시코는 실데이터 거의 없음 → 대부분 is_missing이지만 항목은 모두 존재
        result = asyncio.get_event_loop().run_until_complete(
            L.load_research_items("MX", "MARKET")
        )
        market_ids = {i["catalog_item_id"] for i in CATALOG_ITEMS if i["category_id"] == "MARKET"}
        assert set(result.keys()) == market_ids

    def test_korean_name_equivalent_to_iso(self):
        by_iso = asyncio.get_event_loop().run_until_complete(
            L.load_research_items("DE", "MARKET")
        )
        by_name = asyncio.get_event_loop().run_until_complete(
            L.load_research_items("독일", "MARKET")
        )
        assert by_iso["MKT_001"]["value_normalized"] == by_name["MKT_001"]["value_normalized"]

    def test_entry_record_loaded(self):
        rec = asyncio.get_event_loop().run_until_complete(L.load_entry_record("US"))
        assert rec is not None
        assert rec["prep_cost_usd"] == 1500000
        assert rec["country_id"] == "US"


# ── license 변환 ──────────────────────────────────────────────────────────────

class TestLicenseTransformer:
    def _kr_license(self):
        import json
        path = os.path.join(os.path.dirname(__file__), "..", "..", "..",
                            "data", "regulations", "capital_license.json")
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        return next(l for l in d["licenses"] if l["country_code"] == "KR")

    def test_kr_license_value_not_none(self):
        items = T.transform_license_data(self._kr_license(), "KR_test")
        by_id = {i["catalog_item_id"]: i for i in items}
        assert "REG_006" in by_id
        assert by_id["REG_006"]["value_normalized"] is not None
