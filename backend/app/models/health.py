"""Health-check contract.

Deliberately contains no dependency, version or environment detail: the
endpoint must stay side-effect free and must not leak deployment information
(see ``03-DATA-CONTRACTS.md`` §8.2).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict


class HealthResponse(BaseModel):
    """Response body for ``GET /health``."""

    model_config = ConfigDict(extra="forbid")

    status: Literal["ok"] = "ok"
