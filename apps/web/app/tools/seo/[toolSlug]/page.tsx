'use client';

import { useState } from 'react';
import Link from 'next/link';
import { ArrowLeft, Play, Sparkles, Copy, Check, Loader2, Search } from 'lucide-react';
import { seoTools } from '@/lib/tools-data';

interface PageProps {
  params: { toolSlug: string };
}

// Configuration des formulaires par outil SEO
const toolFormConfigs: Record<string, { fields: any[], promptTemplate: string }> = {
  // ===== BATCH 1 - CRITIQUE (7) =====
  'meta-tag-generator': {
    fields: [
      { name: 'page_title', type: 'text', label: 'Titre de la page', required: true, placeholder: 'Ex: Guide SEO complet pour débutants' },
      { name: 'page_content', type: 'textarea', label: 'Contenu/Description de la page', required: true, placeholder: 'Décrivez le contenu de votre page...' },
      { name: 'target_keyword', type: 'text', label: 'Mot-clé principal', required: true, placeholder: 'Ex: SEO débutant' },
      { name: 'secondary_keywords', type: 'text', label: 'Mots-clés secondaires', placeholder: 'mot1, mot2, mot3...' },
      { name: 'page_type', type: 'select', label: 'Type de page', options: ['Article', 'Page produit', 'Service', 'Accueil', 'Catégorie', 'Landing page'] },
    ],
    promptTemplate: `Génère des meta tags SEO complets avec Title, Description, OG Tags et Twitter Cards...`
  },
  'keyword-generator': {
    fields: [
      { name: 'seed_keyword', type: 'text', label: 'Mot-clé de base', required: true, placeholder: 'Ex: marketing digital' },
      { name: 'industry', type: 'text', label: 'Secteur d\'activité', placeholder: 'Ex: e-commerce, santé, tech...' },
      { name: 'location', type: 'text', label: 'Localisation', placeholder: 'Algérie' },
      { name: 'language', type: 'select', label: 'Langue', options: ['Français', 'Arabe', 'Anglais', 'Darija'] },
      { name: 'intent', type: 'select', label: 'Intention de recherche', options: ['Toutes', 'Informationnel', 'Transactionnel', 'Navigationnel', 'Commercial'] },
    ],
    promptTemplate: `Génère 50+ mots-clés organisés par intention, volume et difficulté...`
  },
  'longtail-keyword-generator': {
    fields: [
      { name: 'main_keyword', type: 'text', label: 'Mot-clé principal', required: true, placeholder: 'Ex: créer site web' },
      { name: 'count', type: 'number', label: 'Nombre de suggestions', placeholder: '30' },
      { name: 'include_questions', type: 'checkbox', label: 'Inclure les questions (Comment, Pourquoi...)' },
      { name: 'include_local', type: 'checkbox', label: 'Inclure variantes locales (Algérie, Alger...)' },
    ],
    promptTemplate: `Génère des mots-clés longue traîne avec questions, comparaisons et variantes locales...`
  },
  'meta-description-generator': {
    fields: [
      { name: 'page_title', type: 'text', label: 'Titre de la page', required: true, placeholder: 'Ex: Les 10 meilleurs outils SEO' },
      { name: 'keyword', type: 'text', label: 'Mot-clé cible', required: true, placeholder: 'Ex: outils SEO' },
      { name: 'page_type', type: 'select', label: 'Type de page', options: ['Article', 'Produit', 'Service', 'Accueil', 'Catégorie'] },
      { name: 'usp', type: 'text', label: 'Argument clé / USP', placeholder: 'Ex: Gratuit, Guide complet, Expert...' },
      { name: 'cta', type: 'select', label: 'Type de CTA', options: ['Découvrez', 'Achetez', 'Apprenez', 'Téléchargez', 'Contactez'] },
    ],
    promptTemplate: `Génère 5 meta descriptions de 155 caractères optimisées pour le CTR...`
  },
  'seo-content-optimizer': {
    fields: [
      { name: 'content', type: 'textarea', label: 'Contenu à optimiser', required: true, placeholder: 'Collez votre article ou texte ici...' },
      { name: 'target_keyword', type: 'text', label: 'Mot-clé cible', required: true, placeholder: 'Ex: SEO local' },
      { name: 'secondary_keywords', type: 'text', label: 'Mots-clés secondaires', placeholder: 'mot1, mot2, mot3...' },
    ],
    promptTemplate: `Analyse et optimise ce contenu : densité, structure, lisibilité, score SEO et version améliorée...`
  },
  'competitor-keyword-analyzer': {
    fields: [
      { name: 'competitor_content', type: 'textarea', label: 'Contenu du concurrent (copier-coller)', required: true, placeholder: 'Collez le contenu de la page concurrente...' },
      { name: 'competitor_url', type: 'text', label: 'URL du concurrent', placeholder: 'https://...' },
      { name: 'your_keyword', type: 'text', label: 'Votre mot-clé cible', required: true, placeholder: 'Ex: formation marketing' },
    ],
    promptTemplate: `Analyse le contenu concurrent : mots-clés, structure, forces, faiblesses et stratégie pour les battre...`
  },
  'schema-markup-generator': {
    fields: [
      { name: 'schema_type', type: 'select', label: 'Type de Schema', required: true, options: ['Article', 'Product', 'LocalBusiness', 'FAQ', 'HowTo', 'Recipe', 'Event', 'Organization', 'Person', 'Review'] },
      { name: 'content_data', type: 'textarea', label: 'Informations à structurer', required: true, placeholder: 'Titre, description, auteur, date, prix...' },
      { name: 'website_name', type: 'text', label: 'Nom du site', placeholder: 'Ex: IAFactory' },
      { name: 'website_url', type: 'text', label: 'URL du site', placeholder: 'https://iafactory.dz' },
    ],
    promptTemplate: `Génère le code JSON-LD complet pour Schema.org avec instructions d'implémentation...`
  },

  // ===== BATCH 2 - HAUTE PRIORITÉ (8) =====
  'title-tag-optimizer': {
    fields: [
      { name: 'current_title', type: 'text', label: 'Title actuel (optionnel)', placeholder: 'Votre title actuel...' },
      { name: 'keyword', type: 'text', label: 'Mot-clé cible', required: true, placeholder: 'Ex: agence web Algérie' },
      { name: 'brand', type: 'text', label: 'Nom de marque', placeholder: 'Ex: IAFactory' },
      { name: 'page_type', type: 'select', label: 'Type de page', options: ['Article', 'Produit', 'Service', 'Accueil'] },
    ],
    promptTemplate: `Génère 5 title tags de 60 caractères avec mot-clé et power words...`
  },
  'internal-linking-suggester': {
    fields: [
      { name: 'current_article', type: 'textarea', label: 'Article actuel', required: true, placeholder: 'Collez votre article...' },
      { name: 'site_pages', type: 'textarea', label: 'Liste de vos pages/articles', placeholder: 'Titre 1 - URL1\nTitre 2 - URL2...' },
      { name: 'max_links', type: 'number', label: 'Nombre max de liens', placeholder: '5' },
    ],
    promptTemplate: `Suggère les meilleurs liens internes avec textes d'ancre et emplacements...`
  },
  'url-slug-optimizer': {
    fields: [
      { name: 'page_title', type: 'text', label: 'Titre de la page', required: true, placeholder: 'Ex: Guide complet du SEO local en Algérie' },
      { name: 'keyword', type: 'text', label: 'Mot-clé cible', required: true, placeholder: 'Ex: SEO local Algérie' },
      { name: 'current_url', type: 'text', label: 'URL actuelle (si modification)', placeholder: '/ancien-slug' },
    ],
    promptTemplate: `Génère 5 URLs SEO-friendly courtes avec mot-clé et recommandation...`
  },
  'heading-structure-analyzer': {
    fields: [
      { name: 'content', type: 'textarea', label: 'Contenu avec titres', required: true, placeholder: 'Collez votre contenu avec les titres H1, H2, H3...' },
      { name: 'target_keyword', type: 'text', label: 'Mot-clé cible', placeholder: 'Ex: marketing digital' },
    ],
    promptTemplate: `Analyse la structure Hn : hiérarchie, problèmes, score et structure optimisée...`
  },
  'image-alt-generator': {
    fields: [
      { name: 'image_description', type: 'textarea', label: 'Description de l\'image', required: true, placeholder: 'Décrivez ce que montre l\'image...' },
      { name: 'page_keyword', type: 'text', label: 'Mot-clé de la page', placeholder: 'Ex: recette couscous' },
      { name: 'image_context', type: 'text', label: 'Contexte (section de l\'article)', placeholder: 'Ex: Section ingrédients' },
      { name: 'count', type: 'number', label: 'Nombre d\'images', placeholder: '1' },
    ],
    promptTemplate: `Génère alt text SEO, title, nom de fichier et légende pour chaque image...`
  },
  'content-gap-analyzer': {
    fields: [
      { name: 'your_content', type: 'textarea', label: 'Votre contenu actuel', required: true, placeholder: 'Collez votre article...' },
      { name: 'competitor_content', type: 'textarea', label: 'Contenu concurrent (top 3 Google)', required: true, placeholder: 'Collez le contenu des concurrents...' },
      { name: 'target_keyword', type: 'text', label: 'Mot-clé cible', required: true, placeholder: 'Ex: créer entreprise Algérie' },
    ],
    promptTemplate: `Identifie les lacunes : sujets manquants, questions, mots-clés et plan d'action...`
  },
  'seo-audit-checklist': {
    fields: [
      { name: 'page_url', type: 'text', label: 'URL de la page', required: true, placeholder: 'https://example.com/page' },
      { name: 'page_content', type: 'textarea', label: 'Contenu de la page', placeholder: 'Collez le contenu...' },
      { name: 'target_keyword', type: 'text', label: 'Mot-clé cible', required: true, placeholder: 'Ex: consultant SEO' },
    ],
    promptTemplate: `Génère une checklist d'audit SEO complète : On-Page, Technique, Contenu avec score...`
  },
  'serp-preview': {
    fields: [
      { name: 'title', type: 'text', label: 'Title Tag', required: true, placeholder: 'Votre title de 60 caractères...' },
      { name: 'url', type: 'text', label: 'URL', required: true, placeholder: 'https://example.com/page' },
      { name: 'description', type: 'textarea', label: 'Meta Description', required: true, placeholder: 'Votre description de 155 caractères...' },
      { name: 'rich_snippet', type: 'select', label: 'Rich Snippet', options: ['Aucun', 'FAQ', 'Rating', 'Breadcrumb', 'Sitelinks'] },
    ],
    promptTemplate: `Génère un aperçu SERP avec analyse CTR et optimisations suggérées...`
  },

  // ===== BATCH 3 - MOYENNE PRIORITÉ (5) =====
  'readability-analyzer': {
    fields: [
      { name: 'content', type: 'textarea', label: 'Contenu à analyser', required: true, placeholder: 'Collez votre texte...' },
      { name: 'target_audience', type: 'select', label: 'Public cible', options: ['Grand public', 'Professionnels', 'Experts', 'Étudiants'] },
      { name: 'language', type: 'select', label: 'Langue', options: ['Français', 'Anglais', 'Arabe'] },
    ],
    promptTemplate: `Analyse la lisibilité : Score Flesch, phrases, recommandations et version simplifiée...`
  },
  'keyword-density-checker': {
    fields: [
      { name: 'content', type: 'textarea', label: 'Contenu à analyser', required: true, placeholder: 'Collez votre article...' },
      { name: 'target_keyword', type: 'text', label: 'Mot-clé cible', required: true, placeholder: 'Ex: SEO' },
      { name: 'secondary_keywords', type: 'text', label: 'Mots-clés secondaires', placeholder: 'mot1, mot2...' },
    ],
    promptTemplate: `Analyse la densité des mots-clés avec recommandations (optimal 1-2%)...`
  },
  'anchor-text-optimizer': {
    fields: [
      { name: 'target_page', type: 'text', label: 'Page cible du lien', required: true, placeholder: 'https://example.com/page-cible' },
      { name: 'target_keyword', type: 'text', label: 'Mot-clé de la page cible', required: true, placeholder: 'Ex: formation SEO' },
      { name: 'current_anchors', type: 'textarea', label: 'Textes d\'ancre actuels (un par ligne)', placeholder: 'formation SEO\ncliquez ici\nen savoir plus...' },
      { name: 'count', type: 'number', label: 'Nombre de suggestions', placeholder: '10' },
    ],
    promptTemplate: `Génère des textes d'ancre variés pour un profil de liens naturel...`
  },
  'robots-txt-generator': {
    fields: [
      { name: 'website_url', type: 'text', label: 'URL du site', required: true, placeholder: 'https://example.com' },
      { name: 'site_type', type: 'select', label: 'Type de site', options: ['Blog/Magazine', 'E-commerce', 'Corporate', 'SaaS', 'Forum'] },
      { name: 'blocked_paths', type: 'textarea', label: 'Chemins à bloquer', placeholder: '/admin\n/private\n/tmp...' },
      { name: 'sitemap_url', type: 'text', label: 'URL du sitemap', placeholder: 'https://example.com/sitemap.xml' },
    ],
    promptTemplate: `Génère un fichier robots.txt optimisé avec explications...`
  },
  'sitemap-generator': {
    fields: [
      { name: 'pages', type: 'textarea', label: 'Liste des pages (URL par ligne)', required: true, placeholder: 'https://example.com/\nhttps://example.com/about\nhttps://example.com/blog...' },
      { name: 'website_url', type: 'text', label: 'URL du site', required: true, placeholder: 'https://example.com' },
      { name: 'default_frequency', type: 'select', label: 'Fréquence par défaut', options: ['daily', 'weekly', 'monthly', 'yearly'] },
      { name: 'include_images', type: 'checkbox', label: 'Inclure sitemap images' },
    ],
    promptTemplate: `Génère un sitemap XML complet avec priorités et fréquences...`
  },
};

