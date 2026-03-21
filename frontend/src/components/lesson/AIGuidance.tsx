import type { Section } from '../../types';
import MarkdownRenderer from '../common/MarkdownRenderer';

export default function AIGuidance({ data }: { data: Section }) {
  return (
    <div className="bg-gradient-to-r from-violet-900/20 to-purple-900/20 border border-violet-500/30 rounded-xl overflow-hidden">
      <div className="px-5 py-3 border-b border-violet-500/20 flex items-center gap-2">
        <span className="text-xl">🤖</span>
        <h3 className="font-semibold text-violet-400">{data.title || 'Bu Derste AI ile Ogren'}</h3>
      </div>
      <div className="p-5 space-y-4">
        {data.content && (
          <MarkdownRenderer content={data.content} className="text-sm" />
        )}

        {data.model_recommendation && (
          <div className="flex items-center gap-2">
            <span className="text-xs text-gray-500">Onerilen Model:</span>
            <span className="px-2 py-0.5 bg-violet-900/30 text-violet-400 rounded text-xs font-medium">
              {data.model_recommendation}
            </span>
          </div>
        )}

        {data.prompts?.length > 0 && (
          <div className="space-y-3">
            <h4 className="text-xs font-semibold text-gray-500 uppercase">Prompt Ornekleri</h4>
            {(data.prompts as { prompt: string; why?: string; follow_up?: string }[]).map((p, i: number) => (
              <div key={i} className="bg-gray-900/50 rounded-lg p-4 space-y-2">
                <div className="font-mono text-sm text-violet-300">{p.prompt}</div>
                {p.why && <div className="text-xs text-gray-500 italic">Neden: {p.why}</div>}
                {p.follow_up && (
                  <div className="text-xs text-gray-400 border-l-2 border-violet-500/30 pl-3 mt-2">
                    Follow-up: <span className="font-mono text-violet-300/80">{p.follow_up}</span>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        {data.pair_programming_tip && (
          <div className="bg-violet-900/10 border border-violet-500/20 rounded-lg p-3">
            <div className="text-xs font-semibold text-violet-400 mb-1">Pair Programming Ipucu</div>
            <div className="text-sm text-gray-300">{data.pair_programming_tip}</div>
          </div>
        )}
      </div>
    </div>
  );
}
