"""Health endpoint (foundation task M1-T01).

Kept dependency-free so it can serve as a deployment smoke test later
(NFR-012) without touching the model provider, catalog or storage.
"""

from __future__ import annotations

from fastapi import APIRouter

from app.models.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse, summary="Liveness check")
def health() -> HealthResponse:
    """Return a static liveness payload."""
    return HealthResponse(status="ok")
