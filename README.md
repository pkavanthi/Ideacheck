# AegisFlow

AegisFlow is the foundation of an autonomous disaster intelligence fabric for climate-adaptive urban governance, designed to grow into an interconnected system of drones, automated floodgates and smart grid rerouting. This MVP backend provides basic CRUD for flood/landslide **incidents** and the **assets** (rescue teams, drones, floodgates, pumps, grid nodes) assigned to them.

## Target audience

- Government emergency operations commanders
- Municipal infrastructure managers
- Field rescue coordinators in flood- and landslide-prone districts

## Technology stack

The stack was not specified, so these defaults were assumed: Python 3.11+, FastAPI, SQLAlchemy 2.0, Pydantic v2, SQLite (any SQLAlchemy URL works, e.g. PostgreSQL).

## Architecture

Modular monolith, single deployment unit and shared database:

```
backend/
├── main.py            # app setup, middleware, router wiring
├── config.py          # env-based settings
├── models.py          # DB engine/session + Incident, Asset models
├── schemas.py         # Pydantic validation schemas
├── security.py        # API key authentication
└── routers/
    ├── incidents.py   # incident module
    └── assets.py      # asset module
```

## Prerequisites

- Python 3.11+

## Installation

```bash
cp .env.example backend/.env     # then set API_KEY to a long random value
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Environment variables

| Variable | Description | Default |
|---|---|---|
| `API_KEY` | Required. Secret expected in the `X-API-Key` header | – |
| `DATABASE_URL` | SQLAlchemy database URL | `sqlite:///./aegisflow.db` |
| `CORS_ORIGINS` | JSON list of allowed origins | `["http://localhost:3000"]` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `DEBUG` | FastAPI debug mode | `false` |

## Running locally

```bash
cd backend
uvicorn main:app --reload
```

Interactive docs: http://localhost:8000/docs (tables are created automatically on startup).

## Frontend

A React + TypeScript (Vite) dashboard in `frontend/` for managing incidents and assets. Requires Node 18+.

```bash
cd frontend
cp .env.example .env     # VITE_API_URL, defaults to http://localhost:8000
npm install
npm run dev              # http://localhost:3000 (matches the default CORS_ORIGINS)
```

Sign in with the backend `API_KEY`; it is kept in `sessionStorage` for the browser tab only. Build for production with `npm run build`.

## API endpoints

All `/api/*` endpoints require the `X-API-Key` header.

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/api/incidents` | Create incident |
| GET | `/api/incidents` | List (filters: `district`, `hazard_type`, `severity`, `status`, `skip`, `limit`) |
| GET | `/api/incidents/{id}` | Get incident |
| PATCH | `/api/incidents/{id}` | Update incident |
| DELETE | `/api/incidents/{id}` | Delete incident |
| POST | `/api/assets` | Create asset |
| GET | `/api/assets` | List (filters: `district`, `asset_type`, `status`, `incident_id`, `skip`, `limit`) |
| GET | `/api/assets/{id}` | Get asset |
| PATCH | `/api/assets/{id}` | Update asset |
| DELETE | `/api/assets/{id}` | Delete asset |

Example:

```bash
curl -X POST localhost:8000/api/incidents -H "X-API-Key: $API_KEY" -H "Content-Type: application/json" \
  -d '{"title":"River overflow","hazard_type":"flood","severity":"high","district":"Riverside"}'
```

## Core features implemented

- Basic CRUD for incidents (flood/landslide, severity, status, location, district)
- Basic CRUD for response assets, optionally linked to an incident

## Deployment

Not containerised in this MVP. Run with `uvicorn main:app --host 0.0.0.0 --port 8000` behind a TLS-terminating reverse proxy, use PostgreSQL via `DATABASE_URL` for production, and keep `API_KEY` in a secret store.
