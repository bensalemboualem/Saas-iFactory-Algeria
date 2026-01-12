"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { 
  Play, 
  Sparkles, 
  Mic, 
  Film, 
  ArrowRight, 
  Zap, 
  Globe, 
  Shield,
  Users,
  Star,
  ChevronRight
} from "lucide-react";
import { useLocaleStore } from "@/lib/store";
import { useTranslation, isRTL } from "@/lib/i18n";

export default function HomePage() {
  const { locale } = useLocaleStore();
  const t = useTranslation(locale);
  const rtl = isRTL(locale);

  const features = [
    {
      icon: Sparkles,
      titleKey: "textToVideo" as const,
      descKey: "textToVideoDesc" as const,
    },
    {
      icon: Film,
      titleKey: "imageToVideo" as const,
      descKey: "imageToVideoDesc" as const,
    },
    {
      icon: Mic,
      titleKey: "darijaVoice" as const,
      descKey: "darijaVoiceDesc" as const,
    },
  ];

  const stats = [
    { value: "10K+", label: locale === 'ar' ? 'فيديوهات مُنشأة' : locale === 'en' ? 'Videos Generated' : 'Vidéos Générées' },
    { value: "5K+", label: locale === 'ar' ? 'مستخدم نشط' : locale === 'en' ? 'Active Users' : 'Utilisateurs Actifs' },
    { value: "99.9%", label: locale === 'ar' ? 'وقت التشغيل' : locale === 'en' ? 'Uptime' : 'Disponibilité' },
    { value: "< 2min", label: locale === 'ar' ? 'وقت الإنشاء' : locale === 'en' ? 'Generation Time' : 'Temps de Génération' },
  ];

  const useCases = [
    {
      icon: Users,
      title: locale === 'ar' ? 'التسويق الرقمي' : locale === 'en' ? 'Digital Marketing' : 'Marketing Digital',
      desc: locale === 'ar' ? 'إنشاء إعلانات فيديو مؤثرة بالعربية الجزائرية' : locale === 'en' ? 'Create impactful video ads in Algerian Arabic' : 'Créez des publicités vidéo percutantes en arabe algérien',
    },
    {
      icon: Globe,
      title: locale === 'ar' ? 'التجارة الإلكترونية' : locale === 'en' ? 'E-commerce' : 'E-commerce',
      desc: locale === 'ar' ? 'عرض المنتجات بفيديوهات احترافية' : locale === 'en' ? 'Showcase products with professional videos' : 'Présentez vos produits avec des vidéos professionnelles',
    },
    {
      icon: Shield,
      title: locale === 'ar' ? 'وسائل التواصل' : locale === 'en' ? 'Social Media' : 'Réseaux Sociaux',
      desc: locale === 'ar' ? 'محتوى فيديو متميز لجميع المنصات' : locale === 'en' ? 'Outstanding video content for all platforms' : 'Contenu vidéo remarquable pour toutes les plateformes',
    },
  ];

  return (
    <div className="min-h-screen" dir={rtl ? 'rtl' : 'ltr'}>
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-8 pb-20">
        {/* Background effects */}
        <div className="absolute inset-0 bg-gradient-to-br from-primary/20 via-transparent to-accent/10" />
        <div className="absolute inset-0 bg-[linear-gradient(rgba(99,102,241,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(99,102,241,0.03)_1px,transparent_1px)] bg-[size:64px_64px]" />
        
        {/* Floating orbs */}
        <div className="absolute top-20 left-10 w-72 h-72 bg-primary/30 rounded-full blur-[120px] animate-pulse" />
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-accent/20 rounded-full blur-[150px] animate-pulse" />

        <div className="relative max-w-7xl mx-auto px-6">
          {/* Hero content */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center max-w-4xl mx-auto pt-16"
          >
            {/* Badge */}
            <motion.div 
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.2 }}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-surface/80 backdrop-blur border border-border mb-8"
            >
              <Sparkles className="w-4 h-4 text-accent" />
              <span className="text-sm text-text-muted">
                {locale === 'ar' ? 'مدعوم بـ Kling 1.6 و ElevenLabs' : 
                 locale === 'en' ? 'Powered by Kling 1.6 & ElevenLabs' : 
                 'Propulsé par Kling 1.6 & ElevenLabs'}
              </span>
            </motion.div>

            {/* Main headline */}
            <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
              <span className="bg-gradient-to-r from-white via-primary to-accent bg-clip-text text-transparent">
                {t('heroTitle')}
              </span>
            </h1>

            <p className="text-xl text-text-muted mb-12 max-w-2xl mx-auto leading-relaxed">
              {t('heroSubtitle')}
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link
                href="/studio"
                className="group flex items-center gap-2 px-8 py-4 bg-primary hover:bg-primary-hover rounded-xl font-semibold text-lg transition-all pulse-glow"
              >
                <Play className="w-5 h-5" />
                {t('startFree')}
                <ArrowRight className={`w-5 h-5 transition-transform ${rtl ? 'group-hover:-translate-x-1 rotate-180' : 'group-hover:translate-x-1'}`} />
              </Link>
              <Link
                href="/editor"
                className="flex items-center gap-2 px-8 py-4 bg-surface hover:bg-surface-hover border border-border rounded-xl font-semibold text-lg transition-colors"
              >
                <Film className="w-5 h-5" />
                {locale === 'ar' ? 'جرب المحرر المتقدم' : 
                 locale === 'en' ? 'Try Pro Editor' : 
                 'Essayer l\'Éditeur Pro'}
              </Link>
            </div>
          </motion.div>

          {/* Stats */}
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-20"
          >
            {stats.map((stat, i) => (
              <div key={i} className="text-center p-6 rounded-2xl bg-surface/50 backdrop-blur border border-border">
                <div className="text-3xl font-bold text-primary mb-1">{stat.value}</div>
                <div className="text-sm text-text-muted">{stat.label}</div>
              </div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 relative">
        <div className="max-w-7xl mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold mb-4">
              {locale === 'ar' ? 'ميزات قوية' : 
               locale === 'en' ? 'Powerful Features' : 
               'Fonctionnalités Puissantes'}
            </h2>
            <p className="text-text-muted text-lg max-w-2xl mx-auto">
              {locale === 'ar' ? 'كل ما تحتاجه لإنشاء فيديوهات احترافية بالذكاء الاصطناعي' : 
               locale === 'en' ? 'Everything you need to create professional AI videos' : 
               'Tout ce dont vous avez besoin pour créer des vidéos IA professionnelles'}
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="group p-8 rounded-3xl bg-surface border border-border hover:border-primary/50 transition-all hover:shadow-xl hover:shadow-primary/5"
              >
                <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-primary/20 to-accent/20 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                  <feature.icon className="w-7 h-7 text-primary" />
                </div>
                <h3 className="text-2xl font-semibold mb-3">{t(feature.titleKey)}</h3>
                <p className="text-text-muted leading-relaxed">{t(feature.descKey)}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Use Cases Section */}
      <section className="py-24 bg-surface/30">
        <div className="max-w-7xl mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold mb-4">
              {locale === 'ar' ? 'حالات الاستخدام' : 
               locale === 'en' ? 'Use Cases' : 
               'Cas d\'Utilisation'}
            </h2>
            <p className="text-text-muted text-lg">
              {locale === 'ar' ? 'اكتشف كيف تستفيد الشركات من فيديوهاتنا بالذكاء الاصطناعي' : 
               locale === 'en' ? 'Discover how businesses leverage our AI videos' : 
               'Découvrez comment les entreprises tirent parti de nos vidéos IA'}
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {useCases.map((useCase, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, scale: 0.95 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="relative overflow-hidden p-8 rounded-3xl bg-gradient-to-br from-surface to-surface-hover border border-border group"
              >
                <div className="absolute top-0 right-0 w-32 h-32 bg-primary/10 rounded-full blur-3xl group-hover:bg-primary/20 transition-colors" />
                <useCase.icon className="w-10 h-10 text-accent mb-4" />
                <h3 className="text-xl font-semibold mb-2">{useCase.title}</h3>
                <p className="text-text-muted">{useCase.desc}</p>
                <ChevronRight className={`w-5 h-5 text-primary mt-4 ${rtl ? 'rotate-180' : ''}`} />
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24">
        <div className="max-w-4xl mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="relative overflow-hidden p-12 rounded-3xl bg-gradient-to-r from-primary/20 via-surface to-accent/20 border border-border text-center"
          >
            {/* Decorative elements */}
            <div className="absolute -top-20 -left-20 w-40 h-40 bg-primary/30 rounded-full blur-3xl" />
            <div className="absolute -bottom-20 -right-20 w-40 h-40 bg-accent/30 rounded-full blur-3xl" />
            
            <div className="relative">
              <div className="flex items-center justify-center gap-1 mb-4">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} className="w-5 h-5 fill-yellow-500 text-yellow-500" />
                ))}
              </div>
              
              <h2 className="text-4xl font-bold mb-4">
                {locale === 'ar' ? 'ابدأ الإنشاء اليوم' : 
                 locale === 'en' ? 'Start Creating Today' : 
                 'Commencez à Créer Aujourd\'hui'}
              </h2>
              
              <p className="text-text-muted text-lg mb-8 max-w-xl mx-auto">
                {locale === 'ar' ? 'انضم إلى آلاف المبدعين الذين يستخدمون IA Factory لإنشاء فيديوهات مذهلة' : 
                 locale === 'en' ? 'Join thousands of creators using IA Factory to produce stunning videos' : 
                 'Rejoignez des milliers de créateurs qui utilisent IA Factory pour produire des vidéos époustouflantes'}
              </p>
              
              <Link
                href="/studio"
                className="inline-flex items-center gap-2 px-8 py-4 bg-primary hover:bg-primary-hover rounded-xl font-semibold text-lg transition-all"
              >
                <Zap className="w-5 h-5" />
                {locale === 'ar' ? 'ابدأ مجاناً' : 
                 locale === 'en' ? 'Get Started Free' : 
                 'Démarrer Gratuitement'}
              </Link>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  );
}
