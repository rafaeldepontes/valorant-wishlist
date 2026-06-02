import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient

from app.main import app
from app.api.deps import get_user_store, get_auth_service

@pytest.fixture
def mock_user_store():
    return AsyncMock()

@pytest.fixture
def mock_auth_service():
    return MagicMock()

@pytest.fixture
def client(
    mock_user_store,
    mock_auth_service
):
    app.dependency_overrides[get_user_store] = lambda: mock_user_store
    app.dependency_overrides[get_auth_service] = lambda: mock_auth_service

    yield TestClient(app)

    app.dependency_overrides = {}
