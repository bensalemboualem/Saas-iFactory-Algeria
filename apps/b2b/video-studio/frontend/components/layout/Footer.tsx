"use client";

import Link from "next/link";
import { useThemeStore, useLocaleStore } from "@/lib/store";
import { t } from "@/lib/i18n";
import { Twitter, Github, Youtube, Mail } from "lucide-react";

export default function Footer() {
  const { theme } = useThemeStore();
  const { locale } = useLocaleStore();

  const socialLinks = [
    { icon: Twitter, href: "https://twitter.com/iafactory", label: "Twitter" },
    { icon: Github, href: "https://github.com/iafactory", label: "GitHub" },
    { icon: Youtube, href: "https://youtube.com/@iafactory", label: "YouTube" },
    { icon: Mail, href: "mailto:contact@iafactory.ch", label: "Email" },
  ];

  const footerLinks = [
    { label: t("footer.privacy", locale), href: "/privacy" },
    { label: t("footer.terms", locale), href: "/terms" },
    { label: t("footer.contact", locale), href: "/contact" },
  ];

  return (
    <footer
      className={`border-t transition-colors ${
        theme === "dark"
          ? "bg-[#0a0a0f] border-[#2a2a35]"
          : "bg-gray-50 border-gray-200"
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="md:col-span-2">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-400 to-fuchsia-500 flex items-center justify-center font-bold text-sm shadow-lg shadow-cyan-500/30">
                IA
              </div>
              <span className="font-mono font-bold text-lg bg-gradient-to-r from-cyan-400 to-fuchsia-500 bg-clip-text text-transparent">
                IA Factory Studio
              </span>
            </div>
            <p
              className={`text-sm max-w-md ${
                theme === "dark" ? "text-gray-400" : "text-gray-600"
              }`}
            >
              {t("hero.description", locale)}
            </p>

            {/* Social Links */}
            <div className="flex gap-4 mt-6">
              {socialLinks.map((social) => (
                <a
                  key={social.label}
                  href={social.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className={`p-2 rounded-lg transition-all ${
                    theme === "dark"
                      ? "text-gray-400 hover:text-cyan-400 hover:bg-white/5"
                      : "text-gray-500 hover:text-cyan-600 hover:bg-gray-100"
                  }`}
                >
                  <social.icon className="w-5 h-5" />
                </a>
              ))}
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3
              className={`font-semibold mb-4 ${
                theme === "dark" ? "text-white" : "text-gray-900"
              }`}
            >
              Navigation
            </h3>
            <ul className="space-y-2">
              {[
                { label: t("nav.studio", locale), href: "/studio" },
                { label: t("nav.editor", locale), href: "/editor" },
                { label: t("nav.templates", locale), href: "/templates" },
                { label: t("nav.projects", locale), href: "/projects" },
              ].map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className={`text-sm transition-colors ${
                      theme === "dark"
                        ? "text-gray-400 hover:text-cyan-400"
                        : "text-gray-600 hover:text-cyan-600"
                    }`}
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h3
              className={`font-semibold mb-4 ${
                theme === "dark" ? "text-white" : "text-gray-900"
              }`}
            >
              Légal
            </h3>
            <ul className="space-y-2">
              {footerLinks.map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className={`text-sm transition-colors ${
                      theme === "dark"
                        ? "text-gray-400 hover:text-cyan-400"
                        : "text-gray-600 hover:text-cyan-600"
                    }`}
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Bottom */}
        <div
          className={`mt-12 pt-8 border-t flex flex-col sm:flex-row justify-between items-center gap-4 ${
            theme === "dark" ? "border-[#2a2a35]" : "border-gray-200"
          }`}
        >
          <p
            className={`text-sm ${
              theme === "dark" ? "text-gray-500" : "text-gray-500"
            }`}
          >
            © {new Date().getFullYear()} IA Factory. {t("footer.rights", locale)}.
          </p>
          <p
            className={`text-sm ${
              theme === "dark" ? "text-gray-500" : "text-gray-500"
            }`}
          >
            🇩🇿 Made in Algeria with ❤️
          </p>
        </div>
      </div>
    </footer>
  );
}
