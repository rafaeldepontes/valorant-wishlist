import pytest

@pytest.mark.asyncio
async def test_get_user_success(client, mock_user_store, mock_wishlist_store):
    mock_user_store.get.return_value = {
        "id": 1,
        "uuid": "u1",
        "name": "Sage",
        "username": "sage_main",
        "email": "sage@valorant.com",
        "status": "active",
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00",
        "bio": "I am the shield."
    }
    mock_wishlist_store.get.return_value = [{}, {}]

    response = client.get("/users/u1")
    assert response.status_code == 200
    assert response.json()["wishlist_count"] == 2

@pytest.mark.asyncio
async def test_get_user_not_found(client, mock_user_store):
    mock_user_store.get.side_effect = KeyError("user not found")

    response = client.get("/users/invalid")
    assert response.status_code == 404
    assert response.json()["detail"] == "'user not found'"

@pytest.mark.asyncio
async def test_update_user_forbidden(client, current_user):
    response = client.patch("/users/u2", json={"name": "New Name"})
    assert response.status_code == 403
    assert response.json()["detail"] == "not enough permissions"

@pytest.mark.asyncio
async def test_get_users_me(client, current_user, mock_wishlist_store):
    mock_wishlist_store.get.return_value = []
    response = client.get("/users/me")
    assert response.status_code == 200
    assert response.json()["user_id"] == "u1"
