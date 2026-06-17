"""
seed.py — JSON 목업 데이터를 정식 스키마(03_db_schema.md)로 MongoDB에 적재

사용법:
    cd src/backend
    MONGODB_URI=mongodb://localhost:27017 python -m db.seed

적재 순서:
    catalog_categories   — catalog_seed.CATALOG_CATEGORIES (4)
    catalog_items        — catalog_seed.CATALOG_ITEMS (69)
    countries            — countries.json + ISO 코드 보강 (12)
    entry_records        — entry_baseline.json baselines 변환 (7)
    weight_rulesets      — catalog_seed.DEFAULT_RULESET (1)
    research_snapshots   — 국가당 1 CURRENT 스냅샷
    research_items       — transformers 변환 결과 (~수백건)
    baseline_multipliers — multiplier_table (1)

멱등성: 각 컬렉션 drop 후 재삽입 (개발 환경 전용).
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import motor.motor_asyncio

from db import transformers as T
from db.catalog_seed import CATALOG_CATEGORIES, CATALOG_ITEMS, DEFAULT_RULESET

_HERE = Path(__file__).resolve().parent
# 컨테이너에서는 백엔드가 /app 로 평탄화되어 parents[2]가 없을 수 있다.
# DATA_DIR env > repo 루트(../../../data) > /data 순으로 해석.
if os.getenv("DATA_DIR"):
    _DATA = Path(os.environ["DATA_DIR"]).resolve()
elif len(_HERE.parents) >= 3 and (_HERE.parents[2] / "data").is_dir():
    _DATA = _HERE.parents[2] / "data"
else:
    _DATA = Path("/data")

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGODB_DB", "auto_finance")


def _read(rel: str) -> dict:
    with open(_DATA / rel, encoding="utf-8") as f:
        return json.load(f)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _build_countries() -> list[dict]:
    """countries.json + ISO 코드 보강."""
    raw = _read("countries/countries.json")
    out = []
    for c in raw.get("countries", []):
        iso = T.COUNTRY_ISO_MAP.get(c["name"])
        out.append({
            **c,
            "country_id": iso,
            "country_code": iso,
            "seeded_at": _now(),
        })
    return out


def _build_entry_records() -> list[dict]:
    raw = _read("baseline/entry_baseline.json")
    return [T.transform_entry_record(b) for b in raw.get("baselines", [])]


def _build_research(country_iso: str, name: str) -> tuple[dict | None, list[dict]]:
    """국가 1개의 snapshot + research_items 생성. 데이터 없으면 (None, [])."""
    snapshot_id = f"{country_iso}_CURRENT"
    by_id: dict[str, dict] = {}

    def absorb(items: list[dict]) -> None:
        for it in items:
            cid = it["catalog_item_id"]
            existing = by_id.get(cid)
            if existing is None or (existing.get("is_missing") and not it.get("is_missing")):
                by_id[cid] = it

    markets = {m["country_code"]: m for m in _read("auto_finance_market/auto_finance_market.json").get("markets", [])}
    segments = {s["country_code"]: s for s in _read("customer_segment/customer_segment.json").get("segments", [])}
    regs = {r["country_code"]: r for r in _read("regulations/auto_finance_regulation.json").get("regulations", [])}
    lics = {l["country_code"]: l for l in _read("regulations/capital_license.json").get("licenses", [])}
    procs = {p["country_code"]: p for p in _read("purchase_process/purchase_process.json").get("processes", [])}

    if country_iso in markets:
        absorb(T.transform_market_data(markets[country_iso], snapshot_id))
    if country_iso in segments:
        absorb(T.transform_segment_data(segments[country_iso], snapshot_id))
    if country_iso in regs:
        absorb(T.transform_regulation_data(regs[country_iso], snapshot_id))
    if country_iso in lics:
        absorb(T.transform_license_data(lics[country_iso], snapshot_id))
    if country_iso in procs:
        absorb(T.transform_purchase_process(procs[country_iso], snapshot_id))

    # 킬스위치 목업 보강
    ks_items = T._apply_killswitch_mockup(
        [by_id[c] for c in ("REG_001", "REG_002", "REG_003", "REG_004", "REG_005") if c in by_id],
        country_iso, snapshot_id,
    )
    for it in ks_items:
        by_id[it["catalog_item_id"]] = it

    has_real_data = any(not v.get("is_missing") for v in by_id.values())

    # 전 카탈로그 항목을 is_missing으로 채움
    for ci in CATALOG_ITEMS:
        cid = ci["catalog_item_id"]
        if cid not in by_id:
            by_id[cid] = T._missing_item(snapshot_id, cid)

    if not has_real_data:
        return None, []

    snapshot = {
        "snapshot_id": snapshot_id,
        "country_id": country_iso,
        "survey_date": _now(),
        "data_kind": "CURRENT",
        "created_by": "seed",
        "status": "CONFIRMED",
        "created_at": _now(),
    }
    items = list(by_id.values())
    for it in items:
        it["survey_date"] = _now()
    return snapshot, items


async def seed(drop: bool = True) -> None:
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
    db = client[DB_NAME]

    async def load_collection(name: str, docs: list[dict], key: str | None = None) -> None:
        if not docs:
            print(f"  [SKIP] {name} — 데이터 없음")
            return
        col = db[name]
        if drop:
            await col.drop()
        await col.insert_many([dict(d) for d in docs])
        print(f"  [OK]   {name:22s} {len(docs):>4}건")

    # 1. catalog_categories
    await load_collection("catalog_categories", CATALOG_CATEGORIES)
    # 2. catalog_items
    await load_collection("catalog_items", CATALOG_ITEMS)
    # 3. countries (ISO 보강)
    countries = _build_countries()
    await load_collection("countries", countries)
    # 4. entry_records
    await load_collection("entry_records", _build_entry_records())
    # 5. weight_rulesets (rulesets 이름 유지 — 라우터 호환)
    ruleset = dict(DEFAULT_RULESET)
    ruleset["created_at"] = _now()
    await load_collection("rulesets", [ruleset])
    # 6+7. research_snapshots + research_items
    snapshots: list[dict] = []
    all_items: list[dict] = []
    for c in countries:
        iso = c.get("country_id")
        if not iso:
            continue
        snap, items = _build_research(iso, c["name"])
        if snap:
            snapshots.append(snap)
            all_items.extend(items)
    await load_collection("research_snapshots", snapshots)
    await load_collection("research_items", all_items)
    # 8. baseline_multipliers
    raw_baseline = _read("baseline/entry_baseline.json")
    await load_collection(
        "baseline_multipliers",
        [{"_id": "default", "table": raw_baseline.get("multiplier_table", {})}],
    )

    total = len(CATALOG_CATEGORIES) + len(CATALOG_ITEMS) + len(countries) + len(snapshots) + len(all_items)
    print(f"\n총 {total}건+ 적재 완료 → {MONGODB_URI}/{DB_NAME}")
    print(f"  (research_items {len(all_items)}건, snapshots {len(snapshots)}개국)")
    client.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="JSON 목업 → 정식 스키마 MongoDB 시딩")
    parser.add_argument("--no-drop", action="store_true", help="컬렉션 drop 없이 삽입")
    args = parser.parse_args()

    print(f"MongoDB: {MONGODB_URI}/{DB_NAME}")
    print(f"모드: {'append' if args.no_drop else 'drop & reload'}\n")
    asyncio.run(seed(drop=not args.no_drop))


if __name__ == "__main__":
    main()
