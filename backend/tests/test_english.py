def test_get_vocabulary_empty(client):
    response = client.get("/api/english/vocabulary")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_vocabulary_with_domain(client):
    response = client.get("/api/english/vocabulary?domain=programming")
    assert response.status_code == 200


def test_get_scenarios(client):
    response = client.get("/api/english/scenarios")
    assert response.status_code == 200


def test_get_patterns(client):
    response = client.get("/api/english/patterns")
    assert response.status_code == 200


def test_get_english_progress(client):
    response = client.get("/api/english/progress")
    assert response.status_code == 200
