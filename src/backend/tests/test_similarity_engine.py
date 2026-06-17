"""
유사도 엔진 단위 테스트

검증 항목:
  - null ≠ 0 원칙 (미확보 데이터 마스킹)
  - 킬스위치 코드 판정
  - 게이트 코드 판정
  - coverage 가중 점수 계산
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from core.similarity_engine import (
    ItemSimilarity,
    KillswitchResult,
    ScoringResult,
    calculate_category_score,
    calculate_total,
    score_item,
)


# ── score_item ────────────────────────────────────────────────────────────────

class TestScoreItem:
    def test_continuous_identical(self):
        # LOW confidence_grade(0.7) × 완전일치(1.0) = 0.7
        result = score_item(100.0, 100.0, "CONTINUOUS", confidence_grade="LOW")
        assert result.similarity == pytest.approx(0.7)
        assert not result.is_missing

    def test_continuous_identical_high_confidence(self):
        result = score_item(100.0, 100.0, "CONTINUOUS", confidence_grade="HIGH")
        assert result.similarity == pytest.approx(1.0)

    def test_continuous_zero_target(self):
        result = score_item(0.0, 100.0, "CONTINUOUS")
        assert result.similarity == pytest.approx(0.0)

    def test_null_target_is_missing(self):
        result = score_item(None, 100.0, "CONTINUOUS")
        assert result.is_missing
        assert result.similarity is None

    def test_null_baseline_is_missing(self):
        result = score_item(100.0, None, "CONTINUOUS")
        assert result.is_missing
        assert result.similarity is None

    def test_categorical_match(self):
        # LOW confidence_grade = 0.7
        result = score_item("COMMON_LAW", "COMMON_LAW", "CATEGORICAL", confidence_grade="HIGH")
        assert result.similarity == pytest.approx(1.0)

    def test_categorical_mismatch(self):
        result = score_item("CIVIL_LAW", "COMMON_LAW", "CATEGORICAL", confidence_grade="HIGH")
        assert result.similarity == pytest.approx(0.0)

    def test_binary_match(self):
        result = score_item(True, True, "BINARY", confidence_grade="HIGH")
        assert result.similarity == pytest.approx(1.0)

    def test_binary_mismatch(self):
        result = score_item(True, False, "BINARY", confidence_grade="HIGH")
        assert result.similarity == pytest.approx(0.0)

    def test_confidence_grade_applied(self):
        high = score_item(100.0, 100.0, "CONTINUOUS", confidence_grade="HIGH")
        low = score_item(100.0, 100.0, "CONTINUOUS", confidence_grade="LOW")
        # HIGH 신뢰도가 LOW보다 크거나 같아야 함
        assert high.similarity >= low.similarity


# ── calculate_category_score ──────────────────────────────────────────────────

class TestCalculateCategoryScore:
    def test_null_not_zero(self):
        items = [
            ItemSimilarity("item1", similarity=None, is_missing=True),
            ItemSimilarity("item2", similarity=0.8),
            ItemSimilarity("item3", similarity=0.6),
        ]
        score = calculate_category_score(items, category="MARKET")
        # item1은 분모에서 제외 → coverage = 2/3
        assert score.coverage == pytest.approx(2 / 3, rel=1e-3)
        assert score.raw_score == pytest.approx((0.8 + 0.6) / 2 * 100, rel=1e-3)

    def test_all_missing_returns_none(self):
        items = [
            ItemSimilarity("item1", similarity=None, is_missing=True),
            ItemSimilarity("item2", similarity=None, is_missing=True),
        ]
        score = calculate_category_score(items, category="MARKET")
        assert score.weighted_score == 0.0
        assert score.coverage == 0.0

    def test_full_coverage(self):
        items = [ItemSimilarity(f"i{i}", similarity=1.0) for i in range(5)]
        score = calculate_category_score(items, category="MARKET")
        assert score.coverage == pytest.approx(1.0)
        assert score.raw_score == pytest.approx(100.0)


# ── calculate_total / 킬스위치 / 게이트 ──────────────────────────────────────

class TestCalculateTotal:
    def _make_category_scores(self, scores: dict[str, float]):
        from dataclasses import dataclass, field as dc_field

        result = {}
        for cat, val in scores.items():
            from core.similarity_engine import CategoryScore
            result[cat] = CategoryScore(
                category=cat,
                weighted_score=val,
                raw_score=val,
                coverage=1.0,
            )
        return result

    def test_transplantable_verdict(self):
        cat_scores = self._make_category_scores({
            "MARKET": 80.0, "REGULATION": 70.0, "ENVIRONMENT": 75.0, "SYSTEM": 65.0
        })
        result = calculate_total(
            category_scores=cat_scores,
            killswitch_results=[],
            category_weights={"MARKET": 0.25, "REGULATION": 0.25, "ENVIRONMENT": 0.20, "SYSTEM": 0.30},
            thresholds={"entry": 60.0, "system_gate": 50.0},
        )
        assert result.verdict == "TRANSPLANTABLE"
        assert result.total_score is not None
        assert result.total_score >= 60.0

    def test_blocked_by_killswitch(self):
        cat_scores = self._make_category_scores({
            "MARKET": 90.0, "REGULATION": 90.0, "ENVIRONMENT": 90.0, "SYSTEM": 90.0
        })
        killswitch = [KillswitchResult(item_id="sanction_risk", blocked=True, value=True, threshold=False)]
        result = calculate_total(
            category_scores=cat_scores,
            killswitch_results=killswitch,
            category_weights={"MARKET": 0.25, "REGULATION": 0.25, "ENVIRONMENT": 0.20, "SYSTEM": 0.30},
            thresholds={"entry": 60.0, "system_gate": 50.0},
        )
        assert result.verdict == "BLOCKED"

    def test_system_gate_fails(self):
        cat_scores = self._make_category_scores({
            "MARKET": 80.0, "REGULATION": 80.0, "ENVIRONMENT": 80.0, "SYSTEM": 30.0
        })
        result = calculate_total(
            category_scores=cat_scores,
            killswitch_results=[],
            category_weights={"MARKET": 0.25, "REGULATION": 0.25, "ENVIRONMENT": 0.20, "SYSTEM": 0.30},
            thresholds={"entry": 60.0, "system_gate": 50.0},
        )
        assert result.verdict in ("DEEP_RESEARCH", "BLOCKED")
        assert not result.system_gate_passed

    def test_low_total_deep_research(self):
        cat_scores = self._make_category_scores({
            "MARKET": 30.0, "REGULATION": 40.0, "ENVIRONMENT": 35.0, "SYSTEM": 55.0
        })
        result = calculate_total(
            category_scores=cat_scores,
            killswitch_results=[],
            category_weights={"MARKET": 0.25, "REGULATION": 0.25, "ENVIRONMENT": 0.20, "SYSTEM": 0.30},
            thresholds={"entry": 60.0, "system_gate": 50.0},
        )
        assert result.verdict == "DEEP_RESEARCH"
        assert result.total_score < 60.0
