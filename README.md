# GUARDIAN - Disaster Response Management System

GUARDIAN transforms disaster response from a reactive scramble into a proactive, data-driven operation where every critical decision in the 24–48 hour imminent-threat window is backed by a live, unified operational picture.

Designed for District Emergency Managers, Field Relief Coordinators, and State Disaster Authority Analysts operating during active monsoon emergencies in flood-prone regions of India.

---

## 🛠️ Technology Stack & Architecture

- **Architecture:** Modular Monolith
- **Backend:** Python 3.11, FastAPI, SQLAlchemy ORM, Pydantic, Uvicorn
- **Frontend:** React 18, Vite, TailwindCSS, Lucide Icons
- **Database:** SQLite (default / zero-config) / PostgreSQL-ready
- **Testing:** Pytest, HTTPX TestClient
- **Containerization:** Docker & Docker Compose

---

## 📁 Repository Structure

```
.
├── backend/
│   ├── config.py             # Application settings & environment parsing
│   ├── database.py           # SQLAlchemy engine & session management
│   ├── models.py             # Database models (Incidents, Relief Resources)
│   ├── schemas.py            # Pydantic validation & transfer schemas
│   ├── main.py               # FastAPI entrypoint & router registry
│   ├── routers/
│   │   ├── incidents.py      # Incident reporting & triage CRUD routes
│   │   └── resources.py      # Relief resource management CRUD routes
│   ├── tests/
│   │   └── test_api.py       # Pytest unit & integration test suite
│   ├── requirements.txt      # Python dependencies
│   └── Dockerfile            # Container build for backend service
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── IncidentForm.jsx
│   │   │   ├── IncidentList.jsx
│   │   │   └── ResourcePanel.jsx
│   │   ├── api.js            # API client module
│   │   ├── App.jsx           # Main React Dashboard
│   │   ├── main.jsx          # React DOM render entry
│   │   └── index.css         # Tailwind style directives
│   ├── package.json          # Node dependencies & scripts
│   ├── vite.config.js        # Vite bundler config
│   ├── tailwind.config.js    # Tailwind styling config
│   └── Dockerfile            # Container build for frontend UI
├── docker-compose.yml        # Multi-container orchestration
├── .env.example              # Example environment variables
└── README.md                 # Setup & deployment documentation
```

---

## 🚀 Getting Started Locally

### 1. Backend Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Run backend development server
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`
- Interactive API Docs (Swagger): `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The UI dashboard will be available at `http://localhost:3000`.

---

## 🐳 Running with Docker

Run the entire stack with Docker Compose:

```bash
docker-compose up --build
```

- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000/docs`

---

## 🧪 Running Tests

Execute the backend integration and unit test suite:

```bash
pytest backend/tests/test_api.py -v
```

---

## 📡 API Endpoints

### Incidents (`/api/v1/incidents`)
- `GET /api/v1/incidents/` - List all incidents (filterable by `district`, `threat_level`, `status_filter`)
- `POST /api/v1/incidents/` - Log a new threat incident
- `GET /api/v1/incidents/{id}` - Fetch single incident details
- `PUT /api/v1/incidents/{id}` - Update incident severity, status, or details
- `DELETE /api/v1/incidents/{id}` - Remove incident entry

### Relief Resources (`/api/v1/resources`)
- `GET /api/v1/resources/` - List resources and inventory levels
- `POST /api/v1/resources/` - Register rescue units and emergency supplies
- `GET /api/v1/resources/{id}` - Get resource details
- `PUT /api/v1/resources/{id}` - Update available quantities and hub location
- `DELETE /api/v1/resources/{id}` - Decommission resource entry
