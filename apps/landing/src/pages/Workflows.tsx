import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from '../i18n';

type Theme = 'dark' | 'light';

interface Workflow {
  id: string;
  name: string;
  icon: string;
  description: string;
  steps: string[];
  category: string;
  estimatedTime: string;
}

// Liste complète des workflows IA
const allWorkflows: Workflow[] = [
  // ===== CONTENU =====
  { id: 'content-pipeline', name: 'Pipeline de Contenu', icon: '📝', description: 'Création automatisée d\'articles de blog optimisés SEO', steps: ['Recherche', 'Rédaction', 'SEO', 'Images', 'Publication'], category: 'Contenu', estimatedTime: '15 min' },
  { id: 'blog-automation', name: 'Automatisation Blog', icon: '✍️', description: 'Génération et publication automatique d\'articles', steps: ['Idées', 'Plan', 'Rédaction', 'Révision', 'Planification'], category: 'Contenu', estimatedTime: '20 min' },
  { id: 'ebook-creator', name: 'Créateur d\'Ebook', icon: '📖', description: 'Création d\'ebooks complets de A à Z', steps: ['Structure', 'Chapitres', 'Design', 'Export PDF', 'Distribution'], category: 'Contenu', estimatedTime: '2h' },
  { id: 'newsletter-flow', name: 'Flow Newsletter', icon: '📧', description: 'Création et envoi automatisé de newsletters', steps: ['Sujet', 'Contenu', 'Design', 'Test', 'Envoi'], category: 'Contenu', estimatedTime: '30 min' },

  // ===== MARKETING =====
  { id: 'lead-generation', name: 'Génération de Leads', icon: '🎯', description: 'Pipeline complet de génération et qualification de leads', steps: ['Capture', 'Qualification', 'Scoring', 'Nurturing', 'Conversion'], category: 'Marketing', estimatedTime: 'Continu' },
  { id: 'social-media-flow', name: 'Flux Réseaux Sociaux', icon: '📱', description: 'Gestion automatisée des réseaux sociaux', steps: ['Idéation', 'Création', 'Adaptation', 'Planification', 'Analytics'], category: 'Marketing', estimatedTime: '1h/semaine' },
  { id: 'ad-campaign', name: 'Campagne Publicitaire', icon: '📣', description: 'Création et optimisation de campagnes ads', steps: ['Audience', 'Créatifs', 'A/B Test', 'Optimisation', 'Reporting'], category: 'Marketing', estimatedTime: '2h' },
  { id: 'influencer-outreach', name: 'Outreach Influenceurs', icon: '🌟', description: 'Identification et contact d\'influenceurs', steps: ['Recherche', 'Sélection', 'Contact', 'Négociation', 'Suivi'], category: 'Marketing', estimatedTime: '3h' },
  { id: 'seo-audit', name: 'Audit SEO Complet', icon: '🔍', description: 'Analyse et optimisation SEO de votre site', steps: ['Crawl', 'Analyse', 'Mots-clés', 'Recommandations', 'Suivi'], category: 'Marketing', estimatedTime: '4h' },

  // ===== VENTES =====
  { id: 'sales-pipeline', name: 'Pipeline Commercial', icon: '💼', description: 'Gestion automatisée du cycle de vente', steps: ['Prospection', 'Qualification', 'Présentation', 'Négociation', 'Closing'], category: 'Ventes', estimatedTime: 'Continu' },
  { id: 'proposal-generator', name: 'Générateur Devis', icon: '📋', description: 'Création automatique de propositions commerciales', steps: ['Brief', 'Chiffrage', 'Rédaction', 'Design', 'Envoi'], category: 'Ventes', estimatedTime: '45 min' },
  { id: 'follow-up-automation', name: 'Relances Automatiques', icon: '🔄', description: 'Séquences de relance client automatisées', steps: ['Segmentation', 'Séquence', 'Personnalisation', 'Envoi', 'Analyse'], category: 'Ventes', estimatedTime: '30 min' },
  { id: 'crm-sync', name: 'Synchronisation CRM', icon: '🔗', description: 'Intégration et synchronisation avec votre CRM', steps: ['Connexion', 'Mapping', 'Import', 'Automatisation', 'Reporting'], category: 'Ventes', estimatedTime: '1h' },

  // ===== SUPPORT CLIENT =====
  { id: 'customer-support', name: 'Support Client IA', icon: '💬', description: 'Automatisation du support client avec IA', steps: ['Réception', 'Classification', 'Réponse IA', 'Escalade', 'Suivi'], category: 'Support', estimatedTime: '24/7' },
  { id: 'ticket-triage', name: 'Triage Tickets', icon: '🎫', description: 'Classification automatique des tickets support', steps: ['Réception', 'Analyse', 'Catégorie', 'Priorité', 'Attribution'], category: 'Support', estimatedTime: 'Instantané' },
  { id: 'faq-builder', name: 'Constructeur FAQ', icon: '❓', description: 'Création et mise à jour automatique de FAQ', steps: ['Analyse questions', 'Regroupement', 'Rédaction', 'Validation', 'Publication'], category: 'Support', estimatedTime: '2h' },
  { id: 'feedback-analysis', name: 'Analyse Feedback', icon: '📊', description: 'Analyse automatique des retours clients', steps: ['Collecte', 'Sentiment', 'Catégories', 'Insights', 'Actions'], category: 'Support', estimatedTime: '1h' },

  // ===== DONNÉES =====
  { id: 'data-analysis', name: 'Analyse de Données', icon: '📈', description: 'Pipeline complet d\'analyse de données', steps: ['Import', 'Nettoyage', 'Analyse', 'Visualisation', 'Rapport'], category: 'Données', estimatedTime: '2h' },
  { id: 'report-automation', name: 'Rapports Automatiques', icon: '📑', description: 'Génération automatique de rapports périodiques', steps: ['Sources', 'Agrégation', 'Analyse', 'Format', 'Distribution'], category: 'Données', estimatedTime: '30 min' },
  { id: 'competitor-monitoring', name: 'Veille Concurrentielle', icon: '👁️', description: 'Surveillance automatique de vos concurrents', steps: ['Sources', 'Scraping', 'Analyse', 'Alertes', 'Rapport'], category: 'Données', estimatedTime: 'Continu' },
  { id: 'market-research', name: 'Étude de Marché', icon: '🌍', description: 'Recherche et analyse de marché automatisée', steps: ['Définition', 'Collecte', 'Analyse', 'Tendances', 'Recommandations'], category: 'Données', estimatedTime: '4h' },

  // ===== RH =====
  { id: 'recruitment-flow', name: 'Recrutement Automatisé', icon: '👥', description: 'Pipeline de recrutement de bout en bout', steps: ['Offre', 'Sourcing', 'Screening', 'Entretiens', 'Onboarding'], category: 'RH', estimatedTime: 'Variable' },
  { id: 'cv-screening', name: 'Tri de CV', icon: '📄', description: 'Analyse et tri automatique des candidatures', steps: ['Réception', 'Parsing', 'Scoring', 'Classement', 'Shortlist'], category: 'RH', estimatedTime: '5 min/CV' },
  { id: 'onboarding-flow', name: 'Onboarding Employé', icon: '🎯', description: 'Parcours d\'intégration automatisé', steps: ['Accueil', 'Documents', 'Formation', 'Équipement', 'Suivi'], category: 'RH', estimatedTime: '1 semaine' },
  { id: 'performance-review', name: 'Évaluation Performance', icon: '⭐', description: 'Processus d\'évaluation annuelle', steps: ['Auto-éval', 'Manager', '360°', 'Synthèse', 'Plan action'], category: 'RH', estimatedTime: '2h' },

  // ===== FINANCE =====
  { id: 'invoice-processing', name: 'Traitement Factures', icon: '🧾', description: 'Automatisation du traitement des factures', steps: ['Réception', 'OCR', 'Validation', 'Comptabilisation', 'Paiement'], category: 'Finance', estimatedTime: '2 min/facture' },
  { id: 'expense-management', name: 'Gestion Notes de Frais', icon: '💳', description: 'Automatisation des notes de frais', steps: ['Soumission', 'OCR', 'Catégorie', 'Approbation', 'Remboursement'], category: 'Finance', estimatedTime: '1 min/note' },
  { id: 'budget-tracking', name: 'Suivi Budgétaire', icon: '📊', description: 'Suivi automatique des budgets', steps: ['Définition', 'Suivi', 'Alertes', 'Ajustements', 'Reporting'], category: 'Finance', estimatedTime: 'Continu' },
  { id: 'tax-preparation', name: 'Préparation Fiscale', icon: '🏛️', description: 'Préparation des déclarations fiscales', steps: ['Collecte', 'Calculs', 'Vérification', 'Déclaration', 'Archivage'], category: 'Finance', estimatedTime: '4h' },

  // ===== E-COMMERCE =====
  { id: 'product-listing', name: 'Listing Produits', icon: '🛍️', description: 'Création automatique de fiches produits', steps: ['Import', 'Descriptions', 'Images', 'SEO', 'Publication'], category: 'E-Commerce', estimatedTime: '10 min/produit' },
  { id: 'inventory-sync', name: 'Sync Inventaire', icon: '📦', description: 'Synchronisation multi-canal de l\'inventaire', steps: ['Connexion', 'Mapping', 'Sync', 'Alertes', 'Rapports'], category: 'E-Commerce', estimatedTime: 'Temps réel' },
  { id: 'abandoned-cart', name: 'Paniers Abandonnés', icon: '🛒', description: 'Récupération automatique des paniers', steps: ['Détection', 'Segmentation', 'Email 1', 'Email 2', 'Offre'], category: 'E-Commerce', estimatedTime: 'Auto' },
  { id: 'review-management', name: 'Gestion Avis', icon: '⭐', description: 'Collecte et gestion des avis clients', steps: ['Demande', 'Collecte', 'Modération', 'Réponse', 'Analyse'], category: 'E-Commerce', estimatedTime: '15 min/jour' },

  // ===== JURIDIQUE =====
  { id: 'contract-review', name: 'Révision Contrats', icon: '⚖️', description: 'Analyse automatique de contrats', steps: ['Upload', 'OCR', 'Analyse', 'Risques', 'Recommandations'], category: 'Juridique', estimatedTime: '30 min' },
  { id: 'compliance-check', name: 'Vérification Conformité', icon: '✅', description: 'Audit de conformité automatisé', steps: ['Référentiel', 'Audit', 'Écarts', 'Actions', 'Rapport'], category: 'Juridique', estimatedTime: '2h' },
  { id: 'gdpr-audit', name: 'Audit RGPD', icon: '🔒', description: 'Audit de conformité RGPD', steps: ['Inventaire', 'Analyse', 'Risques', 'Plan action', 'Documentation'], category: 'Juridique', estimatedTime: '1 jour' },
];

