import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getChallenges } from '../api/client';
import type { Challenge } from '../types';

export default function ChallengeListPage() {
  const [challenges, setChallenges] = useState<Challenge[]>([]);
  const [filter, setFilter] = useState({ difficulty: '', status: '' });

  useEffect(() => {
    getChallenges({ difficulty: filter.difficulty || undefined })
      .then((data) => {
        if (filter.status === 'solved') return data.filter((c: Challenge) => c.solved);
        if (filter.status === 'not_started') return data.filter((c: Challenge) => !c.solved);
        return data;
      })
      .then(setChallenges)
      .catch(console.error);
  }, [filter]);

  const diffColors: Record<string, string> = {
    kolay: 'text-green-400', orta: 'text-yellow-400', zor: 'text-red-400', expert: 'text-purple-400',
    easy: 'text-green-400', medium: 'text-yellow-400', hard: 'text-red-400',
  };
  const diffLabels: Record<string, string> = { kolay: 'Kolay', orta: 'Orta', zor: 'Zor', expert: 'Uzman', easy: 'Kolay', medium: 'Orta', hard: 'Zor' };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-white mb-6">Challenges</h1>

      {/* Filters */}
      <div className="flex gap-3 mb-6">
        <select
          value={filter.difficulty}
          onChange={(e) => setFilter((f) => ({ ...f, difficulty: e.target.value }))}
          className="bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-sm text-gray-300"
        >
          <option value="">Tüm Zorluklar</option>
          <option value="kolay">Kolay</option>
          <option value="orta">Orta</option>
          <option value="zor">Zor</option>
          <option value="expert">Uzman</option>
        </select>
        <select
          value={filter.status}
          onChange={(e) => setFilter((f) => ({ ...f, status: e.target.value }))}
          className="bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-sm text-gray-300"
        >
          <option value="">Tüm Durumlar</option>
          <option value="solved">Çözüldü</option>
          <option value="not_started">Çözülmedi</option>
        </select>
      </div>

      {/* List */}
      <div className="space-y-2">
        {challenges.map((ch) => (
          <Link
            key={ch.id}
            to={`/challenge/${ch.id}`}
            className="flex items-center justify-between p-4 bg-gray-900 border border-gray-800 hover:border-gray-700 rounded-lg transition-colors"
          >
            <div className="flex items-center gap-4">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm ${
                ch.solved ? 'bg-green-600 text-white' :
                'bg-gray-800 text-gray-500'
              }`}>
                {ch.solved ? '✓' : '?'}
              </div>
              <div>
                <h3 className="text-sm font-medium text-gray-200">{ch.title}</h3>
                <p className="text-xs text-gray-500 mt-0.5">{(ch as Challenge & { module_title?: string }).module_title}</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              {ch.tags?.map((tag: string) => (
                <span key={tag} className="px-2 py-0.5 bg-gray-800 text-gray-500 rounded text-xs">{tag}</span>
              ))}
              <span className={`text-xs font-medium ${diffColors[ch.difficulty] || 'text-gray-400'}`}>
                {diffLabels[ch.difficulty] || ch.difficulty}
              </span>
            </div>
          </Link>
        ))}
        {challenges.length === 0 && (
          <p className="text-gray-500 text-sm text-center py-8">Henüz challenge eklenmedi.</p>
        )}
      </div>
    </div>
  );
}
