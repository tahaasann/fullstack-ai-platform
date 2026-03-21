import { useState } from 'react';
import type { Section } from '../../types';

export default function CodeBlock({ code }: { code: Section }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(code.content || '');
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
      <div className="flex items-center justify-between px-4 py-2 border-b border-gray-800 bg-gray-900/80">
        <div className="flex items-center gap-2">
          <span className="text-xs text-gray-500 font-mono uppercase">{code.language || 'code'}</span>
          {code.title && <span className="text-xs text-gray-400">— {code.title}</span>}
        </div>
        <button
          onClick={handleCopy}
          className="text-xs text-gray-500 hover:text-gray-300 transition-colors px-2 py-1"
        >
          {copied ? '✓ Kopyalandı' : 'Kopyala'}
        </button>
      </div>
      <pre className="p-4 overflow-x-auto">
        <code className="text-sm font-mono text-gray-300 leading-relaxed whitespace-pre">
          {code.content}
        </code>
      </pre>
    </div>
  );
}
