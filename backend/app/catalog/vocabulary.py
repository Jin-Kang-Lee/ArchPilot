"""Capability vocabulary: the shared, closed set of technical capabilities.

Both AI roles must speak this vocabulary: the Requirements Analyst tags
requirements with capability IDs (M1-T03) and the Architecture Designer composes
nodes from the same IDs (M2-T02). Keeping it as versioned data rather than code
lets us review, version and evaluate it without touching agent prompts.

The vocabulary deliberately contains no graph relationships or obligations yet;
those are introduced with the graph contract (M2-T01) once the queue-consumer
edge semantics are aligned (see ``docs/DECISIONS.md`` D-003).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, model_validator

CAPABILITY_ID_PATTERN = r"^[a-z][a-z0-9_]*$"

# backend/app/catalog/vocabulary.py -> repository root
DEFAULT_VOCABULARY_PATH = Path(__file__).resolve().parents[3] / "catalog" / "capabilities.json"


class Capability(BaseModel):
    """One technical capability ArchPilot may reason about."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    capability_id: str = Field(pattern=CAPABILITY_ID_PATTERN)
    description: str = Field(min_length=1)
    aliases: list[Annotated[str, Field(min_length=1)]] = Field(default_factory=list)


class CapabilityVocabulary(BaseModel):
    """A versioned set of capabilities with unique IDs and unique names."""

    model_config = ConfigDict(extra="forbid")

    version: str = Field(min_length=1)
    capabilities: list[Capability] = Field(default_factory=list)

    @model_validator(mode="after")
    def reject_duplicate_names(self) -> CapabilityVocabulary:
        """Reject repeated capability IDs, repeated aliases and alias/ID clashes.

        Names are compared case-insensitively so that ``Queue`` and ``queue``
        cannot become two different things.
        """
        seen: dict[str, str] = {}
        for capability in self.capabilities:
            identifier = capability.capability_id
            if identifier in seen:
                raise ValueError(f"duplicate capability id: {identifier}")
            seen[identifier] = identifier

            for alias in capability.aliases:
                normalized = alias.casefold()
                if normalized in seen:
                    raise ValueError(
                        f"capability alias {alias!r} on {identifier!r} "
                        f"clashes with {seen[normalized]!r}"
                    )
                seen[normalized] = identifier
        return self

    def get(self, capability_id: str) -> Capability | None:
        """Return the capability with this ID, or ``None`` if it is unsupported."""
        for capability in self.capabilities:
            if capability.capability_id == capability_id:
                return capability
        return None


def load_vocabulary(path: Path | None = None) -> CapabilityVocabulary:
    """Load and validate the vocabulary from a JSON file.

    Defaults to the repository's versioned catalog. A missing or malformed file
    raises instead of returning an empty vocabulary, so an unavailable catalog
    can never be mistaken for "no capabilities required".
    """
    source = DEFAULT_VOCABULARY_PATH if path is None else path
    with source.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    return CapabilityVocabulary.model_validate(payload)
