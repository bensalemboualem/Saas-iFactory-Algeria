// ============================================================
// IA FACTORY - INTERVIEW AGENTS - INTERVIEW CHAT COMPONENT
// Styled to match IAFactory branding
// ============================================================

"use client";

import React, { useState, useRef, useEffect } from "react";
import { InterviewPhase } from "../types/interview";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  phase?: string;
}

interface InterviewChatProps {
  agentId: string;
  agentName: string;
  agentIcon: string;
  agentColor: string;
  systemPrompt: string;
  phases: InterviewPhase[];
  onComplete?: (report: string) => void;
}

export default function InterviewChat({
  agentId,
  agentName,
  agentIcon,
  agentColor,
  systemPrompt,
  phases,
  onComplete,
}: InterviewChatProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [currentPhase, setCurrentPhase] = useState(phases[0]?.id || "");
  const [isComplete, setIsComplete] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [report, setReport] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    initializeConversation();
  }, [agentId]);

  const initializeConversation = async () => {
    setIsLoading(true);
    try {
      const response = await fetch("/api/interview", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ agentId, action: "start", systemPrompt }),
      });
      const data = await response.json();

      if (data.message) {
        setSessionId(data.sessionId);
        setMessages([
          {
            id: Date.now().toString(),
            role: "assistant",
            content: data.message,
            timestamp: new Date(),
            phase: currentPhase,
          },
        ]);
      }
    } catch (error) {
      console.error("Failed to initialize:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input.trim(),
      timestamp: new Date(),
      phase: currentPhase,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await fetch("/api/interview", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          agentId,
          action: "message",
          message: userMessage.content,
          sessionId,
          systemPrompt,
        }),
      });
      const data = await response.json();

      if (data.message) {
        setMessages((prev) => [
          ...prev,
          {
            id: Date.now().toString(),
            role: "assistant",
            content: data.message,
            timestamp: new Date(),
            phase: data.phase || currentPhase,
          },
        ]);

        if (data.phase) setCurrentPhase(data.phase);
        if (data.isComplete) setIsComplete(true);
      }
    } catch (error) {
      console.error("Failed to send:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const generateReport = async () => {
    setIsLoading(true);
    try {
      const response = await fetch("/api/interview", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          agentId,
          action: "report",
          messages: messages.map((m) => ({ role: m.role, content: m.content })),
          systemPrompt,
        }),
      });
      const data = await response.json();
      if (data.report) {
        setReport(data.report);
        onComplete?.(data.report);
      }
    } catch (error) {
      console.error("Failed to generate report:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const getCurrentPhaseIndex = () => phases.findIndex((p) => p.id === currentPhase);

  return (
    <div
      className="flex flex-col h-full rounded-xl overflow-hidden shadow-lg"
      style={{
        background: "#020617",
        border: "1px solid rgba(255, 255, 255, 0.12)"
      }}
    >
      {/* Header */}
      <div
        className="px-4 py-3 flex items-center justify-between"
        style={{
          background: "linear-gradient(135deg, #00a651 0%, #008c45 100%)"
        }}
      >
        <div className="flex items-center gap-3">
          <span className="text-2xl">{agentIcon}</span>
          <div>
            <h2 className="font-semibold text-white">{agentName}</h2>
            <p className="text-xs text-white/80">{phases[getCurrentPhaseIndex()]?.name}</p>
          </div>
        </div>
        <div className="text-white/90 text-sm">
          Phase {getCurrentPhaseIndex() + 1}/{phases.length}
        </div>
      </div>

      {/* Progress Bar */}
      <div className="h-1" style={{ background: "rgba(255, 255, 255, 0.05)" }}>
        <div
          className="h-full transition-all duration-300"
          style={{
            width: `${((getCurrentPhaseIndex() + 1) / phases.length) * 100}%`,
            background: "#00a651",
          }}
        />
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex gap-3 ${message.role === "user" ? "flex-row-reverse" : ""}`}
          >
            <div
              className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0`}
              style={
                message.role === "user"
                  ? { background: "#00a651", color: "#021014" }
                  : { background: "#00a651", color: "white" }
              }
            >
              {message.role === "user" ? "👤" : agentIcon}
            </div>
            <div
              className={`max-w-[75%] rounded-2xl px-4 py-2`}
              style={
                message.role === "user"
                  ? { background: "#00a651", color: "#021014" }
                  : {
                      background: "rgba(255, 255, 255, 0.05)",
                      border: "1px solid rgba(255, 255, 255, 0.1)",
                      color: "#f8fafc"
                    }
              }
            >
              <p className="whitespace-pre-wrap">{message.content}</p>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex gap-3">
            <div
              className="w-8 h-8 rounded-full flex items-center justify-center text-white"
              style={{ background: "#00a651" }}
            >
              {agentIcon}
            </div>
            <div
              className="rounded-2xl px-4 py-3"
              style={{
                background: "rgba(255, 255, 255, 0.05)",
                border: "1px solid rgba(255, 255, 255, 0.1)"
              }}
            >
              <div className="animate-pulse" style={{ color: "rgba(248, 250, 252, 0.75)" }}>
                ⏳ En train d'écrire...
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Report Modal */}
      {report && (
        <div
          className="absolute inset-0 flex items-center justify-center p-4 z-50"
          style={{ background: "rgba(0, 0, 0, 0.8)" }}
        >
          <div
            className="rounded-xl max-w-2xl w-full max-h-[80vh] flex flex-col"
            style={{
              background: "#020617",
              border: "1px solid rgba(0, 166, 81, 0.3)"
            }}
          >
            <div
              className="p-4 flex items-center justify-between"
              style={{ borderBottom: "1px solid rgba(255, 255, 255, 0.12)" }}
            >
              <h3 className="font-semibold" style={{ color: "#f8fafc" }}>
                📋 Rapport d'Interview
              </h3>
              <button
                onClick={() => {
                  const blob = new Blob([report], { type: "text/markdown" });
                  const url = URL.createObjectURL(blob);
                  const a = document.createElement("a");
                  a.href = url;
                  a.download = `${agentId}-report-${Date.now()}.md`;
                  a.click();
                }}
                className="px-3 py-1.5 rounded-lg text-sm transition"
                style={{
                  background: "#00a651",
                  color: "#021014"
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.background = "#008c45";
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background = "#00a651";
                }}
              >
                📥 Télécharger
              </button>
            </div>
            <div className="flex-1 overflow-y-auto p-4">
              <pre
                className="whitespace-pre-wrap text-sm"
                style={{ color: "#f8fafc" }}
              >
                {report}
              </pre>
            </div>
            <div
              className="p-4"
              style={{ borderTop: "1px solid rgba(255, 255, 255, 0.12)" }}
            >
              <button
                onClick={() => setReport(null)}
                className="w-full py-2 rounded-lg transition"
                style={{
                  background: "rgba(255, 255, 255, 0.05)",
                  border: "1px solid rgba(255, 255, 255, 0.1)",
                  color: "#f8fafc"
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.background = "rgba(255, 255, 255, 0.08)";
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background = "rgba(255, 255, 255, 0.05)";
                }}
              >
                Fermer
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Input Area */}
      <div
        className="p-4"
        style={{
          borderTop: "1px solid rgba(255, 255, 255, 0.12)",
          background: "rgba(0, 0, 0, 0.2)"
        }}
      >
        {isComplete ? (
          <button
            onClick={generateReport}
            disabled={isLoading}
            className="w-full py-3 rounded-xl font-medium transition-all duration-300"
            style={{
              background: isLoading ? "rgba(0, 166, 81, 0.5)" : "#00a651",
              color: "#021014",
              cursor: isLoading ? "not-allowed" : "pointer"
            }}
            onMouseEnter={(e) => {
              if (!isLoading) {
                e.currentTarget.style.transform = "translateY(-1px)";
                e.currentTarget.style.boxShadow = "0 4px 12px rgba(0, 166, 81, 0.4)";
              }
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = "translateY(0)";
              e.currentTarget.style.boxShadow = "none";
            }}
          >
            {isLoading ? "⏳ Génération..." : "📋 Générer le Rapport"}
          </button>
        ) : (
          <div className="flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
              placeholder="Votre réponse..."
              disabled={isLoading}
              className="flex-1 px-4 py-3 rounded-xl transition"
              style={{
                background: "rgba(255, 255, 255, 0.05)",
                border: "1px solid rgba(255, 255, 255, 0.12)",
                color: "#f8fafc",
                outline: "none"
              }}
              onFocus={(e) => {
                e.currentTarget.style.borderColor = "#00a651";
              }}
              onBlur={(e) => {
                e.currentTarget.style.borderColor = "rgba(255, 255, 255, 0.12)";
              }}
            />
            <button
              onClick={sendMessage}
              disabled={!input.trim() || isLoading}
              className="px-4 py-3 rounded-xl transition"
              style={{
                background: !input.trim() || isLoading ? "rgba(0, 166, 81, 0.3)" : "#00a651",
                color: !input.trim() || isLoading ? "rgba(2, 16, 20, 0.5)" : "#021014",
                cursor: !input.trim() || isLoading ? "not-allowed" : "pointer"
              }}
              onMouseEnter={(e) => {
                if (input.trim() && !isLoading) {
                  e.currentTarget.style.background = "#008c45";
                }
              }}
              onMouseLeave={(e) => {
                if (input.trim() && !isLoading) {
                  e.currentTarget.style.background = "#00a651";
                }
              }}
            >
              {isLoading ? "⏳" : "➤"}
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
