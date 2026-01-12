"use client"

import * as React from "react"

export function HelpChatbot() {
  const [isOpen, setIsOpen] = React.useState(false)
  const [message, setMessage] = React.useState("")
  const [mode, setMode] = React.useState<"chat" | "rag" | "support">("chat")
  const [ragSelection, setRagSelection] = React.useState("DZ")
  const [messages, setMessages] = React.useState<
    Array<{ role: "user" | "assistant"; content: string }>
  >([
    {
      role: "assistant",
      content:
        "👋 Bonjour ! Je suis <strong>Dzir IA</strong>, votre assistant IAFactory Algeria. Comment puis-je vous aider ?",
    },
  ])

  const toggleHelpWindow = () => {
    setIsOpen(!isOpen)
  }

  const setHelpMode = (newMode: "chat" | "rag" | "support") => {
    setMode(newMode)
  }

  const sendHelpMessage = () => {
    if (!message.trim()) return

    setMessages((prev) => [...prev, { role: "user", content: message }])

    // Simulate AI response based on mode
    setTimeout(() => {
      let response = ""
      if (mode === "chat") {
        response =
          "Je suis le chatbot d'aide IA. Pour l'instant, je suis en mode démo. Bientôt, je pourrai vous aider avec vos questions sur les générateurs vidéo, les templates, et plus encore !"
      } else if (mode === "rag") {
        response = `Recherche RAG activée pour ${
          ragSelection === "DZ"
            ? "Business DZ (Algérie)"
            : ragSelection === "CH"
            ? "École (Suisse)"
            : ragSelection === "GLOBAL"
            ? "Islam (Global)"
            : "Tous les RAG"
        }. Fonctionnalité en cours de développement...`
      } else {
        response =
          "Mode support humain activé. Un agent humain vous répondra bientôt. En attendant, essayez le mode IA !"
      }

      setMessages((prev) => [...prev, { role: "assistant", content: response }])
    }, 500)

    setMessage("")
  }

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      sendHelpMessage()
    }
  }

  return (
    <div className="iaf-chatbot-bubble" id="iaf-chatbot-bubble">
      <span className="iaf-chatbot-label">Dzir IA - Aide</span>
      <button className="iaf-chatbot-btn" onClick={toggleHelpWindow}>
        💬
      </button>

      {isOpen && (
        <div className="iaf-chatbot-window show">
          {/* Header */}
          <div className="iaf-chatbot-header">
            <h3>🤖 Dzir IA</h3>
            <button className="iaf-chatbot-close-btn" onClick={toggleHelpWindow}>
              ×
            </button>
          </div>

          {/* 3 MODES : Chat IA / Recherche RAG / Support */}
          <div className="iaf-chatbot-modes">
            <button
              className={`iaf-chatbot-mode-btn ${mode === "chat" ? "active" : ""}`}
              onClick={() => setHelpMode("chat")}
            >
              💬 Chat IA
            </button>
            <button
              className={`iaf-chatbot-mode-btn ${mode === "rag" ? "active" : ""}`}
              onClick={() => setHelpMode("rag")}
            >
              🔍 Recherche RAG
            </button>
            <button
              className={`iaf-chatbot-mode-btn ${mode === "support" ? "active" : ""}`}
              onClick={() => setHelpMode("support")}
            >
              📞 Support
            </button>
          </div>

          {/* SÉLECTEUR RAG (affiché en mode Recherche) */}
          {mode === "rag" && (
            <div className="iaf-chatbot-rag-selector" style={{ padding: "12px" }}>
              <select
                value={ragSelection}
                onChange={(e) => setRagSelection(e.target.value)}
                style={{
                  width: "100%",
                  padding: "8px 12px",
                  borderRadius: "8px",
                  border: "1px solid var(--border)",
                  background: "var(--background)",
                  color: "var(--foreground)",
                  fontSize: "14px",
                }}
              >
                <option value="DZ">🇩🇿 Business DZ (Algérie)</option>
                <option value="CH">🎓 École (Suisse)</option>
                <option value="GLOBAL">🕌 Islam (Global)</option>
                <option value="ALL">🌍 Tous les RAG</option>
              </select>
            </div>
          )}

          {/* BANNER SUPPORT (affiché en mode Support) */}
          {mode === "support" && (
            <div
              className="iaf-chatbot-support-banner"
              style={{
                padding: "12px",
                background: "rgba(234, 179, 8, 0.1)",
                borderBottom: "1px solid var(--border)",
                textAlign: "center",
                fontSize: "14px",
                color: "var(--foreground)",
              }}
            >
              ⚠️ Mode support humain activé
              <br />
              <button
                onClick={() => setHelpMode("chat")}
                style={{
                  marginTop: "8px",
                  padding: "6px 12px",
                  borderRadius: "6px",
                  border: "none",
                  background: "var(--primary)",
                  color: "white",
                  fontSize: "13px",
                  cursor: "pointer",
                }}
              >
                🤖 Revenir au mode IA
              </button>
            </div>
          )}

          {/* MESSAGES */}
          <div className="iaf-chatbot-messages">
            {messages.map((msg, i) => (
              <div
                key={i}
                className={`iaf-chatbot-message ${
                    msg.role === "user" ? "iaf-chatbot-user" : "iaf-chatbot-bot"
                  }`}
              >
                {msg.role === "assistant" && (
                  <div className="iaf-chatbot-avatar">
                    <div
                      style={{
                        width: "32px",
                        height: "32px",
                        background:
                          "linear-gradient(135deg, #00843D 0%, #2ecc71 100%)",
                        color: "white",
                        borderRadius: "8px",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        fontWeight: "bold",
                        fontSize: "11px",
                        boxShadow: "0 2px 8px rgba(0,132,61,0.3)",
                      }}
                    >
                      DZ
                    </div>
                  </div>
                )}
                <div
                  className="iaf-chatbot-bubble-msg"
                  dangerouslySetInnerHTML={{ __html: msg.content }}
                />
              </div>
            ))}
          </div>

          {/* INPUT */}
          <div className="iaf-chatbot-input">
            <input
              type="text"
              placeholder="Tapez votre message..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={handleKeyPress}
            />
            <button className="iaf-chatbot-send-btn" onClick={sendHelpMessage}>
              ➤
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
