import { renderHook, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { createElement } from 'react';
import { usePhases } from './usePhases';

vi.mock('../api/client', () => ({
  getPhases: vi.fn().mockResolvedValue([
    { id: 'phase-1', title: 'Temeller', order_index: 1, module_count: 5, completed_lessons: 0, total_lessons: 14 }
  ]),
}));

const wrapper = ({ children }: { children: React.ReactNode }) => {
  const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return createElement(QueryClientProvider, { client: queryClient }, children);
};

describe('usePhases', () => {
  it('fetches phases successfully', async () => {
    const { result } = renderHook(() => usePhases(), { wrapper });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data).toHaveLength(1);
    expect(result.current.data![0].title).toBe('Temeller');
  });
});
