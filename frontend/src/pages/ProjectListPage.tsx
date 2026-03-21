import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getProjects } from '../api/client';
import type { Project } from '../types';

export default function ProjectListPage() {
  const [projects, setProjects] = useState<Project[]>([]);

  useEffect(() => {
    getProjects().then(setProjects).catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-white mb-2">Portfolyo Projeleri</h1>
      <p className="text-gray-400 text-sm mb-6">10 proje ile "bu adam bu işi biliyor" dedirtecek portföy oluştur.</p>

      <div className="space-y-3">
        {projects.map((project, i) => {
          const pct = project.total_milestones > 0
            ? Math.round((project.completed_milestones / project.total_milestones) * 100) : 0;
          return (
            <Link
              key={project.id}
              to={`/project/${project.id}`}
              className="block p-5 bg-gray-900 border border-gray-800 hover:border-gray-700 rounded-xl transition-colors"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-1">
                    <span className="text-lg font-bold text-gray-600">#{i + 1}</span>
                    <h3 className="text-lg font-semibold text-white">{project.title}</h3>
                    <StatusBadge status={project.status} />
                  </div>
                  <p className="text-sm text-gray-400 mt-1">{project.description}</p>
                  <div className="flex flex-wrap gap-2 mt-3">
                    {project.tech_stack?.map((tech: string) => (
                      <span key={tech} className="px-2 py-0.5 bg-gray-800 text-gray-400 rounded text-xs">{tech}</span>
                    ))}
                  </div>
                </div>
                <div className="text-right ml-4 shrink-0">
                  <div className="text-sm font-bold text-white">{pct}%</div>
                  <div className="text-xs text-gray-400">
                    {project.completed_milestones}/{project.total_milestones} milestone
                  </div>
                </div>
              </div>
              {pct > 0 && (
                <div className="mt-3 h-1.5 bg-gray-800 rounded-full overflow-hidden">
                  <div className="h-full bg-purple-500 rounded-full transition-all" style={{ width: `${pct}%` }} />
                </div>
              )}
            </Link>
          );
        })}
        {projects.length === 0 && (
          <p className="text-gray-400 text-sm text-center py-8">Henüz proje eklenmedi.</p>
        )}
      </div>
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const map: Record<string, { label: string; cls: string }> = {
    not_started: { label: 'Başlanmadı', cls: 'bg-gray-800 text-gray-400' },
    in_progress: { label: 'Devam Ediyor', cls: 'bg-blue-900/50 text-blue-400' },
    completed: { label: 'Tamamlandı', cls: 'bg-green-900/50 text-green-400' },
  };
  const s = map[status] || map.not_started;
  return <span className={`px-2 py-0.5 rounded text-xs font-medium ${s.cls}`}>{s.label}</span>;
}
