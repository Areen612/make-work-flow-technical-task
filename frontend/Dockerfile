# Start from a clean, reproducible Alpine base. The official Node images bundle
# a vulnerable npm toolchain even though npm is only needed during installation.
FROM alpine:3.24@sha256:28bd5fe8b56d1bd048e5babf5b10710ebe0bae67db86916198a6eec434943f8b

# Keep Node for Vite, but remove npm in the same layer after dependencies are
# installed so npm's build-only packages are absent from the resulting image.
RUN apk add --no-cache nodejs npm

WORKDIR /app

# Copy dependency files first for better Docker caching.
COPY package.json package-lock.json ./

RUN npm ci \
    && npm cache clean --force \
    && apk del npm

# Copy the frontend source code.
COPY . .

EXPOSE 5173

# Vite must listen outside localhost inside Docker. Run it directly because npm
# is intentionally not included in the final image.
CMD ["node", "node_modules/vite/bin/vite.js", "--host", "0.0.0.0", "--port", "5173"]
