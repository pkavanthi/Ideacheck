# GUARDIAN — Disaster Response Operations Platform

> **Transforms disaster response from a reactive scramble into a proactive, data-driven operation** where every critical decision in the 24–48 hour imminent-threat window is backed by a live, unified operational picture.

---

## Target Audience

| Persona | Role |
|---|---|
| District Emergency Managers | Oversee all district-level response activities |
| Field Relief Coordinators | Deploy and track resources in the field |
| State Disaster Authority Analysts | Cross-district situational awareness & analytics |

---

## Core Features

- **Incident Management** — Report, track, update, and resolve disaster incidents with severity and geo-coordinates.
- **Resource Registry** — Maintain an inventory of personnel, vehicles, equipment, medical supplies, food, water, and shelter.
- **Resource Deployment** — Deploy resources to incidents, track quantities, and automatically update availability.

---

## Technology Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11+, FastAPI 0.111 |
| ORM | SQLAlchemy 2.0 |
| Validation | Pydantic v2 |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Server | Uvicorn (ASGI) |

---

## Prerequisites

- Python 3.11 or later
- `pip` / `venv`

---

## Installation & Local Setup

```bash
# 1. Clone the repository
git clone <repo-url>
cd guardian

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r backend/requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env and set SECRET_KEY and DATABASE_URL as needed

# 5. Run the development server
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at **http://localhost:8000**.  
Interactive docs: **http://localhost:8000/docs**

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `APP_NAME` | `GUARDIAN` | Application display name |
| `APP_VERSION` | `1.0.0` | API version string |
| `DEBUG` | `false` | Enable SQLAlchemy query logging |
| `SECRET_KEY` | *(required)* | Secret used for JWT signing |
| `DATABASE_URL` | `sqlite:///./guardian.db` | SQLAlchemy database URL |
| `ALLOWED_ORIGINS` | `http://localhost:3000,...` | Comma-separated CORS origins |
| `JWT_ALGORITHM` | `HS256` | JWT signing algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `480` | Token lifetime (minutes) |

---

## API Endpoints

### Health

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Liveness check |

### Incidents  (`/api/v1/incidents`)

| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/incidents/` | List incidents (filterable by `severity`, `status`) |
| POST | `/api/v1/incidents/` | Report a new incident |
| GET | `/api/v1/incidents/{id}` | Get incident details |
| PUT | `/api/v1/incidents/{id}` | Update an incident |
| DELETE | `/api/v1/incidents/{id}` | Delete an incident |

### Resources  (`/api/v1/resources`)

| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/resources/` | List resources (filterable by `resource_type`, `status`) |
| POST | `/api/v1/resources/` | Register a new resource |
| GET | `/api/v1/resources/{id}` | Get resource details |
| PUT | `/api/v1/resources/{id}` | Update a resource |
| DELETE | `/api/v1/resources/{id}` | Delete a resource |
| POST | `/api/v1/resources/deployments/incident/{incident_id}` | Deploy a resource to an incident |

---

## Architecture Overview

```
backend/
├── main.py          # FastAPI app factory, CORS, startup hooks
├── config.py        # Pydantic-settings configuration
├── database.py      # SQLAlchemy engine, session factory, init_db()
├── models.py        # ORM models: Incident, Resource, ResourceDeployment
└── routers/
    ├── incidents.py # Incident CRUD endpoints + Pydantic schemas
    └── resources.py # Resource CRUD + deployment endpoints + schemas
```

The application follows a **Modular Monolith** pattern:
- Each domain (incidents, resources) owns its router, schemas, and business logic.
- All modules share a single SQLite/PostgreSQL database.
- Clear boundaries make it straightforward to extract services later.

---

## Running with PostgreSQL

```bash
# Install the psycopg2 driver
pip install psycopg2-binary

# Update DATABASE_URL in .env
DATABASE_URL=postgresql://guardian_user:password@localhost:5432/guardian_db
```

---

## Testing

```bash
pip install pytest httpx
pytest backend/tests/
```

---

## Deployment

For production, replace SQLite with PostgreSQL, set `DEBUG=false`, and run behind a reverse proxy (Nginx / Caddy):

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```
