'use client';

import Link from 'next/link';
import {
  FileText, Search, Share2, Youtube, Mail, ShoppingCart,
  Building, GraduationCap, Calculator, Shield, Users, Headphones,
  PenTool, Languages, Sparkles, Image, Video, Mic,
  Facebook, Instagram, Linkedin, Twitter, MessageCircle
} from 'lucide-react';

// Type pour l'outil
interface Tool {
  id: string;
  slug: string;
  name: { fr: string; ar: string; en: string };
  description: { fr: string; ar: string; en: string };
  category: string;
  credits: number;
  priority: 'critical' | 'high' | 'medium' | 'low';
  isAlgeriaExclusive?: boolean;
  icon?: string;
}

interface ToolCardProps {
  tool: Tool;
  lang?: 'fr' | 'ar' | 'en';
  basePath?: string;
}

// Map des icônes par catégorie et outil
const categoryIcons: Record<string, any> = {
  blog: FileText,
  seo: Search,
  social: Share2,
  youtube: Youtube,
  email: Mail,
  ecommerce: ShoppingCart,
  'admin-dz': Building,
  'education-dz': GraduationCap,
  'finance-dz': Calculator,
  'compliance-dz': Shield,
  hr: Users,
  support: Headphones,
  writing: PenTool,
  translation: Languages,
  images: Image,
  video: Video,
  audio: Mic,
};

const toolIcons: Record<string, any> = {
  // Social
  'facebook-post-generator': Facebook,
  'facebook-ad-copy': Facebook,
  'instagram-caption': Instagram,
  'instagram-bio': Instagram,
  'linkedin-post': Linkedin,
  'linkedin-headline': Linkedin,
  'twitter-tweet': Twitter,
  'twitter-thread': Twitter,
  'tiktok-script': MessageCircle,
};

export function ToolCard({ tool, lang = 'fr', basePath }: ToolCardProps) {
  const IconComponent = toolIcons[tool.id] || categoryIcons[tool.category] || Sparkles;

  const priorityStyles = {
    critical: { bg: 'bg-red-100', text: 'text-red-700', label: '🔥 Populaire' },
    high: { bg: 'bg-orange-100', text: 'text-orange-700', label: '⭐ Recommandé' },
    medium: { bg: 'bg-yellow-100', text: 'text-yellow-700', label: '' },
    low: { bg: 'bg-gray-100', text: 'text-gray-600', label: '' },
  };

  const priority = priorityStyles[tool.priority];
  const href = basePath ? `${basePath}/${tool.slug}` : `/tools/${tool.category}/${tool.slug}`;

  return (
    <Link href={href}>
      <div className="group relative bg-white border border-gray-200 rounded-xl p-5 hover:border-green-500 hover:shadow-lg transition-all duration-200 cursor-pointer h-full">

        {/* Badge Algérie Exclusif */}
        {tool.isAlgeriaExclusive && (
          <div className="absolute -top-2 -right-2 bg-green-600 text-white text-xs font-bold px-2 py-1 rounded-full flex items-center gap-1 shadow-md">
            🇩🇿 Exclusif
          </div>
        )}

        {/* Icône */}
        <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4 group-hover:bg-green-600 transition-colors">
          <IconComponent className="w-6 h-6 text-green-600 group-hover:text-white transition-colors" />
        </div>

        {/* Titre */}
        <h3 className="font-semibold text-gray-900 mb-2 group-hover:text-green-600 transition-colors">
          {tool.name[lang]}
        </h3>

        {/* Description */}
        <p className="text-sm text-gray-500 line-clamp-2 mb-4">
          {tool.description[lang]}
        </p>

        {/* Footer */}
        <div className="flex items-center justify-between mt-auto">
          {/* Crédits */}
          <span className="inline-flex items-center text-xs font-medium text-green-700 bg-green-50 px-2.5 py-1 rounded-full">
            {tool.credits} crédits
          </span>

          {/* Badge Priorité */}
          {priority.label && (
            <span className={`text-xs px-2 py-1 rounded-full ${priority.bg} ${priority.text}`}>
              {priority.label}
            </span>
          )}
        </div>
      </div>
    </Link>
  );
}

// Composant pour les statistiques
interface StatCardProps {
  number: string;
  label: string;
  color: 'blue' | 'purple' | 'green' | 'red' | 'orange';
}

export function StatCard({ number, label, color }: StatCardProps) {
  const colors = {
    blue: 'bg-blue-50 text-blue-700 border-blue-200',
    purple: 'bg-purple-50 text-purple-700 border-purple-200',
    green: 'bg-green-50 text-green-700 border-green-200',
    red: 'bg-red-50 text-red-700 border-red-200',
    orange: 'bg-orange-50 text-orange-700 border-orange-200',
  };

  return (
    <div className={`rounded-xl p-4 border ${colors[color]}`}>
      <div className="text-3xl font-bold mb-1">{number}</div>
      <div className="text-sm opacity-80">{label}</div>
    </div>
  );
}

// Composant pour le header de catégorie
interface CategoryHeaderProps {
  icon: any;
  title: string;
  description: string;
  toolCount: number;
  criticalCount?: number;
  isExclusive?: boolean;
}

export function CategoryHeader({ icon: Icon, title, description, toolCount, criticalCount, isExclusive }: CategoryHeaderProps) {
  return (
    <div className="mb-8">
      <div className="flex items-center gap-3 mb-2">
        <div className="w-12 h-12 bg-green-600 rounded-xl flex items-center justify-center">
          <Icon className="w-6 h-6 text-white" />
        </div>
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-3xl font-bold text-gray-900">{title}</h1>
            {isExclusive && (
              <span className="bg-green-100 text-green-700 px-2 py-1 rounded-full text-xs font-medium">
                🇩🇿 Exclusif Algérie
              </span>
            )}
          </div>
          <p className="text-gray-600">{description}</p>
        </div>
      </div>
      <div className="flex gap-2 mt-4">
        <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-medium">
          {toolCount} outils
        </span>
        {criticalCount && criticalCount > 0 && (
          <span className="bg-red-100 text-red-700 px-3 py-1 rounded-full text-sm font-medium">
            {criticalCount} populaires
          </span>
        )}
      </div>
    </div>
  );
}

export default ToolCard;
