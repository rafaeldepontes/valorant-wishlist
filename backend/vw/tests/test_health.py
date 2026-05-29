def test_health_check_success(client):
    response = client.get("/health-check")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}