def test_get_challenges_list(client):
    response = client.get("/api/challenges")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_challenge_not_found(client):
    response = client.get("/api/challenges/nonexistent")
    assert response.status_code == 404
