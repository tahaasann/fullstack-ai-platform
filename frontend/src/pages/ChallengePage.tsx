import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getChallenge, runChallenge, submitChallenge, getChallengeHints, getChallengeSolution } from '../api/client';
import type { ChallengeDetail, ChallengeRunResult, TestResult } from '../types';
import Editor from '@monaco-editor/react';
import BookmarkButton from '../components/common/BookmarkButton';

interface ChallengeTestCase {
  input: unknown;
  expected: unknown;
  visible?: boolean;
}

export default function ChallengePage() {
  const { challengeId } = useParams();
  const [challenge, setChallenge] = useState<ChallengeDetail | null>(null);
  const [language, setLanguage] = useState<'python' | 'javascript'>('python');
  const [code, setCode] = useState('');
  const [output, setOutput] = useState<ChallengeRunResult | null>(null);
  const [running, setRunning] = useState(false);
  const [hints, setHints] = useState<string[]>([]);
  const [hintsRevealed, setHintsRevealed] = useState(0);
  const [solution, setSolution] = useState<{ solution: string; explanation: string } | null>(null);
  const [submitted, setSubmitted] = useState(false);

  useEffect(() => {
    if (!challengeId) return;
    getChallenge(challengeId).then((data) => {
      setChallenge(data);
      setCode(data.starter_code?.python || data.starter_code?.javascript || '');
      setLanguage(data.starter_code?.python ? 'python' : 'javascript');
    }).catch(console.error);
  }, [challengeId]);

  const switchLang = (lang: 'python' | 'javascript') => {
    setLanguage(lang);
    setCode(challenge?.starter_code?.[lang] || '');
    setOutput(null);
  };

  const handleRun = async () => {
    if (!challengeId) return;
    setRunning(true);
    try {
      const res = await runChallenge(challengeId, code, language);
      setOutput(res);
    } catch {
      setOutput({ error: 'Çalıştırma hatası', status: 'error', tests_passed: 0, tests_total: 0, results: [], execution_time_ms: 0 });
    }
    setRunning(false);
  };

  const handleSubmit = async () => {
    if (!challengeId) return;
    setRunning(true);
    try {
      const res = await submitChallenge(challengeId, code, language);
      setOutput(res);
      setSubmitted(true);
    } catch {
      setOutput({ error: 'Gönderim hatası', status: 'error', tests_passed: 0, tests_total: 0, results: [], execution_time_ms: 0 });
    }
    setRunning(false);
  };

  const revealHint = async () => {
    if (!challengeId) return;
    if (hints.length === 0) {
      const data = await getChallengeHints(challengeId, 1);
      setHints(data.hints || []);
      setHintsRevealed(1);
    } else {
      const nextReveal = Math.min(hintsRevealed + 1, hints.length);
      await getChallengeHints(challengeId, nextReveal);
      setHintsRevealed(nextReveal);
    }
  };

  const showSolution = async () => {
    if (!challengeId) return;
    const data = await getChallengeSolution(challengeId);
    setSolution(data);
  };

  if (!challenge) return <div className="text-gray-400">Yükleniyor...</div>;

  const challengeWithTestCases = challenge as ChallengeDetail & { test_cases?: ChallengeTestCase[] };

  return (
    <div className="space-y-6">
      <div className="mb-4">
        <Link to="/challenges" className="text-sm text-blue-400 hover:underline">← Challenges</Link>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 h-[calc(100vh-12rem)]">
        {/* Left: Description */}
        <div className="bg-gray-900 border border-gray-800 rounded-xl overflow-y-auto">
          <div className="p-5">
            <div className="flex items-center gap-3 mb-3">
              <h1 className="text-xl font-bold text-white">{challenge.title}</h1>
              <DifficultyBadge difficulty={challenge.difficulty} />
              {challengeId && <BookmarkButton itemType="challenge" itemId={challengeId} />}
            </div>
            <p className="text-gray-300 text-sm leading-relaxed mb-4">{challenge.description}</p>

            {/* Test Cases */}
            {challengeWithTestCases.test_cases?.filter((t: ChallengeTestCase) => t.visible !== false).map((tc: ChallengeTestCase, i: number) => (
              <div key={i} className="bg-gray-950 rounded-lg p-3 mb-2">
                <div className="text-xs text-gray-400 mb-1">Test {i + 1}</div>
                <div className="font-mono text-sm">
                  <span className="text-gray-400">Input: </span>
                  <span className="text-blue-300">{JSON.stringify(tc.input)}</span>
                </div>
                <div className="font-mono text-sm">
                  <span className="text-gray-400">Expected: </span>
                  <span className="text-green-300">{JSON.stringify(tc.expected)}</span>
                </div>
              </div>
            ))}

            {/* Hints */}
            <div className="mt-4">
              <button onClick={revealHint} className="text-sm text-yellow-400 hover:underline">
                İpucu Al ({hintsRevealed}/{hints.length || '?'})
              </button>
              {hints.slice(0, hintsRevealed).map((hint, i) => (
                <div key={i} className="mt-2 p-3 bg-yellow-900/20 border border-yellow-500/20 rounded-lg text-sm text-yellow-200">
                  İpucu {i + 1}: {hint}
                </div>
              ))}
            </div>

            {/* Solution */}
            {submitted && (
              <div className="mt-4">
                <button onClick={showSolution} className="text-sm text-purple-400 hover:underline">
                  Çözümü Göster
                </button>
                {solution && (
                  <div className="mt-2 bg-gray-950 rounded-lg p-4">
                    <pre className="text-sm font-mono text-gray-300 whitespace-pre-wrap">{solution.solution}</pre>
                    {solution.explanation && (
                      <p className="text-sm text-gray-400 mt-3 border-t border-gray-800 pt-3">{solution.explanation}</p>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Right: Editor + Output */}
        <div className="flex flex-col gap-4">
          {/* Language Tabs */}
          <div className="flex items-center gap-2">
            {challenge.starter_code?.python && (
              <button
                onClick={() => switchLang('python')}
                className={`px-3 py-1.5 rounded text-sm font-medium transition-colors ${
                  language === 'python' ? 'bg-blue-600 text-white' : 'bg-gray-800 text-gray-400 hover:text-white'
                }`}
              >
                Python
              </button>
            )}
            {challenge.starter_code?.javascript && (
              <button
                onClick={() => switchLang('javascript')}
                className={`px-3 py-1.5 rounded text-sm font-medium transition-colors ${
                  language === 'javascript' ? 'bg-blue-600 text-white' : 'bg-gray-800 text-gray-400 hover:text-white'
                }`}
              >
                JavaScript
              </button>
            )}
          </div>

          {/* Editor */}
          <div className="flex-1 border border-gray-800 rounded-xl overflow-hidden min-h-[300px]">
            <Editor
              height="100%"
              language={language}
              value={code}
              onChange={(v) => setCode(v || '')}
              theme="vs-dark"
              options={{
                minimap: { enabled: false },
                fontSize: 14,
                lineNumbers: 'on',
                scrollBeyondLastLine: false,
                automaticLayout: true,
                tabSize: 2,
              }}
            />
          </div>

          {/* Buttons */}
          <div className="flex gap-3">
            <button
              onClick={handleRun}
              disabled={running}
              className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg text-sm transition-colors disabled:opacity-50"
            >
              {running ? 'Çalışıyor...' : 'Çalıştır'}
            </button>
            <button
              onClick={handleSubmit}
              disabled={running}
              className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg text-sm font-medium transition-colors disabled:opacity-50"
            >
              Gönder
            </button>
          </div>

          {/* Output */}
          {output && (
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-4 max-h-48 overflow-y-auto">
              {output.error ? (
                <pre className="text-red-400 text-sm font-mono whitespace-pre-wrap">{output.error}</pre>
              ) : (
                <div className="space-y-2">
                  {output.results?.map((r: TestResult, i: number) => (
                    <div key={i} className={`flex items-center gap-2 text-sm ${r.passed ? 'text-green-400' : 'text-red-400'}`}>
                      <span>{r.passed ? '✓' : '✗'}</span>
                      <span className="font-mono">
                        Input: {JSON.stringify(r.input)} → {JSON.stringify(r.actual)}
                        {!r.passed && <span className="text-gray-400"> (beklenen: {JSON.stringify(r.expected)})</span>}
                      </span>
                    </div>
                  ))}
                  {output.tests_passed === output.tests_total && output.tests_total > 0 && (
                    <div className="text-green-400 font-medium mt-2">Tüm testler geçti!</div>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function DifficultyBadge({ difficulty }: { difficulty: string }) {
  const colors: Record<string, string> = {
    easy: 'bg-green-900/50 text-green-400 border-green-500/30',
    medium: 'bg-yellow-900/50 text-yellow-400 border-yellow-500/30',
    hard: 'bg-red-900/50 text-red-400 border-red-500/30',
    expert: 'bg-purple-900/50 text-purple-400 border-purple-500/30',
  };
  const labels: Record<string, string> = { easy: 'Kolay', medium: 'Orta', hard: 'Zor', expert: 'Uzman' };
  return (
    <span className={`px-2 py-0.5 rounded border text-xs font-medium ${colors[difficulty] || colors.medium}`}>
      {labels[difficulty] || difficulty}
    </span>
  );
}
