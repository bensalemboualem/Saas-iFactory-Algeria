import { useTheme } from '../../hooks';
import './Models.css';

interface Model {
  name: string;
  icon?: string;
  emoji?: string;
  free?: boolean;
}

interface ModelCategory {
  id: string;
  title: string;
  models: Model[];
}

const MODEL_CATEGORIES: ModelCategory[] = [
  {
    id: 'text',
    title: 'MODÈLES TEXTE',
    models: [
      { name: 'ChatGPT 5.2', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/openai.png' },
      { name: 'Claude 4.5', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/claude-color.png' },
      { name: 'Gemini 3', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/gemini-color.png' },
      { name: 'Grok 3', icon: 'https://cdn.worldvectorlogo.com/logos/grok-1.svg' },
      { name: 'DeepSeek R1', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/deepseek-color.png' },
      { name: 'Mistral Large', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/mistral-color.png' },
      { name: 'Qwen 3', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/qwen-color.png' },
      { name: 'Copilot', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/latest/files/light/copilot.png' },
      { name: 'Perplexity', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/perplexity-color.png' },
      { name: 'Kimi', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/kimi-color.png' },
    ],
  },
  {
    id: 'image',
    title: 'MODÈLES IMAGE',
    models: [
      { name: 'Midjourney', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/midjourney.png' },
      { name: 'DALL-E 3', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/openai.png' },
      { name: 'FLUX Pro', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/flux.png' },
      { name: 'Stable Diffusion', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/stability-color.png' },
      { name: 'Ideogram 3', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/ideogram.png' },
      { name: 'Recraft V3', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/recraft.png' },
      { name: 'Leonardo', icon: 'https://images.seeklogo.com/logo-png/62/1/leonardo-ai-logo-png_seeklogo-621169.png' },
      { name: 'Imagen 3', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/google-color.png' },
      { name: 'Adobe Firefly', icon: 'https://www.adobe.com/content/dam/shared/images/product-icons/svg/firefly.svg' },
      { name: 'Playground v2', icon: 'https://playground.com/favicon.ico' },
    ],
  },
  {
    id: 'video',
    title: 'MODÈLES VIDÉO',
    models: [
      { name: 'Sora 2', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/latest/files/light/sora.png' },
      { name: 'Veo 2', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/google-color.png' },
      { name: 'Runway Gen-4', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/runway.png' },
      { name: 'Pika 2.0', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/pika.png' },
      { name: 'Kling 1.6', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/latest/files/light/kling.png' },
      { name: 'Hailuo', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/latest/files/light/hailuo.png' },
      { name: 'LTX-2', icon: 'https://www.aixploria.com/wp-content/uploads/favicons/ltx-studio.png' },
      { name: 'Seedance 1.0', icon: 'https://www.seedance.ai/favicon.ico' },
      { name: 'Luma Ray', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/latest/files/light/luma.png' },
      { name: 'PixVerse v4.5', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/latest/files/light/pixverse.png' },
    ],
  },
  {
    id: 'audio',
    title: 'MODÈLES AUDIO',
    models: [
      { name: 'ElevenLabs', icon: 'https://img.icons8.com/ios-filled/512/elevenlabs.png' },
      { name: 'Suno', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/suno.png' },
      { name: 'Udio', icon: 'https://www.udio.com/favicon.ico' },
      { name: 'Whisper', icon: 'https://img.icons8.com/ios-filled/512/microphone.png' },
      { name: 'Play.ht', icon: 'https://www.aixploria.com/wp-content/uploads/favicons/play-ht.png' },
      { name: 'Resemble AI', icon: 'https://www.resemble.ai/favicon.ico' },
    ],
  },
  {
    id: 'local',
    title: 'MODÈLES LOCAUX',
    models: [
      { name: 'Ollama', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/ollama.png', free: true },
      { name: 'LM Studio', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/lmstudio.png', free: true },
      { name: 'Groq', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/groq.png', free: true },
      { name: 'Together AI', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/together-color.png', free: true },
      { name: 'Llama 4', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/meta-color.png', free: true },
      { name: 'Hugging Face', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/latest/files/light/huggingface.png', free: true },
    ],
  },
  {
    id: 'code',
    title: 'MODÈLES CODE',
    models: [
      { name: 'GitHub Copilot', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/github.png' },
      { name: 'Cursor', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/cursor.png' },
      { name: 'Codestral', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/mistral-color.png' },
      { name: 'Claude Code', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/claude-color.png' },
      { name: 'VS Code', icon: 'https://code.visualstudio.com/favicon.ico', free: true },
      { name: 'Gemini CLI', icon: 'https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/light/gemini-color.png' },
    ],
  },
];

export default function Models() {
  const { colors, isDark } = useTheme();

  return (
    <section className="models-section" id="models">
      <div className="container">
        <div className="section-title">
          <h2>+30 Modèles IA disponibles</h2>
          <p style={{ color: colors.textMuted }}>
            Accédez aux meilleurs modèles d'IA au monde avec votre abonnement
          </p>
        </div>

        <div className="models-grid-full">
          {MODEL_CATEGORIES.map((category) => (
            <div
              key={category.id}
              className="model-category"
              style={{
                background: isDark ? colors.bgSecondary : '#ffffff',
                border: `1px solid ${colors.borderColor}`,
              }}
            >
              <div className="category-title" style={{ color: colors.textPrimary }}>
                {category.title}
              </div>
              <div className="models-list">
                {category.models.map((model) => (
                  <div
                    key={model.name}
                    className="model-card"
                    style={{
                      background: isDark ? colors.bgPrimary : '#f8f8f8',
                      border: `1px solid ${colors.borderColor}`,
                    }}
                  >
                    <div className="model-icon">
                      {model.icon ? (
                        <img src={model.icon} alt={model.name} />
                      ) : (
                        <span className="model-emoji">{model.emoji}</span>
                      )}
                    </div>
                    <div className="model-info">
                      <span className="model-name" style={{ color: colors.textPrimary }}>
                        {model.name}
                      </span>
                      <span className={`model-badge ${model.free ? 'free' : ''}`}>
                        {model.free ? 'Gratuit' : 'Consomme des crédits'}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Arrow and Summary Card */}
        <div className="models-summary-wrapper">
          <div className="models-arrow">
            <svg width="100" height="60" viewBox="0 0 100 60" fill="none">
              <path d="M10 0 L10 40 L50 40 L50 0" stroke={colors.borderColor} strokeWidth="2" fill="none" />
              <path d="M90 0 L90 40 L50 40 L50 55" stroke={colors.borderColor} strokeWidth="2" fill="none" />
              <path d="M42 48 L50 58 L58 48" stroke="#00A86B" strokeWidth="2" fill="none" />
            </svg>
          </div>
          <div
            className="models-summary-card"
            style={{
              background: isDark ? colors.bgSecondary : '#f5f5f0',
              border: `2px solid #00A86B`,
            }}
          >
            <div className="summary-icon">
              <span style={{ background: '#00A86B', color: '#fff', padding: '8px 12px', borderRadius: '8px', fontWeight: 700 }}>IA</span>
            </div>
            <div className="summary-content">
              <h3 style={{ color: colors.textPrimary, margin: 0, fontSize: '20px', fontWeight: 700 }}>IA FACTORY ALGERIA</h3>
              <p style={{ color: colors.textPrimary, margin: '4px 0', fontSize: '16px' }}>
                Tout inclus : <strong>2 500 DZD/mois</strong>
              </p>
              <p style={{ color: colors.textMuted, margin: 0, fontSize: '14px' }}>
                +30 modèles • Texte • Image • Vidéo • Audio • Code
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