// Catégories uniques
const categories = [...new Set(allWorkflows.map(w => w.category))];

export default function Workflows() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [theme, setTheme] = useState<Theme>('dark');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [isLoggedIn] = useState(() => localStorage.getItem('isLoggedIn') === 'true');

  useEffect(() => {
    const savedTheme = (localStorage.getItem('theme') as Theme) || 'dark';
    setTheme(savedTheme);

    const observer = new MutationObserver(() => {
      const currentTheme = document.documentElement.dataset.theme as Theme;
      if (currentTheme) setTheme(currentTheme);
    });

    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['data-theme'],
    });

    return () => observer.disconnect();
  }, []);

  // Filtrer les workflows
  const filteredWorkflows = allWorkflows.filter(workflow => {
    const matchesSearch = workflow.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          workflow.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || workflow.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  // Gérer le clic sur "Utiliser"
  const handleConnect = (workflowId: string) => {
    if (!isLoggedIn) {
      localStorage.setItem('redirectTool', `workflow-${workflowId}`);
      navigate('/login');
    } else {
      navigate(`/chat?workflow=${workflowId}`);
    }
  };

  const isDark = theme === 'dark';
  const bgColor = isDark ? '#1a1a1a' : '#FAF9F7';
  const cardBg = isDark ? '#262626' : '#ffffff';
  const textColor = isDark ? '#f0f0f0' : '#1F1F1F';
  const textMuted = isDark ? '#A3A3A3' : '#5D5D5D';
  const borderColor = isDark ? 'rgba(255, 255, 255, 0.12)' : 'rgba(0, 0, 0, 0.08)';
  const inputBg = isDark ? '#1f1f1f' : '#ffffff';

  return (
    <div
      style={{
        paddingTop: '120px',
        paddingBottom: '80px',
        minHeight: '100vh',
        background: bgColor,
      }}
    >
      <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '0 24px' }}>
        {/* Header */}
        <div style={{ textAlign: 'center', marginBottom: '40px' }}>
          <h1
            style={{
              fontSize: 'clamp(32px, 5vw, 48px)',
              fontWeight: 700,
              color: textColor,
              marginBottom: '16px',
            }}
          >
            {t('workflows_page_title')}
          </h1>
          <p
            style={{
              fontSize: 'clamp(16px, 3vw, 20px)',
              color: textMuted,
              maxWidth: '700px',
              margin: '0 auto',
            }}
          >
            {allWorkflows.length} {t('workflows_page_subtitle')}
          </p>
        </div>

        {/* Search & Filters */}
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '16px',
            marginBottom: '40px',
            alignItems: 'center',
          }}
        >
          {/* Search Bar */}
          <div style={{ position: 'relative', width: '100%', maxWidth: '500px' }}>
            <input
              type="text"
              placeholder={t('workflows_search')}
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              style={{
                width: '100%',
                padding: '14px 20px 14px 50px',
                borderRadius: '12px',
                border: `1px solid ${borderColor}`,
                background: inputBg,
                color: textColor,
                fontSize: '16px',
                outline: 'none',
              }}
            />
            <span
              style={{
                position: 'absolute',
                left: '18px',
                top: '50%',
                transform: 'translateY(-50%)',
                fontSize: '20px',
              }}
            >
              🔍
            </span>
          </div>

          {/* Category Filters */}
          <div
            style={{
              display: 'flex',
              flexWrap: 'wrap',
              gap: '8px',
              justifyContent: 'center',
            }}
          >
            <button
              type="button"
              onClick={() => setSelectedCategory('all')}
              style={{
                padding: '8px 16px',
                borderRadius: '20px',
                border: `1px solid ${selectedCategory === 'all' ? '#00A86B' : borderColor}`,
                background: selectedCategory === 'all' ? 'rgba(0, 168, 107, 0.15)' : 'transparent',
                color: selectedCategory === 'all' ? '#00A86B' : textMuted,
                fontSize: '14px',
                fontWeight: 500,
                cursor: 'pointer',
              }}
            >
              {t('all')} ({allWorkflows.length})
            </button>
            {categories.map((cat) => {
              const count = allWorkflows.filter(w => w.category === cat).length;
              return (
                <button
                  key={cat}
                  type="button"
                  onClick={() => setSelectedCategory(cat)}
                  style={{
                    padding: '8px 16px',
                    borderRadius: '20px',
                    border: `1px solid ${selectedCategory === cat ? '#00A86B' : borderColor}`,
                    background: selectedCategory === cat ? 'rgba(0, 168, 107, 0.15)' : 'transparent',
                    color: selectedCategory === cat ? '#00A86B' : textMuted,
                    fontSize: '14px',
                    fontWeight: 500,
                    cursor: 'pointer',
                  }}
                >
                  {cat} ({count})
                </button>
              );
            })}
          </div>
        </div>

        {/* Results Count */}
        <p style={{ color: textMuted, marginBottom: '24px', textAlign: 'center' }}>
          {filteredWorkflows.length} {filteredWorkflows.length > 1 ? t('workflows_found_plural') : t('workflows_found')} {t('found')}
        </p>

        {/* Workflows Grid */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))',
            gap: '20px',
          }}
        >
          {filteredWorkflows.map((workflow) => (
            <div
              key={workflow.id}
              style={{
                background: cardBg,
                borderRadius: '16px',
                padding: '24px',
                border: `1px solid ${borderColor}`,
                transition: 'all 0.3s ease',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-4px)';
                e.currentTarget.style.borderColor = '#00A86B';
                e.currentTarget.style.boxShadow = '0 12px 24px rgba(0, 168, 107, 0.15)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.borderColor = borderColor;
                e.currentTarget.style.boxShadow = 'none';
              }}
            >
              {/* Header */}
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  marginBottom: '16px',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <span style={{ fontSize: '32px' }}>{workflow.icon}</span>
                  <div>
                    <h3
                      style={{
                        fontSize: 'clamp(16px, 2.5vw, 18px)',
                        fontWeight: 600,
                        color: textColor,
                        margin: 0,
                      }}
                    >
                      {workflow.name}
                    </h3>
                    <span
                      style={{
                        fontSize: '12px',
                        color: '#00A86B',
                        fontWeight: 500,
                      }}
                    >
                      {workflow.category}
                    </span>
                  </div>
                </div>
                <span
                  style={{
                    background: isDark ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.04)',
                    padding: '4px 10px',
                    borderRadius: '12px',
                    fontSize: '12px',
                    color: textMuted,
                  }}
                >
                  {workflow.estimatedTime}
                </span>
              </div>

              {/* Description */}
              <p
                style={{
                  color: textMuted,
                  fontSize: '14px',
                  lineHeight: 1.6,
                  marginBottom: '16px',
                }}
              >
                {workflow.description}
              </p>

              {/* Steps */}
              <div style={{ marginBottom: '20px' }}>
                <div
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '6px',
                    overflowX: 'auto',
                    padding: '8px 0',
                  }}
                >
                  {workflow.steps.map((step, idx) => (
                    <div key={step} style={{ display: 'flex', alignItems: 'center' }}>
                      <div
                        style={{
                          background: isDark ? 'rgba(0, 168, 107, 0.15)' : 'rgba(0, 168, 107, 0.1)',
                          border: '1px solid rgba(0, 168, 107, 0.3)',
                          padding: '4px 10px',
                          borderRadius: '6px',
                          fontSize: '11px',
                          color: '#00A86B',
                          whiteSpace: 'nowrap',
                        }}
                      >
                        {step}
                      </div>
                      {idx < workflow.steps.length - 1 && (
                        <span style={{ color: textMuted, margin: '0 2px', fontSize: '12px' }}>→</span>
                      )}
                    </div>
                  ))}
                </div>
              </div>

              {/* Connect Button */}
              <button
                type="button"
                onClick={() => handleConnect(workflow.id)}
                style={{
                  width: '100%',
                  padding: '12px',
                  background: 'linear-gradient(135deg, #00A86B, #2ECC71)',
                  border: 'none',
                  borderRadius: '10px',
                  color: '#fff',
                  fontSize: '14px',
                  fontWeight: 600,
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '8px',
                }}
              >
                {isLoggedIn ? (
                  <>
                    <span>{t('workflows_use_btn')}</span>
                    <span>→</span>
                  </>
                ) : (
                  <>
                    <span>🔗</span>
                    <span>{t('connect')}</span>
                  </>
                )}
              </button>
            </div>
          ))}
        </div>

        {/* No Results */}
        {filteredWorkflows.length === 0 && (
          <div
            style={{
              textAlign: 'center',
              padding: '60px 20px',
              color: textMuted,
            }}
          >
            <span style={{ fontSize: 'clamp(36px, 6vw, 48px)', display: 'block', marginBottom: '16px' }}>🔄</span>
            <p style={{ fontSize: 'clamp(16px, 2.5vw, 18px)' }}>{t('workflows_no_result')} "{searchQuery}"</p>
            <button
              type="button"
              onClick={() => {
                setSearchQuery('');
                setSelectedCategory('all');
              }}
              style={{
                marginTop: '16px',
                padding: '10px 20px',
                background: 'transparent',
                border: `1px solid ${borderColor}`,
                borderRadius: '8px',
                color: textColor,
                cursor: 'pointer',
              }}
            >
              {t('reset_filters')}
            </button>
          </div>
        )}

        {/* CTA Section */}
        <div
          style={{
            marginTop: '60px',
            background: `linear-gradient(135deg, ${isDark ? '#1a2e1a' : '#e8f5e9'}, ${isDark ? '#1a1a2e' : '#e3f2fd'})`,
            borderRadius: '20px',
            padding: 'clamp(24px, 5vw, 48px)',
            textAlign: 'center',
            border: `1px solid ${borderColor}`,
          }}
        >
          <h2
            style={{
              fontSize: 'clamp(22px, 4vw, 28px)',
              fontWeight: 600,
              color: textColor,
              marginBottom: '16px',
            }}
          >
            {t('workflows_custom_title')}
          </h2>
          <p
            style={{
              color: textMuted,
              fontSize: 'clamp(14px, 2.5vw, 16px)',
              maxWidth: '500px',
              margin: '0 auto 24px',
            }}
          >
            {t('workflows_custom_desc')}
          </p>
          <button
            type="button"
            onClick={() => navigate(isLoggedIn ? '/chat' : '/login')}
            style={{
              padding: '16px 32px',
              background: 'linear-gradient(135deg, #00A86B, #2ECC71)',
              color: '#fff',
              fontSize: 'clamp(16px, 2.5vw, 18px)',
              fontWeight: 600,
              border: 'none',
              borderRadius: '12px',
              cursor: 'pointer',
              boxShadow: '0 4px 16px rgba(0, 168, 107, 0.3)',
            }}
          >
            {isLoggedIn ? t('workflows_create') : t('workflows_request')}
          </button>
        </div>
      </div>
    </div>
  );
}
