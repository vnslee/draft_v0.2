#!/usr/bin/env bash
# ECR 리포 생성 + 백엔드/프론트 이미지 빌드 & 푸시
# 사용: deploy/build_and_push.sh [TAG]   (기본 TAG=v1)
set -euo pipefail

REGION="${AWS_REGION:-ap-northeast-2}"
ACCOUNT="$(aws sts get-caller-identity --query Account --output text)"
REGISTRY="${ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com"
TAG="${1:-v1}"
PLATFORM="linux/arm64"   # 빌드 호스트가 arm64 → Fargate도 ARM64(Graviton)로 실행 (에뮬레이션 회피)

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

BACKEND_REPO="auto-finance-backend"
FRONTEND_REPO="auto-finance-frontend"

echo "==> ECR 리포 보장"
for repo in "$BACKEND_REPO" "$FRONTEND_REPO"; do
  aws ecr describe-repositories --region "$REGION" --repository-names "$repo" >/dev/null 2>&1 \
    || aws ecr create-repository --region "$REGION" --repository-name "$repo" \
         --image-scanning-configuration scanOnPush=true >/dev/null
done

echo "==> ECR 로그인"
aws ecr get-login-password --region "$REGION" \
  | docker login --username AWS --password-stdin "$REGISTRY"

echo "==> 백엔드 빌드 (컨텍스트=repo 루트)"
docker build --platform "$PLATFORM" -f src/backend/Dockerfile \
  -t "${REGISTRY}/${BACKEND_REPO}:${TAG}" .
docker push "${REGISTRY}/${BACKEND_REPO}:${TAG}"

echo "==> 프론트 빌드 (컨텍스트=src/frontend)"
docker build --platform "$PLATFORM" -f src/frontend/Dockerfile \
  -t "${REGISTRY}/${FRONTEND_REPO}:${TAG}" src/frontend
docker push "${REGISTRY}/${FRONTEND_REPO}:${TAG}"

echo "==> 완료"
echo "BACKEND_IMAGE=${REGISTRY}/${BACKEND_REPO}:${TAG}"
echo "FRONTEND_IMAGE=${REGISTRY}/${FRONTEND_REPO}:${TAG}"
