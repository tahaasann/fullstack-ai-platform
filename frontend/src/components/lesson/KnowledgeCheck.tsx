import { useState } from 'react';
import type { Section } from '../../types';

export default function KnowledgeCheck({ data }: { data: Section }) {
  const [selected, setSelected] = useState<string | null>(null);
  const [revealed, setRevealed] = useState(false);

  const question = data.question || data.content || '';
  const options = data.options || [];
  const answer = data.answer;
  const explanation = data.explanation || '';

  const handleCheck = () => {
    setRevealed(true);
  };

  const isCorrect = selected === answer;

  return (
    <div className="bg-gradient-to-r from-indigo-900/20 to-transparent border border-indigo-500/30 rounded-xl p-5">
      <div className="flex items-center gap-2 mb-3">
        <span className="text-xl">🧪</span>
        <h4 className="font-semibold text-indigo-400">Bilgi Kontrolü</h4>
      </div>
      <p className="text-gray-200 mb-4">{question}</p>

      {options.length > 0 && (
        <div className="space-y-2 mb-4">
          {options.map((opt: string, i: number) => {
            const letter = String.fromCharCode(65 + i);
            const isThis = selected === letter;
            const isAnswer = letter === answer;
            let cls = 'border-gray-700 hover:border-gray-600';
            if (revealed && isAnswer) cls = 'border-green-500 bg-green-900/20';
            else if (revealed && isThis && !isCorrect) cls = 'border-red-500 bg-red-900/20';
            else if (isThis) cls = 'border-blue-500 bg-blue-900/20';

            return (
              <button
                key={i}
                onClick={() => !revealed && setSelected(letter)}
                className={`w-full text-left p-3 rounded-lg border ${cls} transition-colors text-sm`}
              >
                <span className="font-mono text-gray-400 mr-2">{letter}.</span>
                <span className="text-gray-300">{opt}</span>
              </button>
            );
          })}
        </div>
      )}

      {!revealed && selected && (
        <button
          onClick={handleCheck}
          className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-sm transition-colors"
        >
          Kontrol Et
        </button>
      )}

      {revealed && (
        <div className={`mt-3 p-3 rounded-lg text-sm ${isCorrect ? 'bg-green-900/30 text-green-300' : 'bg-red-900/30 text-red-300'}`}>
          {isCorrect ? '✓ Doğru!' : '✗ Yanlış.'} {explanation}
        </div>
      )}
    </div>
  );
}
