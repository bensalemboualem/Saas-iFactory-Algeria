import { useRef, useState, useCallback, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useTranslation } from '../i18n';
import { useTheme } from '../hooks';

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

  // Fermer le menu au clic extérieur
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

  const logoSrc = isDark
    ? '/assets/images/logodarkiafa.png'
    : '/assets/images/logoclaireiafa.png';

  return (
    <>
      <header
        style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          height: '66px',
          zIndex: 1000,
          background: 'transparent',
          backdropFilter: 'blur(16px)',
          borderBottom: `1px solid ${colors.borderColor}`,
        }}
      >
        <nav
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            height: '100%',
            maxWidth: '1400px',
            margin: '0 auto',
            padding: '0 24px',
          }}
          aria-label="Navigation principale"
        >
          {/* Logo */}
          <Link
            to="/"
            style={{
              display: 'flex',
              alignItems: 'center',
              textDecoration: 'none',
            }}
            aria-label="IA Factory Algeria - Accueil"
          >
            <img
              alt="IA Factory Algeria"
              src={logoSrc}
              style={{
                height: '200px',
                width: 'auto',
                objectFit: 'contain',
              }}
            />
          </Link>

          {/* Desktop Nav Links */}
          <div
            className="desktop-nav"
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '4px',
            }}
            role="navigation"
            aria-label="Liens de navigation"
          >
            {navLinks
              .filter((link) => link.to !== location.pathname)
              .map((link) => (
                <Link
                  key={link.to}
                  to={link.to}
                  style={{
                    color: colors.textMuted,
                    fontSize: '14px',
                    fontWeight: 500,
                    textDecoration: 'none',
                    padding: '8px 14px',
                    borderRadius: '8px',
                    transition: 'all 0.2s',
                  }}
                >
                  {link.label}
                </Link>
              ))}
          </div>

          {/* Right Side */}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
            }}
          >
            {/* Menu 3 dots button */}
            <div ref={menuRef} style={{ position: 'relative' }}>
              <button
                type="button"
                onClick={() => setMenuOpen(!menuOpen)}
                className="desktop-only"
                aria-label="Ouvrir le menu des paramètres"
                aria-expanded={menuOpen}
                aria-haspopup="true"
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  width: '40px',
                  height: '40px',
                  background: isDark ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.05)',
                  border: `1px solid ${colors.borderColor}`,
                  borderRadius: '10px',
                  cursor: 'pointer',
                  color: colors.textMuted,
                  fontSize: '20px',
                }}
              >
                ⋮
              </button>

              {/* Dropdown Menu */}
              {menuOpen && (
                <div
                  role="menu"
                  aria-label="Menu des paramètres"
                  style={{
                    position: 'absolute',
                    top: 'calc(100% + 8px)',
                    right: 0,
                    width: '280px',
                    background: isDark ? '#171717' : '#ffffff',
                    borderRadius: '12px',
                    border: `1px solid ${colors.borderColor}`,
                    boxShadow: isDark
                      ? '0 8px 32px rgba(0, 0, 0, 0.4)'
                      : '0 8px 32px rgba(0, 0, 0, 0.12)',
                    padding: '8px',
                    zIndex: 1001,
                  }}
                >
                  {/* Theme Toggle */}
                  <div
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      padding: '12px',
                    }}
                  >
                    <span style={{ color: colors.textPrimary, fontSize: '14px' }}>
                      {t('dark_theme')}
                    </span>
                    <button
                      type="button"
                      onClick={toggleTheme}
                      role="switch"
                      aria-checked={isDark}
                      aria-label="Activer/désactiver le thème sombre"
                      style={{
                        width: '44px',
                        height: '24px',
                        borderRadius: '12px',
                        border: 'none',
                        background: isDark ? accent.primary : '#d1d5db',
                        position: 'relative',
                        cursor: 'pointer',
                      }}
                    >
                      <span
                        style={{
                          position: 'absolute',
                          top: '2px',
                          left: isDark ? '22px' : '2px',
                          width: '20px',
                          height: '20px',
                          borderRadius: '50%',
                          background: '#fff',
                          transition: 'left 0.2s',
                          boxShadow: '0 1px 3px rgba(0,0,0,0.2)',
                        }}
                      />
                    </button>
                  </div>

                  {/* Language Selector */}
                  <div
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      padding: '12px',
                    }}
                  >
                    <label
                      htmlFor="language-select"
                      style={{ color: colors.textPrimary, fontSize: '14px' }}
                    >
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
                        <option key={l.code} value={l.code}>
                          {l.label}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div style={{ height: '1px', background: colors.borderColor, margin: '4px 0' }} role="separator" />

                  {/* Menu Links */}
                  {menuLinks.map((link) => (
                    <a
                      key={link.label}
                      href={link.href}
                      role="menuitem"
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '12px',
                        padding: '10px 12px',
                        color: colors.textPrimary,
                        textDecoration: 'none',
                        fontSize: '14px',
                        borderRadius: '8px',
                      }}
                    >
                      <span aria-hidden="true">{link.icon}</span>
                      <span>{link.label}</span>
                    </a>
                  ))}

                  <div style={{ height: '1px', background: colors.borderColor, margin: '4px 0' }} role="separator" />

                  {/* Pro Links */}
                  {menuLinksPro.map((link) =>
                    link.to ? (
                      <button
                        key={link.label}
                        type="button"
                        onClick={() => handleNavClick(link.to)}
                        role="menuitem"
                        style={{
                          display: 'flex',
                          alignItems: 'center',
                          gap: '12px',
                          padding: '10px 12px',
                          color: colors.textPrimary,
                          background: 'transparent',
                          border: 'none',
                          fontSize: '14px',
                          borderRadius: '8px',
                          cursor: 'pointer',
                          width: '100%',
                          textAlign: 'left',
                        }}
                      >
                        <span aria-hidden="true">{link.icon}</span>
                        <span>{link.label}</span>
                      </button>
                    ) : (
                      <a
                        key={link.label}
                        href={link.href}
                        role="menuitem"
                        style={{
                          display: 'flex',
                          alignItems: 'center',
                          gap: '12px',
                          padding: '10px 12px',
                          color: colors.textPrimary,
                          textDecoration: 'none',
                          fontSize: '14px',
                          borderRadius: '8px',
                        }}
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
              className="desktop-only"
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                padding: '10px 20px',
                background: accent.gradient,
                color: '#fff',
                fontSize: '14px',
                fontWeight: 600,
                textDecoration: 'none',
                borderRadius: '10px',
                boxShadow: '0 4px 12px rgba(0, 168, 107, 0.3)',
              }}
            >
              {t('launch_app')}
            </Link>

            {/* Mobile Hamburger */}
            <button
              type="button"
              className="mobile-only"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              aria-label={mobileMenuOpen ? 'Fermer le menu' : 'Ouvrir le menu de navigation'}
              aria-expanded={mobileMenuOpen}
              aria-controls="mobile-menu"
              style={{
                display: 'none',
                alignItems: 'center',
                justifyContent: 'center',
                width: '40px',
                height: '40px',
                background: 'transparent',
                border: `1px solid ${colors.borderColor}`,
                borderRadius: '10px',
                cursor: 'pointer',
                color: colors.textPrimary,
                fontSize: '24px',
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
          className="mobile-menu-overlay"
          role="navigation"
          aria-label="Menu mobile"
          style={{
            position: 'fixed',
            top: '66px',
            left: 0,
            right: 0,
            bottom: 0,
            background: colors.bgPrimary,
            zIndex: 999,
            padding: '20px',
            overflowY: 'auto',
          }}
        >
          {/* Mobile Nav Links */}
          <div style={{ marginBottom: '20px' }}>
            {navLinks
              .filter((link) => link.to !== location.pathname)
              .map((link) => (
                <button
                  key={link.to}
                  type="button"
                  onClick={() => handleNavClick(link.to)}
                  style={{
                    display: 'block',
                    width: '100%',
                    textAlign: 'left',
                    color: colors.textPrimary,
                    fontSize: '18px',
                    fontWeight: 500,
                    background: 'transparent',
                    border: 'none',
                    padding: '16px 0',
                    borderBottom: `1px solid ${colors.borderColor}`,
                    cursor: 'pointer',
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
                <option key={l.code} value={l.code}>
                  {l.label}
                </option>
              ))}
            </select>
          </div>

          {/* CTA Mobile */}
          <Link
            to="/chat"
            style={{
              display: 'block',
              textAlign: 'center',
              padding: '16px',
              marginTop: '24px',
              background: accent.gradient,
              color: '#fff',
              fontSize: '16px',
              fontWeight: 600,
              textDecoration: 'none',
              borderRadius: '12px',
            }}
            onClick={() => setMobileMenuOpen(false)}
          >
            {t('launch_app')}
          </Link>
        </div>
      )}

      {/* CSS for responsive */}
      <style>{`
        @media (min-width: 769px) {
          .mobile-only { display: none !important; }
          .desktop-only { display: flex !important; }
          .desktop-nav { display: flex !important; }
        }
        @media (max-width: 768px) {
          .mobile-only { display: flex !important; }
          .desktop-only { display: none !important; }
          .desktop-nav { display: none !important; }
        }
      `}</style>
    </>
  );
};

export default Header;
