// D:\iafactorychatgpt\dzir-ia\frontend\src\components\Layout.tsx
import React, { useEffect, useMemo, useState } from "react";
import { NavLink } from "react-router-dom";
import CopilotPanel from "./copilot/CopilotPanel";
import ThemeToggle from "./ThemeToggle";
import LanguageSwitcher from "./LanguageSwitcher";
import { useI18n } from "../lib/i18n";

export default function Layout({ children }: { children: React.ReactNode }) {
  const { t } = useI18n();
  const [sidebarCollapsed, setSidebarCollapsed] = useState<boolean>(() => {
    const v = localStorage.getItem("dziria_sidebar_collapsed");
    return v ? v === "1" : false;
  });

  const [copilotOpen, setCopilotOpen] = useState<boolean>(() => {
    const v = localStorage.getItem("dziria_copilot_open");
    return v ? v === "1" : false;
  });

  useEffect(() => {
    localStorage.setItem("dziria_sidebar_collapsed", sidebarCollapsed ? "1" : "0");
  }, [sidebarCollapsed]);

  useEffect(() => {
    localStorage.setItem("dziria_copilot_open", copilotOpen ? "1" : "0");
  }, [copilotOpen]);

  // Shortcuts:
  // Ctrl+B => sidebar
  // Ctrl+J => copilot
  // Esc => close copilot
  useEffect(() => {
    const onKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "b") {
        e.preventDefault();
        setSidebarCollapsed((s) => !s);
      }
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "j") {
        e.preventDefault();
        setCopilotOpen((s) => !s);
      }
      if (e.key === "Escape") {
        setCopilotOpen(false);
      }
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, []);

  const leftW = sidebarCollapsed ? 72 : 260;
  const rightW = copilotOpen ? 380 : 0;

  const shellStyle = useMemo<React.CSSProperties>(
    () => ({
      background: "var(--bg-primary)",
      color: "var(--text-primary)",
      display: "grid",
      gridTemplateColumns: `${leftW}px 1fr ${rightW}px`,
      height: "100vh",
      overflow: "hidden",
      width: "100%",
    }),
    [leftW, rightW]
  );

  return (
    <div style={shellStyle}>
      <style>{`
        .dziria-sidebar {
          background: var(--bg-secondary);
          color: var(--text-primary);
          border-right: 1px solid var(--border-color);
          display: flex;
          flex-direction: column;
          min-width: 0;
        }
        .dziria-sb-header {
          height: 56px;
          display: flex;
          align-items: center;
          gap: 10px;
          padding: 0 12px;
          border-bottom: 1px solid var(--border-color);
        }
        .dziria-brand {
          font-weight: 900;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }
        .dziria-toggle {
          margin-left: auto;
          border: 1px solid var(--border-color);
          background: var(--bg-tertiary);
          color: var(--text-primary);
          border-radius: 10px;
          padding: 6px 10px;
          cursor: pointer;
          font-weight: 900;
        }
        [dir="rtl"] .dziria-toggle { margin-left: 0; margin-right: auto; }
        .dziria-toggle:hover { border-color: rgba(0,166,81,.45); }

        .dziria-nav {
          padding: 10px;
          display: flex;
          flex-direction: column;
          gap: 8px;
        }
        .dziria-link {
          display: flex;
          align-items: center;
          gap: 10px;
          padding: 10px 12px;
          border-radius: 12px;
          border: 1px solid var(--border-color);
          text-decoration: none;
          color: var(--text-secondary);
          font-weight: 800;
        }
        .dziria-link:hover {
          background: var(--bg-tertiary);
          color: var(--text-primary);
        }
        .dziria-link.active {
          background: rgba(0,166,81,.16);
          border-color: rgba(0,166,81,.35);
          color: #00a651;
        }
        .dziria-icon {
          width: 26px;
          height: 26px;
          border-radius: 10px;
          display: grid;
          place-items: center;
          background: var(--bg-tertiary);
          border: 1px solid var(--border-color);
          flex-shrink: 0;
        }
        .dziria-label {
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }
        .collapsed .dziria-label { display: none; }

        .dziria-main {
          min-width: 0;
          display: flex;
          flex-direction: column;
          background: var(--bg-primary);
          color: var(--text-primary);
        }
        .dziria-topbar {
          height: 56px;
          display: flex;
          align-items: center;
          gap: 10px;
          padding: 0 12px;
          border-bottom: 1px solid var(--border-color);
          background: var(--bg-secondary);
          backdrop-filter: blur(10px);
        }
        .dziria-topbar-right {
          display: flex;
          align-items: center;
          gap: 8px;
          margin-left: auto;
        }
        [dir="rtl"] .dziria-topbar-right {
          margin-left: 0;
          margin-right: auto;
        }
        .dziria-btn {
          border: 1px solid var(--border-color);
          background: var(--bg-tertiary);
          color: var(--text-primary);
          border-radius: 10px;
          padding: 8px 10px;
          cursor: pointer;
          font-weight: 900;
        }
        .dziria-btn:hover { border-color: rgba(0,166,81,.45); }

        .dziria-content {
          flex: 1;
          min-height: 0;
          overflow: auto;
        }

        /* Copilot handle (quand fermé) */
        .dziria-copilot-handle {
          position: fixed;
          right: 0;
          top: 45%;
          transform: translateY(-50%);
          z-index: 9999;
          border-radius: 12px 0 0 12px;
          padding: 12px 10px;
          border: 1px solid var(--border-color);
          border-right: none;
          background: var(--bg-secondary);
          color: var(--text-primary);
          cursor: pointer;
          font-weight: 900;
          box-shadow: 0 10px 25px rgba(0,0,0,.25);
        }
        [dir="rtl"] .dziria-copilot-handle {
          right: auto;
          left: 0;
          border-radius: 0 12px 12px 0;
          border-left: none;
          border-right: 1px solid var(--border-color);
        }
        .dziria-copilot-handle:hover { border-color: rgba(0,166,81,.45); color: #00a651; }

        .dziria-copilot {
          border-left: 1px solid var(--border-color);
          min-width: 0;
          background: var(--bg-secondary);
        }
        [dir="rtl"] .dziria-copilot {
          border-left: none;
          border-right: 1px solid var(--border-color);
        }
      `}</style>

      {/* LEFT: Sidebar (jamais 0px => jamais perdue) */}
      <aside className={`dziria-sidebar ${sidebarCollapsed ? "collapsed" : ""}`}>
        <div className="dziria-sb-header">
          <div className="dziria-brand">{sidebarCollapsed ? "D" : "Dzir IA"}</div>
          <button
            className="dziria-toggle"
            onClick={() => setSidebarCollapsed((s) => !s)}
            title="Toggle Sidebar (Ctrl+B)"
          >
            {sidebarCollapsed ? "›" : "‹"}
          </button>
        </div>

        <nav className="dziria-nav">
          <NavLink className={({ isActive }) => `dziria-link ${isActive ? "active" : ""}`} to="/chat">
            <span className="dziria-icon">💬</span>
            <span className="dziria-label">{t('nav.chat')}</span>
          </NavLink>

          <NavLink className={({ isActive }) => `dziria-link ${isActive ? "active" : ""}`} to="/collections">
            <span className="dziria-icon">📁</span>
            <span className="dziria-label">{t('nav.collections')}</span>
          </NavLink>

          <NavLink className={({ isActive }) => `dziria-link ${isActive ? "active" : ""}`} to="/search">
            <span className="dziria-icon">🔎</span>
            <span className="dziria-label">{t('nav.search')}</span>
          </NavLink>

          <NavLink className={({ isActive }) => `dziria-link ${isActive ? "active" : ""}`} to="/timeline">
            <span className="dziria-icon">🕒</span>
            <span className="dziria-label">{t('nav.timeline')}</span>
          </NavLink>

          <NavLink className={({ isActive }) => `dziria-link ${isActive ? "active" : ""}`} to="/graph">
            <span className="dziria-icon">🧠</span>
            <span className="dziria-label">{t('nav.graph')}</span>
          </NavLink>
        </nav>
      </aside>

      {/* CENTER */}
      <div className="dziria-main">
        <div className="dziria-topbar">
          <button className="dziria-btn" onClick={() => setSidebarCollapsed(false)} title="Open Sidebar">
            ☰
          </button>

          <div style={{ fontWeight: 900, opacity: 0.9 }}>{t('app.name')}</div>

          <div className="dziria-topbar-right">
            <div style={{ fontSize: 12, opacity: 0.7 }}>
              {t('copilot.hint')}
            </div>
            <ThemeToggle />
            <LanguageSwitcher />
          </div>
        </div>

        <div className="dziria-content">{children}</div>
      </div>

      {/* RIGHT: Copilot */}
      {copilotOpen ? (
        <aside className="dziria-copilot">
          <CopilotPanel onClose={() => setCopilotOpen(false)} />
        </aside>
      ) : (
        <button
          className="dziria-copilot-handle"
          onClick={() => setCopilotOpen(true)}
          title="Open Copilot (Ctrl+J)"
        >
          {t('copilot.title')}
        </button>
      )}
    </div>
  );
}
