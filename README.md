# Disaster Resilience Platform

> A continuously learning, multi-hazard intelligence layer that enables communities to **outrun disasters rather than react to them.**

## Target Audience

| Persona | Role |
|---------|------|
| Government disaster-management officers | District & state-level planning |
| NDRF field commanders | Field deployment and resource coordination |
| Hospital emergency coordinators | Medical resource allocation |

## Features Implemented

- **Incident management** — Create, read, update, and delete disaster incidents with hazard type, severity, location (lat/lon), district, and state
- **Resource deployments** — Track NDRF teams, hospitals, and equipment deployed per incident
- **Filtering** — Filter incidents by state, district, severity, status, and hazard type

## Architecture

Modular Monolith with clear separation of concerns:

```
backend/
├── main.py          # FastAPI application entry point
├── config.py        # Settings via pydantic-settings + .env
├── models.py        # SQLAlchemy ORM models + DB session
└── routers/
    ├── incidents.py # /api/v1/incidents  CRUD
    └── resources.py # /api/v1/incidents/{id}/resources  CRUD
README.md
.env.example
```

## Technology Stack

| Layer | Technology |
|-------|------------|
| Backend framework | FastAPI ≥ 0.110 |
| ORM | SQLAlchemy ≥ 2.0 |
| Validation | Pydantic ≥ 2.6 |
| Database (dev) | SQLite |
| Database (prod) | PostgreSQL (swap `DATABASE_URL`) |
| Migrations | Alembic |
| Server | Uvicorn |

## Prerequisites

- Python ≥ 3.11
- pip

## Installation

```bash
# 1. Clone / enter project directory
cd <project-root>

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r backend/requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and set SECRET_KEY to a long random value
```

## Running Locally

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.  
Interactive docs: `http://localhost:8000/docs`

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | SQLAlchemy database URL | `sqlite:///./disaster_resilience.db` |
| `SECRET_KEY` | JWT signing key — **change in production** | `change-me-in-production` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token lifetime | `60` |
| `ALLOWED_ORIGINS` | Comma-separated CORS origins | `http://localhost:3000,...` |
| `DEBUG` | Enable debug mode | `false` |

## API Endpoints

### Incidents

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/incidents/` | Report a new incident |
| `GET` | `/api/v1/incidents/` | List incidents (supports filters) |
| `GET` | `/api/v1/incidents/{id}` | Get a single incident |
| `PATCH` | `/api/v1/incidents/{id}` | Update an incident |
| `DELETE` | `/api/v1/incidents/{id}` | Delete an incident |

**Query filters for `GET /incidents/`:** `state`, `district`, `severity`, `status`, `hazard_type`, `skip`, `limit`

### Resource Deployments

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/incidents/{id}/resources/` | Deploy a resource |
| `GET` | `/api/v1/incidents/{id}/resources/` | List resources for incident |
| `GET` | `/api/v1/incidents/{id}/resources/{rid}` | Get a single resource |
| `PATCH` | `/api/v1/incidents/{id}/resources/{rid}` | Update a resource |
| `DELETE` | `/api/v1/incidents/{id}/resources/{rid}` | Remove a resource |

### Health

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Liveness check |

## Database Migrations (Alembic)

```bash
# Initialise (first time)
alembic init alembic

# Generate a migration
alembic revision --autogenerate -m "initial"

# Apply migrations
alembic upgrade head
```

## Deployment Guide

1. Set `DATABASE_URL` to a PostgreSQL connection string.
2. Set a strong `SECRET_KEY`.
3. Set `ALLOWED_ORIGINS` to your frontend domain(s).
4. Set `DEBUG=false`.
5. Run with a production ASGI server:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```
