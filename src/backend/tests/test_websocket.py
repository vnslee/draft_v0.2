"""
WebSocket 연결 / 메시지 수신 / 폴백 테스트
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import json
import pytest
import db.connection as _conn
_conn._db = None
_conn._client = None

from fastapi.testclient import TestClient
from main import app
from ws.progress import broadcast_completed, broadcast_error, broadcast_progress, ws_manager

client = TestClient(app)


class TestWebSocketConnection:
    def test_websocket_connects(self):
        with client.websocket_connect("/ws/analysis/test_analysis_001") as ws:
            # 연결만 확인 — 데이터 없이도 accept 돼야 함
            assert ws is not None

    def test_websocket_receives_broadcast(self):
        import asyncio

        analysis_id = "test_ws_broadcast_001"
        received = []

        with client.websocket_connect(f"/ws/analysis/{analysis_id}") as ws:
            # 브로드캐스트 발송 (동기 컨텍스트에서 실행)
            asyncio.get_event_loop().run_until_complete(
                broadcast_progress(analysis_id, "market", 50, "running", "데이터 수집 중")
            )
            msg = ws.receive_text()
            received.append(json.loads(msg))

        assert len(received) == 1
        assert received[0]["type"] == "progress"
        assert received[0]["agent"] == "market"
        assert received[0]["progress"] == 50
        assert received[0]["status"] == "running"

    def test_websocket_receives_completed(self):
        import asyncio

        analysis_id = "test_ws_completed_001"
        with client.websocket_connect(f"/ws/analysis/{analysis_id}") as ws:
            asyncio.get_event_loop().run_until_complete(
                broadcast_completed(analysis_id, "result_xyz", "TRANSPLANTABLE", 72.5)
            )
            msg = ws.receive_text()
            data = json.loads(msg)

        assert data["type"] == "completed"
        assert data["verdict"] == "TRANSPLANTABLE"
        assert data["result_id"] == "result_xyz"
        assert data["total_score"] == pytest.approx(72.5)

    def test_websocket_receives_error(self):
        import asyncio

        analysis_id = "test_ws_error_001"
        with client.websocket_connect(f"/ws/analysis/{analysis_id}") as ws:
            asyncio.get_event_loop().run_until_complete(
                broadcast_error(analysis_id, "market", "연결 오류", recoverable=True)
            )
            msg = ws.receive_text()
            data = json.loads(msg)

        assert data["type"] == "error"
        assert data["agent"] == "market"
        assert data["recoverable"] is True


class TestWebSocketFallback:
    """WebSocket 불가 시 폴링 엔드포인트 폴백 테스트"""

    def test_polling_endpoint_returns_status(self):
        # 분석 시작
        run_r = client.post("/analysis/run", json={
            "target_country": "호주",
            "compared_country": "한국",
        })
        assert run_r.status_code == 200
        analysis_id = run_r.json()["analysis_id"]

        # 5초 폴링 엔드포인트
        poll_r = client.get(f"/analysis/{analysis_id}/status")
        assert poll_r.status_code == 200
        body = poll_r.json()
        assert body["analysis_id"] == analysis_id
        assert "status" in body
        assert "agents" in body
        assert "updated_at" in body

    def test_polling_reflects_all_agents(self):
        run_r = client.post("/analysis/run", json={
            "target_country": "미국",
            "compared_country": "한국",
        })
        analysis_id = run_r.json()["analysis_id"]

        poll_r = client.get(f"/analysis/{analysis_id}/status")
        body = poll_r.json()
        agents = body["agents"]
        for agent_name in ["market", "regulation", "environment", "system", "summary"]:
            assert agent_name in agents
