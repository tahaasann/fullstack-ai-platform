import type { Section } from '../../types';

export default function ConceptCard({ concept }: { concept: Section }) {
  return (
    <div className="bg-gradient-to-r from-blue-900/30 to-purple-900/30 border border-blue-500/30 rounded-xl p-5">
      <div className="flex items-start gap-3">
        <span className="text-2xl">💡</span>
        <div className="flex-1">
          <h3 className="text-lg font-bold text-white mb-1">{concept.title}</h3>
          {concept.turkish && (
            <div className="text-sm text-blue-300 mb-2">Türkçe: {concept.turkish}</div>
          )}
          <p className="text-gray-300 leading-relaxed">{concept.content}</p>
          {concept.analogy && (
            <div className="mt-3 p-3 bg-gray-900/50 rounded-lg">
              <span className="text-xs text-gray-500 uppercase font-semibold">Gerçek Hayat Benzetmesi</span>
              <p className="text-gray-400 text-sm mt-1">{concept.analogy}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
