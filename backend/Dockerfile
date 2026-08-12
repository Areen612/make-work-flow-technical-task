# Pin the vulnerability-free, multi-platform Python 3.12 Alpine image.
FROM python:3.12.13-alpine3.24@sha256:6d43704baacd1bfbe7c295d7f13079d5d8104ed33568873133f8fc69980419df

# Copy a reproducibly pinned uv release into the image.
COPY --from=ghcr.io/astral-sh/uv:0.12.3@sha256:2d890623d310b57771ce840f0da5eed5fc6d657da05ffaa45d82797b53fa3abc /uv /uvx /bin/

# All following commands run from /app.
WORKDIR /app

# Copy dependency files first for better Docker caching.
COPY pyproject.toml uv.lock ./

# Install exactly the dependencies recorded in uv.lock.
RUN uv sync --frozen --no-dev

# Copy the backend source code.
COPY . .

# Make the virtual environment executables available.
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

# Listen on all container network interfaces.
CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
