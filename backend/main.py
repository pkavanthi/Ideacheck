from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from backend.config import settings
from backend.routers import health_centers, diagnostics

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Rural Healthcare Diagnostic Hub",
    description="Transform rural health centers into connected diagnostic hubs",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_centers.router, prefix="/api/v1/health-centers", tags=["Health Centers"])
app.include_router(diagnostics.router, prefix="/api/v1/diagnostics", tags=["Diagnostics"])

@app.get("/")
async def root():
    return {
        "message": "Rural Healthcare Diagnostic Hub API",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
