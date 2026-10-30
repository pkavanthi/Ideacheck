"""Simple API-key authentication dependency."""
import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from config import get_settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def require_api_key(provided: str | None = Depends(api_key_header)) -> None:
    expected = get_settings().api_key
    if not expected:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="API key is not configured on the server",
        )
    if not provided or not secrets.compare_digest(provided, expected):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API key")
