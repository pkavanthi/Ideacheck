import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.config import get_settings
from backend.models import Base

logger = logging.getLogger(__name__)

settings = get_settings()

# SQLite requires connect_args for thread-safety with FastAPI
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=settings.DEBUG,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """Create all tables if they do not exist."""
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables initialised.")


def get_db():
    """FastAPI dependency that yields a SQLAlchemy session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
