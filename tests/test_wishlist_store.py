import pytest
import json
from pathlib import Path
from app.services.wishlist_store import WishlistStore

@pytest.fixture
async def wishlist_store(tmp_path):
    file_path = tmp_path / "wishlist.json"
    store = WishlistStore(file_path)
    return store

@pytest.mark.asyncio
async def test_add_item_to_wishlist(wishlist_store):
    item = await wishlist_store.add(user="user1", item_id="skin_001", notes="Cool skin")

    assert item["item_id"] == "skin_001"
    assert item["notes"] == "Cool skin"

    assert wishlist_store.file_path.exists()
    data = json.loads(wishlist_store.file_path.read_text())
    assert "user1" in data
    assert data["user1"][0]["item_id"] == "skin_001"

@pytest.mark.asyncio
async def test_load_migration_logic(tmp_path):
    file_path = tmp_path / "old_wishlist.json"
    old_data = {"user1": ["skin_id_123"]}
    file_path.write_text(json.dumps(old_data))

    store = WishlistStore(file_path)
    await store.load()

    items = await store.get("user1")
    assert isinstance(items[0], dict)
    assert items[0]["item_id"] == "skin_id_123"
    assert items[0]["status"] == "active"

@pytest.mark.asyncio
async def test_remove_item(wishlist_store):
    await wishlist_store.add("user1", "item_a")
    await wishlist_store.remove("user1", "item_a")

    items = await wishlist_store.get("user1")
    assert len(items) == 0