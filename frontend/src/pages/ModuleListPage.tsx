import { useEffect, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { getPhases, getPhase } from '../api/client';
import type { Phase, Module } from '../types';

export default function ModuleListPage() {
  const [phases, setPhases] = useState<Phase[]>([]);
  const [expandedPhase, setExpandedPhase] = useState<string | null>(null);
  const [phaseModules, setPhaseModules] = useState<Record<string, (Module & { lessons: unknown[] })[]>>({});
  const [searchParams] = useSearchParams();

  useEffect(() => {
    getPhases().then((data) => {
      setPhases(data);
      const targetPhase = searchParams.get('phase');
      if (targetPhase) {
        setExpandedPhase(targetPhase);
        loadPhaseModules(targetPhase);
      }
    }).catch(console.error);
  }, []);

  const loadPhaseModules = async (phaseId: string) => {
    if (phaseModules[phaseId]) return;
    const data = await getPhase(phaseId);
    setPhaseModules((prev) => ({ ...prev, [phaseId]: data.modules }));
  };

  const togglePhase = (phaseId: string) => {
    if (expandedPhase === phaseId) {
      setExpandedPhase(null);
    } else {
      setExpandedPhase(phaseId);
      loadPhaseModules(phaseId);
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-white mb-6">Eğitim Modülleri</h1>

      <div className="space-y-3">
        {phases.map((phase) => {
          const pct = phase.total_lessons > 0
            ? Math.round((phase.completed_lessons / phase.total_lessons) * 100) : 0;
          const isExpanded = expandedPhase === phase.id;

          return (
            <div key={phase.id} className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
              <button
                onClick={() => togglePhase(phase.id)}
                className="w-full p-5 text-left hover:bg-gray-800/50 transition-colors"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <h2 className="text-lg font-semibold text-white">
                      {phase.icon} {phase.title}
                    </h2>
                    <p className="text-sm text-gray-400 mt-1">{phase.description}</p>
                  </div>
                  <div className="text-right ml-4">
                    <div className="text-sm font-medium text-gray-300">{pct}%</div>
                    <div className="text-xs text-gray-500">{phase.module_count} modül · Hafta {phase.estimated_weeks}</div>
                  </div>
                </div>
                <div className="mt-3 h-2 bg-gray-800 rounded-full overflow-hidden">
                  <div className="h-full bg-blue-500 rounded-full transition-all" style={{ width: `${pct}%` }} />
                </div>
              </button>

              {isExpanded && phaseModules[phase.id] && (
                <div className="border-t border-gray-800 p-4 space-y-2">
                  {phaseModules[phase.id].map((mod) => {
                    const modPct = mod.lesson_count > 0
                      ? Math.round((mod.completed_lessons / mod.lesson_count) * 100) : 0;
                    const isComplete = modPct === 100;
                    const isStarted = modPct > 0;
                    return (
                      <Link
                        key={mod.id}
                        to={`/module/${mod.id}`}
                        className="block p-4 bg-gray-800/50 hover:bg-gray-800 rounded-lg transition-colors"
                      >
                        <div className="flex items-center justify-between">
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-2">
                              <h3 className="text-sm font-medium text-gray-200 truncate">{mod.title}</h3>
                              {isComplete && (
                                <span className="shrink-0 px-1.5 py-0.5 bg-green-500/20 text-green-400 text-[10px] font-semibold rounded">
                                  TAMAMLANDI
                                </span>
                              )}
                            </div>
                            <p className="text-xs text-gray-500 mt-1 truncate">{mod.description}</p>
                          </div>
                          <div className="flex items-center gap-3 ml-4 shrink-0">
                            <div className="text-right">
                              <div className="text-xs text-gray-400">
                                {mod.completed_lessons}/{mod.lesson_count} ders
                              </div>
                              <div className="text-xs text-gray-500">{mod.estimated_hours}h</div>
                            </div>
                            <div className={`w-10 h-10 rounded-full border-2 flex items-center justify-center ${
                              isComplete ? 'border-green-500' : isStarted ? 'border-blue-500' : 'border-gray-700'
                            }`}>
                              <span className={`text-xs font-bold ${
                                isComplete ? 'text-green-400' : isStarted ? 'text-blue-400' : 'text-gray-600'
                              }`}>
                                {modPct}%
                              </span>
                            </div>
                          </div>
                        </div>
                        <div className="mt-2 h-1.5 bg-gray-700 rounded-full overflow-hidden">
                          <div
                            className={`h-full rounded-full transition-all ${isComplete ? 'bg-green-500' : 'bg-blue-500'}`}
                            style={{ width: `${modPct}%` }}
                          />
                        </div>
                      </Link>
                    );
                  })}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
