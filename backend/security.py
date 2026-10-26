"""API key authentication dependency."""
import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from config import get_settings

_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def require_api_key(provided: str | None = Depends(_api_key_header)) -> None:
    expected = get_settings().api_key
    if not provided or not secrets.compare_digest(provided, expected):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API key")
