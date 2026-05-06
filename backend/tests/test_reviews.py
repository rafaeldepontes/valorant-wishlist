import pytest
from unittest.mock import MagicMock
from uuid import uuid4

@pytest.mark.asyncio
async def test_create_review_success(client, mock_review_store, mock_user_store, mock_skin_cache):
    mock_user_store.get.return_value = {"id": 1, "uuid": "u1", "username": "testuser"}
    mock_skin_cache.get.return_value = {"weapon_name": "Vandal", "skin_name": "Reaver"}

    mock_review_store.create.return_value = {
        "uuid": uuid4(),
        "user_id": 1,
        "item_id": "s1",
        "rating": 5,
        "comment": "Nice",
        "is_anonymous": False,
        "created_at": "now",
        "updated_at": "now"
    }

    mock_result = MagicMock()
    mock_result.first.return_value = MagicMock(uuid="u1", username="testuser")
    mock_user_store.session.exec.return_value = mock_result

    payload = {
        "user_id": "u1",
        "item_id": "s1",
        "rating": 5,
        "comment": "Nice",
        "is_anonymous": False
    }
    response = client.post("/reviews", json=payload)
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"

@pytest.mark.asyncio
async def test_create_review_forbidden(client, current_user):
    payload = {
        "user_id": "u2",
        "item_id": "s1",
        "rating": 5,
        "comment": "forbidden",
        "is_anonymous": False
    }
    response = client.post("/reviews", json=payload)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_update_review_forbidden(client, mock_review_store):
    mock_review_store.update.side_effect = PermissionError("not enough permissions")

    response = client.patch("/reviews/r1", json={"rating": 1})
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_update_anonymous_review_forbidden(client, mock_review_store):
    # ReviewStore.update raises PermissionError for anonymous reviews
    mock_review_store.update.side_effect = PermissionError("not enough permissions")

    response = client.patch("/reviews/r_anon", json={"rating": 1})
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_delete_review_not_found(client, mock_review_store):
    mock_review_store.delete.side_effect = KeyError("review not found")

    response = client.delete("/reviews/invalid")
    assert response.status_code == 404
