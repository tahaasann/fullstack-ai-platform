export interface Phase {
  id: string;
  title: string;
  description: string;
  order_index: number;
  estimated_weeks: string;
  icon: string;
  module_count: number;
  completed_lessons: number;
  total_lessons: number;
}

export interface Module {
  id: string;
  phase_id: string;
  title: string;
  description: string;
  order_index: number;
  estimated_hours: number;
  lesson_count: number;
  completed_lessons: number;
}

export interface Lesson {
  id: string;
  module_id: string;
  title: string;
  description: string;
  order_index: number;
  estimated_minutes: number;
  tags: string[];
  status: string;
}

export interface LessonContent {
  id: string;
  title: string;
  module_id: string;
  estimated_minutes: number;
  tags: string[];
  sections: Section[];
  meta: Record<string, unknown>;
  status: string;
  time_spent_seconds: number;
  prev_lesson_id: string | null;
  next_lesson_id: string | null;
}

export interface Section {
  type: string;
  content?: string;
  text?: string;
  level?: number;
  label?: string;
  title?: string;
  language?: string;
  code?: string;
  question?: string;
  options?: string[];
  correct?: number | boolean;
  explanation?: string;
  [key: string]: unknown;
}

export interface Quiz {
  id: string;
  title: string;
  description: string;
  passing_score: number;
  questions: QuizQuestion[];
  best_score: number | null;
  attempt_count: number;
}

export interface QuizQuestion {
  id: string;
  type: string;
  question: string;
  options?: string[];
  code?: string;
  code_template?: string;
  steps?: string[];
  difficulty: string;
  points: number;
}

export interface QuizResult {
  score: number;
  passed: boolean;
  correct_count: number;
  total_count: number;
  results: QuizQuestionResult[];
  attempt_number: number;
}

export interface QuizQuestionResult {
  question_id: string;
  question: string;
  type: string;
  user_answer: unknown;
  is_correct: boolean;
  explanation: string;
  correct_answer: unknown;
  points: number;
  earned: number;
}

export interface Challenge {
  id: string;
  title: string;
  description: string;
  difficulty: string;
  category: string;
  tags: string[];
  module_id: string;
  solved: boolean;
}

export interface ChallengeDetail {
  id: string;
  title: string;
  description: string;
  description_detail: string;
  difficulty: string;
  category: string;
  tags: string[];
  examples: { input: string; output: string; explanation: string }[];
  constraints: string[];
  starter_code: Record<string, string>;
  hints_available: number;
  solved: boolean;
  complexity: { optimal_time: string; optimal_space: string };
  learn_after_solving: string;
}

export interface ChallengeRunResult {
  status: string;
  tests_passed: number;
  tests_total: number;
  results: TestResult[];
  execution_time_ms: number;
  error?: string;
}

export interface TestResult {
  passed: boolean;
  input: string;
  expected: string;
  actual: string | null;
  error: string | null;
}

export interface Project {
  id: string;
  title: string;
  description: string;
  order_index: number;
  difficulty: string;
  estimated_days: number;
  tech_stack: string[];
  status: string;
  completed_milestones: number;
  total_milestones: number;
}

export interface ProgressOverview {
  overall_completion_percent: number;
  current_streak_days: number;
  total_study_hours: number;
  lessons: { completed: number; total: number };
  quizzes: { passed: number; total: number; average_score: number };
  challenges: { solved: number; total: number };
  projects: { completed: number; in_progress: number; total: number };
  english: { learned: number; total: number };
  current_phase: string | null;
  next_lesson: { id: string; title: string } | null;
  today: { time_seconds: number; lessons_completed: number; challenges_solved: number };
  weekly_activity: { date: string; seconds: number; lessons: number }[];
}

// Career
export interface CareerGuide {
  title: string;
  description: string;
  sections: CareerSection[];
  // AI Tools Guide specific
  model_comparison?: CareerModelComparison[];
  workflow_templates?: CareerWorkflowTemplate[];
  anti_patterns?: CareerAntiPattern[];
  // Cover Letter specific
  general_tips?: string[];
  templates?: CareerCoverLetterTemplate[];
  per_project_guidance?: CareerPerProjectGuidance[];
  [key: string]: unknown;
}

export interface CareerSection {
  id: string;
  title: string;
  icon?: string;
  content: string;
  tips?: string[];
  examples?: string[];
  checklist?: string[];
  templates?: string[];
}

export interface CareerModelComparison {
  name: string;
  provider: string;
  when_to_use: string;
  strengths?: string[];
  best_for?: string[];
  context_window: string;
  pricing_tier: string;
}

export interface CareerWorkflowTemplate {
  task: string;
  recommended_model: string;
  prompt_template: string;
  tips?: string[];
}

export interface CareerAntiPattern {
  pattern: string;
  description: string;
  better_approach: string;
}

export interface CareerCoverLetterTemplate {
  role: string;
  language?: string;
  tone?: string;
  template?: Record<string, string>;
  example?: string;
}

export interface CareerPerProjectGuidance {
  project_title: string;
  highlight_for_cover_letter?: string;
  skills_to_emphasize?: string[];
  talking_points?: string[];
}

