import { Link } from 'react-router-dom';
import { useState, useRef, useEffect, useCallback, CSSProperties } from 'react';
import { useTheme } from '../hooks';
import {
  PenLine,
  Palette,
  Code2,
  GraduationCap,
  CreditCard,
  Globe,
  ShieldCheck,
  Scale,
  Zap,
  Brain,
  BarChart3,
  Sun,
  Moon,
  Send,
  Check,
  ImagePlus,
  Lock,
  FileText,
  Sparkles,
  Gift,
  User,
} from 'lucide-react';


// ============================================================================
// I18N - FR / EN / AR
// ============================================================================
type Lang = 'fr' | 'en' | 'ar';

const I18N: Record<Lang, Record<string, string>> = {
  fr: {
    heroTitle: "La plateforme IA tout-en-un pour l'Algérie",
    heroSub: "Texte, Image, Vidéo, Audio, Code, Agents. Paiement en DZD. Système de crédits. Accès instantané.",
    ctaTry: "Essayer gratuitement",
    ctaPricing: "Voir les tarifs",
    heroBadge: "+5,000 utilisateurs en Algérie",
    stat1Value: "25+", stat1Label: "Outils IA",
    stat2Value: "30+", stat2Label: "Modèles",
    stat3Value: "5", stat3Label: "Langues",
    stat4Value: "100%", stat4Label: "Local",
    trust1: "Sans carte bancaire",
    trust2: "50 crédits offerts",
    trust3: "BaridiMob & CCP",
    proof1: "+30 modèles IA",
    proof2: "Paiement local",
    proof3: "Support Algérie",
    proof4: "Hébergement sécurisé",
    howTitle: "Comment ça marche",
    howSub: "Vous utilisez. L'IA travaille. Résultats en toute transparence.",
    step1Title: "Inscrivez-vous",
    step1Desc: "Créez votre compte et recevez vos crédits instantanément",
    step2Title: "Choisissez",
    step2Desc: "Sélectionnez un modèle IA — texte, image, code, audio",
    step3Title: "Créez",
    step3Desc: "L'IA travaille. Vous obtenez des résultats. Crédits déduits.",
    step4Title: "Suivez & optimisez",
    step4Desc: "Historique, consommation de crédits et export des résultats en un clic",
    useCasesTitle: "Que voulez-vous faire ?",
    uc1: "Rédiger", uc1d: "Articles, emails, rapports, résumés",
    uc2: "Créer", uc2d: "Images, logos, designs, vidéos",
    uc3: "Coder", uc3d: "Apps, scripts, automatisation, debug",
    uc4: "Apprendre", uc4d: "Langues, matières, compétences",
    algeriaTitle: "Fait pour l'Algérie",
    alg1: "Paiement local", alg1d: "CCP, BaridiMob, cartes locales. Pas de carte internationale requise.",
    alg2: "Support multilingue", alg2d: "Français, Arabe, Darija, Anglais et Tamazight.",
    alg3: "Données sécurisées", alg3d: "Hébergement conforme RGPD. Vos données restent privées.",
    alg4: "Cybersécurité", alg4d: "Protection avancée, chiffrement et conformité légale algérienne.",
    testimonialsTitle: "Ce que disent nos utilisateurs",
    demoTitle: "Voyez l'IA en action",
    demo1: "Discutez avec l'IA",
    demo2: "Générez des images",
    demo3: "Codez avec l'IA",
    demoPrompt1: "Écris un poème sur Alger",
    demoPrompt2: "Un chat sur la plage au coucher du soleil",
    demoPrompt3: "Fonction pour trier une liste",
    demo4: "RAG légal & conformité",
    demo4d: "Vos documents, vos règles. IA connectée à votre base juridique.",
    creditsTitle: "1 abonnement = crédits mensuels",
    creditsSub: "Chaque modèle consomme des crédits selon sa puissance.",
    creditsBtn: "Voir les tarifs et crédits",
    faqTitle: "Questions fréquentes",
    faq1q: "Comment je paie ?",
    faq1a: "CCP, BaridiMob et cartes bancaires locales. Paiements en DZD.",
    faq2q: "C'est illimité ?",
    faq2a: "Vous recevez des crédits mensuels. Chaque modèle consomme selon sa puissance.",
    faq3q: "Mes données sont privées ?",
    faq3a: "Oui. Nous ne stockons ni partageons vos conversations. Conforme RGPD.",
    faq4q: "Quelles langues ?",
    faq4a: "Arabe, français, anglais et +50 langues supportées.",
    faq5q: "Puis-je annuler ?",
    faq5a: "Oui. Sans engagement. Annulez en un clic.",
    finalCta: "Prêt à accéder à l'IA mondiale ?",
    finalCtaSub: "Rejoignez des milliers d'utilisateurs en Algérie.",
    finalBtn: "S'inscrire gratuitement",
    footer: "2025 IAFactory. Tous droits réservés.",
    generate: "Générer",
    output: "Résultat",
    // DashboardMockup i18n
    ragTitle: "RAG Légal",
    ragConnected: "Connecté",
    ragLegalBase: "Base juridique",
    ragActive: "Active",
    ragCompliance: "RGPD - Contrats - DZ",
    ragRealtime: "RAG temps réel",
    ragAnalysis: "Analyse automatique",
    chatPoem: "Voici un poème pour vous:",
    chatPoemLine: "Alger, perle blanche au bord de la mer...",
  },
  en: {
    heroTitle: "The all-in-one AI platform for Algeria",
    heroSub: "Text, Image, Video, Audio, Code, Agents. Pay in DZD. Credit system. Instant access.",
    ctaTry: "Try for free",
    ctaPricing: "See pricing",
    heroBadge: "+5,000 users in Algeria",
    stat1Value: "25+", stat1Label: "AI Tools",
    stat2Value: "30+", stat2Label: "Models",
    stat3Value: "5", stat3Label: "Languages",
    stat4Value: "100%", stat4Label: "Local",
    trust1: "No credit card required",
    trust2: "50 free credits",
    trust3: "BaridiMob & CCP",
    proof1: "+30 AI models",
    proof2: "Local payment",
    proof3: "Algeria support",
    proof4: "Secure hosting",
    howTitle: "How it works",
    howSub: "You use it. AI works. Results with full transparency.",
    step1Title: "Sign up",
    step1Desc: "Create your account and get credits instantly",
    step2Title: "Choose",
    step2Desc: "Select an AI model — text, image, code, audio",
    step3Title: "Create",
    step3Desc: "AI works. You get results. Credits deducted.",
    step4Title: "Track & optimize",
    step4Desc: "History, credit usage and one-click export of your results",
    useCasesTitle: "What do you want to do?",
    uc1: "Write", uc1d: "Articles, emails, reports, summaries",
    uc2: "Create", uc2d: "Images, logos, designs, videos",
    uc3: "Code", uc3d: "Apps, scripts, automation, debug",
    uc4: "Learn", uc4d: "Languages, subjects, skills",
    algeriaTitle: "Built for Algeria",
    alg1: "Local payment", alg1d: "CCP, BaridiMob, local cards. No international card required.",
    alg2: "Multilingual", alg2d: "French, Arabic, Darija, English and Tamazight.",
    alg3: "Secure data", alg3d: "GDPR compliant hosting. Your data stays private.",
    alg4: "Cybersecurity", alg4d: "Advanced protection, encryption and Algerian legal compliance.",
    testimonialsTitle: "What our users say",
    demoTitle: "See AI in action",
    demo1: "Chat with AI",
    demo2: "Generate images",
    demo3: "Code with AI",
    demoPrompt1: "Write a poem about Algiers",
    demoPrompt2: "A cat on the beach at sunset",
    demoPrompt3: "Function to sort a list",
    demo4: "Legal RAG & compliance",
    demo4d: "Your documents, your rules. AI connected to your legal base.",
    creditsTitle: "1 subscription = monthly credits",
    creditsSub: "Each model consumes credits based on its power.",
    creditsBtn: "See pricing and credits",
    faqTitle: "Frequently asked questions",
    faq1q: "How do I pay?",
    faq1a: "CCP, BaridiMob and local bank cards. Payments in DZD.",
    faq2q: "Is it unlimited?",
    faq2a: "You get monthly credits. Each model consumes based on its power.",
    faq3q: "Is my data private?",
    faq3a: "Yes. We never store or share your conversations. GDPR compliant.",
    faq4q: "What languages?",
    faq4a: "Arabic, French, English and 50+ supported languages.",
    faq5q: "Can I cancel?",
    faq5a: "Yes. No commitment. Cancel in one click.",
    finalCta: "Ready to access global AI?",
    finalCtaSub: "Join thousands of users in Algeria.",
    finalBtn: "Sign up for free",
    footer: "2025 IAFactory. All rights reserved.",
    generate: "Generate",
    output: "Output",
    // DashboardMockup i18n
    ragTitle: "Legal RAG",
    ragConnected: "Connected",
    ragLegalBase: "Legal base",
    ragActive: "Active",
    ragCompliance: "GDPR - Contracts - DZ",
    ragRealtime: "Real-time RAG",
    ragAnalysis: "Auto analysis",
    chatPoem: "Here is a poem for you:",
    chatPoemLine: "Algiers, white pearl by the sea...",
  },
  ar: {
    heroTitle: "منصة الذكاء الاصطناعي الشاملة للجزائر",
    heroSub: "نص، صورة، فيديو، صوت، كود. الدفع بالدينار. نظام الرصيد. وصول فوري.",
    ctaTry: "جرب مجاناً",
    ctaPricing: "عرض الأسعار",
    heroBadge: "+5,000 مستخدم في الجزائر",
    stat1Value: "25+", stat1Label: "أدوات ذكاء",
    stat2Value: "30+", stat2Label: "نموذج",
    stat3Value: "5", stat3Label: "لغات",
    stat4Value: "100%", stat4Label: "محلي",
    trust1: "بدون بطاقة بنكية",
    trust2: "50 رصيد مجاني",
    trust3: "بريدي موب و CCP",
    proof1: "+30 نموذج ذكاء",
    proof2: "دفع محلي",
    proof3: "دعم الجزائر",
    proof4: "استضافة آمنة",
    howTitle: "كيف يعمل",
    howSub: "أنت تستخدم. الذكاء الاصطناعي يعمل. نتائج بشفافية.",
    step1Title: "سجّل",
    step1Desc: "أنشئ حسابك واحصل على رصيدك فوراً",
    step2Title: "اختر",
    step2Desc: "اختر نموذج ذكاء اصطناعي — نص، صورة، كود، صوت",
    step3Title: "أنشئ",
    step3Desc: "الذكاء الاصطناعي يعمل. تحصل على النتائج. يُخصم الرصيد.",
    step4Title: "تابع وحسّن",
    step4Desc: "سجل الاستخدام، استهلاك الرصيد وتصدير النتائج بنقرة واحدة",
    useCasesTitle: "ماذا تريد أن تفعل؟",
    uc1: "اكتب", uc1d: "مقالات، إيميلات، تقارير",
    uc2: "أنشئ", uc2d: "صور، شعارات، تصاميم",
    uc3: "برمج", uc3d: "تطبيقات، سكربتات، أتمتة",
    uc4: "تعلم", uc4d: "لغات، مواد، مهارات",
    algeriaTitle: "مصمم للجزائر",
    alg1: "دفع محلي", alg1d: "CCP، بريدي موب، بطاقات محلية. بدون بطاقة دولية.",
    alg2: "متعدد اللغات", alg2d: "فرنسية، عربية، دارجة، إنجليزية وأمازيغية.",
    alg3: "بيانات آمنة", alg3d: "استضافة متوافقة مع RGPD. بياناتك تبقى خاصة.",
    alg4: "الأمن السيبراني", alg4d: "حماية متقدمة وتشفير وامتثال قانوني جزائري.",
    testimonialsTitle: "ماذا يقول مستخدمونا",
    demoTitle: "شاهد الذكاء الاصطناعي",
    demo1: "تحدث مع الذكاء",
    demo2: "أنشئ صور",
    demo3: "برمج مع الذكاء",
    demoPrompt1: "اكتب قصيدة عن الجزائر",
    demoPrompt2: "قطة على الشاطئ عند الغروب",
    demoPrompt3: "دالة لترتيب قائمة",
    demo4: "RAG قانوني والامتثال",
    demo4d: "مستنداتك وقواعدك. ذكاء اصطناعي مرتبط ببياناتك القانونية.",
    creditsTitle: "اشتراك واحد = رصيد شهري",
    creditsSub: "كل نموذج يستهلك رصيد حسب قوته.",
    creditsBtn: "عرض الأسعار والرصيد",
    faqTitle: "أسئلة شائعة",
    faq1q: "كيف أدفع؟",
    faq1a: "CCP، بريدي موب وبطاقات بنكية محلية. الدفع بالدينار.",
    faq2q: "هل هو غير محدود؟",
    faq2a: "تحصل على رصيد شهري. كل نموذج يستهلك حسب قوته.",
    faq3q: "هل بياناتي خاصة؟",
    faq3a: "نعم. لا نخزن أو نشارك محادثاتك. متوافق مع RGPD.",
    faq4q: "أي لغات؟",
    faq4a: "عربي، فرنسي، إنجليزي و+50 لغة مدعومة.",
    faq5q: "هل يمكنني الإلغاء؟",
    faq5a: "نعم. بدون التزام. ألغِ بنقرة واحدة.",
    finalCta: "مستعد للوصول للذكاء العالمي؟",
    finalCtaSub: "انضم لآلاف المستخدمين في الجزائر.",
    finalBtn: "سجّل مجاناً",
    footer: "2025 IAFactory. جميع الحقوق محفوظة.",
    generate: "توليد",
    output: "النتيجة",
    // DashboardMockup i18n
    ragTitle: "RAG قانوني",
    ragConnected: "متصل",
    ragLegalBase: "قاعدة قانونية",
    ragActive: "نشط",
    ragCompliance: "RGPD - عقود - DZ",
    ragRealtime: "RAG فوري",
    ragAnalysis: "تحليل تلقائي",
    chatPoem: "إليك قصيدة:",
    chatPoemLine: "الجزائر، لؤلؤة بيضاء على البحر...",
  },
};

