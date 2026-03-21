def test_get_bookmarks_empty(client):
    response = client.get("/api/bookmarks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_check_bookmark(client):
    response = client.get("/api/bookmarks/check?item_type=lesson&item_id=test")
    assert response.status_code == 200
    data = response.json()
    assert "bookmarked" in data


def test_bookmark_lifecycle(client, seed_test_data):
    """Create, check, list, and delete a bookmark"""
    # Create
    r1 = client.post("/api/bookmarks?item_type=lesson&item_id=test-lesson&note=test")
    assert r1.status_code == 200
    bookmark_id = r1.json().get("id")

    # Check
    r2 = client.get("/api/bookmarks/check?item_type=lesson&item_id=test-lesson")
    assert r2.status_code == 200
    assert r2.json()["bookmarked"] == True

    # List
    r3 = client.get("/api/bookmarks")
    assert r3.status_code == 200
    assert len(r3.json()) >= 1

    # Delete
    if bookmark_id:
        r4 = client.delete(f"/api/bookmarks/{bookmark_id}")
        assert r4.status_code == 200
