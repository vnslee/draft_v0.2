from __future__ import annotations

from fastapi import APIRouter, HTTPException
from db.loaders import get_result, list_results, save_result
from db.models import SimilarityResult

router = APIRouter()

# 인메모리 폴백 (loaders._memory_results와 병행)
_reports: dict[str, SimilarityResult] = {}


async def save_report(result: SimilarityResult) -> None:
    _reports[result.id] = result
    await save_result(result.model_dump())


@router.get("/{result_id}")
async def get_report(result_id: str):
    doc = await get_result(result_id)
    if doc is None:
        report = _reports.get(result_id)
        if report is None:
            raise HTTPException(status_code=404, detail=f"보고서를 찾을 수 없습니다: {result_id}")
        return report.model_dump()
    return doc


@router.get("")
async def list_reports_endpoint(limit: int = 20):
    docs = await list_results(limit)
    if docs:
        return {
            "reports": [
                {
                    "id": r.get("id"),
                    "target_country": r.get("target_country"),
                    "compared_country": r.get("compared_country"),
                    "verdict": r.get("verdict"),
                    "total_score": r.get("total_score"),
                    "created_at": r.get("created_at").isoformat()
                    if isinstance(r.get("created_at"), __import__("datetime").datetime)
                    else r.get("created_at"),
                }
                for r in docs
            ]
        }
    # 인메모리 폴백
    items = sorted(_reports.values(), key=lambda r: r.created_at, reverse=True)[:limit]
    return {
        "reports": [
            {
                "id": r.id,
                "target_country": r.target_country,
                "compared_country": r.compared_country,
                "verdict": r.verdict,
                "total_score": r.total_score,
                "created_at": r.created_at.isoformat(),
            }
            for r in items
        ]
    }