// ============================================================================
// LUCIDE ICON WRAPPER (Premium style with gradient + glow)
// ============================================================================
type LucideIcon = React.ComponentType<{ size?: number; className?: string; strokeWidth?: number }>;

const PremiumIconBadge = ({ icon: Icon, glow }: { icon: LucideIcon; glow: string }) => (
  <div
    className="premium-badge"
    style={{
      '--badge-glow': glow,
    } as React.CSSProperties}
  >
    <Icon size={28} strokeWidth={1.8} />
  </div>
);

// ============================================================================
// CSS VARIABLES + GLOBAL STYLES
// ============================================================================
const CSS_VARS = `
:root, [data-theme="dark"]{
  --bg: #0A0F1A;
  --bg2: #111827;
  --text: #F8FAFC;
  --muted: rgba(248,250,252,0.65);
  --card: rgba(255,255,255,0.06);
  --card2: rgba(255,255,255,0.04);
  --card-surface: rgba(255,255,255,0.08);
  --border: rgba(255,255,255,0.10);
  --shadow: 0 18px 60px rgba(0,0,0,0.55);
  --accent: #22C55E;
  --accent2: #D21034;
  --primary: #006233;
  --accent-glow: rgba(0,98,51,0.20);
  --gradient-hero: radial-gradient(900px 520px at 50% -10%, rgba(0,98,51,0.15), transparent 60%);
  --gradient-hero2: radial-gradient(900px 520px at 90% 115%, rgba(210,16,52,0.08), transparent 55%);
}

[data-theme="light"]{
  --bg: #F6F3EE;
  --bg2: #FBF8F3;
  --text: #141414;
  --muted: rgba(20,20,20,0.62);
  --card: #EDE9E3;
  --card2: rgba(237,233,227,0.85);
  --card-surface: #EDE9E3;
  --border: rgba(20,20,20,0.10);
  --shadow: 0 18px 60px rgba(20,20,20,0.10);
  --accent: #1C7A5F;
  --accent2: #6D5DFC;
  --primary: #1C7A5F;
  --accent-glow: rgba(28,122,95,0.10);
  --gradient-hero: radial-gradient(ellipse 80% 55% at 50% -10%, rgba(28,122,95,0.06) 0%, transparent 62%);
  --gradient-hero2: radial-gradient(ellipse 65% 45% at 85% 100%, rgba(109,93,252,0.04) 0%, transparent 55%);
}

section[id] {
  scroll-margin-top: 90px;
}

/* Premium Icon Badge - Transparent */
.premium-badge {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--accent);
  margin: 0 auto 18px;
  position: relative;
  border: none;
  box-shadow: none;
}
.premium-badge::before {
  display: none;
}
[data-theme="light"] .premium-badge {
  color: var(--accent);
  background: transparent;
  box-shadow: none;
}

.ai-card{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 18px;
  box-shadow: var(--shadow);
  backdrop-filter: blur(12px);
  position: relative;
  overflow: hidden;
  transition: transform 240ms cubic-bezier(0.4,0,0.2,1),
              box-shadow 240ms cubic-bezier(0.4,0,0.2,1),
              border-color 240ms cubic-bezier(0.4,0,0.2,1);
}
.ai-card::before{
  content:"";
  position:absolute;
  inset:-1px;
  background: linear-gradient(135deg, rgba(255,255,255,0.14), transparent 58%);
  opacity:0;
  transition: opacity 240ms ease;
  pointer-events:none;
}
.ai-card:hover{
  border-color: rgba(87,214,170,0.28);
  box-shadow: var(--shadow), 0 0 28px var(--accent-glow);
  transform: translateY(-6px) scale(1.01);
}
.ai-card:hover::before{ opacity:1; }

.ai-card-clickable {
  cursor: pointer;
}

@media (prefers-reduced-motion: reduce){
  .ai-card, .ai-card:hover{ transform:none !important; }
}

.section-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--border), transparent);
  margin: 0 auto;
  max-width: 800px;
}
@keyframes typing-cursor {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}
@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
@keyframes pulse-badge {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.02); }
}
@keyframes pulse-dot {
  0%, 100% { opacity: 1; box-shadow: 0 0 8px #22C55E; }
  50% { opacity: 0.6; box-shadow: 0 0 16px #22C55E; }
}
.typing-cursor {
  display: inline-block;
  width: 2px;
  height: 14px;
  background: var(--accent);
  margin-left: 2px;
  animation: typing-cursor 1s ease-in-out infinite;
}
.shimmer-loading {
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
  background-size: 200% 100%;
  animation: shimmer 2s ease-in-out infinite;
}

.card-grid-4 {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 20px;
  max-width: 1100px;
  margin: 0 auto;
}
@media (max-width: 1100px) {
  .card-grid-4 {
    grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
    max-width: 600px;
  }
}
@media (max-width: 640px) {
  .card-grid-4 {
    grid-template-columns: 1fr !important;
    max-width: 320px;
  }
}

.demo-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 20px;
  max-width: 1100px;
  margin: 0 auto;
}
.demo-grid > div {
  min-height: 380px;
  width: 100%;
}
.demo-grid > div > div {
  height: 100% !important;
  min-height: 380px !important;
  width: 100% !important;
}
@media (max-width: 1100px) {
  .demo-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
    max-width: 600px;
  }
}
@media (max-width: 640px) {
  .demo-grid {
    grid-template-columns: 1fr !important;
    max-width: 320px;
  }
}

/* Initials Avatar */
.initials-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent), #2a9d8f);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
  color: #fff;
  border: 2px solid rgba(255,255,255,0.2);
}
`;

