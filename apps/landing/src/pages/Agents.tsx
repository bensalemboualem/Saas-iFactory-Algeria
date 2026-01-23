import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from '../i18n';

type Theme = 'dark' | 'light';

interface Agent {
  id: string;
  name: string;
  icon: string;
  description: string;
  capabilities: string[];
  category: string;
}

// Liste complète des agents IA
const allAgents: Agent[] = [
  // ===== BUSINESS =====
  { id: 'business-consultant', name: 'Consultant Business', icon: '💼', description: 'Stratégie d\'entreprise, études de marché et plans d\'affaires', capabilities: ['Études de marché', 'Business plans', 'Analyse concurrentielle', 'Stratégie croissance'], category: 'Business' },
  { id: 'marketing-expert', name: 'Expert Marketing', icon: '📣', description: 'Stratégies marketing digital et campagnes publicitaires', capabilities: ['SEO/SEM', 'Social Media', 'Content Marketing', 'Publicité'], category: 'Business' },
  { id: 'sales-coach', name: 'Coach Commercial', icon: '🎯', description: 'Techniques de vente et négociation commerciale', capabilities: ['Prospection', 'Négociation', 'Closing', 'CRM'], category: 'Business' },
  { id: 'startup-advisor', name: 'Conseiller Startup', icon: '🚀', description: 'Accompagnement création et développement startup', capabilities: ['Pitch deck', 'Levée de fonds', 'MVP', 'Growth hacking'], category: 'Business' },

  // ===== FINANCE =====
  { id: 'finance-analyst', name: 'Analyste Finance', icon: '📈', description: 'Analyse financière, comptabilité et gestion de trésorerie', capabilities: ['Bilan comptable', 'Déclarations fiscales', 'Trésorerie', 'Ratios financiers'], category: 'Finance' },
  { id: 'tax-advisor', name: 'Conseiller Fiscal', icon: '💵', description: 'Optimisation fiscale et déclarations d\'impôts', capabilities: ['IRG/IBS', 'TVA', 'Optimisation', 'Déclarations'], category: 'Finance' },
  { id: 'investment-advisor', name: 'Conseiller Investissement', icon: '💰', description: 'Stratégies d\'investissement et gestion de patrimoine', capabilities: ['Actions', 'Immobilier', 'Crypto', 'Diversification'], category: 'Finance' },
  { id: 'budget-planner', name: 'Planificateur Budget', icon: '📊', description: 'Gestion budgétaire personnelle et professionnelle', capabilities: ['Budget mensuel', 'Épargne', 'Dépenses', 'Prévisions'], category: 'Finance' },

  // ===== JURIDIQUE =====
  { id: 'legal-advisor', name: 'Conseiller Juridique', icon: '⚖️', description: 'Conseil juridique et rédaction de contrats', capabilities: ['Contrats', 'Conseils légaux', 'Veille juridique', 'Litiges'], category: 'Juridique' },
  { id: 'contract-specialist', name: 'Spécialiste Contrats', icon: '📜', description: 'Rédaction et analyse de contrats commerciaux', capabilities: ['NDA', 'CGV/CGU', 'Contrats travail', 'Partenariats'], category: 'Juridique' },
  { id: 'ip-lawyer', name: 'Expert Propriété Intellectuelle', icon: '®️', description: 'Protection marques, brevets et droits d\'auteur', capabilities: ['Marques', 'Brevets', 'Copyright', 'Licences'], category: 'Juridique' },
  { id: 'gdpr-expert', name: 'Expert RGPD', icon: '🔒', description: 'Conformité protection des données personnelles', capabilities: ['Audit RGPD', 'Politique confidentialité', 'DPO', 'Registre'], category: 'Juridique' },

  // ===== ÉDUCATION =====
  { id: 'tutor-general', name: 'Tuteur Général', icon: '🎓', description: 'Aide aux devoirs et cours particuliers tous niveaux', capabilities: ['Cours personnalisés', 'Exercices', 'Prépa examens', 'Méthodologie'], category: 'Éducation' },
  { id: 'bac-coach', name: 'Coach BAC', icon: '📚', description: 'Préparation intensive au baccalauréat algérien', capabilities: ['Révisions', 'Annales', 'Fiches', 'Simulations'], category: 'Éducation' },
  { id: 'bem-coach', name: 'Coach BEM', icon: '📝', description: 'Préparation au Brevet d\'Enseignement Moyen', capabilities: ['Maths', 'Français', 'Arabe', 'Sciences'], category: 'Éducation' },
  { id: 'language-teacher', name: 'Prof de Langues', icon: '🌍', description: 'Apprentissage des langues étrangères', capabilities: ['Anglais', 'Français', 'Espagnol', 'Allemand'], category: 'Éducation' },
  { id: 'math-tutor', name: 'Tuteur Maths', icon: '🔢', description: 'Mathématiques tous niveaux', capabilities: ['Algèbre', 'Géométrie', 'Analyse', 'Statistiques'], category: 'Éducation' },
  { id: 'science-tutor', name: 'Tuteur Sciences', icon: '🔬', description: 'Physique, Chimie et Sciences naturelles', capabilities: ['Physique', 'Chimie', 'SVT', 'Expériences'], category: 'Éducation' },

  // ===== ADMINISTRATION ALGÉRIE =====
  { id: 'cnas-agent', name: 'Agent CNAS', icon: '🏥', description: 'Guide complet pour les démarches CNAS', capabilities: ['Affiliation', 'Remboursements', 'Arrêts maladie', 'Maternité'], category: 'Admin DZ' },
  { id: 'casnos-agent', name: 'Agent CASNOS', icon: '👷', description: 'Aide pour les travailleurs non-salariés', capabilities: ['Cotisations', 'Retraite', 'Couverture santé', 'Déclarations'], category: 'Admin DZ' },
  { id: 'cnrc-agent', name: 'Agent CNRC', icon: '📋', description: 'Registre du commerce et création d\'entreprise', capabilities: ['Immatriculation', 'Modifications', 'Radiation', 'Attestations'], category: 'Admin DZ' },
  { id: 'impots-agent', name: 'Agent Impôts', icon: '🏛️', description: 'Déclarations fiscales et taxes', capabilities: ['G50', 'IRG', 'IBS', 'TAP'], category: 'Admin DZ' },
  { id: 'douanes-agent', name: 'Agent Douanes', icon: '🛃', description: 'Procédures d\'import/export', capabilities: ['Dédouanement', 'Tarifs', 'Documents', 'Franchise'], category: 'Admin DZ' },
  { id: 'anem-agent', name: 'Agent ANEM', icon: '💼', description: 'Aide à l\'emploi et recherche de travail', capabilities: ['Offres emploi', 'CV', 'Formation', 'DAIP'], category: 'Admin DZ' },
  { id: 'ansej-agent', name: 'Agent ANADE', icon: '🚀', description: 'Création d\'entreprise pour jeunes', capabilities: ['Dossier', 'Financement', 'Accompagnement', 'Avantages'], category: 'Admin DZ' },
  { id: 'passport-agent', name: 'Agent Passeport', icon: '🛂', description: 'Demande de passeport biométrique', capabilities: ['Documents', 'Rendez-vous', 'Renouvellement', 'Urgence'], category: 'Admin DZ' },

  // ===== TECHNIQUE =====
  { id: 'dev-assistant', name: 'Assistant Développeur', icon: '💻', description: 'Aide au développement et debugging', capabilities: ['Code review', 'Debug', 'Architecture', 'Best practices'], category: 'Tech' },
  { id: 'devops-expert', name: 'Expert DevOps', icon: '🔧', description: 'CI/CD, cloud et infrastructure', capabilities: ['Docker', 'Kubernetes', 'AWS/GCP', 'Terraform'], category: 'Tech' },
  { id: 'data-scientist', name: 'Data Scientist', icon: '📊', description: 'Analyse de données et machine learning', capabilities: ['Python', 'ML/AI', 'Visualisation', 'Big Data'], category: 'Tech' },
  { id: 'cybersecurity', name: 'Expert Cybersécurité', icon: '🔐', description: 'Sécurité informatique et audit', capabilities: ['Audit', 'Pentest', 'SIEM', 'Compliance'], category: 'Tech' },

  // ===== CRÉATIF =====
  { id: 'content-creator', name: 'Créateur de Contenu', icon: '✍️', description: 'Rédaction web, blogs et réseaux sociaux', capabilities: ['Articles', 'Posts sociaux', 'Scripts', 'Newsletters'], category: 'Créatif' },
  { id: 'copywriter', name: 'Copywriter', icon: '📝', description: 'Textes publicitaires et pages de vente', capabilities: ['Landing pages', 'Emails', 'Slogans', 'Storytelling'], category: 'Créatif' },
  { id: 'seo-expert', name: 'Expert SEO', icon: '🔍', description: 'Optimisation pour les moteurs de recherche', capabilities: ['Mots-clés', 'Backlinks', 'Technique', 'Contenu'], category: 'Créatif' },
  { id: 'social-manager', name: 'Community Manager', icon: '📱', description: 'Gestion des réseaux sociaux', capabilities: ['Planning', 'Engagement', 'Modération', 'Analytics'], category: 'Créatif' },

  // ===== SANTÉ & BIEN-ÊTRE =====
  { id: 'health-advisor', name: 'Conseiller Santé', icon: '🏥', description: 'Conseils santé et bien-être général', capabilities: ['Prévention', 'Nutrition', 'Sommeil', 'Exercice'], category: 'Santé' },
  { id: 'nutrition-coach', name: 'Coach Nutrition', icon: '🥗', description: 'Plans alimentaires et conseils nutritionnels', capabilities: ['Régimes', 'Menus', 'Compléments', 'Allergies'], category: 'Santé' },
  { id: 'fitness-coach', name: 'Coach Fitness', icon: '💪', description: 'Programmes d\'entraînement personnalisés', capabilities: ['Musculation', 'Cardio', 'Stretching', 'HIIT'], category: 'Santé' },
  { id: 'mental-coach', name: 'Coach Mental', icon: '🧘', description: 'Gestion du stress et développement personnel', capabilities: ['Méditation', 'Productivité', 'Confiance', 'Motivation'], category: 'Santé' },

  // ===== SUPPORT =====
  { id: 'customer-support', name: 'Support Client', icon: '🎧', description: 'Assistance client et résolution de problèmes', capabilities: ['FAQ', 'Réclamations', 'Suivi', 'Satisfaction'], category: 'Support' },
  { id: 'tech-support', name: 'Support Technique', icon: '🔧', description: 'Aide technique et dépannage', capabilities: ['Diagnostic', 'Installation', 'Configuration', 'Maintenance'], category: 'Support' },
  { id: 'hr-assistant', name: 'Assistant RH', icon: '👥', description: 'Ressources humaines et recrutement', capabilities: ['Recrutement', 'Onboarding', 'Formation', 'Paie'], category: 'Support' },
  { id: 'project-manager', name: 'Chef de Projet', icon: '📋', description: 'Gestion de projet et méthodologies agiles', capabilities: ['Planning', 'Scrum', 'Kanban', 'Reporting'], category: 'Support' },
];

