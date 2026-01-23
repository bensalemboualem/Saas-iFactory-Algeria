"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Play, Download, Trash2, MoreVertical, Calendar, Clock } from "lucide-react";
import { useLocaleStore, useThemeStore } from "@/lib/store";
import { t, isRTL } from "@/lib/i18n";

interface Project {
  id: string;
  name: Record<string, string>;
  thumbnail: string;
  status: "completed" | "processing" | "failed";
  createdAt: string;
  duration: string;
  type: "text-to-video" | "image-to-video";
}

const projects: Project[] = [
  {
    id: "1",
    name: { fr: "Promo Ramadan 2025", ar: "إعلان رمضان 2025", en: "Ramadan 2025 Promo" },
    thumbnail: "/projects/ramadan.jpg",
    status: "completed",
    createdAt: "2024-12-19",
    duration: "15s",
    type: "text-to-video",
  },
  {
    id: "2",
    name: { fr: "Story Instagram - Nouveau produit", ar: "ستوري انستغرام - منتج جديد", en: "Instagram Story - New Product" },
    thumbnail: "/projects/story.jpg",
    status: "completed",
    createdAt: "2024-12-18",
    duration: "10s",
    type: "image-to-video",
  },
  {
    id: "3",
    name: { fr: "Intro chaîne YouTube", ar: "مقدمة قناة يوتيوب", en: "YouTube Channel Intro" },
    thumbnail: "/projects/intro.jpg",
    status: "processing",
    createdAt: "2024-12-19",
    duration: "5s",
    type: "text-to-video",
  },
];

