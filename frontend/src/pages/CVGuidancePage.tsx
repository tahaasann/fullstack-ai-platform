import { useEffect, useState } from 'react';
import { getCvGuidance, getCoverLetterTemplates } from '../api/client';
import type { CvGuidanceProject, CareerGuide, CareerCoverLetterTemplate, CareerPerProjectGuidance } from '../types';
import MarkdownRenderer from '../components/common/MarkdownRenderer';

type TabType = 'cv' | 'github' | 'cover-letter';

export default function CVGuidancePage() {
  const [data, setData] = useState<CvGuidanceProject[]>([]);
  const [coverLetterData, setCoverLetterData] = useState<CareerGuide | null>(null);
  const [activeTab, setActiveTab] = useState<TabType>('cv');
  const [selectedRole, setSelectedRole] = useState<string>('Full Stack Developer');
  const [expandedProject, setExpandedProject] = useState<string | null>(null);

  useEffect(() => {
    getCvGuidance().then(setData).catch(console.error);
    getCoverLetterTemplates().then(setCoverLetterData).catch(() => {});
  }, []);

  const tabs: { id: TabType; label: string; icon: string }[] = [
    { id: 'cv', label: 'CV Rehberi', icon: '📄' },
    { id: 'github', label: 'GitHub Portfolyo', icon: '🐙' },
    { id: 'cover-letter', label: 'Cover Letter', icon: '✉️' },
  ];

  const roles = ['Full Stack Developer', 'AI Engineer'];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">CV & GitHub Rehberi</h1>
        <p className="text-gray-400 text-sm mt-1">
          ATS/AI tarama sistemlerinden geçen CV oluştur ve GitHub profilini optimize et
        </p>
      </div>

      {/* Tab Navigation */}
      <div className="flex gap-2 border-b border-gray-800 pb-0">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-2.5 text-sm font-medium rounded-t-lg transition-colors ${
              activeTab === tab.id
                ? 'bg-gray-900 text-white border border-gray-800 border-b-gray-900 -mb-px'
                : 'text-gray-400 hover:text-gray-300'
            }`}
          >
            {tab.icon} {tab.label}
          </button>
        ))}
      </div>

      {activeTab === 'cv' && (
        <div className="space-y-6">
          {/* ATS Checklist */}
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
            <h2 className="text-lg font-semibold text-white mb-4">ATS Geçiş Kuralları</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              {[
                'Standart bölüm başlıkları kullan (Summary, Technical Skills, Projects, Education)',
                'Her madde eylem fiili ile başlasın (Developed, Implemented, Designed, Built)',
                'Tablo, kolon, grafik KULLANMA — ATS parse edemez',
                'PDF formatı (Word değil)',
                'Standart font (Arial, Calibri, Helvetica) — 10-12pt',
                'Header/footer\'a kritik bilgi KOYMA',
                'Tek sayfa (senior değilsen)',
                'Teknoloji isimlerini TAM yaz: React.js, Node.js, PostgreSQL',
                'İş ilanındaki AYNI kelimeleri kullan (synonym değil)',
                'Tarihler tutarlı format: 2025 – 2026',
              ].map((rule, i) => (
                <div key={i} className="flex items-start gap-2 text-sm text-gray-300">
                  <span className="text-green-400 shrink-0 mt-0.5">✅</span>
                  <span>{rule}</span>
                </div>
              ))}
            </div>
          </div>

          {/* CV Template */}
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
            <h2 className="text-lg font-semibold text-white mb-4">ATS-Optimized CV Şablonu</h2>
            <pre className="bg-gray-950 text-gray-300 text-xs p-4 rounded-lg overflow-x-auto whitespace-pre-wrap leading-relaxed font-mono">
{`AD SOYAD
Sehir, Ulke | email@email.com | linkedin.com/in/xxx | github.com/xxx

SUMMARY
[2-3 cumle: rol + ana teknolojiler + one cikan basari]

TECHNICAL SKILLS
Languages: Python, JavaScript, TypeScript, SQL
Frontend: React.js, Next.js, Tailwind CSS, Vite
Backend: FastAPI, Node.js, Express.js
Databases: PostgreSQL, MongoDB, Redis
AI/ML: LangChain, OpenAI API, scikit-learn, RAG, Vector Databases
DevOps: Docker, GitHub Actions, CI/CD
Tools: Git, pnpm, uv, VS Code, Postman

PROJECTS
[Project Title] | [Tech Stack] | 2025 – 2026 | GitHub: link | Demo: link
• [Action verb] + [Technology] + [Measurable impact]
• [Action verb] + [Technology] + [Measurable impact]

(10 projeden en alakali 4-5 tanesi, is ilanina gore sirala)

EDUCATION
B.S. Computer Engineering — Karadeniz Technical University (KTU)`}
            </pre>
          </div>

          {/* Role Selector */}
          <div className="flex items-center gap-3">
            <span className="text-sm text-gray-400">Hedef Rol:</span>
            {roles.map((role) => (
              <button
                key={role}
                onClick={() => setSelectedRole(role)}
                className={`px-3 py-1.5 rounded-lg text-sm transition-colors ${
                  selectedRole === role
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
                }`}
              >
                {role}
              </button>
            ))}
          </div>

          {/* Per-Project CV Bullets */}
          <div className="space-y-3">
            {data.filter(p => p.cv_guidance).map((p) => (
              <div key={p.project_id} className="bg-gray-900 border border-gray-800 rounded-xl p-4">
                <button
                  onClick={() => setExpandedProject(expandedProject === p.project_id ? null : p.project_id)}
                  className="w-full text-left flex items-center justify-between"
                >
                  <div>
                    <div className="text-sm font-semibold text-white">{p.project_title}</div>
                    <div className="text-xs text-blue-400 mt-0.5">{p.cv_guidance.project_title_for_cv}</div>
                  </div>
                  <span className="text-gray-400 text-lg">{expandedProject === p.project_id ? '−' : '+'}</span>
                </button>

                {expandedProject === p.project_id && (
                  <div className="mt-4 space-y-4">
                    {/* Bullet Points for Selected Role */}
                    {p.cv_guidance.bullet_points?.[selectedRole] && (
                      <div>
                        <div className="text-xs font-semibold text-emerald-400 uppercase mb-2">
                          {selectedRole} — CV Maddeleri
                        </div>
                        <div className="space-y-2">
                          {p.cv_guidance.bullet_points[selectedRole].map((bp: string, i: number) => (
                            <div key={i} className="bg-gray-950 rounded-lg p-3 flex items-start gap-2">
                              <span className="text-emerald-400 shrink-0 mt-0.5">•</span>
                              <span className="text-sm text-gray-200 font-mono leading-relaxed">{bp}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* ATS Keywords */}
                    {p.cv_guidance.ats_keywords?.length > 0 && (
                      <div>
                        <div className="text-xs font-semibold text-gray-400 uppercase mb-2">ATS Anahtar Kelimeler</div>
                        <div className="flex flex-wrap gap-1.5">
                          {p.cv_guidance.ats_keywords.map((kw: string, i: number) => (
                            <span key={i} className="px-2 py-0.5 bg-blue-900/30 text-blue-400 rounded text-xs">{kw}</span>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Metrics */}
                    {p.cv_guidance.metrics_you_can_claim?.length > 0 && (
                      <div>
                        <div className="text-xs font-semibold text-gray-400 uppercase mb-2">Metrikler</div>
                        <div className="space-y-1">
                          {p.cv_guidance.metrics_you_can_claim.map((m: string, i: number) => (
                            <div key={i} className="text-sm text-yellow-300 flex items-start gap-2">
                              <span className="shrink-0">📊</span> {m}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Placement Advice */}
                    {p.cv_guidance.cv_placement && (
                      <div className="bg-yellow-900/10 border border-yellow-500/20 rounded-lg p-3">
                        <div className="text-xs font-semibold text-yellow-400 mb-1">Yerlestirme Tavsiyesi</div>
                        <div className="text-sm text-gray-300">{p.cv_guidance.cv_placement}</div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {activeTab === 'github' && (
        <div className="space-y-6">
          {/* Profile Setup Guide */}
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
            <h2 className="text-lg font-semibold text-white mb-4">GitHub Profil Kurulumu</h2>
            <div className="space-y-3">
              <div>
                <div className="text-xs font-semibold text-gray-400 uppercase mb-1">Bio Şablonu</div>
                <code className="text-sm text-green-400 bg-gray-950 px-3 py-1.5 rounded block">
                  Full Stack Developer & AI Engineer | React, TypeScript, Python, FastAPI | Building intelligent applications
                </code>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-4">
                {[
                  'Iki hedef rolu de yaz: Full Stack Developer & AI Engineer',
                  'En guclu 4-5 teknolojini listele',
                  'Portfolio siteni website alanina ekle',
                  'Profile README ile profilini ozellestir (username/username repo)',
                ].map((tip, i) => (
                  <div key={i} className="text-sm text-gray-300 flex items-start gap-2">
                    <span className="text-blue-400 shrink-0">💡</span> {tip}
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Pinned Repos Strategy */}
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
            <h2 className="text-lg font-semibold text-white mb-4">Pinli Repo Stratejisi</h2>
            <p className="text-sm text-gray-400 mb-4">GitHub profilinde 6 repo pinleyebilirsin. En etkileyici projeleri pinle.</p>
            <div className="space-y-2">
              {data
                .filter(p => p.github_guidance?.pin_on_profile)
                .sort((a, b) => (a.github_guidance?.pin_priority || 99) - (b.github_guidance?.pin_priority || 99))
                .map((p) => (
                  <div key={p.project_id} className="flex items-center gap-3 bg-gray-950 rounded-lg px-3 py-2">
                    <span className="text-yellow-400 font-bold text-sm w-6">#{p.github_guidance.pin_priority}</span>
                    <code className="text-sm text-green-400">{p.github_guidance.repo_name}</code>
                    <span className="text-xs text-gray-400 flex-1 truncate">{p.project_title}</span>
                  </div>
                ))}
            </div>
            <div className="mt-4 space-y-2">
              <div className="text-xs font-semibold text-gray-400 uppercase mb-2">Pozisyona Gore Pinleme</div>
              <div className="text-sm text-gray-300">🎯 <strong>AI Engineer:</strong> Proje 9, 10, 7, 8 pinle</div>
              <div className="text-sm text-gray-300">🎯 <strong>Full Stack:</strong> Proje 10, 5, 2, 1 pinle</div>
              <div className="text-sm text-gray-300">🎯 <strong>Her ikisi:</strong> Proje 10, 9, 7, 5, 8, 1 pinle</div>
            </div>
          </div>

          {/* Per-Project GitHub Guide */}
          <div className="space-y-3">
            <h2 className="text-lg font-semibold text-white">Proje Repo Rehberleri</h2>
            {data.filter(p => p.github_guidance).map((p) => (
              <div key={p.project_id} className="bg-gray-900 border border-gray-800 rounded-xl p-4">
                <button
                  onClick={() => setExpandedProject(expandedProject === `gh-${p.project_id}` ? null : `gh-${p.project_id}`)}
                  className="w-full text-left flex items-center justify-between"
                >
                  <div className="flex items-center gap-3">
                    <code className="text-sm text-green-400 bg-gray-950 px-2 py-0.5 rounded">{p.github_guidance.repo_name}</code>
                    <span className="text-sm text-gray-400">{p.project_title}</span>
                    {p.github_guidance.pin_on_profile && <span className="text-yellow-400 text-xs">⭐ Pin</span>}
                  </div>
                  <span className="text-gray-400 text-lg">{expandedProject === `gh-${p.project_id}` ? '−' : '+'}</span>
                </button>

                {expandedProject === `gh-${p.project_id}` && (
                  <div className="mt-4 space-y-4">
                    {p.github_guidance.repo_description && (
                      <div>
                        <div className="text-xs font-semibold text-gray-400 uppercase mb-1">Repo Açıklaması</div>
                        <div className="text-sm text-gray-300 italic">{p.github_guidance.repo_description}</div>
                      </div>
                    )}

                    {p.github_guidance.topics?.length > 0 && (
                      <div>
                        <div className="text-xs font-semibold text-gray-400 uppercase mb-2">Topics</div>
                        <div className="flex flex-wrap gap-1.5">
                          {p.github_guidance.topics.map((t: string, i: number) => (
                            <span key={i} className="px-2 py-0.5 bg-gray-800 text-gray-400 rounded text-xs">{t}</span>
                          ))}
                        </div>
                      </div>
                    )}

                    {p.github_guidance.readme_sections?.length > 0 && (
                      <div>
                        <div className="text-xs font-semibold text-gray-400 uppercase mb-2">README Bölümleri</div>
                        <div className="space-y-1">
                          {p.github_guidance.readme_sections.map((s: string, i: number) => (
                            <div key={i} className="text-sm text-gray-300 flex items-start gap-2">
                              <span className="text-blue-400 shrink-0">{i + 1}.</span> {s}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {p.github_guidance.commit_examples?.length > 0 && (
                      <div>
                        <div className="text-xs font-semibold text-gray-400 uppercase mb-2">Örnek Commit Mesajları</div>
                        <div className="space-y-1">
                          {p.github_guidance.commit_examples.map((c: string, i: number) => (
                            <code key={i} className="block text-xs text-gray-300 bg-gray-950 px-2 py-1 rounded">{c}</code>
                          ))}
                        </div>
                      </div>
                    )}

                    {p.github_guidance.when_to_create && (
                      <div className="bg-blue-900/10 border border-blue-500/20 rounded-lg p-3">
                        <div className="text-xs font-semibold text-blue-400 mb-1">Ne Zaman Oluştur?</div>
                        <div className="text-sm text-gray-300">{p.github_guidance.when_to_create}</div>
                      </div>
                    )}

                    {p.github_guidance.pro_tips?.length > 0 && (
                      <div>
                        <div className="text-xs font-semibold text-gray-400 uppercase mb-2">Pro Tips</div>
                        <div className="space-y-1">
                          {p.github_guidance.pro_tips.map((tip: string, i: number) => (
                            <div key={i} className="text-sm text-gray-300 flex items-start gap-2">
                              <span className="text-yellow-400 shrink-0">💡</span> {tip}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    <div className="bg-gray-950 rounded-lg p-3">
                      <div className="text-xs text-gray-400">
                        <strong>Branch Strategy:</strong> {p.github_guidance.branch_strategy}
                      </div>
                      <div className="text-xs text-gray-400 mt-1">
                        <strong>Commit Convention:</strong> {p.github_guidance.commit_convention}
                      </div>
                      <div className="text-xs text-gray-400 mt-1">
                        <strong>Günlük Hedef:</strong> {p.github_guidance.daily_commit_target}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Contribution Graph Tips */}
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
            <h2 className="text-lg font-semibold text-white mb-4">Contribution Graph Stratejisi</h2>
            <p className="text-sm text-gray-400 mb-3">Yeşil contribution graph, tutarlılığını ve aktifliğini gösterir. Recruiter'lar buna bakar.</p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              {[
                'Günde en az 3-5 anlamlı commit at',
                'Boş commit atma — anlamlı değişiklikler yap',
                'Hafta sonları da commit at — tutarlılık gösterir',
                'Sadece kod değil: docs, tests, refactoring de commit sayılır',
                'GitHub Actions workflow\'ları da contribution olarak sayılır',
                'Her milestone bittiğinde git tag ekle: v0.1.0, v0.2.0...',
              ].map((tip, i) => (
                <div key={i} className="text-sm text-gray-300 flex items-start gap-2">
                  <span className="text-green-400 shrink-0">✅</span> {tip}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {activeTab === 'cover-letter' && (
        <div className="space-y-6">
          {/* General Tips */}
          {coverLetterData?.general_tips && coverLetterData.general_tips.length > 0 && (
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
              <h2 className="text-lg font-semibold text-white mb-4">Cover Letter Yazım Kuralları</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                {coverLetterData.general_tips.map((tip: string, i: number) => (
                  <div key={i} className="flex items-start gap-2 text-sm text-gray-300">
                    <span className="text-green-400 shrink-0 mt-0.5">✅</span>
                    <span>{tip}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Templates */}
          {coverLetterData?.templates && coverLetterData.templates.length > 0 && (
            <div className="space-y-3">
              <h2 className="text-lg font-semibold text-white">Şablonlar</h2>
              {coverLetterData.templates.map((tmpl: CareerCoverLetterTemplate, i: number) => (
                <div key={i} className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
                  <button
                    onClick={() => setExpandedProject(expandedProject === `cl-${i}` ? null : `cl-${i}`)}
                    className="w-full flex items-center justify-between p-5 text-left hover:bg-gray-800/50 transition-colors"
                  >
                    <div className="flex items-center gap-3">
                      <span className="text-sm font-semibold text-white">{tmpl.role}</span>
                      <span className="text-xs px-2 py-0.5 bg-gray-800 text-gray-400 rounded">{tmpl.language?.toUpperCase()}</span>
                      <span className="text-xs text-gray-400">{tmpl.tone}</span>
                    </div>
                    <span className="text-gray-400 text-lg">{expandedProject === `cl-${i}` ? '−' : '+'}</span>
                  </button>
                  {expandedProject === `cl-${i}` && (
                    <div className="px-5 pb-5 border-t border-gray-800 pt-4 space-y-3">
                      {tmpl.template && (
                        <div className="space-y-2">
                          {Object.entries(tmpl.template).map(([key, val]) => (
                            <div key={key}>
                              <div className="text-xs font-semibold text-gray-400 uppercase mb-1">{key.replace(/_/g, ' ')}</div>
                              <div className="bg-gray-950 rounded-lg p-3"><MarkdownRenderer content={val} className="text-sm" /></div>
                            </div>
                          ))}
                        </div>
                      )}
                      {tmpl.example && (
                        <div>
                          <div className="text-xs font-semibold text-emerald-400 uppercase mb-2">Ornek Cover Letter</div>
                          <div className="bg-emerald-900/10 border border-emerald-500/20 rounded-lg p-4">
                            <MarkdownRenderer content={tmpl.example} className="text-sm" />
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}

          {/* Per-Project Cover Letter Guidance */}
          {coverLetterData?.per_project_guidance && coverLetterData.per_project_guidance.length > 0 && (
            <div className="space-y-3">
              <h2 className="text-lg font-semibold text-white">Proje Bazlı Cover Letter İpuçları</h2>
              {coverLetterData.per_project_guidance.map((pg: CareerPerProjectGuidance, i: number) => (
                <div key={i} className="bg-gray-900 border border-gray-800 rounded-xl p-4">
                  <div className="text-sm font-semibold text-white mb-2">{pg.project_title}</div>
                  {pg.highlight_for_cover_letter && (
                    <p className="text-sm text-gray-400 mb-2">{pg.highlight_for_cover_letter}</p>
                  )}
                  {pg.skills_to_emphasize && pg.skills_to_emphasize.length > 0 && (
                    <div className="flex flex-wrap gap-1.5 mb-2">
                      {pg.skills_to_emphasize.map((s: string, j: number) => (
                        <span key={j} className="px-2 py-0.5 bg-blue-900/30 text-blue-400 rounded text-xs">{s}</span>
                      ))}
                    </div>
                  )}
                  {pg.talking_points && pg.talking_points.length > 0 && (
                    <ul className="space-y-1">
                      {pg.talking_points.map((tp: string, j: number) => (
                        <li key={j} className="text-sm text-gray-300 flex items-start gap-2">
                          <span className="text-yellow-400 shrink-0">•</span> {tp}
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              ))}
            </div>
          )}

          {!coverLetterData && (
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-8 text-center text-gray-400">
              Cover letter şablonları yükleniyor...
            </div>
          )}
        </div>
      )}
    </div>
  );
}
