import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getPhases } from '../api/client';
import type { Phase } from '../types';

const weekPlan = [
  { week: '1-2', phase: 'Faz 1', title: 'Temeller', desc: 'İnternet, Python, JavaScript/TypeScript, Git, Terminal', color: 'blue' },
  { week: '3-4', phase: 'Faz 2', title: 'Frontend Geliştirme', desc: 'HTML5/CSS3, React+TypeScript, Component Mimarisi', color: 'green' },
  { week: '5', phase: 'Faz 2-3', title: 'Frontend → Backend Geçiş', desc: 'API tüketimi, Node.js/Express temelleri', color: 'teal' },
  { week: '6-7', phase: 'Faz 3', title: 'Backend Geliştirme', desc: 'REST API, Veritabanı, Auth, Testing', color: 'yellow' },
  { week: '7-8', phase: 'Faz 4', title: 'DevOps & Güvenlik', desc: 'Docker, CI/CD, Cloud, OWASP', color: 'orange' },
  { week: '8-9', phase: 'Faz 5', title: 'AI/ML Temelleri', desc: 'Matematik, Python ML, Deep Learning', color: 'pink' },
  { week: '10', phase: 'Faz 5', title: 'Generative AI & RAG', desc: 'LLM, Prompt Engineering, RAG, AI Agents', color: 'purple' },
  { week: '10-11', phase: 'Faz 6', title: 'Mimari & System Design', desc: 'Design Patterns, SOLID, DSA', color: 'red' },
  { week: '12', phase: 'Faz 6', title: 'Kariyer & Mülakat', desc: 'Portfolio, CV, Mock Interview, Open Source', color: 'indigo' },
];

const colorMap: Record<string, { bg: string; border: string; text: string; dot: string }> = {
  blue: { bg: 'bg-blue-900/20', border: 'border-blue-500/30', text: 'text-blue-400', dot: 'bg-blue-500' },
  green: { bg: 'bg-green-900/20', border: 'border-green-500/30', text: 'text-green-400', dot: 'bg-green-500' },
  teal: { bg: 'bg-teal-900/20', border: 'border-teal-500/30', text: 'text-teal-400', dot: 'bg-teal-500' },
  yellow: { bg: 'bg-yellow-900/20', border: 'border-yellow-500/30', text: 'text-yellow-400', dot: 'bg-yellow-500' },
  orange: { bg: 'bg-orange-900/20', border: 'border-orange-500/30', text: 'text-orange-400', dot: 'bg-orange-500' },
  pink: { bg: 'bg-pink-900/20', border: 'border-pink-500/30', text: 'text-pink-400', dot: 'bg-pink-500' },
  purple: { bg: 'bg-purple-900/20', border: 'border-purple-500/30', text: 'text-purple-400', dot: 'bg-purple-500' },
  red: { bg: 'bg-red-900/20', border: 'border-red-500/30', text: 'text-red-400', dot: 'bg-red-500' },
  indigo: { bg: 'bg-indigo-900/20', border: 'border-indigo-500/30', text: 'text-indigo-400', dot: 'bg-indigo-500' },
};

export default function RoadmapPage() {
  const [phases, setPhases] = useState<Phase[]>([]);

  useEffect(() => {
    getPhases().then(setPhases).catch(console.error);
  }, []);

  // Calculate current week (assuming start from a reference date)
  const overallPct = phases.length > 0
    ? Math.round(phases.reduce((sum, p) => sum + (p.total_lessons > 0 ? (p.completed_lessons / p.total_lessons) : 0), 0) / phases.length * 100)
    : 0;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">🗺️ 12 Haftalık Yol Haritası</h1>
        <p className="text-gray-400 text-sm mt-1">
          AI-Capable Full Stack Developer olma yolculuğun. Genel ilerleme: {overallPct}%
        </p>
      </div>

      {/* English Transition */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
        <h3 className="text-sm font-semibold text-gray-400 mb-3">🌐 İngilizce Geçiş Planı</h3>
        <div className="flex gap-1">
          {[
            { weeks: '1-3', tr: 70, en: 30, label: 'Foundation' },
            { weeks: '4-6', tr: 50, en: 50, label: 'Building' },
            { weeks: '7-9', tr: 30, en: 70, label: 'Professional' },
            { weeks: '10-12', tr: 20, en: 80, label: 'Career Ready' },
          ].map((phase, i) => (
            <div key={i} className="flex-1 text-center">
              <div className="h-8 flex rounded overflow-hidden mb-1">
                <div className="bg-orange-500/50" style={{ width: `${phase.tr}%` }} />
                <div className="bg-emerald-500/50" style={{ width: `${phase.en}%` }} />
              </div>
              <div className="text-[10px] text-gray-400">Hafta {phase.weeks}</div>
              <div className="text-[10px] text-gray-400">{phase.label}</div>
              <div className="text-[10px] text-gray-600">TR {phase.tr}% / EN {phase.en}%</div>
            </div>
          ))}
        </div>
      </div>

      {/* Timeline */}
      <div className="relative">
        <div className="absolute left-6 top-0 bottom-0 w-px bg-gray-800" />

        <div className="space-y-4">
          {weekPlan.map((item, i) => {
            const c = colorMap[item.color] || colorMap.blue;
            return (
              <div key={i} className="relative pl-14">
                <div className={`absolute left-4 top-5 w-4 h-4 rounded-full ${c.dot} border-4 border-gray-950 z-10`} />
                <div className={`${c.bg} border ${c.border} rounded-xl p-5`}>
                  <div className="flex items-center justify-between mb-1">
                    <div className="flex items-center gap-3">
                      <span className={`text-xs font-bold ${c.text}`}>Hafta {item.week}</span>
                      <span className="text-xs text-gray-400">{item.phase}</span>
                    </div>
                  </div>
                  <h3 className="text-lg font-semibold text-white">{item.title}</h3>
                  <p className="text-sm text-gray-400 mt-1">{item.desc}</p>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Bottom CTA */}
      <div className="text-center py-6">
        <Link
          to="/modules"
          className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
        >
          Eğitime Başla →
        </Link>
      </div>
    </div>
  );
}
