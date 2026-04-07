def test_get_user_success(client, mock_user_store, mock_wishlist_store):
    mock_user_store.get.return_value = {
        "user_id": "u1",
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

def test_get_user_not_found(client, mock_user_store):
    mock_user_store.get.side_effect = KeyError("user not found")

    response = client.get("/users/invalid")
    assert response.status_code == 404
    assert response.json()["detail"] == "'user not found'"

def test_create_user_duplicate(client, mock_user_store):
    mock_user_store.create.side_effect = ValueError("user already exists")

    payload = {
        "user_id": "u1",
        "name": "Sage",
        "username": "sage_main",
        "email": "sage@valorant.com",
        "bio": "I am the shield."
    }
    response = client.post("/users", json=payload)
    assert response.status_code == 409