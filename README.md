# Rural India Village Health Monitor

> **Vision:** Make every rural Indian village health-legible so that no healthcare gap goes undetected and no community remains underserved — through the power of open data and AI.

---

## Target Audience

| Persona | Role |
|---|---|
| District Health Officers | Monitor district-wide health coverage and detect underserved areas |
| PHC Doctors | Record and review health observations at Primary Health Centre level |
| ASHA Workers | Submit ground-level health reports from individual villages |
| State NHM Administrators | Track state-level health programme performance |
| National Policy Planners | Analyse aggregated data for policy decisions |

---

## Core Features

- **Village Registry** — Full CRUD for village entities (name, district, state, coordinates, PHC linkage)
- **Health Records** — Categorised health observations per village (maternal health, immunisation, nutrition, disease outbreak, sanitation)
- **Gap Detection** — Flag `is_gap_detected` on any record; aggregate gap summary endpoint surfaces highest-need villages
- **ASHA Worker Registry** — Track field workers assigned to villages

---

## Technology Stack

| Layer | Technology |
|---|---|
| API Framework | FastAPI 0.111 |
| ORM | SQLAlchemy 2.0 |
| Validation | Pydantic v2 |
| Database (dev) | SQLite |
| Database (prod) | PostgreSQL (swap `DATABASE_URL`) |
| Server | Uvicorn |

**Architecture:** Modular Monolith — routes, models, database, and config are separate modules inside a single deployable unit.

---

## Prerequisites

- Python 3.11+
- pip

---

## Installation & Local Run

```bash
# 1. Clone the repository
git clone <repo-url>
cd <repo-root>

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r backend/requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env as needed (DATABASE_URL, SECRET_KEY, etc.)

# 5. Run the development server
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at **http://localhost:8000**

- Interactive docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health check: http://localhost:8000/health

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `APP_NAME` | `Rural India Village Health Monitor` | Application display name |
| `APP_VERSION` | `1.0.0` | API version string |
| `DEBUG` | `false` | Enable SQLAlchemy query logging |
| `LOG_LEVEL` | `INFO` | Python logging level |
| `DATABASE_URL` | `sqlite:///./health_monitor.db` | SQLAlchemy database URL |
| `SECRET_KEY` | *(required)* | JWT signing secret — **change in production** |
| `ALGORITHM` | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `480` | Token TTL in minutes |
| `ALLOWED_ORIGINS` | `["http://localhost:3000",...]` | CORS allowed origins (JSON list) |

---

## API Endpoints

### System
| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `GET` | `/` | Root info |

### Villages `/api/v1/villages`
| Method | Path | Description |
|---|---|---|
| `GET` | `/api/v1/villages/` | List villages (supports `search`, `state`, `district`, pagination) |
| `POST` | `/api/v1/villages/` | Create a village |
| `GET` | `/api/v1/villages/{id}` | Get village by ID |
| `PATCH` | `/api/v1/villages/{id}` | Update village fields |
| `DELETE` | `/api/v1/villages/{id}` | Delete village |

### Health Records `/api/v1/health-records`
| Method | Path | Description |
|---|---|---|
| `GET` | `/api/v1/health-records/` | List records (filter by `village_id`, `category`, `is_gap_detected`) |
| `POST` | `/api/v1/health-records/` | Create a health record |
| `GET` | `/api/v1/health-records/{id}` | Get record by ID |
| `PATCH` | `/api/v1/health-records/{id}` | Update record fields |
| `DELETE` | `/api/v1/health-records/{id}` | Delete record |
| `GET` | `/api/v1/health-records/summary/gaps` | Top villages by gap count |

#### Valid Health Record Categories
`maternal_health` · `immunisation` · `nutrition` · `disease_outbreak` · `sanitation` · `other`

---

## Project Structure

```
.
├── backend/
│   ├── __init__.py
│   ├── main.py          # FastAPI app, middleware, router registration
│   ├── config.py        # Settings via pydantic-settings
│   ├── database.py      # SQLAlchemy engine + session factory
│   ├── models.py        # ORM models: Village, ASHAWorker, HealthRecord
│   ├── requirements.txt # Python dependencies
│   └── routers/
│       ├── __init__.py
│       ├── villages.py  # Village CRUD endpoints
│       └── health.py    # Health record CRUD + gap summary
├── .env.example         # Environment variable template
└── README.md
```

---

## Switching to PostgreSQL

1. Install the driver: `pip install psycopg2-binary`
2. Set `DATABASE_URL` in `.env`:
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/health_monitor
   ```
3. Restart the server — SQLAlchemy will create tables automatically on startup.

---

## Running Tests

```bash
pip install pytest httpx
pytest backend/tests/
```

*(Test files are not included in the MVP; add them under `backend/tests/` as needed.)*
