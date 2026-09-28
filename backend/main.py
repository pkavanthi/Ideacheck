import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import get_settings
from backend.models import init_db
from backend.routers import incidents, resources

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "Multi-hazard intelligence layer enabling government disaster-management officers, "
        "NDRF field commanders, and hospital emergency coordinators to manage and respond "
        "to disaster incidents across India."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
)

# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Database initialisation
# ---------------------------------------------------------------------------

@app.on_event("startup")
def on_startup():
    logger.info("Initialising database tables…")
    init_db()
    logger.info("Database ready.")


# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

app.include_router(incidents.router, prefix="/api/v1")
app.include_router(resources.router, prefix="/api/v1")


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "version": settings.app_version}
