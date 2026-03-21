import { useState } from 'react';

interface ArchitectureDiagramProps {
  title?: string;
  content: string;
  description?: string;
}

export default function ArchitectureDiagram({ title, content, description }: ArchitectureDiagramProps) {
  const [zoom, setZoom] = useState(1);

  return (
    <div className="bg-gray-950 border border-blue-500/20 rounded-xl overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between px-5 py-3 border-b border-blue-500/10 bg-blue-900/10">
        <div className="flex items-center gap-2">
          <span className="text-blue-400 text-lg">📐</span>
          <h4 className="text-sm font-semibold text-blue-300">{title || 'Mimari Diyagram'}</h4>
        </div>
        <div className="flex items-center gap-1">
          <button
            onClick={() => setZoom(z => Math.max(0.5, z - 0.25))}
            className="w-7 h-7 rounded bg-gray-800 hover:bg-gray-700 text-gray-400 hover:text-white text-xs transition-colors"
            aria-label="Küçült"
          >
            −
          </button>
          <span className="text-xs text-gray-500 w-10 text-center">{Math.round(zoom * 100)}%</span>
          <button
            onClick={() => setZoom(z => Math.min(2, z + 0.25))}
            className="w-7 h-7 rounded bg-gray-800 hover:bg-gray-700 text-gray-400 hover:text-white text-xs transition-colors"
            aria-label="Büyüt"
          >
            +
          </button>
          <button
            onClick={() => setZoom(1)}
            className="ml-1 w-7 h-7 rounded bg-gray-800 hover:bg-gray-700 text-gray-400 hover:text-white text-xs transition-colors"
            aria-label="Sıfırla"
          >
            ↺
          </button>
        </div>
      </div>

      {/* Diagram */}
      <div className="overflow-auto p-4" style={{ maxHeight: '600px' }}>
        <pre
          className="text-gray-300 font-mono leading-relaxed whitespace-pre select-text"
          style={{
            fontSize: `${zoom * 0.75}rem`,
            transform: `scale(${zoom})`,
            transformOrigin: 'top left',
          }}
        >
          {content}
        </pre>
      </div>

      {/* Description */}
      {description && (
        <div className="px-5 py-3 border-t border-blue-500/10 bg-blue-900/5">
          <p className="text-xs text-gray-400 leading-relaxed">{description}</p>
        </div>
      )}
    </div>
  );
}
