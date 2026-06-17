"""
에이전트 부분 실패 복구 / 킬스위치 · 게이트 시나리오 테스트
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
import db.connection as _conn
_conn._db = None
_conn._client = None

from agents.base import AgentResult
from agents.orchestrator import run_analysis
from core.similarity_engine import CategoryScore, KillswitchResult, ScoringResult, calculate_total


# ── AgentResult 기본 동작 ─────────────────────────────────────────────────────

class TestAgentResult:
    def test_empty_result_has_none_score(self):
        result = AgentResult(category="MARKET")
        assert result.category_score is None

    def test_failed_result_zero_coverage(self):
        result = AgentResult(category="MARKET", warnings=["timeout"])
        assert result.coverage == 0.0

    def test_result_with_score(self):
        result = AgentResult(category="MARKET", category_score=75.0, coverage=0.8)
        assert result.category_score == pytest.approx(75.0)


# ── 킬스위치 시나리오 ─────────────────────────────────────────────────────────

class TestKillswitchScenarios:
    def _cat_scores(self, val: float = 80.0) -> dict[str, CategoryScore]:
        return {
            cat: CategoryScore(category=cat, weighted_score=val, raw_score=val, coverage=1.0)
            for cat in ["MARKET", "REGULATION", "ENVIRONMENT", "SYSTEM"]
        }

    def test_killswitch_blocks_high_score(self):
        """점수가 높아도 킬스위치 트리거 시 BLOCKED"""
        ks = [KillswitchResult(item_id="war_zone", blocked=True, value=True, threshold=False)]
        result = calculate_total(
            category_scores=self._cat_scores(95.0),
            killswitch_results=ks,
            category_weights={"MARKET": 0.25, "REGULATION": 0.25, "ENVIRONMENT": 0.20, "SYSTEM": 0.30},
        )
        assert result.verdict == "BLOCKED"
        assert len(result.killswitch_hits) == 1
        assert result.killswitch_hits[0].item_id == "war_zone"

    def test_no_killswitch_proceeds_normally(self):
        result = calculate_total(
            category_scores=self._cat_scores(80.0),
            killswitch_results=[],
            category_weights={"MARKET": 0.25, "REGULATION": 0.25, "ENVIRONMENT": 0.20, "SYSTEM": 0.30},
        )
        assert result.verdict != "BLOCKED"

    def test_inactive_killswitch_not_blocked(self):
        ks = [KillswitchResult(item_id="soft_flag", blocked=False, value=True, threshold=True)]
        result = calculate_total(
            category_scores=self._cat_scores(80.0),
            killswitch_results=ks,
        )
        assert result.verdict != "BLOCKED"

    def test_multiple_killswitches_all_must_pass(self):
        ks = [
            KillswitchResult(item_id="flag_a", blocked=False),
            KillswitchResult(item_id="flag_b", blocked=True),
        ]
        result = calculate_total(
            category_scores=self._cat_scores(90.0),
            killswitch_results=ks,
        )
        assert result.verdict == "BLOCKED"


# ── 게이트 시나리오 ───────────────────────────────────────────────────────────

class TestGateScenarios:
    def _cat_scores_with_system(self, system_score: float) -> dict[str, CategoryScore]:
        base = {
            cat: CategoryScore(category=cat, weighted_score=80.0, raw_score=80.0, coverage=1.0)
            for cat in ["MARKET", "REGULATION", "ENVIRONMENT"]
        }
        base["SYSTEM"] = CategoryScore(
            category="SYSTEM",
            weighted_score=system_score,
            raw_score=system_score,
            coverage=1.0,
        )
        return base

    def test_system_gate_pass(self):
        result = calculate_total(
            category_scores=self._cat_scores_with_system(60.0),
            killswitch_results=[],
            thresholds={"entry": 60.0, "system_gate": 50.0},
        )
        assert result.system_gate_passed is True

    def test_system_gate_fail(self):
        result = calculate_total(
            category_scores=self._cat_scores_with_system(40.0),
            killswitch_results=[],
            thresholds={"entry": 60.0, "system_gate": 50.0},
        )
        assert result.system_gate_passed is False
        assert result.verdict in ("DEEP_RESEARCH", "BLOCKED")

    def test_gate_boundary_exact(self):
        # raw_score = 50.0 exactly (경계값)
        result = calculate_total(
            category_scores=self._cat_scores_with_system(50.0),
            killswitch_results=[],
            thresholds={"entry": 60.0, "system_gate": 50.0},
        )
        # 50.0 < 50.0 is False → gate passed
        assert result.system_gate_passed is True


# ── 에이전트 부분 실패 판정 로직 ──────────────────────────────────────────────

class TestAgentPartialFailure:
    """오케스트레이터 실패 판정 로직 단위 테스트"""

    def _count_failed(self, results: list[AgentResult]) -> int:
        return sum(
            1 for r in results
            if r.category_score is None and r.coverage == 0.0
        )

    def test_one_failure_continues(self):
        results = [
            AgentResult(category="MARKET", category_score=70.0, coverage=0.8),
            AgentResult(category="REGULATION"),        # 실패
            AgentResult(category="ENVIRONMENT", category_score=65.0, coverage=0.7),
            AgentResult(category="SYSTEM", category_score=60.0, coverage=0.9),
        ]
        assert self._count_failed(results) == 1
        assert self._count_failed(results) < 2

    def test_two_failures_stops(self):
        results = [
            AgentResult(category="MARKET"),            # 실패
            AgentResult(category="REGULATION"),        # 실패
            AgentResult(category="ENVIRONMENT", category_score=65.0, coverage=0.7),
            AgentResult(category="SYSTEM", category_score=60.0, coverage=0.9),
        ]
        assert self._count_failed(results) >= 2

    def test_all_pass(self):
        results = [
            AgentResult(category="MARKET", category_score=70.0, coverage=0.8),
            AgentResult(category="REGULATION", category_score=75.0, coverage=0.9),
            AgentResult(category="ENVIRONMENT", category_score=65.0, coverage=0.7),
            AgentResult(category="SYSTEM", category_score=80.0, coverage=1.0),
        ]
        assert self._count_failed(results) == 0
