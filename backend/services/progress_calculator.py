from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from models import (
    Phase, Module, Lesson, Quiz, Challenge, Project, ProjectMilestone,
    LessonProgress, QuizAttempt, ChallengeAttempt, ProjectProgress,
    MilestoneProgress, DailyActivity, EnglishVocabulary, EnglishExercise
)
from datetime import datetime, timedelta, timezone, date

# Weights for overall completion calculation
_COMPLETION_WEIGHTS = {
    "lesson": 0.35,
    "quiz": 0.20,
    "challenge": 0.15,
    "milestone": 0.20,
    "english": 0.10,
}


def _safe_pct(completed: int, total: int) -> float:
    """Return percentage, guarding against division by zero."""
    return (completed / total * 100) if total > 0 else 0


def _query_completion_stats(db: Session) -> dict:
    """Query all completion counts from the database.

    Returns:
        A dict with raw counts for lessons, quizzes, challenges,
        projects, milestones, and english terms.
    """
    total_lessons = db.query(func.count(Lesson.id)).scalar() or 0
    completed_lessons = db.query(func.count(LessonProgress.id)).filter(
        LessonProgress.status == "completed"
    ).scalar() or 0

    total_quizzes = db.query(func.count(Quiz.id)).scalar() or 0
    passed_quizzes = db.query(func.count(func.distinct(QuizAttempt.quiz_id))).filter(
        QuizAttempt.passed == True
    ).scalar() or 0
    avg_quiz_score = db.query(func.avg(QuizAttempt.score)).scalar() or 0

    total_challenges = db.query(func.count(Challenge.id)).scalar() or 0
    solved_challenges = db.query(func.count(func.distinct(ChallengeAttempt.challenge_id))).filter(
        ChallengeAttempt.status == "solved"
    ).scalar() or 0

    total_projects = db.query(func.count(Project.id)).scalar() or 0
    completed_projects = db.query(func.count(ProjectProgress.id)).filter(
        ProjectProgress.status == "completed"
    ).scalar() or 0
    in_progress_projects = db.query(func.count(ProjectProgress.id)).filter(
        ProjectProgress.status == "in_progress"
    ).scalar() or 0

    total_milestones = db.query(func.count(ProjectMilestone.id)).scalar() or 0
    completed_milestones = db.query(func.count(MilestoneProgress.id)).filter(
        MilestoneProgress.completed == True
    ).scalar() or 0

    total_terms = db.query(func.count(EnglishVocabulary.id)).scalar() or 0
    learned_terms = db.query(func.count(EnglishVocabulary.id)).filter(
        EnglishVocabulary.learned == True
    ).scalar() or 0

    return {
        "lessons": {"completed": completed_lessons, "total": total_lessons},
        "quizzes": {"passed": passed_quizzes, "total": total_quizzes, "avg_score": avg_quiz_score},
        "challenges": {"solved": solved_challenges, "total": total_challenges},
        "projects": {"completed": completed_projects, "in_progress": in_progress_projects, "total": total_projects},
        "milestones": {"completed": completed_milestones, "total": total_milestones},
        "english": {"learned": learned_terms, "total": total_terms},
    }


def _calculate_overall_completion(stats: dict) -> float:
    """Calculate weighted overall completion percentage.

    Args:
        stats: The dict returned by _query_completion_stats.

    Returns:
        Overall completion as a percentage (0-100).
    """
    lesson_pct = _safe_pct(stats["lessons"]["completed"], stats["lessons"]["total"])
    quiz_pct = _safe_pct(stats["quizzes"]["passed"], stats["quizzes"]["total"])
    challenge_pct = _safe_pct(stats["challenges"]["solved"], stats["challenges"]["total"])
    milestone_pct = _safe_pct(stats["milestones"]["completed"], stats["milestones"]["total"])
    english_pct = _safe_pct(stats["english"]["learned"], stats["english"]["total"])

    return (
        lesson_pct * _COMPLETION_WEIGHTS["lesson"] +
        quiz_pct * _COMPLETION_WEIGHTS["quiz"] +
        challenge_pct * _COMPLETION_WEIGHTS["challenge"] +
        milestone_pct * _COMPLETION_WEIGHTS["milestone"] +
        english_pct * _COMPLETION_WEIGHTS["english"]
    )


def _get_weekly_activity(db: Session) -> tuple[dict | None, list[dict]]:
    """Fetch today's activity and the last 7 days of weekly activity.

    Returns:
        A tuple of (today_activity_row_or_None, weekly_list).
    """
    today_str = date.today().isoformat()
    today_activity = db.query(DailyActivity).filter(DailyActivity.date == today_str).first()

    week_start = (date.today() - timedelta(days=6)).isoformat()
    week_activities = db.query(DailyActivity).filter(
        DailyActivity.date >= week_start,
        DailyActivity.date <= today_str
    ).all()
    activity_map = {a.date: a for a in week_activities}

    weekly = []
    for i in range(7):
        d = (date.today() - timedelta(days=6 - i)).isoformat()
        act = activity_map.get(d)
        weekly.append({
            "date": d,
            "seconds": act.total_time_seconds if act else 0,
            "lessons": act.lessons_completed if act else 0
        })

    return today_activity, weekly


