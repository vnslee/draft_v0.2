# 프론트엔드 이미지 — Vite 빌드 → nginx 정적 서빙
#   docker build -f src/frontend/Dockerfile -t auto-finance-frontend src/frontend
# /api·/ws 라우팅은 ALB가 담당하므로 이 컨테이너는 정적 파일 + SPA 폴백만 처리.
FROM node:20-slim AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
