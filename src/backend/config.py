from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    anthropic_api_key: str = ""
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db: str = "auto_finance"

    # CORS 허용 오리진 (쉼표 구분). 운영 배포 시 ALB/도메인 주소를 env로 주입.
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    # 데이터 경로 (JSON 모드)
    data_dir: str = "../../data"

    # ── LLM 제공자 (AWS Bedrock 경유) ──────────────────────────────
    # AWS_BEARER_TOKEN_BEDROCK 환경변수로 인증. 미설정 시 목업 폴백.
    aws_region: str = "ap-northeast-2"
    aws_bearer_token_bedrock: str = ""

    # Claude 모델 — Bedrock inference profile ID (서울 리전 활성 모델)
    # Haiku 역할(병렬 분석) / Sonnet 역할(요약·보고서)
    haiku_model: str = "apac.anthropic.claude-3-haiku-20240307-v1:0"
    sonnet_model: str = "apac.anthropic.claude-sonnet-4-20250514-v1:0"


settings = Settings()
