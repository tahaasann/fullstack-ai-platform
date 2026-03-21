from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Literal, Optional
from database import get_db
from models import Challenge, ChallengeAttempt, Module
from schemas import (
    ChallengeRunRequest, ChallengeListItem, ChallengeDetailOut,
    ChallengeRunResult, ChallengeHintsOut, ChallengeSolutionOut,
)
from services.challenge_runner import run_challenge
from services.lesson_loader import load_challenge_content
from services.progress_calculator import update_daily_activity
from datetime import datetime, timezone
import json

router = APIRouter()


@router.get("/challenges", response_model=list[ChallengeListItem])
def list_challenges(
    difficulty: Optional[Literal["easy", "medium", "hard"]] = None,
    category: Optional[str] = Query(default=None, max_length=100),
    module_id: Optional[str] = Query(default=None, max_length=100),
    db: Session = Depends(get_db)
) -> list[ChallengeListItem]:
    """Return filtered list of challenges with solved status."""
    query = db.query(Challenge)
    if difficulty:
        query = query.filter(Challenge.difficulty == difficulty)
    if category:
        query = query.filter(Challenge.category == category)
    if module_id:
        query = query.filter(Challenge.module_id == module_id)

    challenges = query.order_by(Challenge.order_index).all()
    result = []
    for ch in challenges:
        solved = db.query(ChallengeAttempt).filter(
            ChallengeAttempt.challenge_id == ch.id,
            ChallengeAttempt.status == "solved"
        ).first() is not None
        module = db.query(Module).filter(Module.id == ch.module_id).first()
        result.append(ChallengeListItem(
            id=ch.id,
            title=ch.title,
            description=ch.description,
            difficulty=ch.difficulty,
            category=ch.category,
            tags=json.loads(ch.tags) if ch.tags else [],
            module_id=ch.module_id,
            module_title=module.title if module else "",
            solved=solved,
        ))
    return result


@router.get("/challenges/{challenge_id}", response_model=ChallengeDetailOut)
def get_challenge(challenge_id: str, db: Session = Depends(get_db)) -> ChallengeDetailOut:
    """Return full challenge detail with examples and starter code."""
    ch = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not ch:
        raise HTTPException(status_code=404, detail="Challenge not found")

    content = load_challenge_content(ch.content_path)
    solved = db.query(ChallengeAttempt).filter(
        ChallengeAttempt.challenge_id == ch.id,
        ChallengeAttempt.status == "solved"
    ).first() is not None

    return ChallengeDetailOut(
        id=ch.id,
        title=content.get("title", ch.title),
        description=content.get("description_tr", ch.description),
        description_detail=content.get("description_detail", ""),
        difficulty=content.get("difficulty", ch.difficulty),
        category=content.get("category", ch.category),
        tags=json.loads(ch.tags) if ch.tags else [],
        examples=content.get("examples", []),
        constraints=content.get("constraints", []),
        starter_code=content.get("starter_code", {}),
        hints_available=len(content.get("hints", [])),
        solved=solved,
        complexity=content.get("complexity", {}),
        learn_after_solving=content.get("learn_after_solving", ""),
    )


@router.post("/challenges/{challenge_id}/run", response_model=ChallengeRunResult)
def run_challenge_code(challenge_id: str, req: ChallengeRunRequest, db: Session = Depends(get_db)) -> ChallengeRunResult:
    """Run challenge code against visible test cases."""
    ch = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not ch:
        raise HTTPException(status_code=404, detail="Challenge not found")

    result = run_challenge(ch.content_path, req.code, req.language, include_hidden=False)
    return ChallengeRunResult(**result)


@router.post("/challenges/{challenge_id}/submit", response_model=ChallengeRunResult)
def submit_challenge(challenge_id: str, req: ChallengeRunRequest, db: Session = Depends(get_db)) -> ChallengeRunResult:
    """Submit challenge solution against all test cases (including hidden)."""
    ch = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not ch:
        raise HTTPException(status_code=404, detail="Challenge not found")

    result = run_challenge(ch.content_path, req.code, req.language, include_hidden=True)

    status = "solved" if result["status"] == "passed" else "attempted"
    attempt = ChallengeAttempt(
        challenge_id=challenge_id,
        status=status,
        solution_code=req.code,
        language=req.language,
        tests_passed=result["tests_passed"],
        tests_total=result["tests_total"],
        attempted_at=datetime.now(timezone.utc)
    )
    db.add(attempt)
    db.commit()

    if status == "solved":
        update_daily_activity(db, challenges_delta=1)

    return ChallengeRunResult(**result)


@router.get("/challenges/{challenge_id}/hints", response_model=ChallengeHintsOut)
def get_hints(challenge_id: str, reveal: int = Query(default=1, ge=1, le=20), db: Session = Depends(get_db)) -> ChallengeHintsOut:
    """Return revealed hints for a challenge."""
    ch = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not ch:
        raise HTTPException(status_code=404, detail="Challenge not found")

    content = load_challenge_content(ch.content_path)
    hints = content.get("hints", [])
    return ChallengeHintsOut(hints=hints[:reveal], total=len(hints))


@router.get("/challenges/{challenge_id}/solution", response_model=ChallengeSolutionOut)
def get_solution(challenge_id: str, db: Session = Depends(get_db)) -> ChallengeSolutionOut:
    """Return challenge solution and explanation."""
    ch = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not ch:
        raise HTTPException(status_code=404, detail="Challenge not found")

    content = load_challenge_content(ch.content_path)
    return ChallengeSolutionOut(
        solution=content.get("solution", {}),
        complexity=content.get("complexity", {}),
        learn_after_solving=content.get("learn_after_solving", ""),
    )
