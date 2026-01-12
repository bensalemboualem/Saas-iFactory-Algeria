import React from 'react';
import { Link } from 'react-router-dom';

const BoltFooter: React.FC = () => {
  const footerSections = {
    resources: [
      { label: 'Support', href: '/support', arrow: true },
      { label: 'Blog', href: '/blog', arrow: true },
      { label: 'Gallery', href: '/gallery', arrow: true },
      { label: 'Status', href: '/status', arrow: true }
    ],
    company: [
      { label: 'About', href: '/about' },
      { label: 'Careers', href: '/careers' },
      { label: 'Privacy', href: '/privacy' },
      { label: 'Terms', href: '/terms' }
    ],
    social: [
      { icon: '💬', label: 'Discord', href: '#' },
      { icon: '💼', label: 'LinkedIn', href: '#' },
      { icon: '📺', label: 'YouTube', href: '#' },
      { icon: '🐦', label: 'Twitter/X', href: '#' },
      { icon: '📸', label: 'Instagram', href: '#' },
      { icon: '🔗', label: 'Reddit', href: '#' }
    ]
  };

  return (
    <footer className="relative site-footer pt-20 pb-10 mt-32">
      {/* Effet de lumière bleue signature */}
      <div className="absolute top-0 left-0 right-0 h-[200px] pointer-events-none">
        <div
          className="absolute inset-0"
          style={{
            background: 'radial-gradient(ellipse 120% 50% at 50% 0%, rgba(59, 130, 246, 0.3) 0%, rgba(59, 130, 246, 0.15) 40%, transparent 70%)'
          }}
        />
      </div>

      <div className="relative container mx-auto px-6">
        {/* Grille du footer */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12 mb-16">
          {/* Section Logo/Marque */}
          <div className="lg:col-span-1">
            <div className="flex items-center mb-4">
              <span className="text-white font-bold text-2xl tracking-tight">
                IAFactory
              </span>
              <span className="bg-gradient-to-r from-blue-500 to-purple-600 text-white text-xs px-2 py-0.5 rounded ml-2 font-medium">
                Docs
              </span>
            </div>
            <p className="text-sm leading-relaxed max-w-xs">
              Gestion documentaire intelligente avec RAG.
              Powered by AI, built for innovation.
            </p>
              <div className="flex items-center space-x-3 mt-6">
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                className="p-2 rounded-lg hover:bg-white/5 transition-all"
              >
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                </svg>
              </a>
            </div>
          </div>

          {/* Section Resources */}
          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wider mb-5">
              Resources
            </h3>
            <ul className="space-y-3">
              {footerSections.resources.map((item, i) => (
                <li key={i}>
                  <Link
                    to={item.href}
                    className="group inline-flex items-center hover:text-white transition-colors text-sm"
                  >
                    {item.label}
                    {item.arrow && (
                      <svg
                        className="w-3 h-3 ml-1 opacity-0 -translate-x-2 group-hover:opacity-100 group-hover:translate-x-0 transition-all"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                      >
                        <path d="M2 5h8M6 2l3 3-3 3"/>
                      </svg>
                    )}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Section Company */}
          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wider mb-5">
              Company
            </h3>
            <ul className="space-y-3">
              {footerSections.company.map((item, i) => (
                <li key={i}>
                  <Link
                    to={item.href}
                    className="hover:text-white transition-colors text-sm block"
                  >
                    {item.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Section Social */}
          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wider mb-5">
              Community
            </h3>
            <ul className="space-y-3">
              {footerSections.social.map((item, i) => (
                <li key={i}>
                  <a
                    href={item.href}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-2 hover:text-white transition-colors text-sm"
                  >
                    <span className="text-base">{item.icon}</span>
                    {item.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Copyright et liens légaux */}
        <div className="pt-8 border-t border-white/5">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-sm">
              © {new Date().getFullYear()} IAFactory - All rights reserved.
            </p>
            <div className="flex items-center space-x-6">
              <Link
                to="/privacy"
                className="text-sm hover:text-white transition-colors"
              >
                Privacy Policy
              </Link>
              <Link
                to="/terms"
                className="text-sm hover:text-white transition-colors"
              >
                Terms of Service
              </Link>
              <Link
                to="/cookies"
                className="text-sm hover:text-white transition-colors"
              >
                Cookie Policy
              </Link>
            </div>
          </div>

          {/* Badge "Made in Algeria" */}
          <div className="mt-6 flex justify-center">
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-white/10">
              <span className="text-2xl">🇩🇿</span>
              <span className="text-sm text-white/60 font-medium">
                Proudly Made in Algeria
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Effet de glow en bas */}
      <div className="absolute bottom-0 left-0 right-0 h-[100px] pointer-events-none overflow-hidden">
        <div
          className="absolute -bottom-12 left-1/2 -translate-x-1/2 w-[800px] h-[200px] rounded-full blur-3xl"
          style={{
            background: 'radial-gradient(circle, rgba(59, 130, 246, 0.2) 0%, transparent 70%)'
          }}
        />
      </div>
    </footer>
  );
};

export default BoltFooter;