// Catégories uniques
const categories = [...new Set(allAgents.map(a => a.category))];

export default function Agents() {
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

  // Filtrer les agents
  const filteredAgents = allAgents.filter(agent => {
    const matchesSearch = agent.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          agent.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || agent.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  // Gérer le clic sur "Connecter"
  const handleConnect = (agentId: string) => {
    if (!isLoggedIn) {
      localStorage.setItem('redirectTool', `agent-${agentId}`);
      navigate('/login');
    } else {
      navigate(`/chat?agent=${agentId}`);
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
            {t('agents_page_title')}
          </h1>
          <p
            style={{
              fontSize: 'clamp(16px, 3vw, 20px)',
              color: textMuted,
              maxWidth: '700px',
              margin: '0 auto',
            }}
          >
            {allAgents.length} {t('agents_page_subtitle')}
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
              placeholder={t('agents_search')}
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
              ��
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
              {t('all')} ({allAgents.length})
            </button>
            {categories.map((cat) => {
              const count = allAgents.filter(a => a.category === cat).length;
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
          {filteredAgents.length} {filteredAgents.length > 1 ? t('agents_found_plural') : t('agents_found')} {t('found')}
        </p>

        {/* Agents Grid */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
            gap: '20px',
          }}
        >
          {filteredAgents.map((agent) => (
            <div
              key={agent.id}
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
                  gap: '16px',
                  marginBottom: '16px',
                }}
              >
                <div
                  style={{
                    width: '56px',
                    height: '56px',
                    borderRadius: '14px',
                    background: isDark ? 'rgba(0, 168, 107, 0.1)' : 'rgba(0, 168, 107, 0.08)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '28px',
                  }}
                >
                  {agent.icon}
                </div>
                <div>
                  <h3
                    style={{
                      fontSize: 'clamp(16px, 2.5vw, 18px)',
                      fontWeight: 600,
                      color: textColor,
                      margin: 0,
                    }}
                  >
                    {agent.name}
                  </h3>
                  <span
                    style={{
                      fontSize: '12px',
                      color: '#00A86B',
                      fontWeight: 500,
                    }}
                  >
                    {agent.category}
                  </span>
                </div>
              </div>

              {/* Description */}
              <p
                style={{
                  color: textMuted,
                  fontSize: '14px',
                  lineHeight: 1.6,
                  marginBottom: '16px',
                  minHeight: '44px',
                }}
              >
                {agent.description}
              </p>

              {/* Capabilities */}
              <div style={{ marginBottom: '20px' }}>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                  {agent.capabilities.map((cap) => (
                    <span
                      key={cap}
                      style={{
                        background: isDark ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.04)',
                        padding: '4px 10px',
                        borderRadius: '12px',
                        fontSize: '12px',
                        color: textMuted,
                      }}
                    >
                      {cap}
                    </span>
                  ))}
                </div>
              </div>

              {/* Connect Button */}
              <button
                type="button"
                onClick={() => handleConnect(agent.id)}
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
                    <span>{t('agents_discuss')}</span>
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
        {filteredAgents.length === 0 && (
          <div
            style={{
              textAlign: 'center',
              padding: '60px 20px',
              color: textMuted,
            }}
          >
            <span style={{ fontSize: 'clamp(36px, 6vw, 48px)', display: 'block', marginBottom: '16px' }}>🤖</span>
            <p style={{ fontSize: 'clamp(16px, 2.5vw, 18px)' }}>{t('agents_no_result')} "{searchQuery}"</p>
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
            background: cardBg,
            borderRadius: '20px',
            padding: 'clamp(24px, 5vw, 48px)',
            textAlign: 'center',
            border: `2px solid #00A86B`,
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
            {t('agents_custom_title')}
          </h2>
          <p
            style={{
              color: textMuted,
              fontSize: 'clamp(14px, 2.5vw, 16px)',
              maxWidth: '500px',
              margin: '0 auto 24px',
            }}
          >
            {t('agents_custom_desc')}
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
            {isLoggedIn ? t('agents_create') : t('apps_start_free')}
          </button>
        </div>
      </div>
    </div>
  );
}
