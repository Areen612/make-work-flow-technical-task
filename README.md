# MAKE WORK FLOW Technical Task

Technical assessment project containing a React and TypeScript frontend, a
FastAPI backend, and a PostgreSQL database.

## Prerequisites

- Node.js 20.19 or newer (Node.js 22.23.2 is declared in `.tool-versions`)
- Python 3.12
- [uv](https://docs.astral.sh/uv/)
- PostgreSQL with a `make_work_flow` database

If you use asdf, install and activate the declared Node.js version from the
repository root:

```sh
asdf install
```

## Run the backend

```sh
cd backend
cp .env.example .env
uv sync
uv run fastapi dev main.py
```

The API is available at `http://localhost:8000`. It creates the `users` table
and seeds two example users when the database is empty.

## Run the frontend

In a separate terminal:

```sh
cd frontend
npm ci
npm run dev
```

The frontend is available at `http://localhost:5173`.

## Checks

```sh
cd backend
uv run python -m compileall -q .

cd ../frontend
npm run lint
npm run build
```
