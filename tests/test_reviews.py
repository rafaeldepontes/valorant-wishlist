import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.api.deps import review_store_singleton, user_store_singleton, skin_cache_singleton

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_data():
    # Clear store
    review_store_singleton.data = {}
    
    # Create a user for testing
    user_store_singleton.data = {}
    user_store_singleton.create({
        "user_id": "test-user",
        "username": "testuser",
        "email": "test@example.com",
        "bio": "test bio"
    })
    
    # Ensure skin cache has something (mock or wait for load)
    # We'll assume a skin ID exists from the real API for simplicity in this integration test
    # or we can mock skin_cache_singleton.exists
    pass

def test_create_review():
    # Mock skin existence
    skin_id = "4e459b3b-4dab-934f-1d77-bdbe75b6fcca"
    
    # We need to make sure the skin is in cache for enrichment
    # For testing, we can manually inject it
    skin_cache_singleton.data[skin_id] = {
        "weapon_name": "Vandal",
        "skin_id": skin_id,
        "skin_name": "Reaver Vandal",
        "image": None
    }

    response = client.post(
        "/reviews",
        json={
            "user_id": "test-user",
            "item_id": skin_id,
            "rating": 5,
            "comment": "Amazing!",
            "is_anonymous": False
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["rating"] == 5
    assert data["comment"] == "Amazing!"
    assert data["username"] == "testuser"
    assert data["weapon_name"] == "Vandal"

def test_get_skin_reviews():
    skin_id = "skin-1"
    review_store_singleton.create({
        "user_id": "test-user",
        "item_id": skin_id,
        "rating": 4,
        "comment": "Good",
        "is_anonymous": True
    })

    response = client.get(f"/reviews/skin/{skin_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["rating"] == 4
    assert data[0]["username"] is None  # Anonymous

def test_delete_review():
    record = review_store_singleton.create({
        "user_id": "test-user",
        "item_id": "skin-1",
        "rating": 3,
        "comment": "Meh",
        "is_anonymous": False
    })
    review_id = record["review_id"]

    response = client.delete(f"/reviews/{review_id}")
    assert response.status_code == 204
    assert review_id not in review_store_singleton.data
