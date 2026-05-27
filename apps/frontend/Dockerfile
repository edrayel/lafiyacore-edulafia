FROM node:20-alpine AS builder
WORKDIR /app

ARG VITE_API_URL
ARG VITE_APP_NAME
ENV VITE_API_URL=$VITE_API_URL
ENV VITE_APP_NAME=$VITE_APP_NAME

COPY . .
RUN corepack enable && pnpm install --frozen-lockfile
RUN pnpm --filter frontend build

FROM nginxinc/nginx-unprivileged:alpine AS runtime
COPY --from=builder /app/apps/frontend/dist /usr/share/nginx/html
COPY apps/frontend/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]