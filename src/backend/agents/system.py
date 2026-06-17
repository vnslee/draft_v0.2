"""SystemAgent — 시스템 카테고리 분석 (가중치 30%) + 시스템 게이트"""
from __future__ import annotations

import json
from typing import Callable

from agents.base import AgentResult, BaseAgent
from agents.common import build_item_scores, collect_category_data

_CATEGORY_ID = "SYSTEM"
_SYSTEM_GATE_THRESHOLD = 50.0

_SYSTEM_PROMPT = """당신은 오토금융 IT·시스템 환경 분석 전문가입니다.
두 국가의 시스템 환경(핵심 솔루션, 디지털 채널 성숙도, 결제 인프라 등)을 비교하고 근거 문장을 작성하세요.

규칙:
- 점수는 계산하지 않습니다. 근거 문장(evidence)만 작성하세요.
- 코어시스템 벤더 락인 여부는 연동 비용에 직결되므로 반드시 분석하세요.
- 디지털 채널 성숙도(앱·온라인 금융 비중)를 포함하세요.
- null 값은 "공식 데이터 미확보"로 명시하세요.

응답 형식 (JSON):
{
  "evidences": {"<catalog_item_id>": "<근거 문장>"},
  "system_gate_risk": "LOW|MEDIUM|HIGH",
  "warnings": ["<경고>"]
}"""


class SystemAgent(BaseAgent):

    async def analyze(
        self,
        target_country: str,
        compared_country: str,
        ruleset_id: str = "default",
        ws_broadcaster: Callable | None = None,
    ) -> AgentResult:

        async def _broadcast(progress: int, message: str, status: str = "running") -> None:
            if ws_broadcaster:
                await ws_broadcaster("system", progress, status, message)

        await _broadcast(0, "시스템 데이터 수집 시작")

        try:
            catalog, target_items, baseline_items = await collect_category_data(
                target_country, compared_country, _CATEGORY_ID
            )

            await _broadcast(30, "데이터 로드 완료, LLM 근거 생성 시작")

            # 시스템 데이터는 대부분 미확보 → LLM 게이트 리스크 평가 포함
            from agents.common import _summarize_items
            messages = [
                {
                    "role": "user",
                    "content": (
                        f"대상국: {target_country}, 기준국: {compared_country}\n\n"
                        f"[대상국 시스템 항목]\n{json.dumps(_summarize_items(catalog, target_items), ensure_ascii=False, indent=2)}\n\n"
                        f"[기준국 시스템 항목]\n{json.dumps(_summarize_items(catalog, baseline_items), ensure_ascii=False, indent=2)}\n\n"
                        "솔루션사·벤더락인·디지털 성숙도 항목별 근거 문장과 system_gate_risk를 JSON으로 작성하세요."
                    ),
                }
            ]
            parsed: dict = {}
            try:
                response = await self._call_haiku(_SYSTEM_PROMPT, messages)
                text = self._extract_text(response)
                start, end = text.find("{"), text.rfind("}") + 1
                if start >= 0 and end > start:
                    parsed = json.loads(text[start:end])
            except Exception:
                parsed = {"warnings": ["LLM 응답 파싱 실패"]}

            evidences = parsed.get("evidences", {})
            warnings = list(parsed.get("warnings", []))
            gate_risk = parsed.get("system_gate_risk", "MEDIUM")

            await _broadcast(80, "근거 문장 생성 완료, 시스템 게이트 검증 중")

            items, cat_score = build_item_scores(
                catalog, target_items, baseline_items, evidences, "SYSTEM"
            )

            # 시스템 게이트 평가
            if cat_score.coverage < 0.3:
                gate_passed = gate_risk != "HIGH"
                warnings.append("SYSTEM 카테고리 데이터 미확보 — LLM 게이트 리스크 평가로 폴백")
                if not gate_passed:
                    warnings.append("시스템 게이트: LLM 평가 HIGH 리스크 — DEEP_RESEARCH 권고")
            else:
                gate_passed = cat_score.raw_score >= _SYSTEM_GATE_THRESHOLD

            await _broadcast(100, "시스템 분석 완료")

            return AgentResult(
                category="SYSTEM",
                items=items,
                category_score=cat_score.raw_score,
                coverage=cat_score.coverage,
                gate_passed=gate_passed,
                warnings=warnings,
            )

        except Exception as e:
            if ws_broadcaster:
                await ws_broadcaster("system", 0, "error", str(e))
            return AgentResult(category="SYSTEM", gate_passed=None, warnings=[f"SystemAgent 오류: {e}"])
