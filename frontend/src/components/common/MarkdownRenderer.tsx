import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeHighlight from 'rehype-highlight';
import type { Components } from 'react-markdown';

const components: Components = {
  h1: ({ children }) => <h1 className="text-2xl font-bold text-white mt-8 mb-4">{children}</h1>,
  h2: ({ children }) => <h2 className="text-xl font-bold text-white mt-6 mb-3">{children}</h2>,
  h3: ({ children }) => <h3 className="text-lg font-semibold text-white mt-5 mb-2">{children}</h3>,
  h4: ({ children }) => <h4 className="text-base font-semibold text-white mt-4 mb-2">{children}</h4>,
  p: ({ children }) => <p className="text-gray-300 leading-relaxed mb-3">{children}</p>,
  strong: ({ children }) => <strong className="text-white font-semibold">{children}</strong>,
  em: ({ children }) => <em className="text-gray-400 italic">{children}</em>,
  a: ({ href, children }) => (
    <a href={href} target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:underline">
      {children}
    </a>
  ),
  ul: ({ children }) => <ul className="list-disc ml-5 space-y-1 mb-3 text-gray-300">{children}</ul>,
  ol: ({ children }) => <ol className="list-decimal ml-5 space-y-1 mb-3 text-gray-300">{children}</ol>,
  li: ({ children }) => <li className="text-gray-300 leading-relaxed">{children}</li>,
  blockquote: ({ children }) => (
    <blockquote className="border-l-4 border-emerald-500/50 pl-4 py-1 my-3 text-gray-400 italic">
      {children}
    </blockquote>
  ),
  code: ({ className, children }) => {
    const isBlock = className?.includes('language-');
    if (isBlock) {
      return <code className={`${className} block`}>{children}</code>;
    }
    return (
      <code className="px-1.5 py-0.5 bg-gray-800 text-blue-300 rounded text-sm font-mono">
        {children}
      </code>
    );
  },
  pre: ({ children }) => (
    <pre className="bg-gray-950 rounded-lg p-4 overflow-x-auto mb-3 text-sm">{children}</pre>
  ),
  table: ({ children }) => (
    <div className="overflow-x-auto mb-3">
      <table className="w-full text-sm text-gray-300 border-collapse">{children}</table>
    </div>
  ),
  thead: ({ children }) => <thead className="border-b border-gray-700">{children}</thead>,
  th: ({ children }) => <th className="text-left py-2 px-3 text-gray-400 font-semibold">{children}</th>,
  td: ({ children }) => <td className="py-2 px-3 border-b border-gray-800">{children}</td>,
  hr: () => <hr className="border-gray-800 my-4" />,
};

export default function MarkdownRenderer({ content, className = '' }: { content: string; className?: string }) {
  if (!content) return null;
  return (
    <div className={className}>
      <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeHighlight]} components={components}>
        {content}
      </ReactMarkdown>
    </div>
  );
}
