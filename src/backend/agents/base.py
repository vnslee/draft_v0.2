"""에이전트 공통 인터페이스 및 데이터 클래스"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Callable

import anthropic

from config import settings


def build_bedrock_client() -> anthropic.AsyncAnthropicBedrock:
    """AWS Bedrock 경유 Claude 클라이언트.

    인증: AWS_BEARER_TOKEN_BEDROCK 환경변수(또는 settings). 미설정 시에도
    객체는 생성되며, 실제 호출 시점에 인증 오류가 발생한다(목업 폴백이 흡수).
    """
    if settings.aws_bearer_token_bedrock and not os.environ.get("AWS_BEARER_TOKEN_BEDROCK"):
        os.environ["AWS_BEARER_TOKEN_BEDROCK"] = settings.aws_bearer_token_bedrock
    return anthropic.AsyncAnthropicBedrock(aws_region=settings.aws_region)


def llm_enabled() -> bool:
    """Bedrock 인증 토큰이 있으면 True. 없으면 목업 모드."""
    return bool(settings.aws_bearer_token_bedrock or os.environ.get("AWS_BEARER_TOKEN_BEDROCK"))


@dataclass
class ItemScore:
    catalog_item_id: str
    similarity: float | None = None   # None = 비교 불가
    confidence_grade: str = "LOW"
    source_tier: str = "TIER3"
    evidence: str = ""
    is_missing: bool = False


@dataclass
class KillswitchResult:
    item_id: str
    blocked: bool
    value: Any = None
    threshold: Any = None
    reason: str = ""


@dataclass
class AgentResult:
    category: str          # MARKET | REGULATORY | FINANCIAL | SYSTEM
    items: list[ItemScore] = field(default_factory=list)
    category_score: float | None = None
    coverage: float = 0.0
    gate_passed: bool | None = None           # SYSTEM 에이전트만 사용
    killswitch_results: list[KillswitchResult] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    human_review_flags: list[str] = field(default_factory=list)
    raw_data: dict[str, Any] = field(default_factory=dict)


class BaseAgent:
    """모든 Phase 1 에이전트의 기반 클래스"""

    def __init__(self) -> None:
        self._client = build_bedrock_client()

    async def analyze(
        self,
        target_country: str,
        compared_country: str,
        ruleset_id: str,
        ws_broadcaster: Callable | None = None,
    ) -> AgentResult:
        raise NotImplementedError

    async def _call_haiku(
        self,
        system: str,
        messages: list[dict],
        tools: list[dict] | None = None,
        max_tokens: int = 2048,
    ) -> anthropic.types.Message:
        kwargs: dict[str, Any] = {
            "model": settings.haiku_model,
            "max_tokens": max_tokens,
            "system": system,
            "messages": messages,
        }
        if tools:
            kwargs["tools"] = tools
        return await self._client.messages.create(**kwargs)

    async def _call_sonnet(
        self,
        system: str,
        messages: list[dict],
        max_tokens: int = 4096,
    ) -> anthropic.types.Message:
        return await self._client.messages.create(
            model=settings.sonnet_model,
            max_tokens=max_tokens,
            system=system,
            messages=messages,
        )

    @staticmethod
    def _extract_text(message: anthropic.types.Message) -> str:
        for block in message.content:
            if block.type == "text":
                return block.text
        return ""

    @staticmethod
    def _extract_tool_use(message: anthropic.types.Message) -> list[dict]:
        return [
            {"name": b.name, "input": b.input, "id": b.id}
            for b in message.content
            if b.type == "tool_use"
        ]
