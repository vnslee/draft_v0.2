"""
connection.py — MongoDB 비동기 연결 싱글턴

FastAPI 앱 시작 시 init_db()를 호출하고, 종료 시 close_db()를 호출한다.
MONGODB_URI 미설정 시 JSON 모드(loaders.py 자동 폴백)로 동작하므로 연결 실패가 앱을 중단하지 않는다.
"""
from __future__ import annotations

import logging

import motor.motor_asyncio
from pymongo import ASCENDING, DESCENDING

from config import settings

logger = logging.getLogger(__name__)

_client: motor.motor_asyncio.AsyncIOMotorClient | None = None
_db: motor.motor_asyncio.AsyncIOMotorDatabase | None = None


def get_db() -> motor.motor_asyncio.AsyncIOMotorDatabase | None:
    return _db


async def init_db() -> bool:
    """MongoDB 연결 초기화. 성공 시 True, 실패(혹은 URI 미설정) 시 False."""
    global _client, _db

    uri = settings.mongodb_uri
    if not uri or uri == "mongodb://localhost:27017" and not _is_reachable(uri):
        logger.info("MongoDB URI 미설정 또는 연결 불가 — JSON 모드로 동작")
        return False

    try:
        _client = motor.motor_asyncio.AsyncIOMotorClient(
            uri,
            serverSelectionTimeoutMS=3000,
        )
        # 실제 연결 확인
        await _client.admin.command("ping")
        _db = _client[settings.mongodb_db]
        await _ensure_indexes(_db)
        logger.info("MongoDB 연결 성공: %s / %s", uri, settings.mongodb_db)
        return True
    except Exception as exc:
        logger.warning("MongoDB 연결 실패 (%s) — JSON 모드로 폴백", exc)
        _client = None
        _db = None
        return False


async def close_db() -> None:
    global _client, _db
    if _client:
        _client.close()
        _client = None
        _db = None
        logger.info("MongoDB 연결 종료")


def _is_reachable(uri: str) -> bool:
    """로컬 소켓 연결 가능 여부 빠른 확인 (sync, 타임아웃 1s)."""
    import socket
    from urllib.parse import urlparse

    try:
        parsed = urlparse(uri)
        host = parsed.hostname or "localhost"
        port = parsed.port or 27017
        with socket.create_connection((host, port), timeout=1):
            return True
    except OSError:
        return False


async def _ensure_indexes(db: motor.motor_asyncio.AsyncIOMotorDatabase) -> None:
    # 정식 스키마 (03_db_schema.md)
    await db.countries.create_index([("country_id", ASCENDING)], unique=True, sparse=True, background=True)
    await db.catalog_categories.create_index([("category_id", ASCENDING)], unique=True, background=True)
    await db.catalog_items.create_index([("catalog_item_id", ASCENDING)], unique=True, background=True)
    await db.catalog_items.create_index([("category_id", ASCENDING)], background=True)
    await db.research_snapshots.create_index([("country_id", ASCENDING), ("survey_date", DESCENDING)], background=True)
    await db.research_items.create_index([("snapshot_id", ASCENDING)], background=True)
    await db.research_items.create_index([("catalog_item_id", ASCENDING)], background=True)
    await db.entry_records.create_index([("country_id", ASCENDING)], unique=True, background=True)
    # 운영
    await db.rulesets.create_index([("id", ASCENDING)], unique=True, background=True)
    await db.analyses.create_index([("id", ASCENDING)], unique=True, background=True)
    await db.results.create_index([("analysis_id", ASCENDING)], background=True)
