import { useEffect, useState } from 'react';
import { getLinkedInGuide } from '../api/client';
import type { CareerGuide, CareerSection } from '../types';
import MarkdownRenderer from '../components/common/MarkdownRenderer';

export default function LinkedInGuidePage() {
  const [guide, setGuide] = useState<CareerGuide | null>(null);
  const [expandedId, setExpandedId] = useState<string | null>(null);

  useEffect(() => {
    getLinkedInGuide().then(setGuide).catch(console.error);
  }, []);

  if (!guide) return <div className="text-gray-400">Yükleniyor...</div>;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">LinkedIn Profil Optimizasyonu</h1>
        <p className="text-gray-400 mt-1">{guide.description}</p>
      </div>

      <div className="space-y-3">
        {guide.sections?.map((section: CareerSection) => {
          const isOpen = expandedId === section.id;
          return (
            <div key={section.id} className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
              <button
                onClick={() => setExpandedId(isOpen ? null : section.id)}
                className="w-full flex items-center justify-between p-5 text-left hover:bg-gray-800/50 transition-colors"
              >
                <div className="flex items-center gap-3">
                  <span className="text-xl">{section.icon}</span>
                  <h2 className="text-lg font-semibold text-white">{section.title}</h2>
                </div>
                <span className="text-gray-400 text-lg">{isOpen ? '−' : '+'}</span>
              </button>

              {isOpen && (
                <div className="px-5 pb-5 border-t border-gray-800 pt-4 space-y-4">
                  {section.content && (
                    <MarkdownRenderer content={section.content} className="text-sm" />
                  )}

                  {section.templates && (
                    <div className="space-y-2">
                      <h3 className="text-sm font-semibold text-gray-400">Sablonlar:</h3>
                      {section.templates.map((t: string, i: number) => (
                        <div key={i} className="bg-gray-950 rounded-lg p-3 font-mono text-sm text-green-400">{t}</div>
                      ))}
                    </div>
                  )}

                  {section.examples && section.examples.length > 0 && (
                    <div className="space-y-2">
                      <h3 className="text-sm font-semibold text-gray-400">Ornekler:</h3>
                      {section.examples.map((ex: string, i: number) => (
                        <div key={i} className="bg-blue-900/20 border border-blue-800/30 rounded-lg p-3 text-sm text-blue-300">{ex}</div>
                      ))}
                    </div>
                  )}

                  {section.tips && section.tips.length > 0 && (
                    <div>
                      <h3 className="text-sm font-semibold text-gray-400 mb-2">İpuçları:</h3>
                      <ul className="space-y-1">
                        {section.tips.map((tip: string, i: number) => (
                          <li key={i} className="text-sm text-gray-300 flex items-start gap-2">
                            <span className="text-green-400 mt-0.5">✓</span>
                            {tip}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {section.checklist && section.checklist.length > 0 && (
                    <div>
                      <h3 className="text-sm font-semibold text-gray-400 mb-2">Checklist:</h3>
                      <ul className="space-y-1">
                        {section.checklist.map((item: string, i: number) => (
                          <li key={i} className="text-sm text-gray-300 flex items-start gap-2">
                            <span className="text-yellow-400">☐</span>
                            {item}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
