import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from '../i18n';

type Theme = 'dark' | 'light';

interface App {
  id: string;
  name: string;
  icon: string;
  description: string;
  features: string[];
  category: string;
  status: 'available' | 'coming_soon' | 'beta';
  statusColor: string;
  statusText: string;
}

// Liste complète des applications IA
const allApps: App[] = [
  // ===== PRODUCTIVITÉ =====
  { id: 'cv-builder', name: 'CV Builder IA', icon: '📄', description: 'Créez des CV professionnels optimisés pour les ATS', features: ['Templates modernes', 'Optimisation ATS', 'Export PDF', 'Multi-langues'], category: 'Productivité', status: 'available', statusColor: '#00A86B', statusText: 'Disponible' },
  { id: 'document-editor', name: 'Éditeur Documents IA', icon: '📝', description: 'Rédigez et éditez des documents avec l\'aide de l\'IA', features: ['Rédaction assistée', 'Correction', 'Formatage', 'Export'], category: 'Productivité', status: 'available', statusColor: '#00A86B', statusText: 'Disponible' },
  { id: 'presentation-maker', name: 'Créateur Présentations', icon: '🎯', description: 'Générez des présentations professionnelles automatiquement', features: ['Design auto', 'Templates', 'Animations', 'Export PPT'], category: 'Productivité', status: 'available', statusColor: '#00A86B', statusText: 'Disponible' },
  { id: 'note-taker', name: 'Prise de Notes IA', icon: '📋', description: 'Notes intelligentes avec résumé automatique', features: ['Transcription', 'Résumé', 'Tags auto', 'Recherche'], category: 'Productivité', status: 'available', statusColor: '#00A86B', statusText: 'Disponible' },
  { id: 'task-manager', name: 'Gestionnaire Tâches', icon: '✅', description: 'Organisez vos tâches avec l\'IA', features: ['Priorisation', 'Rappels', 'Collaboration', 'Analytics'], category: 'Productivité', status: 'beta', statusColor: '#3B82F6', statusText: 'Bêta' },
  { id: 'calendar-ai', name: 'Calendrier IA', icon: '📅', description: 'Planification intelligente de votre emploi du temps', features: ['Auto-scheduling', 'Rappels smart', 'Sync calendriers', 'Suggestions'], category: 'Productivité', status: 'available', statusColor: '#00A86B', statusText: 'Disponible' },

  // ===== CRÉATION =====
  { id: 'image-studio', name: 'Studio Images IA', icon: '🎨', description: 'Générez et éditez des images avec l\'IA', features: ['Génération', 'Retouche', 'Styles', 'Upscaling'], category: 'Création', status: 'available', statusColor: '#00A86B', statusText: 'Disponible' },
  { id: 'video-studio', name: 'Studio Vidéo IA', icon: '🎬', description: 'Créez et montez des vidéos automatiquement', features: ['Montage auto', 'Sous-titres', 'Effets', 'Export HD'], category: 'Création', status: 'coming_soon', statusColor: '#F59E0B', statusText: 'Bientôt' },
  { id: 'audio-studio', name: 'Studio Audio IA', icon: '🎵', description: 'Créez de la musique et des podcasts', features: ['Voix off', 'Musique', 'Nettoyage', 'Export MP3'], category: 'Création', status: 'beta', statusColor: '#3B82F6', statusText: 'Bêta' },
  { id: 'logo-maker', name: 'Créateur Logos', icon: '✨', description: 'Créez des logos professionnels en minutes', features: ['100+ styles', 'Vecteur', 'Palette', 'Variations'], category: 'Création', status: 'available', statusColor: '#00A86B', statusText: 'Disponible' },
  { id: 'banner-studio', name: 'Studio Bannières', icon: '🖼️', description: 'Créez des bannières pour tous vos réseaux', features: ['Multi-formats', 'Templates', 'Animation', 'Export'], category: 'Création', status: 'available', statusColor: '#00A86B', statusText: 'Disponible' },
  { id: '3d-model-maker', name: 'Modélisation 3D', icon: '🎲', description: 'Créez des modèles 3D avec l\'IA', features: ['Text-to-3D', 'Textures', 'Animation', 'Export GLB'], category: 'Création', status: 'coming_soon', statusColor: '#F59E0B', statusText: 'Bientôt' },

  // ===== BUSINESS =====
  { id: 'crm-app', name: 'CRM Intelligent', icon: '👥', description: 'Gérez vos clients avec l\'intelligence artificielle', features: ['Contacts', 'Pipeline', 'Automatisation', 'Rapports'], category: 'Business', status: 'available', statusColor: '#00A86B', statusText: 'Disponible' },
  { id: 'invoice-app', name: 'Facturation IA', icon: '🧾', description: 'Créez et gérez vos factures automatiquement', features: ['Templates', 'Suivi paiements', 'Rappels', 'Export'], category: 'Business', status: 'available', statusColor: '#00A86B', statusText: 'Disponible' },
  { id: 'accounting-app', name: 'Comptabilité IA', icon: '📊', description: 'Comptabilité simplifiée pour entrepreneurs', features: ['Saisie auto', 'Rapports', 'TVA', 'Export comptable'], category: 'Business', status: 'beta', statusColor: '#3B82F6', statusText: 'Bêta' },
  { id: 'hr-app', name: 'RH Manager', icon: '💼', description: 'Gestion des ressources humaines', features: ['Recrutement', 'Onboarding', 'Paie', 'Congés'], category: 'Business', status: 'coming_soon', statusColor: '#F59E0B', statusText: 'Bientôt' },
  { id: 'project-app', name: 'Gestion Projets', icon: '📋', description: 'Gérez vos projets efficacement', features: ['Kanban', 'Gantt', 'Équipes', 'Deadlines'], category: 'Business', status: 'available', statusColor: '#00A86B', statusText: 'Disponible' },
  { id: 'business-plan', name: 'Business Plan IA', icon: '📑', description: 'Générez votre business plan complet', features: ['Templates DZ', 'Projections', 'SWOT auto', 'Export PDF'], category: 'Business', status: 'available', statusColor: '#00A86B', statusText: 'Disponible' },

  // ===== MARKETING =====
  { id: 'social-manager', name: 'Social Media Manager', icon: '📱', description: 'Gérez tous vos réseaux sociaux', features: ['Planning', 'Publication', 'Analytics', 'Multi-comptes'], category: 'Marketing', status: 'available', statusColor: '#00A86B', statusText: 'Disponible' },
  { id: 'email-marketing', name: 'Email Marketing', icon: '📧', description: 'Campagnes email automatisées', features: ['Templates', 'Séquences', 'A/B Testing', 'Analytics'], category: 'Marketing', status: 'available', statusColor: '#00A86B', statusText: 'Disponible' },
  { id: 'seo-tools', name: 'SEO Tools', icon: '🔍', description: 'Optimisez votre référencement', features: ['Audit', 'Mots-clés', 'Backlinks', 'Suivi positions'], category: 'Marketing', status: 'available', statusColor: '#00A86B', statusText: 'Disponible' },
  { id: 'analytics-dashboard', name: 'Analytics Dashboard', icon: '📈', description: 'Tableau de bord analytique complet', features: ['Multi-sources', 'Visualisation', 'Rapports', 'Alertes'], category: 'Marketing', status: 'beta', statusColor: '#3B82F6', statusText: 'Bêta' },
  { id: 'ad-manager', name: 'Ads Manager', icon: '📣', description: 'Gérez vos publicités multi-plateformes', features: ['Google', 'Facebook', 'Optimisation', 'Budget'], category: 'Marketing', status: 'coming_soon', statusColor: '#F59E0B', statusText: 'Bientôt' },

  // ===== E-COMMERCE =====
  { id: 'store-builder', name: 'Store Builder', icon: '🛍️', description: 'Créez votre boutique en ligne', features: ['Templates', 'Paiement DZ', 'Inventaire', 'Livraison'], category: 'E-Commerce', status: 'available', statusColor: '#00A86B', statusText: 'Disponible' },
  { id: 'product-manager', name: 'Product Manager', icon: '📦', description: 'Gérez votre catalogue produits', features: ['Descriptions IA', 'Photos', 'Prix', 'Stock'], category: 'E-Commerce', status: 'available', statusColor: '#00A86B', statusText: 'Disponible' },
  { id: 'order-tracker', name: 'Order Tracker', icon: '🚚', description: 'Suivi des commandes et livraisons', features: ['Temps réel', 'SMS', 'Historique', 'Retours'], category: 'E-Commerce', status: 'available', statusColor: '#00A86B', statusText: 'Disponible' },
  { id: 'marketplace-sync', name: 'Marketplace Sync', icon: '🔗', description: 'Synchronisation multi-marketplaces', features: ['Jumia', 'Ouedkniss', 'Facebook', 'Stock sync'], category: 'E-Commerce', status: 'beta', statusColor: '#3B82F6', statusText: 'Bêta' },
  { id: 'pricing-optimizer', name: 'Optimiseur Prix', icon: '💰', description: 'Optimisez vos prix avec l\'IA', features: ['Analyse marché', 'Concurrence', 'Marge auto', 'Alertes'], category: 'E-Commerce', status: 'available', statusColor: '#00A86B', statusText: 'Disponible' },

  // ===== ÉDUCATION =====
  { id: 'academy-app', name: 'Academy IA', icon: '🎓', description: 'Plateforme d\'apprentissage personnalisée', features: ['Cours IA', 'Quiz', 'Certificats', 'Progression'], category: 'Éducation', status: 'available', statusColor: '#00A86B', statusText: 'Disponible' },
  { id: 'tutor-app', name: 'Tuteur Personnel', icon: '👨‍🏫', description: 'Tuteur IA pour étudiants', features: ['Tous sujets', 'Exercices', 'Corrections', 'Fiches'], category: 'Éducation', status: 'available', statusColor: '#00A86B', statusText: 'Disponible' },
  { id: 'exam-prep', name: 'Prépa Examens', icon: '📚', description: 'Préparation aux examens algériens', features: ['BAC', 'BEM', 'QCM', 'Annales'], category: 'Éducation', status: 'available', statusColor: '#00A86B', statusText: 'Disponible' },
  { id: 'flashcards', name: 'Flashcards IA', icon: '🃏', description: 'Mémorisation avec répétition espacée', features: ['Génération auto', 'Spaced rep', 'Stats', 'Import'], category: 'Éducation', status: 'available', statusColor: '#00A86B', statusText: 'Disponible' },
  { id: 'language-learning', name: 'Apprendre Langues', icon: '🌍', description: 'Apprenez l\'anglais, français ou arabe', features: ['Conversation IA', 'Grammaire', 'Vocabulaire', 'Tests'], category: 'Éducation', status: 'available', statusColor: '#00A86B', statusText: 'Disponible' },
  { id: 'homework-helper', name: 'Aide Devoirs', icon: '✏️', description: 'Assistant pour résoudre les exercices', features: ['Maths', 'Physique', 'Sciences', 'Explications'], category: 'Éducation', status: 'available', statusColor: '#00A86B', statusText: 'Disponible' },

  // ===== DÉVELOPPEMENT =====
  { id: 'code-editor', name: 'Code Editor IA', icon: '💻', description: 'Éditeur de code avec assistance IA', features: ['Autocomplétion', 'Debug', 'Refactoring', 'Multi-lang'], category: 'Développement', status: 'available', statusColor: '#00A86B', statusText: 'Disponible' },
  { id: 'api-portal', name: 'API Portal', icon: '🔌', description: 'Accès aux APIs IA Factory', features: ['Documentation', 'Clés API', 'Usage', 'Support'], category: 'Développement', status: 'available', statusColor: '#00A86B', statusText: 'Disponible' },
  { id: 'no-code-builder', name: 'No-Code Builder', icon: '🧩', description: 'Créez des apps sans coder', features: ['Drag & drop', 'Templates', 'Intégrations', 'Publish'], category: 'Développement', status: 'beta', statusColor: '#3B82F6', statusText: 'Bêta' },
  { id: 'database-studio', name: 'Database Studio', icon: '🗄️', description: 'Gestion de bases de données', features: ['Visual', 'Requêtes IA', 'Migration', 'Backup'], category: 'Développement', status: 'coming_soon', statusColor: '#F59E0B', statusText: 'Bientôt' },
  { id: 'git-assistant', name: 'Git Assistant', icon: '🔀', description: 'Assistant pour Git et versioning', features: ['Commits IA', 'Merge helper', 'Conflits', 'Historique'], category: 'Développement', status: 'available', statusColor: '#00A86B', statusText: 'Disponible' },

  // ===== JURIDIQUE =====
  { id: 'legal-assistant', name: 'Assistant Juridique', icon: '⚖️', description: 'Aide juridique pour entrepreneurs', features: ['Contrats', 'Conseils', 'Veille', 'Templates'], category: 'Juridique', status: 'available', statusColor: '#00A86B', statusText: 'Disponible' },
  { id: 'contract-generator', name: 'Générateur Contrats', icon: '📜', description: 'Créez des contrats personnalisés', features: ['50+ modèles', 'Personnalisation', 'Signature', 'Archivage'], category: 'Juridique', status: 'available', statusColor: '#00A86B', statusText: 'Disponible' },
  { id: 'droit-travail-dz', name: 'Droit Travail DZ', icon: '📋', description: 'Guide du droit du travail algérien', features: ['Code travail', 'Licenciement', 'Congés', 'Salaires'], category: 'Juridique', status: 'available', statusColor: '#00A86B', statusText: 'Disponible' },
  { id: 'registre-commerce', name: 'Registre Commerce', icon: '🏢', description: 'Aide création entreprise en Algérie', features: ['CNRC', 'Statuts', 'Formulaires', 'Suivi'], category: 'Juridique', status: 'available', statusColor: '#00A86B', statusText: 'Disponible' },

  // ===== ADMIN DZ =====
  { id: 'admin-dz', name: 'Admin DZ', icon: '🇩🇿', description: 'Guide démarches administratives algériennes', features: ['CNAS', 'CNRC', 'Impôts', 'Douanes'], category: 'Admin DZ', status: 'available', statusColor: '#00A86B', statusText: 'Disponible' },
  { id: 'tax-calculator', name: 'Calculateur Impôts', icon: '🧮', description: 'Calculez vos impôts et taxes', features: ['IRG', 'IBS', 'TVA', 'TAP'], category: 'Admin DZ', status: 'available', statusColor: '#00A86B', statusText: 'Disponible' },
  { id: 'cnas-assistant', name: 'Assistant CNAS', icon: '🏥', description: 'Aide pour les démarches CNAS/CASNOS', features: ['Cotisations', 'Remboursements', 'Formulaires', 'Simulation'], category: 'Admin DZ', status: 'available', statusColor: '#00A86B', statusText: 'Disponible' },
  { id: 'baridimob-helper', name: 'BaridiMob Helper', icon: '💳', description: 'Guide paiements et transferts BaridiMob', features: ['Virement', 'Recharge', 'Factures', 'Support'], category: 'Admin DZ', status: 'available', statusColor: '#00A86B', statusText: 'Disponible' },
  { id: 'visa-dz', name: 'Visa & Passeport DZ', icon: '🛂', description: 'Démarches visa et passeport biométrique', features: ['RDV en ligne', 'Documents', 'Suivi', 'FAQ'], category: 'Admin DZ', status: 'available', statusColor: '#00A86B', statusText: 'Disponible' },
];

