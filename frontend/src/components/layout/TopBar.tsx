import { useEffect, useState } from 'react';
import { getProgressOverview } from '../../api/client';
import { useUIStore } from '../../store';
import { HiOutlineMenu, HiOutlineSearch } from 'react-icons/hi';
import SearchModal from '../search/SearchModal';

export default function TopBar() {
  const [overview, setOverview] = useState<import('../../types').ProgressOverview | null>(null);
  const [searchOpen, setSearchOpen] = useState(false);
  const toggleSidebar = useUIStore((s) => s.toggleSidebar);

  useEffect(() => {
    getProgressOverview().then(setOverview).catch(console.error);
  }, []);

  // Ctrl+K global shortcut
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        setSearchOpen((prev) => !prev);
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, []);

  const pct = overview?.overall_completion_percent ?? 0;
  const streak = overview?.current_streak_days ?? 0;
  const hours = overview?.total_study_hours ?? 0;

  return (
    <>
      <header className="h-14 bg-gray-900/80 backdrop-blur border-b border-gray-800 flex items-center justify-between px-4 sticky top-0 z-10">
        <div className="flex items-center gap-3">
          <button onClick={toggleSidebar} className="text-gray-400 hover:text-white p-1">
            <HiOutlineMenu className="w-5 h-5" />
          </button>
          <button
            onClick={() => setSearchOpen(true)}
            className="flex items-center gap-2 px-3 py-1.5 bg-gray-800 hover:bg-gray-700 rounded-lg text-sm text-gray-400 transition-colors"
          >
            <HiOutlineSearch className="w-4 h-4" />
            <span className="hidden sm:inline">Ara...</span>
            <kbd className="hidden sm:inline text-xs text-gray-600 border border-gray-700 rounded px-1 py-0.5 ml-2">Ctrl+K</kbd>
          </button>
        </div>

        <div className="flex items-center gap-6 text-sm">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-full border-2 border-blue-500 flex items-center justify-center">
              <span className="text-xs font-bold text-blue-400">{Math.round(pct)}%</span>
            </div>
          </div>

          <div className="flex items-center gap-1 text-gray-400">
            <span className="text-orange-400">🔥</span>
            <span className="font-medium text-white">{streak}</span>
            <span className="text-xs">gun</span>
          </div>

          <div className="flex items-center gap-1 text-gray-400">
            <span>⏱️</span>
            <span className="font-medium text-white">{hours}</span>
            <span className="text-xs">saat</span>
          </div>
        </div>
      </header>
      <SearchModal open={searchOpen} onClose={() => setSearchOpen(false)} />
    </>
  );
}
