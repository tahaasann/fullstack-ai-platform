from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from models import LessonProgress, DailyActivity
from schemas import ProgressOverview, StatusResponse, TimeResponse, DailyActivityItem
from services.progress_calculator import get_overview, update_daily_activity
from datetime import datetime, timezone

router = APIRouter()


@router.get("/progress/overview", response_model=ProgressOverview)
def progress_overview(db: Session = Depends(get_db)) -> ProgressOverview:
    """Return overall progress overview with stats and streaks."""
    data = get_overview(db)
    return ProgressOverview(**data)


@router.post("/progress/lesson/{lesson_id}/start", response_model=StatusResponse)
def start_lesson(lesson_id: str, db: Session = Depends(get_db)) -> StatusResponse:
    """Mark a lesson as in-progress."""
    prog = db.query(LessonProgress).filter(LessonProgress.lesson_id == lesson_id).first()
    if not prog:
        prog = LessonProgress(
            lesson_id=lesson_id,
            status="in_progress",
            started_at=datetime.now(timezone.utc)
        )
        db.add(prog)
    elif prog.status == "not_started":
        prog.status = "in_progress"
        prog.started_at = datetime.now(timezone.utc)
    db.commit()
    return StatusResponse(status=prog.status)


@router.post("/progress/lesson/{lesson_id}/complete", response_model=StatusResponse)
def complete_lesson(lesson_id: str, db: Session = Depends(get_db)) -> StatusResponse:
    """Mark a lesson as completed."""
    prog = db.query(LessonProgress).filter(LessonProgress.lesson_id == lesson_id).first()
    if not prog:
        prog = LessonProgress(
            lesson_id=lesson_id,
            status="completed",
            started_at=datetime.now(timezone.utc),
            completed_at=datetime.now(timezone.utc)
        )
        db.add(prog)
    else:
        prog.status = "completed"
        prog.completed_at = datetime.now(timezone.utc)
    db.commit()
    update_daily_activity(db, lessons_delta=1)
    return StatusResponse(status="completed")


@router.patch("/progress/lesson/{lesson_id}/time", response_model=TimeResponse)
def update_lesson_time(
    lesson_id: str,
    seconds: int = Query(default=60, ge=0, le=86400),
    db: Session = Depends(get_db)
) -> TimeResponse:
    """Add time spent on a lesson."""
    prog = db.query(LessonProgress).filter(LessonProgress.lesson_id == lesson_id).first()
    if not prog:
        prog = LessonProgress(
            lesson_id=lesson_id,
            status="in_progress",
            started_at=datetime.now(timezone.utc),
            time_spent_seconds=seconds
        )
        db.add(prog)
    else:
        prog.time_spent_seconds = (prog.time_spent_seconds or 0) + seconds
    db.commit()
    update_daily_activity(db, time_delta=seconds)
    return TimeResponse(time_spent_seconds=prog.time_spent_seconds)


@router.get("/progress/daily", response_model=list[DailyActivityItem])
def get_daily_activity(days: int = Query(default=90, ge=1, le=365), db: Session = Depends(get_db)) -> list[DailyActivityItem]:
    """Return daily activity data for the heatmap."""
    from datetime import date, timedelta
    result = []
    for i in range(days):
        d = (date.today() - timedelta(days=days - 1 - i)).isoformat()
        act = db.query(DailyActivity).filter(DailyActivity.date == d).first()
        result.append(DailyActivityItem(
            date=d,
            seconds=act.total_time_seconds if act else 0,
            lessons=act.lessons_completed if act else 0,
            quizzes=act.quizzes_taken if act else 0,
            challenges=act.challenges_solved if act else 0,
        ))
    return result
