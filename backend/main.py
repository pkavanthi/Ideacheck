from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.database import Base, engine
from backend.routers import incidents, resources

# Initialize database schema
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="GUARDIAN - Unified Operational Disaster Response API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins if settings.cors_origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Attach API routers
app.include_router(incidents.router, prefix="/api/v1")
app.include_router(resources.router, prefix="/api/v1")

@app.get("/")
def root():
    return {
        "system": settings.APP_NAME,
        "status": "OPERATIONAL",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
