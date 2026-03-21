import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getProgressOverview, getPhases, getDailyGoal, getSuggestions } from '../api/client';
import type { ProgressOverview, Phase } from '../types';
import ResumeBar from '../components/dashboard/ResumeBar';

interface DailyGoalData {
  date: string;
  targets: { lessons: number; quizzes: number; challenges: number; time_minutes: number };
  progress: { lessons: number; quizzes: number; challenges: number; time_minutes: number };
  completed: boolean;
}

interface Suggestion {
  type: string;
  title: string;
  link: string;
  icon: string;
  reason: string;
}

export default function DashboardPage() {
  const [overview, setOverview] = useState<ProgressOverview | null>(null);
  const [phases, setPhases] = useState<Phase[]>([]);
  const [goal, setGoal] = useState<DailyGoalData | null>(null);
  const [suggestions, setSuggestions] = useState<Suggestion[]>([]);

  useEffect(() => {
    getProgressOverview().then(setOverview).catch(console.error);
    getPhases().then(setPhases).catch(console.error);
    getDailyGoal().then(setGoal).catch(console.error);
    getSuggestions().then(setSuggestions).catch(console.error);
  }, []);

  if (!overview) return <div className="text-gray-400">Yükleniyor...</div>;

  const streakMessages = [
    { min: 0, msg: 'Bugün başla, streak oluştur!' },
    { min: 1, msg: 'Harika başlangıç, devam et!' },
    { min: 3, msg: 'Süper gidiyorsun!' },
    { min: 7, msg: 'Bir haftalık disiplin, etkileyici!' },
    { min: 14, msg: 'İki hafta, alışkanlık oluşuyor!' },
    { min: 30, msg: 'Bir ay! Artık durdurulamaz!' },
  ];
  const streakMsg = [...streakMessages].reverse().find(s => overview.current_streak_days >= s.min)?.msg || '';

  return (
    <div className="space-y-6">
      {/* Resume Bar */}
      <ResumeBar />

      {/* Welcome + Streak */}
      <div className="bg-gradient-to-r from-blue-600/20 to-purple-600/20 border border-blue-500/30 rounded-xl p-6">
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-2xl font-bold text-white mb-2">Hos Geldin, Developer! </h1>
            <p className="text-gray-300">
              AI-Capable Full Stack Developer olma yolculugunda {Math.round(overview.overall_completion_percent)}% ilerleme kaydettin.
            </p>
          </div>
          <div className="text-right shrink-0 ml-4">
            <div className="text-3xl font-bold text-orange-400">{overview.current_streak_days}</div>
            <div className="text-xs text-orange-300/80 font-medium">gun streak</div>
          </div>
        </div>
        <div className="flex items-center gap-4 mt-3">
          <span className="text-sm text-orange-300/80">{streakMsg}</span>
        </div>
        {overview.next_lesson && (
          <Link
            to={`/lesson/${encodeURIComponent(overview.next_lesson.id)}`}
            className="inline-flex items-center gap-2 mt-4 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm transition-colors"
          >
            Devam Et: {overview.next_lesson.title}
          </Link>
        )}
      </div>

      {/* Daily Goal + Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Daily Goal */}
        {goal && (
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-5 md:col-span-1">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-semibold text-gray-400">Gunluk Hedef</h3>
            </div>
            <div className="space-y-3">
              <GoalBar label="Ders" icon="📖" current={goal.progress.lessons} target={goal.targets.lessons} />
              <GoalBar label="Quiz" icon="✅" current={goal.progress.quizzes} target={goal.targets.quizzes} />
              <GoalBar label="Challenge" icon="💻" current={goal.progress.challenges} target={goal.targets.challenges} />
              <GoalBar label="Sure" icon="⏱️" current={goal.progress.time_minutes} target={goal.targets.time_minutes} suffix="dk" />
            </div>
          </div>
        )}

        {/* Stats Grid */}
        <div className="grid grid-cols-2 gap-3 md:col-span-2">
          <StatCard
            title="Dersler"
            value={`${overview.lessons.completed}/${overview.lessons.total}`}
            icon="📚"
            color="blue"
          />
          <StatCard
            title="Quizler"
            value={`${overview.quizzes.passed}/${overview.quizzes.total}`}
            subtitle={overview.quizzes.average_score > 0 ? `Ort: %${overview.quizzes.average_score}` : undefined}
            icon="✅"
            color="green"
          />
          <StatCard
            title="Challenges"
            value={`${overview.challenges.solved}/${overview.challenges.total}`}
            icon="💻"
            color="purple"
          />
          <StatCard
            title="Projeler"
            value={`${overview.projects.completed}/${overview.projects.total}`}
            subtitle={overview.projects.in_progress > 0 ? `${overview.projects.in_progress} devam ediyor` : undefined}
            icon="🏗️"
            color="orange"
          />
        </div>
      </div>

      {/* Suggestions */}
      {suggestions.length > 0 && (
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
          <h3 className="text-sm font-semibold text-gray-400 mb-3">Onerilen Aksiyonlar</h3>
          <div className="space-y-2">
            {suggestions.map((s, i) => (
              <Link
                key={i}
                to={s.link}
                className="flex items-center gap-3 p-3 hover:bg-gray-800/50 rounded-lg transition-colors"
              >
                <span className="text-lg">{s.icon}</span>
                <div className="flex-1">
                  <div className="text-sm text-gray-200">{s.title}</div>
                  <div className="text-xs text-gray-500">{s.reason}</div>
                </div>
                <span className="text-gray-600 text-sm">&rarr;</span>
              </Link>
            ))}
          </div>
        </div>
      )}

      {/* Today + Weekly Activity */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
          <h3 className="text-sm font-semibold text-gray-400 mb-3">Bugun</h3>
          <div className="flex items-center gap-6">
            <div>
              <div className="text-2xl font-bold text-white">
                {Math.round(overview.today.time_seconds / 60)} dk
              </div>
              <div className="text-xs text-gray-500">calisma suresi</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-white">{overview.today.lessons_completed}</div>
              <div className="text-xs text-gray-500">ders tamamlandi</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-white">{overview.today.challenges_solved}</div>
              <div className="text-xs text-gray-500">challenge cozuldu</div>
            </div>
          </div>
        </div>

        <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
          <h3 className="text-sm font-semibold text-gray-400 mb-3">Haftalik Aktivite</h3>
          <div className="flex items-end gap-1 h-16">
            {overview.weekly_activity.map((day, i) => {
              const maxSec = Math.max(...overview.weekly_activity.map(d => d.seconds), 1);
              const h = Math.max((day.seconds / maxSec) * 100, 4);
              return (
                <div key={i} className="flex-1 flex flex-col items-center gap-1">
                  <div
                    className="w-full bg-blue-500/60 rounded-sm transition-all"
                    style={{ height: `${h}%` }}
                    title={`${day.date}: ${Math.round(day.seconds / 60)} dk`}
                  />
                  <span className="text-[10px] text-gray-600">
                    {new Date(day.date).toLocaleDateString('tr', { weekday: 'narrow' })}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Phase Progress */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
        <h3 className="text-sm font-semibold text-gray-400 mb-4">Faz Ilerlemesi</h3>
        <div className="space-y-3">
          {phases.map((phase) => {
            const pct = phase.total_lessons > 0
              ? Math.round((phase.completed_lessons / phase.total_lessons) * 100) : 0;
            return (
              <Link
                key={phase.id}
                to={`/modules?phase=${phase.id}`}
                className="block hover:bg-gray-800/50 rounded-lg p-3 transition-colors"
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="text-sm text-gray-200">
                    {phase.icon} {phase.title}
                  </span>
                  <span className="text-xs text-gray-500">
                    {phase.completed_lessons}/{phase.total_lessons} ders · {pct}%
                  </span>
                </div>
                <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded-full transition-all"
                    style={{ width: `${pct}%` }}
                  />
                </div>
              </Link>
            );
          })}
        </div>
      </div>

      {/* English Progress */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-sm font-semibold text-gray-400">Teknik Ingilizce</h3>
          <Link to="/english" className="text-xs text-blue-400 hover:underline">Detay &rarr;</Link>
        </div>
        <div className="flex items-center gap-4">
          <div className="text-lg font-bold text-white">
            {overview.english.learned}/{overview.english.total} kelime
          </div>
          <div className="flex-1 h-2 bg-gray-800 rounded-full overflow-hidden">
            <div
              className="h-full bg-green-500 rounded-full"
              style={{ width: `${overview.english.total > 0 ? (overview.english.learned / overview.english.total) * 100 : 0}%` }}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

function GoalBar({ label, icon, current, target, suffix }: {
  label: string; icon: string; current: number; target: number; suffix?: string;
}) {
  const pct = target > 0 ? Math.min((current / target) * 100, 100) : 0;
  const done = current >= target;
  return (
    <div>
      <div className="flex items-center justify-between mb-1">
        <span className="text-xs text-gray-400">{icon} {label}</span>
        <span className={`text-xs font-medium ${done ? 'text-green-400' : 'text-gray-500'}`}>
          {current}/{target}{suffix ? ` ${suffix}` : ''} {done ? '✓' : ''}
        </span>
      </div>
      <div className="h-1.5 bg-gray-800 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full transition-all ${done ? 'bg-green-500' : 'bg-blue-500'}`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}

function StatCard({ title, value, subtitle, icon, color }: {
  title: string; value: string; subtitle?: string; icon: string; color: string;
}) {
  const borderColors: Record<string, string> = {
    blue: 'border-blue-500/30', green: 'border-green-500/30',
    purple: 'border-purple-500/30', orange: 'border-orange-500/30',
  };
  return (
    <div className={`bg-gray-900 border ${borderColors[color] || 'border-gray-800'} rounded-xl p-4`}>
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs text-gray-500 uppercase">{title}</span>
        <span className="text-lg">{icon}</span>
      </div>
      <div className="text-xl font-bold text-white">{value}</div>
      {subtitle && <div className="text-xs text-gray-500 mt-1">{subtitle}</div>}
    </div>
  );
}
