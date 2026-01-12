"use client"

import * as React from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import {
  LayoutDashboard,
  Sparkles,
  FolderOpen,
  FileText,
  BarChart3,
  Settings,
  Video,
} from "lucide-react"

const navigation = [
  {
    name: "Dashboard",
    href: "/",
    icon: LayoutDashboard,
    description: "Vue d'ensemble et statistiques",
  },
  {
    name: "Studio",
    href: "/studio",
    icon: Sparkles,
    description: "Créer une nouvelle vidéo",
  },
  {
    name: "Bibliothèque",
    href: "/library",
    icon: FolderOpen,
    description: "Mes vidéos générées",
  },
  {
    name: "Templates",
    href: "/templates",
    icon: FileText,
    description: "Modèles prédéfinis",
  },
  {
    name: "Analytics",
    href: "/analytics",
    icon: BarChart3,
    description: "Statistiques d'utilisation",
  },
  {
    name: "Paramètres",
    href: "/settings",
    icon: Settings,
    description: "Configuration",
  },
]

export function AppSidebar() {
  const pathname = usePathname()

  return (
    <div className="flex h-full w-64 flex-col border-r bg-card">
      {/* Logo */}
      <div className="flex h-16 items-center gap-2 border-b px-6">
        <Video className="h-6 w-6 text-primary" />
        <div className="flex flex-col">
          <span className="text-sm font-semibold">Dzir IA Video</span>
          <span className="text-xs text-muted-foreground">Studio Pro</span>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-1 p-4">
        {navigation.map((item) => {
          const isActive = pathname === item.href
          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                isActive
                  ? "bg-primary text-primary-foreground"
                  : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
              )}
            >
              <item.icon className="h-5 w-5" />
              <div className="flex flex-col">
                <span>{item.name}</span>
                {!isActive && (
                  <span className="text-xs opacity-70">{item.description}</span>
                )}
              </div>
            </Link>
          )
        })}
      </nav>

      {/* Footer - Quota Info */}
      <div className="border-t p-4">
        <div className="rounded-lg bg-muted p-3">
          <div className="flex items-center justify-between text-xs">
            <span className="text-muted-foreground">Quota du jour</span>
            <span className="font-semibold text-primary">6,100 vidéos</span>
          </div>
          <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-background">
            <div className="h-full w-[15%] bg-primary" />
          </div>
          <p className="mt-1 text-xs text-muted-foreground">
            15% utilisé · 10 générateurs actifs
          </p>
        </div>
      </div>
    </div>
  )
}
