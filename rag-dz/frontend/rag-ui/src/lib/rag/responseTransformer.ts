/**
 * Transforme les réponses RAG brutes en format ithy-style
 * Pour IA Factory (Algérie/Suisse)
 */

import type {
  IthyResponseProps,
  Section,
  Source,
  FAQ,
  ChartData,
  ComparisonRow
} from '../../components/presentation/types';

interface RawRAGResponse {
  query: string;
  answer: string;
  sources?: RawSource[];
  chunks?: any[];
  confidence?: number;
  metadata?: any;
}

interface RawSource {
  title: string;
  text?: string;
  score?: number;
  metadata?: any;
}

/**
 * Transforme une réponse RAG brute en format ithy-style enrichi
 */
export function transformToIthyFormat(rawResponse: RawRAGResponse): IthyResponseProps {
  // 1. Générer le titre depuis la query
  const title = generateTitle(rawResponse.query);

  // 2. Structurer les sections
  const sections = generateSections(rawResponse);

  // 3. Extraire et formater les sources
  const sources = formatSources(rawResponse.sources || []);

  // 4. Générer les FAQ automatiquement
  const faqs = generateFAQs(rawResponse);

  // 5. Créer les charts si données comparatives détectées
  const charts = detectAndCreateCharts(rawResponse);

  return {
    title,
    sections,
    sources,
    faqs,
    charts,
    metadata: {
      generatedAt: new Date(),
      agents: ['RAG Agent'], // TODO: extraire agents réels si disponibles
      confidence: rawResponse.confidence || 0.75,
      language: detectPrimaryLanguage(rawResponse.query)
    }
  };
}

/**
 * Génère un titre propre depuis la query
 */
