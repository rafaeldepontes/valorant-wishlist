import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.wishlist_store import WishlistStore

@pytest.fixture
def mock_session():
    return AsyncMock()

@pytest.fixture
def wishlist_store(mock_session):
    return WishlistStore(mock_session)

@pytest.mark.asyncio
async def test_add_item_to_wishlist(wishlist_store, mock_session):
    mock_result = MagicMock()
    mock_result.first.return_value = None
    mock_session.exec.return_value = mock_result

    async def mock_refresh(obj):
        obj.id = 1
        obj.status = "active"
        obj.created_at = "now"
        obj.updated_at = "now"

    mock_session.refresh.side_effect = mock_refresh

    item = await wishlist_store.add(user_id=1, item_id="skin_001", notes="Cool skin")

    assert item["item_id"] == "skin_001"
    assert item["notes"] == "Cool skin"
    assert mock_session.add.called
    assert mock_session.commit.called

@pytest.mark.asyncio
async def test_remove_item(wishlist_store, mock_session):
    mock_item = MagicMock()
    mock_session.get.return_value = mock_item

    # We need to mock the find logic if remove uses it
    # Actually looking at wishlist_store.py remove:
    # async def remove(self, user_id: int, item_id: str) -> None:
    #     statement = select(WishlistItem).where(WishlistItem.user_id == user_id, WishlistItem.item_id == item_id)
    #     results = await self.session.exec(statement)
    #     record = results.first()

    mock_result = MagicMock()
    mock_result.first.return_value = {"id": 1}
    mock_session.exec.return_value = mock_result

    await wishlist_store.remove(1, "item_a")
    assert mock_session.delete.called
    assert mock_session.commit.called
