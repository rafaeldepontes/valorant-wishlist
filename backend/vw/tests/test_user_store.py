import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.user_store import UserStore

@pytest.fixture
def mock_session():
    return AsyncMock()

@pytest.fixture
def user_store(mock_session):
    return UserStore(mock_session)

@pytest.mark.asyncio
async def test_create_user_success(user_store, mock_session):
    user_data = {"username": "sage", "email": "sage@valorant.com", "name": "Sage"}

    mock_result = MagicMock()
    mock_result.first.return_value = None
    mock_session.exec.return_value = mock_result

    async def mock_refresh(obj):
        obj.id = 1
        obj.uuid = "uuid-123"

    mock_session.refresh.side_effect = mock_refresh

    result = await user_store.create(user_data)

    assert result["username"] == "sage"
    assert mock_session.add.called
    assert mock_session.commit.called

@pytest.mark.asyncio
async def test_create_duplicate_user_raises_error(user_store, mock_session):
    user_data = {"username": "sage"}

    mock_user = MagicMock()
    mock_user.model_dump.return_value = {"id": 1}

    mock_result = MagicMock()
    mock_result.first.return_value = mock_user
    mock_session.exec.return_value = mock_result

    with pytest.raises(ValueError, match="user already exists"):
        await user_store.create(user_data)
