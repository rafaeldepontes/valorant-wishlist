import pytest

@pytest.mark.asyncio
async def test_add_wishlist_success(client, mock_skin_cache, mock_wishlist_store):
    mock_skin_cache.get.return_value = {"weapon_name": "Vandal", "skin_name": "Prime"}
    mock_wishlist_store.add.return_value = {
        "notes": "test", "priority": 1, "notify_on_sale": False,
        "status": "active", "created_at": "now", "updated_at": "now"
    }

    payload = {"user_id": "u1", "item_id": "s1", "notes": "test"}
    response = client.post("/wishlist", json=payload)

    assert response.status_code == 201
    assert response.json()["weapon_name"] == "Vandal"

def test_add_wishlist_skin_not_found(client, mock_skin_cache):
    mock_skin_cache.get.return_value = None

    response = client.post("/wishlist", json={"user_id": "u1", "item_id": "bad"})
    assert response.status_code == 404
    assert response.json()["detail"] == "skin not found"

def test_delete_wishlist_item_missing(client, mock_wishlist_store):
    mock_wishlist_store.remove.side_effect = KeyError("item not found")

    response = client.delete("/wishlist/u1/s1")
    assert response.status_code == 404