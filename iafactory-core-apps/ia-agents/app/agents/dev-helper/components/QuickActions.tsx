'use client';

interface QuickAction {
  id: string;
  emoji: string;
  label: string;
  prompt: string;
  color: string;
}

const QUICK_ACTIONS: QuickAction[] = [
  {
    id: 'fix-bug',
    emoji: '🐛',
    label: 'Fix This Bug',
    prompt: "J'ai un bug, peux-tu m'aider à le résoudre?",
    color: 'bg-red-500 hover:bg-red-600',
  },
  {
    id: 'explain-code',
    emoji: '📖',
    label: 'Explain Code',
    prompt: 'Peux-tu expliquer ce code étape par étape?',
    color: 'bg-blue-500 hover:bg-blue-600',
  },
  {
    id: 'optimize',
    emoji: '⚡',
    label: 'Optimize',
    prompt: 'Comment optimiser ce code pour la performance?',
    color: 'bg-yellow-500 hover:bg-yellow-600',
  },
  {
    id: 'document',
    emoji: '📝',
    label: 'Document',
    prompt: 'Peux-tu générer la documentation pour ce code?',
    color: 'bg-green-500 hover:bg-green-600',
  },
];

interface QuickActionsProps {
  onActionClick: (prompt: string) => void;
}

export default function QuickActions({ onActionClick }: QuickActionsProps) {
  return (
    <div className="card p-4">
      <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-4">
        ⚡ Quick Actions
      </h3>

      <div className="space-y-2">
        {QUICK_ACTIONS.map((action) => (
          <button
            key={action.id}
            onClick={() => onActionClick(action.prompt)}
            className={`w-full text-left px-4 py-3 ${action.color} text-white rounded-lg transition-colors flex items-center space-x-3`}
          >
            <span className="text-2xl">{action.emoji}</span>
            <span className="font-medium">{action.label}</span>
          </button>
        ))}
      </div>

      <div className="mt-6 p-3 bg-slate-100 dark:bg-slate-800 rounded-lg">
        <p className="text-xs text-slate-600 dark:text-slate-400">
          💡 <strong>Tip:</strong> Paste your code in the chat for better results!
        </p>
      </div>
    </div>
  );
}
