# Rural Bond Exchange

A rural bond exchange platform that enables smallholder horticulture farmers to convert verified harvest fractions into immediate capital, eliminating intermediary lenders from village-level agricultural credit.

## Target Audience

| Persona | Role |
|---|---|
| Smallholder horticulture farmers | Create harvest-backed bonds to access credit |
| FPO treasurers | Manage FPO membership and surplus savings |
| Institutional agri-buyers | Browse and purchase bonds with verifiable produce provenance |

## Technology Stack

- **Runtime**: Python 3.11+
- **Framework**: FastAPI
- **ORM**: SQLAlchemy 2.x
- **Validation**: Pydantic v2
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Migrations**: Alembic
- **Server**: Uvicorn

## Architecture

Modular Monolith with clear separation of concerns:

```
backend/
├── main.py          # FastAPI application entrypoint
├── config.py        # Settings via pydantic-settings
├── database.py      # Engine, session factory, table creation
├── models.py        # SQLAlchemy ORM models
├── schemas.py       # Pydantic request/response schemas
└── routers/
    ├── bonds.py     # Bond CRUD endpoints
    └── farmers.py   # Farmer, FPO, and Buyer CRUD endpoints
```

## Prerequisites

- Python 3.11 or higher
- pip

## Installation

```bash
# 1. Clone the repository
git clone <repo-url>
cd rural-bond-exchange

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r backend/requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env as needed
```

## Running Locally

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Interactive API docs will be available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc:       http://localhost:8000/redoc

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `APP_NAME` | No | `Rural Bond Exchange` | Application display name |
| `APP_VERSION` | No | `1.0.0` | Semantic version |
| `DEBUG` | No | `false` | Enable debug mode |
| `DATABASE_URL` | Yes | `sqlite:///./rural_bond_exchange.db` | SQLAlchemy database URL |
| `SECRET_KEY` | Yes | — | JWT signing secret (change in production) |
| `ALGORITHM` | No | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | `1440` | Token lifetime in minutes |
| `ALLOWED_ORIGINS` | No | `["http://localhost:3000"]` | CORS allowed origins (JSON array) |

## API Endpoints

### Health
| Method | Path | Description |
|---|---|---|
| GET | `/health` | Health check |

### Farmers `/api/v1/farmers`
| Method | Path | Description |
|---|---|---|
| POST | `/` | Register a new farmer |
| GET | `/` | List farmers (filterable by `district`) |
| GET | `/{farmer_id}` | Get farmer by ID |
| PATCH | `/{farmer_id}` | Update farmer |
| DELETE | `/{farmer_id}` | Delete farmer |

### FPOs `/api/v1/fpos`
| Method | Path | Description |
|---|---|---|
| POST | `/` | Create a new FPO |
| GET | `/` | List FPOs |
| GET | `/{fpo_id}` | Get FPO by ID |
| PATCH | `/{fpo_id}` | Update FPO |
| DELETE | `/{fpo_id}` | Delete FPO |

### Buyers `/api/v1/buyers`
| Method | Path | Description |
|---|---|---|
| POST | `/` | Register a new buyer |
| GET | `/` | List buyers |
| GET | `/{buyer_id}` | Get buyer by ID |
| PATCH | `/{buyer_id}` | Update buyer |
| DELETE | `/{buyer_id}` | Delete buyer |

### Bonds `/api/v1/bonds`
| Method | Path | Description |
|---|---|---|
| POST | `/` | Issue a new harvest bond |
| GET | `/` | List bonds (filterable by `status`) |
| GET | `/{bond_id}` | Get bond by ID |
| PATCH | `/{bond_id}` | Update bond (verify, assign buyer, etc.) |
| DELETE | `/{bond_id}` | Delete pending/cancelled bond |

## Database Migrations (Alembic)

```bash
# Initialise Alembic (first time only)
alembic init alembic

# Edit alembic/env.py to import Base from backend.models and set target_metadata

# Generate a migration
alembic revision --autogenerate -m "initial schema"

# Apply migrations
alembic upgrade head
```

## Core Features Implemented

- **Farmer management** — register, update, deactivate smallholder farmers linked to FPOs
- **FPO management** — create and manage Farmer Producer Organisations
- **Buyer management** — register institutional agri-buyers
- **Harvest bond CRUD** — issue bonds backed by a verified harvest fraction; update verification status, assign buyers, and track lifecycle (`pending → verified → active → redeemed`)
