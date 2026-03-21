import { useEffect, useState, useRef, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { searchContent } from '../../api/client';
import { HiOutlineSearch, HiOutlineBookOpen, HiOutlineCode, HiOutlineBriefcase, HiOutlineGlobeAlt } from 'react-icons/hi';

interface Props {
  open: boolean;
  onClose: () => void;
}

interface SearchResult {
  id: string;
  title: string;
  description?: string;
  difficulty?: string;
  translation?: string;
  term?: string;
  link: string;
}

interface SearchResults {
  lessons: SearchResult[];
  challenges: SearchResult[];
  projects: SearchResult[];
  vocabulary: SearchResult[];
}

export default function SearchModal({ open, onClose }: Props) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResults | null>(null);
  const [selectedIdx, setSelectedIdx] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const navigate = useNavigate();
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const allResults = results
    ? [
        ...results.lessons.map((r) => ({ ...r, type: 'lesson' })),
        ...results.challenges.map((r) => ({ ...r, type: 'challenge' })),
        ...results.projects.map((r) => ({ ...r, type: 'project' })),
        ...results.vocabulary.map((r) => ({ ...r, type: 'vocabulary', title: `${r.term} — ${r.translation}` })),
      ]
    : [];

  useEffect(() => {
    if (open) {
      inputRef.current?.focus();
      setQuery('');
      setResults(null);
      setSelectedIdx(0);
    }
  }, [open]);

  const doSearch = useCallback((q: string) => {
    if (q.length < 2) { setResults(null); return; }
    searchContent(q).then(setResults).catch(() => setResults(null));
  }, []);

  useEffect(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => doSearch(query), 300);
    return () => { if (debounceRef.current) clearTimeout(debounceRef.current); };
  }, [query, doSearch]);

  const handleNav = (link: string) => {
    navigate(link);
    onClose();
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelectedIdx((i) => Math.min(i + 1, allResults.length - 1));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelectedIdx((i) => Math.max(i - 1, 0));
    } else if (e.key === 'Enter' && allResults[selectedIdx]) {
      handleNav(allResults[selectedIdx].link);
    } else if (e.key === 'Escape') {
      onClose();
    }
  };

  if (!open) return null;

  const typeIcons: Record<string, React.ReactNode> = {
    lesson: <HiOutlineBookOpen className="w-4 h-4 text-blue-400" />,
    challenge: <HiOutlineCode className="w-4 h-4 text-purple-400" />,
    project: <HiOutlineBriefcase className="w-4 h-4 text-orange-400" />,
    vocabulary: <HiOutlineGlobeAlt className="w-4 h-4 text-green-400" />,
  };

  const typeLabels: Record<string, string> = {
    lesson: 'Ders', challenge: 'Challenge', project: 'Proje', vocabulary: 'Kelime',
  };

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-[15vh]" onClick={onClose}>
      <div className="fixed inset-0 bg-black/60 backdrop-blur-sm" />
      <div
        className="relative w-full max-w-xl bg-gray-900 border border-gray-700 rounded-xl shadow-2xl overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Input */}
        <div className="flex items-center gap-3 px-4 py-3 border-b border-gray-800">
          <HiOutlineSearch className="w-5 h-5 text-gray-500" />
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => { setQuery(e.target.value); setSelectedIdx(0); }}
            onKeyDown={handleKeyDown}
            placeholder="Ders, challenge, proje veya kelime ara..."
            className="flex-1 bg-transparent text-white text-sm outline-none placeholder-gray-500"
          />
          <kbd className="text-xs text-gray-600 border border-gray-700 rounded px-1.5 py-0.5">ESC</kbd>
        </div>

        {/* Results */}
        <div className="max-h-80 overflow-y-auto">
          {allResults.length === 0 && query.length >= 2 && (
            <div className="px-4 py-8 text-center text-gray-500 text-sm">Sonuc bulunamadi.</div>
          )}
          {allResults.length === 0 && query.length < 2 && (
            <div className="px-4 py-8 text-center text-gray-600 text-sm">En az 2 karakter yaz...</div>
          )}
          {allResults.map((item, i) => (
            <button
              key={`${item.type}-${item.id}`}
              className={`w-full flex items-center gap-3 px-4 py-2.5 text-left transition-colors ${
                i === selectedIdx ? 'bg-blue-600/20 text-white' : 'text-gray-300 hover:bg-gray-800'
              }`}
              onClick={() => handleNav(item.link)}
              onMouseEnter={() => setSelectedIdx(i)}
            >
              {typeIcons[item.type]}
              <div className="flex-1 min-w-0">
                <div className="text-sm truncate">{item.title}</div>
                {item.description && (
                  <div className="text-xs text-gray-500 truncate">{item.description}</div>
                )}
              </div>
              <span className="text-xs text-gray-600 shrink-0">{typeLabels[item.type]}</span>
            </button>
          ))}
        </div>

        {/* Footer */}
        <div className="px-4 py-2 border-t border-gray-800 flex items-center gap-4 text-xs text-gray-600">
          <span>↑↓ gezin</span>
          <span>↵ ac</span>
          <span>esc kapat</span>
        </div>
      </div>
    </div>
  );
}
