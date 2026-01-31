import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

type Theme = 'dark' | 'light';
type Lang = 'fr' | 'en' | 'ar';

// ============================================================================
// I18N - FR / EN / AR
// ============================================================================
const I18N: Record<Lang, Record<string, string>> = {
  fr: {
    title: 'Tarifs simples & transparents',
    subtitle: "Tous les plans fonctionnent avec un système de crédits mensuels utilisables sur l'ensemble des modèles IA.",
    popular: 'Plus populaire',
    perMonth: 'DZD/mois',
    creditsMonth: 'crédits/mois',
    // Starter
    starter_name: 'Starter',
    starter_f1: '100 crédits/mois',
    starter_f2: 'Accès aux modèles essentiels',
    starter_f3: 'Génération texte & image basique',
    starter_f4: 'Support communautaire',
    starter_cta: 'Commencer gratuitement',
    // Pro
    pro_name: 'Pro',
    pro_f1: '1 000 crédits/mois',
    pro_f2: 'Accès à tous les modèles IA',
    pro_f3: 'Texte, Image, Audio, Code & Vidéo',
    pro_f4: 'Support prioritaire',
    pro_f5: 'Accès API',
    pro_f6: 'Gestion des crédits en temps réel',
    pro_cta: 'Choisir Pro',
    // Business
    business_name: 'Business',
    business_f1: '5 000 crédits/mois',
    business_f2: 'Accès aux modèles premium',
    business_f3: 'Agents IA personnalisés',
    business_f4: 'Accès API étendu',
    business_f5: 'Support dédié (SLA)',
    business_f6: 'Facturation entreprise',
    business_cta: 'Contacter ventes',
    // Credit examples
    creditTitle: 'Exemples de consommation de crédits',
    creditSubtitle: 'Estimations indicatives pour chaque type de génération',
    creditNote: 'Les valeurs peuvent évoluer selon la charge et la version des modèles.',
    text: 'Texte',
    textUsage: '~1 crédit / réponse courte',
    image: 'Image',
    imageUsage: '~10-20 crédits / image',
    video: 'Vidéo',
    videoUsage: '~100-300 crédits / génération',
    audio: 'Audio',
    audioUsage: '~5-15 crédits / action',
    code: 'Code',
    codeUsage: '~1-5 crédits / requête',
    // Payment
    paymentTitle: 'Moyens de paiement acceptés',
    disclaimer: "Les modèles et services tiers sont accessibles via notre plateforme d'orchestration IA. L'accès dépend de la disponibilité et des quotas des fournisseurs.",
  },
  en: {
    title: 'Simple & transparent pricing',
    subtitle: 'All plans work with a monthly credit system usable across all AI models.',
    popular: 'Most popular',
    perMonth: 'DZD/month',
    creditsMonth: 'credits/month',
    // Starter
    starter_name: 'Starter',
    starter_f1: '100 credits/month',
    starter_f2: 'Access to essential models',
    starter_f3: 'Basic text & image generation',
    starter_f4: 'Community support',
    starter_cta: 'Start for free',
    // Pro
    pro_name: 'Pro',
    pro_f1: '1,000 credits/month',
    pro_f2: 'Access to all AI models',
    pro_f3: 'Text, Image, Audio, Code & Video',
    pro_f4: 'Priority support',
    pro_f5: 'API access',
    pro_f6: 'Real-time credit management',
    pro_cta: 'Choose Pro',
    // Business
    business_name: 'Business',
    business_f1: '5,000 credits/month',
    business_f2: 'Access to premium models',
    business_f3: 'Custom AI agents',
    business_f4: 'Extended API access',
    business_f5: 'Dedicated support (SLA)',
    business_f6: 'Enterprise billing',
    business_cta: 'Contact sales',
    // Credit examples
    creditTitle: 'Credit consumption examples',
    creditSubtitle: 'Indicative estimates for each generation type',
    creditNote: 'Values may change depending on load and model versions.',
    text: 'Text',
    textUsage: '~1 credit / short response',
    image: 'Image',
    imageUsage: '~10-20 credits / image',
    video: 'Video',
    videoUsage: '~100-300 credits / generation',
    audio: 'Audio',
    audioUsage: '~5-15 credits / action',
    code: 'Code',
    codeUsage: '~1-5 credits / request',
    // Payment
    paymentTitle: 'Accepted payment methods',
    disclaimer: 'Third-party models and services are accessible via our AI orchestration platform. Access depends on provider availability and quotas.',
  },
  ar: {
    title: 'أسعار بسيطة وشفافة',
    subtitle: 'جميع الخطط تعمل بنظام رصيد شهري يمكن استخدامه على جميع نماذج الذكاء الاصطناعي.',
    popular: 'الأكثر شعبية',
    perMonth: 'دج/شهر',
    creditsMonth: 'رصيد/شهر',
    // Starter
    starter_name: 'المبتدئ',
    starter_f1: '100 رصيد/شهر',
    starter_f2: 'الوصول للنماذج الأساسية',
    starter_f3: 'توليد نص وصورة أساسي',
    starter_f4: 'دعم المجتمع',
    starter_cta: 'ابدأ مجاناً',
    // Pro
    pro_name: 'احترافي',
    pro_f1: '1,000 رصيد/شهر',
    pro_f2: 'الوصول لجميع نماذج الذكاء الاصطناعي',
    pro_f3: 'نص، صورة، صوت، كود وفيديو',
    pro_f4: 'دعم ذو أولوية',
    pro_f5: 'الوصول لـ API',
    pro_f6: 'إدارة الرصيد في الوقت الفعلي',
    pro_cta: 'اختر Pro',
    // Business
    business_name: 'الأعمال',
    business_f1: '5,000 رصيد/شهر',
    business_f2: 'الوصول للنماذج المتميزة',
    business_f3: 'وكلاء ذكاء اصطناعي مخصصون',
    business_f4: 'وصول API موسع',
    business_f5: 'دعم مخصص (SLA)',
    business_f6: 'فواتير المؤسسات',
    business_cta: 'اتصل بالمبيعات',
    // Credit examples
    creditTitle: 'أمثلة استهلاك الرصيد',
    creditSubtitle: 'تقديرات إرشادية لكل نوع من التوليد',
    creditNote: 'قد تتغير القيم حسب الحمل وإصدارات النماذج.',
    text: 'نص',
    textUsage: '~1 رصيد / رد قصير',
    image: 'صورة',
    imageUsage: '~10-20 رصيد / صورة',
    video: 'فيديو',
    videoUsage: '~100-300 رصيد / توليد',
    audio: 'صوت',
    audioUsage: '~5-15 رصيد / إجراء',
    code: 'كود',
    codeUsage: '~1-5 رصيد / طلب',
    // Payment
    paymentTitle: 'طرق الدفع المقبولة',
    disclaimer: 'نماذج وخدمات الطرف الثالث متاحة عبر منصة تنسيق الذكاء الاصطناعي. الوصول يعتمد على توفر المزود والحصص.',
  },
};

