"use client";

import { Sidebar } from "@/components/layout";
import { useLocaleStore } from "@/lib/store";
import { isRTL } from "@/lib/i18n";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { locale } = useLocaleStore();
  const rtl = isRTL(locale);

  return (
    <div className="min-h-screen flex" dir={rtl ? "rtl" : "ltr"}>
      {/* Sidebar from layout components */}
      <Sidebar />
      
      {/* Main content - with margin for sidebar */}
      <main className="flex-1 ml-16 lg:ml-64 transition-all duration-300">
        {children}
      </main>
    </div>
  );
}