// ============================================================================
// AI PROVIDERS - Using jsDelivr CDN with correct filenames
// ============================================================================
const ICON_CDN = 'https://cdn.jsdelivr.net/npm/@lobehub/icons-static-png@1.78.0/light';

const AI_TEXT_PROVIDERS = [
  { name: 'ChatGPT', icon: `${ICON_CDN}/openai.png` },
  { name: 'Claude', icon: `${ICON_CDN}/claude-color.png` },
  { name: 'Gemini', icon: `${ICON_CDN}/gemini-color.png` },
  { name: 'Mistral', icon: `${ICON_CDN}/mistral-color.png` },
  { name: 'DeepSeek', icon: `${ICON_CDN}/deepseek-color.png` },
  { name: 'Grok', icon: `${ICON_CDN}/grok.png` },
  { name: 'Perplexity', icon: `${ICON_CDN}/perplexity-color.png` },
  { name: 'Qwen', icon: `${ICON_CDN}/qwen-color.png` },
  { name: 'Kimi', icon: `${ICON_CDN}/kimi-color.png` },
  { name: 'Ollama', icon: `${ICON_CDN}/ollama.png` },
];

const AI_MEDIA_PROVIDERS = [
  { name: 'Sora', icon: `${ICON_CDN}/openai.png` },
  { name: 'FLUX', icon: `${ICON_CDN}/flux.png` },
  { name: 'Veo', icon: `${ICON_CDN}/google-color.png` },
  { name: 'ElevenLabs', icon: `${ICON_CDN}/elevenlabs.png` },
  { name: 'Runway', icon: `${ICON_CDN}/runway.png` },
  { name: 'Midjourney', icon: `${ICON_CDN}/midjourney.png` },
];

// ============================================================================
// COMPONENTS
// ============================================================================
function useReveal() {
  const [revealed, setRevealed] = useState<Set<string>>(new Set());
  const observer = useRef<IntersectionObserver | null>(null);

  useEffect(() => {
    observer.current = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          const id = e.target.getAttribute('data-id');
          if (id) { setRevealed((p) => new Set(p).add(id)); observer.current?.unobserve(e.target); }
        }
      });
    }, { threshold: 0.1 });
    return () => observer.current?.disconnect();
  }, []);

  const observe = useCallback((el: HTMLElement | null, id: string) => {
    if (el && observer.current) { el.setAttribute('data-id', id); observer.current.observe(el); }
  }, []);

  const style = useCallback((id: string, delay = 0): CSSProperties => ({
    opacity: revealed.has(id) ? 1 : 0,
    transform: revealed.has(id) ? 'translateY(0)' : 'translateY(20px)',
    transition: `opacity 500ms ease ${delay}ms, transform 500ms ease ${delay}ms`,
  }), [revealed]);

  return { observe, style };
}

// Helper to get initials from name
function getInitials(name: string): string {
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
}

interface DashboardMockupProps {
  type: 'chat' | 'image' | 'code' | 'rag';
  label: string;
  prompt?: string;
  generateLabel?: string;
  t: Record<string, string>;
}

