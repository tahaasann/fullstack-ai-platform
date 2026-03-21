import { useState, useEffect } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { usePhases } from '../../hooks/usePhases';
import { useUIStore } from '../../store';
import {
  HiOutlineHome, HiOutlineBookOpen, HiOutlineCode,
  HiOutlineBriefcase, HiOutlineChartBar, HiOutlineGlobeAlt,
  HiOutlineMap, HiOutlineCollection, HiOutlineDocumentText,
  HiOutlineBookmark, HiOutlineSearch, HiOutlineLightningBolt,
  HiOutlineClipboardList, HiOutlineTemplate, HiOutlineLightBulb,
  HiOutlineX
} from 'react-icons/hi';

interface NavItem {
  to: string;
  icon: React.ComponentType<{ className?: string }>;
  label: string;
}

interface NavGroup {
  title: string;
  items: NavItem[];
}

const navGroups: NavGroup[] = [
  {
    title: 'Ana Menü',
    items: [
      { to: '/', icon: HiOutlineHome, label: 'Dashboard' },
      { to: '/modules', icon: HiOutlineBookOpen, label: 'Modüller' },
      { to: '/challenges', icon: HiOutlineCode, label: 'Challenges' },
      { to: '/projects', icon: HiOutlineBriefcase, label: 'Projeler' },
    ],
  },
  {
    title: 'İlerleme',
    items: [
      { to: '/progress', icon: HiOutlineChartBar, label: 'İlerleme' },
      { to: '/english', icon: HiOutlineGlobeAlt, label: 'İngilizce' },
      { to: '/bookmarks', icon: HiOutlineBookmark, label: 'Yer İmleri' },
    ],
  },
  {
    title: 'Kariyer Rehberi',
    items: [
      { to: '/cv-guide', icon: HiOutlineDocumentText, label: 'CV & GitHub' },
      { to: '/linkedin-guide', icon: HiOutlineSearch, label: 'LinkedIn Rehberi' },
      { to: '/job-tracker', icon: HiOutlineClipboardList, label: 'İş Takip' },
      { to: '/cv-templates', icon: HiOutlineTemplate, label: 'CV Şablonları' },
      { to: '/job-search-strategy', icon: HiOutlineSearch, label: 'İş Arama' },
      { to: '/employment-gap-guide', icon: HiOutlineLightBulb, label: 'Boşluk Rehberi' },
    ],
  },
  {
    title: 'Araçlar',
    items: [
      { to: '/ai-tools', icon: HiOutlineLightningBolt, label: 'AI Araçları' },
      { to: '/resources', icon: HiOutlineCollection, label: 'Kaynaklar' },
      { to: '/roadmap', icon: HiOutlineMap, label: 'Yol Haritası' },
    ],
  },
];

export default function Sidebar() {
  const { data: phases = [] } = usePhases();
  const [expandedPhase, setExpandedPhase] = useState<string | null>(null);
  const sidebarOpen = useUIStore((s) => s.sidebarOpen);
  const setSidebarOpen = useUIStore((s) => s.setSidebarOpen);
  const location = useLocation();

  // Close sidebar on mobile when route changes
  useEffect(() => {
    if (window.innerWidth < 768) {
      setSidebarOpen(false);
    }
  }, [location.pathname, setSidebarOpen]);

  return (
    <>
      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-30 md:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`
          w-64 bg-gray-900 border-r border-gray-800 flex flex-col h-screen overflow-y-auto shrink-0
          fixed inset-y-0 left-0 z-40 transform transition-transform duration-200 ease-in-out
          ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}
          md:sticky md:top-0 md:translate-x-0 md:transition-none
        `}
      >
        <div className="p-4 border-b border-gray-800 flex items-center justify-between">
          <h1 className="text-lg font-bold text-white flex items-center gap-2">
            <span className="text-2xl">🚀</span>
            <span>DevMaster</span>
          </h1>
          {/* Close button on mobile */}
          <button
            onClick={() => setSidebarOpen(false)}
            className="text-gray-400 hover:text-white p-1 md:hidden focus:ring-2 focus:ring-blue-500 focus:outline-none rounded"
            aria-label="Menüyü kapat"
          >
            <HiOutlineX className="w-5 h-5" />
          </button>
        </div>
        <p className="text-xs text-gray-400 px-4 pb-2">AI-Capable Full Stack</p>

        <nav className="flex-1 p-3 space-y-4" role="navigation" aria-label="Ana navigasyon">
          {navGroups.map((group) => (
            <div key={group.title}>
              <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1.5 px-3">
                {group.title}
              </h3>
              <div className="space-y-0.5">
                {group.items.map(({ to, icon: Icon, label }) => (
                  <NavLink
                    key={to}
                    to={to}
                    className={({ isActive }) =>
                      `flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors focus:ring-2 focus:ring-blue-500 focus:outline-none ${
                        isActive
                          ? 'bg-blue-600/20 text-blue-400'
                          : 'text-gray-400 hover:bg-gray-800 hover:text-gray-200'
                      }`
                    }
                  >
                    <Icon className="w-5 h-5" />
                    {label}
                  </NavLink>
                ))}
              </div>
            </div>
          ))}
        </nav>

        <div className="p-3 border-t border-gray-800">
          <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2 px-3">
            Fazlar
          </h3>
          <div className="space-y-1">
            {phases.map((phase) => {
              const pct = phase.total_lessons > 0
                ? Math.round((phase.completed_lessons / phase.total_lessons) * 100)
                : 0;
              return (
                <button
                  key={phase.id}
                  onClick={() => setExpandedPhase(expandedPhase === phase.id ? null : phase.id)}
                  className="w-full text-left px-3 py-2 rounded-lg text-xs text-gray-400 hover:bg-gray-800 transition-colors"
                >
                  <div className="flex items-center justify-between">
                    <span className="truncate">{phase.icon} {phase.title}</span>
                    <span className="text-gray-600">{pct}%</span>
                  </div>
                  <div className="mt-1 h-1 bg-gray-800 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-blue-500 rounded-full transition-all"
                      style={{ width: `${pct}%` }}
                    />
                  </div>
                </button>
              );
            })}
          </div>
        </div>
      </aside>
    </>
  );
}
