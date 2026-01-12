/**
 * iaFactory API Portal - Docs & Playground
 * Module 16 - Documentation API + console de test interactive
 */

import React, { useState } from 'react';

// Types
interface EndpointDoc {
  id: string;
  category: string;
  name: string;
  path: string;
  method: 'GET' | 'POST';
  description: string;
  credits: number;
  params: {
    name: string;
    type: string;
    required: boolean;
    description: string;
  }[];
  exampleBody: object;
  exampleResponse: object;
}

// Configuration des endpoints documentés
const ENDPOINTS: EndpointDoc[] = [
  {
    id: 'rag-query',
    category: 'RAG',
    name: 'Query RAG',
    path: '/api/v1/rag/query',
    method: 'POST',
    description: "Interroge le système RAG avec des sources officielles algériennes (Journal Officiel, DGI, CNRC, CNAS).",
    credits: 2,
    params: [
      { name: 'query', type: 'string', required: true, description: 'Question à poser au système RAG' },
      { name: 'sources', type: 'array', required: false, description: 'Sources à interroger: ["dgi", "joradp", "cnrc", "cnas"]' },
      { name: 'language', type: 'string', required: false, description: 'Langue de réponse: "fr" ou "ar"' },
      { name: 'max_results', type: 'integer', required: false, description: 'Nombre max de sources (1-10)' },
    ],
    exampleBody: {
      query: "Quels sont les taux de TVA en Algérie ?",
      sources: ["dgi", "joradp"],
      language: "fr",
      max_results: 5
    },
    exampleResponse: {
      answer: "En Algérie, les taux de TVA sont de 19% (taux normal) et 9% (taux réduit)...",
      sources: [
        { title: "Code des impôts 2025", url: "https://...", excerpt: "..." }
      ],
      confidence: 0.92,
      credits_used: 2
    }
  },
  {
    id: 'legal-ask',
    category: 'Legal',
    name: 'Legal Assistant',
    path: '/api/v1/legal/ask',
    method: 'POST',
    description: "Assistant juridique IA spécialisé dans le droit algérien (commercial, travail, fiscal, civil).",
    credits: 3,
    params: [
      { name: 'question', type: 'string', required: true, description: 'Question juridique' },
      { name: 'domain', type: 'string', required: false, description: 'Domaine: "commercial", "travail", "fiscal", "civil"' },
      { name: 'include_sources', type: 'boolean', required: false, description: 'Inclure les références légales' },
    ],
    exampleBody: {
      question: "Comment créer une EURL en Algérie ?",
      domain: "commercial",
      include_sources: true
    },
    exampleResponse: {
      answer: "Pour créer une EURL en Algérie, vous devez suivre les étapes suivantes...",
      legal_references: [
        { code: "Code de commerce", article: "Art. 564", text: "..." }
      ],
      related_procedures: ["inscription_cnrc", "immatriculation_fiscale"],
      credits_used: 3
    }
  },
  {
    id: 'fiscal-simulate',
    category: 'Fiscal',
    name: 'Fiscal Simulator',
    path: '/api/v1/fiscal/simulate',
    method: 'POST',
    description: "Simulateur fiscal pour calculs d'impôts et taxes en Algérie (IRG, IBS, TVA, TAP).",
    credits: 1,
    params: [
      { name: 'type', type: 'string', required: true, description: 'Type: "irg_salarie", "irg_independant", "ibs", "tva", "tap"' },
      { name: 'salaire_brut', type: 'number', required: false, description: 'Pour IRG salarié (en DZD)' },
      { name: 'chiffre_affaires', type: 'number', required: false, description: 'Pour IBS/TAP (en DZD)' },
      { name: 'regime', type: 'string', required: false, description: 'Régime fiscal applicable' },
      { name: 'annee', type: 'integer', required: false, description: 'Année fiscale (défaut: 2025)' },
    ],
    exampleBody: {
      type: "irg_salarie",
      salaire_brut: 150000,
      regime: "general",
      annee: 2025
    },
    exampleResponse: {
      type: "irg_salarie",
      input: { salaire_brut: 150000 },
      results: {
        salaire_net: 127500,
        irg: 22500,
        cotisations_sociales: 13500,
        taux_effectif: 0.15
      },
      details: {
        tranches: [
          { min: 0, max: 120000, taux: 0, montant: 0 },
          { min: 120000, max: 360000, taux: 0.23, montant: 6900 }
        ]
      },
      credits_used: 1
    }
  },
  {
    id: 'fiscal-g50',
    category: 'Fiscal',
    name: 'Generate G50',
    path: '/api/v1/fiscal/g50',
    method: 'POST',
    description: "Génère un formulaire G50 pré-rempli pour déclaration TVA mensuelle.",
    credits: 2,
    params: [
      { name: 'periode', type: 'string', required: true, description: 'Période au format YYYY-MM' },
      { name: 'chiffre_affaires', type: 'number', required: true, description: 'Chiffre d\'affaires du mois' },
      { name: 'tva_collectee', type: 'number', required: true, description: 'TVA collectée' },
      { name: 'tva_deductible', type: 'number', required: true, description: 'TVA déductible' },
    ],
    exampleBody: {
      periode: "2025-11",
      chiffre_affaires: 5000000,
      tva_collectee: 950000,
      tva_deductible: 450000
    },
    exampleResponse: {
      document_type: "G50",
      periode: "2025-11",
      calculations: {
        tva_due: 500000,
        base_imposable: 5000000
      },
      pdf_url: "/documents/g50_2025_11.pdf",
      credits_used: 2
    }
  },
  {
    id: 'park-sparkpage',
    category: 'Park',
    name: 'SparkPage Generator',
    path: '/api/v1/park/sparkpage',
    method: 'POST',
    description: "Génère une landing page complète (HTML/CSS) à partir d'une description.",
    credits: 5,
    params: [
      { name: 'title', type: 'string', required: true, description: 'Titre de la page' },
      { name: 'description', type: 'string', required: true, description: 'Description du contenu souhaité' },
      { name: 'theme', type: 'string', required: false, description: 'Thème: "business", "tech", "creative", "minimal"' },
      { name: 'language', type: 'string', required: false, description: 'Langue: "fr", "ar", "en"' },
      { name: 'include_contact', type: 'boolean', required: false, description: 'Inclure formulaire de contact' },
    ],
    exampleBody: {
      title: "Mon Entreprise DZ",
      description: "Landing page pour une société de services professionnels en Algérie",
      theme: "business",
      language: "fr",
      include_contact: true
    },
    exampleResponse: {
      page_id: "sp_abc123",
      preview_url: "/preview/sp_abc123",
      html: "<!DOCTYPE html>...",
      credits_used: 5
    }
  },
  {
    id: 'legal-contract',
    category: 'Legal',
    name: 'Contract Generator',
    path: '/api/v1/legal/contract',
    method: 'POST',
    description: "Génère un modèle de contrat conforme au droit algérien.",
    credits: 4,
    params: [
      { name: 'type', type: 'string', required: true, description: 'Type: "travail_cdi", "travail_cdd", "commercial", "bail"' },
      { name: 'parties', type: 'object', required: true, description: 'Parties au contrat' },
      { name: 'clauses', type: 'array', required: false, description: 'Clauses spéciales à inclure' },
    ],
    exampleBody: {
      type: "travail_cdi",
      parties: {
        employeur: "SARL ABC",
        employe: "Ahmed Ben Ali"
      },
      clauses: ["confidentialite", "non_concurrence"]
    },
    exampleResponse: {
      contract_id: "ct_xyz789",
      type: "travail_cdi",
      preview_url: "/contracts/ct_xyz789/preview",
      pdf_url: "/contracts/ct_xyz789.pdf",
      docx_url: "/contracts/ct_xyz789.docx",
      credits_used: 4
    }
  }
];

