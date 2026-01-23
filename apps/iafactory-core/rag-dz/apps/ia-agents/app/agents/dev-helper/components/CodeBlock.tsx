'use client';

import { useState } from 'react';

interface CodeBlockProps {
  code: string;
  language: string;
}

export default function CodeBlock({ code, language }: CodeBlockProps) {
  const [copied, setCopied] = useState(false);

  const copyToClipboard = async () => {
    await navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="relative group my-4">
      {/* Language badge */}
      <div className="flex items-center justify-between bg-slate-800 px-4 py-2 rounded-t-lg">
        <span className="text-xs font-mono text-slate-400">{language}</span>
        <button
          onClick={copyToClipboard}
          className="text-xs px-3 py-1 bg-slate-700 hover:bg-slate-600 text-slate-300 rounded transition-colors"
        >
          {copied ? '✓ Copied!' : 'Copy'}
        </button>
      </div>

      {/* Code content */}
      <pre className="bg-slate-900 p-4 rounded-b-lg overflow-x-auto">
        <code className="text-sm font-mono text-slate-100">{code}</code>
      </pre>
    </div>
  );
}
