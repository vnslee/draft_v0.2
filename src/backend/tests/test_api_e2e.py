"""
API 엔드투엔드 테스트 (JSON 모드 — MongoDB 불필요)

검증 항목:
  - GET /countries 응답 구조
  - GET /countries/{name} 200/404
  - POST /analysis/run + GET /analysis/{id}/status
  - GET /settings/rulesets + 룰셋 CRUD + 잠금
  - GET /health
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from fastapi.testclient import TestClient

# MongoDB 연결 없이 실행되도록 connection.get_db() = None 강제
import db.connection as _conn
_conn._db = None
_conn._client = None

from main import app

client = TestClient(app)


class TestHealth:
    def test_health_ok(self):
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"


class TestCountries:
    def test_list_countries_returns_array(self):
        r = client.get("/countries")
        assert r.status_code == 200
        body = r.json()
        assert "countries" in body
        assert isinstance(body["countries"], list)
        assert len(body["countries"]) > 0

    def test_country_has_required_fields(self):
        r = client.get("/countries")
        first = r.json()["countries"][0]
        assert "name" in first
        assert "entry_status" in first

    def test_get_existing_country(self):
        r = client.get("/countries/한국")
        assert r.status_code == 200
        body = r.json()
        assert body["name"] == "한국"

    def test_get_nonexistent_country_404(self):
        r = client.get("/countries/존재하지않는국가")
        assert r.status_code == 404


class TestSettings:
    def test_list_rulesets(self):
        r = client.get("/settings/rulesets")
        assert r.status_code == 200
        body = r.json()
        assert "rulesets" in body
        rulesets = body["rulesets"]
        assert len(rulesets) >= 1

    def test_get_default_ruleset(self):
        r = client.get("/settings/rulesets/default")
        assert r.status_code == 200
        body = r.json()
        assert body["id"] == "default"
        assert "weights" in body

    def test_get_nonexistent_ruleset_404(self):
        r = client.get("/settings/rulesets/nonexistent_xyz")
        assert r.status_code == 404

    def test_create_ruleset(self):
        r = client.post("/settings/rulesets", json={
            "name": "테스트 룰셋",
            "weights": {"market": 0.30, "regulation": 0.30, "environment": 0.20, "system": 0.20},
            "thresholds": {"entry": 65.0, "system_gate": 55.0},
            "killswitch_enabled": True,
        })
        assert r.status_code == 200
        body = r.json()
        assert body["name"] == "테스트 룰셋"
        assert body["id"].startswith("ruleset_")
        return body["id"]

    def test_lock_ruleset(self):
        # 새 룰셋 생성
        create_r = client.post("/settings/rulesets", json={"name": "잠금 테스트 룰셋"})
        assert create_r.status_code == 200
        ruleset_id = create_r.json()["id"]

        # 잠금
        lock_r = client.post(f"/settings/rulesets/{ruleset_id}/lock")
        assert lock_r.status_code == 200
        assert lock_r.json()["locked"] is True

        # 잠긴 룰셋 수정 시도 → 409
        update_r = client.put(f"/settings/rulesets/{ruleset_id}", json={"name": "수정 시도"})
        assert update_r.status_code == 409


class TestAnalysis:
    def test_run_analysis_returns_id(self):
        r = client.post("/analysis/run", json={
            "target_country": "호주",
            "compared_country": "한국",
        })
        assert r.status_code == 200
        body = r.json()
        assert "analysis_id" in body
        assert body["status"] == "RUNNING"

    def test_get_analysis_status(self):
        # 분석 시작
        run_r = client.post("/analysis/run", json={
            "target_country": "호주",
            "compared_country": "한국",
        })
        analysis_id = run_r.json()["analysis_id"]

        # 상태 조회
        status_r = client.get(f"/analysis/{analysis_id}/status")
        assert status_r.status_code == 200
        body = status_r.json()
        assert body["analysis_id"] == analysis_id
        assert body["status"] in ("RUNNING", "COMPLETED", "FAILED")
        assert "agents" in body

    def test_get_nonexistent_analysis_404(self):
        r = client.get("/analysis/nonexistent_id_xyz")
        assert r.status_code == 404

    def test_agents_initialized(self):
        run_r = client.post("/analysis/run", json={
            "target_country": "미국",
            "compared_country": "한국",
        })
        analysis_id = run_r.json()["analysis_id"]

        r = client.get(f"/analysis/{analysis_id}")
        body = r.json()
        agents = body.get("agents", {})
        for expected_agent in ["market", "regulation", "environment", "system", "summary"]:
            assert expected_agent in agents


class TestReports:
    def test_list_reports_structure(self):
        r = client.get("/reports")
        assert r.status_code == 200
        body = r.json()
        assert "reports" in body
        assert isinstance(body["reports"], list)

    def test_get_nonexistent_report_404(self):
        r = client.get("/reports/nonexistent_report_xyz")
        assert r.status_code == 404
