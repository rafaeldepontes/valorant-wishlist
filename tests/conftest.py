import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.api.deps import get_user_store, get_wishlist_store, get_skin_cache

@pytest.fixture
def mock_user_store():
    return MagicMock()

@pytest.fixture
def mock_wishlist_store():
    return AsyncMock()

@pytest.fixture
def mock_skin_cache():
    mock = AsyncMock()
    mock.len = MagicMock(return_value=0)
    return mock

@pytest.fixture
def client(mock_user_store, mock_wishlist_store, mock_skin_cache):
    app.dependency_overrides[get_user_store] = lambda: mock_user_store
    app.dependency_overrides[get_wishlist_store] = lambda: mock_wishlist_store
    app.dependency_overrides[get_skin_cache] = lambda: mock_skin_cache
    yield TestClient(app)
    app.dependency_overrides = {}
