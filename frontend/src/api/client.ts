import type {
  Phase, PhaseDetail, ModuleDetail, LessonContent,
  ProgressOverview, DailyActivity,
  Quiz, QuizResult,
  Challenge, ChallengeDetail, ChallengeRunResult,
  Project, ProjectDetail,
  VocabularyItem, EnglishProgress, SentencePattern, Scenario,
  DailyGoal, GoalSuggestion,
  CvGuidanceProject, Bookmark, SearchResults, CareerGuide,
  SuccessResponse
} from '../types';

const BASE_URL = '/api';

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    throw new Error(`API Error: ${res.status} ${res.statusText}`);
  }
  return res.json();
}

// Phases & Lessons
export const getPhases = () => request<Phase[]>('/phases');
export const getPhase = (id: string) => request<PhaseDetail>(`/phases/${id}`);
export const getModule = (id: string) => request<ModuleDetail>(`/modules/${id}`);
export const getLesson = (id: string) => request<LessonContent>(`/lessons/${encodeURIComponent(id)}`);

// Progress
export const getProgressOverview = () => request<ProgressOverview>('/progress/overview');
export const startLesson = (id: string) => request<SuccessResponse>(`/progress/lesson/${encodeURIComponent(id)}/start`, { method: 'POST' });
export const completeLesson = (id: string) => request<SuccessResponse>(`/progress/lesson/${encodeURIComponent(id)}/complete`, { method: 'POST' });
export const updateLessonTime = (id: string, seconds: number) =>
  request<SuccessResponse>(`/progress/lesson/${encodeURIComponent(id)}/time?seconds=${seconds}`, { method: 'PATCH' });
export const getDailyActivity = (days?: number) => request<DailyActivity[]>(`/progress/daily${days ? `?days=${days}` : ''}`);

// Quizzes
export const getQuiz = (id: string) => request<Quiz>(`/quizzes/${encodeURIComponent(id)}`);
export const submitQuiz = (id: string, answers: Record<string, unknown>, timeSpent: number) =>
  request<QuizResult>(`/quizzes/${encodeURIComponent(id)}/submit`, {
    method: 'POST',
    body: JSON.stringify({ answers, time_spent_seconds: timeSpent }),
  });
export const getQuizAttempts = (id: string) => request<QuizResult[]>(`/quizzes/${encodeURIComponent(id)}/attempts`);
export const getModuleQuizzes = (moduleId: string) => request<Quiz[]>(`/quizzes/module/${moduleId}`);

// Challenges
export const getChallenges = (params?: { difficulty?: string; category?: string; module_id?: string }) => {
  const clean: Record<string, string> = {};
  if (params) {
    Object.entries(params).forEach(([k, v]) => { if (v) clean[k] = v; });
  }
  const query = new URLSearchParams(clean).toString();
  return request<Challenge[]>(`/challenges${query ? `?${query}` : ''}`);
};
export const getChallenge = (id: string) => request<ChallengeDetail>(`/challenges/${id}`);
export const runChallenge = (id: string, code: string, language: string) =>
  request<ChallengeRunResult>(`/challenges/${id}/run`, {
    method: 'POST',
    body: JSON.stringify({ code, language }),
  });
export const submitChallenge = (id: string, code: string, language: string) =>
  request<ChallengeRunResult>(`/challenges/${id}/submit`, {
    method: 'POST',
    body: JSON.stringify({ code, language }),
  });
export const getChallengeHints = (id: string, reveal: number) =>
  request<{ hints: string[] }>(`/challenges/${id}/hints?reveal=${reveal}`);
export const getChallengeSolution = (id: string) => request<{ solution: string; explanation: string }>(`/challenges/${id}/solution`);

