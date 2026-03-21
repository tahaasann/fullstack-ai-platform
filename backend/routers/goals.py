from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import (
    DailyGoal, UserSettings, DailyActivity,
    Lesson, LessonProgress, Quiz, QuizAttempt,
    Challenge, ChallengeAttempt, Module, Phase,
    EnglishVocabulary
)
from schemas import (
    GoalDefaultsOut, StatusResponse, TodayGoalOut,
    TodayGoalTargets, TodayGoalProgress, GoalSuggestionOut,
)
from datetime import date
import json

router = APIRouter()


def _get_setting(db: Session, key: str, default: str) -> str:
    setting = db.query(UserSettings).filter(UserSettings.key == key).first()
    return setting.value if setting else default


def _set_setting(db: Session, key: str, value: str):
    setting = db.query(UserSettings).filter(UserSettings.key == key).first()
    if not setting:
        setting = UserSettings(key=key, value=value)
        db.add(setting)
    else:
        setting.value = value
    db.commit()


@router.get("/goals/defaults", response_model=GoalDefaultsOut)
def get_goal_defaults(db: Session = Depends(get_db)) -> GoalDefaultsOut:
    """Return default daily goal targets."""
    return GoalDefaultsOut(
        target_lessons=int(_get_setting(db, "goal_lessons", "3")),
        target_quizzes=int(_get_setting(db, "goal_quizzes", "1")),
        target_challenges=int(_get_setting(db, "goal_challenges", "2")),
        target_time_minutes=int(_get_setting(db, "goal_time", "120")),
    )


@router.put("/goals/defaults", response_model=StatusResponse)
def set_goal_defaults(
    target_lessons: int = 3,
    target_quizzes: int = 1,
    target_challenges: int = 2,
    target_time_minutes: int = 120,
    db: Session = Depends(get_db)
) -> StatusResponse:
    """Update default daily goal targets."""
    _set_setting(db, "goal_lessons", str(target_lessons))
    _set_setting(db, "goal_quizzes", str(target_quizzes))
    _set_setting(db, "goal_challenges", str(target_challenges))
    _set_setting(db, "goal_time", str(target_time_minutes))
    return StatusResponse(status="ok")


@router.get("/goals/today", response_model=TodayGoalOut)
def get_today_goal(db: Session = Depends(get_db)) -> TodayGoalOut:
    """Return today's goal with targets and progress."""
    today_str = date.today().isoformat()

    goal = db.query(DailyGoal).filter(DailyGoal.date == today_str).first()
    if not goal:
        # Auto-create with defaults
        goal = DailyGoal(
            date=today_str,
            target_lessons=int(_get_setting(db, "goal_lessons", "3")),
            target_quizzes=int(_get_setting(db, "goal_quizzes", "1")),
            target_challenges=int(_get_setting(db, "goal_challenges", "2")),
            target_time_minutes=int(_get_setting(db, "goal_time", "120")),
        )
        db.add(goal)
        db.commit()

    activity = db.query(DailyActivity).filter(DailyActivity.date == today_str).first()

    return TodayGoalOut(
        date=today_str,
        targets=TodayGoalTargets(
            lessons=goal.target_lessons,
            quizzes=goal.target_quizzes,
            challenges=goal.target_challenges,
            time_minutes=goal.target_time_minutes,
        ),
        progress=TodayGoalProgress(
            lessons=activity.lessons_completed if activity else 0,
            quizzes=activity.quizzes_taken if activity else 0,
            challenges=activity.challenges_solved if activity else 0,
            time_minutes=round((activity.total_time_seconds or 0) / 60) if activity else 0,
        ),
        completed=goal.completed,
    )


@router.put("/goals/today", response_model=StatusResponse)
def update_today_goal(
    target_lessons: int = 3,
    target_quizzes: int = 1,
    target_challenges: int = 2,
    target_time_minutes: int = 120,
    db: Session = Depends(get_db)
) -> StatusResponse:
    """Update today's goal targets."""
    today_str = date.today().isoformat()
    goal = db.query(DailyGoal).filter(DailyGoal.date == today_str).first()
    if not goal:
        goal = DailyGoal(date=today_str)
        db.add(goal)
    goal.target_lessons = target_lessons
    goal.target_quizzes = target_quizzes
    goal.target_challenges = target_challenges
    goal.target_time_minutes = target_time_minutes
    db.commit()
    return StatusResponse(status="ok")


@router.get("/goals/suggestions", response_model=list[GoalSuggestionOut])
def get_suggestions(db: Session = Depends(get_db)) -> list[GoalSuggestionOut]:
    """Get smart action suggestions based on progress."""
    suggestions = []

    # 1. Next incomplete lesson
    all_lessons = db.query(Lesson).join(Module).join(Phase).order_by(
        Phase.order_index, Module.order_index, Lesson.order_index
    ).all()
    for lesson in all_lessons:
        prog = db.query(LessonProgress).filter(LessonProgress.lesson_id == lesson.id).first()
        if not prog or prog.status != "completed":
            suggestions.append(GoalSuggestionOut(
                type="lesson",
                title=lesson.title,
                link=f"/lesson/{lesson.id}",
                icon="\U0001f4d6",
                reason="Sıradaki ders",
            ))
            break

    # 2. In-progress lessons (started but not completed)
    in_progress = db.query(LessonProgress).filter(LessonProgress.status == "in_progress").all()
    for prog in in_progress[:1]:
        lesson = db.query(Lesson).filter(Lesson.id == prog.lesson_id).first()
        if lesson:
            suggestions.append(GoalSuggestionOut(
                type="lesson",
                title=lesson.title,
                link=f"/lesson/{lesson.id}",
                icon="\u25b6\ufe0f",
                reason="Yarım kalan ders",
            ))

    # 3. Unsolved challenge
    solved_ids = db.query(ChallengeAttempt.challenge_id).filter(
        ChallengeAttempt.status == "solved"
    ).distinct().subquery()
    unsolved = db.query(Challenge).filter(
        ~Challenge.id.in_(solved_ids)
    ).order_by(Challenge.order_index).first()
    if unsolved:
        suggestions.append(GoalSuggestionOut(
            type="challenge",
            title=unsolved.title,
            link=f"/challenge/{unsolved.id}",
            icon="\U0001f4bb",
            reason="Çözülmemiş challenge",
        ))

    # 4. Unattempted quiz
    attempted_ids = db.query(QuizAttempt.quiz_id).distinct().subquery()
    unattempted = db.query(Quiz).filter(
        ~Quiz.id.in_(attempted_ids)
    ).order_by(Quiz.order_index).first()
    if unattempted:
        suggestions.append(GoalSuggestionOut(
            type="quiz",
            title=unattempted.title,
            link=f"/quiz/{unattempted.id}",
            icon="\u2705",
            reason="Çözülmemiş quiz",
        ))

    # 5. English vocabulary review
    unlearned_count = db.query(func.count(EnglishVocabulary.id)).filter(
        EnglishVocabulary.learned == False
    ).scalar() or 0
    if unlearned_count > 0:
        suggestions.append(GoalSuggestionOut(
            type="english",
            title=f"{min(unlearned_count, 10)} yeni kelime öğren",
            link="/english",
            icon="\U0001f310",
            reason=f"{unlearned_count} kelime bekliyor",
        ))

    return suggestions[:5]
