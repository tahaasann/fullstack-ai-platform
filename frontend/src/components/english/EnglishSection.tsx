import { useState } from 'react';
import type { Section } from '../../types';
import MarkdownRenderer from '../common/MarkdownRenderer';

interface LessonVocabWord {
  term: string;
  pronunciation?: string;
  turkish?: string;
  definition?: string;
  example?: string;
}

export default function EnglishSection({ data }: { data: Section }) {
  const [showAnswers, setShowAnswers] = useState(false);

  const vocabulary = data.vocabulary || [];
  const reading = data.reading || null;
  const writing = data.writing || null;
  const hasStructuredData = vocabulary.length > 0 || reading || writing;
  const rawContent = typeof data.content === 'string' ? data.content : null;

  return (
    <div className="bg-gradient-to-r from-emerald-900/20 to-teal-900/20 border border-emerald-500/30 rounded-xl overflow-hidden">
      <div className="px-5 py-3 border-b border-emerald-500/20 flex items-center gap-2">
        <span className="text-xl">🌐</span>
        <h3 className="font-semibold text-emerald-400">Teknik İngilizce</h3>
      </div>

      {/* Raw markdown content from :::english directive */}
      {!hasStructuredData && rawContent && (
        <div className="p-5">
          <MarkdownRenderer content={rawContent} className="text-sm" />
        </div>
      )}

      {/* Vocabulary */}
      {vocabulary.length > 0 && (
        <div className="p-5 border-b border-emerald-500/10">
          <h4 className="text-sm font-semibold text-gray-400 mb-3 uppercase">Yeni Kelimeler</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {vocabulary.map((word: LessonVocabWord, i: number) => (
              <VocabCard key={i} word={word} />
            ))}
          </div>
        </div>
      )}

      {/* Reading Exercise */}
      {reading && (
        <div className="p-5 border-b border-emerald-500/10">
          <h4 className="text-sm font-semibold text-gray-400 mb-3 uppercase">Okuma Egzersizi</h4>
          <div className="bg-gray-900/50 rounded-lg p-4 mb-3">
            <p className="text-gray-300 text-sm font-mono leading-relaxed">{reading.text}</p>
          </div>
          {reading.question && (
            <div>
              <p className="text-gray-300 text-sm mb-2">{reading.question}</p>
              <button
                onClick={() => setShowAnswers(!showAnswers)}
                className="text-xs text-emerald-400 hover:underline"
              >
                {showAnswers ? 'Cevabı Gizle' : 'Cevabı Göster'}
              </button>
              {showAnswers && reading.answer && (
                <p className="text-sm text-gray-400 mt-2 p-3 bg-gray-900/50 rounded-lg">{reading.answer}</p>
              )}
            </div>
          )}
        </div>
      )}

      {/* Writing Exercise */}
      {writing && (
        <div className="p-5">
          <h4 className="text-sm font-semibold text-gray-400 mb-3 uppercase">Yazma Egzersizi</h4>
          <p className="text-gray-300 text-sm mb-3">{writing.prompt}</p>
          <textarea
            className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-sm text-gray-300 placeholder-gray-600 focus:border-emerald-500 focus:outline-none resize-y min-h-20"
            placeholder="İngilizce yazınızı buraya yazın..."
            rows={3}
          />
          {writing.example && (
            <details className="mt-2">
              <summary className="text-xs text-emerald-400 cursor-pointer hover:underline">Örnek Cevap</summary>
              <p className="text-sm text-gray-400 mt-2 p-3 bg-gray-900/50 rounded-lg">{writing.example}</p>
            </details>
          )}
        </div>
      )}
    </div>
  );
}

function VocabCard({ word }: { word: LessonVocabWord }) {
  const [flipped, setFlipped] = useState(false);

  return (
    <button
      onClick={() => setFlipped(!flipped)}
      className="text-left p-3 bg-gray-900/50 rounded-lg border border-gray-800 hover:border-emerald-500/30 transition-colors"
    >
      <div className="flex items-center justify-between">
        <span className="font-mono text-emerald-300 font-medium">{word.term}</span>
        <span className="text-xs text-gray-600">{word.pronunciation || ''}</span>
      </div>
      {flipped ? (
        <div className="mt-2">
          <p className="text-sm text-gray-400">{word.turkish || word.definition}</p>
          {word.example && (
            <p className="text-xs text-gray-500 mt-1 italic">"{word.example}"</p>
          )}
        </div>
      ) : (
        <p className="text-xs text-gray-600 mt-1">Çevirmek için tıkla</p>
      )}
    </button>
  );
}
