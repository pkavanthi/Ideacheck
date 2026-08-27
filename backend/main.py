from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from backend.config import settings
from backend.routers import translations
from backend.database import engine, Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")
    Base.metadata.create_all(bind=engine)
    yield
    logger.info("Shutting down application...")


app = FastAPI(
    title="Educational Translation Platform",
    description="Transform global education into a borderless experience with multilingual support",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(translations.router, prefix="/api/v1/translations", tags=["translations"])


@app.get("/")
async def root():
    return {
        "message": "Educational Translation Platform API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
