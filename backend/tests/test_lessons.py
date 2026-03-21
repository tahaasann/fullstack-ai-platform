def test_get_phases_empty(client):
    """Phases should return empty list when no data indexed"""
    response = client.get("/api/phases")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_phase_not_found(client):
    response = client.get("/api/phases/nonexistent")
    assert response.status_code == 404


def test_get_module_not_found(client):
    response = client.get("/api/modules/nonexistent")
    assert response.status_code == 404


def test_get_lesson_not_found(client):
    response = client.get("/api/lessons/nonexistent")
    assert response.status_code == 404


def test_get_phases_with_data(client, seed_test_data):
    response = client.get("/api/phases")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["title"] == "Test Phase"


def test_get_phase_with_data(client, seed_test_data):
    response = client.get("/api/phases/test-phase")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Phase"
    assert "modules" in data


def test_get_module_with_data(client, seed_test_data):
    response = client.get("/api/modules/test-module")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Module"
    assert "lessons" in data
