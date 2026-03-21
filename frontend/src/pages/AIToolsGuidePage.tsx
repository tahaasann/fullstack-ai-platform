import { useEffect, useState } from 'react';
import { getAIToolsGuide } from '../api/client';
import type { CareerGuide, CareerSection, CareerModelComparison, CareerWorkflowTemplate, CareerAntiPattern } from '../types';
import MarkdownRenderer from '../components/common/MarkdownRenderer';

export default function AIToolsGuidePage() {
  const [guide, setGuide] = useState<CareerGuide | null>(null);
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'models' | 'guide' | 'workflows' | 'antipatterns'>('models');

  useEffect(() => {
    getAIToolsGuide().then(setGuide).catch(console.error);
  }, []);

  if (!guide) return <div className="text-gray-400">Yükleniyor...</div>;

  const tabs = [
    { id: 'models' as const, label: 'Model Karşılaştırma', icon: '🤖' },
    { id: 'guide' as const, label: 'Kullanım Rehberi', icon: '📖' },
    { id: 'workflows' as const, label: 'Workflow Şablonları', icon: '⚡' },
    { id: 'antipatterns' as const, label: 'Anti-Patterns', icon: '⚠️' },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">AI Araçları Rehberi</h1>
        <p className="text-gray-400 mt-1">{guide.description}</p>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 border-b border-gray-800 pb-2">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              activeTab === tab.id
                ? 'bg-violet-600/20 text-violet-400 border border-violet-500/30'
                : 'text-gray-400 hover:bg-gray-800 hover:text-gray-200'
            }`}
          >
            {tab.icon} {tab.label}
          </button>
        ))}
      </div>

      {/* Model Comparison */}
      {activeTab === 'models' && guide.model_comparison && (
        <div className="space-y-4">
          {guide.model_comparison.map((model: CareerModelComparison) => (
            <div key={model.name} className="bg-gray-900 border border-gray-800 rounded-xl p-5">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-lg font-bold text-white">{model.name}</h3>
                <span className="text-xs px-2 py-1 bg-violet-900/30 text-violet-400 rounded">{model.provider}</span>
              </div>
              <p className="text-sm text-gray-400 mb-3">{model.when_to_use}</p>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div>
                  <h4 className="text-xs font-semibold text-gray-400 uppercase mb-1">Güçlü Yanları</h4>
                  <ul className="space-y-1">
                    {model.strengths?.map((s: string, i: number) => (
                      <li key={i} className="text-sm text-green-400 flex items-start gap-1">
                        <span>+</span> {s}
                      </li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h4 className="text-xs font-semibold text-gray-400 uppercase mb-1">En İyi İçin</h4>
                  <ul className="space-y-1">
                    {model.best_for?.map((b: string, i: number) => (
                      <li key={i} className="text-sm text-blue-400 flex items-start gap-1">
                        <span>→</span> {b}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              <div className="flex gap-4 mt-3 text-xs text-gray-400">
                <span>Context: {model.context_window}</span>
                <span>Fiyat: {model.pricing_tier}</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Guide Sections */}
      {activeTab === 'guide' && guide.sections && (
        <div className="space-y-3">
          {guide.sections.map((section: CareerSection) => {
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
                  <div className="px-5 pb-5 border-t border-gray-800 pt-4 space-y-3">
                    <MarkdownRenderer content={section.content} className="text-sm" />
                    {section.examples?.map((ex: string, i: number) => (
                      <div key={i} className="bg-violet-900/20 border border-violet-800/30 rounded-lg p-3 text-sm text-violet-300 font-mono">{ex}</div>
                    ))}
                    {section.tips?.length > 0 && (
                      <ul className="space-y-1">
                        {section.tips.map((tip: string, i: number) => (
                          <li key={i} className="text-sm text-gray-300 flex items-start gap-2">
                            <span className="text-violet-400">💡</span> {tip}
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}

      {/* Workflow Templates */}
      {activeTab === 'workflows' && guide.workflow_templates && (
        <div className="space-y-3">
          {guide.workflow_templates.map((wf: CareerWorkflowTemplate, i: number) => (
            <div key={i} className="bg-gray-900 border border-gray-800 rounded-xl p-5">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-white font-semibold">{wf.task}</h3>
                <span className="text-xs px-2 py-1 bg-blue-900/30 text-blue-400 rounded">{wf.recommended_model}</span>
              </div>
              <div className="bg-gray-950 rounded-lg p-3 mb-3">
                <MarkdownRenderer content={wf.prompt_template} className="text-sm text-green-400 font-mono" />
              </div>
              {wf.tips?.map((tip: string, j: number) => (
                <p key={j} className="text-sm text-gray-400 flex items-start gap-2">
                  <span className="text-yellow-400">💡</span> {tip}
                </p>
              ))}
            </div>
          ))}
        </div>
      )}

      {/* Anti-patterns */}
      {activeTab === 'antipatterns' && guide.anti_patterns && (
        <div className="space-y-3">
          {guide.anti_patterns.map((ap: CareerAntiPattern, i: number) => (
            <div key={i} className="bg-gray-900 border border-red-900/30 rounded-xl p-5">
              <h3 className="text-red-400 font-semibold mb-2">❌ {ap.pattern}</h3>
              <p className="text-sm text-gray-400 mb-3">{ap.description}</p>
              <div className="bg-green-900/20 border border-green-800/30 rounded-lg p-3">
                <h4 className="text-xs font-semibold text-green-400 mb-1">Doğru Yaklaşım:</h4>
                <p className="text-sm text-green-300">{ap.better_approach}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
