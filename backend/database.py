from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.exc import OperationalError
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "education.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def run_migrations():
    """Add missing columns to existing tables (SQLite compatible)."""
    new_columns = [
        ("english_vocabulary", "definition_en", "TEXT"),
        ("english_vocabulary", "definition_tr", "TEXT"),
        ("english_vocabulary", "difficulty_level", "VARCHAR"),
        ("english_vocabulary", "usage_context", "TEXT"),
        ("english_vocabulary", "common_patterns", "TEXT"),
        ("english_vocabulary", "scenario", "TEXT"),
        ("english_vocabulary", "related_terms", "TEXT"),
        ("english_vocabulary", "common_mistakes", "TEXT"),
        ("english_vocabulary", "example_sentences", "TEXT"),
    ]

    with engine.connect() as conn:
        for table, column, col_type in new_columns:
            try:
                conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}"))
                conn.commit()
            except OperationalError:
                # Column already exists
                pass
