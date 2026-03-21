import { useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';

const STORAGE_KEY = 'devmaster_last_position';
const SCROLL_INTERVAL = 30000; // 30 seconds

// Pages that should NOT be saved as resume targets
const EXCLUDED_PATHS = ['/', '/modules', '/challenges', '/projects', '/progress', '/bookmarks', '/job-tracker'];

export interface LastPosition {
  path: string;
  title: string;
  scrollY: number;
  timestamp: number;
}

export function savePosition(path: string, title: string, scrollY = 0) {
  const position: LastPosition = { path, title, scrollY, timestamp: Date.now() };
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(position));
  } catch { /* localStorage full or unavailable */ }
}

export function getLastPosition(): LastPosition | null {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    const pos: LastPosition = JSON.parse(raw);
    // Expire after 30 days
    if (Date.now() - pos.timestamp > 30 * 24 * 60 * 60 * 1000) return null;
    return pos;
  } catch {
    return null;
  }
}

export default function useAutoResume() {
  const location = useLocation();
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    const path = location.pathname;

    // Don't save list/index pages
    if (EXCLUDED_PATHS.includes(path)) return;

    // Extract page title from document
    const getTitle = () => {
      const h1 = document.querySelector('h1, h2');
      return h1?.textContent?.trim() || document.title;
    };

    // Save on route change (with small delay to let page render)
    const saveTimeout = setTimeout(() => {
      savePosition(path, getTitle(), window.scrollY);
    }, 500);

    // Save scroll position periodically
    intervalRef.current = setInterval(() => {
      savePosition(path, getTitle(), window.scrollY);
    }, SCROLL_INTERVAL);

    return () => {
      clearTimeout(saveTimeout);
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [location.pathname]);
}
