from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from backend.config import settings
from backend.database import engine, Base
from backend.routers import patients, health_workers, consultations

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")
    Base.metadata.create_all(bind=engine)
    yield
    logger.info("Shutting down application...")


app = FastAPI(
    title="Rural Healthcare Platform",
    description="AI-augmented healthcare delivery platform for rural areas",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(patients.router, prefix="/api/v1/patients", tags=["Patients"])
app.include_router(health_workers.router, prefix="/api/v1/health-workers", tags=["Health Workers"])
app.include_router(consultations.router, prefix="/api/v1/consultations", tags=["Consultations"])


@app.get("/")
async def root():
    return {
        "message": "Rural Healthcare Platform API",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
