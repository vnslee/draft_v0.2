"""오케스트레이터 — Phase 1 병렬 + Phase 2 순차"""
from __future__ import annotations

import asyncio

from agents.base import AgentResult
from agents.environment import EnvironmentAgent
from agents.market import MarketAgent
from agents.regulation import RegulationAgent
from agents.summary import SummaryAgent
from agents.system import SystemAgent
from db.models import Ruleset, CategoryWeight, Thresholds
from routers.analysis import update_agent_progress, update_job, _jobs
from routers.reports import save_report
from ws.progress import broadcast_completed, broadcast_error, broadcast_progress

_DEFAULT_RULESET = Ruleset(
    id="default",
    name="기본 룰셋 v1",
    version=1,
    locked=False,
    weights=CategoryWeight(),
    thresholds=Thresholds(),
)


async def _get_ruleset(ruleset_id: str) -> Ruleset:
    try:
        from db.loaders import load_ruleset
        raw = await load_ruleset(ruleset_id)
        if raw:
            return Ruleset(**raw)
    except Exception:
        pass
    return _DEFAULT_RULESET


def _make_broadcaster(analysis_id: str):
    async def broadcaster(agent: str, progress: int, status: str, message: str) -> None:
        update_agent_progress(analysis_id, agent, progress, status, message)
        await broadcast_progress(analysis_id, agent, progress, status, message)
    return broadcaster


async def run_analysis(analysis_id: str) -> None:
    job = _jobs.get(analysis_id)
    if job is None:
        return

    target = job.target_country
    compared = job.compared_country
    ruleset = await _get_ruleset(job.ruleset_id)
    broadcaster = _make_broadcaster(analysis_id)

    # ── Phase 1: 병렬 실행 ────────────────────────────────────────────────────
    agents = [
        MarketAgent(),
        RegulationAgent(),
        EnvironmentAgent(),
        SystemAgent(),
    ]

    async def run_agent(agent, name: str) -> AgentResult:
        try:
            return await agent.analyze(target, compared, job.ruleset_id, broadcaster)
        except Exception as e:
            await broadcast_error(analysis_id, name, str(e), recoverable=True)
            from agents.base import AgentResult as AR
            return AR(category=name.upper(), warnings=[f"{name} 실패: {e}"])

    phase1_tasks = [
        run_agent(agents[0], "market"),
        run_agent(agents[1], "regulation"),
        run_agent(agents[2], "environment"),
        run_agent(agents[3], "system"),
    ]

    phase1_results: list[AgentResult] = await asyncio.gather(*phase1_tasks)

    # 실패 판정: 2개 이상 핵심 실패
    failed_count = sum(
        1 for r in phase1_results
        if r.category_score is None and r.coverage == 0.0
    )
    if failed_count >= 2:
        update_job(analysis_id, status="FAILED")
        await broadcast_error(
            analysis_id, "orchestrator",
            f"Phase 1 에이전트 {failed_count}개 실패 — 분석 중단",
            recoverable=False,
        )
        return

    # ── Phase 2: SummaryAgent ─────────────────────────────────────────────────
    try:
        summary_agent = SummaryAgent()
        result = await summary_agent.synthesize(
            analysis_id=analysis_id,
            target_country=target,
            compared_country=compared,
            phase1_results=phase1_results,
            ruleset=ruleset,
            ws_broadcaster=broadcaster,
        )

        await save_report(result)
        update_job(analysis_id, status="COMPLETED", result_id=result.id)
        await broadcast_completed(
            analysis_id,
            result_id=result.id,
            verdict=result.verdict,
            total_score=result.total_score,
        )

    except Exception as e:
        update_job(analysis_id, status="FAILED")
        await broadcast_error(analysis_id, "summary", f"Summary 에이전트 실패: {e}", recoverable=False)
