import { useEffect, useState } from 'react';
import toast from 'react-hot-toast';
import { getVocabulary, markVocabLearned, getPatterns, getScenarios, getEnglishProgress } from '../api/client';
import type { VocabularyItem, SentencePattern, Scenario, EnglishProgress } from '../types';

type Tab = 'vocabulary' | 'patterns' | 'scenarios';

export default function EnglishProgressPage() {
  const [tab, setTab] = useState<Tab>('vocabulary');
  const [vocabulary, setVocabulary] = useState<VocabularyItem[]>([]);
  const [patterns, setPatterns] = useState<SentencePattern[]>([]);
  const [scenarios, setScenarios] = useState<Scenario[]>([]);
  const [progress, setProgress] = useState<EnglishProgress | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<'all' | 'learned' | 'not_learned'>('all');
  const [domainFilter, setDomainFilter] = useState<string>('all');
  const [expandedCard, setExpandedCard] = useState<number | null>(null);
  const [expandedScenario, setExpandedScenario] = useState<string | number | null>(null);

  const loadData = () => {
    setLoading(true);
    setError(null);
    Promise.all([
      getVocabulary().then(setVocabulary),
      getPatterns().then(setPatterns),
      getScenarios().then(setScenarios),
      getEnglishProgress().then(setProgress),
    ])
      .catch((err) => setError(err.message || 'Veri yüklenemedi'))
      .finally(() => setLoading(false));
  };

  useEffect(loadData, []);

  const handleLearn = async (id: number) => {
    try {
      await markVocabLearned(id);
      setVocabulary((prev) => prev.map((v) => v.id === id ? { ...v, learned: true } : v));
    } catch (err) {
      toast.error('Kelime durumu güncellenemedi.');
    }
  };

  const domains = [...new Set(vocabulary.map((v) => v.domain))].filter(Boolean);
  const learnedCount = vocabulary.filter((v) => v.learned).length;
  const pct = vocabulary.length > 0 ? Math.round((learnedCount / vocabulary.length) * 100) : 0;

  const filteredVocab = vocabulary.filter((v) => {
    if (filter === 'learned' && !v.learned) return false;
    if (filter === 'not_learned' && v.learned) return false;
    if (domainFilter !== 'all' && v.domain !== domainFilter) return false;
    return true;
  });

  const patternDomains = [...new Set(patterns.map((p) => p.domain))].filter(Boolean);
  const filteredPatterns = domainFilter !== 'all' ? patterns.filter(p => p.domain === domainFilter) : patterns;
  const groupedPatterns: Record<string, SentencePattern[]> = {};
  filteredPatterns.forEach(p => {
    const key = `${p.domain}|${p.category}`;
    if (!groupedPatterns[key]) groupedPatterns[key] = [];
    groupedPatterns[key].push(p);
  });

  const filteredScenarios = domainFilter !== 'all' ? scenarios.filter(s => s.domain === domainFilter) : scenarios;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Teknik İngilizce</h1>
        <p className="text-gray-400 text-sm mt-1">İş hayatında kullanacağın teknik İngilizce kelimeler, kalıplar ve senaryolar</p>
      </div>

      {loading && (
        <div className="flex items-center justify-center py-12">
          <div className="text-gray-400 text-sm">Yükleniyor...</div>
        </div>
      )}

      {error && (
        <div className="bg-red-900/20 border border-red-500/30 rounded-xl p-4 flex items-center justify-between">
          <span className="text-red-400 text-sm">{error}</span>
          <button onClick={loadData} className="text-sm px-3 py-1 bg-red-600 hover:bg-red-700 text-white rounded transition-colors">
            Tekrar Dene
          </button>
        </div>
      )}

      {/* Overall Progress */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-sm font-semibold text-gray-400">Genel İlerleme</h3>
          <div className="flex items-center gap-4 text-sm text-gray-300">
            <span>{learnedCount}/{vocabulary.length} kelime</span>
            {progress && <span>{progress.total_patterns} kalıp</span>}
            {progress && <span>{progress.total_scenarios} senaryo</span>}
          </div>
        </div>
        <div className="h-3 bg-gray-800 rounded-full overflow-hidden">
          <div className="h-full bg-emerald-500 rounded-full transition-all" style={{ width: `${pct}%` }} />
        </div>
      </div>

      {/* Domain Breakdown */}
      {domains.length > 0 && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {domains.map((domain) => {
            const domainWords = vocabulary.filter((v) => v.domain === domain);
            const domainLearned = domainWords.filter((v) => v.learned).length;
            const isActive = domainFilter === domain;
            return (
              <button
                key={domain}
                onClick={() => setDomainFilter(isActive ? 'all' : domain)}
                className={`bg-gray-900 border rounded-xl p-4 text-left transition-colors ${
                  isActive ? 'border-emerald-500/50 bg-emerald-900/10' : 'border-gray-800 hover:border-gray-700'
                }`}
              >
                <div className="text-xs text-gray-400 uppercase mb-1">{domain}</div>
                <div className="text-lg font-bold text-white">{domainLearned}/{domainWords.length}</div>
              </button>
            );
          })}
        </div>
      )}

      {/* Tabs */}
      <div className="flex gap-1 bg-gray-900 border border-gray-800 rounded-xl p-1">
        {([
          { value: 'vocabulary' as Tab, label: 'Kelimeler', count: vocabulary.length },
          { value: 'patterns' as Tab, label: 'Cümle Kalıpları', count: patterns.length },
          { value: 'scenarios' as Tab, label: 'İş Senaryoları', count: scenarios.length },
        ]).map((t) => (
          <button
            key={t.value}
            onClick={() => setTab(t.value)}
            className={`flex-1 px-4 py-2.5 rounded-lg text-sm font-medium transition-colors ${
              tab === t.value
                ? 'bg-emerald-600 text-white'
                : 'text-gray-400 hover:text-white hover:bg-gray-800'
            }`}
          >
            {t.label} ({t.count})
          </button>
        ))}
      </div>

      {/* Vocabulary Tab */}
      {tab === 'vocabulary' && (
        <>
          {/* Filter */}
          <div className="flex gap-2">
            {[
              { value: 'all' as const, label: 'Tümü' },
              { value: 'not_learned' as const, label: 'Öğrenilmemiş' },
              { value: 'learned' as const, label: 'Öğrenilmiş' },
            ].map((f) => (
              <button
                key={f.value}
                onClick={() => setFilter(f.value)}
                className={`px-3 py-1.5 rounded-lg text-sm transition-colors ${
                  filter === f.value ? 'bg-emerald-600 text-white' : 'bg-gray-800 text-gray-400 hover:text-white'
                }`}
              >
                {f.label}
              </button>
            ))}
          </div>

          {/* Vocabulary Cards */}
          <div className="space-y-3">
            {filteredVocab.map((word) => {
              const isExpanded = expandedCard === word.id;
              return (
                <div
                  key={word.id}
                  className={`rounded-xl border transition-colors ${
                    word.learned ? 'bg-emerald-900/10 border-emerald-500/20' : 'bg-gray-900 border-gray-800'
                  }`}
                >
                  {/* Header */}
                  <div
                    className="p-4 cursor-pointer"
                    onClick={() => setExpandedCard(isExpanded ? null : word.id)}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-3">
                          <span className="font-mono text-emerald-300 font-medium text-lg">{word.term}</span>
                          {word.difficulty_level && (
                            <span className={`px-2 py-0.5 rounded text-[10px] font-medium ${
                              word.difficulty_level === 'beginner' ? 'bg-green-900/30 text-green-400' :
                              word.difficulty_level === 'intermediate' ? 'bg-yellow-900/30 text-yellow-400' :
                              'bg-red-900/30 text-red-400'
                            }`}>
                              {word.difficulty_level}
                            </span>
                          )}
                          {word.domain && (
                            <span className="px-2 py-0.5 bg-gray-800 text-gray-400 rounded text-[10px]">{word.domain}</span>
                          )}
                        </div>
                        {word.pronunciation && <div className="text-xs text-gray-400 mt-0.5">{word.pronunciation}</div>}
                        <div className="text-sm text-gray-400 mt-1">{word.translation}</div>
                        {!isExpanded && <div className="text-xs text-gray-600 mt-1">Detaylar için tıkla</div>}
                      </div>
                      <div className="flex items-center gap-2 shrink-0">
                        {!word.learned && (
                          <button
                            onClick={(e) => { e.stopPropagation(); handleLearn(word.id); }}
                            className="px-3 py-1 bg-emerald-600 hover:bg-emerald-700 text-white rounded text-xs transition-colors"
                          >
                            Öğrendim
                          </button>
                        )}
                        {word.learned && <span className="text-emerald-400 text-sm">✓</span>}
                        <span className={`w-6 h-6 flex items-center justify-center rounded-full bg-gray-800 text-gray-400 transition-transform ${isExpanded ? 'rotate-180' : ''}`}>
                          ▼
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Expanded Details */}
                  {isExpanded && (
                    <div className="border-t border-gray-800 p-4 space-y-4">
                      {/* Definitions */}
                      {(word.definition_en || word.definition_tr) && (
                        <div className="space-y-1">
                          {word.definition_en && (
                            <div className="text-sm text-gray-300">
                              <span className="text-gray-400 text-xs mr-2">EN:</span>{word.definition_en}
                            </div>
                          )}
                          {word.definition_tr && (
                            <div className="text-sm text-gray-400">
                              <span className="text-gray-400 text-xs mr-2">TR:</span>{word.definition_tr}
                            </div>
                          )}
                        </div>
                      )}

                      {/* Example Sentences */}
                      {word.example_sentences?.length > 0 && (
                        <div>
                          <div className="text-xs font-semibold text-gray-400 uppercase mb-2">Örnek Cümleler</div>
                          <div className="space-y-2">
                            {word.example_sentences.map((ex, i: number) => (
                              <div key={i} className="bg-gray-800/50 rounded-lg p-3">
                                <div className="text-sm text-emerald-300">{ex.en}</div>
                                <div className="text-sm text-gray-400 mt-1">{ex.tr}</div>
                                {ex.context && (
                                  <div className="text-xs text-gray-600 mt-1 italic">{ex.context}</div>
                                )}
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Common Patterns */}
                      {word.common_patterns?.length > 0 && (
                        <div>
                          <div className="text-xs font-semibold text-gray-400 uppercase mb-2">Kullanım Kalıpları</div>
                          <div className="space-y-1">
                            {word.common_patterns.map((p: string, i: number) => (
                              <div key={i} className="text-sm text-gray-300 flex items-start gap-2">
                                <span className="text-blue-400 mt-0.5">·</span> {p}
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Scenario */}
                      {word.scenario && (
                        <div>
                          <div className="text-xs font-semibold text-gray-400 uppercase mb-2">İş Senaryosu</div>
                          <div className="text-sm text-gray-300 bg-gray-800/50 rounded-lg p-3">{word.scenario}</div>
                        </div>
                      )}

                      {/* Common Mistakes */}
                      {word.common_mistakes && (
                        <div>
                          <div className="text-xs font-semibold text-gray-400 uppercase mb-2">Sık Yapılan Hatalar</div>
                          <div className="text-sm text-orange-300/80 bg-orange-900/10 border border-orange-500/20 rounded-lg p-3">
                            {word.common_mistakes}
                          </div>
                        </div>
                      )}

                      {/* Related Terms */}
                      {word.related_terms && word.related_terms.length > 0 && (
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className="text-xs text-gray-400">İlişkili:</span>
                          {word.related_terms.map((t: string, i: number) => (
                            <span key={i} className="px-2 py-0.5 bg-gray-800 text-gray-400 rounded text-xs">{t}</span>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          {filteredVocab.length === 0 && (
            <p className="text-gray-400 text-sm text-center py-8">
              {filter === 'not_learned' ? 'Tüm kelimeler öğrenilmiş!' :
               filter === 'learned' ? 'Henüz öğrenilen kelime yok.' :
               'Henüz kelime eklenmedi.'}
            </p>
          )}
        </>
      )}

      {/* Patterns Tab */}
      {tab === 'patterns' && (
        <div className="space-y-6">
          {/* Domain filter for patterns */}
          <div className="flex gap-2 flex-wrap">
            <button
              onClick={() => setDomainFilter('all')}
              className={`px-3 py-1.5 rounded-lg text-sm transition-colors ${
                domainFilter === 'all' ? 'bg-emerald-600 text-white' : 'bg-gray-800 text-gray-400 hover:text-white'
              }`}
            >
              Tümü
            </button>
            {patternDomains.map(d => (
              <button
                key={d}
                onClick={() => setDomainFilter(d)}
                className={`px-3 py-1.5 rounded-lg text-sm transition-colors ${
                  domainFilter === d ? 'bg-emerald-600 text-white' : 'bg-gray-800 text-gray-400 hover:text-white'
                }`}
              >
                {d}
              </button>
            ))}
          </div>

          {Object.entries(groupedPatterns).map(([key, items]) => {
            const [domain, category] = key.split('|');
            return (
              <div key={key} className="bg-gray-900 border border-gray-800 rounded-xl p-5">
                <div className="flex items-center gap-2 mb-4">
                  <span className="px-2 py-0.5 bg-blue-900/30 text-blue-400 rounded text-xs">{domain}</span>
                  <h3 className="text-sm font-semibold text-gray-300">{category}</h3>
                </div>
                <div className="space-y-4">
                  {items.map((p) => (
                    <div key={p.id ?? p.pattern} className="border-l-2 border-blue-500/30 pl-4">
                      <div className="font-mono text-sm text-emerald-300 mb-1">{p.pattern}</div>
                      <div className="text-sm text-gray-400 mb-2">{p.turkish}</div>
                      {p.when_to_use && (
                        <div className="text-xs text-gray-400 mb-2">
                          <span className="text-gray-600 font-medium">Ne zaman:</span> {p.when_to_use}
                        </div>
                      )}
                      {p.variations?.length > 0 && (
                        <div className="space-y-1 mb-2">
                          <div className="text-xs text-gray-600 font-medium">Varyasyonlar:</div>
                          {p.variations.map((v: string, i: number) => (
                            <div key={i} className="text-xs text-gray-400 pl-3">· {v}</div>
                          ))}
                        </div>
                      )}
                      {p.real_example && (
                        <div className="bg-gray-800/50 rounded-lg p-3 mt-2">
                          <div className="text-xs text-gray-600 font-medium mb-1">Gerçek Örnek:</div>
                          <div className="text-sm text-gray-300 italic">{p.real_example}</div>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            );
          })}

          {filteredPatterns.length === 0 && (
            <p className="text-gray-400 text-sm text-center py-8">Henüz kalıp eklenmedi.</p>
          )}
        </div>
      )}

      {/* Scenarios Tab */}
      {tab === 'scenarios' && (
        <div className="space-y-4">
          {filteredScenarios.map((scenario) => {
            const isExpanded = expandedScenario === scenario.id;
            return (
              <div key={scenario.id} className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
                <button
                  className="w-full text-left p-5 hover:bg-gray-800/30 transition-colors"
                  onClick={() => setExpandedScenario(isExpanded ? null : scenario.id)}
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        {scenario.domain && (
                          <span className="px-2 py-0.5 bg-purple-900/30 text-purple-400 rounded text-xs">{scenario.domain}</span>
                        )}
                        <h3 className="text-sm font-semibold text-gray-200">{scenario.title}</h3>
                      </div>
                      <p className="text-xs text-gray-400">{scenario.context}</p>
                    </div>
                    <span className={`text-gray-600 transition-transform shrink-0 ml-2 ${isExpanded ? 'rotate-180' : ''}`}>
                      ▼
                    </span>
                  </div>
                </button>

                {isExpanded && (
                  <div className="border-t border-gray-800 p-5 space-y-4">
                    {/* Dialogue */}
                    <div className="space-y-3">
                      {scenario.dialogue?.map((msg, i: number) => (
                        <div
                          key={i}
                          className={`flex gap-3 ${msg.role === 'you' ? 'flex-row-reverse' : ''}`}
                        >
                          <div className={`max-w-[80%] rounded-xl p-3 ${
                            msg.role === 'you'
                              ? 'bg-blue-600/20 border border-blue-500/30'
                              : 'bg-gray-800/80 border border-gray-700/50'
                          }`}>
                            <div className="text-xs text-gray-400 mb-1">
                              {msg.role === 'you' ? 'Sen' : msg.role}
                            </div>
                            <div className="text-sm text-gray-200">{msg.message}</div>
                            {msg.translation && (
                              <div className="text-xs text-gray-400 mt-1 italic">{msg.translation}</div>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>

                    {/* Key Phrases */}
                    {scenario.key_phrases?.length > 0 && (
                      <div>
                        <div className="text-xs font-semibold text-gray-400 uppercase mb-2">Anahtar İfadeler</div>
                        <div className="flex flex-wrap gap-2">
                          {scenario.key_phrases.map((phrase: string, i: number) => (
                            <span key={i} className="px-2 py-1 bg-emerald-900/20 border border-emerald-500/20 text-emerald-300 rounded text-xs font-mono">
                              {phrase}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Cultural Note */}
                    {scenario.cultural_note && (
                      <div className="bg-yellow-900/10 border border-yellow-500/20 rounded-lg p-3">
                        <div className="text-xs font-semibold text-yellow-400 mb-1">Kültür Notu</div>
                        <div className="text-sm text-yellow-200/80">{scenario.cultural_note}</div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}

          {filteredScenarios.length === 0 && (
            <p className="text-gray-400 text-sm text-center py-8">Henüz senaryo eklenmedi.</p>
          )}
        </div>
      )}
    </div>
  );
}