// Composant onglet de catégorie
const CategoryTabs: React.FC<{
  categories: string[];
  active: string;
  onChange: (cat: string) => void;
}> = ({ categories, active, onChange }) => (
  <div className="flex gap-2 border-b border-gray-200 dark:border-gray-700 pb-2 mb-4 overflow-x-auto">
    {categories.map(cat => (
      <button
        key={cat}
        onClick={() => onChange(cat)}
        className={`px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap transition-colors ${
          active === cat
            ? 'bg-emerald-500 text-white'
            : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'
        }`}
      >
        {cat}
      </button>
    ))}
  </div>
);

// Composant documentation d'un endpoint
const EndpointDocCard: React.FC<{
  endpoint: EndpointDoc;
  onTest: (endpoint: EndpointDoc) => void;
}> = ({ endpoint, onTest }) => {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden mb-4">
      {/* Header */}
      <div 
        className="p-4 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
        onClick={() => setExpanded(!expanded)}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className={`px-2 py-1 rounded text-xs font-mono font-bold ${
              endpoint.method === 'POST' 
                ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/50 dark:text-emerald-400'
                : 'bg-blue-100 text-blue-700 dark:bg-blue-900/50 dark:text-blue-400'
            }`}>
              {endpoint.method}
            </span>
            <code className="text-sm font-mono text-gray-700 dark:text-gray-300">
              {endpoint.path}
            </code>
            <span className="text-xs text-gray-400">({endpoint.credits} crédits)</span>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={(e) => {
                e.stopPropagation();
                onTest(endpoint);
              }}
              className="px-3 py-1 bg-purple-500 text-white text-sm rounded-lg hover:bg-purple-600 transition-colors"
            >
              🧪 Tester
            </button>
            <span className="text-gray-400">{expanded ? '▼' : '▶'}</span>
          </div>
        </div>
        <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
          {endpoint.description}
        </p>
      </div>

      {/* Contenu expandable */}
      {expanded && (
        <div className="p-4 border-t border-gray-200 dark:border-gray-700 space-y-4">
          {/* Paramètres */}
          <div>
            <h4 className="font-semibold text-gray-800 dark:text-white mb-2">Paramètres</h4>
            <div className="bg-gray-50 dark:bg-gray-900 rounded-lg overflow-hidden">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-gray-200 dark:border-gray-700">
                    <th className="text-left py-2 px-3 text-gray-500">Nom</th>
                    <th className="text-left py-2 px-3 text-gray-500">Type</th>
                    <th className="text-left py-2 px-3 text-gray-500">Requis</th>
                    <th className="text-left py-2 px-3 text-gray-500">Description</th>
                  </tr>
                </thead>
                <tbody>
                  {endpoint.params.map(param => (
                    <tr key={param.name} className="border-b border-gray-100 dark:border-gray-800">
                      <td className="py-2 px-3 font-mono text-emerald-600 dark:text-emerald-400">
                        {param.name}
                      </td>
                      <td className="py-2 px-3 text-purple-600 dark:text-purple-400">
                        {param.type}
                      </td>
                      <td className="py-2 px-3">
                        {param.required ? (
                          <span className="text-red-500">Oui</span>
                        ) : (
                          <span className="text-gray-400">Non</span>
                        )}
                      </td>
                      <td className="py-2 px-3 text-gray-600 dark:text-gray-400">
                        {param.description}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Exemple Request */}
          <div>
            <h4 className="font-semibold text-gray-800 dark:text-white mb-2">Exemple Request</h4>
            <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto text-sm">
              <code>{JSON.stringify(endpoint.exampleBody, null, 2)}</code>
            </pre>
          </div>

          {/* Exemple Response */}
          <div>
            <h4 className="font-semibold text-gray-800 dark:text-white mb-2">Exemple Response</h4>
            <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto text-sm">
              <code>{JSON.stringify(endpoint.exampleResponse, null, 2)}</code>
            </pre>
          </div>

          {/* cURL */}
          <div>
            <h4 className="font-semibold text-gray-800 dark:text-white mb-2">cURL</h4>
            <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto text-sm">
              <code>{`curl -X ${endpoint.method} https://api.iafactoryalgeria.com${endpoint.path} \\
  -H "Authorization: Bearer IAFK_live_xxxxx" \\
  -H "Content-Type: application/json" \\
  -d '${JSON.stringify(endpoint.exampleBody)}'`}</code>
            </pre>
          </div>
        </div>
      )}
    </div>
  );
};

// Composant Playground
const Playground: React.FC<{
  endpoint: EndpointDoc | null;
  onClose: () => void;
}> = ({ endpoint, onClose }) => {
  const [body, setBody] = useState('');
  const [response, setResponse] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<number | null>(null);
  const [latency, setLatency] = useState<number | null>(null);

  React.useEffect(() => {
    if (endpoint) {
      setBody(JSON.stringify(endpoint.exampleBody, null, 2));
      setResponse(null);
      setStatus(null);
      setLatency(null);
    }
  }, [endpoint]);

  const handleSend = async () => {
    if (!endpoint) return;
    
    setLoading(true);
    const start = Date.now();
    
    // TODO: Appel API réel POST /api/dev/playground/execute
    await new Promise(r => setTimeout(r, 800));
    
    setLatency(Date.now() - start);
    setStatus(200);
    setResponse(JSON.stringify(endpoint.exampleResponse, null, 2));
    setLoading(false);
  };

  if (!endpoint) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-gray-800 rounded-2xl max-w-4xl w-full shadow-2xl max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="p-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-2xl">🧪</span>
            <div>
              <h2 className="font-bold text-gray-800 dark:text-white">API Playground</h2>
              <code className="text-sm text-gray-500">{endpoint.method} {endpoint.path}</code>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
          >
            ✕
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {/* Request Body */}
          <div>
            <label className="block font-semibold text-gray-800 dark:text-white mb-2">
              Request Body (JSON)
            </label>
            <textarea
              value={body}
              onChange={(e) => setBody(e.target.value)}
              className="w-full h-48 p-4 font-mono text-sm bg-gray-900 text-gray-100 rounded-lg border border-gray-700 focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
              spellCheck={false}
            />
          </div>

          {/* Send Button */}
          <button
            onClick={handleSend}
            disabled={loading}
            className="w-full py-3 bg-emerald-500 text-white rounded-xl font-medium hover:bg-emerald-600 disabled:opacity-50 transition-colors flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <span className="animate-spin">⚙️</span>
                Envoi en cours...
              </>
            ) : (
              <>
                🚀 Envoyer la requête
              </>
            )}
          </button>

          {/* Response */}
          {response && (
            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="font-semibold text-gray-800 dark:text-white">
                  Response
                </label>
                <div className="flex items-center gap-3 text-sm">
                  <span className={`px-2 py-1 rounded-full font-medium ${
                    status && status < 400
                      ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/50 dark:text-emerald-400'
                      : 'bg-red-100 text-red-700 dark:bg-red-900/50 dark:text-red-400'
                  }`}>
                    {status}
                  </span>
                  {latency && (
                    <span className="text-gray-500">{latency}ms</span>
                  )}
                </div>
              </div>
              <pre className="w-full p-4 font-mono text-sm bg-gray-900 text-gray-100 rounded-lg overflow-x-auto max-h-64">
                <code>{response}</code>
              </pre>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-gray-200 dark:border-gray-700 flex items-center justify-between">
          <p className="text-sm text-gray-500">
            💡 Coût: {endpoint.credits} crédit(s) par requête
          </p>
          <button
            onClick={onClose}
            className="px-4 py-2 bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-white rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
          >
            Fermer
          </button>
        </div>
      </div>
    </div>
  );
};