// Catégories uniques
const categories = [...new Set(allApps.map(a => a.category))];

export default function Apps() {
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

  // Filtrer les apps
  const filteredApps = allApps.filter(app => {
    const matchesSearch = app.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          app.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || app.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  // Gérer le clic sur "Ouvrir"
  const handleConnect = (appId: string, status: string) => {
    if (status === 'coming_soon') return;

    if (!isLoggedIn) {
      localStorage.setItem('redirectTool', `app-${appId}`);
      navigate('/login');
    } else {
      navigate(`/chat?app=${appId}`);
    }
  };

  const isDark = theme === 'dark';
  const bgColor = isDark ? '#1a1a1a' : '#FAF9F7';
  const cardBg = isDark ? '#262626' : '#ffffff';
  const textColor = isDark ? '#f0f0f0' : '#1F1F1F';
  const textMuted = isDark ? '#A3A3A3' : '#5D5D5D';
  const borderColor = isDark ? 'rgba(255, 255, 255, 0.12)' : 'rgba(0, 0, 0, 0.08)';
  const inputBg = isDark ? '#1f1f1f' : '#ffffff';

  const availableCount = allApps.filter(a => a.status === 'available').length;
  const betaCount = allApps.filter(a => a.status === 'beta').length;

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
            {t('apps_page_title')}
          </h1>
          <p
            style={{
              fontSize: 'clamp(16px, 3vw, 20px)',
              color: textMuted,
              maxWidth: '700px',
              margin: '0 auto',
            }}
          >
            {allApps.length} {t('apps_page_subtitle')} • {availableCount} {t('apps_available_count')} • {betaCount} {t('apps_beta_count')}
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
              placeholder={t('apps_search')}
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
              {t('apps_all')} ({allApps.length})
            </button>
            {categories.map((cat) => {
              const count = allApps.filter(a => a.category === cat).length;
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
          {filteredApps.length} {filteredApps.length > 1 ? t('apps_found_plural') : t('apps_found')} {t('found')}
        </p>

        {/* Apps Grid */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
            gap: '20px',
          }}
        >
          {filteredApps.map((app) => (
            <div
              key={app.id}
              style={{
                background: cardBg,
                borderRadius: '16px',
                padding: '24px',
                border: `1px solid ${borderColor}`,
                transition: 'all 0.3s ease',
                position: 'relative',
                opacity: app.status === 'coming_soon' ? 0.7 : 1,
              }}
              onMouseEnter={(e) => {
                if (app.status !== 'coming_soon') {
                  e.currentTarget.style.transform = 'translateY(-4px)';
                  e.currentTarget.style.borderColor = '#00A86B';
                  e.currentTarget.style.boxShadow = '0 12px 24px rgba(0, 168, 107, 0.15)';
                }
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.borderColor = borderColor;
                e.currentTarget.style.boxShadow = 'none';
              }}
            >
              {/* Status Badge */}
              <div
                style={{
                  position: 'absolute',
                  top: '16px',
                  right: '16px',
                  background: app.statusColor,
                  color: '#fff',
                  padding: '4px 12px',
                  borderRadius: '20px',
                  fontSize: '12px',
                  fontWeight: 500,
                }}
              >
                {app.statusText}
              </div>

              {/* Icon */}
              <div style={{ fontSize: '48px', marginBottom: '16px' }}>
                {app.icon}
              </div>

              {/* Name & Category */}
              <h3
                style={{
                  fontSize: 'clamp(16px, 2.5vw, 18px)',
                  fontWeight: 600,
                  color: textColor,
                  marginBottom: '4px',
                }}
              >
                {app.name}
              </h3>
              <span
                style={{
                  fontSize: '12px',
                  color: '#00A86B',
                  fontWeight: 500,
                }}
              >
                {app.category}
              </span>

              {/* Description */}
              <p
                style={{
                  color: textMuted,
                  fontSize: '14px',
                  lineHeight: 1.6,
                  marginTop: '12px',
                  marginBottom: '16px',
                }}
              >
                {app.description}
              </p>

              {/* Features */}
              <div style={{ marginBottom: '20px' }}>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                  {app.features.map((feature) => (
                    <span
                      key={feature}
                      style={{
                        background: isDark ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.04)',
                        padding: '4px 10px',
                        borderRadius: '12px',
                        fontSize: '12px',
                        color: textMuted,
                      }}
                    >
                      {feature}
                    </span>
                  ))}
                </div>
              </div>

              {/* Connect Button */}
              <button
                type="button"
                onClick={() => handleConnect(app.id, app.status)}
                disabled={app.status === 'coming_soon'}
                style={{
                  width: '100%',
                  padding: '12px',
                  background: app.status === 'coming_soon'
                    ? 'transparent'
                    : 'linear-gradient(135deg, #00A86B, #2ECC71)',
                  border: app.status === 'coming_soon'
                    ? `1px solid ${borderColor}`
                    : 'none',
                  borderRadius: '10px',
                  color: app.status === 'coming_soon' ? textMuted : '#fff',
                  fontSize: '14px',
                  fontWeight: 600,
                  cursor: app.status === 'coming_soon' ? 'not-allowed' : 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '8px',
                }}
              >
                {app.status === 'coming_soon' ? (
                  t('apps_coming_soon_btn')
                ) : isLoggedIn ? (
                  <>
                    <span>{t('apps_open_btn')}</span>
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
        {filteredApps.length === 0 && (
          <div
            style={{
              textAlign: 'center',
              padding: '60px 20px',
              color: textMuted,
            }}
          >
            <span style={{ fontSize: 'clamp(36px, 6vw, 48px)', display: 'block', marginBottom: '16px' }}>📱</span>
            <p style={{ fontSize: 'clamp(16px, 2.5vw, 18px)' }}>{t('apps_no_result')} "{searchQuery}"</p>
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
            {t('apps_cta_title')}
          </h2>
          <p
            style={{
              color: textMuted,
              fontSize: 'clamp(14px, 2.5vw, 16px)',
              maxWidth: '500px',
              margin: '0 auto 24px',
            }}
          >
            {t('apps_cta_desc')} {availableCount} {t('apps_cta_desc2')}
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
            {isLoggedIn ? t('apps_access') : t('apps_start_free')}
          </button>
        </div>
      </div>
    </div>
  );
}