// Projects
export const getProjects = () => request<Project[]>('/projects');
export const getProject = (id: string) => request<ProjectDetail>(`/projects/${id}`);
export const startProject = (id: string) => request<SuccessResponse>(`/projects/${id}/start`, { method: 'POST' });
export const completeProject = (id: string) => request<SuccessResponse>(`/projects/${id}/complete`, { method: 'POST' });
export const toggleMilestone = (id: string) => request<{ completed: boolean }>(`/milestones/${id}/toggle`, { method: 'POST' });

// English
export const getVocabulary = (domain?: string) =>
  request<VocabularyItem[]>(`/english/vocabulary${domain ? `?domain=${domain}` : ''}`);
export const markVocabLearned = (id: number) =>
  request<{ learned: boolean }>(`/english/vocabulary/${id}/learned`, { method: 'POST' });
export const getEnglishProgress = () => request<EnglishProgress>('/english/progress');
export const getPatterns = (domain?: string) =>
  request<SentencePattern[]>(`/english/patterns${domain ? `?domain=${domain}` : ''}`);
export const getScenarios = (domain?: string) =>
  request<Scenario[]>(`/english/scenarios${domain ? `?domain=${domain}` : ''}`);

// Goals
export const getDailyGoal = () => request<DailyGoal>('/goals/today');
export const setDailyGoal = (targets: { target_lessons: number; target_quizzes: number; target_challenges: number; target_time_minutes: number }) =>
  request<DailyGoal>(`/goals/today?target_lessons=${targets.target_lessons}&target_quizzes=${targets.target_quizzes}&target_challenges=${targets.target_challenges}&target_time_minutes=${targets.target_time_minutes}`, { method: 'PUT' });
export const getGoalDefaults = () => request<DailyGoal>('/goals/defaults');
export const setGoalDefaults = (defaults: { target_lessons: number; target_quizzes: number; target_challenges: number; target_time_minutes: number }) =>
  request<DailyGoal>(`/goals/defaults?target_lessons=${defaults.target_lessons}&target_quizzes=${defaults.target_quizzes}&target_challenges=${defaults.target_challenges}&target_time_minutes=${defaults.target_time_minutes}`, { method: 'PUT' });
export const getSuggestions = () => request<GoalSuggestion[]>('/goals/suggestions');

// CV & GitHub Guidance
export const getCvGuidance = () => request<CvGuidanceProject[]>('/projects/cv-guidance');

// Bookmarks
export const getBookmarks = () => request<Bookmark[]>('/bookmarks');
export const checkBookmark = (itemType: string, itemId: string) =>
  request<{ bookmarked: boolean; id: number | null }>(`/bookmarks/check?item_type=${itemType}&item_id=${encodeURIComponent(itemId)}`);
export const createBookmark = (itemType: string, itemId: string, note?: string) =>
  request<{ id: number }>(`/bookmarks?item_type=${itemType}&item_id=${encodeURIComponent(itemId)}${note ? `&note=${encodeURIComponent(note)}` : ''}`, { method: 'POST' });
export const deleteBookmark = (id: number) =>
  request<SuccessResponse>(`/bookmarks/${id}`, { method: 'DELETE' });

// Search
export const searchContent = (q: string) => request<SearchResults>(`/search?q=${encodeURIComponent(q)}`);

// Career
export const getLinkedInGuide = () => request<CareerGuide>('/career/linkedin-guide');
export const getCoverLetterTemplates = () => request<CareerGuide>('/career/cover-letter-templates');
export const getAIToolsGuide = () => request<CareerGuide>('/career/ai-tools-guide');
export const getCvTemplates = () => request<CareerGuide>('/career/cv-templates');
export const getJobSearchStrategy = () => request<CareerGuide>('/career/job-search-strategy');
export const getEmploymentGapGuide = () => request<CareerGuide>('/career/employment-gap-guide');
export const getGithubProfileGuide = () => request<CareerGuide>('/career/github-profile-guide');

// Reindex
export const reindexContent = () => request<SuccessResponse>('/reindex', { method: 'POST' });
