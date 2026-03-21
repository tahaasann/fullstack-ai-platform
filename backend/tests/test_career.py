def test_get_linkedin_guide(client):
    response = client.get("/api/career/linkedin-guide")
    assert response.status_code == 200
    data = response.json()
    assert "title" in data or "sections" in data or isinstance(data, dict)


def test_get_cv_templates(client):
    response = client.get("/api/career/cv-templates")
    assert response.status_code == 200


def test_get_job_search_strategy(client):
    response = client.get("/api/career/job-search-strategy")
    assert response.status_code == 200


def test_get_employment_gap_guide(client):
    response = client.get("/api/career/employment-gap-guide")
    assert response.status_code == 200


def test_get_ai_tools_guide(client):
    response = client.get("/api/career/ai-tools-guide")
    assert response.status_code == 200


def test_get_cover_letter_templates(client):
    response = client.get("/api/career/cover-letter-templates")
    assert response.status_code == 200


def test_get_github_profile_guide(client):
    response = client.get("/api/career/github-profile-guide")
    assert response.status_code == 200
