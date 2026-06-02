import pytest
from uuid import uuid4

@pytest.mark.asyncio
async def test_login_success(
    client,
    mock_user_store,
    mock_auth_service
):
    mock_user_store.get_by_username.return_value = {
        "username": "henry",
        "password": "hashed_123456"
    }

    mock_auth_service.verify_password.return_value = True
    mock_auth_service.create_access_token.return_value = "jwt_token"

    response = client.post(
        "/auth/login",
        json={
            "username": "henry",
            "password": "123456"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["access_token"] == "jwt_token"
    assert data["token_type"] == "bearer"

    assert "access_token" in response.cookies
    set_cookie = response.headers.get("set-cookie")
    assert "access_token=" in set_cookie
    assert "jwt_token" in set_cookie
    assert "HttpOnly" in set_cookie
    assert "samesite=lax" in set_cookie.lower()

@pytest.mark.asyncio
async def test_login_invalid_credentials(client, mock_user_store, mock_auth_service):
    mock_user_store.get_by_username.return_value = None
    mock_user_store.get_by_email.return_value = None

    response = client.post(
        "/auth/login",
        json={"username": "wrong", "password": "password"}
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_logout_clears_cookie(client):
    client.cookies.set("access_token", "some_token")

    response = client.post("/auth/logout")
    assert response.status_code == 200

    assert "access_token" not in response.cookies or response.cookies.get("access_token") == ""

@pytest.mark.asyncio
async def test_register_success(client, mock_user_store, mock_auth_service):
    mock_user_store.create.return_value = {
        "uuid": uuid4(),
        "username": "newuser",
        "email": "new@example.com",
        "status": "active",
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z"
    }

    payload = {
        "username": "newuser",
        "email": "new@example.com",
        "password": "password123",
        "name": "New User"
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 201
    assert response.json()["username"] == "newuser"
    mock_user_store.create.assert_called_once()

@pytest.mark.asyncio
async def test_register_duplicate_username(client, mock_user_store):
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
