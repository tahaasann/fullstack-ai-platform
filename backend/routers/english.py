from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import EnglishVocabulary, EnglishExercise, SentencePattern, WorkScenario
from schemas import (
    VocabularyDetailOut, LearnedResponse, PatternOut,
    ScenarioOut, EnglishProgressOut,
)
from datetime import datetime, timezone
import json
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


def safe_json_loads(value, fallback=None):
    """Safely parse JSON string, returning fallback on failure."""
    if fallback is None:
        fallback = []
    if not value:
        return fallback
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        logger.warning(f"Malformed JSON data: {value[:100] if isinstance(value, str) else value}")
        return fallback


@router.get("/english/vocabulary", response_model=list[VocabularyDetailOut])
def get_vocabulary(domain: str = None, learned: bool = None, db: Session = Depends(get_db)) -> list[VocabularyDetailOut]:
    """Return vocabulary items, optionally filtered by domain or learned status."""
    query = db.query(EnglishVocabulary)
    if domain:
        query = query.filter(EnglishVocabulary.domain == domain)
    if learned is not None:
        query = query.filter(EnglishVocabulary.learned == learned)
    items = query.order_by(EnglishVocabulary.id).all()

    result = []
    for v in items:
        result.append(VocabularyDetailOut(
            id=v.id,
            term=v.term,
            translation=v.translation,
            pronunciation=v.pronunciation,
            example_sentence=v.example_sentence,
            domain=v.domain,
            lesson_id=v.lesson_id,
            learned=v.learned,
            review_count=v.review_count,
            definition_en=v.definition_en,
            definition_tr=v.definition_tr,
            difficulty_level=v.difficulty_level,
            usage_context=v.usage_context,
            common_patterns=safe_json_loads(v.common_patterns),
            scenario=v.scenario,
            related_terms=safe_json_loads(v.related_terms),
            common_mistakes=v.common_mistakes,
            example_sentences=safe_json_loads(v.example_sentences),
        ))
    return result


@router.post("/english/vocabulary/{vocab_id}/learned", response_model=LearnedResponse)
def mark_learned(vocab_id: int, db: Session = Depends(get_db)) -> LearnedResponse:
    """Mark a vocabulary item as learned."""
    vocab = db.query(EnglishVocabulary).filter(EnglishVocabulary.id == vocab_id).first()
    if vocab:
        vocab.learned = True
        vocab.review_count = (vocab.review_count or 0) + 1
        db.commit()
    return LearnedResponse(learned=True)


@router.get("/english/patterns", response_model=list[PatternOut])
def get_patterns(domain: str = None, db: Session = Depends(get_db)) -> list[PatternOut]:
    """Return sentence patterns, optionally filtered by domain."""
    query = db.query(SentencePattern)
    if domain:
        query = query.filter(SentencePattern.domain == domain)
    items = query.order_by(SentencePattern.order_index).all()

    result = []
    for p in items:
        result.append(PatternOut(
            id=p.id,
            domain=p.domain,
            category=p.category,
            pattern=p.pattern,
            turkish=p.turkish,
            when_to_use=p.when_to_use,
            variations=safe_json_loads(p.variations),
            real_example=p.real_example,
        ))
    return result


@router.get("/english/scenarios", response_model=list[ScenarioOut])
def get_scenarios(domain: str = None, db: Session = Depends(get_db)) -> list[ScenarioOut]:
    """Return work scenarios, optionally filtered by domain."""
    query = db.query(WorkScenario)
    if domain:
        query = query.filter(WorkScenario.domain == domain)
    items = query.order_by(WorkScenario.order_index).all()

    result = []
    for s in items:
        result.append(ScenarioOut(
            id=s.id_str,
            title=s.title,
            context=s.context,
            dialogue=safe_json_loads(s.dialogue),
            key_phrases=safe_json_loads(s.key_phrases),
            cultural_note=s.cultural_note,
            domain=s.domain,
        ))
    return result


@router.get("/english/progress", response_model=EnglishProgressOut)
def english_progress(db: Session = Depends(get_db)) -> EnglishProgressOut:
    """Return English learning progress stats."""
    total = db.query(func.count(EnglishVocabulary.id)).scalar() or 0
    learned = db.query(func.count(EnglishVocabulary.id)).filter(
        EnglishVocabulary.learned == True
    ).scalar() or 0

    # Terms by domain
    domains_raw = db.query(
        EnglishVocabulary.domain,
        func.count(EnglishVocabulary.id)
    ).group_by(EnglishVocabulary.domain).all()

    terms_by_domain = {}
    for domain, count in domains_raw:
        learned_in_domain = db.query(func.count(EnglishVocabulary.id)).filter(
            EnglishVocabulary.domain == domain,
            EnglishVocabulary.learned == True
        ).scalar() or 0
        terms_by_domain[domain or "general"] = {
            "total": count,
            "learned": learned_in_domain
        }

    # Exercises
    exercises_completed = db.query(func.count(EnglishExercise.id)).scalar() or 0
    avg_score = db.query(func.avg(EnglishExercise.score)).scalar() or 0

    # Due for review
    now = datetime.now(timezone.utc)
    due = db.query(func.count(EnglishVocabulary.id)).filter(
        EnglishVocabulary.learned == True,
        EnglishVocabulary.next_review_at <= now
    ).scalar() or 0

    # Pattern & scenario counts
    total_patterns = db.query(func.count(SentencePattern.id)).scalar() or 0
    total_scenarios = db.query(func.count(WorkScenario.id_str)).scalar() or 0

    return EnglishProgressOut(
        total_terms=total,
        learned_terms=learned,
        terms_by_domain=terms_by_domain,
        exercises_completed=exercises_completed,
        average_score=round(avg_score, 1),
        due_for_review=due,
        total_patterns=total_patterns,
        total_scenarios=total_scenarios,
    )
