# DisasterOps API

> **Product Vision:** Make disasters anticipated rather than endured by giving every coordinator the intelligence of a full data science team.

A FastAPI-based disaster management platform for NDRF/SDMA coordinators, district administrations, and field rescue teams.

---

## Prerequisites

- Python 3.11+
- pip

---

## Installation

```bash
# 1. Clone the repository
git clone <repo-url>
cd <repo-folder>

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r backend/requirements.txt

# 4. Copy environment variables
cp .env.example .env
# Edit .env and set SECRET_KEY and DATABASE_URL
```

---

## Environment Variables

| Variable            | Required | Default                      | Description                            |
|---------------------|----------|------------------------------|----------------------------------------|
| `SECRET_KEY`        | ✅ Yes   | —                            | Secret key for JWT signing             |
| `DATABASE_URL`      | No       | `sqlite:///./disasterops.db` | SQLAlchemy connection string           |
| `DEBUG`             | No       | `false`                      | Enable debug mode                      |
| `CORS_ORIGINS`      | No       | `http://localhost:3000,...`  | Comma-separated allowed origins        |
| `JWT_EXPIRE_MINUTES`| No       | `1440`                       | JWT token lifetime in minutes          |

---

## Running Locally

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

- **Interactive Dynamic Web UI**: [http://localhost:8000/](http://localhost:8000/)
- **Interactive API Docs (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc Documentation**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Dynamic Frontend Capabilities

- **Tactical Geospatial Map (Leaflet.js)**: Live markers color-coded by severity, radar pulse alerts for critical incidents, popups with direct status actions, and click-on-map coordinate prefill.
- **Incident Management**: Real-time CRUD operations, status escalation workflow (`reported` → `active` → `contained` → `resolved`), severity prioritization, and multi-field filtering.
- **Resource Inventory**: Track units, deployment statuses (`available`, `deployed`, `unavailable`), 1-click deploy/recall toggles, and contact info.
- **Tactical Analytics (Chart.js)**: Real-time visual breakdowns of incidents by severity and status pipeline, plus resource allocation and type distributions.
- **Auto-Sync & Telemetry**: 10-second automatic polling toggle, live UTC tactical clock, and demo seed data button for instant simulation.

---

## API Endpoints

### Health
| Method | Path      | Description    |
|--------|-----------|----------------|
| GET    | `/health` | Health check   |

### Incidents  `/api/v1/incidents`
| Method | Path                   | Description                              |
|--------|------------------------|------------------------------------------|
| POST   | `/`                    | Report a new incident                    |
| GET    | `/`                    | List incidents (filter by status/severity) |
| GET    | `/{incident_id}`       | Get a single incident                    |
| PATCH  | `/{incident_id}`       | Update incident fields                   |
| DELETE | `/{incident_id}`       | Delete an incident                       |

**Query params for GET /** — `status`, `severity`, `skip`, `limit`

### Resources  `/api/v1/resources`
| Method | Path                   | Description                              |
|--------|------------------------|------------------------------------------|
| POST   | `/`                    | Register a new resource                  |
| GET    | `/`                    | List resources (filter by status/type)   |
| GET    | `/{resource_id}`       | Get a single resource                    |
| PATCH  | `/{resource_id}`       | Update resource fields                   |
| DELETE | `/{resource_id}`       | Delete a resource                        |

**Query params for GET /** — `status`, `type`, `skip`, `limit`

---

## Architecture Overview

```
backend/
├── main.py          # FastAPI application entry point, CORS, startup hooks
├── config.py        # Pydantic-settings based configuration
├── database.py      # SQLAlchemy engine, session factory, init_db()
├── models.py        # ORM models: Incident, Resource, ResourceDeployment
└── routers/
    ├── incidents.py  # CRUD routes + Pydantic schemas for Incident
    └── resources.py  # CRUD routes + Pydantic schemas for Resource
```

**Modular Monolith** — single deployment unit with clear module boundaries (router ↔ model ↔ config).

---

## Technology Stack

| Layer       | Technology            | Version  |
|-------------|-----------------------|----------|
| Framework   | FastAPI               | 0.111.0  |
| Server      | Uvicorn               | 0.29.0   |
| ORM         | SQLAlchemy            | 2.0.30   |
| Validation  | Pydantic v2           | 2.7.1    |
| Config      | pydantic-settings     | 2.2.1    |
| Migrations  | Alembic               | 1.13.1   |
| Database    | SQLite (dev) / PostgreSQL (prod) | — |

---

## Target Audience

- **NDRF / SDMA Coordinators** — manage active incidents and track resources nationally/state-wide
- **District Administrations** — report and monitor local incidents
- **Field Rescue Teams** — update incident status and resource availability in real time

---

## Core Features Implemented

- ✅ **Incident CRUD** — report, list, filter, update status/severity, delete incidents
- ✅ **Resource CRUD** — register, list, filter, update status, delete resources
- ✅ **Resource Deployment tracking** — junction table linking resources to incidents
- ✅ **Geo-coordinates** — latitude/longitude on incidents for map integration
- ✅ **Filtering & pagination** — by status, severity, type on all list endpoints

---

## Database Migrations (Alembic)

```bash
# Initialise (first time only)
alembic init alembic

# Generate a migration after model changes
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

---

## Testing

```bash
pip install pytest httpx
pytest
```
