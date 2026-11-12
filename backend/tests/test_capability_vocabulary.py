"""Tests for the capability vocabulary contract (FR-009 groundwork)."""

from __future__ import annotations

from pathlib import Path

import pytest
from app.catalog.vocabulary import (
    DEFAULT_VOCABULARY_PATH,
    Capability,
    CapabilityVocabulary,
    load_vocabulary,
)
from pydantic import ValidationError

EXPECTED_CAPABILITY_IDS = {
    "api_backend",
    "async_worker",
    "authentication",
    "data_storage",
    "document_ingestion",
    "document_retrieval",
    "human_review",
    "llm_inference",
    "message_queue",
    "model_inference",
    "notification",
    "object_storage",
    "observability",
    "web_ui",
}


def test_shipped_vocabulary_loads_and_is_versioned() -> None:
    vocabulary = load_vocabulary()

    assert DEFAULT_VOCABULARY_PATH.is_file()
    assert vocabulary.version
    assert len(vocabulary.capabilities) == len(EXPECTED_CAPABILITY_IDS)


def test_shipped_vocabulary_contains_exactly_the_agreed_capabilities() -> None:
    vocabulary = load_vocabulary()

    assert {capability.capability_id for capability in vocabulary.capabilities} == (
        EXPECTED_CAPABILITY_IDS
    )


def test_every_capability_has_a_description() -> None:
    vocabulary = load_vocabulary()

    assert all(capability.description for capability in vocabulary.capabilities)


def test_unknown_capability_returns_none() -> None:
    vocabulary = load_vocabulary()

    assert vocabulary.get("api_backend") is not None
    assert vocabulary.get("smart_answer_engine") is None


def test_duplicate_capability_id_is_rejected() -> None:
    with pytest.raises(ValidationError, match="duplicate capability id"):
        CapabilityVocabulary(
            version="test",
            capabilities=[
                Capability(capability_id="message_queue", description="Queue"),
                Capability(capability_id="message_queue", description="Queue again"),
            ],
        )


def test_duplicate_alias_is_rejected() -> None:
    with pytest.raises(ValidationError, match="clashes with"):
        CapabilityVocabulary(
            version="test",
            capabilities=[
                Capability(capability_id="message_queue", description="Queue", aliases=["queue"]),
                Capability(capability_id="async_worker", description="Worker", aliases=["Queue"]),
            ],
        )


def test_alias_equal_to_a_real_capability_id_is_rejected() -> None:
    with pytest.raises(ValidationError, match="clashes with"):
        CapabilityVocabulary(
            version="test",
            capabilities=[
                Capability(capability_id="message_queue", description="Queue"),
                Capability(
                    capability_id="async_worker", description="Worker", aliases=["message_queue"]
                ),
            ],
        )


def test_invalid_capability_id_pattern_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Capability(capability_id="Message Queue", description="Queue")


def test_missing_vocabulary_file_fails_loudly(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_vocabulary(tmp_path / "does-not-exist.json")


def test_versions_are_required(tmp_path: Path) -> None:
    payload = '{"capabilities": []}'
    source = tmp_path / "capabilities.json"
    source.write_text(payload, encoding="utf-8")

    with pytest.raises(ValidationError):
        load_vocabulary(source)


def test_loaded_instances_do_not_share_alias_lists() -> None:
    first = Capability(capability_id="queue_one", description="Queue")
    second = Capability(capability_id="queue_two", description="Queue")

    first.aliases.append("mutated")

    assert second.aliases == []
