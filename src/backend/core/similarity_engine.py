"""
유사도 엔진 — 결정적(재현 가능), LLM 없음

설계 원칙:
  - null ≠ 0: 미확보 데이터는 분모에서 제외
  - 점수·판정은 이 모듈에서만 산출
  - 킬스위치·게이트는 코드로 처리
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from core.normalizer import normalize_pair, normalize_rate


# ── 신뢰도 계수 ────────────────────────────────────────────────────────────────

_CONFIDENCE_COEF: dict[str, float] = {
    "HIGH": 1.0,
    "MEDIUM": 0.85,
    "LOW": 0.70,
}


# ── 반환 타입 ──────────────────────────────────────────────────────────────────

@dataclass
class ItemSimilarity:
    catalog_item_id: str
    similarity: float | None      # None = 비교 불가 (데이터 미확보)
    confidence_grade: str = "LOW"
    is_missing: bool = False


@dataclass
class CategoryScore:
    category: str
    weighted_score: float         # 0~100, coverage 보정 후
    raw_score: float              # 0~100, 유효 항목 평균
    coverage: float               # 유효 항목 비율 0~1
    item_similarities: list[ItemSimilarity] = field(default_factory=list)


@dataclass
class KillswitchResult:
    item_id: str
    blocked: bool
    value: Any = None
    threshold: Any = None


@dataclass
class ScoringResult:
    verdict: str                  # TRANSPLANTABLE / DEEP_RESEARCH / BLOCKED
    total_score: float | None
    category_scores: dict[str, CategoryScore] = field(default_factory=dict)
    killswitch_hits: list[KillswitchResult] = field(default_factory=list)
    system_gate_passed: bool = True


# ── 항목 유사도 (1층) ──────────────────────────────────────────────────────────

def score_item(
    target_value: float | str | bool | None,
    baseline_value: float | str | bool | None,
    similarity_type: str,          # CONTINUOUS | CATEGORICAL | BINARY | REFERENCE
    confidence_grade: str = "LOW",
    currency_target: str = "USD",
    currency_baseline: str = "USD",
    catalog_item_id: str = "",
) -> ItemSimilarity:

    if target_value is None or baseline_value is None:
        return ItemSimilarity(catalog_item_id=catalog_item_id, similarity=None, is_missing=True)

    raw: float | None = None

    if similarity_type == "CONTINUOUS":
        try:
            t = float(target_value)
            b = float(baseline_value)
        except (TypeError, ValueError):
            return ItemSimilarity(catalog_item_id=catalog_item_id, similarity=None, is_missing=True)

        # 통화 정규화
        pair = normalize_pair(t, b, currency_target, currency_baseline)
        if pair is None:
            pair = (t, b)
        t, b = pair

        # 비율 형태 통일
        t = normalize_rate(t)
        b = normalize_rate(b)

        denom = max(abs(t), abs(b))
        if denom == 0:
            raw = 1.0
        else:
            raw = 1.0 - abs(t - b) / denom
        raw = max(0.0, min(1.0, raw))

    elif similarity_type == "CATEGORICAL":
        raw = 1.0 if str(target_value) == str(baseline_value) else 0.0

    elif similarity_type == "BINARY":
        raw = 1.0 if bool(target_value) == bool(baseline_value) else 0.0

    elif similarity_type == "REFERENCE":
        # 점수 기여 없음 — 보고서용 참조 데이터
        return ItemSimilarity(catalog_item_id=catalog_item_id, similarity=None, is_missing=False)

    else:
        return ItemSimilarity(catalog_item_id=catalog_item_id, similarity=None, is_missing=True)

    coef = _CONFIDENCE_COEF.get(confidence_grade.upper(), _CONFIDENCE_COEF["LOW"])
    return ItemSimilarity(
        catalog_item_id=catalog_item_id,
        similarity=raw * coef,
        confidence_grade=confidence_grade,
        is_missing=False,
    )


# ── 카테고리 점수 (2층) ────────────────────────────────────────────────────────

def calculate_category_score(
    item_similarities: list[ItemSimilarity],
    item_weights: list[float] | None = None,
    category: str = "",
) -> CategoryScore:
    """
    item_weights: 항목별 가중치 (None이면 균등)
    null 항목은 분모에서 제외 (null ≠ 0 원칙)
    """
    n = len(item_similarities)
    if item_weights is None:
        item_weights = [1.0] * n

    valid = [
        (s.similarity, w)
        for s, w in zip(item_similarities, item_weights)
        if s.similarity is not None
    ]

    if not valid:
        return CategoryScore(
            category=category,
            weighted_score=0.0,
            raw_score=0.0,
            coverage=0.0,
            item_similarities=item_similarities,
        )

    total_weight = sum(w for _, w in valid)
    raw_score = sum(s * w for s, w in valid) / total_weight * 100
    coverage = len(valid) / n if n > 0 else 0.0

    return CategoryScore(
        category=category,
        weighted_score=raw_score * coverage,  # 데이터 부족 페널티
        raw_score=raw_score,
        coverage=coverage,
        item_similarities=item_similarities,
    )


# ── 종합 점수 + 게이트 + 킬스위치 (3층) ──────────────────────────────────────

def calculate_total(
    category_scores: dict[str, CategoryScore],
    killswitch_results: list[KillswitchResult],
    category_weights: dict[str, float] | None = None,
    thresholds: dict[str, float] | None = None,
) -> ScoringResult:
    """
    category_scores: {"MARKET": ..., "REGULATION": ..., "ENVIRONMENT": ..., "SYSTEM": ...}
    killswitch_results: RegulationAgent에서 전달
    """
    if category_weights is None:
        category_weights = {
            "MARKET": 0.25,
            "REGULATION": 0.25,
            "ENVIRONMENT": 0.20,
            "SYSTEM": 0.30,
        }
    if thresholds is None:
        thresholds = {"entry": 60.0, "system_gate": 50.0}

    # 1. 킬스위치 우선
    blocked = [r for r in killswitch_results if r.blocked]
    if blocked:
        return ScoringResult(
            verdict="BLOCKED",
            total_score=0.0,
            category_scores=category_scores,
            killswitch_hits=blocked,
            system_gate_passed=False,
        )

    # 2. 시스템 게이트
    system = category_scores.get("SYSTEM")
    system_gate_passed = True
    if system is not None and system.raw_score < thresholds["system_gate"]:
        system_gate_passed = False

    # 3. 종합 점수
    total = sum(
        cs.weighted_score * category_weights.get(cat, 0.0)
        for cat, cs in category_scores.items()
    )

    if not system_gate_passed:
        return ScoringResult(
            verdict="DEEP_RESEARCH",
            total_score=total,
            category_scores=category_scores,
            killswitch_hits=[],
            system_gate_passed=False,
        )

    verdict = "TRANSPLANTABLE" if total >= thresholds["entry"] else "DEEP_RESEARCH"
    return ScoringResult(
        verdict=verdict,
        total_score=total,
        category_scores=category_scores,
        killswitch_hits=[],
        system_gate_passed=True,
    )
