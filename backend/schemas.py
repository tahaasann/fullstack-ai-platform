from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Any


# --- Phase / Module / Lesson ---

class PhaseOut(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    order_index: int
    estimated_weeks: Optional[str] = None
    icon: Optional[str] = None
    module_count: int = 0
    completed_lessons: int = 0
    total_lessons: int = 0
    model_config = ConfigDict(from_attributes=True)


class ModuleOut(BaseModel):
    id: str
    phase_id: str
    title: str
    description: Optional[str] = None
    order_index: int
    estimated_hours: Optional[float] = None
    lesson_count: int = 0
    completed_lessons: int = 0
    quiz_count: int = 0
    challenge_count: int = 0
    model_config = ConfigDict(from_attributes=True)


class LessonOut(BaseModel):
    id: str
    module_id: str
    title: str
    description: Optional[str] = None
    order_index: int
    estimated_minutes: Optional[int] = None
    tags: Optional[str] = None
    status: str = "not_started"
    model_config = ConfigDict(from_attributes=True)


class LessonContentOut(BaseModel):
    id: str
    title: str
    estimated_minutes: Optional[int] = None
    tags: Optional[str] = None
    sections: list
    status: str = "not_started"
    time_spent_seconds: int = 0
    prev_lesson_id: Optional[str] = None
    next_lesson_id: Optional[str] = None


# --- New response models for nested endpoints ---

class LessonListItem(BaseModel):
    """Lesson item within a module listing."""
    id: str
    title: str
    description: Optional[str] = None
    order_index: int
    estimated_minutes: Optional[int] = None
    tags: list = []
    status: str = "not_started"
    model_config = ConfigDict(from_attributes=True)


class ModuleDetailOut(BaseModel):
    """Module detail with nested lesson list."""
    id: str
    phase_id: str
    title: str
    description: Optional[str] = None
    estimated_hours: Optional[float] = None
    lessons: list[LessonListItem] = []
    model_config = ConfigDict(from_attributes=True)


class PhaseModuleItem(BaseModel):
    """Module item within a phase detail response."""
    id: str
    title: str
    description: Optional[str] = None
    order_index: int
    estimated_hours: Optional[float] = None
    lesson_count: int = 0
    completed_lessons: int = 0


class PhaseDetailOut(BaseModel):
    """Phase detail with nested module list."""
    id: str
    title: str
    description: Optional[str] = None
    order_index: int
    estimated_weeks: Optional[str] = None
    icon: Optional[str] = None
    modules: list[PhaseModuleItem] = []


class LessonDetailOut(BaseModel):
    """Full lesson content for the lesson viewer."""
    id: str
    title: str
    module_id: str
    estimated_minutes: Optional[int] = None
    tags: list = []
    sections: list = []
    meta: dict = {}
    status: str = "not_started"
    time_spent_seconds: int = 0
    prev_lesson_id: Optional[str] = None
    next_lesson_id: Optional[str] = None


class ReindexResponse(BaseModel):
    status: str
    message: str


# --- Quiz ---

class QuizListItem(BaseModel):
    """Quiz item in module quiz listing."""
    id: str
    title: str
    description: Optional[str] = None
    passing_score: int = 70
    best_score: Optional[float] = None
    passed: bool = False


class QuizOut(BaseModel):
    id: str
    module_id: str
    title: str
    description: Optional[str] = None
    passing_score: int = 70
    questions: list = []
    best_score: Optional[float] = None
    attempt_count: int = 0
    model_config = ConfigDict(from_attributes=True)


class QuizSubmit(BaseModel):
    answers: dict
    time_spent_seconds: int = 0


class QuizResultOut(BaseModel):
    score: float
    passed: bool
    correct_count: int
    total_count: int
    results: list
    attempt_number: int


class QuizAttemptOut(BaseModel):
    """Single quiz attempt in attempts history."""
    id: int
    score: float
    passed: bool
    correct_count: int
    total_count: int
    attempted_at: Optional[str] = None
    time_spent_seconds: Optional[int] = None


# --- Challenge ---

class ChallengeOut(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    difficulty: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[str] = None
    module_id: Optional[str] = None
    solved: bool = False
    model_config = ConfigDict(from_attributes=True)


class ChallengeListItem(BaseModel):
    """Challenge item in filtered listing."""
    id: str
    title: str
    description: Optional[str] = None
    difficulty: Optional[str] = None
    category: Optional[str] = None
    tags: list = []
    module_id: Optional[str] = None
    module_title: str = ""
    solved: bool = False


class ChallengeDetailOut(BaseModel):
    id: str
    title: str
    description: str
    description_detail: str = ""
    difficulty: str
    category: Optional[str] = None
    tags: list = []
    examples: list = []
    constraints: list = []
    starter_code: dict = {}
    hints_available: int = 0
    solved: bool = False
    complexity: dict = {}
    learn_after_solving: str = ""


class ChallengeRunRequest(BaseModel):
    code: str
    language: str = "python"


class ChallengeRunResult(BaseModel):
    status: str  # passed, failed, error
    tests_passed: int
    tests_total: int
    results: list
    execution_time_ms: Optional[int] = None
    error: Optional[str] = None


class ChallengeHintsOut(BaseModel):
    hints: list = []
    total: int = 0


class ChallengeSolutionOut(BaseModel):
    solution: dict = {}
    complexity: dict = {}
    learn_after_solving: str = ""


# --- Project ---

class ProjectOut(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    order_index: int
    difficulty: Optional[str] = None
    estimated_days: Optional[int] = None
    tech_stack: Optional[str] = None
    status: str = "not_started"
    completed_milestones: int = 0
    total_milestones: int = 0
    model_config = ConfigDict(from_attributes=True)


class ProjectListItem(BaseModel):
    """Project item in listing."""
    id: str
    title: str
    description: Optional[str] = None
    order_index: int
    difficulty: Optional[str] = None
    estimated_days: Optional[int] = None
    tech_stack: list = []
    status: str = "not_started"
    completed_milestones: int = 0
    total_milestones: int = 0


class ProjectCvGuidanceItem(BaseModel):
    """CV guidance for a project."""
    project_id: str
    project_title: str
    cv_guidance: Optional[Any] = None
    github_guidance: Optional[Any] = None


class MilestoneDetailItem(BaseModel):
    """Milestone item in project detail."""
    id: str
    title: str
    description: Optional[str] = None
    order_index: int
    checklist: list = []
    completed: bool = False
    checklist_state: Optional[list] = None


class ProjectDetailOut(BaseModel):
    """Full project detail with milestones and content."""
    id: str
    title: str
    description: Optional[str] = None
    difficulty: Optional[str] = None
    estimated_days: Optional[int] = None
    tech_stack: list = []
    required_phases: list = []
    status: str = "not_started"
    repo_url: Optional[str] = None
    milestones: list[MilestoneDetailItem] = []
    brief: str = ""
    requirements: dict = {}
    resources: list = []
    target_roles: list = []
    architecture: dict = {}
    what_you_learn: dict = {}
    evaluation_criteria: list = []
    interview_prep: dict = {}
    milestone_details: list = []
    cv_guidance: Optional[Any] = None
    github_guidance: Optional[Any] = None


class MilestoneOut(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    order_index: int
    checklist: Optional[str] = None
    completed: bool = False
    checklist_state: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


# --- Progress ---

class StatusResponse(BaseModel):
    """Generic status response."""
    status: str


class TimeResponse(BaseModel):
    time_spent_seconds: int


class DailyActivityItem(BaseModel):
    date: str
    seconds: int = 0
    lessons: int = 0
    quizzes: int = 0
    challenges: int = 0


class ProgressOverview(BaseModel):
    overall_completion_percent: float
    current_streak_days: int
    total_study_hours: float
    lessons: dict
    quizzes: dict
    challenges: dict
    projects: dict
    english: dict
    current_phase: Optional[str] = None
    next_lesson: Optional[dict] = None
    today: dict
    weekly_activity: list


class LessonProgressUpdate(BaseModel):
    time_spent_seconds: Optional[int] = None


# --- English ---

class VocabularyOut(BaseModel):
    id: int
    term: str
    translation: str
    pronunciation: Optional[str] = None
    example_sentence: Optional[str] = None
    domain: Optional[str] = None
    learned: bool = False
    review_count: int = 0
    model_config = ConfigDict(from_attributes=True)


class VocabularyDetailOut(BaseModel):
    """Extended vocabulary item with all fields."""
    id: int
    term: str
    translation: str
    pronunciation: Optional[str] = None
    example_sentence: Optional[str] = None
    domain: Optional[str] = None
    lesson_id: Optional[str] = None
    learned: bool = False
    review_count: int = 0
    definition_en: Optional[str] = None
    definition_tr: Optional[str] = None
    difficulty_level: Optional[str] = None
    usage_context: Optional[str] = None
    common_patterns: list = []
    scenario: Optional[str] = None
    related_terms: list = []
    common_mistakes: Optional[str] = None
    example_sentences: list = []


class PatternOut(BaseModel):
    """Sentence pattern item."""
    id: int
    domain: Optional[str] = None
    category: Optional[str] = None
    pattern: Optional[str] = None
    turkish: Optional[str] = None
    when_to_use: Optional[str] = None
    variations: list = []
    real_example: Optional[str] = None


class ScenarioOut(BaseModel):
    """Work scenario item."""
    id: str
    title: Optional[str] = None
    context: Optional[str] = None
    dialogue: list = []
    key_phrases: list = []
    cultural_note: Optional[str] = None
    domain: Optional[str] = None


class EnglishProgressOut(BaseModel):
    total_terms: int
    learned_terms: int
    terms_by_domain: dict
    exercises_completed: int
    average_score: float
    due_for_review: int
    total_patterns: int = 0
    total_scenarios: int = 0


class LearnedResponse(BaseModel):
    learned: bool


# --- Bookmark ---

class BookmarkOut(BaseModel):
    """Bookmark item in listing."""
    id: int
    item_type: str
    item_id: str
    note: Optional[str] = None
    created_at: Optional[str] = None
    title: str = ""
    link: str = ""
    model_config = ConfigDict(from_attributes=True)


class BookmarkCheck(BaseModel):
    bookmarked: bool
    id: Optional[int] = None


class BookmarkCreateResponse(BaseModel):
    id: int
    message: str


class BookmarkDeleteResponse(BaseModel):
    message: str


# --- Search ---

class SearchLessonItem(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    link: str


class SearchChallengeItem(BaseModel):
    id: str
    title: str
    difficulty: Optional[str] = None
    link: str


class SearchProjectItem(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    link: str


class SearchVocabularyItem(BaseModel):
    id: int
    term: str
    translation: str
    link: str


class SearchResults(BaseModel):
    lessons: list[SearchLessonItem] = []
    challenges: list[SearchChallengeItem] = []
    projects: list[SearchProjectItem] = []
    vocabulary: list[SearchVocabularyItem] = []


# --- Goals ---

class GoalDefaultsOut(BaseModel):
    target_lessons: int = 3
    target_quizzes: int = 1
    target_challenges: int = 2
    target_time_minutes: int = 120


class TodayGoalTargets(BaseModel):
    lessons: int = 0
    quizzes: int = 0
    challenges: int = 0
    time_minutes: int = 0


class TodayGoalProgress(BaseModel):
    lessons: int = 0
    quizzes: int = 0
    challenges: int = 0
    time_minutes: int = 0


class TodayGoalOut(BaseModel):
    date: str
    targets: TodayGoalTargets
    progress: TodayGoalProgress
    completed: bool = False


class GoalSuggestionOut(BaseModel):
    type: str
    title: str
    link: str
    icon: str
    reason: str


# --- Career ---

class CareerGuideResponse(BaseModel):
    """Generic response for career guide JSON files. Content varies per endpoint."""
    model_config = ConfigDict(extra="allow")


# --- Shared ---

class CompletedResponse(BaseModel):
    completed: bool


class RepoUrlResponse(BaseModel):
    repo_url: str


class ChecklistStateResponse(BaseModel):
    checklist_state: list
