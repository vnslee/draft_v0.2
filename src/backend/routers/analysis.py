from __future__ import annotations

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel

from db.loaders import get_analysis, save_analysis
from db.models import AgentProgress, AnalysisJob

router = APIRouter()

# 인메모리 폴백 (MongoDB 미연결 시 loaders._memory_analyses 사용)
_jobs: dict[str, AnalysisJob] = {}


class RunRequest(BaseModel):
    target_country: str
    compared_country: str
    ruleset_id: str = "default"


@router.post("/run")
async def run_analysis(body: RunRequest, background_tasks: BackgroundTasks):
    analysis_id = f"analysis_{uuid.uuid4().hex[:12]}"

    job = AnalysisJob(
        id=analysis_id,
        target_country=body.target_country,
        compared_country=body.compared_country,
        ruleset_id=body.ruleset_id,
        status="RUNNING",
        agents={
            agent: AgentProgress(agent=agent)
            for agent in ["market", "regulation", "environment", "system", "summary"]
        },
    )
    _jobs[analysis_id] = job
    await save_analysis(job.model_dump())

    background_tasks.add_task(_run_orchestrator, analysis_id)
    return {"analysis_id": analysis_id, "status": "RUNNING"}


@router.get("/{analysis_id}")
async def get_analysis_endpoint(analysis_id: str):
    # 라이브 진행 상태(_jobs) 우선, 영속 저장소(DB/JSON) 폴백
    job = _jobs.get(analysis_id)
    if job is not None:
        return job.model_dump()
    doc = await get_analysis(analysis_id)
    if doc is None:
        raise HTTPException(status_code=404, detail=f"분석을 찾을 수 없습니다: {analysis_id}")
    return doc


@router.get("/{analysis_id}/status")
async def get_analysis_status(analysis_id: str):
    """WebSocket 폴백용 5초 폴링 엔드포인트"""
    # 라이브 진행 상태(_jobs) 우선, 영속 저장소(DB/JSON) 폴백
    job = _jobs.get(analysis_id)
    if job is not None:
        doc = job.model_dump()
    else:
        doc = await get_analysis(analysis_id)
        if doc is None:
            raise HTTPException(status_code=404, detail=f"분석을 찾을 수 없습니다: {analysis_id}")
    return {
        "analysis_id": analysis_id,
        "status": doc.get("status"),
        "agents": doc.get("agents", {}),
        "result_id": doc.get("result_id"),
        "updated_at": doc.get("updated_at", datetime.now(timezone.utc)).isoformat()
        if isinstance(doc.get("updated_at"), datetime)
        else doc.get("updated_at"),
    }


def update_job(analysis_id: str, **kwargs) -> None:
    job = _jobs.get(analysis_id)
    if job:
        updated = job.model_copy(update={**kwargs, "updated_at": datetime.now(timezone.utc)})
        _jobs[analysis_id] = updated


def update_agent_progress(analysis_id: str, agent: str, progress: int, status: str, message: str = "") -> None:
    job = _jobs.get(analysis_id)
    if job:
        agents = dict(job.agents)
        agents[agent] = AgentProgress(agent=agent, progress=progress, status=status, message=message)
        _jobs[analysis_id] = job.model_copy(update={
            "agents": agents,
            "updated_at": datetime.now(timezone.utc),
        })


async def _run_orchestrator(analysis_id: str) -> None:
    try:
        from agents.orchestrator import run_analysis
        await run_analysis(analysis_id)
    except Exception as e:
        update_job(analysis_id, status="FAILED")
        from ws.progress import broadcast_error
        await broadcast_error(analysis_id, "orchestrator", str(e), recoverable=False)
