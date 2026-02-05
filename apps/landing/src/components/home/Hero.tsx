import { Link } from 'react-router-dom';
import { useTheme } from '../../hooks/useTheme';
import { useTranslation } from '../../i18n';
import './Hero.css';

const AI_PROVIDERS = [
  { name: 'ChatGPT', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/openai.png' },
  { name: 'Claude', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/claude-color.png' },
  { name: 'Gemini', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/gemini-color.png' },
  { name: 'Perplexity', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/perplexity-color.png' },
  { name: 'Grok', icon: 'https://cdn.worldvectorlogo.com/logos/grok-1.svg' },
  { name: 'Llama', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/meta-color.png' },
  { name: 'Mistral', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/mistral-color.png' },
  { name: 'DeepSeek', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/deepseek-color.png' },
  { name: 'Qwen', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/qwen-color.png' },
  { name: 'Midjourney', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/midjourney.png' },
  { name: 'FLUX', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/flux.png' },
  { name: 'ElevenLabs', icon: 'https://img.icons8.com/ios-filled/512/elevenlabs.png' },
  { name: 'Stable Diffusion', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/stability-color.png' },
];

export default function Hero() {
  const { theme } = useTheme();
  const isDark = theme === 'dark';
  const { t } = useTranslation();
  const subtitleLine2 = t('hero_subtitle_line2');
  const priceMatch = subtitleLine2.match(/([0-9][0-9\s,]*\s?DZD\/(?:mois|month))/);
  const priceText = priceMatch ? priceMatch[1] : '2 500 DZD/mois';
  const subtitleParts = priceMatch ? subtitleLine2.split(priceText) : [subtitleLine2, ''];

  return (
    <section className="hero-v2">
      {/* Social proof badge */}
      <div
        className="hero-badge"
        style={{
          background: isDark ? 'rgba(0, 168, 107, 0.12)' : 'rgba(0, 168, 107, 0.08)',
          color: '#00A86B',
          border: `1px solid ${isDark ? 'rgba(0, 168, 107, 0.25)' : 'rgba(0, 168, 107, 0.2)'}`,
        }}
      >
        <span className="hero-badge-dot" />
        {t('hero_badge')}
      </div>

      {/* Main headline */}
      <h1 className="hero-title">
        {t('hero_title_main')},{' '}
        <span className="hero-gradient-text">{t('hero_title_highlight')}</span>
      </h1>

      {/* Subtitle */}
      <p
        className="hero-subtitle"
        style={{ color: isDark ? 'rgba(255,255,255,0.55)' : 'rgba(0,0,0,0.5)' }}
      >
        {t('hero_subtitle_line1')}
        <br />
        {subtitleParts[0]}
        <strong style={{ color: '#00A86B' }}>{priceText}</strong>
        {subtitleParts[1]}
      </p>

      {/* CTA buttons */}
      <div className="hero-cta-group">
        <Link to="/chat" className="hero-cta-primary">
          {t('hero_cta_primary')}
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M6 3l5 5-5 5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </Link>
        <Link
          to="/pricing"
          className="hero-cta-secondary"
          style={{
            background: isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.04)',
            color: isDark ? 'rgba(255,255,255,0.8)' : 'rgba(0,0,0,0.7)',
            border: `1px solid ${isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)'}`,
          }}
        >
          {t('hero_cta_secondary')}
        </Link>
      </div>

      {/* Provider marquee */}
      <div className="hero-marquee-wrap">
        <p
          className="hero-marquee-label"
          style={{ color: isDark ? 'rgba(255,255,255,0.35)' : 'rgba(0,0,0,0.35)' }}
        >
          {t('hero_marquee_label')}
        </p>
        <div className="hero-marquee">
          <div className="hero-marquee-track">
            {AI_PROVIDERS.map((p) => (
              <div
                key={p.name}
                className="hero-provider-chip"
                style={{
                  background: isDark ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.03)',
                  border: `1px solid ${isDark ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.06)'}`,
                }}
              >
                <img src={p.icon} alt={p.name} width={20} height={20} loading="lazy" />
                <span style={{ color: isDark ? 'rgba(255,255,255,0.7)' : 'rgba(0,0,0,0.65)' }}>
                  {p.name}
                </span>
              </div>
            ))}
            {AI_PROVIDERS.map((p) => (
              <div
                key={`${p.name}-dup`}
                className="hero-provider-chip"
                style={{
                  background: isDark ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.03)',
                  border: `1px solid ${isDark ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.06)'}`,
                }}
              >
                <img src={p.icon} alt={p.name} width={20} height={20} loading="lazy" />
                <span style={{ color: isDark ? 'rgba(255,255,255,0.7)' : 'rgba(0,0,0,0.65)' }}>
                  {p.name}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
