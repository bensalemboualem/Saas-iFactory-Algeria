"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Play, Star, Clock, Sparkles } from "lucide-react";
import Link from "next/link";
import { useLocaleStore, useThemeStore } from "@/lib/store";
import { t, isRTL } from "@/lib/i18n";

interface Template {
  id: string;
  name: Record<string, string>;
  description: Record<string, string>;
  category: string;
  thumbnail: string;
  duration: string;
  credits: number;
  popular?: boolean;
}

const templates: Template[] = [
  {
    id: "1",
    name: { fr: "Pub Produit E-commerce", ar: "إعلان منتج تجارة إلكترونية", en: "E-commerce Product Ad" },
    description: { 
      fr: "Présentez vos produits avec des animations modernes et dynamiques",
      ar: "اعرض منتجاتك مع رسوم متحركة حديثة وديناميكية",
      en: "Showcase your products with modern and dynamic animations"
    },
    category: "E-commerce",
    thumbnail: "/templates/ecommerce.jpg",
    duration: "15s",
    credits: 15,
    popular: true,
  },
  {
    id: "2",
    name: { fr: "Story Instagram Promo", ar: "قصة إنستغرام ترويجية", en: "Instagram Story Promo" },
    description: { 
      fr: "Format vertical optimisé pour les stories avec call-to-action",
      ar: "تنسيق عمودي محسن للقصص مع دعوة للعمل",
      en: "Vertical format optimized for stories with call-to-action"
    },
    category: "Social Media",
    thumbnail: "/templates/story.jpg",
    duration: "10s",
    credits: 10,
  },
  {
    id: "3",
    name: { fr: "Intro YouTube", ar: "مقدمة يوتيوب", en: "YouTube Intro" },
    description: { 
      fr: "Intro professionnelle pour chaîne YouTube avec logo animé",
      ar: "مقدمة احترافية لقناة يوتيوب مع شعار متحرك",
      en: "Professional intro for YouTube channel with animated logo"
    },
    category: "YouTube",
    thumbnail: "/templates/youtube.jpg",
    duration: "5s",
    credits: 8,
  },
  {
    id: "4",
    name: { fr: "CAN 2025 - Match Preview", ar: "كان 2025 - معاينة المباراة", en: "CAN 2025 - Match Preview" },
    description: { 
      fr: "Template spécial CAN 2025 pour présenter les matchs à venir",
      ar: "قالب خاص بكان 2025 لعرض المباريات القادمة",
      en: "Special CAN 2025 template to present upcoming matches"
    },
    category: "Sport",
    thumbnail: "/templates/can2025.jpg",
    duration: "20s",
    credits: 20,
    popular: true,
  },
  {
    id: "5",
    name: { fr: "Immobilier - Visite Virtuelle", ar: "عقارات - جولة افتراضية", en: "Real Estate - Virtual Tour" },
    description: { 
      fr: "Présentez des biens immobiliers avec survol cinématique",
      ar: "اعرض العقارات مع تحليق سينمائي",
      en: "Present real estate with cinematic flyover"
    },
    category: "Immobilier",
    thumbnail: "/templates/realestate.jpg",
    duration: "30s",
    credits: 25,
  },
  {
    id: "6",
    name: { fr: "Restaurant - Menu du Jour", ar: "مطعم - قائمة اليوم", en: "Restaurant - Daily Menu" },
    description: { 
      fr: "Mettez en valeur vos plats avec des plans appétissants",
      ar: "أبرز أطباقك مع لقطات شهية",
      en: "Highlight your dishes with appetizing shots"
    },
    category: "Food",
    thumbnail: "/templates/food.jpg",
    duration: "15s",
    credits: 12,
  },
];

const categories = [
  { id: "all", label: { fr: "Tous", ar: "الكل", en: "All" } },
  { id: "e-commerce", label: { fr: "E-commerce", ar: "تجارة إلكترونية", en: "E-commerce" } },
  { id: "social", label: { fr: "Social Media", ar: "وسائل التواصل", en: "Social Media" } },
  { id: "youtube", label: { fr: "YouTube", ar: "يوتيوب", en: "YouTube" } },
  { id: "sport", label: { fr: "Sport", ar: "رياضة", en: "Sport" } },
  { id: "immobilier", label: { fr: "Immobilier", ar: "عقارات", en: "Real Estate" } },
  { id: "food", label: { fr: "Food", ar: "طعام", en: "Food" } },
];

