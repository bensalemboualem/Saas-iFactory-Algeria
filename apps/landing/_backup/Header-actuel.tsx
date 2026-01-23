import { useEffect, useRef, useState } from 'react';

type Theme = 'dark' | 'light';

type NavLink = {
  label: string;
  page?: string;
  href?: string;
};

type MenuLink = {
  href?: string;
  icon: string;
  label: string;
  page?: string;
};

const navLinks: NavLink[] = [
  { label: 'Accueil', page: 'home' },
  { label: 'Tarifs', page: 'pricing' },
  { label: 'B2B', page: 'b2b' },
  { label: 'Applications', href: './apps.html' },
  { label: 'Agents IA', href: './agents.html' },
  { label: 'Workflows', href: './workflows.html' },
];

const menuLinks: MenuLink[] = [
  { href: './docs/getstarted.html', icon: '🚀', label: 'Commencer' },
  { href: './docs/documentation.html', icon: '📖', label: 'Documentation' },
  { href: './docs/help.html', icon: '💬', label: "Centre d'aide" },
  { href: './docs/changelog.html', icon: '📋', label: 'Changelog' },
  { href: './docs/blog.html', icon: '📝', label: 'Blog' },
];

const menuLinksPro: MenuLink[] = [
  { href: './docs/pro.html', icon: '⭐', label: 'IA Factory Pro' },
  { icon: '🏢', label: 'B2B', page: 'b2b' },
  { icon: '🔌', label: 'API', page: 'api' },
];