function generateTitle(query: string): string {
  // Nettoyer la query
  const cleaned = query
    .replace(/^(qu'est-ce que|what is|ما هو|comment|how|quels sont|quelle est)/i, '')
    .trim();

  // Capitaliser
  return cleaned.charAt(0).toUpperCase() + cleaned.slice(1);
}

/**
 * Génère les sections structurées
 */
function generateSections(response: RawRAGResponse): Section[] {
  const sections: Section[] = [];

  // Section résumé exécutif
  sections.push({
    id: 'executive-summary',
    type: 'text',
    title: '📋 Résumé',
    icon: '📋',
    content: formatTextContent(response.answer)
  });

  // Détecter si comparaison Algérie/Suisse nécessaire
  if (isComparativeQuery(response.query)) {
    const comparisonData = extractComparisonData(response);
    if (comparisonData.length > 0) {
      sections.push({
        id: 'comparison',
        type: 'table',
        title: '⚖️ Comparaison Algérie - Suisse',
        content: {
          title: 'Comparaison des critères',
          rows: comparisonData,
          showFlags: true
        }
      });
    }
  }

  // Section sources détaillées si pertinent
  if (response.chunks && response.chunks.length > 0) {
    const detailedContent = response.chunks
      .slice(0, 3)
      .map((chunk, i) => `<h4>Source ${i + 1}: ${chunk.metadata?.title || 'Document'}</h4><p>${chunk.text?.substring(0, 300)}...</p>`)
      .join('\n');

    sections.push({
      id: 'detailed-sources',
      type: 'text',
      title: '📖 Extraits Détaillés',
      icon: '📖',
      content: detailedContent
    });
  }

  return sections;
}

/**
 * Formate les sources brutes en format structuré
 */
function formatSources(rawSources: RawSource[]): Source[] {
  return rawSources.map((source, index) => ({
    id: `source-${index}`,
    title: source.title || `Document ${index + 1}`,
    type: detectSourceType(source),
    country: detectCountry(source),
    relevance: source.score || 0.5,
    reference: source.metadata?.reference,
    date: source.metadata?.date,
    url: source.metadata?.url
  }));
}

/**
 * Détecte le type de source (loi, décret, etc.)
 */
function detectSourceType(source: RawSource): Source['type'] {
  const title = source.title?.toLowerCase() || '';
  const text = source.text?.toLowerCase() || '';

  if (title.includes('loi') || text.includes('loi n°')) return 'law';
  if (title.includes('décret') || text.includes('décret')) return 'decree';
  if (title.includes('circulaire')) return 'circular';
  if (title.includes('jurisprudence') || title.includes('arrêt')) return 'jurisprudence';
  if (title.includes('officiel') || title.includes('jo')) return 'official';

  return 'academic';
}

/**
 * Détecte le pays de la source
 */
function detectCountry(source: RawSource): 'DZ' | 'CH' {
  const title = source.title?.toLowerCase() || '';
  const text = source.text?.toLowerCase() || '';
  const combined = title + ' ' + text;

  // Indices Algérie
  if (
    combined.includes('algérie') ||
    combined.includes('alger') ||
    combined.includes('dz') ||
    combined.includes('wilaya')
  ) {
    return 'DZ';
  }

  // Indices Suisse
  if (
    combined.includes('suisse') ||
    combined.includes('ch') ||
    combined.includes('confédération') ||
    combined.includes('canton')
  ) {
    return 'CH';
  }

  // Par défaut (probabilité plus élevée Algérie pour IA Factory)
  return 'DZ';
}

/**
 * Génère des FAQs pertinentes
 */
function generateFAQs(response: RawRAGResponse): FAQ[] {
  const faqs: FAQ[] = [];

  // FAQ basique si query longue
  if (response.query.length > 50) {
    faqs.push({
      question: "Puis-je obtenir plus de détails sur ce sujet ?",
      answer: "Oui, posez une question plus spécifique ou consultez les sources ci-dessous pour plus d'informations.",
      category: "Information"
    });
  }

  // FAQ spécifique aux comparaisons
  if (isComparativeQuery(response.query)) {
    faqs.push({
      question: "Quelles sont les principales différences entre l'Algérie et la Suisse sur ce point ?",
      answer: "Consultez le tableau comparatif ci-dessus pour voir les différences détaillées entre les deux pays.",
      category: "Comparaison"
    });
  }

  return faqs;
}

/**
 * Détecte et crée les graphiques appropriés
 */
function detectAndCreateCharts(response: RawRAGResponse): ChartData[] {
  const charts: ChartData[] = [];

  // Si query comparative, créer un chart de comparaison
  if (isComparativeQuery(response.query)) {
    const compData = extractComparisonData(response);
    if (compData.length > 0 && compData.length <= 6) {
      // Convertir en données de chart
      charts.push({
        type: 'comparison',
        title: 'Comparaison Algérie vs Suisse',
        data: compData.map(row => ({
          criterion: row.criterion,
          algerie: typeof row.algerie === 'number' ? row.algerie : 0,
          suisse: typeof row.suisse === 'number' ? row.suisse : 0
        }))
      });
    }
  }

  return charts;
}

/**
 * Détecte si la query demande une comparaison
 */
function isComparativeQuery(query: string): boolean {
  const lowerQuery = query.toLowerCase();
  return (
    lowerQuery.includes('vs') ||
    lowerQuery.includes('versus') ||
    lowerQuery.includes('comparaison') ||
    lowerQuery.includes('différence') ||
    lowerQuery.includes('compare') ||
    (lowerQuery.includes('algérie') && lowerQuery.includes('suisse'))
  );
}

/**
 * Extrait les données de comparaison depuis la réponse
 */
function extractComparisonData(response: RawRAGResponse): ComparisonRow[] {
  const rows: ComparisonRow[] = [];

  // Pattern matching simple pour extraire des comparaisons
  // Format attendu: "En Algérie: X, en Suisse: Y"
  const algeriePattern = /(?:algérie|alger|dz)[\s:]+([^,\.]+)/gi;
  const suissePattern = /(?:suisse|ch|confédération)[\s:]+([^,\.]+)/gi;

  // TODO: Améliorer l'extraction avec NLP
  // Pour l'instant, retourner des données d'exemple si comparaison détectée
  if (isComparativeQuery(response.query)) {
    rows.push({
      criterion: 'Information disponible',
      algerie: 'Voir réponse détaillée',
      suisse: 'Voir réponse détaillée',
      notes: 'Consultez les sources pour plus de détails'
    });
  }

  return rows;
}

/**
 * Détecte la langue principale de la query
 */
function detectPrimaryLanguage(query: string): 'fr' | 'ar' | 'de' | 'amazigh' | 'en' {
  // Patterns arabe
  if (/[\u0600-\u06FF]/.test(query)) return 'ar';

  // Patterns allemand
  if (/[äöüß]/i.test(query)) return 'de';

  // Mots-clés amazigh (Tamazight)
  if (/^(azul|tanemmirt|ma\s+tugi)/i.test(query)) return 'amazigh';

  // Mots-clés anglais
  if (/^(what|how|when|where|which|who)/i.test(query)) return 'en';

  // Par défaut français (langue principale IA Factory)
  return 'fr';
}

/**
 * Formate le contenu texte avec HTML basique
 */
function formatTextContent(text: string): string {
  // Convertir sauts de ligne en paragraphes
  const paragraphs = text.split('\n\n').filter(p => p.trim());

  return paragraphs
    .map(p => {
      // Détecter les listes
      if (p.includes('\n- ') || p.includes('\n• ')) {
        const items = p.split(/\n[-•]\s+/).filter(i => i.trim());
        return '<ul>' + items.map(item => `<li>${item.trim()}</li>`).join('') + '</ul>';
      }

      // Détecter les numéros (1. 2. 3.)
      if (/^\d+\./.test(p)) {
        const items = p.split(/\n\d+\.\s+/).filter(i => i.trim());
        return '<ol>' + items.map(item => `<li>${item.trim()}</li>`).join('') + '</ol>';
      }

      // Paragraphe normal
      return `<p>${p}</p>`;
    })
    .join('\n');
}
