import React, { useState } from 'react';

type ChatMode = 'chat' | 'rag' | 'support';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export function HelpChatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [message, setMessage] = useState("");
  const [mode, setMode] = useState<ChatMode>("chat");
  const [ragSelection, setRagSelection] = useState("DZ");
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "Bonjour ! Je suis <strong>Dzir IA</strong>, votre assistant IAFactory Algeria. Comment puis-je vous aider ?",
    },
  ]);

  const toggleHelpWindow = () => {
    setIsOpen(!isOpen);
  };

  const setHelpMode = (newMode: ChatMode) => {
    setMode(newMode);
  };

  const sendHelpMessage = async () => {
    if (!message.trim()) return;

    const userMessage = message;
    setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
    setMessage("");

    // API call based on mode
    try {
      let response = "";

      if (mode === "chat") {
        // Call AI chat endpoint
        const res = await fetch('/api/help-chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: userMessage })
        });
        if (res.ok) {
          const data = await res.json();
          response = data.response || "Je suis le chatbot d'aide IA. Comment puis-je vous assister ?";
        } else {
          response = "Je suis en mode demo. Bientot, je pourrai vous aider avec vos questions !";
        }
      } else if (mode === "rag") {
        // Call RAG endpoint
        const res = await fetch('/api/query', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: userMessage, country: ragSelection })
        });
        if (res.ok) {
          const data = await res.json();
          response = data.answer || `Recherche RAG pour ${ragSelection}: ${data.results?.length || 0} resultats trouves.`;
        } else {
          response = `Recherche RAG activee pour ${ragSelection}. Fonctionnalite en cours de developpement...`;
        }
      } else {
        response = "Mode support humain active. Un agent humain vous repondra bientot.";
      }

      setMessages((prev) => [...prev, { role: "assistant", content: response }]);
    } catch (error) {
      setMessages((prev) => [...prev, {
        role: "assistant",
        content: "Desolee, une erreur s'est produite. Veuillez reessayer."
      }]);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      sendHelpMessage();
    }
  };

  return (
    <div className="help-bubble" id="helpBubble">
      <span className="help-label">Dzir IA - Aide</span>
      <button className="help-btn" onClick={toggleHelpWindow}>
        <img
          src="/assets/images/lala-fatma.png"
          alt="Dzir IA"
          style={{width: '28px', height: '28px', borderRadius: '50%', objectFit: 'cover'}}
          onError={(e) => { (e.target as HTMLImageElement).src = '/favicon.png'; }}
        />
      </button>

      {isOpen && (
        <div className="help-window open">
          {/* Header */}
          <div className="help-header">
            <h3>
              <img
                src="/assets/images/lala-fatma.png"
                alt="Dzir IA"
                style={{width: '24px', height: '24px', borderRadius: '50%', objectFit: 'cover', verticalAlign: 'middle', marginRight: '8px'}}
                onError={(e) => { (e.target as HTMLImageElement).src = '/favicon.png'; }}
              />
              Dzir IA
            </h3>
            <button className="close-help-btn" onClick={toggleHelpWindow}>
              &times;
            </button>
          </div>

          {/* 3 MODES : Chat IA / Recherche RAG / Support */}
          <div className="help-modes">
            <button
              className={`help-mode-btn ${mode === "chat" ? "active" : ""}`}
              onClick={() => setHelpMode("chat")}
            >
              💬 Chat IA
            </button>
            <button
              className={`help-mode-btn ${mode === "rag" ? "active" : ""}`}
              onClick={() => setHelpMode("rag")}
            >
              🔍 RAG
            </button>
            <button
              className={`help-mode-btn ${mode === "support" ? "active" : ""}`}
              onClick={() => setHelpMode("support")}
            >
              📞 Support
            </button>
          </div>

          {/* RAG Selector */}
          {mode === "rag" && (
            <div className="help-rag-selector">
              <select
                value={ragSelection}
                onChange={(e) => setRagSelection(e.target.value)}
              >
                <option value="DZ">🇩🇿 Business DZ (Algerie)</option>
                <option value="CH">🎓 Ecole (Suisse)</option>
                <option value="GLOBAL">🕌 Islam (Global)</option>
                <option value="ALL">🌍 Tous les RAG</option>
              </select>
            </div>
          )}

          {/* Support Banner */}
          {mode === "support" && (
            <div className="help-support-banner">
              ⚠️ Mode support humain active
              <br />
              <button onClick={() => setHelpMode("chat")}>
                <img
                  src="/assets/images/lala-fatma.png"
                  alt="Dzir IA"
                  style={{width: '18px', height: '18px', borderRadius: '50%', objectFit: 'cover', verticalAlign: 'middle', marginRight: '4px'}}
                  onError={(e) => { (e.target as HTMLImageElement).src = '/favicon.png'; }}
                />
                Revenir au mode IA
              </button>
            </div>
          )}

          {/* Messages */}
          <div className="help-messages">
            {messages.map((msg, i) => (
              <div
                key={i}
                className={`help-message ${msg.role === "user" ? "help-user" : "help-bot"}`}
              >
                {msg.role === "assistant" && (
                  <div className="help-avatar">
                    <img
                      src="/assets/images/lala-fatma.png"
                      alt="Dzir IA"
                      style={{width: '32px', height: '32px', borderRadius: '50%', objectFit: 'cover', boxShadow: '0 2px 8px rgba(0,132,61,0.3)'}}
                      onError={(e) => { (e.target as HTMLImageElement).src = '/favicon.png'; }}
                    />
                  </div>
                )}
                <div
                  className="help-bubble-msg"
                  dangerouslySetInnerHTML={{ __html: msg.content }}
                />
              </div>
            ))}
          </div>

          {/* Input */}
          <div className="help-input">
            <input
              type="text"
              placeholder="Tapez votre message..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={handleKeyPress}
            />
            <button className="help-send-btn" onClick={sendHelpMessage}>
              ➤
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default HelpChatbot;
