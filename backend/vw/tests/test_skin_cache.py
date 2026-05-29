import pytest
import respx
from httpx import Response
from app.services.skin_cache import SkinCache

@pytest.fixture
def mock_api_data():
    return {
        "data": [
            {
                "displayName": "Vandal",
                "skins": [
                    {
                        "uuid": "vandal-uuid-1",
                        "displayName": "Reaver Vandal",
                        "displayIcon": "http://image.url"
                    }
                ]
            }
        ]
    }

@pytest.mark.asyncio
@respx.mock
async def test_refresh_skins(mock_api_data):
    respx.get("https://valorant-api.com/v1/weapons").mock(
        return_value=Response(200, json=mock_api_data)
    )

    cache = SkinCache()
    await cache.load()

    assert cache.len() == 1
    skin = await cache.get("vandal-uuid-1")
    assert skin["skin_name"] == "Reaver Vandal"
    assert skin["weapon_name"] == "Vandal"

@pytest.mark.asyncio
@respx.mock
async def test_ttl_expiry_triggers_refresh(mock_api_data):
    route = respx.get("https://valorant-api.com/v1/weapons").mock(
        return_value=Response(200, json=mock_api_data)
    )

    cache = SkinCache(ttl=-1)
    await cache.load()
    await cache.get("vandal-uuid-1")
    assert route.call_count == 2