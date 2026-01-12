"use client";

import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MessageCircle, X, Send, Loader2, Sparkles } from "lucide-react";
import { useThemeStore, useLocaleStore, useChatStore } from "@/lib/store";
import { t } from "@/lib/i18n";

export default function ChatHelp() {
  const { theme } = useThemeStore();
  const { locale } = useLocaleStore();
  const { isOpen, messages, toggle, addMessage } = useChatStore();
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Dziria assistant labels
  const dziria = {
    name: locale === 'ar' ? 'ذزيريا' : 'Dziria',
    subtitle: locale === 'ar' ? 'مساعدتك الذكية الجزائرية' : locale === 'en' ? 'Your Algerian AI Assistant' : 'Votre assistante IA algérienne',
    placeholder: locale === 'ar' ? 'اكتب سؤالك هنا...' : locale === 'en' ? 'Type your question here...' : 'Écrivez votre question ici...',
    greeting: locale === 'ar' ? 'مرحبا! أنا ذزيريا، مساعدتك الذكية. كيف يمكنني مساعدتك اليوم؟' : locale === 'en' ? 'Hello! I\'m Dziria, your AI assistant. How can I help you today?' : 'Bonjour ! Je suis Dziria, votre assistante IA. Comment puis-je vous aider aujourd\'hui ?',
  };

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput("");
    addMessage("user", userMessage);
    setIsLoading(true);

    // Simulate AI response (replace with actual API call)
    setTimeout(() => {
      const responses: Record<string, string[]> = {
        fr: [
          "Je suis Dziria, votre assistante IA algérienne ! Pour créer une vidéo, allez dans le Studio.",
          "Besahtek ! L'éditeur vous permet de monter vos vidéos avec une timeline professionnelle.",
          "Les voix en Darija sont disponibles dans l'onglet Audio du Studio.",
          "Pour acheter des crédits, rendez-vous dans la section Crédits.",
        ],
        ar: [
          "أنا ذزيريا، مساعدتك الذكية الجزائرية! لإنشاء فيديو، اذهب إلى الاستوديو.",
          "بصحتك! المحرر يسمح لك بمونتاج الفيديوهات مع تايم لاين احترافي.",
          "أصوات الدارجة متاحة في تبويب الصوت بالاستوديو.",
          "لشراء الأرصدة، اذهب إلى قسم الأرصدة.",
        ],
        en: [
          "I'm Dziria, your Algerian AI assistant! To create a video, go to the Studio.",
          "Great! The editor allows you to edit your videos with a professional timeline.",
          "Darija voices are available in the Audio tab of the Studio.",
          "To purchase credits, go to the Credits section.",
        ],
      };

      const randomResponse =
        responses[locale][Math.floor(Math.random() * responses[locale].length)];
      addMessage("assistant", randomResponse);
      setIsLoading(false);
    }, 1000);
  };

  return (
    <>
      {/* Floating Button - Dziria style */}
      <motion.button
        onClick={toggle}
        className={`fixed bottom-6 z-50 w-14 h-14 rounded-full shadow-xl flex items-center justify-center transition-all ${
          locale === 'ar' ? 'left-6' : 'right-6'
        } ${
          isOpen
            ? "bg-red-500 hover:bg-red-600"
            : "bg-gradient-to-r from-emerald-500 to-cyan-500 hover:shadow-emerald-500/50"
        }`}
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.95 }}
      >
        {isOpen ? (
          <X className="w-6 h-6 text-white" />
        ) : (
          <div className="relative">
            <MessageCircle className="w-6 h-6 text-white" />
            <Sparkles className="w-3 h-3 text-yellow-300 absolute -top-1 -right-1" />
          </div>
        )}
      </motion.button>

      {/* Chat Window - Dziria themed */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.95 }}
            className={`fixed bottom-24 z-50 w-96 h-[500px] rounded-2xl shadow-2xl overflow-hidden flex flex-col ${
              locale === 'ar' ? 'left-6' : 'right-6'
            } ${
              theme === "dark"
                ? "bg-[#141419] border border-[#2a2a35]"
                : "bg-white border border-gray-200"
            }`}
          >
            {/* Header - Dziria branding */}
            <div className="px-4 py-3 bg-gradient-to-r from-emerald-500 to-cyan-500">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-white/20 flex items-center justify-center text-xl">
                  🇩🇿
                </div>
                <div>
                  <h3 className="font-bold text-white">{dziria.name}</h3>
                  <p className="text-xs text-white/80">{dziria.subtitle}</p>
                </div>
              </div>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.length === 0 && (
                <div className="text-center py-8">
                  <div className="text-4xl mb-4">🇩🇿</div>
                  <p
                    className={`text-sm ${
                      theme === "dark" ? "text-gray-400" : "text-gray-500"
                    }`}
                  >
                    {dziria.greeting}
                  </p>
                </div>
              )}

              {messages.map((msg, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`flex gap-3 ${
                    msg.role === "user" ? "flex-row-reverse" : ""
                  }`}
                >
                  <div
                    className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 text-sm ${
                      msg.role === "user"
                        ? "bg-gradient-to-r from-cyan-400 to-fuchsia-500"
                        : "bg-gradient-to-r from-emerald-500 to-cyan-500"
                    }`}
                  >
                    {msg.role === "user" ? (
                      "👤"
                    ) : (
                      "🇩🇿"
                    )}
                  </div>
                  <div
                    className={`max-w-[75%] px-4 py-2 rounded-2xl text-sm ${
                      msg.role === "user"
                        ? "bg-gradient-to-r from-cyan-500 to-fuchsia-500 text-white"
                        : theme === "dark"
                        ? "bg-[#1a1a24] text-gray-200"
                        : "bg-gray-100 text-gray-800"
                    }`}
                  >
                    {msg.content}
                  </div>
                </motion.div>
              ))}

              {isLoading && (
                <div className="flex gap-3">
                  <div className="w-8 h-8 rounded-full bg-gradient-to-r from-emerald-500 to-cyan-500 flex items-center justify-center text-sm">
                    🇩🇿
                  </div>
                  <div
                    className={`px-4 py-3 rounded-2xl ${
                      theme === "dark" ? "bg-[#1a1a24]" : "bg-gray-100"
                    }`}
                  >
                    <Loader2 className="w-4 h-4 animate-spin text-emerald-500" />
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div
              className={`p-4 border-t ${
                theme === "dark" ? "border-[#2a2a35]" : "border-gray-200"
              }`}
            >
              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  handleSend();
                }}
                className="flex gap-2"
              >
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder={dziria.placeholder}
                  className={`flex-1 px-4 py-2 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400/50 ${
                    theme === "dark"
                      ? "bg-[#1a1a24] border border-[#2a2a35] text-white placeholder:text-gray-500"
                      : "bg-gray-100 text-gray-900 placeholder:text-gray-400"
                  }`}
                />
                <button
                  type="submit"
                  disabled={!input.trim() || isLoading}
                  className="w-10 h-10 rounded-xl bg-gradient-to-r from-emerald-500 to-cyan-500 flex items-center justify-center text-white disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-lg hover:shadow-emerald-500/30 transition-all"
                >
                  <Send className="w-4 h-4" />
                </button>
              </form>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
