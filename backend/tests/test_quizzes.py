import pytest
from unittest.mock import patch
from models import Quiz, QuizAttempt


@pytest.fixture
def seed_quiz_data(db, seed_test_data):
    """Seed test database with quiz data"""
    quiz = Quiz(
        id="test-quiz",
        module_id="test-module",
        title="Test Quiz",
        description="A test quiz",
        passing_score=70,
        content_path="test",
        order_index=1,
    )
    db.add(quiz)
    db.commit()
    return {"quiz": quiz}


def test_get_quiz_not_found(client):
    response = client.get("/api/quizzes/nonexistent")
    assert response.status_code == 404


def test_get_module_quizzes_empty(client):
    """Module quizzes should return empty list for nonexistent module"""
    response = client.get("/api/quizzes/module/nonexistent")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 0


def test_get_module_quizzes_with_data(client, seed_quiz_data):
    """Module quizzes should include seeded quiz"""
    response = client.get("/api/quizzes/module/test-module")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["id"] == "test-quiz"
    assert data[0]["title"] == "Test Quiz"
    assert data[0]["passing_score"] == 70
    assert data[0]["best_score"] is None
    assert data[0]["passed"] is False


def test_get_quiz_with_data(client, seed_quiz_data):
    """Get quiz should return quiz with questions stripped of answers"""
    with patch("routers.quizzes.load_quiz_content") as mock_load:
        mock_load.return_value = {
            "questions": [
                {
                    "id": "q1",
                    "type": "multiple_choice",
                    "question": "What is 1+1?",
                    "options": ["1", "2", "3"],
                    "answer": "2",  # this should be stripped
                    "points": 10,
                }
            ]
        }
        response = client.get("/api/quizzes/test-quiz")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "test-quiz"
        assert data["title"] == "Test Quiz"
        assert len(data["questions"]) == 1
        # Answer should NOT be in the response
        assert "answer" not in data["questions"][0]
        assert data["questions"][0]["question"] == "What is 1+1?"
        assert data["attempt_count"] == 0


def test_submit_quiz_not_found(client):
    """Submitting to nonexistent quiz should 404"""
    response = client.post("/api/quizzes/nonexistent/submit", json={
        "answers": {"q1": "2"},
        "time_spent_seconds": 60,
    })
    assert response.status_code == 404


def test_submit_quiz_with_data(client, seed_quiz_data):
    """Submitting quiz should evaluate and save attempt"""
    with patch("routers.quizzes.evaluate_quiz") as mock_eval:
        mock_eval.return_value = {
            "score": 100.0,
            "passed": True,
            "correct_count": 1,
            "total_count": 1,
            "results": [{"id": "q1", "correct": True}],
        }
        response = client.post("/api/quizzes/test-quiz/submit", json={
            "answers": {"q1": "2"},
            "time_spent_seconds": 45,
        })
        assert response.status_code == 200
        data = response.json()
        assert data["score"] == 100.0
        assert data["passed"] is True
        assert data["correct_count"] == 1
        assert data["total_count"] == 1
        assert data["attempt_number"] == 1


def test_submit_quiz_multiple_attempts(client, seed_quiz_data):
    """Multiple submissions should increment attempt count"""
    with patch("routers.quizzes.evaluate_quiz") as mock_eval:
        mock_eval.return_value = {
            "score": 50.0,
            "passed": False,
            "correct_count": 0,
            "total_count": 1,
            "results": [],
        }
        # First attempt
        r1 = client.post("/api/quizzes/test-quiz/submit", json={
            "answers": {"q1": "wrong"},
            "time_spent_seconds": 30,
        })
        assert r1.json()["attempt_number"] == 1

        # Second attempt
        r2 = client.post("/api/quizzes/test-quiz/submit", json={
            "answers": {"q1": "also_wrong"},
            "time_spent_seconds": 25,
        })
        assert r2.json()["attempt_number"] == 2


def test_quiz_attempts_history(client, seed_quiz_data):
    """Attempts history should list all attempts"""
    with patch("routers.quizzes.evaluate_quiz") as mock_eval:
        mock_eval.return_value = {
            "score": 80.0,
            "passed": True,
            "correct_count": 1,
            "total_count": 1,
            "results": [],
        }
        client.post("/api/quizzes/test-quiz/submit", json={
            "answers": {"q1": "2"},
            "time_spent_seconds": 60,
        })

    response = client.get("/api/quizzes/test-quiz/attempts")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["score"] == 80.0
    assert data[0]["passed"] is True


def test_quiz_best_score_in_listing(client, seed_quiz_data):
    """After submission, best score should appear in module listing"""
    with patch("routers.quizzes.evaluate_quiz") as mock_eval:
        mock_eval.return_value = {
            "score": 90.0,
            "passed": True,
            "correct_count": 1,
            "total_count": 1,
            "results": [],
        }
        client.post("/api/quizzes/test-quiz/submit", json={
            "answers": {"q1": "2"},
            "time_spent_seconds": 60,
        })

    response = client.get("/api/quizzes/module/test-module")
    data = response.json()
    assert data[0]["best_score"] == 90.0
    assert data[0]["passed"] is True


def test_submit_quiz_time_validation(client):
    """time_spent_seconds must be 0-86400"""
    response = client.post("/api/quizzes/test/submit", json={
        "answers": {},
        "time_spent_seconds": -1,
    })
    assert response.status_code == 422