export default function TemplatesPage() {
  const { locale } = useLocaleStore();
  const { theme } = useThemeStore();
  const rtl = isRTL(locale);
  const [selectedCategory, setSelectedCategory] = useState("all");

  const labels = {
    credits: { fr: 'crédits', ar: 'رصيد', en: 'credits' },
    use: { fr: 'Utiliser', ar: 'استخدام', en: 'Use' },
    popular: { fr: 'Populaire', ar: 'شائع', en: 'Popular' },
  };

  const filteredTemplates =
    selectedCategory === "all"
      ? templates
      : templates.filter(
          (t) => t.category.toLowerCase() === selectedCategory.toLowerCase()
        );

  return (
    <div className={`min-h-screen p-8 ${theme === 'dark' ? 'bg-[#0a0a0f] text-white' : 'bg-gray-50 text-gray-900'}`} dir={rtl ? 'rtl' : 'ltr'}>
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className={`text-3xl font-bold mb-2 ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
            {t("nav.templates", locale)}
          </h1>
          <p className={theme === 'dark' ? 'text-gray-400' : 'text-gray-600'}>
            {locale === 'ar' ? 'اختر قالبًا جاهزًا لبدء إنشاء الفيديو' : 
             locale === 'en' ? 'Choose a ready-made template to start creating your video' : 
             'Choisissez un modèle prêt à l\'emploi pour démarrer votre vidéo'}
          </p>
        </div>

        {/* Categories */}
        <div className="flex flex-wrap gap-2 mb-8">
          {categories.map((cat) => (
            <button
              key={cat.id}
              onClick={() => setSelectedCategory(cat.id)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
                selectedCategory === cat.id
                  ? "bg-gradient-to-r from-cyan-400 to-fuchsia-500 text-white"
                  : theme === 'dark' 
                    ? "bg-[#1a1a24] border border-[#2a2a35] hover:border-cyan-400" 
                    : "bg-white border border-gray-200 hover:border-cyan-500"
              }`}
            >
              {cat.label[locale]}
            </button>
          ))}
        </div>

        {/* Templates Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredTemplates.map((template, index) => (
            <motion.div
              key={template.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className={`group rounded-2xl overflow-hidden transition-colors border-2 ${
                theme === 'dark' 
                  ? "bg-[#141419] border-[#2a2a35] hover:border-cyan-400/50" 
                  : "bg-white border-gray-200 hover:border-cyan-500/50"
              }`}
            >
              {/* Preview */}
              <div className={`relative aspect-video ${theme === 'dark' ? 'bg-[#0a0a0f]' : 'bg-gray-100'}`}>
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
                
                {template.popular && (
                  <div className={`absolute top-3 ${rtl ? 'right-3' : 'left-3'} flex items-center gap-1 px-2 py-1 bg-gradient-to-r from-cyan-400 to-fuchsia-500 rounded-full text-white text-xs font-medium`}>
                    <Star className="w-3 h-3" />
                    {labels.popular[locale]}
                  </div>
                )}

                <div className={`absolute bottom-3 ${rtl ? 'right-3' : 'left-3'} flex items-center gap-1 px-2 py-1 bg-black/60 backdrop-blur rounded-full`}>
                  <Clock className="w-3 h-3 text-gray-300" />
                  <span className="text-xs text-gray-300">{template.duration}</span>
                </div>
                
                <button className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                  <div className="w-14 h-14 rounded-full bg-gradient-to-r from-cyan-400 to-fuchsia-500 flex items-center justify-center shadow-lg shadow-cyan-500/30">
                    <Play className="w-6 h-6 text-white fill-white" />
                  </div>
                </button>
              </div>

              {/* Content */}
              <div className="p-4">
                <div className="flex items-start justify-between mb-2">
                  <h3 className={`font-semibold ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
                    {template.name[locale]}
                  </h3>
                  <span className="text-sm text-cyan-400 font-medium">
                    {template.credits} {labels.credits[locale]}
                  </span>
                </div>
                <p className={`text-sm mb-4 ${theme === 'dark' ? 'text-gray-400' : 'text-gray-600'}`}>
                  {template.description[locale]}
                </p>
                <div className="flex items-center justify-between">
                  <span className={`text-xs px-2 py-1 rounded ${theme === 'dark' ? 'bg-[#0a0a0f] text-gray-400' : 'bg-gray-100 text-gray-500'}`}>
                    {template.category}
                  </span>
                  <Link
                    href={`/studio?template=${template.id}`}
                    className="flex items-center gap-1 text-sm text-cyan-400 hover:text-cyan-300 font-medium"
                  >
                    <Sparkles className="w-4 h-4" />
                    {labels.use[locale]}
                  </Link>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}