function DashboardMockup({ type, label, prompt, generateLabel, t }: DashboardMockupProps) {
  const accentColor = { chat: 'var(--accent2)', image: '#00d4ff', code: 'var(--accent)', rag: '#ff9f43' }[type];
  const accentHex = { chat: '#6d5dfc', image: '#00d4ff', code: '#38BDA0', rag: '#ff9f43' }[type];

  return (
    <div style={{
      background: 'var(--card)',
      borderRadius: 16,
      overflow: 'hidden',
      border: '1px solid var(--border)',
      boxShadow: `0 8px 32px rgba(0,0,0,0.3), 0 0 0 1px ${accentHex}15`,
      transition: 'all 280ms ease',
      height: 380,
      minHeight: 380,
      display: 'flex',
      flexDirection: 'column',
    }}>
      {/* Window chrome */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 6, padding: '12px 16px', borderBottom: '1px solid var(--border)', background: 'rgba(0,0,0,0.35)' }}>
        <div style={{ width: 12, height: 12, borderRadius: '50%', background: '#ff5f57' }} />
        <div style={{ width: 12, height: 12, borderRadius: '50%', background: '#febc2e' }} />
        <div style={{ width: 12, height: 12, borderRadius: '50%', background: '#28c840' }} />
        <div style={{ flex: 1, textAlign: 'center', fontSize: 12, fontWeight: 600 }}>
          <span style={{ color: 'var(--accent)' }}>iA</span>
          <span style={{ color: 'var(--text)', opacity: 0.9 }}>Factory</span>
          <span style={{ color: 'var(--accent)', marginLeft: 4 }}>Algeria</span>
        </div>
      </div>

      {/* Prompt input bar - only for chat/image/code */}
      {type !== 'rag' && prompt && (
        <div style={{ padding: '14px 16px', borderBottom: '1px solid var(--border)', background: 'rgba(0,0,0,0.2)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, background: 'var(--card-surface)', borderRadius: 12, padding: '12px 16px', border: '1px solid var(--border)' }}>
            <div style={{ flex: 1, fontSize: 13, color: 'var(--text)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
              {prompt}
            </div>
            <div style={{ background: accentColor, color: '#fff', fontSize: 11, fontWeight: 600, padding: '8px 14px', borderRadius: 8, display: 'flex', alignItems: 'center', gap: 6, flexShrink: 0, boxShadow: `0 4px 12px ${accentHex}40` }}>
              <Send size={14} />
              {generateLabel}
            </div>
          </div>
        </div>
      )}
      {/* RAG header bar */}
      {type === 'rag' && (
        <div style={{ padding: '14px 16px', borderBottom: '1px solid var(--border)', background: 'rgba(255,159,67,0.1)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, background: 'var(--card-surface)', borderRadius: 12, padding: '12px 16px', border: '1px solid var(--border)' }}>
            <div style={{ width: 28, height: 28, borderRadius: 6, background: 'linear-gradient(135deg, #ff9f43, #ee7752)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
              <FileText size={14} color="#fff" />
            </div>
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: 12, fontWeight: 600, color: 'var(--text)' }}>{t.ragTitle}</div>
            </div>
            <div style={{ background: '#ff9f43', color: '#fff', fontSize: 11, fontWeight: 600, padding: '8px 14px', borderRadius: 8, flexShrink: 0 }}>
              {t.ragConnected}
            </div>
          </div>
        </div>
      )}

      {/* Content area */}
      <div style={{ padding: 16, flex: 1, background: 'var(--bg2)', display: 'flex', flexDirection: 'column', justifyContent: 'center', minHeight: 180, overflow: 'hidden' }}>
        {type === 'chat' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
            {/* User message */}
            <div style={{ display: 'flex', gap: 10, justifyContent: 'flex-end' }}>
              <div style={{ background: `linear-gradient(135deg, ${accentHex}30, ${accentHex}15)`, borderRadius: '14px 14px 4px 14px', padding: '12px 16px', maxWidth: '80%', border: `1px solid ${accentHex}40` }}>
                <div style={{ fontSize: 12, color: 'var(--text)', lineHeight: 1.5 }}>{prompt}</div>
              </div>
              <div style={{ width: 32, height: 32, borderRadius: '50%', background: `linear-gradient(135deg, ${accentHex}, ${accentHex}80)`, flexShrink: 0, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <User size={16} color="#fff" />
              </div>
            </div>
            {/* AI response */}
            <div style={{ display: 'flex', gap: 10 }}>
              <div style={{ width: 32, height: 32, borderRadius: '50%', background: 'linear-gradient(135deg, var(--accent), #2a9d8f)', flexShrink: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 2px 8px var(--accent-glow)' }}>
                <Sparkles size={16} color="#fff" />
              </div>
              <div style={{ background: 'var(--card)', borderRadius: '14px 14px 14px 4px', padding: '12px 16px', flex: 1, border: '1px solid var(--border)' }}>
                <div style={{ fontSize: 12, color: 'var(--text)', lineHeight: 1.6, opacity: 0.9 }}>
                  <div style={{ marginBottom: 6 }}>{t.chatPoem}</div>
                  <div style={{ fontStyle: 'italic', color: 'var(--muted)' }}>
                    {t.chatPoemLine}<span className="typing-cursor" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {type === 'image' && (
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
            {/* Main large preview */}
            <div className="shimmer-loading" style={{ gridRow: 'span 2', background: `linear-gradient(145deg, ${accentHex}40, ${accentHex}15)`, borderRadius: 12, border: `1px solid ${accentHex}30`, display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: 130, position: 'relative', overflow: 'hidden' }}>
              <div style={{ position: 'absolute', bottom: 0, left: 0, right: 0, height: '40%', background: `linear-gradient(to top, ${accentHex}50, transparent)` }} />
              <div style={{ width: 50, height: 50, borderRadius: 12, background: `linear-gradient(135deg, ${accentHex}80, ${accentHex}40)`, display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: `0 8px 24px ${accentHex}30` }}>
                <ImagePlus size={24} color="#fff" />
              </div>
              <div style={{ position: 'absolute', bottom: 8, right: 8, background: 'rgba(0,0,0,0.6)', padding: '4px 8px', borderRadius: 6, fontSize: 10, color: '#fff' }}>1024x1024</div>
            </div>
            {/* Smaller tiles - variations */}
            <div className="shimmer-loading" style={{ background: `linear-gradient(145deg, ${accentHex}25, ${accentHex}10)`, borderRadius: 10, border: `1px solid ${accentHex}20`, minHeight: 55, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Sun size={18} color={accentHex} />
            </div>
            <div className="shimmer-loading" style={{ background: `linear-gradient(145deg, ${accentHex}20, ${accentHex}08)`, borderRadius: 10, border: `1px solid ${accentHex}15`, minHeight: 55, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Palette size={18} color={accentHex} />
            </div>
          </div>
        )}

        {type === 'code' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
            {/* Code editor */}
            <div style={{ background: '#1e1e2e', borderRadius: 10, padding: 14, border: '1px solid var(--border)', fontFamily: 'Monaco, Consolas, monospace' }}>
              <div style={{ fontSize: 11, lineHeight: 1.8 }}>
                <div><span style={{ color: '#c678dd' }}>def</span> <span style={{ color: '#61afef' }}>sort_list</span><span style={{ color: '#abb2bf' }}>(arr):</span></div>
                <div style={{ paddingLeft: 16 }}><span style={{ color: '#7f848e' }}># Quick sort implementation</span></div>
                <div style={{ paddingLeft: 16 }}><span style={{ color: '#c678dd' }}>if</span> <span style={{ color: '#61afef' }}>len</span><span style={{ color: '#abb2bf' }}>(arr) &lt;= 1:</span></div>
                <div style={{ paddingLeft: 32 }}><span style={{ color: '#c678dd' }}>return</span> <span style={{ color: '#abb2bf' }}>arr</span></div>
                <div style={{ paddingLeft: 16 }}><span style={{ color: '#c678dd' }}>return</span> <span style={{ color: '#61afef' }}>sorted</span><span style={{ color: '#abb2bf' }}>(arr)</span></div>
              </div>
            </div>
            {/* Output panel */}
            <div style={{ background: 'var(--card)', borderRadius: 10, padding: 12, border: '1px solid var(--border)' }}>
              <div style={{ fontSize: 10, color: 'var(--accent)', marginBottom: 8, fontWeight: 600, textTransform: 'uppercase', letterSpacing: 1 }}>{t.output}</div>
              <div style={{ fontFamily: 'Monaco, Consolas, monospace', fontSize: 11, color: '#98c379', background: 'rgba(0,0,0,0.2)', padding: 8, borderRadius: 6 }}>
                [1, 2, 3, 4, 5]<span className="typing-cursor" />
              </div>
            </div>
          </div>
        )}

        {type === 'rag' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10, height: '100%', justifyContent: 'space-between' }}>
            <div style={{ fontSize: 11, color: 'var(--muted)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span>{t.ragLegalBase}</span>
              <span style={{ color: 'var(--accent)', fontSize: 10, display: 'flex', alignItems: 'center', gap: 4 }}>
                <span style={{ width: 6, height: 6, borderRadius: '50%', background: 'var(--accent)' }} />
                {t.ragActive}
              </span>
            </div>
            <div style={{ padding: 14, borderRadius: 8, background: 'rgba(255,159,67,0.12)', fontSize: 12, lineHeight: 1.8, border: '1px solid rgba(255,159,67,0.25)' }}>
              <div style={{ marginBottom: 10, display: 'flex', alignItems: 'center', gap: 8 }}><Lock size={14} color="#ff9f43" /> {t.ragCompliance}</div>
              <div style={{ marginBottom: 10, display: 'flex', alignItems: 'center', gap: 8 }}><Zap size={14} color="#ff9f43" /> {t.ragRealtime}</div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}><BarChart3 size={14} color="#ff9f43" /> {t.ragAnalysis}</div>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 6 }}>
              {['PDF', 'DOC', 'SQL', 'API'].map((m, i) => (
                <div key={i} style={{ padding: '8px 4px', borderRadius: 6, background: 'linear-gradient(135deg, rgba(255,159,67,0.18), transparent)', fontSize: 10, textAlign: 'center', border: '1px solid var(--border)', fontWeight: 500 }}>
                  {m}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Label footer */}
      <div style={{ padding: '12px 16px', textAlign: 'center', color: 'var(--text)', fontSize: 13, fontWeight: 500, borderTop: '1px solid var(--border)', background: `linear-gradient(to right, transparent, ${accentHex}10, transparent)` }}>{label}</div>
    </div>
  );
}

// ============================================================================
// SCROLL HELPER
// ============================================================================
const scrollToId = (id: string) => {
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
};

// ============================================================================
// MAIN COMPONENT
// ============================================================================
export default function Home() {
  const [lang, setLang] = useState<Lang>(() => {
    const saved = localStorage.getItem('lang') as Lang;
    return saved && ['fr', 'en', 'ar'].includes(saved) ? saved : 'fr';
  });
  const { theme, setTheme, isDark } = useTheme();
  const [openFaq, setOpenFaq] = useState<number | null>(null);
  const { observe, style: revealStyle } = useReveal();

  // Sync language with localStorage and Header
  useEffect(() => {
    const syncLang = () => {
      const stored = localStorage.getItem('lang') as Lang;
      if (stored && stored !== lang && ['fr', 'en', 'ar'].includes(stored)) {
        setLang(stored);
      }
    };
    window.addEventListener('storage', syncLang);
    window.addEventListener('languageChanged', syncLang);
    const interval = setInterval(syncLang, 500);
    return () => {
      window.removeEventListener('storage', syncLang);
      window.removeEventListener('languageChanged', syncLang);
      clearInterval(interval);
    };
  }, [lang]);

  // Set document direction for RTL languages
  useEffect(() => {
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
  }, [lang]);

  // Auth detection (safe heuristic for landing page only)
  const isAuthed = Boolean(
    localStorage.getItem('auth_token') ||
    localStorage.getItem('token') ||
    localStorage.getItem('access_token') ||
    localStorage.getItem('isLoggedIn')
  );
  const appOrLogin = isAuthed ? '/app' : '/login';

  const t = I18N[lang];
  const isRTL = lang === 'ar';

  const STEPS = [
    { icon: Brain, title: t.step1Title, desc: t.step1Desc, glow: 'rgba(138,125,255,0.4)' },
    { icon: Zap, title: t.step2Title, desc: t.step2Desc, glow: 'rgba(0,212,255,0.4)' },
    { icon: ImagePlus, title: t.step3Title, desc: t.step3Desc, glow: 'rgba(87,214,170,0.4)' },
    { icon: BarChart3, title: t.step4Title, desc: t.step4Desc, glow: 'rgba(255,159,67,0.4)' },
  ];

  const USE_CASES = [
    { icon: PenLine, title: t.uc1, desc: t.uc1d, glow: 'rgba(138,125,255,0.4)' },
    { icon: Palette, title: t.uc2, desc: t.uc2d, glow: 'rgba(0,212,255,0.4)' },
    { icon: Code2, title: t.uc3, desc: t.uc3d, glow: 'rgba(87,214,170,0.4)' },
    { icon: GraduationCap, title: t.uc4, desc: t.uc4d, glow: 'rgba(255,159,67,0.4)' },
  ];

  const ALGERIA_DIFF = [
    { icon: CreditCard, title: t.alg1, desc: t.alg1d, glow: 'rgba(87,214,170,0.4)', scrollTarget: 'credits' },
    { icon: Globe, title: t.alg2, desc: t.alg2d, glow: 'rgba(138,125,255,0.4)', scrollTarget: 'faq' },
    { icon: ShieldCheck, title: t.alg3, desc: t.alg3d, glow: 'rgba(0,212,255,0.4)', scrollTarget: 'faq' },
    { icon: Scale, title: t.alg4, desc: t.alg4d, glow: 'rgba(255,159,67,0.4)', scrollTarget: 'faq' },
  ];

  const FAQ = [
    { q: t.faq1q, a: t.faq1a },
    { q: t.faq2q, a: t.faq2a },
    { q: t.faq3q, a: t.faq3a },
    { q: t.faq4q, a: t.faq4a },
    { q: t.faq5q, a: t.faq5a },
  ];

  const DEMOS = [
    { type: 'chat' as const, label: t.demo1, prompt: t.demoPrompt1 },
    { type: 'image' as const, label: t.demo2, prompt: t.demoPrompt2 },
    { type: 'code' as const, label: t.demo3, prompt: t.demoPrompt3 },
    { type: 'rag' as const, label: t.demo4 },
  ];

  const TESTIMONIALS = [
    {
      name: "Karim B.",
      role: lang === 'ar' ? "رائد أعمال، الجزائر" : lang === 'en' ? "Entrepreneur, Algiers" : "Entrepreneur, Alger",
      text: lang === 'ar'
        ? "IAFactory مكنني من إنشاء محتوى لشبكاتي الاجتماعية في دقائق. الدفع بالدينار هو تغيير جذري!"
        : lang === 'en'
        ? "IAFactory allowed me to create content for my social networks in minutes. Payment in DZD is a game changer!"
        : "IAFactory m'a permis de créer du contenu pour mes réseaux sociaux en quelques minutes. Le paiement en DZD, c'est un game changer!",
      rating: 5
    },
    {
      name: "Amina K.",
      role: lang === 'ar' ? "مصممة جرافيك، وهران" : lang === 'en' ? "Graphic Designer, Oran" : "Graphiste, Oran",
      text: lang === 'ar'
        ? "أدوات توليد الصور مذهلة. أوفر ساعات من العمل كل أسبوع."
        : lang === 'en'
        ? "The image generation tools are amazing. I save hours of work every week."
        : "Les outils de génération d'images sont incroyables. Je gagne des heures de travail chaque semaine.",
      rating: 5
    },
    {
      name: "Youcef M.",
      role: lang === 'ar' ? "طالب، قسنطينة" : lang === 'en' ? "Student, Constantine" : "Étudiant, Constantine",
      text: lang === 'ar'
        ? "50 رصيد مجاني لاختبار المنصة. بالنسبة للطلاب، هذا مثالي."
        : lang === 'en'
        ? "50 free credits to test the platform. For students, it's perfect."
        : "50 crédits gratuits pour tester la plateforme. Pour les étudiants, c'est parfait.",
      rating: 5
    },
    {
      name: "Fatima Z.",
      role: lang === 'ar' ? "محامية، العاصمة" : lang === 'en' ? "Lawyer, Capital" : "Avocate, Alger",
      text: lang === 'ar'
        ? "أداة RAG القانونية وفرت لي ساعات من البحث. دقيقة وسريعة."
        : lang === 'en'
        ? "The legal RAG tool saved me hours of research. Accurate and fast."
        : "L'outil RAG juridique m'a fait gagner des heures de recherche. Précis et rapide.",
      rating: 5
    }
  ];

  const containerStyle: CSSProperties = { maxWidth: 1200, margin: '0 auto', padding: '0 32px' };
  const sectionPadding: CSSProperties = { padding: '88px 0' };
  const cardInnerStyle: CSSProperties = { padding: 24, textAlign: 'center', minHeight: 190, display: 'flex', flexDirection: 'column', justifyContent: 'center' };

  return (
    <>
      <style>{CSS_VARS}</style>
      <div data-theme={theme} dir={isRTL ? 'rtl' : 'ltr'} style={{ background: 'var(--bg)', minHeight: '100vh', color: 'var(--text)', fontFamily: 'system-ui, -apple-system, sans-serif' }}>
        {/* Background effects */}
        <div style={{ position: 'fixed', inset: 0, zIndex: 0, pointerEvents: 'none', background: 'var(--gradient-hero)' }} />
        <div style={{ position: 'fixed', inset: 0, zIndex: 0, pointerEvents: 'none', background: 'var(--gradient-hero2)' }} />
        <div style={{
          position: 'fixed',
          inset: 0,
          zIndex: 0,
          pointerEvents: 'none',
          backgroundImage: isDark
            ? 'radial-gradient(circle at 1px 1px, rgba(255,255,255,0.08) 0.7px, transparent 0)'
            : 'radial-gradient(circle at 1px 1px, rgba(20,20,20,0.03) 1px, transparent 0)',
          backgroundSize: isDark ? '44px 44px' : '38px 38px',
          opacity: isDark ? 0.35 : 0.6
        }} />

        {/* Top bar - transparent with floating glass capsule */}
        <header style={{ position: 'fixed', top: 0, left: 0, right: 0, zIndex: 100, background: 'transparent', borderBottom: 'none' }}>
          <div style={{ ...containerStyle, height: 70, display: 'flex', alignItems: 'center', justifyContent: 'center', paddingTop: 10 }}>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              padding: '10px 18px',
              borderRadius: 16,
              background: isDark ? 'rgba(255,255,255,0.06)' : 'var(--card)',
              border: '1px solid var(--border)',
              backdropFilter: 'blur(14px)',
              boxShadow: isDark ? '0 10px 30px rgba(0,0,0,0.18)' : 'var(--shadow)',
              minWidth: 320,
              maxWidth: 500
            }}>
              <div style={{ lineHeight: 1.1 }}>
                <div style={{ fontWeight: 800, fontSize: 20, letterSpacing: '0.08em', color: 'var(--accent)' }}>iAF</div>
                <div style={{ fontSize: 11, letterSpacing: '0.12em', color: 'var(--muted)', textTransform: 'uppercase' }}>IAFactory Algeria</div>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                <select
                  value={lang}
                  onChange={(e) => {
                    const newLang = e.target.value as Lang;
                    setLang(newLang);
                    localStorage.setItem('lang', newLang);
                    document.documentElement.lang = newLang;
                    document.documentElement.dir = newLang === 'ar' ? 'rtl' : 'ltr';
                    window.dispatchEvent(new CustomEvent('languageChanged'));
                  }}
                  style={{ background: 'transparent', color: 'var(--text)', border: '1px solid var(--border)', borderRadius: 8, padding: '5px 8px', fontSize: 12, cursor: 'pointer' }}
                >
                  <option value="fr">FR</option>
                  <option value="en">EN</option>
                  <option value="ar">AR</option>
                </select>
                <button
                  onClick={() => setTheme(isDark ? 'light' : 'dark')}
                  style={{ background: 'transparent', color: 'var(--text)', border: '1px solid var(--border)', borderRadius: 8, padding: 6, cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center' }}
                  aria-label="Toggle theme"
                >
                  {isDark ? <Sun size={20} /> : <Moon size={20} />}
                </button>
              </div>
            </div>
          </div>
        </header>

        <main style={{ position: 'relative', zIndex: 1, paddingTop: 100 }}>
          {/* HERO */}
          <section style={{ textAlign: 'center', padding: '50px 20px 60px' }}>
            <div style={containerStyle}>
              {/* Badge utilisateurs */}
              <div style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: 8,
                background: 'linear-gradient(135deg, rgba(0,98,51,0.15), rgba(0,98,51,0.08))',
                border: '1px solid rgba(0,98,51,0.3)',
                borderRadius: 50,
                padding: '8px 18px',
                marginBottom: 24,
                animation: 'pulse-badge 2s ease-in-out infinite'
              }}>
                <span style={{
                  width: 8,
                  height: 8,
                  borderRadius: '50%',
                  background: '#22C55E',
                  boxShadow: '0 0 8px #22C55E',
                  animation: 'pulse-dot 2s ease-in-out infinite'
                }} />
                <span style={{ fontSize: 13, fontWeight: 600, color: 'var(--accent)' }}>{t.heroBadge}</span>
              </div>

              <h1 style={{ fontSize: 'clamp(1.8rem, 5vw, 3rem)', fontWeight: 700, marginBottom: 16, lineHeight: 1.15, maxWidth: 800, margin: '0 auto 16px' }}>
                {t.heroTitle}
              </h1>
              <p style={{ fontSize: 'clamp(1rem, 2.5vw, 1.2rem)', color: 'var(--muted)', marginBottom: 24, lineHeight: 1.6, maxWidth: 600, margin: '0 auto 24px' }}>
                {t.heroSub}
              </p>

              {/* Stats rapides */}
              <div style={{
                display: 'flex',
                gap: 24,
                justifyContent: 'center',
                flexWrap: 'wrap',
                marginBottom: 24,
                padding: '16px 0'
              }}>
                {[
                  { value: t.stat1Value, label: t.stat1Label },
                  { value: t.stat2Value, label: t.stat2Label },
                  { value: t.stat3Value, label: t.stat3Label },
                  { value: t.stat4Value, label: t.stat4Label },
                ].map((stat, i) => (
                  <div key={i} style={{ textAlign: 'center', minWidth: 70 }}>
                    <div style={{ fontSize: 24, fontWeight: 700, color: 'var(--accent)', lineHeight: 1 }}>{stat.value}</div>
                    <div style={{ fontSize: 12, color: 'var(--muted)', marginTop: 4 }}>{stat.label}</div>
                  </div>
                ))}
              </div>

              <div style={{ display: 'flex', gap: 14, justifyContent: 'center', flexWrap: 'wrap', marginBottom: 20 }}>
                <Link to={appOrLogin} style={{ background: 'linear-gradient(135deg, var(--accent), #2a9d8f)', color: '#fff', padding: '14px 32px', borderRadius: 12, textDecoration: 'none', fontWeight: 600, fontSize: '1rem', boxShadow: '0 8px 24px var(--accent-glow)' }}>
                  {t.ctaTry}
                </Link>
                <button
                  onClick={() => scrollToId('credits')}
                  style={{ background: 'var(--card)', color: 'var(--accent)', padding: '14px 32px', borderRadius: 12, fontWeight: 600, fontSize: '1rem', border: '1px solid var(--border)', cursor: 'pointer' }}
                >
                  {t.ctaPricing}
                </button>
              </div>

              {/* Trust badges */}
              <div style={{
                display: 'flex',
                gap: 16,
                justifyContent: 'center',
                flexWrap: 'wrap',
                marginBottom: 32
              }}>
                {[
                  { icon: Check, text: t.trust1, color: '#22C55E' },
                  { icon: Gift, text: t.trust2, color: '#F59E0B' },
                  { icon: CreditCard, text: t.trust3, color: '#3B82F6' },
                ].map((badge, i) => (
                  <div key={i} style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: 6,
                    fontSize: 13,
                    color: 'var(--muted)',
                    background: 'var(--card)',
                    padding: '8px 14px',
                    borderRadius: 8,
                    border: '1px solid var(--border)'
                  }}>
                    <badge.icon size={16} color={badge.color} />
                    <span>{badge.text}</span>
                  </div>
                ))}
              </div>
              {/* Text/Chat AI Models */}
              <div style={{ display: 'flex', gap: 8, justifyContent: 'center', flexWrap: 'wrap', marginBottom: 12 }}>
                {AI_TEXT_PROVIDERS.map((p) => (
                  <div key={p.name} style={{ display: 'flex', alignItems: 'center', gap: 6, background: 'var(--card)', padding: '6px 12px', borderRadius: 20, border: '1px solid var(--border)' }}>
                    <div style={{ width: 20, height: 20, borderRadius: 4, background: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 2 }}>
                      <img src={p.icon} alt={p.name} style={{ width: 16, height: 16 }} />
                    </div>
                    <span style={{ fontSize: 12, color: 'var(--muted)' }}>{p.name}</span>
                  </div>
                ))}
              </div>
              {/* Media AI Models */}
              <div style={{ display: 'flex', gap: 8, justifyContent: 'center', flexWrap: 'wrap' }}>
                {AI_MEDIA_PROVIDERS.map((p) => (
                  <div key={p.name} style={{ display: 'flex', alignItems: 'center', gap: 6, background: 'var(--card)', padding: '6px 12px', borderRadius: 20, border: '1px solid var(--border)' }}>
                    <div style={{ width: 20, height: 20, borderRadius: 4, background: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 2 }}>
                      <img src={p.icon} alt={p.name} style={{ width: 16, height: 16 }} />
                    </div>
                    <span style={{ fontSize: 12, color: 'var(--muted)' }}>{p.name}</span>
                  </div>
                ))}
              </div>
            </div>
          </section>

          {/* QUICK PROOF */}
          <section id="proof" style={{ padding: '16px 20px' }}>
            <div className="section-divider" style={{ marginBottom: 16 }} />
            <div style={{ display: 'flex', gap: 24, justifyContent: 'center', flexWrap: 'wrap' }}>
              {[t.proof1, t.proof2, t.proof3, t.proof4].map((item, i) => (
                <span key={i} style={{ fontSize: 13, color: 'var(--muted)', display: 'flex', alignItems: 'center', gap: 6 }}>
                  <Check size={16} style={{ color: 'var(--accent)' }} /> {item}
                </span>
              ))}
            </div>
            <div className="section-divider" style={{ marginTop: 16 }} />
          </section>

          {/* HOW IT WORKS */}
          <section id="how" style={sectionPadding}>
            <div style={containerStyle}>
              <h2 style={{ textAlign: 'center', fontSize: 'clamp(1.5rem, 4vw, 2rem)', marginBottom: 12, fontWeight: 700, color: 'var(--text)' }}>{t.howTitle}</h2>
              <p style={{ textAlign: 'center', color: 'var(--muted)', marginBottom: 48, fontSize: 15 }}>{t.howSub}</p>
              <div className="card-grid-4">
                {STEPS.map((step, i) => (
                  <button
                    key={i}
                    onClick={() => scrollToId('credits')}
                    style={{ background: 'none', border: 'none', padding: 0, textAlign: 'inherit', cursor: 'pointer', width: '100%' }}
                    aria-label={`${step.title} - ${step.desc}`}
                  >
                    <div ref={(el) => observe(el, `step-${i}`)} style={revealStyle(`step-${i}`, i * 100)} className="ai-card ai-card-clickable">
                      <div style={cardInnerStyle}>
                        <PremiumIconBadge icon={step.icon} glow={step.glow} />
                        <div style={{ display: 'inline-block', background: 'var(--accent)', color: '#fff', fontSize: 10, fontWeight: 700, padding: '4px 12px', borderRadius: 20, marginBottom: 12 }}>
                          {i + 1}
                        </div>
                        <h3 style={{ fontSize: 18, fontWeight: 600, marginBottom: 8, color: 'var(--text)' }}>{step.title}</h3>
                        <p style={{ color: 'var(--muted)', fontSize: 14, margin: 0, lineHeight: 1.5 }}>{step.desc}</p>
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </section>

          <div className="section-divider" />

          {/* USE CASES */}
          <section id="usecases" style={sectionPadding}>
            <div style={containerStyle}>
              <h2 style={{ textAlign: 'center', fontSize: 'clamp(1.5rem, 4vw, 2rem)', marginBottom: 48, fontWeight: 700, color: 'var(--text)' }}>{t.useCasesTitle}</h2>
              <div className="card-grid-4">
                {USE_CASES.map((uc, i) => (
                  <Link key={uc.title} to={appOrLogin} style={{ textDecoration: 'none', color: 'inherit' }} aria-label={uc.title}>
                    <div ref={(el) => observe(el, `uc-${i}`)} style={revealStyle(`uc-${i}`, i * 80)} className="ai-card ai-card-clickable">
                      <div style={cardInnerStyle}>
                        <PremiumIconBadge icon={uc.icon} glow={uc.glow} />
                        <h3 style={{ fontSize: 17, fontWeight: 600, marginBottom: 8, color: 'var(--text)' }}>{uc.title}</h3>
                        <p style={{ fontSize: 13, color: 'var(--muted)', margin: 0 }}>{uc.desc}</p>
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          </section>

          <div className="section-divider" />

          {/* ALGERIA - 4 CARDS */}
          <section id="algeria" style={sectionPadding}>
            <div style={containerStyle}>
              <h2 style={{ textAlign: 'center', fontSize: 'clamp(1.5rem, 4vw, 2rem)', marginBottom: 48, fontWeight: 700, color: 'var(--text)' }}>{t.algeriaTitle}</h2>
              <div className="card-grid-4">
                {ALGERIA_DIFF.map((item, i) => (
                  <button
                    key={item.title}
                    onClick={() => scrollToId(item.scrollTarget)}
                    style={{ background: 'none', border: 'none', padding: 0, textAlign: 'inherit', cursor: 'pointer', width: '100%' }}
                    aria-label={`${item.title} - ${item.desc}`}
                  >
                    <div ref={(el) => observe(el, `alg-${i}`)} style={revealStyle(`alg-${i}`, i * 100)} className="ai-card ai-card-clickable">
                      <div style={{ padding: 24, textAlign: 'center', minHeight: 190, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
                        <PremiumIconBadge icon={item.icon} glow={item.glow} />
                        <h3 style={{ fontSize: 17, fontWeight: 600, marginBottom: 8, color: 'var(--text)' }}>{item.title}</h3>
                        <p style={{ fontSize: 13, color: 'var(--muted)', margin: 0, lineHeight: 1.5 }}>{item.desc}</p>
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </section>

          <div className="section-divider" />

          {/* TESTIMONIALS */}
          <section style={sectionPadding}>
            <div style={containerStyle}>
              <h2 style={{ textAlign: 'center', fontSize: 'clamp(1.5rem, 4vw, 2rem)', marginBottom: 48, fontWeight: 700, color: 'var(--text)' }}>{t.testimonialsTitle}</h2>
              <div className="card-grid-4">
                {TESTIMONIALS.map((testimonial, i) => (
                  <div key={i} ref={(el) => observe(el, `test-${i}`)} style={revealStyle(`test-${i}`, i * 100)} className="ai-card">
                    <div style={{ padding: 24, minHeight: 200, display: 'flex', flexDirection: 'column' }}>
                      {/* Rating stars */}
                      <div style={{ display: 'flex', gap: 2, marginBottom: 12 }}>
                        {[...Array(testimonial.rating)].map((_, j) => (
                          <Sparkles key={j} size={14} color="#F59E0B" />
                        ))}
                      </div>
                      {/* Quote */}
                      <p style={{ fontSize: 14, color: 'var(--text)', lineHeight: 1.6, flex: 1, margin: 0, fontStyle: 'italic' }}>
                        &ldquo;{testimonial.text}&rdquo;
                      </p>
                      {/* Author */}
                      <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginTop: 16, paddingTop: 16, borderTop: '1px solid var(--border)' }}>
                        <div className="initials-avatar">
                          {getInitials(testimonial.name)}
                        </div>
                        <div>
                          <div style={{ fontSize: 14, fontWeight: 600, color: 'var(--text)' }}>{testimonial.name}</div>
                          <div style={{ fontSize: 12, color: 'var(--muted)' }}>{testimonial.role}</div>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </section>

          <div className="section-divider" />

          {/* DEMO */}
          <section id="demo" style={sectionPadding}>
            <div style={containerStyle}>
              <h2 style={{ textAlign: 'center', fontSize: 'clamp(1.5rem, 4vw, 2rem)', marginBottom: 48, fontWeight: 700, color: 'var(--text)' }}>{t.demoTitle}</h2>
              <div className="demo-grid">
                {DEMOS.map((d, i) => (
                  <Link key={d.type} to={appOrLogin} style={{ textDecoration: 'none', color: 'inherit' }} aria-label={d.label}>
                    <div ref={(el) => observe(el, `demo-${i}`)} style={{ ...revealStyle(`demo-${i}`, i * 100), cursor: 'pointer' }}>
                      <DashboardMockup type={d.type} label={d.label} prompt={d.prompt} generateLabel={t.generate} t={t} />
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          </section>

          <div className="section-divider" />

          {/* CREDITS */}
          <section id="credits" style={{ padding: '56px 20px' }}>
            <div style={{ ...containerStyle, maxWidth: 760 }}>
              <div className="ai-card" style={{ padding: '40px 32px', textAlign: 'center', background: 'linear-gradient(145deg, var(--card), var(--card2))' }}>
                <h2 style={{ fontSize: 'clamp(1.3rem, 3vw, 1.6rem)', marginBottom: 14, fontWeight: 600, color: 'var(--text)' }}>{t.creditsTitle}</h2>
                <p style={{ fontSize: 15, marginBottom: 24, color: 'var(--muted)' }}>{t.creditsSub}</p>
                <Link to="/pricing" style={{ background: 'linear-gradient(135deg, var(--accent), #2a9d8f)', color: '#fff', padding: '12px 28px', borderRadius: 12, textDecoration: 'none', fontWeight: 600, display: 'inline-block', boxShadow: '0 8px 24px var(--accent-glow)' }}>
                  {t.creditsBtn}
                </Link>
              </div>
            </div>
          </section>

          <div className="section-divider" />

          {/* FAQ */}
          <section id="faq" style={sectionPadding}>
            <div style={{ ...containerStyle, maxWidth: 700 }}>
              <h2 style={{ textAlign: 'center', fontSize: 'clamp(1.5rem, 4vw, 2rem)', marginBottom: 48, fontWeight: 700, color: 'var(--text)' }}>{t.faqTitle}</h2>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                {FAQ.map((faq, i) => (
                  <div key={i} ref={(el) => observe(el, `faq-${i}`)} style={revealStyle(`faq-${i}`, i * 50)} className="ai-card">
                    <button onClick={() => setOpenFaq(openFaq === i ? null : i)} style={{ width: '100%', padding: '18px 20px', background: 'transparent', border: 'none', textAlign: isRTL ? 'right' : 'left', fontSize: 15, fontWeight: 500, cursor: 'pointer', display: 'flex', justifyContent: 'space-between', alignItems: 'center', color: 'var(--text)' }}>
                      {faq.q}
                      <span style={{ transform: openFaq === i ? 'rotate(180deg)' : 'none', transition: 'transform 200ms', color: 'var(--accent)', marginLeft: isRTL ? 0 : 12, marginRight: isRTL ? 12 : 0, display: 'flex' }}>
                        <Code2 size={16} style={{ transform: 'rotate(90deg)' }} />
                      </span>
                    </button>
                    <div style={{ maxHeight: openFaq === i ? 200 : 0, overflow: 'hidden', transition: 'max-height 250ms ease' }}>
                      <div style={{ padding: '0 20px 18px', fontSize: 14, color: 'var(--muted)', lineHeight: 1.7, textAlign: isRTL ? 'right' : 'left' }}>{faq.a}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </section>

          {/* FINAL CTA */}
          <section id="cta" style={{ padding: '80px 20px', textAlign: 'center' }}>
            <h2 style={{ fontSize: 'clamp(1.5rem, 4vw, 2rem)', marginBottom: 16, fontWeight: 700, color: 'var(--text)' }}>{t.finalCta}</h2>
            <p style={{ color: 'var(--muted)', marginBottom: 28, fontSize: 16 }}>{t.finalCtaSub}</p>
            <div style={{ display: 'flex', gap: 14, justifyContent: 'center', flexWrap: 'wrap' }}>
              <Link to={appOrLogin} style={{ background: 'linear-gradient(135deg, var(--accent), #2a9d8f)', color: '#fff', padding: '14px 32px', borderRadius: 12, textDecoration: 'none', fontWeight: 600, fontSize: '1rem', boxShadow: '0 8px 24px var(--accent-glow)' }}>
                {t.finalBtn}
              </Link>
              <button
                onClick={() => scrollToId('credits')}
                style={{ background: 'var(--card)', color: 'var(--accent)', padding: '14px 32px', borderRadius: 12, fontWeight: 600, fontSize: '1rem', border: '1px solid var(--border)', cursor: 'pointer' }}
              >
                {t.ctaPricing}
              </button>
            </div>
          </section>
        </main>
      </div>
    </>
  );
}
