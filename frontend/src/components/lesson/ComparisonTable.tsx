import type { Section } from '../../types';

export default function ComparisonTable({ comparison }: { comparison: Section }) {
  const headers = comparison.headers || [];
  const rows = comparison.rows || [];

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
      <div className="px-5 py-3 border-b border-gray-800 flex items-center gap-2">
        <span>⚖️</span>
        <h3 className="text-sm font-semibold text-gray-300">
          {comparison.title || 'Karşılaştırma'}
        </h3>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          {headers.length > 0 && (
            <thead>
              <tr className="border-b border-gray-800">
                {headers.map((h: string, i: number) => (
                  <th key={i} className="px-4 py-3 text-left text-gray-400 font-medium">{h}</th>
                ))}
              </tr>
            </thead>
          )}
          <tbody>
            {rows.map((row: string[], ri: number) => (
              <tr key={ri} className="border-b border-gray-800/50 last:border-0">
                {row.map((cell: string, ci: number) => (
                  <td key={ci} className={`px-4 py-3 ${ci === 0 ? 'text-white font-medium' : 'text-gray-400'}`}>
                    {cell}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
