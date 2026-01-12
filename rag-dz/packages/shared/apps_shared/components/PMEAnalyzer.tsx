import React, { useState } from 'react';

// ============================================
// Types
// ============================================
interface PMEFormData {
  company_name: string;
  wilaya: string;
  activity_sector: string;
  legal_form: string;
  employee_count: number;
  annual_revenue?: number;
  creation_date?: string;
  has_employees: boolean;
  is_exporter: boolean;
  is_importer: boolean;
  vat_registered: boolean;
  description?: string;
}

interface Obligation {
  title: string;
  description: string;
  deadline?: string;
  priority: 'high' | 'medium' | 'low';
  category: string;
  penalty?: string;
}

interface Risk {
  title: string;
  description: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  mitigation: string;
}

interface ChecklistItem {
  task: string;
  deadline: string;
  completed: boolean;
  category: string;
}

interface AnalysisResult {
  company_profile: {
    name: string;
    sector: string;
    size_category: string;
    regime_fiscal: string;
  };
  obligations: Obligation[];
  risks: Risk[];
  checklist_30_days: ChecklistItem[];
  taxes: Array<{
    name: string;
    rate: string;
    frequency: string;
    next_deadline: string;
  }>;
  recommendations: string[];
  documents_required: string[];
  estimated_costs: {
    monthly_taxes: number;
    annual_contributions: number;
    compliance_budget: number;
  };
  ai_summary: string;
}

interface PMEAnalyzerProps {
  /** URL de l'API (défaut: /api/pme/analyze) */
  apiUrl?: string;
  /** Pays (DZ ou CH) */
  country?: 'DZ' | 'CH';
  /** Mode démo (limite les analyses) */
  maxAnalyses?: number;
  /** Callback après analyse */
  onAnalysisComplete?: (result: AnalysisResult) => void;
  /** Titre */
  title?: string;
  /** Mode compact */
  compact?: boolean;
}

// ============================================
// Options
// ============================================
const WILAYAS_DZ = [
  { value: '', label: 'Sélectionnez une wilaya...' },
  { value: '16', label: '16 - Alger' },
  { value: '31', label: '31 - Oran' },
  { value: '25', label: '25 - Constantine' },
  { value: '09', label: '09 - Blida' },
  { value: '19', label: '19 - Sétif' },
  { value: '23', label: '23 - Annaba' },
  { value: '06', label: '06 - Béjaïa' },
  { value: '15', label: '15 - Tizi Ouzou' },
  { value: '05', label: '05 - Batna' },
  { value: '07', label: '07 - Biskra' },
  { value: 'autre', label: 'Autre wilaya' },
];

const CANTONS_CH = [
  { value: '', label: 'Sélectionnez un canton...' },
  { value: 'GE', label: 'Genève' },
  { value: 'VD', label: 'Vaud' },
  { value: 'ZH', label: 'Zürich' },
  { value: 'BE', label: 'Berne' },
  { value: 'BS', label: 'Bâle-Ville' },
  { value: 'autre', label: 'Autre canton' },
];

const SECTORS = [
  { value: '', label: 'Sélectionnez un secteur...' },
  { value: 'commerce', label: '🛒 Commerce / Distribution' },
  { value: 'services', label: '💼 Services aux entreprises' },
  { value: 'tech', label: '💻 Tech / IT / Digital' },
  { value: 'industrie', label: '🏭 Industrie / Production' },
  { value: 'immobilier', label: '🏢 Immobilier / BTP' },
  { value: 'sante', label: '🏥 Santé / Médical' },
  { value: 'education', label: '🎓 Éducation / Formation' },
  { value: 'transport', label: '🚚 Transport / Logistique' },
  { value: 'agriculture', label: '🌾 Agriculture / Agroalimentaire' },
  { value: 'restauration', label: '🍽️ Restauration / Hôtellerie' },
  { value: 'autre', label: '📋 Autre' },
];

const LEGAL_FORMS_DZ = [
  { value: '', label: 'Sélectionnez une forme juridique...' },
  { value: 'eurl', label: 'EURL - Entreprise Unipersonnelle' },
  { value: 'sarl', label: 'SARL - Société à Responsabilité Limitée' },
  { value: 'spa', label: 'SPA - Société Par Actions' },
  { value: 'snc', label: 'SNC - Société en Nom Collectif' },
  { value: 'auto', label: 'Auto-entrepreneur' },
  { value: 'ei', label: 'Entreprise Individuelle' },
];

