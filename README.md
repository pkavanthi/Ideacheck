# Unified Climate Risk Brain

A national **Unified Climate Risk Brain** that tracks floods, cyclones, earthquakes and heatwaves, serving state and national disaster management authorities, emergency operations centres, rescue forces and insurers.

---

## Architecture

Full-stack disaster management operations platform featuring a FastAPI backend and a high-performance React + Vite + Tailwind CSS frontend dashboard with Leaflet geospatial intelligence.

```
backend/
├── main.py            # FastAPI application entry point
├── config.py          # Centralised configuration (reads .env)
├── models.py          # SQLAlchemy ORM models + DB bootstrap
├── requirements.txt   # Python dependencies
└── routers/
    ├── risks.py       # /api/v1/risks  – climate risk events CRUD
    └── alerts.py      # /api/v1/alerts – risk alerts CRUD
frontend/
├── src/
│   ├── components/
│   │   ├── Navbar.jsx         # Status banner, live sync badge, emergency broadcast CTAs
│   │   ├── Sidebar.jsx        # Operations navigation & hazard color key
│   │   ├── Dashboard.jsx      # Command center with KPIs, hazard charts & live ticker
│   │   ├── GeospatialMap.jsx  # Interactive Leaflet map with hazard radius & popups
│   │   ├── RisksModule.jsx    # Full CRUD registry for climate risk events
│   │   ├── AlertsModule.jsx   # Emergency broadcast operations & siren resolutions
│   │   ├── ImpactAnalytics.jsx# Parametric loss calculator & inter-agency SOP checklists
│   │   └── Toast.jsx          # Real-time feedback alerts
│   ├── services/
│   │   ├── api.js             # Unified API client with automatic offline demo fallback
│   │   └── mockData.js        # Pre-seeded national hazard scenarios & coordinates
│   ├── App.jsx                # Layout orchestrator & state synchronization
│   └── main.jsx               # React entry point
├── package.json               # Frontend dependencies & scripts
├── tailwind.config.js         # Custom hazard theme styling
└── vite.config.js             # Vite config with backend proxy
.env.example                   # Required environment variables
README.md
```

---

## Technology Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Runtime    | Python 3.11+                      |
| Framework  | FastAPI 0.111                     |
| ORM        | SQLAlchemy 2.0                    |
| Validation | Pydantic v2                       |
| Database   | SQLite (dev) / PostgreSQL (prod)  |
| Server     | Uvicorn                           |

---

## Target Audience

- State and national disaster management authorities
- Emergency operations centres
- Rescue forces
- Insurers in flood-prone regions

---

## Core Features

- **Climate Risk Events** – create, read, update and delete hazard event records (flood / cyclone / earthquake / heatwave)
- **Risk Alerts** – issue, track and resolve active alerts per region
- **Filtering** – list endpoints support filtering by hazard type and severity

---

## Prerequisites

- Python **3.11** or higher
- `pip`

---

## Installation

```bash
# 1. Clone the repository
git clone <repo-url>
cd <repo-root>

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r backend/requirements.txt

# 4. Copy environment variables
cp .env.example .env
# Edit .env as needed
```

---

## Environment Variables

| Variable                      | Default                        | Description                                |
|-------------------------------|--------------------------------|--------------------------------------------|
| `APP_NAME`                    | Unified Climate Risk Brain     | Application display name                   |
| `DEBUG`                       | `false`                        | Enable debug logging                       |
| `DATABASE_URL`                | `sqlite:///./climate_risk.db`  | SQLAlchemy database URL                    |
| `SECRET_KEY`                  | *(required in prod)*           | Secret used for signing tokens             |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60`                           | Token lifetime in minutes                  |
| `CORS_ORIGINS`                | `http://localhost:3000`        | Comma-separated list of allowed origins    |

---

## Running Locally

### 1. Start the FastAPI Backend

```bash
cd backend
uvicorn main:app --reload --port 8000
```

The API is available at `http://localhost:8000`.
Interactive docs: `http://localhost:8000/docs`

### 2. Start the React Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend application runs at `http://localhost:5173`.
*Note: The frontend operates with an automatic graceful fallback and local storage persistence if the backend is not yet started, and synchronises seamlessly once the backend is live.*

---

## API Endpoints

### Health

| Method | Path      | Description        |
|--------|-----------|--------------------|
| GET    | `/health` | Liveness check     |

### Climate Risk Events  `/api/v1/risks`

| Method | Path                  | Description                     |
|--------|-----------------------|---------------------------------|
| POST   | `/api/v1/risks/`      | Record a new risk event         |
| GET    | `/api/v1/risks/`      | List events (filter-able)       |
| GET    | `/api/v1/risks/{id}`  | Get a single event              |
| PUT    | `/api/v1/risks/{id}`  | Update an event                 |
| DELETE | `/api/v1/risks/{id}`  | Delete an event                 |

Query parameters for `GET /api/v1/risks/`: `hazard_type`, `severity`, `skip`, `limit`

### Risk Alerts  `/api/v1/alerts`

| Method | Path                    | Description                      |
|--------|-------------------------|----------------------------------|
| POST   | `/api/v1/alerts/`       | Issue a new alert                |
| GET    | `/api/v1/alerts/`       | List alerts (filter-able)        |
| GET    | `/api/v1/alerts/{id}`   | Get a single alert               |
| PUT    | `/api/v1/alerts/{id}`   | Update / resolve an alert        |
| DELETE | `/api/v1/alerts/{id}`   | Delete an alert                  |

Query parameters for `GET /api/v1/alerts/`: `hazard_type`, `active_only`, `skip`, `limit`

---

## Deployment Guide

### PostgreSQL (production)

Update `.env`:

```
DATABASE_URL=postgresql://user:password@db-host:5432/climate_risk
```

### Running with Docker (manual)

```bash
# Build
docker build -t climate-risk-brain ./backend

# Run
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/climate_risk \
  -e SECRET_KEY=your-secret \
  climate-risk-brain
```

---

## Testing

```bash
pip install pytest httpx
pytest backend/
```

---

## License

MIT
