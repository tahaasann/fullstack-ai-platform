import pytest
from datetime import date


def test_get_goal_defaults(client):
    """Default goal targets should return with default values"""
    response = client.get("/api/goals/defaults")
    assert response.status_code == 200
    data = response.json()
    assert data["target_lessons"] == 3
    assert data["target_quizzes"] == 1
    assert data["target_challenges"] == 2
    assert data["target_time_minutes"] == 120


def test_set_goal_defaults(client):
    """Setting custom goal defaults should persist"""
    response = client.put(
        "/api/goals/defaults?"
        "target_lessons=5&target_quizzes=3&target_challenges=4&target_time_minutes=180"
    )
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

    # Verify they persisted
    get_resp = client.get("/api/goals/defaults")
    data = get_resp.json()
    assert data["target_lessons"] == 5
    assert data["target_quizzes"] == 3
    assert data["target_challenges"] == 4
    assert data["target_time_minutes"] == 180


def test_set_goal_defaults_validation_negative(client):
    """Negative values should be rejected"""
    response = client.put("/api/goals/defaults?target_lessons=-1")
    assert response.status_code == 422


def test_set_goal_defaults_validation_too_large(client):
    """Values exceeding max should be rejected"""
    response = client.put("/api/goals/defaults?target_lessons=101")
    assert response.status_code == 422


def test_set_goal_defaults_time_validation(client):
    """Time > 1440 minutes (24h) should be rejected"""
    response = client.put("/api/goals/defaults?target_time_minutes=1441")
    assert response.status_code == 422


def test_get_today_goal(client):
    """Today's goal should auto-create with defaults"""
    response = client.get("/api/goals/today")
    assert response.status_code == 200
    data = response.json()
    assert data["date"] == date.today().isoformat()
    assert "targets" in data
    assert "progress" in data
    assert data["targets"]["lessons"] == 3
    assert data["targets"]["quizzes"] == 1
    assert data["targets"]["challenges"] == 2
    assert data["targets"]["time_minutes"] == 120
    assert data["progress"]["lessons"] == 0
    assert data["progress"]["quizzes"] == 0
    assert data["progress"]["challenges"] == 0
    assert data["completed"] is False


def test_update_today_goal(client):
    """Updating today's goal should change targets"""
    response = client.put(
        "/api/goals/today?"
        "target_lessons=10&target_quizzes=5&target_challenges=8&target_time_minutes=240"
    )
    assert response.status_code == 200

    # Verify
    get_resp = client.get("/api/goals/today")
    data = get_resp.json()
    assert data["targets"]["lessons"] == 10
    assert data["targets"]["quizzes"] == 5
    assert data["targets"]["challenges"] == 8
    assert data["targets"]["time_minutes"] == 240


def test_update_today_goal_validation(client):
    """Invalid values should be rejected"""
    response = client.put("/api/goals/today?target_lessons=-1")
    assert response.status_code == 422


def test_get_suggestions(client):
    """Suggestions endpoint should return list"""
    response = client.get("/api/goals/suggestions")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_suggestions_with_data(client, seed_test_data):
    """With seeded data, suggestions should include next lesson"""
    response = client.get("/api/goals/suggestions")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Should suggest the seeded lesson
    lesson_suggestions = [s for s in data if s["type"] == "lesson"]
    assert len(lesson_suggestions) >= 1


def test_goal_defaults_then_today_inherits(client):
    """Setting defaults, then getting today should use new defaults"""
    # Set custom defaults
    client.put(
        "/api/goals/defaults?"
        "target_lessons=7&target_quizzes=4&target_challenges=6&target_time_minutes=300"
    )

    # Get today (auto-creates with current defaults)
    response = client.get("/api/goals/today")
    data = response.json()
    assert data["targets"]["lessons"] == 7
    assert data["targets"]["quizzes"] == 4
    assert data["targets"]["challenges"] == 6
    assert data["targets"]["time_minutes"] == 300


def test_suggestions_max_five(client, seed_test_data):
    """Suggestions should return at most 5 items"""
    response = client.get("/api/goals/suggestions")
    data = response.json()
    assert len(data) <= 5
