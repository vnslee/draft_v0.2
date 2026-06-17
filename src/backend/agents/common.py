"""
common.py — Phase 1 에이전트 공통 헬퍼

catalog_item_id 기반 점수 산출 + LLM 근거 생성 로직을 공유한다.
각 에이전트는 카테고리 ID와 시스템 프롬프트만 다르고 흐름은 동일하다.
"""
from __future__ import annotations

import json
from typing import Any

from agents.base import BaseAgent, ItemScore
from core.similarity_engine import CategoryScore, ItemSimilarity, calculate_category_score, score_item
from db.loaders import load_catalog_items, load_research_items


async def collect_category_data(
    target_country: str,
    compared_country: str,
    category_id: str,
) -> tuple[list[dict], dict[str, dict], dict[str, dict]]:
    """카탈로그 + 양국 research_items 로드."""
    catalog = await load_catalog_items(category_id)
    target_items = await load_research_items(target_country, category_id)
    baseline_items = await load_research_items(compared_country, category_id)
    return catalog, target_items, baseline_items


def build_item_scores(
    catalog: list[dict],
    target_items: dict[str, dict],
    baseline_items: dict[str, dict],
    evidences: dict[str, str],
    category_label: str,
    *,
    include_reference: bool = False,
) -> tuple[list[ItemScore], CategoryScore]:
    """
    카탈로그를 순회하며 catalog_item_id 단위로 score_item 호출.
    REFERENCE 항목은 점수에서 제외(기본). null≠0 원칙은 score_item이 보장.
    """
    items: list[ItemScore] = []
    item_sims: list[ItemSimilarity] = []
    item_weights: list[float] = []

    for ci in catalog:
        cid = ci["catalog_item_id"]
        sim_type = ci["similarity_type"]
        if sim_type == "REFERENCE" and not include_reference:
            # 점수 미반영이지만 보고서용 ItemScore는 남김
            t_ri = target_items.get(cid, {})
            items.append(ItemScore(
                catalog_item_id=cid,
                similarity=None,
                confidence_grade=t_ri.get("confidence_grade", "LOW"),
                source_tier=t_ri.get("source_tier", "TIER3"),
                evidence=evidences.get(cid, ""),
                is_missing=True,
            ))
            continue

        t_ri = target_items.get(cid, {})
        b_ri = baseline_items.get(cid, {})
        t_val = None if t_ri.get("is_missing", True) else t_ri.get("value_normalized")
        b_val = None if b_ri.get("is_missing", True) else b_ri.get("value_normalized")

        sim = score_item(
            t_val,
            b_val,
            sim_type,
            confidence_grade=_grade_to_engine(t_ri.get("confidence_grade", "LOW")),
            catalog_item_id=cid,
        )
        items.append(ItemScore(
            catalog_item_id=cid,
            similarity=sim.similarity,
            confidence_grade=t_ri.get("confidence_grade", "LOW"),
            source_tier=t_ri.get("source_tier", "TIER3"),
            evidence=evidences.get(cid, ""),
            is_missing=sim.is_missing,
        ))
        item_sims.append(sim)
        item_weights.append(ci.get("default_item_weight", 1.0))

    cat_score = calculate_category_score(item_sims, item_weights=item_weights or None, category=category_label)
    return items, cat_score


def _grade_to_engine(grade: str) -> str:
    """research_item의 confidence_grade(OFFICIAL/SEMI_OFFICIAL/ESTIMATED) → 엔진 등급(HIGH/MEDIUM/LOW)."""
    return {
        "OFFICIAL": "HIGH",
        "SEMI_OFFICIAL": "MEDIUM",
        "ESTIMATED": "LOW",
        "HIGH": "HIGH",
        "MEDIUM": "MEDIUM",
        "LOW": "LOW",
    }.get(grade, "LOW")


def _summarize_items(catalog: list[dict], items: dict[str, dict]) -> list[dict]:
    """LLM 프롬프트용 간결한 항목 요약 (catalog_item_id + 이름 + 값)."""
    name_by_id = {c["catalog_item_id"]: c["name"] for c in catalog}
    out = []
    for cid, ri in items.items():
        if ri.get("is_missing"):
            continue
        out.append({
            "id": cid,
            "name": name_by_id.get(cid, cid),
            "value": ri.get("value_raw") or ri.get("value_normalized"),
            "source_tier": ri.get("source_tier"),
        })
    return out


async def generate_evidence(
    agent: BaseAgent,
    system_prompt: str,
    target_country: str,
    compared_country: str,
    catalog: list[dict],
    target_items: dict[str, dict],
    baseline_items: dict[str, dict],
    extra_instruction: str = "",
) -> dict[str, Any]:
    """Haiku로 항목별 근거 문장 생성. catalog_item_id를 키로 하는 evidences 반환."""
    messages = [
        {
            "role": "user",
            "content": (
                f"대상국: {target_country}, 기준국: {compared_country}\n\n"
                f"[대상국 항목]\n{json.dumps(_summarize_items(catalog, target_items), ensure_ascii=False, indent=2)}\n\n"
                f"[기준국 항목]\n{json.dumps(_summarize_items(catalog, baseline_items), ensure_ascii=False, indent=2)}\n\n"
                f"각 항목(catalog_item_id 기준)의 근거 문장을 JSON으로 작성하세요. {extra_instruction}"
            ),
        }
    ]
    try:
        response = await agent._call_haiku(system_prompt, messages)
        text = agent._extract_text(response)
        start, end = text.find("{"), text.rfind("}") + 1
        if start >= 0 and end > start:
            return json.loads(text[start:end])
    except Exception:
        pass
    return {"evidences": {}, "warnings": ["LLM 응답 파싱 실패 또는 호출 실패"]}
