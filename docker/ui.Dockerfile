# Generic SPA build (Vite/React) -> Nginx static

ARG NODE_IMAGE=node:20-alpine
ARG FRONTEND_DIR=frontend
FROM ${NODE_IMAGE} AS build
ARG FRONTEND_DIR
WORKDIR /app

# Build args/env for API base
ARG API_BASE_URL
ENV VITE_API_BASE_URL=${API_BASE_URL}
ENV NEXT_PUBLIC_API_BASE_URL=${API_BASE_URL}

COPY ${FRONTEND_DIR}/package*.json ./
RUN npm ci --no-audit --no-fund
COPY ${FRONTEND_DIR}/ .
RUN npm run build

FROM nginx:alpine
ARG FRONTEND_DIR
COPY docker/ui-nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
