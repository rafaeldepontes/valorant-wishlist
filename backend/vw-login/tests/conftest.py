import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient

from app.main import app
from app.api.deps import get_user_store, get_auth_service

@pytest.fixture(autouse=True)
def mock_db_init(monkeypatch):
    monkeypatch.setattr("app.core.lifespan.init_db", AsyncMock())

@pytest.fixture
def mock_user_store():
    return AsyncMock()

@pytest.fixture
def mock_auth_service():
    mock = MagicMock()
    mock.hash_password.side_effect = lambda x: f"hashed_{x}"
    mock.verify_password.side_effect = lambda h, p: h == f"hashed_{p}"
    return mock

@pytest.fixture
def client(
    mock_user_store,
    mock_auth_service
):
    app.dependency_overrides[get_user_store] = lambda: mock_user_store
    app.dependency_overrides[get_auth_service] = lambda: mock_auth_service

    with TestClient(app) as client:
        yield client

    app.dependency_overrides = {}
