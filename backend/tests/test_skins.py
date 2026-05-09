def test_read_skins_success(client, mock_skin_cache):
    mock_skin_cache.len.return_value = 1
    mock_skin_cache.list = [{"skin_name": "Reaver"}]

    response = client.get("/skins")
    assert response.status_code == 200
    assert response.json() == [{"skin_name": "Reaver"}]

def test_read_skins_trigger_load(client, mock_skin_cache):
    mock_skin_cache.len.return_value = 0
    mock_skin_cache.list = []

    client.get("/skins")

    mock_skin_cache.load.assert_awaited_once()