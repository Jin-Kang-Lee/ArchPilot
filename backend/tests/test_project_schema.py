"""Input-contract tests for FR-001 (CT-001 groundwork).

The HTTP 422 assertion arrives with ``POST /api/projects`` in M1-T03; here the
same rejection rules are proven at the model layer, where they are cheap and
deterministic to test.
"""

from __future__ import annotations

import pytest
from app.models.limits import BRIEF_MAX_LENGTH, TITLE_MAX_LENGTH
from app.models.project import ProjectCreate
from pydantic import ValidationError

VALID_BRIEF = "We need an AI assistant that answers support questions in English and Chinese."
VALID_TITLE = "Customer support discovery"


def test_accepts_a_normal_brief() -> None:
    project = ProjectCreate(title=VALID_TITLE, raw_brief=VALID_BRIEF)

    assert project.title == VALID_TITLE
    assert project.raw_brief == VALID_BRIEF


@pytest.mark.parametrize("blank", ["", "   ", "\n\t  \r\n"])
def test_rejects_blank_or_whitespace_only_brief(blank: str) -> None:
    with pytest.raises(ValidationError) as error:
        ProjectCreate(title=VALID_TITLE, raw_brief=blank)

    assert error.value.errors()[0]["loc"] == ("raw_brief",)


def test_accepts_brief_at_the_documented_limit() -> None:
    project = ProjectCreate(title=VALID_TITLE, raw_brief="a" * BRIEF_MAX_LENGTH)

    assert len(project.raw_brief) == BRIEF_MAX_LENGTH


def test_rejects_brief_over_the_documented_limit() -> None:
    with pytest.raises(ValidationError):
        ProjectCreate(title=VALID_TITLE, raw_brief="a" * (BRIEF_MAX_LENGTH + 1))


def test_rejects_blank_title() -> None:
    with pytest.raises(ValidationError) as error:
        ProjectCreate(title="   ", raw_brief=VALID_BRIEF)

    assert error.value.errors()[0]["loc"] == ("title",)


def test_accepts_title_at_the_documented_limit() -> None:
    title = "t" * TITLE_MAX_LENGTH

    assert ProjectCreate(title=title, raw_brief=VALID_BRIEF).title == title


def test_rejects_title_over_the_documented_limit() -> None:
    with pytest.raises(ValidationError):
        ProjectCreate(title="t" * (TITLE_MAX_LENGTH + 1), raw_brief=VALID_BRIEF)


def test_strips_surrounding_whitespace_from_client_input() -> None:
    project = ProjectCreate(title="  Support discovery  ", raw_brief="  hello  ")

    assert project.title == "Support discovery"
    assert project.raw_brief == "hello"


def test_accepts_multilingual_brief() -> None:
    brief = "我们需要一个支持中英文的客户支持助手，每天约 10,000 次对话。"

    assert ProjectCreate(title="支持助手", raw_brief=brief).raw_brief == brief


def test_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        ProjectCreate(
            title=VALID_TITLE,
            raw_brief=VALID_BRIEF,
            approved=True,  # type: ignore[call-arg]
        )
