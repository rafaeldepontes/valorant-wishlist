import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.api.deps import get_user_store, get_wishlist_store, get_skin_cache, get_current_user, get_review_store, get_auth_service

@pytest.fixture
def mock_user_store():
    return AsyncMock()

@pytest.fixture
def mock_wishlist_store():
    return AsyncMock()

@pytest.fixture
def mock_review_store():
    return AsyncMock()

@pytest.fixture
def mock_auth_service():
    return MagicMock()

@pytest.fixture
def mock_skin_cache():
    mock = AsyncMock()
    mock.len = MagicMock(return_value=0)
    mock.exists = AsyncMock(return_value=True)
    return mock

@pytest.fixture
def current_user():
    return {
        "id": 1,
        "uuid": "u1",
        "username": "testuser",
        "email": "test@example.com",
        "password": "hashed_password",
        "status": "active",
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }

@pytest.fixture
def client(mock_user_store, mock_wishlist_store, mock_skin_cache, mock_review_store, mock_auth_service, current_user):
    mock_session = AsyncMock()
    mock_user_store.session = mock_session

    app.dependency_overrides[get_user_store] = lambda: mock_user_store
    app.dependency_overrides[get_wishlist_store] = lambda: mock_wishlist_store
    app.dependency_overrides[get_skin_cache] = lambda: mock_skin_cache
    app.dependency_overrides[get_review_store] = lambda: mock_review_store
    app.dependency_overrides[get_auth_service] = lambda: mock_auth_service
    app.dependency_overrides[get_current_user] = lambda: current_user
    yield TestClient(app)
    app.dependency_overrides = {}
