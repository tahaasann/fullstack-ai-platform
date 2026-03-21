def test_get_progress_overview(client):
    response = client.get("/api/progress/overview")
    assert response.status_code == 200
    data = response.json()
    assert "overall_completion_percent" in data
    assert "current_streak_days" in data


def test_start_lesson(client):
    response = client.post("/api/progress/lesson/test-lesson/start")
    assert response.status_code == 200


def test_complete_lesson(client):
    response = client.post("/api/progress/lesson/test-lesson/complete")
    assert response.status_code == 200


def test_update_lesson_time(client):
    response = client.patch("/api/progress/lesson/test-lesson/time?seconds=60")
    assert response.status_code == 200


def test_update_lesson_time_invalid(client):
    """Seconds must be 0-86400"""
    response = client.patch("/api/progress/lesson/test-lesson/time?seconds=-1")
    assert response.status_code == 422


def test_update_lesson_time_too_large(client):
    response = client.patch("/api/progress/lesson/test-lesson/time?seconds=100000")
    assert response.status_code == 422


def test_start_and_complete_lesson_flow(client, seed_test_data):
    """Test the full lesson lifecycle: start -> update time -> complete"""
    # Start
    r1 = client.post("/api/progress/lesson/test-lesson/start")
    assert r1.status_code == 200

    # Update time
    r2 = client.patch("/api/progress/lesson/test-lesson/time?seconds=300")
    assert r2.status_code == 200

    # Complete
    r3 = client.post("/api/progress/lesson/test-lesson/complete")
    assert r3.status_code == 200

    # Verify in overview
    r4 = client.get("/api/progress/overview")
    assert r4.status_code == 200
    data = r4.json()
    assert data["lessons"]["completed"] >= 1


def test_daily_activity(client, seed_test_data):
    # Create some activity first
    client.post("/api/progress/lesson/test-lesson/start")
    client.patch("/api/progress/lesson/test-lesson/time?seconds=600")

    response = client.get("/api/progress/daily?days=7")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
