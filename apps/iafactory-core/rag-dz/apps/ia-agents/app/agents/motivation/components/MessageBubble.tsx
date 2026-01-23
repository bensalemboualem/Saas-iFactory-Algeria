'use client';

import { Message } from 'ai';
import { format } from 'date-fns';

interface MessageBubbleProps {
  message: Message;
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === 'user';

  return (
    <div
      className={`flex ${isUser ? 'justify-end' : 'justify-start'} message-animate`}
    >
      <div className={`flex items-start space-x-2 max-w-[80%] ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
        {/* Avatar */}
        <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-lg ${
          isUser
            ? 'bg-primary text-white'
            : 'bg-gradient-to-br from-green-500 to-emerald-600 text-white'
        }`}>
          {isUser ? '👤' : '💪'}
        </div>

        {/* Message Content */}
        <div className="flex flex-col">
          <div
            className={`px-4 py-3 rounded-2xl ${
              isUser
                ? 'bg-primary text-white rounded-tr-none'
                : 'bg-slate-200 dark:bg-slate-800 text-slate-900 dark:text-white rounded-tl-none'
            }`}
          >
            <p className="text-sm md:text-base whitespace-pre-wrap leading-relaxed">
              {message.content}
            </p>
          </div>

          {/* Timestamp */}
          <span className={`text-xs text-slate-500 dark:text-slate-400 mt-1 ${isUser ? 'text-right' : 'text-left'}`}>
            {message.createdAt ? format(new Date(message.createdAt), 'HH:mm') : 'maintenant'}
          </span>
        </div>
      </div>
    </div>
  );
}
