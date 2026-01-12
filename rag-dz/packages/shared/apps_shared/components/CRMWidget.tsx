import React, { useState } from 'react';

// ============================================
// Types
// ============================================
interface LeadData {
  name: string;
  email: string;
  phone?: string;
  company?: string;
  activity?: string;
  message?: string;
  source: string;
}

interface CRMWidgetProps {
  /** URL de l'API (défaut: /api/crm/leads) */
  apiUrl?: string;
  /** Source du lead (page d'origine) */
  source?: string;
  /** Titre du formulaire */
  title?: string;
  /** Sous-titre */
  subtitle?: string;
  /** Champs optionnels à afficher */
  showPhone?: boolean;
  showCompany?: boolean;
  showActivity?: boolean;
  showMessage?: boolean;
  /** Texte du bouton */
  submitText?: string;
  /** Callback après soumission réussie */
  onSuccess?: (data: LeadData) => void;
  /** Mode inline (pas de card wrapper) */
  inline?: boolean;
  /** Style personnalisé */
  className?: string;
}

// ============================================
// Options d'activité
// ============================================
const ACTIVITY_OPTIONS = [
  { value: '', label: 'Sélectionnez votre secteur...' },
  { value: 'commerce', label: '🛒 Commerce / Distribution' },
  { value: 'services', label: '💼 Services aux entreprises' },
  { value: 'tech', label: '💻 Tech / IT / Digital' },
  { value: 'industrie', label: '🏭 Industrie / Production' },
  { value: 'immobilier', label: '🏢 Immobilier / BTP' },
  { value: 'sante', label: '🏥 Santé / Médical' },
  { value: 'education', label: '🎓 Éducation / Formation' },
  { value: 'finance', label: '🏦 Finance / Assurance' },
  { value: 'transport', label: '🚚 Transport / Logistique' },
  { value: 'agriculture', label: '🌾 Agriculture / Agroalimentaire' },
  { value: 'tourisme', label: '✈️ Tourisme / Hôtellerie' },
  { value: 'autre', label: '📋 Autre' },
];

