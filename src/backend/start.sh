#!/bin/bash
# 백엔드 실행 스크립트 — 프로덕션 환경

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENV_FILE="${SCRIPT_DIR}/../../.env"

if [ -f "$ENV_FILE" ]; then
  set -a
  source "$ENV_FILE"
  set +a
fi

cd "$SCRIPT_DIR"

exec uvicorn main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 2 \
  --log-level info
