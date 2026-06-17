"""SummaryAgent — Phase 2 통합 판정 + 보고서 생성 (Claude Sonnet 4.6)"""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from typing import Callable

from agents.base import AgentResult, BaseAgent, KillswitchResult
from core.scoring import apply_ruleset, estimate_cost
from core.similarity_engine import CategoryScore, calculate_category_score, ItemSimilarity
from db.loaders import load_entry_record, load_multiplier_table
from db.models import CategoryResult, ItemScore as ModelItemScore, Ruleset, SimilarityResult

_SYSTEM_PROMPT = """당신은 오토금융 해외진출 전략 컨설턴트입니다.
분석 결과를 바탕으로 의사결정자를 위한 보고서를 작성하세요.

작성 지침:
- summary: 3~5문장. 판정 근거와 핵심 리스크를 포함.
- ai_insight: 카테고리별 강약점 + 진출 전략 제언 (항목 형식, 각 항목 50자 이내).
- 수치는 반드시 출처와 함께 인용하세요.
- 킬스위치 항목이 있으면 최우선으로 언급하세요.
- 데이터 미확보 항목은 "데이터 미확보"로 명시하고, 추측하지 마세요.

응답 형식 (JSON):
{
  "summary": "<3~5문장 종합 요약>",
  "ai_insight": "<카테고리별 강약점 및 전략 제언>"
}"""


def _collect_killswitches(phase1_results: list[AgentResult]) -> list[KillswitchResult]:
    results = []
    for r in phase1_results:
        results.extend(r.killswitch_results)
    return results


def _build_category_scores(phase1_results: list[AgentResult]) -> dict[str, CategoryScore]:
    scores: dict[str, CategoryScore] = {}
    category_map = {
        "MARKET": "MARKET",
        "REGULATORY": "REGULATION",
        "FINANCIAL": "ENVIRONMENT",
        "SYSTEM": "SYSTEM",
    }
    for result in phase1_results:
        key = category_map.get(result.category, result.category)
        item_sims = [
            ItemSimilarity(
                catalog_item_id=it.catalog_item_id,
                similarity=it.similarity,
                confidence_grade=it.confidence_grade,
                is_missing=it.is_missing,
            )
            for it in result.items
        ]
        cat_score = calculate_category_score(item_sims, category=key)
        scores[key] = cat_score
    return scores


class SummaryAgent(BaseAgent):

    async def synthesize(
        self,
        analysis_id: str,
        target_country: str,
        compared_country: str,
        phase1_results: list[AgentResult],
        ruleset: Ruleset,
        ws_broadcaster: Callable | None = None,
    ) -> SimilarityResult:

        async def _broadcast(progress: int, message: str, status: str = "running") -> None:
            if ws_broadcaster:
                await ws_broadcaster("summary", progress, status, message)

        await _broadcast(0, "통합 분석 시작")

        # 1. 카테고리 점수 수집
        category_scores = _build_category_scores(phase1_results)
        killswitch_results = _collect_killswitches(phase1_results)

        await _broadcast(20, "종합 점수 계산 중")

        # 2. 룰셋 적용 → 판정 (코드)
        scoring_result = apply_ruleset(category_scores, killswitch_results, ruleset)

        await _broadcast(40, "비용 추정 중")

        # 3. 비용 추정 (코드)
        # entry_records의 prep_cost_usd(달러)를 estimate_cost가 기대하는
        # entry_cost_usd_million(백만 달러) 단위로 변환해 어댑팅한다.
        entry_record = await load_entry_record(compared_country) or {}
        multiplier_table = await load_multiplier_table()
        prep_cost_usd = entry_record.get("prep_cost_usd")
        compared_baseline = (
            {"entry_cost_usd_million": round(prep_cost_usd / 1_000_000, 2)}
            if prep_cost_usd is not None else {}
        )
        cost_estimate = estimate_cost(
            scoring_result.total_score or 0.0,
            compared_baseline,
            multiplier_table,
        )

        await _broadcast(60, "보고서 텍스트 생성 중 (Claude Sonnet)")

        # 4. 보고서 텍스트 생성 (Sonnet)
        summary_text = ""
        ai_insight = ""
        all_warnings = [w for r in phase1_results for w in r.warnings]
        all_human_reviews = [f for r in phase1_results for f in r.human_review_flags]

        try:
            report_context = {
                "target": target_country,
                "compared": compared_country,
                "verdict": scoring_result.verdict,
                "total_score": scoring_result.total_score,
                "category_scores": {
                    k: {
                        "raw_score": v.raw_score,
                        "coverage": v.coverage,
                        "weighted_score": v.weighted_score,
                    }
                    for k, v in scoring_result.category_scores.items()
                },
                "killswitch_hits": [
                    {"item_id": ks.item_id, "blocked": ks.blocked, "reason": ks.reason}
                    for ks in scoring_result.killswitch_hits
                ],
                "system_gate_passed": scoring_result.system_gate_passed,
                "cost_estimate": cost_estimate,
                "warnings": all_warnings,
                "human_review_flags": all_human_reviews,
                "phase1_evidences": {
                    r.category: [
                        {"item_id": it.catalog_item_id, "evidence": it.evidence}
                        for it in r.items if it.evidence
                    ]
                    for r in phase1_results
                },
            }

            messages = [
                {
                    "role": "user",
                    "content": (
                        f"다음 분석 결과를 바탕으로 보고서를 작성하세요.\n\n"
                        f"{json.dumps(report_context, ensure_ascii=False, indent=2)}"
                    ),
                }
            ]
            response = await self._call_sonnet(_SYSTEM_PROMPT, messages)
            text = self._extract_text(response)

            parsed: dict = {}
            try:
                start = text.find("{")
                end = text.rfind("}") + 1
                if start >= 0 and end > start:
                    parsed = json.loads(text[start:end])
            except Exception:
                pass

            summary_text = parsed.get("summary", text[:500] if text else "보고서 생성 실패")
            ai_insight = parsed.get("ai_insight", "")

        except Exception as e:
            summary_text = f"보고서 생성 중 오류: {e}"

        await _broadcast(90, "결과 저장 중")

        # 5. SimilarityResult 조립
        result_id = f"res_{uuid.uuid4().hex[:12]}"

        category_results = []
        for result in phase1_results:
            category_results.append(CategoryResult(
                category=result.category,
                items=[
                    ModelItemScore(
                        catalog_item_id=it.catalog_item_id,
                        similarity=it.similarity,
                        confidence_grade=it.confidence_grade,
                        source_tier=it.source_tier,
                        evidence=it.evidence,
                        is_missing=it.is_missing,
                    )
                    for it in result.items
                ],
                category_score=result.category_score,
                coverage=result.coverage,
                gate_passed=result.gate_passed,
                killswitch_results=[
                    {"item_id": ks.item_id, "blocked": ks.blocked, "reason": ks.reason}
                    for ks in result.killswitch_results
                ],
                warnings=result.warnings,
            ))

        similarity_result = SimilarityResult(
            id=result_id,
            analysis_id=analysis_id,
            target_country=target_country,
            compared_country=compared_country,
            ruleset_id=ruleset.id,
            verdict=scoring_result.verdict,
            total_score=scoring_result.total_score,
            category_results=category_results,
            cost_estimate=cost_estimate,
            summary=summary_text,
            ai_insight=ai_insight,
            human_review_flags=all_human_reviews,
            created_at=datetime.now(timezone.utc),
        )

        await _broadcast(100, "분석 완료")
        return similarity_result
