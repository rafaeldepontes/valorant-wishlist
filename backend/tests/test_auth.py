import pytest

@pytest.mark.asyncio
async def test_register_duplicate_username(client, mock_user_store, mock_auth_service):
    mock_auth_service.hash_password.return_value = "hashed"
    mock_user_store.create.side_effect = ValueError("user already exists")

    payload = {
        "username": "duplicate",
        "email": "new@example.com",
        "password": "password123",
        "name": "New User"
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 409
    assert response.json()["detail"] == "user already exists"

@pytest.mark.asyncio
async def test_login_invalid_credentials(client, mock_user_store, mock_auth_service):
    mock_user_store.get_by_username.return_value = {
        "username": "testuser",
        "password": "hashed_password"
    }
    mock_auth_service.verify_password.return_value = False

    payload = {"username": "testuser", "password": "wrongpassword"}
    response = client.post("/auth/login", json=payload)
    assert response.status_code == 401
    assert response.json()["detail"] == "invalid username and/or password"

@pytest.mark.asyncio
async def test_login_user_not_found(client, mock_user_store):
    mock_user_store.get_by_username.return_value = None
    mock_user_store.get_by_email.return_value = None

    payload = {"username": "nonexistent", "password": "password123"}
    response = client.post("/auth/login", json=payload)
    assert response.status_code == 401
