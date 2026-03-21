import pytest
from unittest.mock import patch


def test_get_challenges_list(client):
    response = client.get("/api/challenges")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_challenge_not_found(client):
    response = client.get("/api/challenges/nonexistent")
    assert response.status_code == 404


def test_get_challenges_filter_by_difficulty(client):
    """Filter challenges by difficulty should return 200"""
    response = client.get("/api/challenges?difficulty=easy")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_challenges_filter_by_category(client):
    """Filter challenges by category should return 200"""
    response = client.get("/api/challenges?category=algorithms")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_challenges_filter_invalid_difficulty(client):
    """Invalid difficulty value should be rejected by Literal validation"""
    response = client.get("/api/challenges?difficulty=impossible")
    assert response.status_code == 422


def test_challenge_run_not_found(client):
    """Running code for nonexistent challenge should 404"""
    response = client.post("/api/challenges/nonexistent/run", json={
        "code": "def solution(): return 1",
        "language": "python"
    })
    assert response.status_code == 404


def test_challenge_submit_not_found(client):
    """Submitting code for nonexistent challenge should 404"""
    response = client.post("/api/challenges/nonexistent/submit", json={
        "code": "def solution(): return 1",
        "language": "python"
    })
    assert response.status_code == 404


def test_challenge_run_invalid_language(client):
    """Invalid language should be rejected by Literal validation"""
    response = client.post("/api/challenges/any-id/run", json={
        "code": "fn main() {}",
        "language": "rust"
    })
    assert response.status_code == 422


def test_challenge_run_code_too_large(client):
    """Code exceeding 10KB max_length should be rejected"""
    large_code = "x" * 10241
    response = client.post("/api/challenges/any-id/run", json={
        "code": large_code,
        "language": "python"
    })
    assert response.status_code == 422


def test_challenge_hints_not_found(client):
    """Hints for nonexistent challenge should 404"""
    response = client.get("/api/challenges/nonexistent/hints")
    assert response.status_code == 404


def test_challenge_solution_not_found(client):
    """Solution for nonexistent challenge should 404"""
    response = client.get("/api/challenges/nonexistent/solution")
    assert response.status_code == 404


# --- Sandbox validation tests (unit-level, no DB needed) ---

from services.challenge_runner import validate_python_code, validate_js_code


def test_sandbox_blocks_dangerous_import_os():
    """Importing os module should be blocked"""
    is_safe, msg = validate_python_code("import os\nos.system('ls')")
    assert is_safe is False
    assert "os" in msg


def test_sandbox_blocks_dangerous_import_subprocess():
    """Importing subprocess module should be blocked"""
    is_safe, msg = validate_python_code("import subprocess")
    assert is_safe is False
    assert "subprocess" in msg


def test_sandbox_blocks_from_import():
    """From-import of dangerous module should be blocked"""
    is_safe, msg = validate_python_code("from os import path")
    assert is_safe is False
    assert "os" in msg


def test_sandbox_blocks_open_function():
    """open() function should be blocked"""
    is_safe, msg = validate_python_code("f = open('test.txt')")
    assert is_safe is False
    assert "open" in msg


def test_sandbox_blocks_exec_function():
    """exec() function should be blocked"""
    is_safe, msg = validate_python_code("exec('print(1)')")
    assert is_safe is False
    assert "exec" in msg


def test_sandbox_blocks_eval_function():
    """eval() function should be blocked"""
    is_safe, msg = validate_python_code("eval('1+1')")
    assert is_safe is False
    assert "eval" in msg


def test_sandbox_allows_safe_code():
    """Normal Python code should pass validation"""
    is_safe, msg = validate_python_code("def add(a, b):\n    return a + b")
    assert is_safe is True
    assert msg == ""


def test_sandbox_allows_safe_imports():
    """Safe imports like math, json should pass"""
    is_safe, msg = validate_python_code("import math\nimport json\nimport collections")
    assert is_safe is True


def test_sandbox_syntax_error_passes():
    """Code with syntax errors should pass validation (caught at runtime)"""
    is_safe, msg = validate_python_code("def foo(:\n    pass")
    assert is_safe is True


def test_js_sandbox_blocks_fs():
    """JS require('fs') should be blocked"""
    is_safe, msg = validate_js_code("const fs = require('fs')")
    assert is_safe is False
    assert "fs" in msg


def test_js_sandbox_blocks_child_process():
    """JS require('child_process') should be blocked"""
    is_safe, msg = validate_js_code("const cp = require('child_process')")
    assert is_safe is False
    assert "child_process" in msg


def test_js_sandbox_blocks_process_exit():
    """JS process.exit should be blocked"""
    is_safe, msg = validate_js_code("process.exit(1)")
    assert is_safe is False


def test_js_sandbox_allows_safe_code():
    """Normal JS code should pass validation"""
    is_safe, msg = validate_js_code("function add(a, b) { return a + b; }")
    assert is_safe is True
    assert msg == ""


def test_challenge_run_with_seeded_data(client, db, seed_test_data):
    """Run endpoint with a seeded challenge and mocked runner"""
    from models import Challenge

    ch = Challenge(
        id="test-challenge",
        module_id="test-module",
        title="Test Challenge",
        description="Test",
        difficulty="easy",
        category="basics",
        content_path="test",
        order_index=1,
        tags='["python"]',
    )
    db.add(ch)
    db.commit()

    with patch("routers.challenges.run_challenge") as mock_run:
        mock_run.return_value = {
            "status": "passed",
            "tests_passed": 2,
            "tests_total": 2,
            "results": [],
            "execution_time_ms": 50,
        }
        response = client.post("/api/challenges/test-challenge/run", json={
            "code": "def solution(x): return x * 2",
            "language": "python"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "passed"
        assert data["tests_passed"] == 2
