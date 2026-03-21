from sqlalchemy import Column, String, Integer, Float, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base


class Phase(Base):
    __tablename__ = "phases"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    order_index = Column(Integer, nullable=False)
    estimated_weeks = Column(String)
    icon = Column(String)

    modules = relationship("Module", back_populates="phase", order_by="Module.order_index")


class Module(Base):
    __tablename__ = "modules"

    id = Column(String, primary_key=True)
    phase_id = Column(String, ForeignKey("phases.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    order_index = Column(Integer, nullable=False)
    estimated_hours = Column(Float)
    prerequisites = Column(Text)  # JSON array of module IDs

    phase = relationship("Phase", back_populates="modules")
    lessons = relationship("Lesson", back_populates="module", order_by="Lesson.order_index")
    quizzes = relationship("Quiz", back_populates="module", order_by="Quiz.order_index")
    challenges = relationship("Challenge", back_populates="module", order_by="Challenge.order_index")


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(String, primary_key=True)
    module_id = Column(String, ForeignKey("modules.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    order_index = Column(Integer, nullable=False)
    content_path = Column(String, nullable=False)
    estimated_minutes = Column(Integer)
    tags = Column(Text)  # JSON array

    module = relationship("Module", back_populates="lessons")
    progress = relationship("LessonProgress", back_populates="lesson", uselist=False)


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(String, primary_key=True)
    module_id = Column(String, ForeignKey("modules.id"), nullable=False)
    after_lesson_id = Column(String, ForeignKey("lessons.id"))
    title = Column(String, nullable=False)
    description = Column(Text)
    passing_score = Column(Integer, default=70)
    content_path = Column(String, nullable=False)
    order_index = Column(Integer, nullable=False)

    module = relationship("Module", back_populates="quizzes")
    attempts = relationship("QuizAttempt", back_populates="quiz", order_by="QuizAttempt.attempted_at.desc()")


class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(String, primary_key=True)
    module_id = Column(String, ForeignKey("modules.id"))
    title = Column(String, nullable=False)
    description = Column(Text)
    difficulty = Column(String)  # kolay, orta, zor, expert
    category = Column(String)
    content_path = Column(String, nullable=False)
    related_lesson_id = Column(String, ForeignKey("lessons.id"))
    order_index = Column(Integer, default=0)
    tags = Column(Text)  # JSON array

    module = relationship("Module", back_populates="challenges")
    attempts = relationship("ChallengeAttempt", back_populates="challenge")


class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    order_index = Column(Integer, nullable=False)
    difficulty = Column(String)
    estimated_days = Column(Integer)
    content_path = Column(String, nullable=False)
    required_phases = Column(Text)  # JSON
    tech_stack = Column(Text)  # JSON

    milestones = relationship("ProjectMilestone", back_populates="project", order_by="ProjectMilestone.order_index")
    progress = relationship("ProjectProgress", back_populates="project", uselist=False)


class ProjectMilestone(Base):
    __tablename__ = "project_milestones"

    id = Column(String, primary_key=True)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    order_index = Column(Integer, nullable=False)
    content_path = Column(String)
    checklist = Column(Text)  # JSON array

    project = relationship("Project", back_populates="milestones")
    progress = relationship("MilestoneProgress", back_populates="milestone", uselist=False)


# Progress tracking tables

class LessonProgress(Base):
    __tablename__ = "lesson_progress"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lesson_id = Column(String, ForeignKey("lessons.id"), nullable=False, unique=True)
    status = Column(String, default="not_started")  # not_started, in_progress, completed
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    time_spent_seconds = Column(Integer, default=0)
    notes = Column(Text)

    lesson = relationship("Lesson", back_populates="progress")


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(String, ForeignKey("quizzes.id"), nullable=False)
    score = Column(Float, nullable=False)
    answers = Column(Text, nullable=False)  # JSON
    correct_count = Column(Integer)
    total_count = Column(Integer)
    passed = Column(Boolean)
    attempted_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    time_spent_seconds = Column(Integer)

    quiz = relationship("Quiz", back_populates="attempts")


class ChallengeAttempt(Base):
    __tablename__ = "challenge_attempts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    challenge_id = Column(String, ForeignKey("challenges.id"), nullable=False)
    status = Column(String)  # attempted, solved, gave_up
    solution_code = Column(Text)
    language = Column(String, default="python")
    tests_passed = Column(Integer)
    tests_total = Column(Integer)
    hints_used = Column(Integer, default=0)
    attempted_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    time_spent_seconds = Column(Integer)

    challenge = relationship("Challenge", back_populates="attempts")


class ProjectProgress(Base):
    __tablename__ = "project_progress"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False, unique=True)
    status = Column(String, default="not_started")
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    repo_url = Column(String)

    project = relationship("Project", back_populates="progress")


class MilestoneProgress(Base):
    __tablename__ = "milestone_progress"

    id = Column(Integer, primary_key=True, autoincrement=True)
    milestone_id = Column(String, ForeignKey("project_milestones.id"), nullable=False, unique=True)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime)
    checklist_state = Column(Text)  # JSON

    milestone = relationship("ProjectMilestone", back_populates="progress")


class DailyActivity(Base):
    __tablename__ = "daily_activity"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String, nullable=False, unique=True)
    total_time_seconds = Column(Integer, default=0)
    lessons_completed = Column(Integer, default=0)
    quizzes_taken = Column(Integer, default=0)
    challenges_solved = Column(Integer, default=0)


class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_type = Column(String, nullable=False)
    item_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    note = Column(Text)


class EnglishVocabulary(Base):
    __tablename__ = "english_vocabulary"

    id = Column(Integer, primary_key=True, autoincrement=True)
    term = Column(String, nullable=False)
    translation = Column(String, nullable=False)
    pronunciation = Column(String)
    example_sentence = Column(Text)
    domain = Column(String)  # programming, git, web, errors, communication, review, docs, interview
    lesson_id = Column(String)
    learned = Column(Boolean, default=False)
    review_count = Column(Integer, default=0)
    next_review_at = Column(DateTime)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    # WS1: Enhanced English fields
    definition_en = Column(Text)
    definition_tr = Column(Text)
    difficulty_level = Column(String)  # beginner, intermediate, advanced
    usage_context = Column(Text)
    common_patterns = Column(Text)  # JSON array
    scenario = Column(Text)
    related_terms = Column(Text)  # JSON array
    common_mistakes = Column(Text)
    example_sentences = Column(Text)  # JSON array of {en, tr, context}


class SentencePattern(Base):
    __tablename__ = "sentence_patterns"

    id = Column(Integer, primary_key=True, autoincrement=True)
    domain = Column(String, nullable=False)
    category = Column(String, nullable=False)
    pattern = Column(Text, nullable=False)
    turkish = Column(Text)
    when_to_use = Column(Text)
    variations = Column(Text)  # JSON array
    real_example = Column(Text)
    order_index = Column(Integer, default=0)


class WorkScenario(Base):
    __tablename__ = "work_scenarios"

    id_str = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    context = Column(Text)
    dialogue = Column(Text)  # JSON array
    key_phrases = Column(Text)  # JSON array
    cultural_note = Column(Text)
    domain = Column(String)
    order_index = Column(Integer, default=0)


class EnglishExercise(Base):
    __tablename__ = "english_exercises"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lesson_id = Column(String, nullable=False)
    exercise_type = Column(String)  # reading, writing, vocabulary
    score = Column(Float)
    completed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


# Daily Goals & Settings

class DailyGoal(Base):
    __tablename__ = "daily_goals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String, nullable=False, unique=True)
    target_lessons = Column(Integer, default=3)
    target_quizzes = Column(Integer, default=1)
    target_challenges = Column(Integer, default=2)
    target_time_minutes = Column(Integer, default=120)
    completed = Column(Boolean, default=False)


class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String, nullable=False, unique=True)
    value = Column(Text)