// Config par défaut pour les outils sans config spécifique
const defaultFormConfig = {
  fields: [
    { name: 'input', type: 'textarea', label: 'Votre demande', required: true, placeholder: 'Décrivez ce que vous souhaitez analyser/générer...' },
    { name: 'keyword', type: 'text', label: 'Mot-clé cible', placeholder: 'Votre mot-clé principal' },
    { name: 'language', type: 'select', label: 'Langue', options: ['Français', 'Arabe', 'Anglais', 'Darija'] },
  ],
  promptTemplate: `Analyse et génère des recommandations SEO basées sur cette demande...`
};

export default function SeoToolExecutionPage({ params }: PageProps) {
  const tool = seoTools.find(t => t.slug === params.toolSlug);
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
          <Link href="/tools/seo" className="text-purple-600 hover:underline">
            Retour aux outils SEO
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
      const mockResult = `# Résultat - ${tool.name.fr}

## Analyse SEO Complète

**Paramètres utilisés:**
${Object.entries(formData).map(([key, value]) => `- **${key}**: ${value}`).join('\n')}

---

## Résultats

### Score SEO Global: 78/100

### Recommandations Principales

1. **Optimisation du Title Tag**
   - Longueur actuelle: OK (55 caractères)
   - Mot-clé positionné: ✅ Au début
   - Suggestion: Ajouter un power word

2. **Meta Description**
   - Longueur: 148/155 caractères ✅
   - CTA présent: ✅
   - Mot-clé inclus: ✅

3. **Structure des Titres**
   - H1 unique: ✅
   - Hiérarchie respectée: ✅
   - Mot-clé dans H2: ⚠️ À améliorer

### Code/Contenu Généré

\`\`\`html
<!-- Meta Tags générés -->
<title>Votre titre optimisé | Marque</title>
<meta name="description" content="Description optimisée...">
\`\`\`

---

### Prochaines Étapes
1. Implémenter les meta tags suggérés
2. Optimiser les titres H2
3. Ajouter des liens internes

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

  const subcategoryLabels: Record<string, string> = {
    'research': 'Recherche',
    'on-page': 'On-Page',
    'optimization': 'Optimisation',
    'technical': 'Technique',
    'analysis': 'Analyse',
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-50">
        <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href="/tools/seo" className="text-gray-400 hover:text-gray-600">
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
                <span>Catégorie: <strong className="text-purple-700">{subcategoryLabels[tool.subcategory || ''] || tool.subcategory}</strong></span>
                <span>•</span>
                <span>ID: <code className="bg-gray-100 px-1 rounded">{tool.id}</code></span>
              </div>
            </div>
            <div className="bg-purple-50 text-purple-700 px-4 py-2 rounded-lg font-semibold text-lg">
              {tool.credits} crédits
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Form */}
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-purple-600" />
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
                      className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:border-purple-500 focus:ring-2 focus:ring-purple-200 transition resize-none"
                      value={formData[field.name] || ''}
                      onChange={(e) => setFormData({ ...formData, [field.name]: e.target.value })}
                    />
                  ) : field.type === 'select' ? (
                    <select
                      name={field.name}
                      className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:border-purple-500 focus:ring-2 focus:ring-purple-200 transition"
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
                        className="w-4 h-4 text-purple-600 border-gray-300 rounded focus:ring-purple-500"
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
                      className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:border-purple-500 focus:ring-2 focus:ring-purple-200 transition"
                      value={formData[field.name] || ''}
                      onChange={(e) => setFormData({ ...formData, [field.name]: e.target.value })}
                    />
                  ) : (
                    <input
                      type="text"
                      name={field.name}
                      placeholder={field.placeholder}
                      required={field.required}
                      className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:border-purple-500 focus:ring-2 focus:ring-purple-200 transition"
                      value={formData[field.name] || ''}
                      onChange={(e) => setFormData({ ...formData, [field.name]: e.target.value })}
                    />
                  )}
                </div>
              ))}
              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-purple-600 text-white py-3 rounded-lg font-semibold hover:bg-purple-700 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Analyse en cours...
                  </>
                ) : (
                  <>
                    <Play className="w-5 h-5" />
                    Analyser ({tool.credits} crédits)
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
                  className="flex items-center gap-1 text-sm text-gray-600 hover:text-purple-600 transition px-3 py-1 rounded-lg hover:bg-gray-50"
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
                    <Loader2 className="w-8 h-8 text-purple-600 animate-spin mx-auto mb-2" />
                    <p className="text-gray-500">Analyse en cours...</p>
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
                    <Search className="w-12 h-12 mx-auto mb-2 opacity-30" />
                    <p>Le résultat apparaîtra ici</p>
                    <p className="text-sm mt-1">Remplissez le formulaire et cliquez sur Analyser</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Tips Section */}
        <div className="mt-6 bg-purple-50 rounded-xl p-6 border border-purple-100">
          <h3 className="font-semibold text-purple-900 mb-2">Conseils SEO</h3>
          <ul className="text-sm text-purple-800 space-y-1">
            <li>• Utilisez des mots-clés pertinents pour votre marché algérien</li>
            <li>• Pensez aux variantes en arabe et en darija</li>
            <li>• Visez un score SEO de 80+ pour un bon positionnement</li>
            <li>• Testez vos meta tags avec l'aperçu SERP avant publication</li>
          </ul>
        </div>
      </main>
    </div>
  );
}
