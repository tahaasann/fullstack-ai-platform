from sqlalchemy.orm import Session
from sqlalchemy import func
from models import (
    Phase, Module, Lesson, Quiz, Challenge, Project, ProjectMilestone,
    LessonProgress, QuizAttempt, ChallengeAttempt, ProjectProgress,
    MilestoneProgress, DailyActivity, EnglishVocabulary, EnglishExercise
)
from datetime import datetime, timedelta, timezone, date


def get_overview(db: Session) -> dict:
    # Lesson stats
    total_lessons = db.query(func.count(Lesson.id)).scalar() or 0
    completed_lessons = db.query(func.count(LessonProgress.id)).filter(
        LessonProgress.status == "completed"
    ).scalar() or 0

    # Quiz stats
    total_quizzes = db.query(func.count(Quiz.id)).scalar() or 0
    passed_quizzes = db.query(func.count(func.distinct(QuizAttempt.quiz_id))).filter(
        QuizAttempt.passed == True
    ).scalar() or 0
    avg_quiz_score = db.query(func.avg(QuizAttempt.score)).scalar() or 0

    # Challenge stats
    total_challenges = db.query(func.count(Challenge.id)).scalar() or 0
    solved_challenges = db.query(func.count(func.distinct(ChallengeAttempt.challenge_id))).filter(
        ChallengeAttempt.status == "solved"
    ).scalar() or 0

    # Project stats
    total_projects = db.query(func.count(Project.id)).scalar() or 0
    completed_projects = db.query(func.count(ProjectProgress.id)).filter(
        ProjectProgress.status == "completed"
    ).scalar() or 0
    in_progress_projects = db.query(func.count(ProjectProgress.id)).filter(
        ProjectProgress.status == "in_progress"
    ).scalar() or 0

    # Milestone stats
    total_milestones = db.query(func.count(ProjectMilestone.id)).scalar() or 0
    completed_milestones = db.query(func.count(MilestoneProgress.id)).filter(
        MilestoneProgress.completed == True
    ).scalar() or 0

    # English stats
    total_terms = db.query(func.count(EnglishVocabulary.id)).scalar() or 0
    learned_terms = db.query(func.count(EnglishVocabulary.id)).filter(
        EnglishVocabulary.learned == True
    ).scalar() or 0

    # Overall completion
    lesson_pct = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
    quiz_pct = (passed_quizzes / total_quizzes * 100) if total_quizzes > 0 else 0
    challenge_pct = (solved_challenges / total_challenges * 100) if total_challenges > 0 else 0
    milestone_pct = (completed_milestones / total_milestones * 100) if total_milestones > 0 else 0
    english_pct = (learned_terms / total_terms * 100) if total_terms > 0 else 0

    overall = (
        lesson_pct * 0.35 +
        quiz_pct * 0.20 +
        challenge_pct * 0.15 +
        milestone_pct * 0.20 +
        english_pct * 0.10
    )

    # Total study time
    total_time = db.query(func.sum(LessonProgress.time_spent_seconds)).scalar() or 0
    total_hours = round(total_time / 3600, 1)

    # Streak calculation
    streak = calculate_streak(db)

    # Today's activity
    today_str = date.today().isoformat()
    today_activity = db.query(DailyActivity).filter(DailyActivity.date == today_str).first()

    # Weekly activity
    weekly = []
    for i in range(7):
        d = (date.today() - timedelta(days=6 - i)).isoformat()
        act = db.query(DailyActivity).filter(DailyActivity.date == d).first()
        weekly.append({
            "date": d,
            "seconds": act.total_time_seconds if act else 0,
            "lessons": act.lessons_completed if act else 0
        })

    # Current phase (first incomplete)
    current_phase = None
    phases = db.query(Phase).order_by(Phase.order_index).all()
    for phase in phases:
        phase_lessons = db.query(Lesson).join(Module).filter(Module.phase_id == phase.id).all()
        phase_completed = db.query(LessonProgress).filter(
            LessonProgress.lesson_id.in_([l.id for l in phase_lessons]),
            LessonProgress.status == "completed"
        ).count()
        if phase_completed < len(phase_lessons):
            current_phase = phase.id
            break

    # Next lesson
    next_lesson = None
    all_lessons = db.query(Lesson).join(Module).join(Phase).order_by(
        Phase.order_index, Module.order_index, Lesson.order_index
    ).all()
    for lesson in all_lessons:
        prog = db.query(LessonProgress).filter(LessonProgress.lesson_id == lesson.id).first()
        if not prog or prog.status != "completed":
            next_lesson = {"id": lesson.id, "title": lesson.title}
            break

    return {
        "overall_completion_percent": round(overall, 1),
        "current_streak_days": streak,
        "total_study_hours": total_hours,
        "lessons": {"completed": completed_lessons, "total": total_lessons},
        "quizzes": {"passed": passed_quizzes, "total": total_quizzes, "average_score": round(avg_quiz_score, 1)},
        "challenges": {"solved": solved_challenges, "total": total_challenges},
        "projects": {"completed": completed_projects, "in_progress": in_progress_projects, "total": total_projects},
        "english": {"learned": learned_terms, "total": total_terms},
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
    """Count consecutive days with >= 30 min activity."""
    streak = 0
    current = date.today()

    while True:
        d = current.isoformat()
        activity = db.query(DailyActivity).filter(DailyActivity.date == d).first()
        if activity and activity.total_time_seconds >= 1800:
            streak += 1
            current -= timedelta(days=1)
        else:
            break

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
