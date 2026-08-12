# MAKE WORK FLOW Technical Task

A small full-stack application with a React and TypeScript frontend, a FastAPI
backend, and PostgreSQL. The frontend loads and displays users from the API.

## Quick start with Docker

This is the simplest way to run the complete application. Docker Desktop (or a
compatible Docker engine) is the only prerequisite.

1. Build and start the database, backend, and frontend:

   ```sh
   docker compose up
   ```

2. Open the application:

   - Frontend: `http://localhost:5173`
   - API documentation: `http://localhost:8000/docs`

The backend creates the `users` table and adds two example users when the table
is empty. Click **Load users** on the frontend to retrieve them.

Stop the application with `Ctrl+C`, then remove its containers and network:

```sh
docker compose down
```

The PostgreSQL data remains in the named Docker volume between runs.

No setup or environment file is required. Compose uses safe local defaults and
builds images automatically on the first run.

## Environment variables

Environment configuration is optional for Docker. To customize the defaults,
create a root `.env` file from the provided template before starting Compose:

```sh
cp .env.example .env
```

Docker Compose reads this file automatically. Vite also reads it when the
frontend is run locally.

| Variable | Used for | Local value |
| --- | --- | --- |
| `POSTGRES_DB` | PostgreSQL database name | `make_work_flow` |
| `POSTGRES_USER` | PostgreSQL user | `postgres` |
| `POSTGRES_PASSWORD` | PostgreSQL password | `postgres` |
| `VITE_API_BASE_URL` | API address used by the browser | `http://localhost:8000` |
| `FRONTEND_ORIGIN` | Origin allowed by backend CORS | `http://localhost:5173` |

Compose provides the listed local values when `.env` is absent and constructs
`DATABASE_URL` from the three PostgreSQL variables. When running the backend
without Docker, `backend/.env` supplies `DATABASE_URL` directly instead.

Keep these points in mind when changing the configuration:

- `.env` is ignored by Git. Keep `.env.example` updated when adding variables.
- Variables prefixed with `VITE_` are included in browser code and must never
  contain secrets.
- `VITE_API_BASE_URL` must be reachable by the browser. With Docker Compose,
  use `localhost`, not the internal Compose service name `backend`.
- Restart the affected development server or Compose service after changing an
  environment variable.
- Replace the example database password before using this configuration beyond
  local development.

## Run locally without Docker

### Prerequisites

- Node.js 20.19 or newer
- Python 3.12
- [uv](https://docs.astral.sh/uv/)
- A running PostgreSQL server with a `make_work_flow` database

Node.js 22.23.2 is declared in `.tool-versions`. If you use asdf, install it
from the repository root:

```sh
asdf install
asdf exec node --version
```

Create the shared root environment file if you have not already done so:

```sh
cp .env.example .env
```

### 1. Start the backend

Create its local database connection file:

```sh
cp backend/.env.example backend/.env
```

Update `DATABASE_URL` in `backend/.env` if your local PostgreSQL connection is
different, then start the API:

```sh
cd backend
uv sync
uv run fastapi dev main.py
```

The backend is available at `http://localhost:8000`.

### 2. Start the frontend

In a second terminal:

```sh
cd frontend
npm ci
npm run dev
```

The frontend is available at `http://localhost:5173`. It reads
`VITE_API_BASE_URL` from the root `.env` file.

If Vite reports that `node:util` does not export `styleText`, the shell is using
an old Node.js version. Confirm that Node 20.19+ is active, or run the commands
through asdf:

```sh
asdf exec npm ci
asdf exec npm run dev
```

## API endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/` | Backend health message |
| `GET` | `/users` | List all users |
| `GET` | `/docs` | Interactive API documentation |

## Checks

Run the backend and frontend checks from the repository root:

```sh
cd backend
uv run pytest
uv run python -m compileall -q .

cd ../frontend
npm run lint
npm run build
```

## Project layout

```text
backend/            FastAPI application and database models
frontend/           React and TypeScript application
docker-compose.yml  Local full-stack orchestration
.env.example        Shared environment variable template
```
