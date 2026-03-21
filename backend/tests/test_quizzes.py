def test_get_quiz_not_found(client):
    response = client.get("/api/quizzes/nonexistent")
    assert response.status_code == 404


def test_get_module_quizzes(client):
    response = client.get("/api/quizzes/module/nonexistent")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