/**
 * Composant principal Docs & Playground
 */
export const ApiDocsPlayground: React.FC = () => {
  const categories = [...new Set(ENDPOINTS.map(e => e.category))];
  const [activeCategory, setActiveCategory] = useState(categories[0]);
  const [playgroundEndpoint, setPlaygroundEndpoint] = useState<EndpointDoc | null>(null);

  const filteredEndpoints = ENDPOINTS.filter(e => e.category === activeCategory);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-gray-800 dark:text-white">
          Documentation API & Playground
        </h2>
        <p className="text-gray-600 dark:text-gray-400 mt-1">
          Explorez et testez les endpoints de l'API iaFactory
        </p>
      </div>

      {/* Auth Info */}
      <div className="bg-blue-50 dark:bg-blue-900/30 border border-blue-200 dark:border-blue-700 rounded-xl p-4">
        <h3 className="font-semibold text-blue-800 dark:text-blue-200 mb-2">
          🔐 Authentification
        </h3>
        <p className="text-sm text-blue-700 dark:text-blue-300 mb-2">
          Toutes les requêtes doivent inclure votre clé API dans le header :
        </p>
        <code className="block bg-blue-100 dark:bg-blue-900 px-3 py-2 rounded-lg text-sm font-mono text-blue-800 dark:text-blue-200">
          Authorization: Bearer IAFK_live_xxxxxxxxxxxxxxxx
        </code>
      </div>

      {/* Base URL */}
      <div className="bg-gray-100 dark:bg-gray-800 rounded-xl p-4 flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-500 mb-1">Base URL</p>
          <code className="font-mono text-gray-800 dark:text-gray-200">
            https://api.iafactoryalgeria.com
          </code>
        </div>
        <button className="px-3 py-1 bg-gray-200 dark:bg-gray-700 rounded-lg text-sm hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors">
          📋 Copier
        </button>
      </div>

      {/* Categories */}
      <CategoryTabs 
        categories={categories} 
        active={activeCategory} 
        onChange={setActiveCategory} 
      />

      {/* Endpoints */}
      <div>
        {filteredEndpoints.map(endpoint => (
          <EndpointDocCard
            key={endpoint.id}
            endpoint={endpoint}
            onTest={setPlaygroundEndpoint}
          />
        ))}
      </div>

      {/* Rate Limits */}
      <div className="bg-amber-50 dark:bg-amber-900/30 border border-amber-200 dark:border-amber-700 rounded-xl p-4">
        <h3 className="font-semibold text-amber-800 dark:text-amber-200 mb-2">
          ⚡ Rate Limits
        </h3>
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <p className="text-amber-700 dark:text-amber-300">Free Tier</p>
            <p className="text-amber-600 dark:text-amber-400">100 requêtes/minute</p>
          </div>
          <div>
            <p className="text-amber-700 dark:text-amber-300">Pro/Business</p>
            <p className="text-amber-600 dark:text-amber-400">1000 requêtes/minute</p>
          </div>
        </div>
      </div>

      {/* Playground Modal */}
      <Playground
        endpoint={playgroundEndpoint}
        onClose={() => setPlaygroundEndpoint(null)}
      />
    </div>
  );
};

export default ApiDocsPlayground;
