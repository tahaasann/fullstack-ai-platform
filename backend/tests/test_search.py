def test_search_empty_query(client):
    response = client.get("/api/search?q=test")
    assert response.status_code == 200
