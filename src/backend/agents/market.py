"""MarketAgent — 시장 카테고리 분석 (가중치 25%)"""
from __future__ import annotations

from typing import Callable

from agents.base import AgentResult, BaseAgent
from agents.common import build_item_scores, collect_category_data, generate_evidence

_CATEGORY_ID = "MARKET"

_SYSTEM_PROMPT = """당신은 오토금융 시장 분석 전문가입니다.
두 국가의 시장 데이터를 비교하고, 각 항목에 대한 근거 문장을 한국어로 작성하세요.

규칙:
- 점수는 계산하지 않습니다. 근거 문장(evidence)만 작성하세요.
- null 값은 "공식 데이터 미확보"로 명시하고, 추측하지 마세요.
- 출처가 TIER2·3인 항목은 "공식 출처 미확보" 표시를 반드시 포함하세요.
- 응답은 반드시 아래 JSON 형식으로만 반환하세요.

응답 형식:
{
  "evidences": {"<catalog_item_id>": "<근거 문장>"},
  "warnings": ["<경고 메시지>"]
}"""


class MarketAgent(BaseAgent):

    async def analyze(
        self,
        target_country: str,
        compared_country: str,
        ruleset_id: str = "default",
        ws_broadcaster: Callable | None = None,
    ) -> AgentResult:

        async def _broadcast(progress: int, message: str, status: str = "running") -> None:
            if ws_broadcaster:
                await ws_broadcaster("market", progress, status, message)

        await _broadcast(0, "시장 데이터 수집 시작")

        try:
            catalog, target_items, baseline_items = await collect_category_data(
                target_country, compared_country, _CATEGORY_ID
            )

            await _broadcast(30, "데이터 로드 완료, LLM 근거 생성 시작")

            parsed = await generate_evidence(
                self, _SYSTEM_PROMPT, target_country, compared_country,
                catalog, target_items, baseline_items,
            )
            evidences = parsed.get("evidences", {})
            warnings = list(parsed.get("warnings", []))

            await _broadcast(80, "근거 문장 생성 완료, 점수 계산 중")

            items, cat_score = build_item_scores(
                catalog, target_items, baseline_items, evidences, "MARKET"
            )
            if cat_score.coverage == 0.0:
                warnings.append(f"{target_country}/{compared_country} 시장 데이터 미확보")

            await _broadcast(100, "시장 분석 완료")

            return AgentResult(
                category="MARKET",
                items=items,
                category_score=cat_score.raw_score,
                coverage=cat_score.coverage,
                warnings=warnings,
            )

        except Exception as e:
            if ws_broadcaster:
                await ws_broadcaster("market", 0, "error", str(e))
            return AgentResult(category="MARKET", warnings=[f"MarketAgent 오류: {e}"])
