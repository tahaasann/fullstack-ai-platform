import MarkdownRenderer from '../common/MarkdownRenderer';

const styles: Record<string, { icon: string; border: string; bg: string; title_color: string }> = {
  warning: { icon: '⚠️', border: 'border-yellow-500/30', bg: 'from-yellow-900/20 to-transparent', title_color: 'text-yellow-400' },
  tip: { icon: '💡', border: 'border-blue-500/30', bg: 'from-blue-900/20 to-transparent', title_color: 'text-blue-400' },
  realworld: { icon: '🌍', border: 'border-green-500/30', bg: 'from-green-900/20 to-transparent', title_color: 'text-green-400' },
  interview: { icon: '🎯', border: 'border-purple-500/30', bg: 'from-purple-900/20 to-transparent', title_color: 'text-purple-400' },
  deha: { icon: '🧠', border: 'border-cyan-500/30', bg: 'from-cyan-900/20 to-transparent', title_color: 'text-cyan-400' },
  mistake: { icon: '🚫', border: 'border-red-500/30', bg: 'from-red-900/20 to-transparent', title_color: 'text-red-400' },
  exercise: { icon: '🏋️', border: 'border-orange-500/30', bg: 'from-orange-900/20 to-transparent', title_color: 'text-orange-400' },
  resource: { icon: '📎', border: 'border-gray-500/30', bg: 'from-gray-800/50 to-transparent', title_color: 'text-gray-300' },
};

export default function InfoBox({ type, title, content, url }: {
  type: string; title: string; content: string; url?: string;
}) {
  const s = styles[type] || styles.tip;

  return (
    <div className={`bg-gradient-to-r ${s.bg} border ${s.border} rounded-xl p-5`}>
      <div className="flex items-start gap-3">
        <span className="text-xl mt-0.5">{s.icon}</span>
        <div className="flex-1">
          <h4 className={`font-semibold ${s.title_color} mb-2`}>{title}</h4>
          <MarkdownRenderer content={content} className="text-sm" />
          {url && (
            <a
              href={url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block mt-3 text-sm text-blue-400 hover:underline"
            >
              Kaynağa Git →
            </a>
          )}
        </div>
      </div>
    </div>
  );
}
