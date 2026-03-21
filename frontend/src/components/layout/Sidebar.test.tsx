import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { MemoryRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { createElement } from 'react';
import Sidebar from './Sidebar';

// Mock usePhases hook
vi.mock('../../hooks/usePhases', () => ({
  usePhases: vi.fn().mockReturnValue({
    data: [
      {
        id: 'phase-1',
        title: 'Temeller',
        icon: '📚',
        order_index: 1,
        completed_lessons: 3,
        total_lessons: 10,
      },
    ],
    isSuccess: true,
  }),
}));

// Mock useUIStore
vi.mock('../../store', () => ({
  useUIStore: vi.fn((selector: (s: any) => any) => {
    const state = { sidebarOpen: true, setSidebarOpen: vi.fn() };
    return selector(state);
  }),
}));

function renderSidebar() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });

  return render(
    createElement(
      QueryClientProvider,
      { client: queryClient },
      createElement(MemoryRouter, null, createElement(Sidebar))
    )
  );
}

describe('Sidebar', () => {
  it('renders the app title', () => {
    renderSidebar();
    expect(screen.getByText('DevMaster')).toBeInTheDocument();
  });

  it('renders main navigation links', () => {
    renderSidebar();
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
    expect(screen.getByText('Modüller')).toBeInTheDocument();
    expect(screen.getByText('Challenges')).toBeInTheDocument();
    expect(screen.getByText('Projeler')).toBeInTheDocument();
  });

  it('renders progress section links', () => {
    renderSidebar();
    // "İlerleme" appears as both group title and nav link
    const matches = screen.getAllByText('İlerleme');
    expect(matches.length).toBeGreaterThanOrEqual(2);
    expect(screen.getByText('İngilizce')).toBeInTheDocument();
    expect(screen.getByText('Yer İmleri')).toBeInTheDocument();
  });

  it('renders career guide links', () => {
    renderSidebar();
    expect(screen.getByText('CV & GitHub')).toBeInTheDocument();
    expect(screen.getByText('LinkedIn Rehberi')).toBeInTheDocument();
    expect(screen.getByText('İş Takip')).toBeInTheDocument();
  });

  it('renders tools section links', () => {
    renderSidebar();
    expect(screen.getByText('AI Araçları')).toBeInTheDocument();
    expect(screen.getByText('Kaynaklar')).toBeInTheDocument();
    expect(screen.getByText('Yol Haritası')).toBeInTheDocument();
  });

  it('has correct ARIA navigation role and label', () => {
    renderSidebar();
    const nav = screen.getByRole('navigation', { name: 'Ana navigasyon' });
    expect(nav).toBeInTheDocument();
  });

  it('renders navigation links as anchor elements', () => {
    renderSidebar();
    const dashboardLink = screen.getByText('Dashboard').closest('a');
    expect(dashboardLink).toBeInTheDocument();
    expect(dashboardLink).toHaveAttribute('href', '/');
  });

  it('renders phase progress section', () => {
    renderSidebar();
    expect(screen.getByText('Fazlar')).toBeInTheDocument();
    // The mocked phase should appear
    expect(screen.getByText(/Temeller/)).toBeInTheDocument();
    // 30% progress (3/10)
    expect(screen.getByText('30%')).toBeInTheDocument();
  });

  it('renders close button with correct aria-label', () => {
    renderSidebar();
    const closeBtn = screen.getByLabelText('Menüyü kapat');
    expect(closeBtn).toBeInTheDocument();
  });
});
