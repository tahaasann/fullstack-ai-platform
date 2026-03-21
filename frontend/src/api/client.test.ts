import { describe, it, expect, vi, beforeEach } from 'vitest';

const mockFetch = vi.fn();
global.fetch = mockFetch;

// Import after mocking
import { getPhases, getLesson } from './client';

describe('API Client', () => {
  beforeEach(() => {
    mockFetch.mockReset();
  });

  it('getPhases calls correct endpoint', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: () => Promise.resolve([]) });
    await getPhases();
    expect(mockFetch).toHaveBeenCalledWith(
      '/api/phases',
      expect.objectContaining({ headers: { 'Content-Type': 'application/json' } })
    );
  });

  it('getLesson encodes lesson ID', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: () => Promise.resolve({}) });
    await getLesson('phase-1/module-01/lesson-01');
    const calledUrl = mockFetch.mock.calls[0][0];
    expect(calledUrl).toContain(encodeURIComponent('phase-1/module-01/lesson-01'));
  });

  it('throws on non-ok response', async () => {
    mockFetch.mockResolvedValue({ ok: false, status: 404, statusText: 'Not Found' });
    await expect(getPhases()).rejects.toThrow('API Error: 404');
  });
});
