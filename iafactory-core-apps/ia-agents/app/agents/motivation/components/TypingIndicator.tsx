export default function TypingIndicator() {
  return (
    <div className="flex justify-start message-animate">
      <div className="flex items-start space-x-2">
        {/* Avatar */}
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-green-500 to-emerald-600 text-white flex items-center justify-center text-lg">
          💪
        </div>

        {/* Typing Animation */}
        <div className="px-4 py-3 rounded-2xl rounded-tl-none bg-slate-200 dark:bg-slate-800">
          <div className="flex space-x-2">
            <div className="w-2 h-2 bg-slate-500 dark:bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
            <div className="w-2 h-2 bg-slate-500 dark:bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
            <div className="w-2 h-2 bg-slate-500 dark:bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
          </div>
        </div>
      </div>
    </div>
  );
}
