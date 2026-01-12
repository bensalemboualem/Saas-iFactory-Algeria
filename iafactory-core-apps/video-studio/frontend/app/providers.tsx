"use client";

import { useEffect } from "react";
import { useThemeStore, useLocaleStore } from "@/lib/store";
import { isRTL } from "@/lib/i18n";

export default function ClientProviders({
  children,
}: {
  children: React.ReactNode;
}) {
  const { theme } = useThemeStore();
  const { locale } = useLocaleStore();

  useEffect(() => {
    // Apply theme
    document.documentElement.classList.remove("light", "dark");
    document.documentElement.classList.add(theme);
    document.documentElement.style.colorScheme = theme;
  }, [theme]);

  useEffect(() => {
    // Apply RTL for Arabic
    const rtl = isRTL(locale);
    document.documentElement.dir = rtl ? "rtl" : "ltr";
    document.documentElement.lang = locale;
  }, [locale]);

  return <>{children}</>;
}
