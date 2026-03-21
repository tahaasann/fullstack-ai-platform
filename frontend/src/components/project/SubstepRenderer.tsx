import { useState } from 'react';

interface Substep {
  order: string;
  action: string;
  type: 'terminal' | 'file_open' | 'code_write' | 'code_add' | 'code_modify' | 'validate' | 'explain';
  command?: string;
  expected_output?: string;
  file?: string;
  code?: string;
  position?: string;
  validation?: string;
  why?: string;
}

interface CommonError {
  error: string;
  cause: string;
  fix: string;
}

interface StepWithSubsteps {
  step: number;
  title: string;
  why?: string;
  instructions?: string;
  code_snippet?: string;
  deep_dive?: string;
  checkpoint?: string;
  substeps?: Substep[];
  folder_structure_after?: string;
  common_errors?: CommonError[];
}

function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);
  const handleCopy = () => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };
  return (
    <button
      onClick={handleCopy}
      className="px-2 py-0.5 text-xs bg-gray-700 hover:bg-gray-600 text-gray-300 rounded transition-colors"
      aria-label="Kopyala"
    >
      {copied ? '✓' : '📋'}
    </button>
  );
}

function TerminalBlock({ command, expected_output, validation }: { command?: string; expected_output?: string; validation?: string }) {
  const [showOutput, setShowOutput] = useState(false);

  return (
    <div className="space-y-2">
      {command && (
        <div className="bg-gray-950 border border-gray-700 rounded-lg overflow-hidden">
          <div className="flex items-center justify-between px-3 py-1.5 bg-gray-800/50 border-b border-gray-700">
            <div className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-red-500/60" />
              <span className="w-2.5 h-2.5 rounded-full bg-yellow-500/60" />
              <span className="w-2.5 h-2.5 rounded-full bg-green-500/60" />
              <span className="text-xs text-gray-500 ml-2">Terminal</span>
            </div>
            <CopyButton text={command} />
          </div>
          <div className="p-3">
            <code className="text-sm text-green-400 font-mono">
              <span className="text-gray-500">$ </span>{command}
            </code>
          </div>
        </div>
      )}

      {expected_output && (
        <div>
          <button
            onClick={() => setShowOutput(!showOutput)}
            className="text-xs text-gray-500 hover:text-gray-300 transition-colors flex items-center gap-1"
          >
            <span className={`transition-transform ${showOutput ? 'rotate-90' : ''}`}>▶</span>
            Beklenen çıktı
          </button>
          {showOutput && (
            <pre className="mt-1 bg-gray-900/50 border border-gray-800 rounded p-3 text-xs text-gray-400 font-mono overflow-x-auto">
              {expected_output}
            </pre>
          )}
        </div>
      )}

      {validation && (
        <div className="bg-green-900/10 border border-green-500/20 rounded-lg p-2.5">
          <span className="text-xs text-green-400">✓ </span>
          <span className="text-xs text-green-300">{validation}</span>
        </div>
      )}
    </div>
  );
}

function CodeFileBlock({ file, code, position, type }: { file?: string; code?: string; position?: string; type: string }) {
  const typeLabel = type === 'code_write' ? 'Oluştur' : type === 'code_add' ? `Ekle (${position || 'bottom'})` : 'Değiştir';
  const borderColor = type === 'code_modify' ? 'border-yellow-500/20' : 'border-emerald-500/20';
  const labelColor = type === 'code_modify' ? 'text-yellow-400' : 'text-emerald-400';

  return (
    <div className={`bg-gray-950 border ${borderColor} rounded-lg overflow-hidden`}>
      {file && (
        <div className="flex items-center justify-between px-3 py-1.5 bg-gray-800/50 border-b border-gray-700">
          <div className="flex items-center gap-2">
            <span className="text-xs text-gray-500">📄</span>
            <code className="text-xs text-blue-300 font-mono">{file}</code>
            <span className={`text-[10px] px-1.5 py-0.5 rounded ${labelColor} bg-gray-800`}>{typeLabel}</span>
          </div>
          {code && <CopyButton text={code} />}
        </div>
      )}
      {code && (
        <pre className="p-3 text-sm text-gray-300 font-mono overflow-x-auto leading-relaxed">
          <code>{code}</code>
        </pre>
      )}
    </div>
  );
}

