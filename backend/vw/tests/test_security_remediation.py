import pytest
from httpx import Response

@pytest.mark.asyncio
async def test_login_sets_cookie(client, mock_user_store, mock_auth_service):
    mock_user_store.get_by_username.return_value = {
        "id": 1,
        "uuid": "550e8400-e29b-41d4-a716-446655440000",
        "username": "testuser",
        "password": "hashed_password"
    }
    mock_auth_service.verify_password.return_value = True
    mock_auth_service.create_access_token.return_value = "mock_token"

    payload = {"username": "testuser", "password": "password123"}
    response = client.post("/auth/login", json=payload)

    assert response.status_code == 200
    assert "access_token" in response.cookies
    assert response.cookies["access_token"] == "mock_token"

@pytest.mark.asyncio
async def test_logout_clears_cookie(client):
    client.cookies.set("access_token", "some_token")

    response = client.post("/auth/logout")
    assert response.status_code == 200
    assert "access_token" not in response.cookies or response.cookies["access_token"] == ""

@pytest.mark.asyncio
async def test_security_headers(client):
    response = client.get("/")
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert "Content-Security-Policy" in response.headers
