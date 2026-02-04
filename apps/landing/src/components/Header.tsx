import { useRef, useState, useCallback, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useTranslation } from '../i18n';
import { useTheme } from '../hooks';
import './Header.css';

const Header = () => {
  const { t, lang, changeLanguage } = useTranslation();
  const { isDark, colors, accent, toggleTheme } = useTheme();
  const [menuOpen, setMenuOpen] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();
  const location = useLocation();

  const navLinks = [
    { label: t('home'), to: '/' },
    { label: t('solutions'), anchorId: 'solutions' },
    { label: t('pricing'), to: '/pricing' },
    { label: t('tools'), to: '/tools' },
    { label: t('apps'), to: '/apps' },
    { label: t('agents'), to: '/agents' },
    { label: t('workflows'), to: '/workflows' },
    { label: t('b2b'), to: '/b2b' },
  ];

  const menuLinks = [
    { href: './docs/getstarted.html', icon: '🚀', label: t('get_started') },
    { href: './docs/documentation.html', icon: '📖', label: t('docs') },
    { href: './docs/help.html', icon: '💬', label: t('help_center') },
    { href: './docs/changelog.html', icon: '📋', label: t('changelog') },
    { href: './docs/blog.html', icon: '📝', label: t('blog') },
  ];

  const menuLinksPro = [
    { href: './docs/pro.html', icon: '⭐', label: t('iafactory_pro') },
    { icon: '🏢', label: t('enterprise'), to: '/b2b' },
    { icon: '🔌', label: t('api'), href: './docs/api.html' },
  ];

  const languages = [
    { code: 'fr', label: 'Français' },
    { code: 'en', label: 'English' },
    { code: 'ar', label: 'العربية' },
  ];

  useEffect(() => {
    const onClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setMenuOpen(false);
      }
    };
    document.addEventListener('mousedown', onClickOutside);
    return () => document.removeEventListener('mousedown', onClickOutside);
  }, []);

  const handleLanguageChange = useCallback((newLang: string) => {
    changeLanguage(newLang as 'fr' | 'ar' | 'en');
  }, [changeLanguage]);

  const handleNavClick = useCallback((to?: string) => {
    if (to) {
      navigate(to);
      setMenuOpen(false);
      setMobileMenuOpen(false);
      window.scrollTo(0, 0);
    }
  }, [navigate]);

  const handleAnchorClick = useCallback(
    (anchorId: string) => {
      setMenuOpen(false);
      setMobileMenuOpen(false);
      const scrollToAnchor = () => {
        const target = document.getElementById(anchorId);
        if (target) {
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
          window.history.replaceState(null, '', `/#${anchorId}`);
        }
      };
      if (location.pathname !== '/') {
        navigate('/');
        setTimeout(scrollToAnchor, 80);
      } else {
        scrollToAnchor();
      }
    },
    [location.pathname, navigate]
  );

  const logoSrc = '/assets/images/logo-iafactory.png';

  const glassBg = isDark
    ? 'rgba(20, 20, 20, 0.7)'
    : 'rgba(255, 255, 255, 0.72)';

  const glassBorder = isDark
    ? '1px solid rgba(255, 255, 255, 0.06)'
    : '1px solid rgba(0, 0, 0, 0.06)';

  return (
    <>
      <header
        className="header-glass"
        style={{ background: glassBg, borderBottom: glassBorder }}
      >
        <nav className="header-nav" aria-label="Navigation principale">
          {/* Logo */}
          <Link to="/" className="header-logo" aria-label="IA Factory Algeria - Accueil">
            <img alt="IA Factory Algeria" src={logoSrc} />
          </Link>

          {/* Desktop Nav Links */}
          <div className="header-links" role="navigation" aria-label="Liens de navigation">
            {navLinks
              .filter((link) => (link.to ? link.to !== location.pathname : true))
              .map((link) =>
                link.anchorId ? (
                  <button
                    key={link.anchorId}
                    type="button"
                    className="header-link"
                    onClick={() => handleAnchorClick(link.anchorId)}
                    style={{ color: colors.textMuted }}
                  >
                    {link.label}
                  </button>
                ) : (
                  <Link
                    key={link.to ?? link.anchorId}
                    to={link.to!}
                    className="header-link"
                    style={{ color: colors.textMuted }}
                  >
                    {link.label}
                  </Link>
                )
              )}
          </div>

          {/* Right Side */}
          <div className="header-right">
            {/* Menu 3 dots */}
            <div ref={menuRef} style={{ position: 'relative' }}>
              <button
                type="button"
                onClick={() => setMenuOpen(!menuOpen)}
                className="header-menu-btn desktop-only"
                aria-label="Ouvrir le menu des paramètres"
                aria-expanded={menuOpen}
                aria-haspopup="true"
                style={{
                  background: isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.04)',
                  border: glassBorder,
                  color: colors.textMuted,
                }}
              >
                ⋮
              </button>

              {/* Dropdown Menu */}
              {menuOpen && (
                <div
                  className="header-dropdown"
                  role="menu"
                  aria-label="Menu des paramètres"
                  style={{
                    background: isDark ? 'rgba(23, 23, 23, 0.95)' : 'rgba(255, 255, 255, 0.95)',
                    border: `1px solid ${colors.borderColor}`,
                    boxShadow: isDark
                      ? '0 8px 32px rgba(0, 0, 0, 0.5)'
                      : '0 8px 32px rgba(0, 0, 0, 0.1)',
                  }}
                >
                  {/* Theme Toggle */}
                  <div className="header-dropdown-row">
                    <span style={{ color: colors.textPrimary, fontSize: '14px' }}>
                      {t('dark_theme')}
                    </span>
                    <button
                      type="button"
                      onClick={toggleTheme}
                      className="header-toggle"
                      role="switch"
                      aria-checked={isDark}
                      aria-label="Activer/désactiver le thème sombre"
                      style={{ background: isDark ? accent.primary : '#d1d5db' }}
                    >
                      <span
                        className="header-toggle-knob"
                        style={{ left: isDark ? '22px' : '2px' }}
                      />
                    </button>
                  </div>

                  {/* Language Selector */}
                  <div className="header-dropdown-row">
                    <label htmlFor="language-select" style={{ color: colors.textPrimary, fontSize: '14px' }}>
                      {t('language')}
                    </label>
                    <select
                      id="language-select"
                      value={lang}
                      onChange={(e) => handleLanguageChange(e.target.value)}
                      aria-label="Sélectionner la langue"
                      style={{
                        background: isDark ? '#262626' : '#f5f5f5',
                        border: `1px solid ${colors.borderColor}`,
                        borderRadius: '8px',
                        color: colors.textPrimary,
                        padding: '6px 12px',
                        fontSize: '13px',
                        cursor: 'pointer',
                        outline: 'none',
                      }}
                    >
                      {languages.map((l) => (
                        <option key={l.code} value={l.code}>{l.label}</option>
                      ))}
                    </select>
                  </div>

                  <div className="header-separator" style={{ background: colors.borderColor }} role="separator" />

                  {menuLinks.map((link) => (
                    <a
                      key={link.label}
                      href={link.href}
                      className="header-dropdown-link"
                      role="menuitem"
                      style={{ color: colors.textPrimary }}
                    >
                      <span aria-hidden="true">{link.icon}</span>
                      <span>{link.label}</span>
                    </a>
                  ))}

                  <div className="header-separator" style={{ background: colors.borderColor }} role="separator" />

                  {menuLinksPro.map((link) =>
                    link.to ? (
                      <button
                        key={link.label}
                        type="button"
                        onClick={() => handleNavClick(link.to)}
                        className="header-dropdown-link"
                        role="menuitem"
                        style={{ color: colors.textPrimary }}
                      >
                        <span aria-hidden="true">{link.icon}</span>
                        <span>{link.label}</span>
                      </button>
                    ) : (
                      <a
                        key={link.label}
                        href={link.href}
                        className="header-dropdown-link"
                        role="menuitem"
                        style={{ color: colors.textPrimary }}
                      >
                        <span aria-hidden="true">{link.icon}</span>
                        <span>{link.label}</span>
                      </a>
                    )
                  )}
                </div>
              )}
            </div>

            {/* CTA Button */}
            <Link
              to="/chat"
              className="header-cta desktop-only"
              style={{
                background: accent.gradient,
                boxShadow: '0 4px 12px rgba(0, 168, 107, 0.25)',
              }}
            >
              {t('launch_app')}
            </Link>

            {/* Mobile Hamburger */}
            <button
              type="button"
              className="header-hamburger mobile-only"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              aria-label={mobileMenuOpen ? 'Fermer le menu' : 'Ouvrir le menu de navigation'}
              aria-expanded={mobileMenuOpen}
              aria-controls="mobile-menu"
              style={{
                border: `1px solid ${colors.borderColor}`,
                color: colors.textPrimary,
              }}
            >
              {mobileMenuOpen ? '✕' : '☰'}
            </button>
          </div>
        </nav>
      </header>

      {/* Mobile Menu Overlay */}
      {mobileMenuOpen && (
        <div
          id="mobile-menu"
          className="header-mobile-overlay"
          role="navigation"
          aria-label="Menu mobile"
          style={{ background: isDark ? 'rgba(10, 10, 10, 0.95)' : 'rgba(255, 255, 255, 0.95)' }}
        >
          <div style={{ marginBottom: '20px' }}>
            {navLinks
              .filter((link) => (link.to ? link.to !== location.pathname : true))
              .map((link) => (
                <button
                  key={link.to ?? link.anchorId}
                  type="button"
                  className="header-mobile-link"
                  onClick={() =>
                    link.anchorId ? handleAnchorClick(link.anchorId) : handleNavClick(link.to)
                  }
                  style={{
                    color: colors.textPrimary,
                    borderBottom: `1px solid ${colors.borderColor}`,
                  }}
                >
                  {link.label}
                </button>
              ))}
          </div>

          {/* Theme Toggle Mobile */}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              padding: '16px 0',
              borderBottom: `1px solid ${colors.borderColor}`,
            }}
          >
            <span style={{ color: colors.textPrimary, fontSize: '16px' }}>
              {t('dark_theme')}
            </span>
            <button
              type="button"
              onClick={toggleTheme}
              role="switch"
              aria-checked={isDark}
              aria-label="Activer/désactiver le thème sombre"
              style={{
                width: '50px',
                height: '28px',
                borderRadius: '14px',
                border: 'none',
                background: isDark ? accent.primary : '#d1d5db',
                position: 'relative',
                cursor: 'pointer',
              }}
            >
              <span
                style={{
                  position: 'absolute',
                  top: '3px',
                  left: isDark ? '25px' : '3px',
                  width: '22px',
                  height: '22px',
                  borderRadius: '50%',
                  background: '#fff',
                  transition: 'left 0.2s',
                }}
              />
            </button>
          </div>

          {/* Language Mobile */}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              padding: '16px 0',
              borderBottom: `1px solid ${colors.borderColor}`,
            }}
          >
            <label htmlFor="mobile-language-select" style={{ color: colors.textPrimary, fontSize: '16px' }}>
              {t('language')}
            </label>
            <select
              id="mobile-language-select"
              value={lang}
              onChange={(e) => handleLanguageChange(e.target.value)}
              aria-label="Sélectionner la langue"
              style={{
                background: isDark ? '#262626' : '#f5f5f5',
                border: `1px solid ${colors.borderColor}`,
                borderRadius: '8px',
                color: colors.textPrimary,
                padding: '8px 16px',
                fontSize: '14px',
                cursor: 'pointer',
              }}
            >
              {languages.map((l) => (
                <option key={l.code} value={l.code}>{l.label}</option>
              ))}
            </select>
          </div>

          {/* CTA Mobile */}
          <Link
            to="/chat"
            className="header-mobile-cta"
            style={{ background: accent.gradient }}
            onClick={() => setMobileMenuOpen(false)}
          >
            {t('launch_app')}
          </Link>
        </div>
      )}
    </>
  );
};

export default Header;