def _find_current_phase_and_next_lesson(db: Session) -> tuple[str | None, dict | None]:
    """Determine the current phase and next uncompleted lesson.

    Returns:
        A tuple of (current_phase_id, next_lesson_dict_or_None).
    """
    completed_lesson_ids = set(
        lp.lesson_id for lp in
        db.query(LessonProgress).filter(LessonProgress.status == "completed").all()
    )

    all_lessons = db.query(Lesson).join(Module).join(Phase).options(
        joinedload(Lesson.module)
    ).order_by(
        Phase.order_index, Module.order_index, Lesson.order_index
    ).all()

    # Current phase: first phase with incomplete lessons
    current_phase = None
    phases = db.query(Phase).order_by(Phase.order_index).all()
    lessons_by_phase: dict[str, list] = {}
    for lesson in all_lessons:
        lessons_by_phase.setdefault(lesson.module.phase_id, []).append(lesson)

    for phase in phases:
        phase_lessons = lessons_by_phase.get(phase.id, [])
        phase_completed = sum(1 for l in phase_lessons if l.id in completed_lesson_ids)
        if phase_completed < len(phase_lessons):
            current_phase = phase.id
            break

    # Next lesson: first uncompleted lesson in order
    next_lesson = None
    for lesson in all_lessons:
        if lesson.id not in completed_lesson_ids:
            next_lesson = {"id": lesson.id, "title": lesson.title}
            break

    return current_phase, next_lesson


def get_overview(db: Session) -> dict:
    """Build the full dashboard overview with progress stats, streaks, and activity.

    Aggregates lesson, quiz, challenge, project, milestone, and english
    completion data. Computes a weighted overall completion percentage,
    current streak, weekly activity, and identifies the next lesson.

    Args:
        db: SQLAlchemy database session.

    Returns:
        A dict containing overall_completion_percent, current_streak_days,
        total_study_hours, per-category stats, current_phase, next_lesson,
        today's activity, and weekly_activity.
    """
    stats = _query_completion_stats(db)
    overall = _calculate_overall_completion(stats)

    # Total study time
    total_time = db.query(func.sum(LessonProgress.time_spent_seconds)).scalar() or 0
    total_hours = round(total_time / 3600, 1)

    streak = calculate_streak(db)
    today_activity, weekly = _get_weekly_activity(db)
    current_phase, next_lesson = _find_current_phase_and_next_lesson(db)

    return {
        "overall_completion_percent": round(overall, 1),
        "current_streak_days": streak,
        "total_study_hours": total_hours,
        "lessons": stats["lessons"],
        "quizzes": {
            "passed": stats["quizzes"]["passed"],
            "total": stats["quizzes"]["total"],
            "average_score": round(stats["quizzes"]["avg_score"], 1)
        },
        "challenges": stats["challenges"],
        "projects": stats["projects"],
        "english": stats["english"],
        "current_phase": current_phase,
        "next_lesson": next_lesson,
        "today": {
            "time_seconds": today_activity.total_time_seconds if today_activity else 0,
            "lessons_completed": today_activity.lessons_completed if today_activity else 0,
            "challenges_solved": today_activity.challenges_solved if today_activity else 0
        },
        "weekly_activity": weekly
    }


def calculate_streak(db: Session) -> int:
    """Count consecutive days with at least 30 minutes of activity.

    Starts from today and walks backwards, counting each day that
    has a DailyActivity record with >= 1800 seconds (30 min).

    Args:
        db: SQLAlchemy database session.

    Returns:
        The number of consecutive active days as an integer.
    """
    active_dates = set(
        a.date for a in db.query(DailyActivity).filter(
            DailyActivity.total_time_seconds >= 1800
        ).all()
    )

    streak = 0
    current = date.today()
    while current.isoformat() in active_dates:
        streak += 1
        current -= timedelta(days=1)

    return streak


def update_daily_activity(db: Session, lessons_delta: int = 0, quizzes_delta: int = 0,
                          challenges_delta: int = 0, time_delta: int = 0):
    """Update today's daily activity record."""
    today_str = date.today().isoformat()
    activity = db.query(DailyActivity).filter(DailyActivity.date == today_str).first()

    if not activity:
        activity = DailyActivity(date=today_str)
        db.add(activity)

    activity.total_time_seconds = (activity.total_time_seconds or 0) + time_delta
    activity.lessons_completed = (activity.lessons_completed or 0) + lessons_delta
    activity.quizzes_taken = (activity.quizzes_taken or 0) + quizzes_delta
    activity.challenges_solved = (activity.challenges_solved or 0) + challenges_delta

    db.commit()
