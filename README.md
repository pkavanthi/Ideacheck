# StormSense AI

**National intelligence backbone for multi-hazard disaster response.**  
StormSense AI federates district nodes to deliver predictive resilience across 1.4 billion citizens.

---

## Target Users

| Persona | Role |
|---|---|
| District Collector | Authorizes evacuation orders |
| NDRF Field Commander | Executes ground operations |
| Vulnerable Community Resident | Receives alerts and evacuation guidance |

---

## Core Features

- **District Management** — Full CRUD for 780+ district nodes (name, state, collector, geo-coordinates)
- **Alert Management** — Issue, track, and resolve multi-hazard alerts (flood, cyclone, earthquake, drought, heatwave)
- **Evacuation Tracking** — Flag evacuation-required alerts with zone information and affected population counts

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11 + FastAPI |
| ORM | SQLAlchemy 2.x |
| Validation | Pydantic v2 |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Migrations | Alembic |
| Server | Uvicorn |

---

## Prerequisites

- Python 3.11+
- pip

---

## Installation

```bash
# 1. Clone the repository
git clone <repo-url>
cd stormsense-ai

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r backend/requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env as needed
```

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `DEBUG` | `false` | Enable debug logging |
| `DATABASE_URL` | `sqlite:///./stormsense.db` | SQLAlchemy database URL |
| `SECRET_KEY` | *(required in prod)* | JWT signing secret |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | Token lifetime |
| `ALLOWED_ORIGINS` | `http://localhost:3000` | Comma-separated CORS origins |

---

## Running Locally

```bash
# From the project root
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The database tables are created automatically on first startup.

Interactive API docs available at:
- Swagger UI → http://localhost:8000/api/v1/docs
- ReDoc → http://localhost:8000/api/v1/redoc

---

## API Endpoints

### Health

| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/health` | Service health check |

### Districts

| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/districts/` | Create a district |
| GET | `/api/v1/districts/` | List all districts (filter by `state`, `is_active`) |
| GET | `/api/v1/districts/{id}` | Get a district |
| PATCH | `/api/v1/districts/{id}` | Update a district |
| DELETE | `/api/v1/districts/{id}` | Delete a district |

### Alerts

| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/alerts/` | Issue a new alert |
| GET | `/api/v1/alerts/` | List alerts (filter by `district_id`, `hazard_type`, `severity`, `status`) |
| GET | `/api/v1/alerts/{id}` | Get an alert |
| PATCH | `/api/v1/alerts/{id}` | Update / resolve an alert |
| DELETE | `/api/v1/alerts/{id}` | Delete an alert |

---

## Database Migrations (Alembic)

```bash
# Initialise Alembic (first time only)
alembic init alembic

# Generate a migration after model changes
alembic revision --autogenerate -m "describe change"

# Apply migrations
alembic upgrade head
```

---

## Architecture

```
stormsense-ai/
├── backend/
│   ├── main.py          # FastAPI app, middleware, router registration
│   ├── database.py      # SQLAlchemy engine + session factory
│   ├── models.py        # ORM models: District, Alert
│   ├── config.py        # Settings loaded from environment
│   └── routers/
│       ├── districts.py # District CRUD endpoints
│       └── alerts.py    # Alert CRUD endpoints
├── .env.example         # Environment variable template
└── README.md
```

The application follows a **Modular Monolith** pattern — a single deployable unit with clearly separated modules (routing, models, configuration, database).

---

## Production Notes

- Switch `DATABASE_URL` to a PostgreSQL connection string.
- Set a strong, unique `SECRET_KEY`.
- Set `DEBUG=false`.
- Run behind a reverse proxy (nginx / Caddy) with TLS termination.
