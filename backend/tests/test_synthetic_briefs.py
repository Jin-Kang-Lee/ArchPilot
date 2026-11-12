"""Tests for the synthetic brief fixtures under ``examples/synthetic-briefs/``.

These files are the shared inputs for development, API demos and later
evaluation (FR-024). They contain fabricated companies only (NFR-001).
"""

from __future__ import annotations

from pathlib import Path

import pytest
from app.models.limits import BRIEF_MAX_LENGTH
from app.models.project import ProjectCreate

BRIEF_DIR = Path(__file__).resolve().parents[2] / "examples" / "synthetic-briefs"
BRIEF_NAMES = ("customer_support.txt", "media_moderation.txt", "invoice_processing.txt")
PLACEHOLDER_MARKERS = ("TODO", "TBD", "Lorem ipsum", "<insert", "XXX")


@pytest.mark.parametrize("brief_name", BRIEF_NAMES)
def test_every_brief_exists_and_is_readable(brief_name: str) -> None:
    source = BRIEF_DIR / brief_name

    assert source.is_file()
    assert source.read_text(encoding="utf-8").strip()


@pytest.mark.parametrize("brief_name", BRIEF_NAMES)
def test_every_brief_has_realistic_length(brief_name: str) -> None:
    text = (BRIEF_DIR / brief_name).read_text(encoding="utf-8")

    assert 200 < len(text) < BRIEF_MAX_LENGTH


@pytest.mark.parametrize("brief_name", BRIEF_NAMES)
def test_every_brief_satisfies_the_project_input_contract(brief_name: str) -> None:
    text = (BRIEF_DIR / brief_name).read_text(encoding="utf-8")
    title = brief_name.removesuffix(".txt").replace("_", " ").title()

    project = ProjectCreate(title=title, raw_brief=text)

    assert project.raw_brief == text.strip()


@pytest.mark.parametrize("brief_name", BRIEF_NAMES)
def test_no_brief_contains_placeholder_text(brief_name: str) -> None:
    text = (BRIEF_DIR / brief_name).read_text(encoding="utf-8")

    found = [marker for marker in PLACEHOLDER_MARKERS if marker in text]

    assert found == []


def test_customer_support_brief_keeps_the_as01_anchors() -> None:
    """AS-01 depends on these facts being present and these gaps being absent."""
    text = (BRIEF_DIR / "customer_support.txt").read_text(encoding="utf-8").lower()

    for anchor in ("10,000", "english", "chinese", "sensitive", "budget"):
        assert anchor in text

    # The brief states no budget figure, SLA or region: the Analyst must ask.
    for absent in ("per month", "sla", "us-east", "eu-west"):
        assert absent not in text
