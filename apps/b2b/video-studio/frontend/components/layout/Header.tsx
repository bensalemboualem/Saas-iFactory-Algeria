"use client";

import { useState } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import {
  Menu,
  X,
  Sun,
  Moon,
  Globe,
  ChevronDown,
  Video,
  Scissors,
  LayoutTemplate,
  FolderOpen,
  CreditCard,
  LogIn,
} from "lucide-react";
import { useThemeStore, useLocaleStore } from "@/lib/store";
import { t, locales, localeNames, localeFlags, Locale } from "@/lib/i18n";

export default function Header() {
  const { theme, toggleTheme } = useThemeStore();
  const { locale, setLocale } = useLocaleStore();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [langMenuOpen, setLangMenuOpen] = useState(false);

  const navItems = [
    { href: "/", label: t("nav.home", locale), icon: null },
    { href: "/studio", label: t("nav.studio", locale), icon: Video },
    { href: "/editor", label: t("nav.editor", locale), icon: Scissors },
    { href: "/templates", label: t("nav.templates", locale), icon: LayoutTemplate },
    { href: "/projects", label: t("nav.projects", locale), icon: FolderOpen },
    { href: "/credits", label: t("nav.credits", locale), icon: CreditCard },
  ];

  return (
    <header
      className={`sticky top-0 z-50 backdrop-blur-xl border-b transition-colors ${
        theme === "dark"
          ? "bg-[#0a0a0f]/90 border-[#2a2a35]"
          : "bg-white/90 border-gray-200"
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-400 to-fuchsia-500 flex items-center justify-center font-bold text-sm shadow-lg shadow-cyan-500/30">
              IA
            </div>
            <span className="font-mono font-bold text-lg bg-gradient-to-r from-cyan-400 to-fuchsia-500 bg-clip-text text-transparent hidden sm:block">
              IA Factory Studio
            </span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden lg:flex items-center gap-1">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                  theme === "dark"
                    ? "text-gray-300 hover:text-white hover:bg-white/5"
                    : "text-gray-600 hover:text-gray-900 hover:bg-gray-100"
                }`}
              >
                {item.icon && <item.icon className="w-4 h-4" />}
                {item.label}
              </Link>
            ))}
          </nav>

          {/* Right Actions */}
          <div className="flex items-center gap-2">
            {/* Language Selector */}
            <div className="relative">
              <button
                onClick={() => setLangMenuOpen(!langMenuOpen)}
                className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                  theme === "dark"
                    ? "text-gray-300 hover:text-white hover:bg-white/5"
                    : "text-gray-600 hover:text-gray-900 hover:bg-gray-100"
                }`}
              >
                <Globe className="w-4 h-4" />
                <span className="hidden sm:inline">{localeFlags[locale]}</span>
                <ChevronDown className="w-3 h-3" />
              </button>

              <AnimatePresence>
                {langMenuOpen && (
                  <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    className={`absolute right-0 mt-2 w-40 rounded-xl shadow-xl border overflow-hidden ${
                      theme === "dark"
                        ? "bg-[#1a1a24] border-[#2a2a35]"
                        : "bg-white border-gray-200"
                    }`}
                  >
                    {locales.map((loc) => (
                      <button
                        key={loc}
                        onClick={() => {
                          setLocale(loc);
                          setLangMenuOpen(false);
                        }}
                        className={`w-full flex items-center gap-3 px-4 py-3 text-sm transition-all ${
                          locale === loc
                            ? "bg-gradient-to-r from-cyan-500/20 to-fuchsia-500/20 text-cyan-400"
                            : theme === "dark"
                            ? "hover:bg-white/5"
                            : "hover:bg-gray-50"
                        }`}
                      >
                        <span className="text-lg">{localeFlags[loc]}</span>
                        <span>{localeNames[loc]}</span>
                      </button>
                    ))}
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            {/* Theme Toggle */}
            <button
              onClick={toggleTheme}
              className={`p-2.5 rounded-lg transition-all ${
                theme === "dark"
                  ? "text-gray-300 hover:text-yellow-400 hover:bg-white/5"
                  : "text-gray-600 hover:text-gray-900 hover:bg-gray-100"
              }`}
            >
              {theme === "dark" ? (
                <Sun className="w-5 h-5" />
              ) : (
                <Moon className="w-5 h-5" />
              )}
            </button>

            {/* CTA Button */}
            <Link
              href="/studio"
              className="hidden sm:flex items-center gap-2 px-4 py-2 rounded-lg bg-gradient-to-r from-cyan-400 to-fuchsia-500 text-[#0a0a0f] font-semibold text-sm shadow-lg shadow-cyan-500/30 hover:shadow-cyan-500/50 hover:-translate-y-0.5 transition-all"
            >
              <Video className="w-4 h-4" />
              {t("nav.studio", locale)}
            </Link>

            {/* Mobile Menu Button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className={`lg:hidden p-2.5 rounded-lg transition-all ${
                theme === "dark"
                  ? "text-gray-300 hover:text-white hover:bg-white/5"
                  : "text-gray-600 hover:text-gray-900 hover:bg-gray-100"
              }`}
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        <AnimatePresence>
          {mobileMenuOpen && (
            <motion.nav
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              exit={{ opacity: 0, height: 0 }}
              className="lg:hidden py-4 border-t border-[#2a2a35]"
            >
              {navItems.map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className={`flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all ${
                    theme === "dark"
                      ? "text-gray-300 hover:text-white hover:bg-white/5"
                      : "text-gray-600 hover:text-gray-900 hover:bg-gray-100"
                  }`}
                >
                  {item.icon && <item.icon className="w-5 h-5" />}
                  {item.label}
                </Link>
              ))}
            </motion.nav>
          )}
        </AnimatePresence>
      </div>
    </header>
  );
}
