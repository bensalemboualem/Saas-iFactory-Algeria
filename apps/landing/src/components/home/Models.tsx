import { useState, useMemo } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from '../../i18n';
import { useTheme } from '../../hooks';
import './Models.css';

interface Model {
  name: string;
  icon?: string;
  description: string;
  tags: string[];
  free?: boolean;
  category: string;
}

const ALL_MODELS: Model[] = [
  // TEXTE
  { name: 'ChatGPT 5.2', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/openai.png', description: 'Le modèle le plus populaire au monde pour la conversation, la rédaction et l\'analyse.', tags: ['Texte', 'Code', 'Analyse'], category: 'Texte' },
  { name: 'Claude 4.5', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/claude-color.png', description: 'IA d\'Anthropic, excellente en raisonnement, rédaction longue et code.', tags: ['Texte', 'Code', 'Raisonnement'], category: 'Texte' },
  { name: 'Gemini 3', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/gemini-color.png', description: 'IA multimodale de Google, texte, image et code dans un seul modèle.', tags: ['Texte', 'Multimodal'], category: 'Texte' },
  { name: 'Grok 3', icon: 'https://cdn.worldvectorlogo.com/logos/grok-1.svg', description: 'Modèle d\'xAI avec accès temps réel aux données de X.', tags: ['Texte', 'Actualité'], category: 'Texte' },
  { name: 'DeepSeek R1', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/deepseek-color.png', description: 'Raisonnement avancé avec chaîne de pensée. Excellent en maths et logique.', tags: ['Texte', 'Maths', 'Raisonnement'], category: 'Texte' },
  { name: 'Mistral Large', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/mistral-color.png', description: 'Modèle européen performant, multilingue FR/AR/EN.', tags: ['Texte', 'Multilingue'], category: 'Texte' },
  { name: 'Qwen 3', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/qwen-color.png', description: 'Modèle d\'Alibaba, excellent en code et multilangue.', tags: ['Texte', 'Code'], category: 'Texte' },
  { name: 'Perplexity', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/perplexity-color.png', description: 'Recherche IA avec sources vérifiées en temps réel.', tags: ['Recherche', 'Sources'], category: 'Texte' },
  { name: 'Kimi', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/kimi-color.png', description: 'Contexte ultra-long, idéal pour analyser des documents entiers.', tags: ['Texte', 'Documents'], category: 'Texte' },
  // IMAGE
  { name: 'Midjourney', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/midjourney.png', description: 'Le meilleur générateur d\'images IA, style artistique inégalé.', tags: ['Image', 'Art', 'Design'], category: 'Image' },
  { name: 'DALL-E 3', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/openai.png', description: 'Génération d\'images par OpenAI, excellent suivi de prompt.', tags: ['Image', 'Texte-en-image'], category: 'Image' },
  { name: 'FLUX Pro', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/flux.png', description: 'Qualité photoréaliste exceptionnelle, rendu rapide.', tags: ['Image', 'Photoréaliste'], category: 'Image' },
  { name: 'Stable Diffusion', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/stability-color.png', description: 'Modèle open-source, personnalisable à l\'infini.', tags: ['Image', 'Open-source'], category: 'Image' },
  { name: 'Ideogram 3', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/ideogram.png', description: 'Spécialiste du texte dans les images et des logos.', tags: ['Image', 'Logo', 'Typo'], category: 'Image' },
  { name: 'Recraft V3', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/recraft.png', description: 'Design vectoriel et illustrations professionnelles.', tags: ['Image', 'Vecteur', 'Design'], category: 'Image' },
  // VIDEO
  { name: 'Sora 2', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/latest/files/light/sora.png', description: 'Génération vidéo par OpenAI, qualité cinématographique.', tags: ['Vidéo', 'Cinéma'], category: 'Vidéo' },
  { name: 'Veo 2', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/google-color.png', description: 'Vidéo IA par Google, mouvements réalistes.', tags: ['Vidéo', 'Réaliste'], category: 'Vidéo' },
  { name: 'Runway Gen-4', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/runway.png', description: 'Édition et génération vidéo professionnelle.', tags: ['Vidéo', 'Édition'], category: 'Vidéo' },
  { name: 'Kling 1.6', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/latest/files/light/kling.png', description: 'Vidéos longues avec mouvements naturels.', tags: ['Vidéo', 'Long-form'], category: 'Vidéo' },
  // AUDIO
  { name: 'ElevenLabs', icon: 'https://img.icons8.com/ios-filled/512/elevenlabs.png', description: 'Clonage vocal et synthèse vocale ultra-réaliste.', tags: ['Audio', 'Voix', 'TTS'], category: 'Audio' },
  { name: 'Suno', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/suno.png', description: 'Créez des chansons complètes avec paroles en un clic.', tags: ['Audio', 'Musique'], category: 'Audio' },
  { name: 'Whisper', icon: 'https://img.icons8.com/ios-filled/512/microphone.png', description: 'Transcription audio vers texte, supporte l\'arabe et le français.', tags: ['Audio', 'Transcription'], category: 'Audio' },
  // CODE
  { name: 'GitHub Copilot', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/github.png', description: 'Assistant code IA intégré dans VS Code et JetBrains.', tags: ['Code', 'IDE'], category: 'Code' },
  { name: 'Cursor', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/cursor.png', description: 'Éditeur de code IA-first, édition et debug automatique.', tags: ['Code', 'IDE', 'Debug'], category: 'Code' },
  { name: 'Claude Code', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/claude-color.png', description: 'Agent de code autonome par Anthropic, terminal intelligent.', tags: ['Code', 'Agent', 'CLI'], category: 'Code' },
  // LOCAL / GRATUIT
  { name: 'Ollama', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/ollama.png', description: 'Exécutez des LLMs localement sur votre machine, 100% privé.', tags: ['Local', 'Privé'], free: true, category: 'Local' },
  { name: 'Groq', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/groq.png', description: 'Inférence ultra-rapide, réponses instantanées.', tags: ['Local', 'Rapide'], free: true, category: 'Local' },
  { name: 'Llama 4', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/meta-color.png', description: 'Modèle open-source de Meta, performant et gratuit.', tags: ['Local', 'Open-source'], free: true, category: 'Local' },
  { name: 'Hugging Face', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/latest/files/light/huggingface.png', description: 'Hub de modèles IA open-source, des milliers de modèles.', tags: ['Local', 'Hub'], free: true, category: 'Local' },
];

const CATEGORIES = ['Tous', 'Texte', 'Image', 'Vidéo', 'Audio', 'Code', 'Local'];

const CATEGORY_ICONS: Record<string, string> = {
  Tous: '✨',
  Texte: '💬',
  Image: '🎨',
  Vidéo: '🎬',
  Audio: '🎵',
  Code: '💻',
  Local: '🏠',
};

export default function Models() {
  const { colors, isDark, accent } = useTheme();
  const { t } = useTranslation();
  const [search, setSearch] = useState('');
  const [activeFilter, setActiveFilter] = useState('Tous');
  const categoryLabel = (category: string) => {
    switch (category) {
      case 'Tous':
        return t('models_category_all');
      case 'Texte':
        return t('models_category_text');
      case 'Image':
        return t('models_category_image');
      case 'Vidéo':
        return t('models_category_video');
      case 'Audio':
        return t('models_category_audio');
      case 'Code':
        return t('models_category_code');
      case 'Local':
        return t('models_category_local');
      default:
        return category;
    }
  };

  const filtered = useMemo(() => {
    return ALL_MODELS.filter((m) => {
      const matchSearch =
        search === '' ||
        m.name.toLowerCase().includes(search.toLowerCase()) ||
        m.description.toLowerCase().includes(search.toLowerCase()) ||
        m.tags.some((t) => t.toLowerCase().includes(search.toLowerCase()));
      const matchCategory = activeFilter === 'Tous' || m.category === activeFilter;
      return matchSearch && matchCategory;
    });
  }, [search, activeFilter]);

  return (
    <section className="models-section-v2" id="models">
      {/* Section Title */}
      <div className="models-header">
        <span className="models-badge" style={{ background: isDark ? 'rgba(0,168,107,0.12)' : 'rgba(0,168,107,0.08)', color: accent.primary }}>
          {t('models_badge')}
        </span>
        <h2 style={{ color: colors.textPrimary }}>
          {t('models_title')}{' '}
          <span className="models-gradient-text">{t('models_title_highlight')}</span>
        </h2>
        <p style={{ color: colors.textMuted }}>
          {t('models_subtitle')}
        </p>
      </div>

      {/* Sticky Search + Filters */}
      <div
        className="models-search-bar"
        style={{
          background: isDark ? 'rgba(26,26,26,0.85)' : 'rgba(255,255,255,0.85)',
          borderBottom: `1px solid ${colors.borderColor}`,
        }}
      >
        <div className="models-search-inner">
          {/* Search */}
          <div className="models-search-input-wrap">
            <svg className="models-search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke={colors.textMuted} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="11" cy="11" r="8" />
              <line x1="21" y1="21" x2="16.65" y2="16.65" />
            </svg>
            <input
              type="text"
              placeholder={t('models_search_placeholder')}
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="models-search-input"
              style={{
                background: isDark ? '#262626' : '#f5f5f5',
                border: `1px solid ${colors.borderColor}`,
                color: colors.textPrimary,
              }}
            />
          </div>

          {/* Category Filters */}
          <div className="models-filters">
            {CATEGORIES.map((cat) => (
              <button
                key={cat}
                type="button"
                onClick={() => setActiveFilter(cat)}
                className={`models-filter-btn ${activeFilter === cat ? 'active' : ''}`}
                style={{
                  background:
                    activeFilter === cat
                      ? accent.primary
                      : isDark
                      ? '#262626'
                      : '#f0f0f0',
                  color: activeFilter === cat ? '#fff' : colors.textSecondary,
                  border: activeFilter === cat ? 'none' : `1px solid ${colors.borderColor}`,
                }}
              >
                <span>{CATEGORY_ICONS[cat]}</span>
                <span>{categoryLabel(cat)}</span>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Results count */}
      <div className="models-results-count" style={{ color: colors.textMuted }}>
        {filtered.length} modèle{filtered.length > 1 ? 's' : ''} trouvé{filtered.length > 1 ? 's' : ''}
      </div>

      {/* Cards Grid */}
      <div className="models-cards-grid">
        {filtered.map((model) => (
          <div
            key={model.name}
            className="model-card-v2"
            style={{
              background: isDark ? '#1f1f1f' : '#ffffff',
              border: `1px solid ${colors.borderColor}`,
            }}
          >
            <div className="model-card-inner">
              {/* Header: icon + name + badge */}
              <div className="model-card-head">
                <div className="model-card-identity">
                  {model.icon && (
                    <img
                      src={model.icon}
                      alt={model.name}
                      loading="lazy"
                      width="44"
                      height="44"
                      className="model-card-icon"
                    />
                  )}
                  <div>
                    <h3 className="model-card-name" style={{ color: colors.textPrimary }}>
                      {model.name}
                    </h3>
                    <span className="model-card-category" style={{ color: colors.textMuted }}>
                      {model.category}
                    </span>
                  </div>
                </div>
                <span
                  className={`model-card-badge ${model.free ? 'free' : 'premium'}`}
                >
                  {model.free ? t('models_badge_free') : t('models_badge_premium')}
                </span>
              </div>

              {/* Description */}
              <p className="model-card-desc" style={{ color: colors.textSecondary }}>
                {model.description}
              </p>

              {/* Tags */}
              <div className="model-card-tags">
                {model.tags.map((tag) => (
                  <span
                    key={tag}
                    className="model-card-tag"
                    style={{
                      background: isDark ? '#2a2a2a' : '#f5f5f5',
                      color: colors.textSecondary,
                    }}
                  >
                    {tag}
                  </span>
                ))}
              </div>

              {/* CTA */}
              <Link
                to="/login?next=/chat"
                className="model-card-cta"
                style={{
                  background: isDark ? '#fff' : '#111',
                  color: isDark ? '#111' : '#fff',
                }}
              >
                <span>{t('models_cta_try')}</span>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <line x1="5" y1="12" x2="19" y2="12" />
                  <polyline points="12 5 19 12 12 19" />
                </svg>
              </Link>
            </div>
          </div>
        ))}
      </div>

      {/* Summary */}
      <div className="models-summary-v2">
        <div
          className="models-summary-card-v2"
          style={{
            background: accent.gradient,
          }}
        >
          <div className="summary-v2-content">
            <h3>{t('models_summary_title')}</h3>
            <p>{t('models_summary_items')}</p>
          </div>
          <Link to="/pricing" className="summary-v2-cta">
            {t('models_summary_cta')}
          </Link>
        </div>
      </div>
    </section>
  );
}
