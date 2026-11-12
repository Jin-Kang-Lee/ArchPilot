"""Shared pytest fixtures."""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from app.main import create_app
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> Iterator[TestClient]:
    """Provide a test client bound to a freshly created application."""
    with TestClient(create_app()) as test_client:
        yield test_client
