import pytest

@pytest.mark.asyncio
async def test_add_wishlist_success(client, mock_skin_cache, mock_wishlist_store, mock_user_store):
    mock_skin_cache.get.return_value = {"weapon_name": "Vandal", "skin_name": "Prime"}
    mock_user_store.get_internal_id.return_value = 1
    mock_wishlist_store.add.return_value = {
        "notes": "test", "priority": 1, "notify_on_sale": False,
        "status": "active", "created_at": "now", "updated_at": "now"
    }

    payload = {"user_id": "u1", "item_id": "s1", "notes": "test"}
    response = client.post("/wishlist", json=payload)

    assert response.status_code == 201
    assert response.json()["weapon_name"] == "Vandal"

@pytest.mark.asyncio
async def test_add_wishlist_forbidden(client, current_user):
    payload = {"user_id": "u2", "item_id": "s1"}
    response = client.post("/wishlist", json=payload)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_add_wishlist_skin_not_found(client, mock_skin_cache):
    mock_skin_cache.get.return_value = None

    response = client.post("/wishlist", json={"user_id": "u1", "item_id": "bad"})
    assert response.status_code == 404
    assert response.json()["detail"] == "skin not found"

@pytest.mark.asyncio
async def test_update_wishlist_forbidden(client, current_user):
    response = client.patch("/wishlist/u2/s1", json={"priority": 5})
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_delete_wishlist_forbidden(client, current_user):
    response = client.delete("/wishlist/u2/s1")
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_delete_wishlist_item_missing(client, mock_wishlist_store, mock_user_store):
    mock_user_store.get_internal_id.return_value = 1
    mock_wishlist_store.remove.side_effect = KeyError("item not found")

    response = client.delete("/wishlist/u1/s1")
    assert response.status_code == 404