const LEGAL_FORMS_CH = [
  { value: '', label: 'Sélectionnez une forme juridique...' },
  { value: 'sarl', label: 'Sàrl - Société à responsabilité limitée' },
  { value: 'sa', label: 'SA - Société Anonyme' },
  { value: 'ri', label: 'RI - Raison Individuelle' },
  { value: 'snc', label: 'SNC - Société en Nom Collectif' },
];

// ============================================
// Composant Principal
// ============================================
export const PMEAnalyzer: React.FC<PMEAnalyzerProps> = ({
  apiUrl = '/api/pme/analyze',
  country = 'DZ',
  maxAnalyses = 1,
  onAnalysisComplete,
  title = '🏢 Audit PME Intelligent',
  compact = false,
}) => {
  // State
  const [step, setStep] = useState<'form' | 'loading' | 'result'>('form');
  const [formData, setFormData] = useState<Partial<PMEFormData>>({
    company_name: '',
    wilaya: '',
    activity_sector: '',
    legal_form: '',
    employee_count: 0,
    has_employees: false,
    is_exporter: false,
    is_importer: false,
    vat_registered: false,
  });
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [remainingAnalyses, setRemainingAnalyses] = useState(maxAnalyses);
  const [activeTab, setActiveTab] = useState<'overview' | 'obligations' | 'risks' | 'checklist' | 'taxes'>('overview');

  // Regions selon pays
  const regions = country === 'DZ' ? WILAYAS_DZ : CANTONS_CH;
  const legalForms = country === 'DZ' ? LEGAL_FORMS_DZ : LEGAL_FORMS_CH;

  // Handle input change
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;
    const checked = (e.target as HTMLInputElement).checked;
    
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : type === 'number' ? parseInt(value) || 0 : value,
    }));
    setError(null);
  };

  // Submit
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validation
    if (!formData.company_name?.trim()) {
      setError('Veuillez entrer le nom de votre entreprise');
      return;
    }
    if (!formData.wilaya) {
      setError(`Veuillez sélectionner ${country === 'DZ' ? 'une wilaya' : 'un canton'}`);
      return;
    }
    if (!formData.activity_sector) {
      setError('Veuillez sélectionner un secteur d\'activité');
      return;
    }
    if (!formData.legal_form) {
      setError('Veuillez sélectionner une forme juridique');
      return;
    }

    if (remainingAnalyses <= 0) {
      setError('Limite de démo atteinte. Créez un compte pour continuer.');
      return;
    }

    setStep('loading');
    setError(null);

    try {
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...formData,
          country,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Erreur ${response.status}`);
      }

      const data: AnalysisResult = await response.json();
      setResult(data);
      setStep('result');
      setRemainingAnalyses(prev => prev - 1);

      if (onAnalysisComplete) {
        onAnalysisComplete(data);
      }

    } catch (err) {
      console.error('Erreur PME Analyzer:', err);
      setError(err instanceof Error ? err.message : 'Une erreur est survenue');
      setStep('form');
    }
  };

  // Reset
  const handleReset = () => {
    setStep('form');
    setResult(null);
    setActiveTab('overview');
  };

  // Couleurs de priorité/sévérité
  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'critical': return 'bg-red-500/20 text-red-400 border-red-500/50';
      case 'high': return 'bg-orange-500/20 text-orange-400 border-orange-500/50';
      case 'medium': return 'bg-amber-500/20 text-amber-400 border-amber-500/50';
      case 'low': return 'bg-emerald-500/20 text-emerald-400 border-emerald-500/50';
      default: return 'bg-slate-500/20 text-slate-400 border-slate-500/50';
    }
  };

  return (
    <div className={`
      bg-slate-900 border border-slate-700 rounded-2xl overflow-hidden
      shadow-xl shadow-black/20
      ${compact ? 'max-w-lg' : 'max-w-4xl'} w-full
    `}>
      {/* Header */}
      <div className="bg-gradient-to-r from-indigo-600 to-violet-600 px-6 py-4 flex items-center justify-between">
        <div>
          <h2 className="text-white font-bold text-xl">{title}</h2>
          <p className="text-white/80 text-sm mt-1">
            {country === 'DZ' ? '🇩🇿 Algérie' : '🇨🇭 Suisse'} • Analyse complète de conformité
          </p>
        </div>
        {step !== 'loading' && (
          <span className="text-white/80 text-xs bg-white/20 px-3 py-1.5 rounded-full">
            {remainingAnalyses} analyse{remainingAnalyses !== 1 ? 's' : ''} restante{remainingAnalyses !== 1 ? 's' : ''}
          </span>
        )}
      </div>

      {/* FORMULAIRE */}
      {step === 'form' && (
        <form onSubmit={handleSubmit} className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Nom entreprise */}
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-slate-300 mb-1.5">
                Nom de l'entreprise *
              </label>
              <input
                type="text"
                name="company_name"
                value={formData.company_name}
                onChange={handleChange}
                placeholder="Ex: TechSolutions SARL"
                className="w-full bg-slate-800 border border-slate-600 rounded-lg px-4 py-2.5 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-indigo-500"
              />
            </div>

            {/* Région */}
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-1.5">
                {country === 'DZ' ? 'Wilaya' : 'Canton'} *
              </label>
              <select
                name="wilaya"
                value={formData.wilaya}
                onChange={handleChange}
                className="w-full bg-slate-800 border border-slate-600 rounded-lg px-4 py-2.5 text-white text-sm focus:outline-none focus:border-indigo-500"
              >
                {regions.map(r => (
                  <option key={r.value} value={r.value}>{r.label}</option>
                ))}
              </select>
            </div>

            {/* Secteur */}
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-1.5">
                Secteur d'activité *
              </label>
              <select
                name="activity_sector"
                value={formData.activity_sector}
                onChange={handleChange}
                className="w-full bg-slate-800 border border-slate-600 rounded-lg px-4 py-2.5 text-white text-sm focus:outline-none focus:border-indigo-500"
              >
                {SECTORS.map(s => (
                  <option key={s.value} value={s.value}>{s.label}</option>
                ))}
              </select>
            </div>

            {/* Forme juridique */}
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-1.5">
                Forme juridique *
              </label>
              <select
                name="legal_form"
                value={formData.legal_form}
                onChange={handleChange}
                className="w-full bg-slate-800 border border-slate-600 rounded-lg px-4 py-2.5 text-white text-sm focus:outline-none focus:border-indigo-500"
              >
                {legalForms.map(f => (
                  <option key={f.value} value={f.value}>{f.label}</option>
                ))}
              </select>
            </div>

            {/* Nombre d'employés */}
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-1.5">
                Nombre d'employés
              </label>
              <input
                type="number"
                name="employee_count"
                value={formData.employee_count}
                onChange={handleChange}
                min="0"
                className="w-full bg-slate-800 border border-slate-600 rounded-lg px-4 py-2.5 text-white text-sm focus:outline-none focus:border-indigo-500"
              />
            </div>

            {/* Chiffre d'affaires */}
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-1.5">
                CA annuel estimé ({country === 'DZ' ? 'DZD' : 'CHF'})
              </label>
              <input
                type="number"
                name="annual_revenue"
                value={formData.annual_revenue || ''}
                onChange={handleChange}
                placeholder={country === 'DZ' ? 'Ex: 50000000' : 'Ex: 500000'}
                className="w-full bg-slate-800 border border-slate-600 rounded-lg px-4 py-2.5 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-indigo-500"
              />
            </div>

            {/* Date création */}
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-1.5">
                Date de création
              </label>
              <input
                type="date"
                name="creation_date"
                value={formData.creation_date || ''}
                onChange={handleChange}
                className="w-full bg-slate-800 border border-slate-600 rounded-lg px-4 py-2.5 text-white text-sm focus:outline-none focus:border-indigo-500"
              />
            </div>

            {/* Options */}
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-slate-300 mb-3">
                Caractéristiques
              </label>
              <div className="flex flex-wrap gap-4">
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="checkbox"
                    name="has_employees"
                    checked={formData.has_employees}
                    onChange={handleChange}
                    className="w-4 h-4 rounded border-slate-600 bg-slate-800 text-indigo-500 focus:ring-indigo-500"
                  />
                  <span className="text-slate-300 text-sm">👥 Employés déclarés</span>
                </label>
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="checkbox"
                    name="vat_registered"
                    checked={formData.vat_registered}
                    onChange={handleChange}
                    className="w-4 h-4 rounded border-slate-600 bg-slate-800 text-indigo-500 focus:ring-indigo-500"
                  />
                  <span className="text-slate-300 text-sm">📋 Assujetti TVA</span>
                </label>
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="checkbox"
                    name="is_importer"
                    checked={formData.is_importer}
                    onChange={handleChange}
                    className="w-4 h-4 rounded border-slate-600 bg-slate-800 text-indigo-500 focus:ring-indigo-500"
                  />
                  <span className="text-slate-300 text-sm">📦 Importateur</span>
                </label>
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="checkbox"
                    name="is_exporter"
                    checked={formData.is_exporter}
                    onChange={handleChange}
                    className="w-4 h-4 rounded border-slate-600 bg-slate-800 text-indigo-500 focus:ring-indigo-500"
                  />
                  <span className="text-slate-300 text-sm">🌍 Exportateur</span>
                </label>
              </div>
            </div>

            {/* Description */}
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-slate-300 mb-1.5">
                Description de l'activité (optionnel)
              </label>
              <textarea
                name="description"
                value={formData.description || ''}
                onChange={handleChange}
                rows={3}
                placeholder="Décrivez brièvement votre activité pour une analyse plus précise..."
                className="w-full bg-slate-800 border border-slate-600 rounded-lg px-4 py-2.5 text-white placeholder-slate-500 text-sm resize-none focus:outline-none focus:border-indigo-500"
              />
            </div>
          </div>

          {/* Error */}
          {error && (
            <div className="mt-4 bg-red-900/30 border border-red-700 text-red-300 rounded-lg px-4 py-3 text-sm">
              ⚠️ {error}
            </div>
          )}

          {/* Submit */}
          <button
            type="submit"
            disabled={remainingAnalyses <= 0}
            className="mt-6 w-full bg-gradient-to-r from-indigo-500 to-violet-500 hover:from-indigo-400 hover:to-violet-400 text-white font-bold py-3.5 px-6 rounded-xl disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center justify-center gap-3"
          >
            <span>🔍</span>
            Lancer l'analyse PME
          </button>
        </form>
      )}

      {/* LOADING */}
      {step === 'loading' && (
        <div className="p-12 text-center">
          <div className="text-6xl mb-6 animate-bounce">🔍</div>
          <h3 className="text-xl font-bold text-white mb-2">Analyse en cours...</h3>
          <p className="text-slate-400 mb-6">Notre IA analyse votre situation</p>
          
          <div className="max-w-md mx-auto space-y-3">
            {['Vérification des obligations fiscales...', 'Analyse des cotisations sociales...', 'Évaluation des risques...', 'Génération des recommandations...'].map((text, i) => (
              <div 
                key={i}
                className="flex items-center gap-3 text-slate-300 text-sm animate-pulse"
                style={{ animationDelay: `${i * 0.3}s` }}
              >
                <span className="text-indigo-400">✓</span>
                {text}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* RÉSULTATS */}
      {step === 'result' && result && (
        <div>
          {/* Tabs */}
          <div className="flex border-b border-slate-700 overflow-x-auto">
            {[
              { id: 'overview', label: '📊 Vue globale', icon: '📊' },
              { id: 'obligations', label: '📋 Obligations', icon: '📋' },
              { id: 'risks', label: '⚠️ Risques', icon: '⚠️' },
              { id: 'checklist', label: '✅ Checklist', icon: '✅' },
              { id: 'taxes', label: '💰 Taxes', icon: '💰' },
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`px-4 py-3 text-sm font-medium whitespace-nowrap transition-colors ${
                  activeTab === tab.id
                    ? 'text-indigo-400 border-b-2 border-indigo-400 bg-indigo-500/10'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          <div className="p-6">
            {/* Overview */}
            {activeTab === 'overview' && (
              <div className="space-y-6">
                {/* Profil */}
                <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-700">
                  <h3 className="text-lg font-bold text-white mb-3">📊 Profil de votre entreprise</h3>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div>
                      <p className="text-slate-400 text-xs">Entreprise</p>
                      <p className="text-white font-medium">{result.company_profile.name}</p>
                    </div>
                    <div>
                      <p className="text-slate-400 text-xs">Secteur</p>
                      <p className="text-white font-medium">{result.company_profile.sector}</p>
                    </div>
                    <div>
                      <p className="text-slate-400 text-xs">Catégorie</p>
                      <p className="text-white font-medium">{result.company_profile.size_category}</p>
                    </div>
                    <div>
                      <p className="text-slate-400 text-xs">Régime fiscal</p>
                      <p className="text-white font-medium">{result.company_profile.regime_fiscal}</p>
                    </div>
                  </div>
                </div>

                {/* AI Summary */}
                <div className="bg-gradient-to-r from-indigo-900/50 to-violet-900/50 rounded-xl p-4 border border-indigo-500/30">
                  <h3 className="text-lg font-bold text-white mb-2 flex items-center gap-2">
                    🤖 Synthèse IA
                  </h3>
                  <p className="text-slate-300 text-sm leading-relaxed">
                    {result.ai_summary}
                  </p>
                </div>

                {/* Stats rapides */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="bg-slate-800 rounded-xl p-4 text-center border border-slate-700">
                    <p className="text-3xl font-bold text-orange-400">{result.obligations.length}</p>
                    <p className="text-slate-400 text-sm">Obligations</p>
                  </div>
                  <div className="bg-slate-800 rounded-xl p-4 text-center border border-slate-700">
                    <p className="text-3xl font-bold text-red-400">{result.risks.filter(r => r.severity === 'critical' || r.severity === 'high').length}</p>
                    <p className="text-slate-400 text-sm">Risques majeurs</p>
                  </div>
                  <div className="bg-slate-800 rounded-xl p-4 text-center border border-slate-700">
                    <p className="text-3xl font-bold text-emerald-400">{result.checklist_30_days.length}</p>
                    <p className="text-slate-400 text-sm">Actions 30j</p>
                  </div>
                  <div className="bg-slate-800 rounded-xl p-4 text-center border border-slate-700">
                    <p className="text-3xl font-bold text-blue-400">{result.taxes.length}</p>
                    <p className="text-slate-400 text-sm">Impôts/taxes</p>
                  </div>
                </div>

                {/* Coûts estimés */}
                <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-700">
                  <h3 className="text-lg font-bold text-white mb-3">💰 Coûts estimés</h3>
                  <div className="grid grid-cols-3 gap-4">
                    <div>
                      <p className="text-slate-400 text-xs">Charges mensuelles</p>
                      <p className="text-white font-bold">{result.estimated_costs.monthly_taxes.toLocaleString()} {country === 'DZ' ? 'DZD' : 'CHF'}</p>
                    </div>
                    <div>
                      <p className="text-slate-400 text-xs">Cotisations annuelles</p>
                      <p className="text-white font-bold">{result.estimated_costs.annual_contributions.toLocaleString()} {country === 'DZ' ? 'DZD' : 'CHF'}</p>
                    </div>
                    <div>
                      <p className="text-slate-400 text-xs">Budget conformité</p>
                      <p className="text-white font-bold">{result.estimated_costs.compliance_budget.toLocaleString()} {country === 'DZ' ? 'DZD' : 'CHF'}</p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Obligations */}
            {activeTab === 'obligations' && (
              <div className="space-y-4">
                <h3 className="text-lg font-bold text-white">📋 Vos obligations légales</h3>
                {result.obligations.map((ob, i) => (
                  <div key={i} className={`rounded-xl p-4 border ${getPriorityColor(ob.priority)}`}>
                    <div className="flex items-start justify-between">
                      <div>
                        <h4 className="font-semibold text-white">{ob.title}</h4>
                        <p className="text-slate-300 text-sm mt-1">{ob.description}</p>
                        <div className="flex gap-3 mt-2 text-xs">
                          <span className="text-slate-400">📁 {ob.category}</span>
                          {ob.deadline && <span className="text-amber-400">⏰ {ob.deadline}</span>}
                        </div>
                      </div>
                      <span className={`text-xs px-2 py-1 rounded-full border ${getPriorityColor(ob.priority)}`}>
                        {ob.priority === 'high' ? '🔴 Urgent' : ob.priority === 'medium' ? '🟡 Important' : '🟢 Normal'}
                      </span>
                    </div>
                    {ob.penalty && (
                      <p className="mt-2 text-red-400 text-xs">⚠️ Pénalité : {ob.penalty}</p>
                    )}
                  </div>
                ))}
              </div>
            )}

            {/* Risks */}
            {activeTab === 'risks' && (
              <div className="space-y-4">
                <h3 className="text-lg font-bold text-white">⚠️ Risques identifiés</h3>
                {result.risks.map((risk, i) => (
                  <div key={i} className={`rounded-xl p-4 border ${getPriorityColor(risk.severity)}`}>
                    <h4 className="font-semibold text-white">{risk.title}</h4>
                    <p className="text-slate-300 text-sm mt-1">{risk.description}</p>
                    <div className="mt-3 bg-slate-800/50 rounded-lg p-3">
                      <p className="text-emerald-400 text-sm">
                        💡 <strong>Mitigation :</strong> {risk.mitigation}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Checklist */}
            {activeTab === 'checklist' && (
              <div className="space-y-4">
                <h3 className="text-lg font-bold text-white">✅ Actions des 30 prochains jours</h3>
                {result.checklist_30_days.map((item, i) => (
                  <div key={i} className="flex items-start gap-3 bg-slate-800/50 rounded-xl p-4 border border-slate-700">
                    <input
                      type="checkbox"
                      checked={item.completed}
                      readOnly
                      className="mt-1 w-5 h-5 rounded border-slate-600 bg-slate-700 text-emerald-500"
                    />
                    <div className="flex-1">
                      <p className="text-white font-medium">{item.task}</p>
                      <div className="flex gap-3 mt-1 text-xs">
                        <span className="text-slate-400">📁 {item.category}</span>
                        <span className="text-amber-400">⏰ {item.deadline}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Taxes */}
            {activeTab === 'taxes' && (
              <div className="space-y-4">
                <h3 className="text-lg font-bold text-white">💰 Impôts & Taxes applicables</h3>
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="border-b border-slate-700">
                        <th className="text-left py-3 px-4 text-slate-400 font-medium">Impôt/Taxe</th>
                        <th className="text-left py-3 px-4 text-slate-400 font-medium">Taux</th>
                        <th className="text-left py-3 px-4 text-slate-400 font-medium">Fréquence</th>
                        <th className="text-left py-3 px-4 text-slate-400 font-medium">Prochaine échéance</th>
                      </tr>
                    </thead>
                    <tbody>
                      {result.taxes.map((tax, i) => (
                        <tr key={i} className="border-b border-slate-700/50">
                          <td className="py-3 px-4 text-white font-medium">{tax.name}</td>
                          <td className="py-3 px-4 text-slate-300">{tax.rate}</td>
                          <td className="py-3 px-4 text-slate-300">{tax.frequency}</td>
                          <td className="py-3 px-4 text-amber-400">{tax.next_deadline}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                {/* Documents requis */}
                <div className="mt-6 bg-slate-800/50 rounded-xl p-4 border border-slate-700">
                  <h4 className="font-semibold text-white mb-3">📄 Documents à tenir à jour</h4>
                  <ul className="grid grid-cols-1 md:grid-cols-2 gap-2">
                    {result.documents_required.map((doc, i) => (
                      <li key={i} className="flex items-center gap-2 text-slate-300 text-sm">
                        <span className="text-indigo-400">•</span>
                        {doc}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            )}
          </div>

          {/* Actions */}
          <div className="px-6 pb-6 flex gap-4">
            <button
              onClick={handleReset}
              className="flex-1 bg-slate-700 hover:bg-slate-600 text-white font-semibold py-3 px-6 rounded-xl transition-colors"
            >
              🔄 Nouvelle analyse
            </button>
            <button
              onClick={() => window.print()}
              className="flex-1 bg-gradient-to-r from-indigo-500 to-violet-500 hover:from-indigo-400 hover:to-violet-400 text-white font-semibold py-3 px-6 rounded-xl transition-all"
            >
              📥 Exporter PDF
            </button>
          </div>
        </div>
      )}

      {/* Limite atteinte */}
      {remainingAnalyses <= 0 && step === 'form' && (
        <div className="p-6 border-t border-slate-700 text-center">
          <p className="text-amber-400 text-sm mb-3">
            🔒 Limite de démo atteinte
          </p>
          <a 
            href="/auth/register" 
            className="inline-block bg-gradient-to-r from-indigo-500 to-violet-500 text-white px-6 py-2.5 rounded-lg font-semibold text-sm hover:opacity-90 transition-opacity"
          >
            Créer un compte pour analyses illimitées →
          </a>
        </div>
      )}
    </div>
  );
};

export default PMEAnalyzer;
