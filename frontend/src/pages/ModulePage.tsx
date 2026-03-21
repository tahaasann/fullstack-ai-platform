import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getModule, getModuleQuizzes } from '../api/client';
import type { ModuleDetail, Quiz, Lesson } from '../types';

export default function ModulePage() {
  const { moduleId } = useParams();
  const [module, setModule] = useState<ModuleDetail | null>(null);
  const [quizzes, setQuizzes] = useState<Quiz[]>([]);

  useEffect(() => {
    if (!moduleId) return;
    getModule(moduleId).then(setModule).catch(console.error);
    getModuleQuizzes(moduleId).then(setQuizzes).catch(console.error);
  }, [moduleId]);

  if (!module) return <div className="text-gray-400">Yükleniyor...</div>;

  return (
    <div className="space-y-6">
      <div className="mb-6">
        <Link to="/modules" className="text-sm text-blue-400 hover:underline">← Modüller</Link>
        <h1 className="text-2xl font-bold text-white mt-2">{module.title}</h1>
        <p className="text-gray-400 mt-1">{module.description}</p>
        <div className="text-sm text-gray-500 mt-2">Tahmini süre: {module.estimated_hours} saat</div>
      </div>

      {/* Lessons */}
      <div className="space-y-2 mb-8">
        <h2 className="text-lg font-semibold text-gray-300 mb-3">Dersler</h2>
        {module.lessons?.length === 0 && (
          <p className="text-gray-500 text-sm italic">Bu modülün dersleri henüz eklenmedi.</p>
        )}
        {module.lessons?.map((lesson: Lesson, i: number) => (
          <Link
            key={lesson.id}
            to={`/lesson/${encodeURIComponent(lesson.id)}`}
            className="flex items-center gap-4 p-4 bg-gray-900 border border-gray-800 hover:border-gray-700 rounded-lg transition-colors"
          >
            <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
              lesson.status === 'completed' ? 'bg-green-600 text-white' :
              lesson.status === 'in_progress' ? 'bg-blue-600 text-white' :
              'bg-gray-800 text-gray-500'
            }`}>
              {lesson.status === 'completed' ? '✓' : i + 1}
            </div>
            <div className="flex-1">
              <h3 className="text-sm font-medium text-gray-200">{lesson.title}</h3>
              <p className="text-xs text-gray-500">{lesson.estimated_minutes} dakika</p>
            </div>
            <div className="flex gap-1">
              {lesson.tags?.map((tag: string) => (
                <span key={tag} className="px-2 py-0.5 bg-gray-800 text-gray-400 rounded text-xs">{tag}</span>
              ))}
            </div>
          </Link>
        ))}
      </div>

      {/* Quizzes */}
      {quizzes.length > 0 && (
        <div className="space-y-2 mb-8">
          <h2 className="text-lg font-semibold text-gray-300 mb-3">Quizler</h2>
          {quizzes.map((quiz: Quiz) => (
            <Link
              key={quiz.id}
              to={`/quiz/${encodeURIComponent(quiz.id)}`}
              className="flex items-center justify-between p-4 bg-gray-900 border border-gray-800 hover:border-gray-700 rounded-lg transition-colors"
            >
              <div>
                <h3 className="text-sm font-medium text-gray-200">{quiz.title}</h3>
                <p className="text-xs text-gray-500">{quiz.description}</p>
              </div>
              <div className="text-right">
                {quiz.best_score !== null ? (
                  <span className={`text-sm font-bold ${(quiz as Quiz & { passed?: boolean }).passed ? 'text-green-400' : 'text-red-400'}`}>
                    %{quiz.best_score}
                  </span>
                ) : (
                  <span className="text-xs text-gray-500">Çözülmedi</span>
                )}
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
