# filepath: app/api/v1/endpoints/health.py
"""Liveness endpoint."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health() -> dict:
    """Return service liveness. Placeholder body."""
    raise NotImplementedError