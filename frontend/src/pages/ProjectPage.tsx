import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import { getProject, startProject, toggleMilestone } from '../api/client';
import type { ProjectDetail, Milestone } from '../types';
import BookmarkButton from '../components/common/BookmarkButton';
import MarkdownRenderer from '../components/common/MarkdownRenderer';

interface MilestoneDetail {
  id: string;
  estimated_hours?: number;
  overview?: string;
  concepts_covered?: string[];
  steps?: { step: number; title: string; why?: string; instructions?: string; code_snippet?: string; deep_dive?: string; checkpoint?: string }[];
  must_note?: string;
  senior_learns?: string;
}

export default function ProjectPage() {
  const { projectId } = useParams();
  const [project, setProject] = useState<ProjectDetail | null>(null);
  const [expandedMs, setExpandedMs] = useState<string | null>(null);

  const load = () => {
    if (!projectId) return;
    getProject(projectId).then(setProject).catch(console.error);
  };

  useEffect(load, [projectId]);

  const handleStart = async () => {
    if (!projectId) return;
    try {
      await startProject(projectId);
      load();
    } catch (err) {
      toast.error('Proje baslatilamadi. Tekrar deneyin.');
    }
  };

  const handleToggle = async (milestoneId: string) => {
    try {
      await toggleMilestone(milestoneId);
      load();
    } catch (err) {
      toast.error('Milestone guncellenemedi. Tekrar deneyin.');
    }
  };

  if (!project) return <div className="text-gray-400">Yukleniyor...</div>;

  const completedMs = project.milestones?.filter((ms: Milestone) => ms.completed).length || 0;
  const totalMs = project.milestones?.length || 0;
  const pct = totalMs > 0 ? Math.round((completedMs / totalMs) * 100) : 0;

  // Get detailed milestone info from milestone_details
  const getMilestoneDetail = (msId: string): MilestoneDetail | undefined => {
    return project.milestone_details?.find((md) => md.id === msId);
  };

  return (
    <div className="space-y-6">
      <Link to="/projects" className="text-sm text-blue-400 hover:underline">&larr; Projeler</Link>

      {/* Header */}
      <div>
        <div className="flex items-center gap-2 mb-2">
          {project.target_roles?.map((role: string) => (
            <span key={role} className="px-2 py-0.5 bg-purple-900/30 text-purple-400 rounded text-xs">{role}</span>
          ))}
          {project.difficulty && (
            <span className="px-2 py-0.5 bg-gray-800 text-gray-400 rounded text-xs">{project.difficulty}</span>
          )}
          {project.estimated_days && (
            <span className="px-2 py-0.5 bg-gray-800 text-gray-500 rounded text-xs">{project.estimated_days} gun</span>
          )}
        </div>
        <div className="flex items-center gap-2">
          <h1 className="text-2xl font-bold text-white">{project.title}</h1>
          {projectId && <BookmarkButton itemType="project" itemId={projectId} />}
        </div>
        <p className="text-gray-400 mt-2">{project.description}</p>

        <div className="flex flex-wrap gap-2 mt-3">
          {project.tech_stack?.map((tech: string) => (
            <span key={tech} className="px-2 py-1 bg-blue-900/20 border border-blue-500/20 text-blue-300 rounded text-xs">{tech}</span>
          ))}
        </div>

        {/* Progress */}
        <div className="mt-4 flex items-center gap-4">
          <div className="flex-1 h-2 bg-gray-800 rounded-full overflow-hidden">
            <div className="h-full bg-purple-500 rounded-full transition-all" style={{ width: `${pct}%` }} />
          </div>
          <span className="text-sm font-medium text-white">{completedMs}/{totalMs} · {pct}%</span>
        </div>

        {project.status === 'not_started' && (
          <button
            onClick={handleStart}
            className="mt-4 px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium transition-colors"
          >
            Projeye Basla
          </button>
        )}
      </div>

      {/* Brief */}
      {project.brief && (
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
          <h2 className="text-lg font-semibold text-white mb-3">Proje Briefi</h2>
          <MarkdownRenderer content={project.brief} className="text-sm" />
        </div>
      )}

      {/* What You Learn */}
      {project.what_you_learn && Object.keys(project.what_you_learn).length > 0 && (
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
          <h2 className="text-lg font-semibold text-white mb-4">Ne Ogreneceksin</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {Object.entries(project.what_you_learn).map(([category, skills]) => (
              skills?.length > 0 && (
                <div key={category}>
                  <h3 className="text-xs font-semibold text-gray-500 uppercase mb-2">
                    {category === 'technical' ? 'Teknik' :
                     category === 'architectural' ? 'Mimari' :
                     category === 'ai_specific' ? 'AI/ML' :
                     category === 'soft_skills' ? 'Soft Skills' : category}
                  </h3>
                  <div className="space-y-1">
                    {skills.map((skill: string, i: number) => (
                      <div key={i} className="text-sm text-gray-300 flex items-start gap-2">
                        <span className="text-blue-400 mt-0.5 shrink-0">·</span> {skill}
                      </div>
                    ))}
                  </div>
                </div>
              )
            ))}
          </div>
        </div>
      )}

      {/* Architecture Decisions */}
      {project.architecture?.decisions?.length > 0 && (
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
          <h2 className="text-lg font-semibold text-white mb-2">Mimari Kararlar</h2>
          {project.architecture.overview && (
            <p className="text-sm text-gray-400 mb-4">{project.architecture.overview}</p>
          )}
          {project.architecture.diagram && (
            <pre className="bg-gray-800/50 rounded-lg p-4 text-xs text-gray-300 font-mono mb-4 overflow-x-auto">
              {project.architecture.diagram}
            </pre>
          )}
          <div className="space-y-4">
            {project.architecture.decisions.map((d, i: number) => (
              <div key={i} className="border-l-2 border-purple-500/30 pl-4">
                <h3 className="text-sm font-semibold text-purple-300 mb-1">{d.decision}</h3>
                <p className="text-sm text-gray-300 mb-2">{d.reasoning}</p>
                {d.alternatives && (
                  <div className="text-xs text-gray-500 mb-1">
                    <span className="font-medium text-gray-400">Alternatifler: </span>{d.alternatives}
                  </div>
                )}
                {d.when_to_choose_alternative && (
                  <div className="text-xs text-gray-500">
                    <span className="font-medium text-gray-400">Ne zaman alternatif: </span>{d.when_to_choose_alternative}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Requirements */}
      {project.requirements && (typeof project.requirements === 'object') && (
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
          <h2 className="text-lg font-semibold text-white mb-4">Gereksinimler</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {project.requirements.functional && project.requirements.functional.length > 0 && (
              <div>
                <h3 className="text-xs font-semibold text-gray-500 uppercase mb-2">Fonksiyonel</h3>
                {project.requirements.functional.map((r: string, i: number) => (
                  <div key={i} className="text-sm text-gray-300 flex items-start gap-2 mb-1">
                    <span className="text-green-400 shrink-0">✓</span> {r}
                  </div>
                ))}
              </div>
            )}
            {project.requirements.non_functional && project.requirements.non_functional.length > 0 && (
              <div>
                <h3 className="text-xs font-semibold text-gray-500 uppercase mb-2">Non-Fonksiyonel</h3>
                {project.requirements.non_functional.map((r: string, i: number) => (
                  <div key={i} className="text-sm text-gray-300 flex items-start gap-2 mb-1">
                    <span className="text-blue-400 shrink-0">·</span> {r}
                  </div>
                ))}
              </div>
            )}
            {project.requirements.ai_requirements && project.requirements.ai_requirements.length > 0 && (
              <div>
                <h3 className="text-xs font-semibold text-gray-500 uppercase mb-2">AI Gereksinimleri</h3>
                {project.requirements.ai_requirements.map((r: string, i: number) => (
                  <div key={i} className="text-sm text-gray-300 flex items-start gap-2 mb-1">
                    <span className="text-purple-400 shrink-0">·</span> {r}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Evaluation Criteria */}
      {project.evaluation_criteria && project.evaluation_criteria.length > 0 && (
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
          <h2 className="text-lg font-semibold text-white mb-4">Degerlendirme Kriterleri</h2>
          <div className="space-y-3">
            {project.evaluation_criteria.map((c, i: number) => (
              <div key={i} className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-full bg-gray-800 flex items-center justify-center shrink-0">
                  <span className="text-sm font-bold text-white">%{c.weight}</span>
                </div>
                <div>
                  <h3 className="text-sm font-medium text-gray-200">{c.criterion}</h3>
                  <p className="text-xs text-gray-500">{c.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Milestones */}
      <div className="space-y-4">
        <h2 className="text-lg font-semibold text-white">Milestone'lar</h2>
        {project.milestones?.map((ms: Milestone, i: number) => {
          const detail = getMilestoneDetail(ms.id);
          const isExpanded = expandedMs === ms.id;
          return (
            <div key={ms.id} className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
              {/* Milestone Header */}
              <div className="p-5">
                <div className="flex items-start gap-3">
                  <button
                    onClick={() => handleToggle(ms.id)}
                    className={`w-7 h-7 rounded-full border-2 flex items-center justify-center shrink-0 mt-0.5 transition-colors ${
                      ms.completed
                        ? 'bg-green-600 border-green-600 text-white'
                        : 'border-gray-600 hover:border-gray-400'
                    }`}
                  >
                    {ms.completed ? <span className="text-xs">✓</span> : <span className="text-xs text-gray-500">{i + 1}</span>}
                  </button>
                  <div className="flex-1">
                    <h3 className={`text-sm font-semibold ${ms.completed ? 'text-gray-500' : 'text-gray-200'}`}>
                      {ms.title}
                    </h3>
                    {ms.description && <p className="text-xs text-gray-500 mt-1">{ms.description}</p>}
                    {detail?.estimated_hours && (
                      <span className="text-xs text-gray-600 mt-1 inline-block">{detail.estimated_hours} saat</span>
                    )}
                  </div>
                  {detail?.steps && detail.steps.length > 0 && (
                    <button
                      onClick={() => setExpandedMs(isExpanded ? null : ms.id)}
                      className={`text-gray-600 hover:text-gray-400 transition-transform shrink-0 ${isExpanded ? 'rotate-180' : ''}`}
                    >
                      ▼
                    </button>
                  )}
                </div>
              </div>

              {/* Expanded Detail */}
              {isExpanded && detail && (
                <div className="border-t border-gray-800 p-5 space-y-6">
                  {/* Overview */}
                  {detail.overview && (
                    <div className="text-sm text-gray-300 leading-relaxed">{detail.overview}</div>
                  )}

                  {/* Concepts */}
                  {detail.concepts_covered && detail.concepts_covered.length > 0 && (
                    <div className="flex flex-wrap gap-2">
                      {detail.concepts_covered.map((c: string, j: number) => (
                        <span key={j} className="px-2 py-0.5 bg-blue-900/20 text-blue-300 rounded text-xs">{c}</span>
                      ))}
                    </div>
                  )}

                  {/* Steps */}
                  {detail.steps?.map((step) => (
                    <div key={step.step} className="border-l-2 border-blue-500/20 pl-4 space-y-3">
                      <div>
                        <h4 className="text-sm font-semibold text-blue-300">
                          Adim {step.step}: {step.title}
                        </h4>
                        {step.why && (
                          <div className="text-xs text-yellow-300/70 mt-1 bg-yellow-900/10 border border-yellow-500/10 rounded px-3 py-2">
                            <span className="font-medium">NEDEN: </span>{step.why}
                          </div>
                        )}
                      </div>

                      {step.instructions && (
                        <MarkdownRenderer content={step.instructions} className="text-sm" />
                      )}

                      {step.code_snippet && (
                        <pre className="bg-gray-800/70 rounded-lg p-4 text-xs text-gray-300 font-mono overflow-x-auto">
                          {step.code_snippet}
                        </pre>
                      )}

                      {step.deep_dive && (
                        <div className="bg-indigo-900/10 border border-indigo-500/20 rounded-lg p-3">
                          <div className="text-xs font-semibold text-indigo-400 mb-1">Deep Dive</div>
                          <div className="text-sm text-gray-300">{step.deep_dive}</div>
                        </div>
                      )}

                      {step.checkpoint && (
                        <div className="bg-green-900/10 border border-green-500/20 rounded-lg p-3">
                          <div className="text-xs font-semibold text-green-400 mb-1">Checkpoint</div>
                          <div className="text-sm text-gray-300">{step.checkpoint}</div>
                        </div>
                      )}
                    </div>
                  ))}

                  {/* Must Note */}
                  {detail.must_note && (
                    <div className="bg-orange-900/10 border border-orange-500/20 rounded-xl p-4">
                      <MarkdownRenderer content={detail.must_note} className="text-sm text-orange-300" />
                    </div>
                  )}

                  {/* Senior Learns */}
                  {detail.senior_learns && (
                    <div className="bg-purple-900/10 border border-purple-500/20 rounded-xl p-4">
                      <MarkdownRenderer content={detail.senior_learns} className="text-sm text-purple-300" />
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Interview Prep */}
      {project.interview_prep && (project.interview_prep.questions?.length || project.interview_prep.talking_points?.length) && (
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
          <h2 className="text-lg font-semibold text-white mb-4">Mulakat Hazirlik</h2>

          {project.interview_prep.questions && project.interview_prep.questions.length > 0 && (
            <div className="mb-4">
              <h3 className="text-xs font-semibold text-gray-500 uppercase mb-2">Sorulabilecek Sorular</h3>
              <div className="space-y-2">
                {project.interview_prep.questions.map((q: string, i: number) => (
                  <div key={i} className="text-sm text-gray-300 flex items-start gap-2">
                    <span className="text-yellow-400 shrink-0">?</span> {q}
                  </div>
                ))}
              </div>
            </div>
          )}

          {project.interview_prep.talking_points && project.interview_prep.talking_points.length > 0 && (
            <div>
              <h3 className="text-xs font-semibold text-gray-500 uppercase mb-2">Konusma Noktalari</h3>
              <div className="space-y-2">
                {project.interview_prep.talking_points.map((tp: string, i: number) => (
                  <div key={i} className="text-sm text-gray-300 flex items-start gap-2">
                    <span className="text-emerald-400 shrink-0">·</span> {tp}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* CV Rehberi */}
      {project.cv_guidance && (
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
          <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            CV Rehberi
          </h2>
          <div className="mb-3">
            <div className="text-xs font-semibold text-gray-500 uppercase mb-1">ATS-Optimized Proje Başlığı</div>
            <div className="text-sm text-blue-300 font-medium">{project.cv_guidance.project_title_for_cv}</div>
          </div>

          {project.cv_guidance.bullet_points && Object.entries(project.cv_guidance.bullet_points).map(([role, bullets]) => (
            <div key={role} className="mb-4">
              <h3 className="text-xs font-semibold text-emerald-400 uppercase mb-2">{role} CV Maddeleri</h3>
              <div className="space-y-1.5">
                {bullets.map((bp: string, i: number) => (
                  <div key={i} className="text-sm text-gray-300 flex items-start gap-2">
                    <span className="text-emerald-400 shrink-0 mt-0.5">•</span>
                    <span className="font-mono text-xs leading-relaxed">{bp}</span>
                  </div>
                ))}
              </div>
            </div>
          ))}

          {project.cv_guidance.ats_keywords?.length > 0 && (
            <div className="mb-3">
              <div className="text-xs font-semibold text-gray-500 uppercase mb-2">ATS Anahtar Kelimeler</div>
              <div className="flex flex-wrap gap-1.5">
                {project.cv_guidance.ats_keywords.map((kw: string, i: number) => (
                  <span key={i} className="px-2 py-0.5 bg-blue-900/30 text-blue-400 rounded text-xs">{kw}</span>
                ))}
              </div>
            </div>
          )}

          {project.cv_guidance.metrics_you_can_claim?.length > 0 && (
            <div className="mb-3">
              <div className="text-xs font-semibold text-gray-500 uppercase mb-2">Kullanabileceğin Metrikler</div>
              <div className="space-y-1">
                {project.cv_guidance.metrics_you_can_claim.map((m: string, i: number) => (
                  <div key={i} className="text-sm text-yellow-300 flex items-start gap-2">
                    <span className="shrink-0">📊</span> {m}
                  </div>
                ))}
              </div>
            </div>
          )}

          {project.cv_guidance.cv_placement && (
            <div className="bg-yellow-900/10 border border-yellow-500/20 rounded-lg p-3 mt-3">
              <div className="text-xs font-semibold text-yellow-400 mb-1">CV Yerleştirme Tavsiyesi</div>
              <div className="text-sm text-gray-300">{project.cv_guidance.cv_placement}</div>
            </div>
          )}
        </div>
      )}

      {/* GitHub Rehberi */}
      {project.github_guidance && (
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
          <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            GitHub Rehberi
          </h2>

          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <div className="text-xs font-semibold text-gray-500 uppercase mb-1">Repo Adı</div>
              <code className="text-sm text-green-400 bg-gray-800 px-2 py-1 rounded">{project.github_guidance.repo_name}</code>
            </div>
            {project.github_guidance.pin_on_profile && (
              <div>
                <div className="text-xs font-semibold text-gray-500 uppercase mb-1">Profilde Pinle</div>
                <span className="text-sm text-yellow-400">Evet (Öncelik: {project.github_guidance.pin_priority})</span>
              </div>
            )}
          </div>

          {project.github_guidance.repo_description && (
            <div className="mb-3">
              <div className="text-xs font-semibold text-gray-500 uppercase mb-1">Repo Açıklaması</div>
              <div className="text-sm text-gray-300 italic">{project.github_guidance.repo_description}</div>
            </div>
          )}

          {project.github_guidance.topics && project.github_guidance.topics.length > 0 && (
            <div className="mb-3">
              <div className="text-xs font-semibold text-gray-500 uppercase mb-2">Topics</div>
              <div className="flex flex-wrap gap-1.5">
                {project.github_guidance.topics.map((t: string, i: number) => (
                  <span key={i} className="px-2 py-0.5 bg-gray-800 text-gray-400 rounded text-xs">{t}</span>
                ))}
              </div>
            </div>
          )}

          {project.github_guidance.commit_examples && project.github_guidance.commit_examples.length > 0 && (
            <div className="mb-3">
              <div className="text-xs font-semibold text-gray-500 uppercase mb-2">Örnek Commit Mesajları</div>
              <div className="space-y-1">
                {project.github_guidance.commit_examples.map((c: string, i: number) => (
                  <code key={i} className="block text-xs text-gray-300 bg-gray-800 px-2 py-1 rounded">{c}</code>
                ))}
              </div>
            </div>
          )}

          {project.github_guidance.when_to_create && (
            <div className="bg-blue-900/10 border border-blue-500/20 rounded-lg p-3 mt-3">
              <div className="text-xs font-semibold text-blue-400 mb-1">Ne Zaman Oluştur?</div>
              <div className="text-sm text-gray-300">{project.github_guidance.when_to_create}</div>
            </div>
          )}

          {project.github_guidance.pro_tips && project.github_guidance.pro_tips.length > 0 && (
            <div className="mt-3">
              <div className="text-xs font-semibold text-gray-500 uppercase mb-2">Pro Tips</div>
              <div className="space-y-1">
                {project.github_guidance.pro_tips.map((tip: string, i: number) => (
                  <div key={i} className="text-sm text-gray-300 flex items-start gap-2">
                    <span className="text-yellow-400 shrink-0">💡</span> {tip}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Resources */}
      {project.resources?.length > 0 && (
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
          <h2 className="text-lg font-semibold text-white mb-3">Kaynaklar</h2>
          <div className="space-y-3">
            {project.resources.map((res, i: number) => (
              <div key={i} className="flex items-start gap-3">
                <span className="text-blue-400 mt-0.5 shrink-0">🔗</span>
                <div>
                  <a
                    href={res.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-blue-400 hover:underline"
                  >
                    {res.title || res.url}
                  </a>
                  {res.why && <p className="text-xs text-gray-500 mt-0.5">{res.why}</p>}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
