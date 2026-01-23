'use client';

import { useState } from 'react';
import Link from 'next/link';
import { ArrowLeft, Play, Sparkles, Copy, Check, Loader2, FileText, ListOrdered, BookOpen, GitCompare, Star, FileSearch, HelpCircle, AlignLeft, Maximize, LayoutList, Building2, Newspaper, Link2, CheckCircle } from 'lucide-react';
import { blogTools } from '@/lib/tools-data';

interface PageProps {
  params: { toolSlug: string };
}

// Mapping des icônes
const iconMap: Record<string, any> = {
  'FileText': FileText,
  'ListOrdered': ListOrdered,
  'BookOpen': BookOpen,
  'GitCompare': GitCompare,
  'Star': Star,
  'FileSearch': FileSearch,
  'HelpCircle': HelpCircle,
  'AlignLeft': AlignLeft,
  'Maximize': Maximize,
  'LayoutList': LayoutList,
  'Building2': Building2,
  'Newspaper': Newspaper,
  'Link': Link2,
  'CheckCircle': CheckCircle,
  'Play': Play,
};

// Configuration des formulaires par outil
const toolFormConfigs: Record<string, { fields: any[], promptTemplate: string }> = {
  'blog-introduction': {
    fields: [
      { name: 'title', type: 'text', label: 'Titre de l\'article', required: true, placeholder: 'Ex: Les 10 meilleures pratiques SEO en 2025' },
      { name: 'topic', type: 'textarea', label: 'Sujet principal', required: true, placeholder: 'Décrivez le sujet de votre article...' },
      { name: 'hook_style', type: 'select', label: 'Style d\'accroche', options: ['Question', 'Statistique', 'Anecdote', 'Citation', 'Problème'] },
      { name: 'tone', type: 'select', label: 'Ton', options: ['Professionnel', 'Décontracté', 'Académique', 'Conversationnel'] },
    ],
    promptTemplate: `Écris une introduction captivante...`
  },
  'blog-conclusion': {
    fields: [
      { name: 'article_summary', type: 'textarea', label: 'Résumé des points clés', required: true, placeholder: 'Listez les points principaux de votre article...' },
      { name: 'cta_type', type: 'select', label: 'Type de CTA', options: ['Newsletter', 'Commentaire', 'Partage', 'Produit', 'Article suivant', 'Contact'] },
      { name: 'cta_details', type: 'text', label: 'Détails du CTA', placeholder: 'Lien, nom du produit...' },
    ],
    promptTemplate: `Écris une conclusion mémorable...`
  },
  'listicle-generator': {
    fields: [
      { name: 'topic', type: 'text', label: 'Sujet de la liste', required: true, placeholder: 'Ex: Outils de productivité' },
      { name: 'list_count', type: 'number', label: 'Nombre d\'éléments', placeholder: '10' },
      { name: 'format', type: 'select', label: 'Format', options: ['Top X', 'Meilleures', 'Erreurs à éviter', 'Astuces', 'Raisons', 'Façons'] },
      { name: 'depth', type: 'select', label: 'Profondeur', options: ['Court (100 mots)', 'Moyen (200 mots)', 'Détaillé (400 mots)'] },
    ],
    promptTemplate: `Crée un article listicle complet...`
  },
  'how-to-guide-generator': {
    fields: [
      { name: 'task', type: 'text', label: 'Tâche à accomplir', required: true, placeholder: 'Comment créer un site web...' },
      { name: 'audience_level', type: 'select', label: 'Niveau du public', options: ['Débutant', 'Intermédiaire', 'Avancé'] },
      { name: 'include_images', type: 'checkbox', label: 'Suggérer emplacements images' },
      { name: 'tools_needed', type: 'text', label: 'Outils/prérequis', placeholder: 'Optionnel' },
    ],
    promptTemplate: `Crée un guide pratique étape par étape...`
  },
  'comparison-article': {
    fields: [
      { name: 'item1', type: 'text', label: 'Élément 1', required: true, placeholder: 'Ex: WordPress' },
      { name: 'item2', type: 'text', label: 'Élément 2', required: true, placeholder: 'Ex: Wix' },
      { name: 'criteria', type: 'text', label: 'Critères de comparaison', placeholder: 'prix, facilité, performance...' },
      { name: 'recommendation', type: 'select', label: 'Recommandation', options: ['Oui claire', 'Oui nuancée', 'Non neutre'] },
    ],
    promptTemplate: `Crée un article comparatif objectif...`
  },
  'review-article': {
    fields: [
      { name: 'product', type: 'text', label: 'Produit/Service à tester', required: true, placeholder: 'Ex: ChatGPT Plus' },
      { name: 'category', type: 'text', label: 'Catégorie', placeholder: 'logiciel, téléphone, service...' },
      { name: 'rating', type: 'number', label: 'Note globale /10', placeholder: '8' },
      { name: 'tested_duration', type: 'text', label: 'Durée du test', placeholder: '2 semaines, 3 mois...' },
    ],
    promptTemplate: `Crée un article de test/avis complet...`
  },
  'case-study-writer': {
    fields: [
      { name: 'client', type: 'text', label: 'Client/Entreprise', required: true, placeholder: 'Nom de l\'entreprise' },
      { name: 'challenge', type: 'textarea', label: 'Problématique initiale', required: true, placeholder: 'Décrivez le défi...' },
      { name: 'solution', type: 'textarea', label: 'Solution apportée', required: true, placeholder: 'Décrivez la solution...' },
      { name: 'results', type: 'textarea', label: 'Résultats obtenus', required: true, placeholder: 'Chiffres, témoignages...' },
      { name: 'industry', type: 'text', label: 'Secteur d\'activité', placeholder: 'Tech, Finance, E-commerce...' },
    ],
    promptTemplate: `Crée une étude de cas professionnelle...`
  },
  'faq-article-generator': {
    fields: [
      { name: 'topic', type: 'text', label: 'Sujet principal', required: true, placeholder: 'Ex: Le marketing digital' },
      { name: 'questions_count', type: 'number', label: 'Nombre de questions', placeholder: '15' },
      { name: 'audience', type: 'text', label: 'Public cible', placeholder: 'débutants, professionnels...' },
      { name: 'include_schema', type: 'checkbox', label: 'Inclure le Schema FAQ (SEO)' },
    ],
    promptTemplate: `Crée un article FAQ complet...`
  },
  'paragraph-generator': {
    fields: [
      { name: 'topic', type: 'text', label: 'Sujet du paragraphe', required: true, placeholder: 'Ex: Les avantages du télétravail' },
      { name: 'context', type: 'textarea', label: 'Contexte (paragraphe précédent...)', placeholder: 'Optionnel' },
      { name: 'length', type: 'select', label: 'Longueur', options: ['Court (50 mots)', 'Moyen (100 mots)', 'Long (200 mots)'] },
      { name: 'purpose', type: 'select', label: 'Objectif', options: ['Informer', 'Convaincre', 'Expliquer', 'Illustrer'] },
    ],
    promptTemplate: `Génère un paragraphe de qualité...`
  },
  'content-expander': {
    fields: [
      { name: 'content', type: 'textarea', label: 'Contenu à développer', required: true, placeholder: 'Collez votre texte court ici...' },
      { name: 'expansion_factor', type: 'select', label: 'Facteur d\'expansion', options: ['x2', 'x3', 'x4'] },
      { name: 'add_elements', type: 'select', label: 'Éléments à ajouter', options: ['Exemples', 'Statistiques', 'Citations', 'Analogies', 'Questions'] },
    ],
    promptTemplate: `Développe ce contenu en le rendant plus riche...`
  },
  'blog-section-writer': {
    fields: [
      { name: 'section_title', type: 'text', label: 'Titre H2/H3', required: true, placeholder: 'Ex: Comment choisir le bon outil' },
      { name: 'main_topic', type: 'text', label: 'Sujet principal de l\'article', placeholder: 'Ex: Guide des outils SEO' },
      { name: 'key_points', type: 'textarea', label: 'Points clés à couvrir', placeholder: 'Point 1, Point 2...' },
      { name: 'word_count', type: 'number', label: 'Nombre de mots', placeholder: '300' },
    ],
    promptTemplate: `Rédige une section complète pour un article de blog...`
  },
  'content-brief-generator': {
    fields: [
      { name: 'topic', type: 'text', label: 'Sujet', required: true, placeholder: 'Ex: Le SEO local' },
      { name: 'target_keyword', type: 'text', label: 'Mot-clé cible', placeholder: 'Ex: seo local' },
      { name: 'competitors', type: 'textarea', label: 'URLs concurrents', placeholder: 'Optionnel' },
      { name: 'brand_voice', type: 'select', label: 'Voix de marque', options: ['Corporate', 'Startup', 'Expert', 'Friendly'] },
    ],
    promptTemplate: `Crée un brief de contenu détaillé...`
  },
  'pillar-content': {
    fields: [
      { name: 'main_topic', type: 'text', label: 'Sujet principal', required: true, placeholder: 'Ex: Le marketing de contenu' },
      { name: 'subtopics', type: 'textarea', label: 'Sous-sujets à couvrir', placeholder: 'Stratégie, SEO, Distribution...' },
      { name: 'word_count', type: 'number', label: 'Nombre de mots', placeholder: '5000' },
      { name: 'cluster_articles', type: 'textarea', label: 'Articles du cluster à lier', placeholder: 'URLs des articles liés...' },
    ],
    promptTemplate: `Crée un article pilier exhaustif...`
  },
  'news-article-writer': {
    fields: [
      { name: 'headline', type: 'text', label: 'Titre/Fait principal', required: true, placeholder: 'Ex: Apple annonce le nouvel iPhone' },
      { name: 'details', type: 'textarea', label: 'Détails connus', required: true, placeholder: 'Les informations principales...' },
      { name: 'sources', type: 'textarea', label: 'Sources (citations...)', placeholder: 'Optionnel' },
      { name: 'angle', type: 'select', label: 'Angle', options: ['Factuel', 'Analyse', 'Opinion', 'Investigation'] },
    ],
    promptTemplate: `Rédige un article d'actualité professionnel...`
  },
  'blog-ideas-from-url': {
    fields: [
      { name: 'url_content', type: 'textarea', label: 'Colle le contenu de l\'URL', required: true, placeholder: 'Collez le texte de la page ici...' },
      { name: 'ideas_count', type: 'number', label: 'Nombre d\'idées', placeholder: '10' },
      { name: 'content_type', type: 'select', label: 'Types de contenu', options: ['Article', 'Listicle', 'Guide', 'Comparaison', 'Étude de cas'] },
    ],
    promptTemplate: `Analyse ce contenu et génère des idées d'articles connexes...`
  },
  // ===== BATCH 3 - MEDIUM PRIORITY (10 outils) =====
  'tone-changer': {
    fields: [
      { name: 'text', type: 'textarea', label: 'Texte à transformer', required: true, placeholder: 'Collez votre texte ici...' },
      { name: 'current_tone', type: 'select', label: 'Ton actuel', options: ['Formel', 'Décontracté', 'Technique', 'Académique', 'Commercial'] },
      { name: 'target_tone', type: 'select', label: 'Ton cible', options: ['Formel', 'Décontracté', 'Conversationnel', 'Enthousiaste', 'Professionnel', 'Amical'] },
      { name: 'preserve_meaning', type: 'checkbox', label: 'Préserver le sens exact' },
    ],
    promptTemplate: `Transforme le ton de ce texte de {{current_tone}} vers {{target_tone}} en préservant le message...`
  },
  'blog-meta-description': {
    fields: [
      { name: 'title', type: 'text', label: 'Titre de l\'article', required: true, placeholder: 'Ex: Guide complet du SEO local' },
      { name: 'main_keyword', type: 'text', label: 'Mot-clé principal', required: true, placeholder: 'Ex: SEO local' },
      { name: 'article_summary', type: 'textarea', label: 'Résumé de l\'article', placeholder: 'Points clés de votre article...' },
      { name: 'cta_type', type: 'select', label: 'Type d\'appel à l\'action', options: ['Découvrez', 'Apprenez', 'Téléchargez', 'Commencez', 'Aucun'] },
    ],
    promptTemplate: `Génère 5 meta descriptions de 155 caractères max optimisées pour le CTR avec le mot-clé {{main_keyword}}...`
  },
  'blog-intro-hook': {
    fields: [
      { name: 'topic', type: 'text', label: 'Sujet de l\'article', required: true, placeholder: 'Ex: Les tendances marketing 2026' },
      { name: 'hook_type', type: 'select', label: 'Type d\'accroche', options: ['Question provocante', 'Statistique choc', 'Anecdote', 'Citation', 'Fait surprenant', 'Problème commun'] },
      { name: 'audience', type: 'text', label: 'Public cible', placeholder: 'Ex: entrepreneurs débutants' },
      { name: 'variants', type: 'number', label: 'Nombre de variantes', placeholder: '5' },
    ],
    promptTemplate: `Génère {{variants}} accroches {{hook_type}} pour un article sur {{topic}} ciblant {{audience}}...`
  },
  'sentence-rewriter': {
    fields: [
      { name: 'sentence', type: 'textarea', label: 'Phrase(s) à réécrire', required: true, placeholder: 'Entrez une ou plusieurs phrases...' },
      { name: 'variants_count', type: 'number', label: 'Nombre de variantes', placeholder: '5' },
      { name: 'style', type: 'select', label: 'Style de réécriture', options: ['Plus simple', 'Plus élaboré', 'Plus court', 'Plus formel', 'Plus engageant'] },
      { name: 'preserve_keywords', type: 'text', label: 'Mots-clés à conserver', placeholder: 'mot1, mot2... (optionnel)' },
    ],
    promptTemplate: `Réécris cette phrase en {{variants_count}} variantes différentes, style {{style}}...`
  },
  'text-completer': {
    fields: [
      { name: 'incomplete_text', type: 'textarea', label: 'Texte inachevé', required: true, placeholder: 'Collez votre paragraphe à compléter...' },
      { name: 'context', type: 'textarea', label: 'Contexte (paragraphes précédents)', placeholder: 'Optionnel - aide à la cohérence' },
      { name: 'target_length', type: 'select', label: 'Longueur de la complétion', options: ['1-2 phrases', '1 paragraphe', '2-3 paragraphes'] },
      { name: 'tone', type: 'select', label: 'Ton', options: ['Professionnel', 'Décontracté', 'Académique', 'Technique'] },
    ],
    promptTemplate: `Complète ce texte de manière naturelle et cohérente, en {{target_length}}, ton {{tone}}...`
  },
  'grammar-checker': {
    fields: [
      { name: 'text', type: 'textarea', label: 'Texte à corriger', required: true, placeholder: 'Collez votre texte ici...' },
      { name: 'language', type: 'select', label: 'Langue', options: ['Français', 'Anglais', 'Arabe', 'Darija'] },
      { name: 'check_level', type: 'select', label: 'Niveau de vérification', options: ['Basique (fautes)', 'Standard (+ style)', 'Avancé (+ suggestions)'] },
      { name: 'show_explanations', type: 'checkbox', label: 'Afficher les explications' },
    ],
    promptTemplate: `Analyse et corrige ce texte en {{language}}, niveau {{check_level}}. Montre chaque correction avec explication...`
  },
  'bullet-point-generator': {
    fields: [
      { name: 'text', type: 'textarea', label: 'Texte à transformer', required: true, placeholder: 'Collez le paragraphe ou texte à structurer...' },
      { name: 'bullet_style', type: 'select', label: 'Style de puces', options: ['Points clés', 'Avantages', 'Étapes', 'Caractéristiques', 'Résumé'] },
      { name: 'max_bullets', type: 'number', label: 'Nombre max de puces', placeholder: '7' },
      { name: 'include_intro', type: 'checkbox', label: 'Inclure phrase d\'introduction' },
    ],
    promptTemplate: `Transforme ce texte en liste à puces {{bullet_style}}, max {{max_bullets}} points...`
  },
  'pros-cons-generator': {
    fields: [
      { name: 'subject', type: 'text', label: 'Sujet à analyser', required: true, placeholder: 'Ex: Télétravail, iPhone 15, WordPress...' },
      { name: 'context', type: 'textarea', label: 'Contexte/Critères', placeholder: 'Ex: pour une startup, pour débutants...' },
      { name: 'points_count', type: 'number', label: 'Nombre de points par catégorie', placeholder: '5' },
      { name: 'include_verdict', type: 'checkbox', label: 'Inclure verdict final' },
    ],
    promptTemplate: `Génère une liste équilibrée de {{points_count}} avantages et {{points_count}} inconvénients pour {{subject}}...`
  },
  'faq-answers': {
    fields: [
      { name: 'questions', type: 'textarea', label: 'Questions (une par ligne)', required: true, placeholder: 'Question 1?\nQuestion 2?\nQuestion 3?' },
      { name: 'topic_context', type: 'text', label: 'Contexte/Sujet', placeholder: 'Ex: e-commerce en Algérie' },
      { name: 'answer_length', type: 'select', label: 'Longueur des réponses', options: ['Courte (2-3 phrases)', 'Moyenne (1 paragraphe)', 'Détaillée (2 paragraphes)'] },
      { name: 'include_schema', type: 'checkbox', label: 'Générer Schema FAQ JSON-LD' },
    ],
    promptTemplate: `Génère des réponses {{answer_length}} pour ces FAQ sur {{topic_context}}...`
  },
  'keyword-extractor': {
    fields: [
      { name: 'text', type: 'textarea', label: 'Texte à analyser', required: true, placeholder: 'Collez votre article ou texte...' },
      { name: 'keywords_count', type: 'number', label: 'Nombre de mots-clés', placeholder: '15' },
      { name: 'keyword_type', type: 'select', label: 'Type de mots-clés', options: ['Principaux', 'Longue traîne', 'LSI (sémantiques)', 'Tous'] },
      { name: 'include_density', type: 'checkbox', label: 'Inclure densité/fréquence' },
    ],
    promptTemplate: `Extrait {{keywords_count}} mots-clés {{keyword_type}} de ce texte avec analyse de pertinence...`
  },
};

