from __future__ import annotations

import uuid

from fastapi import APIRouter, HTTPException
from db.loaders import list_rulesets, load_ruleset, save_ruleset
from db.models import CategoryWeight, Ruleset, Thresholds

router = APIRouter()


@router.get("/rulesets")
async def list_rulesets_endpoint():
    rulesets = await list_rulesets()
    return {"rulesets": rulesets}


@router.get("/rulesets/{ruleset_id}")
async def get_ruleset(ruleset_id: str):
    ruleset = await load_ruleset(ruleset_id)
    if ruleset is None:
        raise HTTPException(status_code=404, detail=f"룰셋을 찾을 수 없습니다: {ruleset_id}")
    return ruleset


@router.post("/rulesets")
async def create_ruleset(body: dict):
    ruleset_id = f"ruleset_{uuid.uuid4().hex[:8]}"
    ruleset = Ruleset(
        id=ruleset_id,
        name=body.get("name", "새 룰셋"),
        weights=CategoryWeight(**body.get("weights", {})),
        thresholds=Thresholds(**body.get("thresholds", {})),
        killswitch_enabled=body.get("killswitch_enabled", True),
    )
    await save_ruleset(ruleset.model_dump())
    return ruleset.model_dump()


@router.put("/rulesets/{ruleset_id}")
async def update_ruleset(ruleset_id: str, body: dict):
    existing_raw = await load_ruleset(ruleset_id)
    if existing_raw is None:
        raise HTTPException(status_code=404, detail=f"룰셋을 찾을 수 없습니다: {ruleset_id}")

    existing = Ruleset(**existing_raw)
    if existing.locked:
        raise HTTPException(status_code=409, detail="잠긴 룰셋은 수정할 수 없습니다. 새 버전을 생성하세요.")

    updated = existing.model_copy(update={
        "name": body.get("name", existing.name),
        "weights": CategoryWeight(**body["weights"]) if "weights" in body else existing.weights,
        "thresholds": Thresholds(**body["thresholds"]) if "thresholds" in body else existing.thresholds,
        "killswitch_enabled": body.get("killswitch_enabled", existing.killswitch_enabled),
    })
    await save_ruleset(updated.model_dump())
    return updated.model_dump()


@router.post("/rulesets/{ruleset_id}/lock")
async def lock_ruleset(ruleset_id: str):
    existing_raw = await load_ruleset(ruleset_id)
    if existing_raw is None:
        raise HTTPException(status_code=404, detail=f"룰셋을 찾을 수 없습니다: {ruleset_id}")
    existing = Ruleset(**existing_raw)
    locked = existing.model_copy(update={"locked": True})
    await save_ruleset(locked.model_dump())
    return {"locked": True, "ruleset_id": ruleset_id}
