"""FastAPI application entry point.

Only the foundation surface exists in M1-T01: a factory that wires routers and
a module-level ``app`` for ``uvicorn``. No agents, storage or validation live
here — they are added by later, approved tasks.
"""

from __future__ import annotations

from fastapi import FastAPI

from app.api.health import router as health_router
from app.config import settings


def create_app() -> FastAPI:
    """Build and configure the ArchPilot API application."""
    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
    )
    application.include_router(health_router)
    return application


app = create_app()
