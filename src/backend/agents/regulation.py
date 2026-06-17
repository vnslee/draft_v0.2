"""RegulationAgent — 규제 카테고리 분석 (가중치 25%) + 킬스위치"""
from __future__ import annotations

import json
from typing import Callable

from agents.base import AgentResult, BaseAgent, KillswitchResult
from agents.common import build_item_scores, collect_category_data, generate_evidence

_CATEGORY_ID = "REGULATORY"

_SYSTEM_PROMPT = """당신은 오토금융 규제 분석 전문가입니다.
두 국가의 규제·인허가 데이터를 비교하고, 각 항목에 대한 근거 문장을 한국어로 작성하세요.

규칙:
- 점수는 계산하지 않습니다. 근거 문장(evidence)만 작성하세요.
- null 값은 "공식 데이터 미확보"로 명시하고, 추측하지 마세요.
- 킬스위치 항목(외국인 지분 한도, 외환 송금 규제 등)은 반드시 포함하세요.
- 조건부 규정("원칙 49%, JV 시 100% 가능" 등)은 human_review 항목으로 표시하세요.

응답 형식 (JSON):
{
  "evidences": {"<catalog_item_id>": "<근거 문장>"},
  "human_review_items": ["<조건부 또는 불명확한 항목 설명>"],
  "warnings": ["<경고>"]
}"""


def check_killswitch(catalog_item: dict, research_item: dict | None) -> KillswitchResult | None:
    """
    킬스위치 판정 — LLM이 아닌 코드에서 처리.
    값 미확보(value_normalized is None) → blocked=False + human_review (null ≠ 0, 전 국가 BLOCKED 방지).
    """
    rule = catalog_item.get("killswitch_rule")
    if not rule:
        return None

    cid = catalog_item["catalog_item_id"]
    value = None if (research_item is None or research_item.get("is_missing")) else research_item.get("value_normalized")

    # ── 최우선: 데이터 미확보 → 차단하지 않음 ──
    if value is None:
        return KillswitchResult(
            item_id=cid,
            blocked=False,
            value=None,
            threshold=rule.get("threshold"),
            reason="데이터 미확보 — 사람 검토 필요",
        )

    operator = rule.get("operator")
    threshold = rule.get("threshold")
    blocked = False
    try:
        if operator == "LT":
            blocked = float(value) < float(threshold)
        elif operator == "LTE":
            blocked = float(value) <= float(threshold)
        elif operator == "GT":
            blocked = float(value) > float(threshold)
        elif operator == "GTE":
            blocked = float(value) >= float(threshold)
        elif operator == "EQ":
            blocked = str(value).upper() == str(threshold).upper()
        elif operator == "NEQ":
            blocked = str(value).upper() != str(threshold).upper()
    except (ValueError, TypeError):
        # 값이 비교 불가 타입이면 차단하지 않고 검토 플래그
        return KillswitchResult(
            item_id=cid, blocked=False, value=value, threshold=threshold,
            reason="값 형식 불일치 — 사람 검토 필요",
        )

    return KillswitchResult(
        item_id=cid,
        blocked=blocked,
        value=value,
        threshold=threshold,
        reason=rule.get("block_message", "") if blocked else "",
    )


class RegulationAgent(BaseAgent):

    async def analyze(
        self,
        target_country: str,
        compared_country: str,
        ruleset_id: str = "default",
        ws_broadcaster: Callable | None = None,
    ) -> AgentResult:

        async def _broadcast(progress: int, message: str, status: str = "running") -> None:
            if ws_broadcaster:
                await ws_broadcaster("regulation", progress, status, message)

        await _broadcast(0, "규제 데이터 수집 시작")

        try:
            catalog, target_items, baseline_items = await collect_category_data(
                target_country, compared_country, _CATEGORY_ID
            )

            await _broadcast(30, "데이터 로드 완료, LLM 근거 생성 시작")

            parsed = await generate_evidence(
                self, _SYSTEM_PROMPT, target_country, compared_country,
                catalog, target_items, baseline_items,
                extra_instruction="킬스위치 항목과 조건부 규정을 명시하세요.",
            )
            evidences = parsed.get("evidences", {})
            warnings = list(parsed.get("warnings", []))
            human_review_flags = list(parsed.get("human_review_items", []))

            await _broadcast(80, "근거 문장 생성 완료, 킬스위치 검증 중")

            # 킬스위치 코드 검증 (대상국 기준)
            killswitch_results: list[KillswitchResult] = []
            for ci in catalog:
                if not ci.get("is_killswitch"):
                    continue
                cid = ci["catalog_item_id"]
                result = check_killswitch(ci, target_items.get(cid))
                if result:
                    killswitch_results.append(result)
                    if not result.blocked and result.reason:
                        human_review_flags.append(f"킬스위치 검토 필요: {ci['name']} ({result.reason})")

            items, cat_score = build_item_scores(
                catalog, target_items, baseline_items, evidences, "REGULATION"
            )
            if cat_score.coverage == 0.0:
                warnings.append(f"{target_country}/{compared_country} 규제 데이터 미확보")

            await _broadcast(100, "규제 분석 완료")

            return AgentResult(
                category="REGULATORY",
                items=items,
                category_score=cat_score.raw_score,
                coverage=cat_score.coverage,
                killswitch_results=killswitch_results,
                human_review_flags=human_review_flags,
                warnings=warnings,
            )

        except Exception as e:
            if ws_broadcaster:
                await ws_broadcaster("regulation", 0, "error", str(e))
            return AgentResult(category="REGULATORY", warnings=[f"RegulationAgent 오류: {e}"])
