"""
catalog_item_id 기반 에이전트 점수 산출 / 킬스위치 검증
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import asyncio
import re
import pytest

import db.connection as _conn
_conn._db = None
_conn._client = None

from agents.common import build_item_scores, collect_category_data
from agents.regulation import check_killswitch
from db.catalog_seed import CATALOG_ITEMS


_ID_RE = re.compile(r"^(MKT|REG|FIN|SYS)_\d{3}$")


def _run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


# ── 카탈로그 기반 점수 ────────────────────────────────────────────────────────

class TestCatalogBasedScoring:
    def test_market_items_use_catalog_ids(self):
        catalog, t, b = _run(collect_category_data("DE", "ES", "MARKET"))
        items, _ = build_item_scores(catalog, t, b, {}, "MARKET")
        assert len(items) > 0
        for it in items:
            assert _ID_RE.match(it.catalog_item_id), it.catalog_item_id

    def test_missing_data_not_zero(self):
        # 멕시코 시장 데이터 거의 없음 → similarity None(미확보)이지 0이 아님
        catalog, t, b = _run(collect_category_data("MX", "KR", "MARKET"))
        items, cat = build_item_scores(catalog, t, b, {}, "MARKET")
        missing = [i for i in items if i.is_missing]
        assert len(missing) > 0
        for i in missing:
            assert i.similarity is None    # null ≠ 0

    def test_coverage_reflects_real_data(self):
        catalog, t, b = _run(collect_category_data("DE", "ES", "MARKET"))
        _, cat = build_item_scores(catalog, t, b, {}, "MARKET")
        assert 0.0 <= cat.coverage <= 1.0


# ── 킬스위치 ──────────────────────────────────────────────────────────────────

class TestRegulationKillswitch:
    def _ks_item(self, cid):
        return next(c for c in CATALOG_ITEMS if c["catalog_item_id"] == cid)

    def test_missing_data_not_blocked(self):
        # 데이터 미확보 → blocked=False (전 국가 BLOCKED 방지)
        result = check_killswitch(self._ks_item("REG_001"), None)
        assert result.blocked is False
        assert "미확보" in result.reason

    def test_missing_flag_research_item_not_blocked(self):
        result = check_killswitch(
            self._ks_item("REG_001"),
            {"is_missing": True, "value_normalized": None},
        )
        assert result.blocked is False

    def test_foreign_ownership_below_threshold_blocked(self):
        # 외국인지분 51% < 100 → blocked
        result = check_killswitch(
            self._ks_item("REG_001"),
            {"is_missing": False, "value_normalized": 51},
        )
        assert result.blocked is True

    def test_foreign_ownership_full_not_blocked(self):
        result = check_killswitch(
            self._ks_item("REG_001"),
            {"is_missing": False, "value_normalized": 100},
        )
        assert result.blocked is False

    def test_fx_restricted_eq_blocked(self):
        # REG_002: EQ "RESTRICTED" → blocked
        result = check_killswitch(
            self._ks_item("REG_002"),
            {"is_missing": False, "value_normalized": "RESTRICTED"},
        )
        assert result.blocked is True

    def test_fx_ok_not_blocked(self):
        result = check_killswitch(
            self._ks_item("REG_002"),
            {"is_missing": False, "value_normalized": "OK"},
        )
        assert result.blocked is False

    def test_rate_cap_lte_blocked(self):
        # REG_005: 금리상한 LTE 15 → 12%면 blocked
        result = check_killswitch(
            self._ks_item("REG_005"),
            {"is_missing": False, "value_normalized": 12},
        )
        assert result.blocked is True

    def test_non_killswitch_returns_none(self):
        # 킬스위치 아닌 항목은 None
        non_ks = next(c for c in CATALOG_ITEMS if not c["is_killswitch"])
        result = check_killswitch(non_ks, {"is_missing": False, "value_normalized": 50})
        assert result is None
