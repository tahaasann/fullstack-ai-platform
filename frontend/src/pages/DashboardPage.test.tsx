import { render, screen, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import DashboardPage from './DashboardPage';

// Mock API
vi.mock('../api/client', () => ({
  getProgressOverview: vi.fn().mockResolvedValue({
    overall_completion_percent: 25,
    current_streak_days: 3,
    total_study_hours: 10,
    lessons: { completed: 5, total: 48 },
    quizzes: { passed: 2, total: 20, average_score: 80 },
    challenges: { solved: 3, total: 60 },
    projects: { completed: 0, in_progress: 1, total: 10 },
    english: { learned: 50, total: 504 },
    current_phase: "Phase 1",
    next_lesson: { id: "test", title: "Test Lesson" },
    today: { time_seconds: 3600, lessons_completed: 1, challenges_solved: 0 },
    weekly_activity: [],
  }),
  getPhases: vi.fn().mockResolvedValue([]),
  getDailyGoal: vi.fn().mockResolvedValue({
    date: '2026-03-21',
    targets: { lessons: 3, quizzes: 1, challenges: 2, time_minutes: 120 },
    progress: { lessons: 1, quizzes: 0, challenges: 0, time_minutes: 30 },
    completed: false,
  }),
  getSuggestions: vi.fn().mockResolvedValue([]),
}));

function renderWithProviders(ui: React.ReactElement) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return render(
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>{ui}</BrowserRouter>
    </QueryClientProvider>
  );
}

describe('DashboardPage', () => {
  it('renders loading state initially', () => {
    renderWithProviders(<DashboardPage />);
    expect(screen.getByText('Yükleniyor...')).toBeInTheDocument();
  });

  it('renders welcome message after data loads', async () => {
    renderWithProviders(<DashboardPage />);
    await waitFor(() => {
      expect(screen.getByText(/Hoş Geldin, Developer/)).toBeInTheDocument();
    });
  });

  it('displays completion percentage', async () => {
    renderWithProviders(<DashboardPage />);
    await waitFor(() => {
      expect(screen.getByText(/25% ilerleme/)).toBeInTheDocument();
    });
  });

  it('displays streak count', async () => {
    renderWithProviders(<DashboardPage />);
    await waitFor(() => {
      expect(screen.getByText('3')).toBeInTheDocument();
    });
  });

  it('displays stat cards', async () => {
    renderWithProviders(<DashboardPage />);
    await waitFor(() => {
      expect(screen.getByText('5/48')).toBeInTheDocument(); // Lessons
      expect(screen.getByText('2/20')).toBeInTheDocument(); // Quizzes
      expect(screen.getByText('3/60')).toBeInTheDocument(); // Challenges
      expect(screen.getByText('0/10')).toBeInTheDocument(); // Projects
    });
  });

  it('shows next lesson link', async () => {
    renderWithProviders(<DashboardPage />);
    await waitFor(() => {
      expect(screen.getByText(/Test Lesson/)).toBeInTheDocument();
    });
  });
});
