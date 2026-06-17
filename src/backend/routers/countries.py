from __future__ import annotations

from fastapi import APIRouter, HTTPException
from db.loaders import load_countries_async, load_country
from db.transformers import COUNTRY_ISO_MAP, to_name

router = APIRouter()


def _iso_of(c: dict) -> str | None:
    return c.get("country_id") or c.get("country_code") or COUNTRY_ISO_MAP.get(c.get("name", ""))


@router.get("")
async def list_countries():
    countries = await load_countries_async()
    return {
        "countries": [
            {
                "name": c["name"],
                "country_id": _iso_of(c),
                "country_code": _iso_of(c),
                "region": c.get("region"),
                "entry_status": c.get("entry_status"),
            }
            for c in countries.values()
        ]
    }


@router.get("/{country_id}")
async def get_country(country_id: str):
    # ISO 코드 또는 한국어명 모두 수용
    c = load_country(country_id) or load_country(to_name(country_id))
    if c is None:
        raise HTTPException(status_code=404, detail=f"국가를 찾을 수 없습니다: {country_id}")
    c = dict(c)
    c["country_id"] = _iso_of(c)
    return c
