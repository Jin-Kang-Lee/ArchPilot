"""Discovery-phase state vocabulary.

Only the states required by Month 1 discovery are defined here. Graph, finding,
mapping and review states are introduced by the tasks that first consume them
(M2/M3) so that no semantics are frozen before they can be tested.
"""

from __future__ import annotations

from enum import StrEnum


class RequirementKind(StrEnum):
    """Nature of a requirement."""

    FUNCTIONAL = "functional"
    NON_FUNCTIONAL = "non_functional"
    CONSTRAINT = "constraint"


class KnowledgeStatus(StrEnum):
    """Evidence/confirmation state of a requirement.

    ``CONFIRMED`` means *stated by the customer or SA*, not technically verified.
    """

    CONFIRMED = "confirmed"
    ASSUMED = "assumed"
    UNKNOWN = "unknown"
    CONTRADICTED = "contradicted"


class QuestionPriority(StrEnum):
    """Relative design impact of a requirement or clarification question."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class QuestionStatus(StrEnum):
    """Lifecycle of a clarification question."""

    OPEN = "open"
    ANSWERED = "answered"
    DEFERRED = "deferred"
    SKIPPED = "skipped"
    NOT_APPLICABLE = "not_applicable"


class DiscoveryReadiness(StrEnum):
    """SA-facing design readiness. Not a quality or security score."""

    NEEDS_CLARIFICATION = "needs_clarification"
    READY_FOR_DESIGN = "ready_for_design"
    PROVISIONAL = "provisional"
