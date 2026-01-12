import React, { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';

// Dropdown Resources Component
const ResourcesDropdown: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  const handleMouseEnter = () => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }
    setIsOpen(true);
  };

  const handleMouseLeave = () => {
    timeoutRef.current = setTimeout(() => {
      setIsOpen(false);
    }, 300);
  };

  const resources = [
    { icon: '📚', label: 'Docs & Help Center', href: '/docs' },
    { icon: '📝', label: 'Blog', href: '/blog' },
    { icon: '🎨', label: 'Gallery', href: '/gallery' },
    { icon: '📊', label: 'Status', href: '/status' }
  ];

  const community = [
    { icon: '💬', label: 'Discord', href: '#' },
    { icon: '📺', label: 'YouTube', href: '#' },
    { icon: '📸', label: 'Instagram', href: '#' },
    { icon: '💼', label: 'LinkedIn', href: '#' },
    { icon: '🐦', label: 'Twitter/X', href: '#' },
    { icon: '🔗', label: 'Reddit', href: '#' }
  ];

  return (
    <div
      className="relative"
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      <button
        className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all ${
          isOpen
            ? 'text-gray-900 dark:text-white bg-gray-100 dark:bg-white/5'
            : 'text-gray-700 dark:text-white/70 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-white/5'
        }`}
      >
        Resources
        <svg
          className={`w-3 h-3 transition-transform ${isOpen ? 'rotate-180' : ''}`}
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
        >
          <path d="M2 4L6 8L10 4"/>
        </svg>
      </button>

      {/* Mega Menu */}
      <div className={`
        absolute top-full left-1/2 -translate-x-1/2 mt-5
        bg-[#1A1B1F]/98 backdrop-blur-xl border border-white/10
        rounded-xl shadow-2xl p-6 min-w-[500px]
        transition-all duration-200 z-50
        ${isOpen ? 'opacity-100 visible translate-y-0' : 'opacity-0 invisible -translate-y-2'}
      `}>
        {/* Arrow */}
        <div className="absolute -top-2 left-1/2 -translate-x-1/2 w-4 h-4 bg-[#1A1B1F] border-t border-l border-white/10 rotate-45" />

        <div className="grid grid-cols-2 gap-10 relative z-10">
          {/* Resources Column */}
          <div>
            <h3 className="text-xs font-semibold text-white/50 uppercase tracking-wider mb-4">
              Resources
            </h3>
            <ul className="space-y-2">
              {resources.map((item, i) => (
                <li key={i}>
                  <Link
                    to={item.href}
                    className="flex items-center gap-3 text-white/80 hover:text-white hover:bg-white/5 px-3 py-2 rounded-lg transition-all hover:translate-x-1"
                  >
                    <span className="text-lg">{item.icon}</span>
                    <span className="text-sm">{item.label}</span>
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Community Column */}
          <div>
            <h3 className="text-xs font-semibold text-white/50 uppercase tracking-wider mb-4">
              Community
            </h3>
            <div className="grid grid-cols-2 gap-2">
              {community.map((item, i) => (
                <a
                  key={i}
                  href={item.href}
                  className="flex items-center gap-2 text-white/80 hover:text-white hover:bg-white/5 px-3 py-2 rounded-lg transition-all hover:translate-x-0.5"
                >
                  <span className="text-base">{item.icon}</span>
                  <span className="text-sm">{item.label}</span>
                </a>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Main Header Component
const BoltHeader: React.FC = () => {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <header className={`
      fixed top-0 left-0 right-0 z-[100] transition-all duration-300
      site-header border-b border-gray-200 dark:border-white/10
    `}>
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2 group">
            <div className="flex items-center">
              <span className="text-gray-900 dark:text-white font-bold italic text-xl tracking-tight">
                RAG
              </span>
              <span className="bg-gray-900/10 dark:bg-white/10 text-gray-900 dark:text-white text-xs px-2 py-0.5 rounded ml-1 italic font-medium">
                .dz
              </span>
            </div>
          </Link>

          {/* Navigation */}
          <nav className="hidden md:flex items-center space-x-2">
            <Link
              to="/knowledge"
              className="px-4 py-2 rounded-lg text-gray-700 dark:text-white/70 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-white/5 transition-all"
            >
              Knowledge
            </Link>
            <Link
              to="/projects"
              className="px-4 py-2 rounded-lg text-gray-700 dark:text-white/70 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-white/5 transition-all"
            >
              Projects
            </Link>
            <ResourcesDropdown />
            <Link
              to="/mcp"
              className="px-4 py-2 rounded-lg text-gray-700 dark:text-white/70 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-white/5 transition-all"
            >
              MCP
            </Link>
            <Link
              to="/settings"
              className="px-4 py-2 rounded-lg text-gray-700 dark:text-white/70 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-white/5 transition-all"
            >
              Settings
            </Link>
          </nav>

          {/* Actions */}
          <div className="flex items-center space-x-4">
            {/* Social Icons */}
            <div className="hidden lg:flex items-center space-x-2">
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                className="p-2 rounded-lg text-gray-600 dark:text-white/60 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-white/5 transition-all"
                aria-label="GitHub"
              >
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                </svg>
              </a>
              <a
                href="https://discord.com"
                target="_blank"
                rel="noopener noreferrer"
                className="p-2 rounded-lg text-gray-600 dark:text-white/60 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-white/5 transition-all"
                aria-label="Discord"
              >
                <span className="text-lg">💬</span>
              </a>
            </div>

            {/* CTA Buttons */}
            <button className="hidden sm:block px-4 py-2 rounded-lg text-gray-700 dark:text-white/70 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-white/5 transition-all font-medium">
              Sign in
            </button>
            <Link
              to="/projects"
              className="px-5 py-2 rounded-lg bg-blue-500 hover:bg-blue-600 text-white font-semibold transition-all hover:shadow-[0_0_20px_rgba(59,130,246,0.5)]"
            >
              Get started
            </Link>
          </div>
        </div>
      </div>
    </header>
  );
};

export default BoltHeader;