// Payment methods by language
const PAYMENT_METHODS: Record<Lang, string[]> = {
  fr: ['Chargily', 'CIB', 'BaridiMob', 'Dahabia'],
  en: ['Chargily', 'CIB', 'BaridiMob', 'Dahabia'],
  ar: ['شارجيلي', 'CIB', 'بريدي موب', 'الذهبية'],
};

// Helper to get language from localStorage
const getLang = (): Lang => {
  const saved = localStorage.getItem('lang');
  if (saved === 'fr' || saved === 'en' || saved === 'ar') return saved;
  return 'fr';
};

export default function Pricing() {
  const [theme, setTheme] = useState<Theme>('dark');
  const [lang, setLang] = useState<Lang>(getLang);

  useEffect(() => {
    const savedTheme = (localStorage.getItem('theme') as Theme) || 'dark';
    setTheme(savedTheme);

    // Sync language from lang in localStorage
    const syncLang = () => {
      const l = getLang();
      if (l !== lang) setLang(l);
    };
    window.addEventListener('storage', syncLang);
    window.addEventListener('languageChanged', syncLang);
    const interval = setInterval(syncLang, 500); // Poll for changes

    const observer = new MutationObserver(() => {
      const currentTheme = document.documentElement.dataset.theme as Theme;
      if (currentTheme) setTheme(currentTheme);
    });

    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['data-theme'],
    });

    return () => {
      observer.disconnect();
      window.removeEventListener('storage', syncLang);
      window.removeEventListener('languageChanged', syncLang);
      clearInterval(interval);
    };
  }, [lang]);

  // Set RTL direction
  useEffect(() => {
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
  }, [lang]);

  const t = I18N[lang];
  const isRTL = lang === 'ar';
  const isDark = theme === 'dark';
  // Couleurs synchronisées avec Home.tsx
  const bgColor = isDark ? '#0A0F1A' : '#F6F3EE';
  const cardBg = isDark ? 'rgba(255,255,255,0.06)' : '#EDE9E3';
  const textColor = isDark ? '#F8FAFC' : '#141414';
  const textMuted = isDark ? 'rgba(248,250,252,0.65)' : 'rgba(20,20,20,0.62)';
  const borderColor = isDark ? 'rgba(255,255,255,0.10)' : 'rgba(20,20,20,0.10)';
  const sectionBg = isDark ? '#0A0F1A' : '#F6F3EE';
  const accentColor = isDark ? '#22C55E' : '#1C7A5F';
  const accentGradient = `linear-gradient(135deg, ${isDark ? '#22C55E' : '#1C7A5F'}, ${isDark ? '#57D6AA' : '#22C55E'})`;

  // Build plans with translations
  const PLANS = [
    {
      id: 'dz_starter',
      name: t.starter_name,
      price: 0,
      credits: 100,
      features: [t.starter_f1, t.starter_f2, t.starter_f3, t.starter_f4],
      cta: t.starter_cta,
      ctaLink: '/login',
      popular: false,
    },
    {
      id: 'dz_pro',
      name: t.pro_name,
      price: 1990,
      credits: 1000,
      features: [t.pro_f1, t.pro_f2, t.pro_f3, t.pro_f4, t.pro_f5, t.pro_f6],
      cta: t.pro_cta,
      ctaLink: '/login?plan=pro',
      popular: true,
    },
    {
      id: 'dz_business',
      name: t.business_name,
      price: 5990,
      credits: 5000,
      features: [t.business_f1, t.business_f2, t.business_f3, t.business_f4, t.business_f5, t.business_f6],
      cta: t.business_cta,
      ctaLink: '/contact',
      popular: false,
    },
  ];

  const CREDIT_EXAMPLES = [
    { category: t.text, usage: t.textUsage, icon: '💬' },
    { category: t.image, usage: t.imageUsage, icon: '🖼️' },
    { category: t.video, usage: t.videoUsage, icon: '🎬' },
    { category: t.audio, usage: t.audioUsage, icon: '🎵' },
    { category: t.code, usage: t.codeUsage, icon: '💻' },
  ];

  return (
    <div
      dir={isRTL ? 'rtl' : 'ltr'}
      style={{
        paddingTop: '120px',
        paddingBottom: '80px',
        minHeight: '100vh',
        background: bgColor,
      }}
    >
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 24px' }}>
        {/* Header */}
        <div style={{ textAlign: 'center', marginBottom: '60px' }}>
          <h1
            style={{
              fontSize: 'clamp(32px, 5vw, 48px)',
              fontWeight: 700,
              color: textColor,
              marginBottom: '16px',
            }}
          >
            {t.title}
          </h1>
          <p
            style={{
              fontSize: 'clamp(16px, 3vw, 20px)',
              color: textMuted,
              maxWidth: '700px',
              margin: '0 auto',
              lineHeight: 1.6,
            }}
          >
            {t.subtitle}
          </p>
        </div>

        {/* Plans Grid */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
            gap: '24px',
            marginBottom: '80px',
          }}
        >
          {PLANS.map((plan) => (
            <div
              key={plan.id}
              style={{
                background: cardBg,
                borderRadius: '16px',
                padding: '32px',
                border: plan.popular
                  ? `2px solid ${accentColor}`
                  : `1px solid ${borderColor}`,
                position: 'relative',
                boxShadow: plan.popular
                  ? `0 8px 32px ${isDark ? 'rgba(34, 197, 94, 0.2)' : 'rgba(0, 98, 51, 0.2)'}`
                  : 'none',
                display: 'flex',
                flexDirection: 'column',
              }}
            >
              {plan.popular && (
                <div
                  style={{
                    position: 'absolute',
                    top: '-12px',
                    left: '50%',
                    transform: 'translateX(-50%)',
                    background: accentGradient,
                    color: '#fff',
                    padding: '4px 16px',
                    borderRadius: '20px',
                    fontSize: '12px',
                    fontWeight: 600,
                    whiteSpace: 'nowrap',
                  }}
                >
                  {t.popular}
                </div>
              )}

              <h3
                style={{
                  fontSize: '24px',
                  fontWeight: 600,
                  color: textColor,
                  marginBottom: '8px',
                }}
              >
                {plan.name}
              </h3>

              <div style={{ marginBottom: '8px' }}>
                <span
                  style={{
                    fontSize: '48px',
                    fontWeight: 700,
                    color: textColor,
                  }}
                >
                  {plan.price.toLocaleString()}
                </span>
                <span style={{ color: textMuted, fontSize: '16px' }}>
                  {' '}{t.perMonth}
                </span>
              </div>

              <div
                style={{
                  background: isDark ? 'rgba(34, 197, 94, 0.1)' : 'rgba(0, 98, 51, 0.1)',
                  color: accentColor,
                  padding: '8px 16px',
                  borderRadius: '8px',
                  fontSize: '14px',
                  fontWeight: 600,
                  marginBottom: '24px',
                  display: 'inline-block',
                  alignSelf: 'flex-start',
                }}
              >
                {plan.credits.toLocaleString()} {t.creditsMonth}
              </div>

              <ul
                style={{
                  listStyle: 'none',
                  padding: 0,
                  margin: '0 0 32px 0',
                  flex: 1,
                }}
              >
                {plan.features.map((feature, idx) => (
                  <li
                    key={idx}
                    style={{
                      display: 'flex',
                      alignItems: 'flex-start',
                      gap: '12px',
                      color: textMuted,
                      fontSize: '15px',
                      marginBottom: '12px',
                      lineHeight: 1.4,
                    }}
                  >
                    <span style={{ color: accentColor, flexShrink: 0 }}>✓</span>
                    {feature}
                  </li>
                ))}
              </ul>

              <Link
                to={plan.ctaLink}
                style={{
                  display: 'block',
                  width: '100%',
                  padding: '14px',
                  borderRadius: '10px',
                  border: plan.popular ? 'none' : `1px solid ${borderColor}`,
                  background: plan.popular
                    ? accentGradient
                    : 'transparent',
                  color: plan.popular ? '#fff' : textColor,
                  fontSize: '16px',
                  fontWeight: 600,
                  cursor: 'pointer',
                  textAlign: 'center',
                  textDecoration: 'none',
                  transition: 'all 0.2s ease',
                }}
              >
                {plan.cta}
              </Link>
            </div>
          ))}
        </div>

        {/* Credit Examples Section */}
        <div
          style={{
            background: sectionBg,
            borderRadius: '16px',
            padding: '48px 32px',
            marginBottom: '48px',
          }}
        >
          <h2
            style={{
              fontSize: '28px',
              fontWeight: 700,
              color: textColor,
              textAlign: 'center',
              marginBottom: '12px',
            }}
          >
            {t.creditTitle}
          </h2>
          <p
            style={{
              color: textMuted,
              textAlign: 'center',
              marginBottom: '32px',
              fontSize: '15px',
            }}
          >
            {t.creditSubtitle}
          </p>

          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
              gap: '16px',
            }}
          >
            {CREDIT_EXAMPLES.map((example) => (
              <div
                key={example.category}
                style={{
                  background: cardBg,
                  borderRadius: '12px',
                  padding: '20px',
                  textAlign: 'center',
                  border: `1px solid ${borderColor}`,
                }}
              >
                <div style={{ fontSize: '32px', marginBottom: '12px' }}>
                  {example.icon}
                </div>
                <div
                  style={{
                    fontSize: '16px',
                    fontWeight: 600,
                    color: textColor,
                    marginBottom: '4px',
                  }}
                >
                  {example.category}
                </div>
                <div
                  style={{
                    fontSize: '13px',
                    color: accentColor,
                    fontWeight: 500,
                  }}
                >
                  {example.usage}
                </div>
              </div>
            ))}
          </div>

          <p
            style={{
              color: textMuted,
              textAlign: 'center',
              marginTop: '24px',
              fontSize: '13px',
              fontStyle: 'italic',
            }}
          >
            {t.creditNote}
          </p>
        </div>

        {/* Payment Methods */}
        <div style={{ textAlign: 'center', marginBottom: '48px' }}>
          <p style={{ color: textMuted, marginBottom: '16px', fontSize: '15px' }}>
            {t.paymentTitle}
          </p>
          <div
            style={{
              display: 'flex',
              justifyContent: 'center',
              gap: '16px',
              flexWrap: 'wrap',
            }}
          >
            {PAYMENT_METHODS[lang].map((method) => (
              <span
                key={method}
                style={{
                  background: cardBg,
                  padding: '10px 24px',
                  borderRadius: '8px',
                  color: textColor,
                  fontSize: '14px',
                  fontWeight: 500,
                  border: `1px solid ${borderColor}`,
                }}
              >
                {method}
              </span>
            ))}
          </div>
        </div>

        {/* Disclaimer */}
        <div
          style={{
            background: sectionBg,
            borderRadius: '12px',
            padding: '24px',
            textAlign: 'center',
          }}
        >
          <p
            style={{
              color: textMuted,
              fontSize: '13px',
              lineHeight: 1.6,
              margin: 0,
            }}
          >
            {t.disclaimer}
          </p>
        </div>
      </div>
    </div>
  );
}