function SubstepItem({ substep, index }: { substep: Substep; index: number }) {
  return (
    <div className="flex gap-3">
      {/* Number indicator */}
      <div className="flex flex-col items-center shrink-0">
        <div className="w-7 h-7 rounded-full bg-blue-900/30 border border-blue-500/30 flex items-center justify-center">
          <span className="text-xs font-mono text-blue-400">{substep.order}</span>
        </div>
        {/* Connecting line */}
        <div className="w-px flex-1 bg-gray-800 mt-1" />
      </div>

      {/* Content */}
      <div className="flex-1 pb-5 space-y-2">
        <div className="text-sm font-medium text-gray-200">{substep.action}</div>

        {substep.why && (
          <div className="text-xs text-yellow-300/70 bg-yellow-900/10 border border-yellow-500/10 rounded px-3 py-1.5">
            <span className="font-medium">NEDEN: </span>{substep.why}
          </div>
        )}

        {/* Terminal type */}
        {substep.type === 'terminal' && (
          <TerminalBlock
            command={substep.command}
            expected_output={substep.expected_output}
            validation={substep.validation}
          />
        )}

        {/* File open type */}
        {substep.type === 'file_open' && substep.file && (
          <div className="flex items-center gap-2 bg-gray-800/50 border border-gray-700 rounded-lg px-3 py-2">
            <span className="text-sm">📂</span>
            <code className="text-sm text-blue-300 font-mono">{substep.file}</code>
          </div>
        )}

        {/* Code types */}
        {['code_write', 'code_add', 'code_modify'].includes(substep.type) && (
          <CodeFileBlock
            file={substep.file}
            code={substep.code}
            position={substep.position}
            type={substep.type}
          />
        )}

        {/* Validate type */}
        {substep.type === 'validate' && substep.validation && (
          <div className="bg-green-900/10 border border-green-500/20 rounded-lg p-3">
            <div className="text-xs font-semibold text-green-400 mb-1">✓ Doğrulama</div>
            <div className="text-sm text-green-300">{substep.validation}</div>
          </div>
        )}

        {/* Explain type */}
        {substep.type === 'explain' && (
          <div className="bg-blue-900/10 border border-blue-500/20 rounded-lg p-3">
            <div className="text-sm text-blue-200">{substep.code || ''}</div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function SubstepRenderer({ step }: { step: StepWithSubsteps }) {
  const [showErrors, setShowErrors] = useState(false);
  const [showStructure, setShowStructure] = useState(false);

  if (!step.substeps || step.substeps.length === 0) return null;

  return (
    <div className="space-y-4">
      {/* Substeps */}
      <div className="pl-1">
        {step.substeps.map((substep, i) => (
          <SubstepItem key={substep.order} substep={substep} index={i} />
        ))}
      </div>

      {/* Folder structure after */}
      {step.folder_structure_after && (
        <div>
          <button
            onClick={() => setShowStructure(!showStructure)}
            className="text-xs text-gray-500 hover:text-gray-300 transition-colors flex items-center gap-1"
          >
            <span className={`transition-transform ${showStructure ? 'rotate-90' : ''}`}>▶</span>
            📁 Bu adımdan sonra dosya yapısı
          </button>
          {showStructure && (
            <pre className="mt-2 bg-gray-900/50 border border-gray-800 rounded-lg p-3 text-xs text-gray-400 font-mono overflow-x-auto">
              {step.folder_structure_after}
            </pre>
          )}
        </div>
      )}

      {/* Common errors */}
      {step.common_errors && step.common_errors.length > 0 && (
        <div>
          <button
            onClick={() => setShowErrors(!showErrors)}
            className="text-xs text-gray-500 hover:text-gray-300 transition-colors flex items-center gap-1"
          >
            <span className={`transition-transform ${showErrors ? 'rotate-90' : ''}`}>▶</span>
            ⚠️ Sık karşılaşılan hatalar ({step.common_errors.length})
          </button>
          {showErrors && (
            <div className="mt-2 space-y-2">
              {step.common_errors.map((err, i) => (
                <div key={i} className="bg-red-900/10 border border-red-500/20 rounded-lg p-3">
                  <code className="text-xs text-red-400 font-mono block mb-1">{err.error}</code>
                  <div className="text-xs text-gray-400 mb-1"><span className="font-medium">Sebep:</span> {err.cause}</div>
                  <div className="text-xs text-green-400"><span className="font-medium text-gray-400">Çözüm:</span> {err.fix}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