// English
export interface VocabularyItem {
  id: number;
  term: string;
  translation: string;
  pronunciation: string;
  definition_en: string;
  definition_tr: string;
  example_sentences: { en: string; tr: string; context?: string }[];
  common_patterns: string[];
  domain: string;
  level: string;
  learned: boolean;
  review_count: number;
  difficulty_level?: string;
  scenario?: string;
  common_mistakes?: string;
  related_terms?: string[];
}

export interface Scenario {
  id: string | number;
  title: string;
  domain: string;
  context: string;
  dialogue: { role: string; message: string; translation: string }[];
  key_phrases: string[];
  cultural_note: string;
}

export interface SentencePattern {
  id?: string | number;
  pattern: string;
  turkish: string;
  when_to_use: string;
  variations: string[];
  real_example: string;
  domain: string;
  category: string;
}

export interface EnglishProgress {
  total_terms: number;
  learned_terms: number;
  terms_by_domain: Record<string, { total: number; learned: number }>;
  exercises_completed: number;
  average_score: number;
  due_for_review: number;
  total_patterns?: number;
  total_scenarios?: number;
}

// Goals
export interface DailyGoal {
  id: number;
  date: string;
  target_lessons: number;
  target_quizzes: number;
  target_challenges: number;
  target_time_minutes: number;
  achieved_lessons: number;
  achieved_quizzes: number;
  achieved_challenges: number;
  achieved_time_minutes: number;
}

export interface GoalSuggestion {
  type: string;
  title: string;
  description: string;
  action_url: string;
}

// Bookmarks
export interface Bookmark {
  id: number;
  item_type: string;
  item_id: string;
  note: string | null;
  created_at: string;
  title?: string;
}

// Search
export interface SearchResults {
  lessons: SearchResultItem[];
  challenges: SearchResultItem[];
  quizzes: SearchResultItem[];
  projects: SearchResultItem[];
}

export interface SearchResultItem {
  id: string;
  title: string;
  type: string;
  description?: string;
  url: string;
}

// Daily Activity
export interface DailyActivity {
  date: string;
  seconds: number;
  lessons: number;
}

// CV Guidance (from projects)
export interface CvGuidanceProject {
  project_id: string;
  project_title: string;
  cv_guidance: {
    project_title_for_cv: string;
    bullet_points: Record<string, string[]>;
    ats_keywords: string[];
    metrics_you_can_claim: string[];
    cv_placement: string;
  };
  github_guidance: {
    repo_name: string;
    repo_description: string;
    pin_on_profile: boolean;
    pin_priority: number;
    topics: string[];
    readme_sections: string[];
    commit_examples: string[];
    commit_convention: string;
    branch_strategy: string;
    daily_commit_target: string;
    when_to_create: string;
    pro_tips: string[];
  };
}

// Milestone
export interface Milestone {
  id: string;
  title: string;
  description: string;
  order_index: number;
  completed: boolean;
}

// Phase with modules (detailed response)
export interface PhaseDetail extends Phase {
  modules: (Module & { lessons: Lesson[] })[];
}

// Module with lessons (detailed response)
export interface ModuleDetail extends Module {
  lessons: Lesson[];
  quizzes: { id: string; title: string; description?: string; best_score?: number | null; passed?: boolean }[];
  challenges: { id: string; title: string }[];
}

// Project detail
export interface ProjectDetail extends Project {
  brief: string;
  milestones: Milestone[];
  resources: { url: string; title?: string; why?: string }[];
  target_roles?: string[];
  what_you_learn?: Record<string, string[]>;
  architecture: {
    overview?: string;
    diagram?: string;
    decisions: { decision: string; reasoning: string; alternatives?: string; when_to_choose_alternative?: string }[];
  };
  requirements?: {
    functional?: string[];
    non_functional?: string[];
    ai_requirements?: string[];
  };
  evaluation_criteria?: { criterion: string; description: string; weight: number }[];
  milestone_details?: {
    id: string;
    estimated_hours?: number;
    overview?: string;
    concepts_covered?: string[];
    steps?: { step: number; title: string; why?: string; instructions?: string; code_snippet?: string; deep_dive?: string; checkpoint?: string }[];
    must_note?: string;
    senior_learns?: string;
  }[];
  interview_prep?: {
    questions?: string[];
    talking_points?: string[];
  };
  cv_guidance?: {
    project_title_for_cv: string;
    bullet_points: Record<string, string[]>;
    ats_keywords: string[];
    metrics_you_can_claim: string[];
    cv_placement: string;
  };
  github_guidance?: {
    repo_name: string;
    repo_description?: string;
    pin_on_profile?: boolean;
    pin_priority?: number;
    topics?: string[];
    commit_examples?: string[];
    commit_convention?: string;
    branch_strategy?: string;
    daily_commit_target?: string;
    when_to_create?: string;
    pro_tips?: string[];
  };
  [key: string]: unknown;
}

// API success responses
export interface SuccessResponse {
  message?: string;
  [key: string]: unknown;
}
