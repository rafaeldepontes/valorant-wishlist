import pytest
from app.services.user_store import UserStore

@pytest.fixture
def user_store():
    return UserStore()

def test_create_user_success(user_store):
    user_data = {"user_id": "user123", "name": "Sage"}
    result = user_store.create(user_data)

    assert result["user_id"] == "user123"
    assert result["status"] == "active"
    assert "created_at" in result
    assert user_store.get("user123") == result

def test_create_duplicate_user_raises_error(user_store):
    user_data = {"user_id": "user123"}
    user_store.create(user_data)
    with pytest.raises(ValueError, match="user already exists"):
        user_store.create(user_data)

def test_update_user(user_store):
    user_store.create({"user_id": "user1"})
    updated = user_store.update("user1", {"status": "banned"})
    assert updated["status"] == "banned"
    assert updated["updated_at"] is not None