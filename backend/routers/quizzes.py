from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Quiz, QuizAttempt
from schemas import QuizSubmit, QuizListItem, QuizOut, QuizResultOut, QuizAttemptOut
from services.quiz_evaluator import evaluate_quiz
from services.lesson_loader import load_quiz_content
from services.progress_calculator import update_daily_activity
from datetime import datetime, timezone
import json

router = APIRouter()


@router.get("/quizzes/module/{module_id}", response_model=list[QuizListItem])
def get_module_quizzes(module_id: str, db: Session = Depends(get_db)) -> list[QuizListItem]:
    """Return all quizzes for a module with best scores."""
    quizzes = db.query(Quiz).filter(Quiz.module_id == module_id).order_by(Quiz.order_index).all()
    result = []
    for q in quizzes:
        best = db.query(QuizAttempt).filter(
            QuizAttempt.quiz_id == q.id
        ).order_by(QuizAttempt.score.desc()).first()
        result.append(QuizListItem(
            id=q.id,
            title=q.title,
            description=q.description,
            passing_score=q.passing_score,
            best_score=best.score if best else None,
            passed=best.passed if best else False,
        ))
    return result


@router.get("/quizzes/{quiz_id}", response_model=QuizOut)
def get_quiz(quiz_id: str, db: Session = Depends(get_db)) -> QuizOut:
    """Return quiz with questions (answers stripped) and attempt stats."""
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    content = load_quiz_content(quiz.content_path)
    # Strip answers from questions
    questions = []
    for q in content.get("questions", []):
        safe_q = {
            "id": q["id"],
            "type": q["type"],
            "question": q.get("question", ""),
            "options": q.get("options", []),
            "code": q.get("code", ""),
            "code_template": q.get("code_template", ""),
            "steps": q.get("steps", []),
            "difficulty": q.get("difficulty", ""),
            "points": q.get("points", 10)
        }
        questions.append(safe_q)

    # Get best score
    best = db.query(QuizAttempt).filter(
        QuizAttempt.quiz_id == quiz_id
    ).order_by(QuizAttempt.score.desc()).first()

    attempts = db.query(QuizAttempt).filter(QuizAttempt.quiz_id == quiz_id).count()

    return QuizOut(
        id=quiz.id,
        module_id=quiz.module_id,
        title=quiz.title,
        description=quiz.description,
        passing_score=quiz.passing_score,
        questions=questions,
        best_score=best.score if best else None,
        attempt_count=attempts,
    )


@router.post("/quizzes/{quiz_id}/submit", response_model=QuizResultOut)
def submit_quiz(quiz_id: str, submission: QuizSubmit, db: Session = Depends(get_db)) -> QuizResultOut:
    """Submit quiz answers and get evaluation results."""
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    result = evaluate_quiz(quiz.content_path, submission.answers)

    # Save attempt
    attempt = QuizAttempt(
        quiz_id=quiz_id,
        score=result["score"],
        answers=json.dumps(submission.answers),
        correct_count=result["correct_count"],
        total_count=result["total_count"],
        passed=result["passed"],
        attempted_at=datetime.now(timezone.utc),
        time_spent_seconds=submission.time_spent_seconds
    )
    db.add(attempt)
    db.commit()

    update_daily_activity(db, quizzes_delta=1)

    attempt_count = db.query(QuizAttempt).filter(QuizAttempt.quiz_id == quiz_id).count()

    return QuizResultOut(**result, attempt_number=attempt_count)


@router.get("/quizzes/{quiz_id}/attempts", response_model=list[QuizAttemptOut])
def get_quiz_attempts(quiz_id: str, db: Session = Depends(get_db)) -> list[QuizAttemptOut]:
    """Return all attempts for a quiz, newest first."""
    attempts = db.query(QuizAttempt).filter(
        QuizAttempt.quiz_id == quiz_id
    ).order_by(QuizAttempt.attempted_at.desc()).all()

    return [QuizAttemptOut(
        id=a.id,
        score=a.score,
        passed=a.passed,
        correct_count=a.correct_count,
        total_count=a.total_count,
        attempted_at=a.attempted_at.isoformat() if a.attempted_at else None,
        time_spent_seconds=a.time_spent_seconds,
    ) for a in attempts]
