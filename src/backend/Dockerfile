# 백엔드 이미지 — FastAPI + uvicorn (Bedrock 인증은 ECS Task Role 사용)
# !! 빌드 컨텍스트는 repo 루트여야 함 (data/ 디렉토리를 /data로 포함하기 위함) !!
#   docker build -f src/backend/Dockerfile -t auto-finance-backend .
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# 의존성 먼저 설치 (레이어 캐시)
COPY src/backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 + 데이터 + DocumentDB CA 번들
COPY src/backend /app
COPY data /data
COPY deploy/global-bundle.pem /app/global-bundle.pem

EXPOSE 8000

# loaders.py / db.seed 는 /app/db 기준 ../../../data == /data 를 읽는다.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2", "--log-level", "info"]
