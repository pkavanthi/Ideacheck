# National Resilience Intelligence Backbone

A unified national resilience intelligence backbone delivering predictive and transparent disaster response guidance. This MVP provides the backend CRUD foundation for incidents and response resources.

## Target Audience
Municipal disaster commanders, national and state disaster response forces, and emergency operations center personnel.

## Core Features (MVP)
- Basic CRUD for **Incidents** (type, severity, status, region, location, affected population)
- Basic CRUD for **Resources** (teams/equipment/supplies, optionally assigned to an incident)
- Filtering and pagination, API-key authentication, input validation

## Technology Stack
No stack was specified; defaults used: Python 3.11+, FastAPI, SQLAlchemy 2, Pydantic 2, SQLite (swap via `DATABASE_URL`).

## Architecture
Modular monolith, single deployable unit, shared database:
```
backend/
├── main.py        # app setup, middleware, router registration
├── config.py      # env-based settings
├── database.py    # engine/session/base
├── models.py      # ORM models + Pydantic schemas
├── security.py    # API-key auth dependency
└── routers/       # incidents.py, resources.py
```

## Prerequisites
- Python 3.11+

## Installation
```bash
cp .env.example .env        # set API_KEY
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```
Place/keep `.env` in `backend/` (or export variables) when running from there.

## Environment Variables
| Name | Description |
|------|-------------|
| `APP_NAME` | Application title |
| `APP_ENV` | Environment name |
| `DEBUG` | Enable debug mode |
| `DATABASE_URL` | SQLAlchemy URL (e.g. `postgresql://user:pass@host/db`) |
| `API_KEY` | Required secret for `X-API-Key` header |
| `CORS_ORIGINS` | JSON list of allowed origins |
| `LOG_LEVEL` | Logging level |

## Running Locally
```bash
cd backend
cp ../.env.example .env
uvicorn main:app --reload
```
Docs: http://localhost:8000/docs

## API Endpoints
All `/api/*` endpoints require header `X-API-Key`.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST/GET | `/api/incidents` | Create / list (filters: `region`, `severity`, `status`, `skip`, `limit`) |
| GET/PATCH/DELETE | `/api/incidents/{id}` | Read / update / delete |
| POST/GET | `/api/resources` | Create / list (filters: `resource_type`, `status`, `incident_id`) |
| GET/PATCH/DELETE | `/api/resources/{id}` | Read / update / delete |

Example:
```bash
curl -X POST localhost:8000/api/incidents -H "X-API-Key: $API_KEY" -H "Content-Type: application/json" \
  -d '{"title":"River flood","disaster_type":"flood","region":"Region-A","severity":"high"}'
```

## Docker / Testing / Deployment
Not included in this MVP. Deploy with `uvicorn main:app --host 0.0.0.0 --port 8000` behind a TLS-terminating proxy, using a managed PostgreSQL `DATABASE_URL` and a strong `API_KEY`.
