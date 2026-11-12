"""Runtime configuration.

Values are read once at import time from environment variables so that no
secret or deployment-specific value is ever committed to the repository
(NFR-002). Only non-sensitive, process-wide settings belong here.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field

DEFAULT_ENVIRONMENT = "local"


def _read_environment() -> str:
    """Return the current environment name, defaulting to ``local``."""
    return os.getenv("ARCHPILOT_ENV", DEFAULT_ENVIRONMENT).strip() or DEFAULT_ENVIRONMENT


@dataclass(frozen=True, slots=True)
class Settings:
    """Process-wide, read-only application settings."""

    app_name: str = "ArchPilot API"
    app_version: str = "0.1.0"
    environment: str = field(default_factory=_read_environment)


settings = Settings()
