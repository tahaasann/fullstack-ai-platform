import sys
import os

# Add backend directory to sys.path so bare imports (from database import ...) work
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from database import Base, get_db
from main import app

# Test database (in-memory SQLite)
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def seed_test_data(db):
    """Seed the test database with sample data for positive-path tests"""
    from models import Phase, Module, Lesson

    phase = Phase(id="test-phase", title="Test Phase", description="Test", order_index=1, estimated_weeks="1", icon="📚")
    db.add(phase)

    module = Module(id="test-module", phase_id="test-phase", title="Test Module", description="Test", order_index=1, estimated_hours=5)
    db.add(module)

    lesson = Lesson(id="test-lesson", module_id="test-module", title="Test Lesson", description="Test", order_index=1, estimated_minutes=30, tags='["test","python"]', content_path="test")
    db.add(lesson)

    db.commit()
    return {"phase": phase, "module": module, "lesson": lesson}
