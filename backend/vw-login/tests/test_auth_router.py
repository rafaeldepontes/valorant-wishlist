def test_login_success(
    client,
    mock_user_store,
    mock_auth_service
):
    mock_user_store.get_by_username.return_value = {
        "username": "henry",
        "password": "hash"
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