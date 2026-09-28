import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import get_settings
from backend.database import create_tables
from backend.routers.bonds import router as bonds_router
from backend.routers.farmers import buyer_router, farmers_router, fpo_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "Rural Bond Exchange API — convert verified harvest fractions into "
        "immediate capital for smallholder horticulture farmers."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    logger.info("Creating database tables if they do not exist…")
    create_tables()
    logger.info("Application startup complete.")


# Register routers
app.include_router(farmers_router, prefix="/api/v1")
app.include_router(fpo_router, prefix="/api/v1")
app.include_router(buyer_router, prefix="/api/v1")
app.include_router(bonds_router, prefix="/api/v1")


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "version": settings.APP_VERSION}