// Config par défaut pour les outils sans config spécifique
const defaultFormConfig = {
  fields: [
    { name: 'input', type: 'textarea', label: 'Votre demande', required: true, placeholder: 'Décrivez ce que vous souhaitez générer...' },
    { name: 'tone', type: 'select', label: 'Ton', options: ['Professionnel', 'Décontracté', 'Académique', 'Conversationnel'] },
    { name: 'language', type: 'select', label: 'Langue', options: ['Français', 'Arabe', 'Anglais', 'Darija'] },
  ],
  promptTemplate: `Génère du contenu basé sur cette demande...`
};

export default function ToolExecutionPage({ params }: PageProps) {
  const tool = blogTools.find(t => t.slug === params.toolSlug);
  const [formData, setFormData] = useState<Record<string, string>>({});
  const [result, setResult] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  if (!tool) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Outil non trouvé</h1>
          <p className="text-gray-500 mb-4">L'outil "{params.toolSlug}" n'existe pas.</p>
          <Link href="/tools/blog" className="text-green-600 hover:underline">
            Retour aux outils Blog
          </Link>
        </div>
      </div>
    );
  }

  const formConfig = toolFormConfigs[tool.slug] || defaultFormConfig;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setResult('');

    // Simulation API - En production, appeler le gateway
    setTimeout(() => {
      const mockResult = `# Résultat généré par ${tool.name.fr}

## Contenu Généré

Voici le contenu généré basé sur vos paramètres:

${Object.entries(formData).map(([key, value]) => `**${key}**: ${value}`).join('\n')}

---

### Introduction

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.

### Points Clés

1. **Point 1**: Analyse approfondie du sujet avec données et statistiques
2. **Point 2**: Recommandations pratiques et actionnables
3. **Point 3**: Conclusion et prochaines étapes à suivre

### Conclusion

Ce contenu a été généré par IAFactory Algeria. N'hésitez pas à le modifier selon vos besoins spécifiques.

---
*Généré avec ${tool.credits} crédits • ${new Date().toLocaleDateString('fr-FR')}*`;

      setResult(mockResult);
      setIsLoading(false);
    }, 2500);
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(result);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const priorityColors = {
    critical: 'bg-red-100 text-red-700',
    high: 'bg-orange-100 text-orange-700',
    medium: 'bg-yellow-100 text-yellow-700',
    low: 'bg-gray-100 text-gray-700',
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-50">
        <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href="/tools/blog" className="text-gray-400 hover:text-gray-600">
              <ArrowLeft className="w-5 h-5" />
            </Link>
            <Link href="/" className="flex items-center gap-2">
              <span className="text-2xl font-bold text-green-600">IAFactory</span>
              <span className="text-sm bg-green-100 text-green-800 px-2 py-0.5 rounded">Algeria</span>
            </Link>
          </div>
          <div className="flex items-center gap-4">
            <div className="bg-gray-100 px-3 py-1.5 rounded-lg text-sm">
              <span className="text-gray-500">Crédits:</span>
              <span className="font-semibold text-gray-900 ml-1">847</span>
            </div>
          </div>
        </nav>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-8">
        {/* Tool Header */}
        <div className="bg-white rounded-xl p-6 shadow-sm mb-6">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-2">
                <h1 className="text-2xl font-bold text-gray-900">{tool.name.fr}</h1>
                <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${priorityColors[tool.priority]}`}>
                  {tool.priority}
                </span>
              </div>
              <p className="text-gray-600 mb-3">{tool.description.fr}</p>
              <div className="flex items-center gap-4 text-sm text-gray-500">
                <span>Catégorie: <strong className="text-gray-700">{tool.subcategory}</strong></span>
                <span>•</span>
                <span>ID: <code className="bg-gray-100 px-1 rounded">{tool.id}</code></span>
              </div>
            </div>
            <div className="bg-green-50 text-green-700 px-4 py-2 rounded-lg font-semibold text-lg">
              {tool.credits} crédits
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Form */}
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-green-600" />
              Paramètres
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              {formConfig.fields.map((field: any) => (
                <div key={field.name}>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    {field.label}
                    {field.required && <span className="text-red-500 ml-1">*</span>}
                  </label>
                  {field.type === 'textarea' ? (
                    <textarea
                      name={field.name}
                      placeholder={field.placeholder}
                      rows={4}
                      required={field.required}
                      className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:border-green-500 focus:ring-2 focus:ring-green-200 transition resize-none"
                      value={formData[field.name] || ''}
                      onChange={(e) => setFormData({ ...formData, [field.name]: e.target.value })}
                    />
                  ) : field.type === 'select' ? (
                    <select
                      name={field.name}
                      className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:border-green-500 focus:ring-2 focus:ring-green-200 transition"
                      value={formData[field.name] || ''}
                      onChange={(e) => setFormData({ ...formData, [field.name]: e.target.value })}
                    >
                      <option value="">Sélectionner...</option>
                      {field.options?.map((opt: string) => (
                        <option key={opt} value={opt}>{opt}</option>
                      ))}
                    </select>
                  ) : field.type === 'checkbox' ? (
                    <label className="flex items-center gap-2">
                      <input
                        type="checkbox"
                        name={field.name}
                        className="w-4 h-4 text-green-600 border-gray-300 rounded focus:ring-green-500"
                        checked={formData[field.name] === 'true'}
                        onChange={(e) => setFormData({ ...formData, [field.name]: e.target.checked ? 'true' : 'false' })}
                      />
                      <span className="text-sm text-gray-600">{field.label}</span>
                    </label>
                  ) : field.type === 'number' ? (
                    <input
                      type="number"
                      name={field.name}
                      placeholder={field.placeholder}
                      min={field.min}
                      max={field.max}
                      className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:border-green-500 focus:ring-2 focus:ring-green-200 transition"
                      value={formData[field.name] || ''}
                      onChange={(e) => setFormData({ ...formData, [field.name]: e.target.value })}
                    />
                  ) : (
                    <input
                      type="text"
                      name={field.name}
                      placeholder={field.placeholder}
                      required={field.required}
                      className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:border-green-500 focus:ring-2 focus:ring-green-200 transition"
                      value={formData[field.name] || ''}
                      onChange={(e) => setFormData({ ...formData, [field.name]: e.target.value })}
                    />
                  )}
                </div>
              ))}
              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-green-600 text-white py-3 rounded-lg font-semibold hover:bg-green-700 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Génération en cours...
                  </>
                ) : (
                  <>
                    <Play className="w-5 h-5" />
                    Générer ({tool.credits} crédits)
                  </>
                )}
              </button>
            </form>
          </div>

          {/* Result */}
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold">Résultat</h2>
              {result && (
                <button
                  onClick={copyToClipboard}
                  className="flex items-center gap-1 text-sm text-gray-600 hover:text-green-600 transition px-3 py-1 rounded-lg hover:bg-gray-50"
                >
                  {copied ? (
                    <>
                      <Check className="w-4 h-4" />
                      Copié !
                    </>
                  ) : (
                    <>
                      <Copy className="w-4 h-4" />
                      Copier
                    </>
                  )}
                </button>
              )}
            </div>
            <div className="bg-gray-50 rounded-lg p-4 min-h-[450px] max-h-[600px] overflow-y-auto">
              {isLoading ? (
                <div className="flex items-center justify-center h-full">
                  <div className="text-center">
                    <Loader2 className="w-8 h-8 text-green-600 animate-spin mx-auto mb-2" />
                    <p className="text-gray-500">Génération en cours...</p>
                    <p className="text-sm text-gray-400 mt-1">Cela peut prendre quelques secondes</p>
                  </div>
                </div>
              ) : result ? (
                <div className="prose prose-sm max-w-none">
                  <pre className="whitespace-pre-wrap font-sans text-gray-700 text-sm leading-relaxed">{result}</pre>
                </div>
              ) : (
                <div className="flex items-center justify-center h-full text-gray-400">
                  <div className="text-center">
                    <FileText className="w-12 h-12 mx-auto mb-2 opacity-30" />
                    <p>Le résultat apparaîtra ici</p>
                    <p className="text-sm mt-1">Remplissez le formulaire et cliquez sur Générer</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Tips Section */}
        <div className="mt-6 bg-blue-50 rounded-xl p-6 border border-blue-100">
          <h3 className="font-semibold text-blue-900 mb-2">Conseils pour de meilleurs résultats</h3>
          <ul className="text-sm text-blue-800 space-y-1">
            <li>• Soyez précis et détaillé dans vos descriptions</li>
            <li>• Utilisez des mots-clés pertinents pour votre audience</li>
            <li>• Testez différents tons pour trouver celui qui convient le mieux</li>
            <li>• N'hésitez pas à modifier et personnaliser le résultat généré</li>
          </ul>
        </div>
      </main>
    </div>
  );
}