const Header = () => {
  const [theme, setTheme] = useState<Theme>('dark');
  const [menuOpen, setMenuOpen] = useState(false);
  const [selectedLang, setSelectedLang] = useState('fr');
  const [isScrolled, setIsScrolled] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const savedTheme = (localStorage.getItem('theme') as Theme) || 'dark';
    setTheme(savedTheme);
    document.documentElement.dataset.theme = savedTheme;

    const savedLang = localStorage.getItem('lang') || 'fr';
    setSelectedLang(savedLang);
    document.documentElement.lang = savedLang;
    document.documentElement.dir = savedLang === 'ar' ? 'rtl' : 'ltr';

    const onScroll = () => setIsScrolled(window.scrollY > 50);
    const onClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setMenuOpen(false);
      }
    };

    window.addEventListener('scroll', onScroll);
    document.addEventListener('mousedown', onClickOutside);

    return () => {
      window.removeEventListener('scroll', onScroll);
      document.removeEventListener('mousedown', onClickOutside);
    };
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
    document.documentElement.dataset.theme = newTheme;
    localStorage.setItem('theme', newTheme);
  };

  const setLanguage = (lang: string) => {
    setSelectedLang(lang);
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
    localStorage.setItem('lang', lang);
  };

  const showPage = (pageName: string) => {
    document.querySelectorAll('.page').forEach((page) => page.classList.remove('active'));
    const targetPage = document.getElementById(`page-${pageName}`);
    if (targetPage) targetPage.classList.add('active');
    window.scrollTo(0, 0);
  };

  const isDark = theme === 'dark';

  const headerStyle: React.CSSProperties = {
    WebkitBackdropFilter: 'blur(20px) saturate(180%)',
    backdropFilter: 'blur(20px) saturate(180%)',
    background: isScrolled
      ? isDark
        ? 'rgba(10, 10, 10, 0.85)'
        : 'rgba(255, 255, 255, 0.85)'
      : isDark
        ? 'rgba(10, 10, 10, 0.4)'
        : 'rgba(255, 255, 255, 0.25)',
    borderBottom: isDark
      ? '1px solid rgba(255, 255, 255, 0.1)'
      : '1px solid rgba(0, 0, 0, 0.1)',
    left: 0,
    position: 'fixed',
    right: 0,
    top: 0,
    transition: 'all 0.3s ease',
    zIndex: 100,
  };

  const navStyle: React.CSSProperties = {
    alignItems: 'center',
    display: 'flex',
    height: '70px',
    justifyContent: 'space-between',
    margin: '0 auto',
    maxWidth: '1200px',
    padding: '0 24px',
  };

  const logoImgStyle: React.CSSProperties = {
    height: '50px',
    objectFit: 'contain',
    width: 'auto',
  };

  const navLinksStyle: React.CSSProperties = {
    alignItems: 'center',
    display: 'flex',
    gap: '8px',
    listStyle: 'none',
    margin: 0,
    padding: 0,
  };

  const navLinkStyle: React.CSSProperties = {
    borderRadius: '8px',
    color: isDark ? '#a3a3a3' : '#525252',
    fontSize: '14px',
    fontWeight: 500,
    padding: '8px 16px',
    textDecoration: 'none',
  };

  const navRightStyle: React.CSSProperties = {
    alignItems: 'center',
    display: 'flex',
    gap: '12px',
  };

  const menuDotsStyle: React.CSSProperties = {
    alignItems: 'center',
    background: 'transparent',
    border: isDark
      ? '1px solid rgba(255, 255, 255, 0.1)'
      : '1px solid rgba(0, 0, 0, 0.1)',
    borderRadius: '8px',
    cursor: 'pointer',
    display: 'flex',
    flexDirection: 'column',
    gap: '3px',
    height: '36px',
    justifyContent: 'center',
    width: '36px',
  };

  const dotStyle: React.CSSProperties = {
    background: isDark ? '#a3a3a3' : '#525252',
    borderRadius: '50%',
    height: '4px',
    width: '4px',
  };

  const btnPrimaryStyle: React.CSSProperties = {
    alignItems: 'center',
    background: isDark ? '#9C7DFF' : 'linear-gradient(135deg, #8A5FFF, #6234BB)',
    border: 'none',
    borderRadius: '8px',
    color: '#ffffff',
    cursor: 'pointer',
    display: 'inline-flex',
    fontSize: '14px',
    fontWeight: 600,
    padding: '10px 20px',
    textDecoration: 'none',
  };

  const settingsMenuStyle: React.CSSProperties = {
    background: isDark ? '#171717' : '#ffffff',
    border: isDark
      ? '1px solid rgba(255, 255, 255, 0.1)'
      : '1px solid rgba(0, 0, 0, 0.1)',
    borderRadius: '12px',
    boxShadow: isDark ? '0 16px 48px rgba(0, 0, 0, 0.4)' : '0 16px 48px rgba(0, 0, 0, 0.15)',
    padding: '12px',
    position: 'absolute',
    right: 0,
    top: 'calc(100% + 12px)',
    width: '280px',
    zIndex: 1000,
  };

  const settingsRowStyle: React.CSSProperties = {
    alignItems: 'center',
    display: 'flex',
    justifyContent: 'space-between',
    padding: '10px 8px',
  };

  const settingsLabelStyle: React.CSSProperties = {
    color: isDark ? '#ffffff' : '#0a0a0a',
    fontSize: '14px',
  };

  const toggleSliderStyle: React.CSSProperties = {
    background: isDark ? '#9C7DFF' : '#ccc',
    borderRadius: '24px',
    cursor: 'pointer',
    height: '24px',
    position: 'relative',
    width: '44px',
  };

  const toggleKnobStyle: React.CSSProperties = {
    background: 'white',
    borderRadius: '50%',
    height: '18px',
    left: isDark ? '23px' : '3px',
    position: 'absolute',
    top: '3px',
    transition: '0.3s',
    width: '18px',
  };

  const selectStyle: React.CSSProperties = {
    background: isDark ? '#262626' : '#f5f5f5',
    border: isDark
      ? '1px solid rgba(255, 255, 255, 0.1)'
      : '1px solid rgba(0, 0, 0, 0.1)',
    borderRadius: '8px',
    color: isDark ? '#ffffff' : '#0a0a0a',
    cursor: 'pointer',
    fontSize: '13px',
    padding: '6px 12px',
  };

  const dividerStyle: React.CSSProperties = {
    background: isDark ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)',
    height: '1px',
    margin: '8px 0',
  };

  const settingsLinkStyle: React.CSSProperties = {
    alignItems: 'center',
    borderRadius: '8px',
    color: isDark ? '#a3a3a3' : '#525252',
    cursor: 'pointer',
    display: 'flex',
    fontSize: '14px',
    gap: '12px',
    padding: '10px 8px',
    textDecoration: 'none',
  };

  return (
    <div role="banner" style={headerStyle}>
      <div style={navStyle}>
        <a href="#" onClick={() => showPage('home')} style={{ textDecoration: 'none' }}>
          <img
            alt="IAFactory Algeria"
            src={isDark ? '/assets/images/logodark.png' : '/assets/images/logocalire.png'}
            style={logoImgStyle}
          />
        </a>

        <ul style={navLinksStyle}>
          {navLinks.map((link) => (
            <li key={link.label}>
              {link.page ? (
                <a href="#" onClick={() => showPage(link.page)} style={navLinkStyle}>
                  {link.label}
                </a>
              ) : (
                <a href={link.href} style={navLinkStyle}>
                  {link.label}
                </a>
              )}
            </li>
          ))}
        </ul>

        <div style={navRightStyle}>
          <div ref={menuRef} style={{ position: 'relative' }}>
            <button onClick={() => setMenuOpen(!menuOpen)} style={menuDotsStyle}>
              <span style={dotStyle} />
              <span style={dotStyle} />
              <span style={dotStyle} />
            </button>

            {menuOpen && (
              <div style={settingsMenuStyle}>
                <div style={settingsRowStyle}>
                  <span style={settingsLabelStyle}>Theme sombre</span>
                  <div onClick={toggleTheme} style={toggleSliderStyle}>
                    <div style={toggleKnobStyle} />
                  </div>
                </div>

                <div style={settingsRowStyle}>
                  <span style={settingsLabelStyle}>Langue</span>
                  <select
                    onChange={(event) => setLanguage(event.target.value)}
                    style={selectStyle}
                    value={selectedLang}
                  >
                    <option value="fr">Francais</option>
                    <option value="ar">العربية</option>
                    <option value="en">English</option>
                  </select>
                </div>

                <div style={dividerStyle} />

                {menuLinks.map((link) => (
                  <a href={link.href} key={link.label} style={settingsLinkStyle}>
                    <span>{link.icon}</span>
                    {link.label}
                  </a>
                ))}

                <div style={dividerStyle} />

                {menuLinksPro.map((link) =>
                  link.page ? (
                    <a
                      href="#"
                      key={link.label}
                      onClick={() => {
                        showPage(link.page as string);
                        setMenuOpen(false);
                      }}
                      style={settingsLinkStyle}
                    >
                      <span>{link.icon}</span>
                      {link.label}
                    </a>
                  ) : (
                    <a href={link.href} key={link.label} style={settingsLinkStyle}>
                      <span>{link.icon}</span>
                      {link.label}
                    </a>
                  ),
                )}
              </div>
            )}
          </div>

          <a href="/login?next=/bolt" style={btnPrimaryStyle}>
            Lancer l'application
          </a>
        </div>
      </div>
    </div>
  );
};

export default Header;
