from __future__ import annotations
from typing import Any
from pydantic import BaseModel, Field
from datetime import datetime


# ── 국가 ──────────────────────────────────────────────────────────────────────

class Country(BaseModel):
    name: str
    country_id: str | None = None     # ISO 3166-1 alpha-2 (KR, US, DE ...)
    name_en: str | None = None
    region: str | None = None
    entry_status: str | None = None   # 진출 / 진출예정 / 미진출
    country_code: str | None = None
    population: dict[str, Any] | None = None
    economy: dict[str, Any] | None = None
    automotive: dict[str, Any] | None = None
    extra: dict[str, Any] = Field(default_factory=dict)


# ── 가중치 룰셋 ────────────────────────────────────────────────────────────────

class CategoryWeight(BaseModel):
    market: float = 0.25
    regulation: float = 0.25
    environment: float = 0.20
    system: float = 0.30


class Thresholds(BaseModel):
    entry: float = 60.0          # TRANSPLANTABLE 기준
    system_gate: float = 50.0   # 시스템 게이트


class Ruleset(BaseModel):
    id: str
    name: str
    version: int = 1
    locked: bool = False
    weights: CategoryWeight = Field(default_factory=CategoryWeight)
    thresholds: Thresholds = Field(default_factory=Thresholds)
    killswitch_enabled: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ── 분석 작업 ──────────────────────────────────────────────────────────────────

class AgentProgress(BaseModel):
    agent: str
    progress: int = 0
    status: str = "pending"    # pending / running / completed / error
    message: str = ""


class AnalysisJob(BaseModel):
    id: str
    target_country: str
    compared_country: str
    ruleset_id: str = "default"
    status: str = "RUNNING"    # RUNNING / COMPLETED / FAILED
    agents: dict[str, AgentProgress] = Field(default_factory=dict)
    result_id: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# ── 분석 결과 ──────────────────────────────────────────────────────────────────

class ItemScore(BaseModel):
    catalog_item_id: str
    similarity: float | None = None   # None = 데이터 미확보
    confidence_grade: str = "LOW"
    source_tier: str = "TIER3"
    evidence: str = ""
    is_missing: bool = False


class CategoryResult(BaseModel):
    category: str
    items: list[ItemScore] = Field(default_factory=list)
    category_score: float | None = None
    coverage: float = 0.0
    gate_passed: bool | None = None
    killswitch_results: list[dict[str, Any]] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class SimilarityResult(BaseModel):
    id: str
    analysis_id: str
    target_country: str
    compared_country: str
    ruleset_id: str
    verdict: str    # TRANSPLANTABLE / DEEP_RESEARCH / BLOCKED / FAILED
    total_score: float | None = None
    category_results: list[CategoryResult] = Field(default_factory=list)
    cost_estimate: dict[str, Any] | None = None
    summary: str = ""
    ai_insight: str = ""
    human_review_flags: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ── 정식 스키마 모델 (03_db_schema.md) ────────────────────────────────────────

class CatalogCategory(BaseModel):
    category_id: str                  # MARKET / REGULATORY / FINANCIAL / SYSTEM
    name: str
    name_en: str = ""
    default_weight: float = 0.25
    is_gate: bool = False
    gate_threshold: float | None = None


class CatalogItem(BaseModel):
    catalog_item_id: str              # MKT_001, REG_001 ...
    category_id: str
    sub_category: str = ""
    name: str
    name_en: str = ""
    similarity_type: str              # CONTINUOUS / CATEGORICAL / BINARY / REFERENCE
    data_type: str                    # NUMBER / PERCENT / TEXT / CODE / DATE / MULTI / RANGE
    default_item_weight: float = 1.0
    is_killswitch: bool = False
    killswitch_rule: dict[str, Any] | None = None


class ResearchSnapshot(BaseModel):
    snapshot_id: str
    country_id: str
    survey_date: datetime | None = None
    data_kind: str = "CURRENT"        # ENTRY_PREP / CURRENT
    created_by: str = "agent"
    status: str = "CONFIRMED"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ResearchItem(BaseModel):
    item_id: str
    snapshot_id: str
    catalog_item_id: str
    value_raw: str | None = None
    value_normalized: Any = None
    is_missing: bool = False
    source_name: str | None = None
    source_url: str | None = None
    source_type: str | None = None
    source_tier: str = "TIER3"        # TIER1 / TIER2 / TIER3 / BLOCKED
    is_official: bool = False
    official_gap_flag: bool = False
    confidence_grade: str = "ESTIMATED"  # OFFICIAL / SEMI_OFFICIAL / ESTIMATED
    survey_date: datetime | None = None
    evidence: str | None = None
    condition: str | None = None


class EntryRecord(BaseModel):
    entry_id: str
    country_id: str
    prep_period_days: int | None = None
    prep_cost_usd: int | None = None
    cost_breakdown: dict[str, Any] | None = None
    system_info: dict[str, Any] | None = None
    scope: str | None = None
    note: str | None = None
    estimated: bool = True
