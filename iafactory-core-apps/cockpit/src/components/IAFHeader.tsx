import { useState, useEffect } from 'react';

type Lang = 'fr' | 'en' | 'ar';

interface IAFHeaderProps {
  lang: Lang;
}

export default function IAFHeader({ lang }: IAFHeaderProps) {
  void lang; // Used in future translations
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // Prevent body scroll when mobile menu open
  useEffect(() => {
    document.body.style.overflow = mobileMenuOpen ? 'hidden' : '';
    return () => { document.body.style.overflow = ''; };
  }, [mobileMenuOpen]);

  return (
    <header className="iaf-header" role="banner">
      <div className="iaf-header-container">
        <div className="header-logo" dir="ltr">
          {/* IAFactory Algeria Logo - Contour Neural */}
          <svg width="48" height="48" viewBox="0 0 100 100" style={{ marginRight: '10px' }}>
            <style>{`
              @keyframes pulse {
                0%, 100% { r: 5; opacity: 1; }
                50% { r: 7; opacity: 0.7; }
              }
              @keyframes pulse2 {
                0%, 100% { r: 5; opacity: 0.7; }
                50% { r: 7; opacity: 1; }
              }
              .node1 { animation: pulse 2s ease-in-out infinite; }
              .node2 { animation: pulse2 2s ease-in-out infinite 0.25s; }
              .node3 { animation: pulse 2s ease-in-out infinite 0.5s; }
              .node4 { animation: pulse2 2s ease-in-out infinite 0.75s; }
              .node5 { animation: pulse 2s ease-in-out infinite 1s; }
              .node6 { animation: pulse2 2s ease-in-out infinite 1.25s; }
              .node7 { animation: pulse 2s ease-in-out infinite 1.5s; }
              .node8 { animation: pulse2 2s ease-in-out infinite 1.75s; }
            `}</style>

            {/* Connexions neurales (lignes entre les noeuds) */}
            <line x1="50" y1="5" x2="85" y2="20" stroke="#00a651" strokeWidth="2"/>
            <line x1="85" y1="20" x2="95" y2="50" stroke="#00a651" strokeWidth="2"/>
            <line x1="95" y1="50" x2="85" y2="80" stroke="#00a651" strokeWidth="2"/>
            <line x1="85" y1="80" x2="50" y2="95" stroke="#00a651" strokeWidth="2"/>
            <line x1="50" y1="95" x2="15" y2="80" stroke="#00a651" strokeWidth="2"/>
            <line x1="15" y1="80" x2="5" y2="50" stroke="#00a651" strokeWidth="2"/>
            <line x1="5" y1="50" x2="15" y2="20" stroke="#00a651" strokeWidth="2"/>
            <line x1="15" y1="20" x2="50" y2="5" stroke="#00a651" strokeWidth="2"/>

            {/* Noeuds neuronaux animes - alternance vert/rouge */}
            <circle cx="50" cy="5" r="5" fill="#00a651" className="node1"/>
            <circle cx="85" cy="20" r="5" fill="#ef4444" className="node2"/>
            <circle cx="95" cy="50" r="5" fill="#00a651" className="node3"/>
            <circle cx="85" cy="80" r="5" fill="#ef4444" className="node4"/>
            <circle cx="50" cy="95" r="5" fill="#00a651" className="node5"/>
            <circle cx="15" cy="80" r="5" fill="#ef4444" className="node6"/>
            <circle cx="5" cy="50" r="5" fill="#00a651" className="node7"/>
            <circle cx="15" cy="20" r="5" fill="#ef4444" className="node8"/>

            {/* Fond vert pour iAF */}
            <circle cx="50" cy="50" r="32" fill="#00a651"/>

            {/* Lettres iAF au centre */}
            <text x="50" y="52" fontFamily="Arial Black, sans-serif" fontSize="28" fontWeight="900" textAnchor="middle" dominantBaseline="middle" fill="white">
              <tspan fontSize="22">i</tspan><tspan fontSize="28">AF</tspan>
            </text>
          </svg>
          <span className="logo-text" style={{ fontSize: '16px', position: 'relative', display: 'inline-block' }}>
            <span style={{ position: 'relative', display: 'inline-block', overflow: 'hidden' }}>
              <span className="letter i-bounce" style={{ color: '#00a651' }}>i</span>
              <span className="letter" style={{ color: '#00a651' }}>A</span>
              <span className="letter" style={{ color: 'var(--text)' }}>F</span>
              <span className="letter" style={{ color: 'var(--text)' }}>a</span>
              <span className="letter" style={{ color: 'var(--text)' }}>c</span>
              <span className="letter" style={{ color: 'var(--text)' }}>t</span>
              <span className="letter" style={{ color: 'var(--text)' }}>o</span>
              <span className="letter" style={{ color: '#ef4444', animation: 'bounce 1.5s ease-in-out infinite' }}>r</span>
              <span className="letter" style={{ color: '#ef4444', animation: 'bounce 1.5s ease-in-out infinite 0.15s' }}>y</span>
            </span>
            <span> </span>
            <span style={{ position: 'relative', display: 'inline-block', overflow: 'hidden' }}>
              <span className="letter" style={{ color: 'var(--text)' }}>A</span>
              <span className="letter" style={{ color: 'var(--text)' }}>l</span>
              <span className="letter" style={{ color: 'var(--text)' }}>g</span>
              <span className="letter" style={{ color: 'var(--text)' }}>e</span>
              <span className="letter" style={{ color: 'var(--text)' }}>r</span>
              <span className="letter i-bounce" style={{ color: '#00a651' }}>i</span>
              <span className="letter" style={{ color: '#00a651' }}>a</span>
            </span>
          </span>
        </div>
        <nav className="iaf-nav" role="navigation">
          <a href="/index.html" className="iaf-nav-link"><i className="fa-solid fa-home iaf-nav-icon"></i><span>Accueil</span></a>
          <a href="/apps.html" className="iaf-nav-link"><i className="fa-solid fa-th iaf-nav-icon"></i><span>Applications</span></a>
          <a href="/docs/directory/agents.html" className="iaf-nav-link"><i className="fa-solid fa-robot iaf-nav-icon"></i><span>Agents IA</span></a>
          <a href="/workflows.html" className="iaf-nav-link"><i className="fa-solid fa-diagram-project iaf-nav-icon"></i><span>Workflows</span></a>
        </nav>

        {/* Mobile Menu Button */}
        <button
          className={`iaf-mobile-menu-btn ${mobileMenuOpen ? 'active' : ''}`}
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          aria-label="Menu mobile"
          aria-expanded={mobileMenuOpen}
        >
          <span className="iaf-burger-line"></span>
          <span className="iaf-burger-line"></span>
          <span className="iaf-burger-line"></span>
        </button>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="iaf-mobile-menu open">
          <nav className="iaf-mobile-nav">
            <a href="/index.html" className="iaf-mobile-link" onClick={() => setMobileMenuOpen(false)}>
              <i className="fa-solid fa-home"></i> Accueil
            </a>
            <a href="/apps.html" className="iaf-mobile-link" onClick={() => setMobileMenuOpen(false)}>
              <i className="fa-solid fa-th"></i> Applications
            </a>
            <a href="/docs/directory/agents.html" className="iaf-mobile-link" onClick={() => setMobileMenuOpen(false)}>
              <i className="fa-solid fa-robot"></i> Agents IA
            </a>
            <a href="/workflows.html" className="iaf-mobile-link" onClick={() => setMobileMenuOpen(false)}>
              <i className="fa-solid fa-diagram-project"></i> Workflows
            </a>
          </nav>
        </div>
      )}
    </header>
  );
}