export default function ProjectsPage() {
  const { locale } = useLocaleStore();
  const { theme } = useThemeStore();
  const rtl = isRTL(locale);
  const [selectedProjects, setSelectedProjects] = useState<string[]>([]);

  const toggleSelect = (id: string) => {
    setSelectedProjects((prev) =>
      prev.includes(id) ? prev.filter((p) => p !== id) : [...prev, id]
    );
  };

  const getStatusBadge = (status: Project["status"]) => {
    const labels = {
      completed: { fr: 'Terminé', ar: 'مكتمل', en: 'Completed' },
      processing: { fr: 'En cours...', ar: 'قيد المعالجة...', en: 'Processing...' },
      failed: { fr: 'Échoué', ar: 'فشل', en: 'Failed' }
    };
    
    switch (status) {
      case "completed":
        return (
          <span className="px-2 py-1 text-xs font-medium bg-green-500/20 text-green-400 rounded-full">
            {labels.completed[locale]}
          </span>
        );
      case "processing":
        return (
          <span className="px-2 py-1 text-xs font-medium bg-yellow-500/20 text-yellow-400 rounded-full animate-pulse">
            {labels.processing[locale]}
          </span>
        );
      case "failed":
        return (
          <span className="px-2 py-1 text-xs font-medium bg-red-500/20 text-red-400 rounded-full">
            {labels.failed[locale]}
          </span>
        );
    }
  };

  const labels = {
    noProjects: { fr: 'Aucun projet', ar: 'لا توجد مشاريع', en: 'No projects' },
    createFirst: { fr: 'Créez votre première vidéo dans le Studio', ar: 'أنشئ أول فيديو لك في الاستوديو', en: 'Create your first video in the Studio' },
    goToStudio: { fr: 'Aller au Studio', ar: 'اذهب للاستوديو', en: 'Go to Studio' },
    download: { fr: 'Télécharger', ar: 'تحميل', en: 'Download' },
    delete: { fr: 'Supprimer', ar: 'حذف', en: 'Delete' },
  };

  return (
    <div className={`min-h-screen p-8 ${theme === 'dark' ? 'bg-[#0a0a0f] text-white' : 'bg-gray-50 text-gray-900'}`} dir={rtl ? 'rtl' : 'ltr'}>
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className={`text-3xl font-bold mb-2 ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
              {t("nav.projects", locale)}
            </h1>
            <p className={theme === 'dark' ? 'text-gray-400' : 'text-gray-600'}>
              {locale === 'ar' ? 'جميع فيديوهاتك المُنشأة' : 
               locale === 'en' ? 'All your generated videos' : 
               'Toutes vos vidéos générées'}
            </p>
          </div>
          {selectedProjects.length > 0 && (
            <button className="flex items-center gap-2 px-4 py-2 bg-red-500 hover:bg-red-600 rounded-lg font-medium text-white">
              <Trash2 className="w-4 h-4" />
              {labels.delete[locale]} ({selectedProjects.length})
            </button>
          )}
        </div>

        {projects.length === 0 ? (
          <div className="text-center py-20">
            <div className={`w-20 h-20 rounded-full mx-auto mb-6 flex items-center justify-center ${theme === 'dark' ? 'bg-[#1a1a24]' : 'bg-gray-200'}`}>
              <Play className={`w-10 h-10 ${theme === 'dark' ? 'text-gray-500' : 'text-gray-400'}`} />
            </div>
            <h2 className={`text-xl font-semibold mb-2 ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
              {labels.noProjects[locale]}
            </h2>
            <p className={`mb-6 ${theme === 'dark' ? 'text-gray-400' : 'text-gray-600'}`}>
              {labels.createFirst[locale]}
            </p>
            <a
              href="/studio"
              className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-cyan-400 to-fuchsia-500 text-white rounded-xl font-medium hover:shadow-lg hover:shadow-cyan-500/30 transition-all"
            >
              {labels.goToStudio[locale]}
            </a>
          </div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {projects.map((project, index) => (
              <motion.div
                key={project.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className={`group rounded-2xl overflow-hidden transition-colors border-2 ${
                  selectedProjects.includes(project.id)
                    ? "border-cyan-400"
                    : theme === 'dark' 
                      ? "bg-[#141419] border-[#2a2a35] hover:border-cyan-400/50" 
                      : "bg-white border-gray-200 hover:border-cyan-500/50"
                }`}
              >
                {/* Thumbnail */}
                <div className={`relative aspect-video ${theme === 'dark' ? 'bg-[#0a0a0f]' : 'bg-gray-100'}`}>
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
                  
                  {/* Select checkbox */}
                  <button
                    onClick={() => toggleSelect(project.id)}
                    className={`absolute top-3 ${rtl ? 'right-3' : 'left-3'} w-6 h-6 rounded border-2 flex items-center justify-center transition-colors ${
                      selectedProjects.includes(project.id)
                        ? "bg-cyan-400 border-cyan-400"
                        : "border-white/50 hover:border-white"
                    }`}
                  >
                    {selectedProjects.includes(project.id) && (
                      <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path
                          fillRule="evenodd"
                          d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                          clipRule="evenodd"
                        />
                      </svg>
                    )}
                  </button>

                  {/* Status */}
                  <div className={`absolute top-3 ${rtl ? 'left-3' : 'right-3'}`}>
                    {getStatusBadge(project.status)}
                  </div>

                  {/* Play button */}
                  {project.status === "completed" && (
                    <button className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                      <div className="w-14 h-14 rounded-full bg-gradient-to-r from-cyan-400 to-fuchsia-500 flex items-center justify-center shadow-lg shadow-cyan-500/30">
                        <Play className="w-6 h-6 text-white fill-white" />
                      </div>
                    </button>
                  )}

                  {/* Duration */}
                  <div className={`absolute bottom-3 ${rtl ? 'right-3' : 'left-3'} flex items-center gap-1 px-2 py-1 bg-black/60 backdrop-blur rounded-full`}>
                    <Clock className="w-3 h-3 text-gray-300" />
                    <span className="text-xs text-gray-300">{project.duration}</span>
                  </div>
                </div>

                {/* Content */}
                <div className="p-4">
                  <div className="flex items-start justify-between mb-2">
                    <h3 className={`font-semibold truncate ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
                      {project.name[locale]}
                    </h3>
                    <button className={`p-1 rounded ${theme === 'dark' ? 'hover:bg-[#2a2a35]' : 'hover:bg-gray-100'}`}>
                      <MoreVertical className={`w-4 h-4 ${theme === 'dark' ? 'text-gray-500' : 'text-gray-400'}`} />
                    </button>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <div className={`flex items-center gap-1 text-sm ${theme === 'dark' ? 'text-gray-400' : 'text-gray-500'}`}>
                      <Calendar className="w-4 h-4" />
                      {new Date(project.createdAt).toLocaleDateString(locale === 'ar' ? 'ar-DZ' : locale === 'en' ? 'en-US' : 'fr-FR')}
                    </div>
                    
                    {project.status === "completed" && (
                      <button className="flex items-center gap-1 text-sm text-cyan-400 hover:text-cyan-300 font-medium">
                        <Download className="w-4 h-4" />
                        {labels.download[locale]}
                      </button>
                    )}
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
