import pytest

@pytest.mark.asyncio
async def test_security_headers(client):
    response = client.get("/")
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["X-XSS-Protection"] == "1; mode=block"
    assert response.headers["Strict-Transport-Security"] == "max-age=31536000; includeSubDomains"
    assert "Content-Security-Policy" in response.headers

@pytest.mark.asyncio
async def test_rate_limiting(client, mock_user_store):
    payload = {"username": "test", "password": "password"}

    for _ in range(3):
        client.post("/auth/login", json=payload)

    response = client.post("/auth/login", json=payload)
    assert response.status_code == 429
