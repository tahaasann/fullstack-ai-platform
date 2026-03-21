import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import { getQuiz, submitQuiz } from '../api/client';
import type { Quiz, QuizResult, QuizQuestion } from '../types';

export default function QuizPage() {
  const { quizId } = useParams();
  const [quiz, setQuiz] = useState<Quiz | null>(null);
  const [answers, setAnswers] = useState<Record<number, string | string[]>>({});
  const [result, setResult] = useState<QuizResult | null>(null);
  const [currentQ, setCurrentQ] = useState(0);

  useEffect(() => {
    if (!quizId) return;
    getQuiz(quizId).then(setQuiz).catch(console.error);
  }, [quizId]);

  const handleAnswer = (qIdx: number, value: string | string[]) => {
    setAnswers((prev) => ({ ...prev, [qIdx]: value }));
  };

  const handleSubmit = async () => {
    if (!quizId || !quiz) return;
    try {
      const formattedAnswers = quiz.questions.map((_: QuizQuestion, i: number) => ({
        question_index: i,
        answer: answers[i] ?? null,
      }));
      const res = await submitQuiz(quizId, formattedAnswers, 0);
      setResult(res);
    } catch (err) {
      toast.error('Quiz gönderilemedi. Tekrar deneyin.');
    }
  };

  if (!quiz) return <div className="text-gray-400">Yükleniyor...</div>;

  if (result) {
    return <QuizResultView quiz={quiz} result={result} answers={answers} />;
  }

  const q = quiz.questions[currentQ];
  const total = quiz.questions.length;

  return (
    <div className="max-w-3xl mx-auto">
      <div className="mb-6">
        <Link to={`/module/${(quiz as Quiz & { module_id?: string }).module_id}`} className="text-sm text-blue-400 hover:underline">← Modüle Dön</Link>
        <h1 className="text-2xl font-bold text-white mt-2">{quiz.title}</h1>
        <p className="text-gray-400 text-sm mt-1">{quiz.description}</p>
      </div>

      {/* Progress */}
      <div className="flex items-center gap-2 mb-6">
        {quiz.questions.map((_: QuizQuestion, i: number) => (
          <div
            key={i}
            className={`h-2 flex-1 rounded-full transition-colors ${
              answers[i] !== undefined ? 'bg-blue-500' :
              i === currentQ ? 'bg-blue-500/50' : 'bg-gray-800'
            }`}
          />
        ))}
      </div>

      {/* Question */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
        <div className="flex items-center justify-between mb-4">
          <span className="text-sm text-gray-400">Soru {currentQ + 1} / {total}</span>
          <span className="text-xs px-2 py-1 bg-gray-800 text-gray-400 rounded">{q.type}</span>
        </div>

        <h2 className="text-lg text-white font-medium mb-6">{q.question}</h2>

        <QuestionInput question={q} index={currentQ} value={answers[currentQ]} onChange={handleAnswer} />
      </div>

      {/* Navigation */}
      <div className="flex items-center justify-between mt-6">
        <button
          onClick={() => setCurrentQ(Math.max(0, currentQ - 1))}
          disabled={currentQ === 0}
          className="px-4 py-2 text-sm text-gray-400 hover:text-white disabled:opacity-30 transition-colors focus:ring-2 focus:ring-blue-500 focus:outline-none rounded-lg"
        >
          ← Önceki
        </button>
        {currentQ < total - 1 ? (
          <button
            onClick={() => setCurrentQ(currentQ + 1)}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm transition-colors focus:ring-2 focus:ring-blue-500 focus:outline-none"
          >
            Sonraki →
          </button>
        ) : (
          <button
            onClick={handleSubmit}
            disabled={Object.keys(answers).length < total}
            className="px-6 py-2 bg-green-600 hover:bg-green-700 disabled:opacity-50 text-white rounded-lg text-sm font-medium transition-colors focus:ring-2 focus:ring-blue-500 focus:outline-none"
          >
            Teslim Et
          </button>
        )}
      </div>
    </div>
  );
}

function QuestionInput({ question, index, value, onChange }: {
  question: QuizQuestion; index: number; value: string | string[] | undefined; onChange: (i: number, v: string | string[]) => void;
}) {
  switch (question.type) {
    case 'multiple_choice':
      return (
        <div className="space-y-3">
          {question.options?.map((opt: string, i: number) => {
            const letter = String.fromCharCode(65 + i);
            return (
              <button
                key={i}
                onClick={() => onChange(index, letter)}
                className={`w-full text-left p-4 rounded-lg border transition-colors focus:ring-2 focus:ring-blue-500 focus:outline-none ${
                  value === letter ? 'border-blue-500 bg-blue-900/20' : 'border-gray-700 hover:border-gray-600'
                }`}
              >
                <span className="font-mono text-gray-400 mr-3">{letter}.</span>
                <span className="text-gray-300">{opt}</span>
              </button>
            );
          })}
        </div>
      );

    case 'true_false':
      return (
        <div className="flex gap-4">
          {['true', 'false'].map((v) => (
            <button
              key={v}
              onClick={() => onChange(index, v)}
              className={`flex-1 p-4 rounded-lg border text-center font-medium transition-colors focus:ring-2 focus:ring-blue-500 focus:outline-none ${
                value === v ? 'border-blue-500 bg-blue-900/20 text-blue-400' : 'border-gray-700 hover:border-gray-600 text-gray-400'
              }`}
            >
              {v === 'true' ? 'Doğru' : 'Yanlış'}
            </button>
          ))}
        </div>
      );

    case 'code_completion':
      return (
        <div>
          {(question as QuizQuestion & { code_context?: string }).code_context && (
            <pre className="bg-gray-950 border border-gray-800 rounded-lg p-4 mb-4 text-sm font-mono text-gray-300 overflow-x-auto">
              {(question as QuizQuestion & { code_context?: string }).code_context}
            </pre>
          )}
          <input
            type="text"
            value={(value as string) || ''}
            onChange={(e) => onChange(index, e.target.value)}
            placeholder="Cevabınızı yazın..."
            className="w-full bg-gray-950 border border-gray-700 rounded-lg p-3 text-gray-300 font-mono focus:border-blue-500 focus:outline-none"
          />
        </div>
      );

    case 'explain_code':
      return (
        <div>
          {(question as QuizQuestion & { code_context?: string }).code_context && (
            <pre className="bg-gray-950 border border-gray-800 rounded-lg p-4 mb-4 text-sm font-mono text-gray-300 overflow-x-auto">
              {(question as QuizQuestion & { code_context?: string }).code_context}
            </pre>
          )}
          <textarea
            value={(value as string) || ''}
            onChange={(e) => onChange(index, e.target.value)}
            placeholder="Açıklamanızı yazın..."
            rows={4}
            className="w-full bg-gray-950 border border-gray-700 rounded-lg p-3 text-gray-300 focus:border-blue-500 focus:outline-none resize-y"
          />
        </div>
      );

    case 'order_steps':
      return <OrderSteps items={(question as QuizQuestion & { items?: string[] }).items || []} value={value as string[] | undefined} onChange={(v: string[]) => onChange(index, v)} />;

    default:
      return <p className="text-gray-400">Bilinmeyen soru tipi: {question.type}</p>;
  }
}

function OrderSteps({ items, value, onChange }: { items: string[]; value: string[] | undefined; onChange: (v: string[]) => void }) {
  const [order, setOrder] = useState<string[]>(value || [...items].sort(() => Math.random() - 0.5));

  const moveUp = (i: number) => {
    if (i === 0) return;
    const newOrder = [...order];
    [newOrder[i - 1], newOrder[i]] = [newOrder[i], newOrder[i - 1]];
    setOrder(newOrder);
    onChange(newOrder);
  };

  const moveDown = (i: number) => {
    if (i === order.length - 1) return;
    const newOrder = [...order];
    [newOrder[i], newOrder[i + 1]] = [newOrder[i + 1], newOrder[i]];
    setOrder(newOrder);
    onChange(newOrder);
  };

  return (
    <div className="space-y-2">
      <p className="text-sm text-gray-400 mb-3">Adımları doğru sıraya koyun (yukarı/aşağı butonlarını kullanın):</p>
      {order.map((item, i) => (
        <div key={item} className="flex items-center gap-3 p-3 bg-gray-800/50 rounded-lg border border-gray-700">
          <span className="text-gray-400 font-mono text-sm w-6">{i + 1}.</span>
          <span className="flex-1 text-gray-300 text-sm">{item}</span>
          <div className="flex flex-col gap-1">
            <button onClick={() => moveUp(i)} className="text-gray-400 hover:text-white text-xs px-1 focus:ring-2 focus:ring-blue-500 focus:outline-none rounded" aria-label={`${i + 1}. adımı yukarı taşı`}>▲</button>
            <button onClick={() => moveDown(i)} className="text-gray-400 hover:text-white text-xs px-1 focus:ring-2 focus:ring-blue-500 focus:outline-none rounded" aria-label={`${i + 1}. adımı aşağı taşı`}>▼</button>
          </div>
        </div>
      ))}
    </div>
  );
}

interface QuizResultDetail {
  correct: boolean;
  correct_answer?: string;
  explanation?: string;
}

function QuizResultView({ quiz, result, answers }: { quiz: Quiz; result: QuizResult; answers: Record<number, string | string[]> }) {
  const resultWithDetails = result as QuizResult & { details?: QuizResultDetail[]; total_questions?: number };
  return (
    <div className="max-w-3xl mx-auto">
      <div className="text-center mb-8">
        <div className={`text-6xl font-bold mb-4 ${result.passed ? 'text-green-400' : 'text-red-400'}`}>
          %{result.score}
        </div>
        <h2 className="text-2xl font-bold text-white">
          {result.passed ? 'Tebrikler! Quiz\'i geçtiniz!' : 'Quiz\'i geçemediniz.'}
        </h2>
        <p className="text-gray-400 mt-2">
          {result.correct_count} / {resultWithDetails.total_questions ?? result.results?.length ?? 0} doğru
        </p>
      </div>

      <div className="space-y-4">
        {resultWithDetails.details?.map((detail: QuizResultDetail, i: number) => (
          <div key={i} className={`p-4 rounded-xl border ${
            detail.correct ? 'border-green-500/30 bg-green-900/10' : 'border-red-500/30 bg-red-900/10'
          }`}>
            <div className="flex items-start gap-3">
              <span className="text-lg mt-0.5">{detail.correct ? '✓' : '✗'}</span>
              <div className="flex-1">
                <p className="text-gray-200 font-medium">{quiz.questions[i]?.question}</p>
                <div className="mt-2 text-sm">
                  <p className="text-gray-400">Sizin cevabınız: <span className="text-gray-300">{String(answers[i])}</span></p>
                  {!detail.correct && detail.correct_answer && (
                    <p className="text-green-400 mt-1">Doğru cevap: {detail.correct_answer}</p>
                  )}
                  {detail.explanation && (
                    <p className="text-gray-400 mt-2">{detail.explanation}</p>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="flex justify-center gap-4 mt-8">
        <Link
          to={`/module/${(quiz as Quiz & { module_id?: string }).module_id}`}
          className="px-6 py-2 bg-gray-800 hover:bg-gray-700 text-gray-300 rounded-lg text-sm transition-colors"
        >
          Modüle Dön
        </Link>
        {!result.passed && (
          <button
            onClick={() => window.location.reload()}
            className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm transition-colors"
          >
            Tekrar Dene
          </button>
        )}
      </div>
    </div>
  );
}
