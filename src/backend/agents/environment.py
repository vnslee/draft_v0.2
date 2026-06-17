"""EnvironmentAgent — 금융환경 카테고리 분석 (가중치 20%)"""
from __future__ import annotations

from typing import Callable

from agents.base import AgentResult, BaseAgent
from agents.common import build_item_scores, collect_category_data, generate_evidence

_CATEGORY_ID = "FINANCIAL"

_SYSTEM_PROMPT = """당신은 오토금융 금융환경 분석 전문가입니다.
두 국가의 금융환경(금리, LTV, 캡티브 강도, 신용인프라 등)을 비교하고 근거 문장을 한국어로 작성하세요.

규칙:
- 점수는 계산하지 않습니다. 근거 문장(evidence)만 작성하세요.
- 금리는 수익성 핵심 지표이므로 반드시 포함하세요.
- LTV는 손실 익스포저를 나타내므로 반드시 포함하세요.
- 캡티브 강도는 진입 난이도와 직결됩니다.
- null 값은 "공식 데이터 미확보"로 명시하세요.

응답 형식 (JSON):
{
  "evidences": {"<catalog_item_id>": "<근거 문장>"},
  "warnings": ["<경고>"]
}"""


class EnvironmentAgent(BaseAgent):

    async def analyze(
        self,
        target_country: str,
        compared_country: str,
        ruleset_id: str = "default",
        ws_broadcaster: Callable | None = None,
    ) -> AgentResult:

        async def _broadcast(progress: int, message: str, status: str = "running") -> None:
            if ws_broadcaster:
                await ws_broadcaster("environment", progress, status, message)

        await _broadcast(0, "금융환경 데이터 수집 시작")

        try:
            catalog, target_items, baseline_items = await collect_category_data(
                target_country, compared_country, _CATEGORY_ID
            )

            await _broadcast(30, "데이터 로드 완료, LLM 근거 생성 시작")

            parsed = await generate_evidence(
                self, _SYSTEM_PROMPT, target_country, compared_country,
                catalog, target_items, baseline_items,
                extra_instruction="금리·LTV·캡티브 강도를 우선 다루세요.",
            )
            evidences = parsed.get("evidences", {})
            warnings = list(parsed.get("warnings", []))

            await _broadcast(80, "근거 문장 생성 완료, 점수 계산 중")

            items, cat_score = build_item_scores(
                catalog, target_items, baseline_items, evidences, "ENVIRONMENT"
            )
            if cat_score.coverage == 0.0:
                warnings.append(f"{target_country}/{compared_country} 금융환경 데이터 미확보")

            await _broadcast(100, "금융환경 분석 완료")

            return AgentResult(
                category="FINANCIAL",
                items=items,
                category_score=cat_score.raw_score,
                coverage=cat_score.coverage,
                warnings=warnings,
            )

        except Exception as e:
            if ws_broadcaster:
                await ws_broadcaster("environment", 0, "error", str(e))
            return AgentResult(category="FINANCIAL", warnings=[f"EnvironmentAgent 오류: {e}"])
