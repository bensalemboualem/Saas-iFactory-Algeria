import { Link } from 'react-router-dom';
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
  { name: 'Kimi', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/kimi-color.png' },
  { name: 'Midjourney', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/midjourney.png' },
  { name: 'FLUX', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/flux.png' },
  { name: 'ElevenLabs', icon: 'https://img.icons8.com/ios-filled/512/elevenlabs.png' },
];

export default function Hero() {
  return (
    <section className="hero">
      <h1 data-i18n="hero.title">L'IA mondiale, payee en Dinars</h1>

      <p className="hero-access" data-i18n="hero.access">Accedez a</p>

      <div className="providers-marquee">
        <div className="marquee-track">
          {/* First set */}
          {AI_PROVIDERS.map((provider) => (
            <div key={provider.name} className="provider-item">
              <img src={provider.icon} alt={provider.name} />
              <span>{provider.name}</span>
            </div>
          ))}
          {/* Duplicate for infinite loop */}
          {AI_PROVIDERS.map((provider) => (
            <div key={`${provider.name}-dup`} className="provider-item">
              <img src={provider.icon} alt={provider.name} />
              <span>{provider.name}</span>
            </div>
          ))}
        </div>
      </div>

      <p className="hero-price" data-i18n="hero.price">
        en un seul endroit pour <strong>2 500 DZD/mois</strong>
      </p>

      <Link to="/login?next=/bolt" className="btn-primary hero-cta" data-i18n="hero.cta">
        Commencer
      </Link>

      <p className="hero-credits">
        💳 Fonctionne avec un système de crédits mensuels — chaque modèle consomme des crédits selon sa puissance.{' '}
        <Link to="/pricing">Voir le détail des crédits</Link>
      </p>
    </section>
  );
}
