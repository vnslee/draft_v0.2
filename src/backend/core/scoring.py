"""가중치·킬스위치·게이트 설정을 룰셋에서 읽어 유사도 엔진에 전달하는 어댑터"""
from __future__ import annotations

from db.models import Ruleset
from core.similarity_engine import CategoryScore, KillswitchResult, ScoringResult, calculate_total


def apply_ruleset(
    category_scores: dict[str, CategoryScore],
    killswitch_results: list[KillswitchResult],
    ruleset: Ruleset,
) -> ScoringResult:
    weights = {
        "MARKET": ruleset.weights.market,
        "REGULATION": ruleset.weights.regulation,
        "ENVIRONMENT": ruleset.weights.environment,
        "SYSTEM": ruleset.weights.system,
    }
    thresholds = {
        "entry": ruleset.thresholds.entry,
        "system_gate": ruleset.thresholds.system_gate,
    }

    # 킬스위치 비활성화 옵션
    active_killswitches = killswitch_results if ruleset.killswitch_enabled else []

    return calculate_total(
        category_scores=category_scores,
        killswitch_results=active_killswitches,
        category_weights=weights,
        thresholds=thresholds,
    )


def estimate_cost(
    total_score: float,
    compared_baseline: dict,
    multiplier_table: dict,
) -> dict:
    """
    진출국 baseline 비용에 유사도 역수 multiplier 적용
    total_score: 0~100
    """
    base_cost = compared_baseline.get("entry_cost_usd_million")
    if base_cost is None:
        return {"estimated": False, "reason": "기준국 비용 데이터 미확보"}

    # 유사도가 낮을수록 비용 multiplier 증가
    similarity_ratio = total_score / 100.0
    bands = multiplier_table.get("bands", [])
    multiplier = 2.0  # 기본값
    for band in bands:
        low = band.get("min", 0)
        high = band.get("max", 1.01)
        if low <= similarity_ratio < high:
            multiplier = band.get("duration_x", 2.0)
            break

    return {
        "estimated": True,
        "base_cost_usd_million": base_cost,
        "multiplier": multiplier,
        "estimated_cost_usd_million": round(base_cost * multiplier, 2),
        "similarity_ratio": round(similarity_ratio, 3),
    }
