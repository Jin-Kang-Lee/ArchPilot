"""Project input contract (FR-001).

``ProjectCreate`` is the only documented way customer text enters ArchPilot, so
it also acts as the input-size boundary that later protects model calls
(NFR-003/NFR-006). It is deliberately just the request shape: identifiers,
timestamps and discovery state are owned by the backend in M1-T03 onward.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from app.models.limits import BRIEF_MAX_LENGTH, TITLE_MAX_LENGTH


class ProjectCreate(BaseModel):
    """Request body for creating a project from a customer brief."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=TITLE_MAX_LENGTH)
    raw_brief: str = Field(min_length=1, max_length=BRIEF_MAX_LENGTH)
