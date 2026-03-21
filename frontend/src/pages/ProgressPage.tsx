import { useEffect, useState } from 'react';
import { getProgressOverview, getPhases } from '../api/client';
import type { ProgressOverview, Phase } from '../types';
import { RadarChart, PolarGrid, PolarAngleAxis, Radar, ResponsiveContainer } from 'recharts';

export default function ProgressPage() {
  const [overview, setOverview] = useState<ProgressOverview | null>(null);
  const [phases, setPhases] = useState<Phase[]>([]);

  useEffect(() => {
    getProgressOverview().then(setOverview).catch(console.error);
    getPhases().then(setPhases).catch(console.error);
  }, []);

  if (!overview) return <div className="text-gray-400">Yükleniyor...</div>;

  const radarData = [
    { subject: 'Dersler', value: overview.lessons.total > 0 ? (overview.lessons.completed / overview.lessons.total) * 100 : 0 },
    { subject: 'Quizler', value: overview.quizzes.total > 0 ? (overview.quizzes.passed / overview.quizzes.total) * 100 : 0 },
    { subject: 'Challenges', value: overview.challenges.total > 0 ? (overview.challenges.solved / overview.challenges.total) * 100 : 0 },
    { subject: 'Projeler', value: overview.projects.total > 0 ? (overview.projects.completed / overview.projects.total) * 100 : 0 },
    { subject: 'İngilizce', value: overview.english.total > 0 ? (overview.english.learned / overview.english.total) * 100 : 0 },
  ];

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-white">📊 İlerleme Detayları</h1>

      {/* Overall + Streak */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-5 text-center">
          <div className="text-4xl font-bold text-blue-400">{Math.round(overview.overall_completion_percent)}%</div>
          <div className="text-sm text-gray-400 mt-1">Genel İlerleme</div>
        </div>
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-5 text-center">
          <div className="text-4xl font-bold text-orange-400">{overview.current_streak_days}</div>
          <div className="text-sm text-gray-400 mt-1">Gün Serisi 🔥</div>
        </div>
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-5 text-center">
          <div className="text-4xl font-bold text-purple-400">{overview.total_study_hours}</div>
          <div className="text-sm text-gray-400 mt-1">Toplam Saat</div>
        </div>
      </div>

      {/* Radar Chart */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
        <h3 className="text-sm font-semibold text-gray-400 mb-4">Beceri Dağılımı</h3>
        <ResponsiveContainer width="100%" height={300}>
          <RadarChart data={radarData}>
            <PolarGrid stroke="#374151" />
            <PolarAngleAxis dataKey="subject" tick={{ fill: '#9ca3af', fontSize: 12 }} />
            <Radar dataKey="value" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.3} />
          </RadarChart>
        </ResponsiveContainer>
      </div>

      {/* Weekly Heatmap */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
        <h3 className="text-sm font-semibold text-gray-400 mb-4">Haftalık Aktivite</h3>
        <div className="flex items-end gap-1 h-24">
          {overview.weekly_activity.map((day, i) => {
            const maxSec = Math.max(...overview.weekly_activity.map(d => d.seconds), 1);
            const h = Math.max((day.seconds / maxSec) * 100, 4);
            const minutes = Math.round(day.seconds / 60);
            return (
              <div key={i} className="flex-1 flex flex-col items-center gap-1">
                <div className="text-xs text-gray-500">{minutes}dk</div>
                <div
                  className="w-full bg-blue-500/60 rounded-sm transition-all"
                  style={{ height: `${h}%` }}
                />
                <span className="text-[10px] text-gray-600">
                  {new Date(day.date).toLocaleDateString('tr', { weekday: 'short' })}
                </span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Stats Breakdown */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatDetail label="Dersler" completed={overview.lessons.completed} total={overview.lessons.total} color="blue" />
        <StatDetail label="Quizler" completed={overview.quizzes.passed} total={overview.quizzes.total} extra={`Ort: %${overview.quizzes.average_score}`} color="green" />
        <StatDetail label="Challenges" completed={overview.challenges.solved} total={overview.challenges.total} color="purple" />
        <StatDetail label="Projeler" completed={overview.projects.completed} total={overview.projects.total} extra={`${overview.projects.in_progress} devam`} color="orange" />
      </div>

      {/* Phase Breakdown */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
        <h3 className="text-sm font-semibold text-gray-400 mb-4">Faz Detayları</h3>
        <div className="space-y-4">
          {phases.map((phase) => {
            const pct = phase.total_lessons > 0 ? Math.round((phase.completed_lessons / phase.total_lessons) * 100) : 0;
            return (
              <div key={phase.id}>
                <div className="flex items-center justify-between mb-1">
                  <span className="text-sm text-gray-200">{phase.icon} {phase.title}</span>
                  <span className="text-xs text-gray-500">{pct}% · {phase.completed_lessons}/{phase.total_lessons} ders</span>
                </div>
                <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
                  <div className="h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded-full" style={{ width: `${pct}%` }} />
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

function StatDetail({ label, completed, total, extra, color }: {
  label: string; completed: number; total: number; extra?: string; color: string;
}) {
  const pct = total > 0 ? Math.round((completed / total) * 100) : 0;
  const colorMap: Record<string, string> = {
    blue: 'text-blue-400', green: 'text-green-400', purple: 'text-purple-400', orange: 'text-orange-400',
  };
  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl p-4">
      <div className="text-xs text-gray-500 uppercase mb-2">{label}</div>
      <div className={`text-2xl font-bold ${colorMap[color]}`}>{completed}/{total}</div>
      <div className="text-xs text-gray-500 mt-1">{pct}% tamamlandı</div>
      {extra && <div className="text-xs text-gray-600 mt-0.5">{extra}</div>}
    </div>
  );
}
