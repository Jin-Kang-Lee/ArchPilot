"""Smoke tests for the foundation health endpoint (M1-T01)."""

from __future__ import annotations

import pytest
from app.models.health import HealthResponse
from fastapi.testclient import TestClient
from pydantic import ValidationError


def test_health_returns_exact_ok_payload(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_payload_has_no_extra_dependency_detail(client: TestClient) -> None:
    """The contract is a single status field; no version/env leakage."""
    body = client.get("/health").json()

    assert set(body) == {"status"}


def test_health_response_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        HealthResponse(status="ok", environment="local")
