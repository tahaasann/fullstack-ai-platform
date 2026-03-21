import { useEffect, useState, useRef, memo } from 'react';
import { useParams, Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import { startLesson, updateLessonTime } from '../api/client';
import { useLesson } from '../hooks/useLesson';
import type { Section } from '../types';
import ConceptCard from '../components/lesson/ConceptCard';
import ComparisonTable from '../components/lesson/ComparisonTable';
import CodeBlock from '../components/lesson/CodeBlock';
import InfoBox from '../components/lesson/InfoBox';
import KnowledgeCheck from '../components/lesson/KnowledgeCheck';
import EnglishSection from '../components/english/EnglishSection';
import MustNote from '../components/lesson/MustNote';
import SeniorLearns from '../components/lesson/SeniorLearns';
import AIGuidance from '../components/lesson/AIGuidance';
import ArchitectureDiagram from '../components/lesson/ArchitectureDiagram';
import BookmarkButton from '../components/common/BookmarkButton';
import MarkdownRenderer from '../components/common/MarkdownRenderer';

export default function LessonPage() {
  const { lessonId } = useParams();
  const { lesson, isLoading, completeMutation } = useLesson(lessonId || '');
  const [completed, setCompleted] = useState(false);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const secondsRef = useRef(0);

  // Sync completed state from fetched lesson data
  useEffect(() => {
    if (lesson) {
      setCompleted(lesson.status === 'completed');
    }
  }, [lesson]);

  // Start lesson tracking and time tracking
  useEffect(() => {
    if (!lessonId) return;
    startLesson(lessonId).catch(() => {});

    secondsRef.current = 0;
    timerRef.current = setInterval(() => {
      secondsRef.current += 30;
      updateLessonTime(lessonId, 30).catch(() => {});
    }, 30000);

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
      if (secondsRef.current > 0) {
        updateLessonTime(lessonId, secondsRef.current % 30).catch(() => {});
      }
    };
  }, [lessonId]);

  const handleComplete = async () => {
    if (!lessonId) return;
    try {
      await completeMutation.mutateAsync();
      setCompleted(true);
      toast.success('Ders tamamlandı!');
    } catch (err) {
      toast.error('Ders tamamlanamadı. Tekrar deneyin.');
    }
  };

  if (isLoading || !lesson) return <div className="text-gray-400">Yükleniyor...</div>;

  return (
    <div className="space-y-6">
      {/* Navigation */}
      <div className="flex items-center justify-between mb-6">
        <Link to={`/module/${lesson.module_id}`} className="text-sm text-blue-400 hover:underline">
          ← Modüle Dön
        </Link>
        <div className="flex items-center gap-3">
          {lesson.prev_lesson_id && (
            <Link to={`/lesson/${encodeURIComponent(lesson.prev_lesson_id)}`} className="text-sm text-gray-400 hover:text-white">
              ← Önceki Ders
            </Link>
          )}
          {lesson.next_lesson_id && (
            <Link to={`/lesson/${encodeURIComponent(lesson.next_lesson_id)}`} className="text-sm text-gray-400 hover:text-white">
              Sonraki Ders →
            </Link>
          )}
        </div>
      </div>

      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-2 mb-2">
          {lesson.tags?.map((tag: string) => (
            <span key={tag} className="px-2 py-0.5 bg-gray-800 text-gray-400 rounded text-xs">{tag}</span>
          ))}
        </div>
        <div className="flex items-center gap-2">
          <h1 className="text-3xl font-bold text-white">{lesson.title}</h1>
          {lessonId && <BookmarkButton itemType="lesson" itemId={lessonId} />}
        </div>
        <div className="text-sm text-gray-400 mt-2">Tahmini süre: {lesson.estimated_minutes} dakika</div>
      </div>

      {/* Content Sections */}
      <div className="space-y-6">
        {(lesson.sections || []).map((section: Section, i: number) => (
          <LessonSection key={i} section={section} />
        ))}
      </div>

      {/* Complete Button */}
      <div className="mt-12 mb-8 flex items-center justify-center gap-4">
        {!completed ? (
          <button
            onClick={handleComplete}
            className="px-8 py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium transition-colors"
          >
            Dersi Tamamla ✓
          </button>
        ) : (
          <div className="flex items-center gap-2 text-green-400">
            <span className="text-xl">✓</span>
            <span className="font-medium">Ders tamamlandı!</span>
          </div>
        )}
        {lesson.next_lesson_id && (
          <Link
            to={`/lesson/${encodeURIComponent(lesson.next_lesson_id)}`}
            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
          >
            Sonraki Ders →
          </Link>
        )}
      </div>
    </div>
  );
}

const LessonSection = memo(function LessonSection({ section }: { section: Section }) {
  switch (section.type) {
    case 'text':
      return <MarkdownRenderer content={section.content} />;
    case 'concept':
      return <ConceptCard concept={section} />;
    case 'comparison':
      return <ComparisonTable comparison={section} />;
    case 'code':
      return <CodeBlock code={section} />;
    case 'warning':
      return <InfoBox type="warning" title={section.title} content={section.content} />;
    case 'tip':
      return <InfoBox type="tip" title={section.title} content={section.content} />;
    case 'realworld':
      return <InfoBox type="realworld" title={section.title || 'Gerçek Dünya'} content={section.content} />;
    case 'interview':
      return <InfoBox type="interview" title={section.title || 'Mülakat Sorusu'} content={section.content} />;
    case 'deha-tip':
      return <InfoBox type="deha" title={section.title || 'Deha Seviyesi'} content={section.content} />;
    case 'beginner-mistake':
      return <InfoBox type="mistake" title={section.title || 'Yaygın Hata'} content={section.content} />;
    case 'exercise':
      return <InfoBox type="exercise" title={section.title || 'Pratik'} content={section.content} />;
    case 'knowledge-check':
      return <KnowledgeCheck data={section} />;
    case 'english':
      return <EnglishSection data={section} />;
    case 'external-resource':
      return <InfoBox type="resource" title={section.title || 'Kaynak'} content={section.content} url={section.url as string | undefined} />;
    case 'must-note':
      return <MustNote data={section} />;
    case 'senior-learns':
      return <SeniorLearns data={section} />;
    case 'ai-guidance':
      return <AIGuidance data={section} />;
    case 'architecture':
      return <ArchitectureDiagram title={section.title} content={section.content} description={section.description} />;
    default:
      return <MarkdownRenderer content={section.content || ''} />;
  }
});
