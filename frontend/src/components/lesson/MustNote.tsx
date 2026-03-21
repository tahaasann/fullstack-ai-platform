import type { Section } from '../../types';

export default function MustNote({ data }: { data: Section }) {
  const items = data.items || data.content?.split('\n').filter((l: string) => l.trim()) || [];

  return (
    <div className="bg-gradient-to-r from-amber-900/30 to-yellow-900/20 border-2 border-amber-500/40 rounded-xl p-5">
      <div className="flex items-center gap-2 mb-4">
        <span className="text-2xl">📝</span>
        <h3 className="text-lg font-bold text-amber-400">Bunu Kesinlikle Not Al!</h3>
        <span className="text-xs bg-amber-500/20 text-amber-300 px-2 py-0.5 rounded-full ml-auto">DEFTERE YAZ</span>
      </div>
      <div className="space-y-2">
        {typeof items === 'string' ? (
          <p className="text-gray-200 text-sm leading-relaxed">{items}</p>
        ) : (
          items.map((item: string, i: number) => (
            <div key={i} className="flex items-start gap-2">
              <span className="text-amber-400 mt-0.5 shrink-0">&#9998;</span>
              <p className="text-gray-200 text-sm leading-relaxed">{item.replace(/^[-•]\s*/, '')}</p>
            </div>
          ))
        )}
      </div>
      <div className="mt-3 pt-3 border-t border-amber-500/20">
        <p className="text-xs text-amber-300/60 italic">
          Geri kalanını not almana gerek yok - tekrar baktığında hatırlarsın. Sadece yukarıdakileri yaz.
        </p>
      </div>
    </div>
  );
}
