"""
loaders.py — 데이터 로더 계층 (MVP: JSON 직접 읽기)

⚠️ 나중에 DB로 갈아끼울 유일한 곳.
   엔진(engine/decision)은 이 모듈의 함수 시그니처에만 의존한다.
   DB 전환 시: 아래 함수들의 본문만 DB 쿼리로 교체하고 반환 형태(dict/list)는 유지.

표준 반환 형태:
  - load_countries()     -> {country_name: country_dict}
  - load_dataset(name)   -> {country_name: country_record}  (데이터셋별 원본 구조 유지)
  - load_baseline()      -> {"baselines": {...}, "multiplier_table": {...}}
"""
from __future__ import annotations

import json
import os
from functools import lru_cache

# data 폴더 위치 (이 파일 기준 ../../data)
_HERE = os.path.dirname(os.path.abspath(__file__))
MOCKUP_DIR = os.path.normpath(os.path.join(_HERE, "..", "..", "data"))

# 비교 대상 데이터셋 → 파일 경로 + 국가 목록이 담긴 최상위 키
DATASET_FILES = {
    "regulation": ("regulations/auto_finance_regulation.json", "regulations"),
    "license": ("regulations/capital_license.json", "licenses"),
    "purchase": ("purchase_process/purchase_process.json", "processes"),
    # customer_segment 는 구조 추가분석 후 편입 예정 (design §11)
}


def _read_json(rel_path: str) -> dict:
    path = os.path.join(MOCKUP_DIR, rel_path)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@lru_cache(maxsize=None)
def load_countries() -> dict:
    """countries.json → {국가명: {region, entry_status, gdp, ...}}"""
    raw = _read_json("countries/countries.json")
    return {c["name"]: c for c in raw.get("countries", [])}


@lru_cache(maxsize=None)
def load_dataset(name: str) -> dict:
    """
    비교 데이터셋 로드 → {국가명: 국가레코드}
    국가레코드는 데이터셋별 원본 구조를 그대로 유지(엔진이 데이터셋별로 해석).
    """
    if name not in DATASET_FILES:
        raise ValueError(f"알 수 없는 데이터셋: {name} (가능: {list(DATASET_FILES)})")
    rel_path, list_key = DATASET_FILES[name]
    raw = _read_json(rel_path)
    return {rec["country"]: rec for rec in raw.get(list_key, [])}


@lru_cache(maxsize=None)
def load_baseline() -> dict:
    """entry_baseline.json → {baselines: {국가명: rec}, multiplier_table: {...}}"""
    raw = _read_json("baseline/entry_baseline.json")
    baselines = {b["country"]: b for b in raw.get("baselines", [])}
    return {
        "baselines": baselines,
        "multiplier_table": raw.get("multiplier_table", {}),
        "is_mockup": "MOCKUP" in str(raw.get("meta", {}).get("status", "")),
    }


def available_datasets() -> list[str]:
    return list(DATASET_FILES.keys())


def countries_in_dataset(name: str) -> list[str]:
    return list(load_dataset(name).keys())


def normalize_region(region: str | None) -> str | None:
    """권역 표기 변형을 통일 (design §6.4 안전장치)."""
    if not region:
        return None
    r = region.strip()
    aliases = {
        "아시아": "아시아 & 태평양",
        "아태": "아시아 & 태평양",
        "APAC": "아시아 & 태평양",
        "Asia": "아시아 & 태평양",
    }
    return aliases.get(r, r)


def get_region(country: str) -> str | None:
    c = load_countries().get(country)
    return normalize_region(c["region"]) if c else None


def get_entry_status(country: str) -> str | None:
    c = load_countries().get(country)
    return c.get("entry_status") if c else None


def entered_countries() -> list[str]:
    """진출 완료국 (baseline·기준국 후보)."""
    return [n for n, c in load_countries().items() if c.get("entry_status") == "진출"]


def candidate_countries() -> list[str]:
    """진출 예정국 (평가 대상)."""
    return [n for n, c in load_countries().items() if c.get("entry_status") == "진출예정"]
