import type { Section } from '../../types';
import MarkdownRenderer from '../common/MarkdownRenderer';

export default function SeniorLearns({ data }: { data: Section }) {
  return (
    <div className="bg-gradient-to-r from-slate-900 to-gray-900 border border-slate-500/30 rounded-xl overflow-hidden">
      <div className="px-5 py-3 bg-slate-800/50 border-b border-slate-500/20 flex items-center gap-2">
        <span className="text-xl">🎩</span>
        <h3 className="font-bold text-slate-200">Senior/CTO Böyle Öğrenir</h3>
      </div>
      <div className="p-5 space-y-4">
        <MarkdownRenderer content={data.content} className="text-sm" />

        {data.steps && (
          <div className="space-y-2">
            {data.steps.map((step: string, i: number) => (
              <div key={i} className="flex items-start gap-3">
                <div className="w-6 h-6 rounded-full bg-slate-700 flex items-center justify-center shrink-0 mt-0.5">
                  <span className="text-xs font-bold text-slate-300">{i + 1}</span>
                </div>
                <p className="text-sm text-gray-300">{step}</p>
              </div>
            ))}
          </div>
        )}

        {data.mindset && (
          <div className="bg-slate-800/50 rounded-lg p-4 mt-3">
            <div className="flex items-center gap-2 mb-2">
              <span>🧠</span>
              <span className="text-xs font-semibold text-slate-400 uppercase">Profesyonel Mindset</span>
            </div>
            <p className="text-sm text-gray-400 italic">{data.mindset}</p>
          </div>
        )}
      </div>
    </div>
  );
}
