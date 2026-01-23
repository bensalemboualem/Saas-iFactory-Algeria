"use client";

import { motion, AnimatePresence } from "framer-motion";
import { X, Sun, Moon, Globe, Check } from "lucide-react";
import { useThemeStore, useLocaleStore, useSettingsStore } from "@/lib/store";
import { t, locales, localeNames, localeFlags, Locale } from "@/lib/i18n";

export default function SettingsPanel() {
  const { theme, setTheme } = useThemeStore();
  const { locale, setLocale } = useLocaleStore();
  const { isOpen, close } = useSettingsStore();

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={close}
            className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm"
          />

          {/* Panel */}
          <motion.div
            initial={{ opacity: 0, x: 300 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 300 }}
            className={`fixed right-0 top-0 bottom-0 z-50 w-full max-w-md shadow-2xl overflow-y-auto ${
              theme === "dark" ? "bg-[#141419]" : "bg-white"
            }`}
          >
            {/* Header */}
            <div
              className={`sticky top-0 flex items-center justify-between px-6 py-4 border-b ${
                theme === "dark"
                  ? "bg-[#141419] border-[#2a2a35]"
                  : "bg-white border-gray-200"
              }`}
            >
              <h2
                className={`text-xl font-bold ${
                  theme === "dark" ? "text-white" : "text-gray-900"
                }`}
              >
                {t("settings.title", locale)}
              </h2>
              <button
                onClick={close}
                className={`p-2 rounded-lg transition-colors ${
                  theme === "dark"
                    ? "text-gray-400 hover:text-white hover:bg-white/5"
                    : "text-gray-500 hover:text-gray-900 hover:bg-gray-100"
                }`}
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-6 space-y-8">
              {/* Theme Section */}
              <div>
                <h3
                  className={`text-sm font-semibold uppercase tracking-wider mb-4 flex items-center gap-2 ${
                    theme === "dark" ? "text-gray-400" : "text-gray-500"
                  }`}
                >
                  <div className="w-0.5 h-4 bg-gradient-to-b from-cyan-400 to-fuchsia-500 rounded" />
                  {t("settings.theme", locale)}
                </h3>

                <div className="grid grid-cols-2 gap-3">
                  <button
                    onClick={() => setTheme("light")}
                    className={`flex items-center justify-center gap-3 px-4 py-4 rounded-xl border-2 transition-all ${
                      theme === "light"
                        ? "border-cyan-400 bg-cyan-400/10"
                        : "border-gray-700 hover:border-gray-600"
                    }`}
                  >
                    <Sun
                      className={`w-5 h-5 ${
                        theme === "light" ? "text-cyan-400" : "text-gray-400"
                      }`}
                    />
                    <span
                      className={
                        theme === "light" ? "text-cyan-400 font-semibold" : "text-gray-400"
                      }
                    >
                      {t("settings.light", locale)}
                    </span>
                    {theme === "light" && (
                      <Check className="w-4 h-4 text-cyan-400 ml-auto" />
                    )}
                  </button>

                  <button
                    onClick={() => setTheme("dark")}
                    className={`flex items-center justify-center gap-3 px-4 py-4 rounded-xl border-2 transition-all ${
                      theme === "dark"
                        ? "border-cyan-400 bg-cyan-400/10"
                        : "border-gray-300 hover:border-gray-400"
                    }`}
                  >
                    <Moon
                      className={`w-5 h-5 ${
                        theme === "dark" ? "text-cyan-400" : "text-gray-500"
                      }`}
                    />
                    <span
                      className={
                        theme === "dark" ? "text-cyan-400 font-semibold" : "text-gray-500"
                      }
                    >
                      {t("settings.dark", locale)}
                    </span>
                    {theme === "dark" && (
                      <Check className="w-4 h-4 text-cyan-400 ml-auto" />
                    )}
                  </button>
                </div>
              </div>

              {/* Language Section */}
              <div>
                <h3
                  className={`text-sm font-semibold uppercase tracking-wider mb-4 flex items-center gap-2 ${
                    theme === "dark" ? "text-gray-400" : "text-gray-500"
                  }`}
                >
                  <div className="w-0.5 h-4 bg-gradient-to-b from-cyan-400 to-fuchsia-500 rounded" />
                  {t("settings.language", locale)}
                </h3>

                <div className="space-y-2">
                  {locales.map((loc) => (
                    <button
                      key={loc}
                      onClick={() => setLocale(loc)}
                      className={`w-full flex items-center gap-4 px-4 py-3 rounded-xl border-2 transition-all ${
                        locale === loc
                          ? "border-cyan-400 bg-cyan-400/10"
                          : theme === "dark"
                          ? "border-[#2a2a35] hover:border-gray-600"
                          : "border-gray-200 hover:border-gray-300"
                      }`}
                    >
                      <span className="text-2xl">{localeFlags[loc]}</span>
                      <span
                        className={`flex-1 text-left font-medium ${
                          locale === loc
                            ? "text-cyan-400"
                            : theme === "dark"
                            ? "text-gray-300"
                            : "text-gray-700"
                        }`}
                      >
                        {localeNames[loc]}
                      </span>
                      {locale === loc && <Check className="w-5 h-5 text-cyan-400" />}
                    </button>
                  ))}
                </div>
              </div>

              {/* RTL Info */}
              {locale === "ar" && (
                <div
                  className={`p-4 rounded-xl ${
                    theme === "dark" ? "bg-[#1a1a24]" : "bg-gray-50"
                  }`}
                >
                  <p
                    className={`text-sm ${
                      theme === "dark" ? "text-gray-400" : "text-gray-600"
                    }`}
                  >
                    📝 اللغة العربية تستخدم اتجاه الكتابة من اليمين إلى اليسار (RTL)
                  </p>
                </div>
              )}
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
