from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from models import Lesson, Challenge, Project, EnglishVocabulary
from schemas import (
    SearchResults, SearchLessonItem, SearchChallengeItem,
    SearchProjectItem, SearchVocabularyItem,
)

router = APIRouter()


@router.get("/search", response_model=SearchResults)
def search(q: str = Query(min_length=2, max_length=200), db: Session = Depends(get_db)) -> SearchResults:
    """Search across lessons, challenges, projects, and vocabulary."""
    if len(q) < 2:
        return SearchResults()

    term = f"%{q}%"

    lessons = db.query(Lesson).filter(
        (Lesson.title.ilike(term)) | (Lesson.description.ilike(term)) | (Lesson.tags.ilike(term))
    ).limit(10).all()

    challenges = db.query(Challenge).filter(
        (Challenge.title.ilike(term)) | (Challenge.description.ilike(term))
    ).limit(10).all()

    projects = db.query(Project).filter(
        (Project.title.ilike(term)) | (Project.description.ilike(term)) | (Project.tech_stack.ilike(term))
    ).limit(5).all()

    vocabulary = db.query(EnglishVocabulary).filter(
        (EnglishVocabulary.term.ilike(term)) | (EnglishVocabulary.translation.ilike(term))
    ).limit(10).all()

    return SearchResults(
        lessons=[SearchLessonItem(id=l.id, title=l.title, description=l.description, link=f"/lesson/{l.id}") for l in lessons],
        challenges=[SearchChallengeItem(id=c.id, title=c.title, difficulty=c.difficulty, link=f"/challenge/{c.id}") for c in challenges],
        projects=[SearchProjectItem(id=p.id, title=p.title, description=p.description, link=f"/project/{p.id}") for p in projects],
        vocabulary=[SearchVocabularyItem(id=v.id, term=v.term, translation=v.translation, link="/english") for v in vocabulary],
    )
