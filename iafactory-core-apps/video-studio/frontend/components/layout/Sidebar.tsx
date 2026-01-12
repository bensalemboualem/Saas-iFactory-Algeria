"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion } from "framer-motion";
import {
  Home,
  Video,
  Scissors,
  LayoutTemplate,
  FolderOpen,
  CreditCard,
  Settings,
  HelpCircle,
  ChevronLeft,
  ChevronRight,
  Rocket,
} from "lucide-react";
import { useThemeStore, useLocaleStore, useSidebarStore, useChatStore } from "@/lib/store";
import { t } from "@/lib/i18n";

export default function Sidebar() {
  const pathname = usePathname();
  const { theme } = useThemeStore();
  const { locale } = useLocaleStore();
  const { isCollapsed, toggle } = useSidebarStore();
  const { toggle: toggleChat } = useChatStore();

  const navItems = [
    { href: "/", icon: Home, label: t("nav.home", locale) },
    { href: "/studio", icon: Video, label: t("nav.studio", locale) },
    { href: "/pipeline", icon: Rocket, label: locale === 'ar' ? 'خط الإنتاج' : locale === 'en' ? 'Pipeline' : 'Pipeline' },
    { href: "/editor", icon: Scissors, label: t("nav.editor", locale) },
    { href: "/templates", icon: LayoutTemplate, label: t("nav.templates", locale) },
    { href: "/projects", icon: FolderOpen, label: t("nav.projects", locale) },
    { href: "/credits", icon: CreditCard, label: t("nav.credits", locale) },
  ];

  const bottomItems = [
    { icon: HelpCircle, label: t("chat.title", locale), onClick: toggleChat },
    { href: "/settings", icon: Settings, label: t("nav.settings", locale) },
  ];

  return (
    <aside
      className={`fixed left-0 top-16 bottom-0 z-40 transition-all duration-300 border-r ${
        theme === "dark"
          ? "bg-[#0a0a0f] border-[#2a2a35]"
          : "bg-white border-gray-200"
      } ${isCollapsed ? "w-16" : "w-64"}`}
    >
      <div className="flex flex-col h-full">
        {/* Toggle Button */}
        <button
          onClick={toggle}
          className={`absolute -right-3 top-6 w-6 h-6 rounded-full border flex items-center justify-center transition-all ${
            theme === "dark"
              ? "bg-[#1a1a24] border-[#2a2a35] text-gray-400 hover:text-white hover:border-cyan-400"
              : "bg-white border-gray-300 text-gray-500 hover:text-gray-900 hover:border-gray-400"
          }`}
        >
          {isCollapsed ? (
            <ChevronRight className="w-3 h-3" />
          ) : (
            <ChevronLeft className="w-3 h-3" />
          )}
        </button>

        {/* Main Navigation */}
        <nav className="flex-1 px-3 py-6 space-y-1">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all relative group ${
                  isActive
                    ? "bg-gradient-to-r from-cyan-500/20 to-fuchsia-500/20 text-cyan-400"
                    : theme === "dark"
                    ? "text-gray-400 hover:text-white hover:bg-white/5"
                    : "text-gray-600 hover:text-gray-900 hover:bg-gray-100"
                }`}
              >
                {isActive && (
                  <motion.div
                    layoutId="activeIndicator"
                    className="absolute left-0 top-0 bottom-0 w-0.5 bg-gradient-to-b from-cyan-400 to-fuchsia-500 rounded-full"
                  />
                )}
                <item.icon className="w-5 h-5 flex-shrink-0" />
                {!isCollapsed && (
                  <span className="font-medium text-sm">{item.label}</span>
                )}
                {isCollapsed && (
                  <div
                    className={`absolute left-full ml-2 px-2 py-1 rounded-md text-sm font-medium whitespace-nowrap opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity ${
                      theme === "dark" ? "bg-[#1a1a24] text-white" : "bg-gray-900 text-white"
                    }`}
                  >
                    {item.label}
                  </div>
                )}
              </Link>
            );
          })}
        </nav>

        {/* Bottom Navigation */}
        <div className="px-3 py-4 border-t border-[#2a2a35] space-y-1">
          {bottomItems.map((item, index) => {
            if (item.onClick) {
              return (
                <button
                  key={index}
                  onClick={item.onClick}
                  className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all group ${
                    theme === "dark"
                      ? "text-gray-400 hover:text-white hover:bg-white/5"
                      : "text-gray-600 hover:text-gray-900 hover:bg-gray-100"
                  }`}
                >
                  <item.icon className="w-5 h-5 flex-shrink-0" />
                  {!isCollapsed && (
                    <span className="font-medium text-sm">{item.label}</span>
                  )}
                  {isCollapsed && (
                    <div
                      className={`absolute left-full ml-2 px-2 py-1 rounded-md text-sm font-medium whitespace-nowrap opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity ${
                        theme === "dark" ? "bg-[#1a1a24] text-white" : "bg-gray-900 text-white"
                      }`}
                    >
                      {item.label}
                    </div>
                  )}
                </button>
              );
            }
            return (
              <Link
                key={item.href}
                href={item.href!}
                className={`flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all group ${
                  theme === "dark"
                    ? "text-gray-400 hover:text-white hover:bg-white/5"
                    : "text-gray-600 hover:text-gray-900 hover:bg-gray-100"
                }`}
              >
                <item.icon className="w-5 h-5 flex-shrink-0" />
                {!isCollapsed && (
                  <span className="font-medium text-sm">{item.label}</span>
                )}
              </Link>
            );
          })}
        </div>
      </div>
    </aside>
  );
}