// ============================================
// Composant Principal
// ============================================
export const CRMWidget: React.FC<CRMWidgetProps> = ({
  apiUrl = '/api/crm/leads',
  source = 'website',
  title = '📬 Restez informé',
  subtitle = 'Recevez nos conseils IA pour les entreprises algériennes',
  showPhone = false,
  showCompany = true,
  showActivity = true,
  showMessage = false,
  submitText = 'Je m\'inscris →',
  onSuccess,
  inline = false,
  className = '',
}) => {
  // State
  const [formData, setFormData] = useState<Partial<LeadData>>({
    name: '',
    email: '',
    phone: '',
    company: '',
    activity: '',
    message: '',
    source,
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Validation email
  const isValidEmail = (email: string): boolean => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  };

  // Handle input change
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    setError(null);
  };

  // Submit
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validation
    if (!formData.name?.trim()) {
      setError('Veuillez entrer votre nom');
      return;
    }
    if (!formData.email?.trim() || !isValidEmail(formData.email)) {
      setError('Veuillez entrer un email valide');
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Erreur ${response.status}`);
      }

      setIsSuccess(true);
      
      if (onSuccess) {
        onSuccess(formData as LeadData);
      }

    } catch (err) {
      console.error('Erreur CRM:', err);
      setError(err instanceof Error ? err.message : 'Une erreur est survenue');
    } finally {
      setIsSubmitting(false);
    }
  };

  // Wrapper conditionnel
  const Wrapper = inline ? React.Fragment : ({ children }: { children: React.ReactNode }) => (
    <div className={`
      bg-slate-900 border border-slate-700 rounded-2xl overflow-hidden
      shadow-xl shadow-black/20 max-w-md w-full
      ${className}
    `}>
      {children}
    </div>
  );

  // Succès
  if (isSuccess) {
    return (
      <Wrapper>
        <div className="p-8 text-center">
          <div className="text-5xl mb-4">🎉</div>
          <h3 className="text-xl font-bold text-white mb-2">
            Merci pour votre inscription !
          </h3>
          <p className="text-slate-400 text-sm">
            Vous recevrez bientôt nos conseils et actualités IA.
          </p>
          <div className="mt-6 p-4 bg-emerald-500/10 border border-emerald-500/30 rounded-lg">
            <p className="text-emerald-400 text-sm">
              ✅ Votre demande a été enregistrée
            </p>
          </div>
        </div>
      </Wrapper>
    );
  }

  return (
    <Wrapper>
      {/* Header */}
      {!inline && (
        <div className="bg-gradient-to-r from-purple-600 to-pink-600 px-6 py-4">
          <h3 className="text-white font-bold text-lg">{title}</h3>
          {subtitle && (
            <p className="text-white/80 text-sm mt-1">{subtitle}</p>
          )}
        </div>
      )}

      {/* Formulaire */}
      <form onSubmit={handleSubmit} className={inline ? '' : 'p-6'}>
        <div className="space-y-4">
          {/* Nom */}
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-1.5">
              Nom complet *
            </label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="Votre nom"
              className="
                w-full bg-slate-800 border border-slate-600 rounded-lg px-4 py-2.5
                text-white placeholder-slate-500 text-sm
                focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500
              "
              disabled={isSubmitting}
            />
          </div>

          {/* Email */}
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-1.5">
              Email professionnel *
            </label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="votre@email.com"
              className="
                w-full bg-slate-800 border border-slate-600 rounded-lg px-4 py-2.5
                text-white placeholder-slate-500 text-sm
                focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500
              "
              disabled={isSubmitting}
            />
          </div>

          {/* Téléphone (optionnel) */}
          {showPhone && (
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-1.5">
                Téléphone
              </label>
              <input
                type="tel"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                placeholder="+213 5XX XX XX XX"
                className="
                  w-full bg-slate-800 border border-slate-600 rounded-lg px-4 py-2.5
                  text-white placeholder-slate-500 text-sm
                  focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500
                "
                disabled={isSubmitting}
              />
            </div>
          )}

          {/* Entreprise (optionnel) */}
          {showCompany && (
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-1.5">
                Entreprise
              </label>
              <input
                type="text"
                name="company"
                value={formData.company}
                onChange={handleChange}
                placeholder="Nom de votre entreprise"
                className="
                  w-full bg-slate-800 border border-slate-600 rounded-lg px-4 py-2.5
                  text-white placeholder-slate-500 text-sm
                  focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500
                "
                disabled={isSubmitting}
              />
            </div>
          )}

          {/* Secteur d'activité (optionnel) */}
          {showActivity && (
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-1.5">
                Secteur d'activité
              </label>
              <select
                name="activity"
                value={formData.activity}
                onChange={handleChange}
                className="
                  w-full bg-slate-800 border border-slate-600 rounded-lg px-4 py-2.5
                  text-white text-sm
                  focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500
                "
                disabled={isSubmitting}
              >
                {ACTIVITY_OPTIONS.map(opt => (
                  <option key={opt.value} value={opt.value}>{opt.label}</option>
                ))}
              </select>
            </div>
          )}

          {/* Message (optionnel) */}
          {showMessage && (
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-1.5">
                Message (optionnel)
              </label>
              <textarea
                name="message"
                value={formData.message}
                onChange={handleChange}
                placeholder="Décrivez votre besoin..."
                rows={3}
                className="
                  w-full bg-slate-800 border border-slate-600 rounded-lg px-4 py-2.5
                  text-white placeholder-slate-500 text-sm resize-none
                  focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500
                "
                disabled={isSubmitting}
              />
            </div>
          )}

          {/* Error */}
          {error && (
            <div className="bg-red-900/30 border border-red-700 text-red-300 rounded-lg px-4 py-2.5 text-sm">
              ⚠️ {error}
            </div>
          )}

          {/* Submit */}
          <button
            type="submit"
            disabled={isSubmitting}
            className="
              w-full bg-gradient-to-r from-purple-500 to-pink-500 
              hover:from-purple-400 hover:to-pink-400
              text-white font-semibold py-3 px-6 rounded-lg
              disabled:opacity-50 disabled:cursor-not-allowed
              transition-all duration-200
              flex items-center justify-center gap-2
            "
          >
            {isSubmitting ? (
              <>
                <span className="animate-spin">⏳</span>
                Envoi en cours...
              </>
            ) : (
              submitText
            )}
          </button>

          {/* RGPD */}
          <p className="text-slate-500 text-xs text-center">
            🔒 Vos données sont protégées et ne seront jamais partagées.
          </p>
        </div>
      </form>
    </Wrapper>
  );
};

// ============================================
// Version popup/modal
// ============================================
interface CRMPopupProps extends CRMWidgetProps {
  isOpen: boolean;
  onClose: () => void;
}

export const CRMPopup: React.FC<CRMPopupProps> = ({ isOpen, onClose, ...props }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-black/60 backdrop-blur-sm"
        onClick={onClose}
      />
      
      {/* Modal */}
      <div className="relative z-10 animate-[fadeInUp_0.3s_ease-out]">
        <button
          onClick={onClose}
          className="absolute -top-3 -right-3 w-8 h-8 bg-slate-700 hover:bg-slate-600 rounded-full flex items-center justify-center text-slate-300 z-20"
        >
          ✕
        </button>
        <CRMWidget {...props} />
      </div>
    </div>
  );
};

export default CRMWidget;
