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

// Données des applications par langue
const appsData: Record<string, App[]> = {
  fr: [
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
  ],
  ar: [
    // ===== الإنتاجية =====
    { id: 'cv-builder', name: 'منشئ السيرة الذاتية', icon: '📄', description: 'أنشئ سير ذاتية احترافية محسّنة لأنظمة التتبع', features: ['قوالب عصرية', 'تحسين ATS', 'تصدير PDF', 'متعدد اللغات'], category: 'الإنتاجية', status: 'available', statusColor: '#00A86B', statusText: 'متاح' },
    { id: 'document-editor', name: 'محرر المستندات الذكي', icon: '📝', description: 'اكتب وحرر المستندات بمساعدة الذكاء الاصطناعي', features: ['كتابة مساعدة', 'تصحيح', 'تنسيق', 'تصدير'], category: 'الإنتاجية', status: 'available', statusColor: '#00A86B', statusText: 'متاح' },
    { id: 'presentation-maker', name: 'منشئ العروض التقديمية', icon: '🎯', description: 'أنشئ عروض تقديمية احترافية تلقائياً', features: ['تصميم تلقائي', 'قوالب', 'رسوم متحركة', 'تصدير PPT'], category: 'الإنتاجية', status: 'available', statusColor: '#00A86B', statusText: 'متاح' },
    { id: 'note-taker', name: 'تدوين الملاحظات الذكي', icon: '📋', description: 'ملاحظات ذكية مع تلخيص تلقائي', features: ['النسخ', 'التلخيص', 'وسوم تلقائية', 'البحث'], category: 'الإنتاجية', status: 'available', statusColor: '#00A86B', statusText: 'متاح' },
    { id: 'task-manager', name: 'مدير المهام', icon: '✅', description: 'نظم مهامك بالذكاء الاصطناعي', features: ['الأولويات', 'التذكيرات', 'التعاون', 'التحليلات'], category: 'الإنتاجية', status: 'beta', statusColor: '#3B82F6', statusText: 'تجريبي' },
    { id: 'calendar-ai', name: 'التقويم الذكي', icon: '📅', description: 'تخطيط ذكي لجدولك الزمني', features: ['جدولة تلقائية', 'تذكيرات ذكية', 'مزامنة', 'اقتراحات'], category: 'الإنتاجية', status: 'available', statusColor: '#00A86B', statusText: 'متاح' },
    // ===== الإبداع =====
    { id: 'image-studio', name: 'استوديو الصور الذكي', icon: '🎨', description: 'أنشئ وحرر الصور بالذكاء الاصطناعي', features: ['إنشاء', 'تعديل', 'أنماط', 'تكبير'], category: 'الإبداع', status: 'available', statusColor: '#00A86B', statusText: 'متاح' },
    { id: 'video-studio', name: 'استوديو الفيديو الذكي', icon: '🎬', description: 'أنشئ ومونتاج الفيديوهات تلقائياً', features: ['مونتاج تلقائي', 'ترجمة', 'مؤثرات', 'تصدير HD'], category: 'الإبداع', status: 'coming_soon', statusColor: '#F59E0B', statusText: 'قريباً' },
    { id: 'audio-studio', name: 'استوديو الصوت الذكي', icon: '🎵', description: 'أنشئ الموسيقى والبودكاست', features: ['تعليق صوتي', 'موسيقى', 'تنقية', 'تصدير MP3'], category: 'الإبداع', status: 'beta', statusColor: '#3B82F6', statusText: 'تجريبي' },
    { id: 'logo-maker', name: 'منشئ الشعارات', icon: '✨', description: 'أنشئ شعارات احترافية في دقائق', features: ['100+ نمط', 'فيكتور', 'ألوان', 'تنويعات'], category: 'الإبداع', status: 'available', statusColor: '#00A86B', statusText: 'متاح' },
    { id: 'banner-studio', name: 'استوديو البانرات', icon: '🖼️', description: 'أنشئ بانرات لجميع شبكاتك', features: ['تنسيقات متعددة', 'قوالب', 'رسوم متحركة', 'تصدير'], category: 'الإبداع', status: 'available', statusColor: '#00A86B', statusText: 'متاح' },
    { id: '3d-model-maker', name: 'نمذجة ثلاثية الأبعاد', icon: '🎲', description: 'أنشئ نماذج 3D بالذكاء الاصطناعي', features: ['نص إلى 3D', 'خامات', 'رسوم متحركة', 'تصدير GLB'], category: 'الإبداع', status: 'coming_soon', statusColor: '#F59E0B', statusText: 'قريباً' },
    // ===== الأعمال =====
    { id: 'crm-app', name: 'إدارة العملاء الذكية', icon: '👥', description: 'أدر عملاءك بالذكاء الاصطناعي', features: ['جهات الاتصال', 'خط المبيعات', 'أتمتة', 'تقارير'], category: 'الأعمال', status: 'available', statusColor: '#00A86B', statusText: 'متاح' },
    { id: 'invoice-app', name: 'الفوترة الذكية', icon: '🧾', description: 'أنشئ وأدر فواتيرك تلقائياً', features: ['قوالب', 'تتبع المدفوعات', 'تذكيرات', 'تصدير'], category: 'الأعمال', status: 'available', statusColor: '#00A86B', statusText: 'متاح' },
    { id: 'accounting-app', name: 'المحاسبة الذكية', icon: '📊', description: 'محاسبة مبسطة لرواد الأعمال', features: ['إدخال تلقائي', 'تقارير', 'TVA', 'تصدير محاسبي'], category: 'الأعمال', status: 'beta', statusColor: '#3B82F6', statusText: 'تجريبي' },
    { id: 'hr-app', name: 'مدير الموارد البشرية', icon: '💼', description: 'إدارة الموارد البشرية', features: ['التوظيف', 'الإدماج', 'الرواتب', 'الإجازات'], category: 'الأعمال', status: 'coming_soon', statusColor: '#F59E0B', statusText: 'قريباً' },
    { id: 'project-app', name: 'إدارة المشاريع', icon: '📋', description: 'أدر مشاريعك بكفاءة', features: ['كانبان', 'غانت', 'الفرق', 'المواعيد النهائية'], category: 'الأعمال', status: 'available', statusColor: '#00A86B', statusText: 'متاح' },
    { id: 'business-plan', name: 'خطة العمل الذكية', icon: '📑', description: 'أنشئ خطة عملك الكاملة', features: ['قوالب جزائرية', 'توقعات', 'تحليل SWOT', 'تصدير PDF'], category: 'الأعمال', status: 'available', statusColor: '#00A86B', statusText: 'متاح' },
    // ===== التسويق =====
    { id: 'social-manager', name: 'مدير وسائل التواصل', icon: '📱', description: 'أدر جميع شبكاتك الاجتماعية', features: ['التخطيط', 'النشر', 'التحليلات', 'حسابات متعددة'], category: 'التسويق', status: 'available', statusColor: '#00A86B', statusText: 'متاح' },
    { id: 'email-marketing', name: 'التسويق عبر البريد', icon: '📧', description: 'حملات بريد إلكتروني آلية', features: ['قوالب', 'تسلسلات', 'اختبار A/B', 'تحليلات'], category: 'التسويق', status: 'available', statusColor: '#00A86B', statusText: 'متاح' },
    { id: 'seo-tools', name: 'أدوات تحسين محركات البحث', icon: '🔍', description: 'حسّن ظهورك في محركات البحث', features: ['تدقيق', 'كلمات مفتاحية', 'روابط خلفية', 'تتبع المواقع'], category: 'التسويق', status: 'available', statusColor: '#00A86B', statusText: 'متاح' },
    { id: 'analytics-dashboard', name: 'لوحة التحليلات', icon: '📈', description: 'لوحة تحليلات شاملة', features: ['مصادر متعددة', 'تصور', 'تقارير', 'تنبيهات'], category: 'التسويق', status: 'beta', statusColor: '#3B82F6', statusText: 'تجريبي' },
    { id: 'ad-manager', name: 'مدير الإعلانات', icon: '📣', description: 'أدر إعلاناتك متعددة المنصات', features: ['Google', 'Facebook', 'تحسين', 'الميزانية'], category: 'التسويق', status: 'coming_soon', statusColor: '#F59E0B', statusText: 'قريباً' },
    // ===== التجارة الإلكترونية =====
    { id: 'store-builder', name: 'منشئ المتاجر', icon: '🛍️', description: 'أنشئ متجرك الإلكتروني', features: ['قوالب', 'دفع جزائري', 'المخزون', 'التوصيل'], category: 'التجارة الإلكترونية', status: 'available', statusColor: '#00A86B', statusText: 'متاح' },
    { id: 'product-manager', name: 'مدير المنتجات', icon: '📦', description: 'أدر كتالوج منتجاتك', features: ['أوصاف ذكية', 'صور', 'أسعار', 'المخزون'], category: 'التجارة الإلكترونية', status: 'available', statusColor: '#00A86B', statusText: 'متاح' },
    { id: 'order-tracker', name: 'تتبع الطلبات', icon: '🚚', description: 'تتبع الطلبات والتوصيل', features: ['الوقت الفعلي', 'SMS', 'السجل', 'المرتجعات'], category: 'التجارة الإلكترونية', status: 'available', statusColor: '#00A86B', statusText: 'متاح' },
    { id: 'marketplace-sync', name: 'مزامنة الأسواق', icon: '🔗', description: 'مزامنة متعددة الأسواق', features: ['جوميا', 'واد كنيس', 'فيسبوك', 'مزامنة المخزون'], category: 'التجارة الإلكترونية', status: 'beta', statusColor: '#3B82F6', statusText: 'تجريبي' },
    { id: 'pricing-optimizer', name: 'محسّن الأسعار', icon: '💰', description: 'حسّن أسعارك بالذكاء الاصطناعي', features: ['تحليل السوق', 'المنافسة', 'هامش تلقائي', 'تنبيهات'], category: 'التجارة الإلكترونية', status: 'available', statusColor: '#00A86B', statusText: 'متاح' },
    // ===== التعليم =====
    { id: 'academy-app', name: 'أكاديمية الذكاء الاصطناعي', icon: '🎓', description: 'منصة تعلم مخصصة', features: ['دورات ذكية', 'اختبارات', 'شهادات', 'التقدم'], category: 'التعليم', status: 'available', statusColor: '#00A86B', statusText: 'متاح' },
    { id: 'tutor-app', name: 'المعلم الشخصي', icon: '👨‍🏫', description: 'معلم ذكي للطلاب', features: ['جميع المواد', 'تمارين', 'تصحيحات', 'ملخصات'], category: 'التعليم', status: 'available', statusColor: '#00A86B', statusText: 'متاح' },
    { id: 'exam-prep', name: 'تحضير الامتحانات', icon: '📚', description: 'التحضير للامتحانات الجزائرية', features: ['البكالوريا', 'شهادة التعليم المتوسط', 'QCM', 'المواضيع السابقة'], category: 'التعليم', status: 'available', statusColor: '#00A86B', statusText: 'متاح' },
    { id: 'flashcards', name: 'بطاقات الحفظ الذكية', icon: '🃏', description: 'حفظ بالتكرار المتباعد', features: ['إنشاء تلقائي', 'تكرار متباعد', 'إحصائيات', 'استيراد'], category: 'التعليم', status: 'available', statusColor: '#00A86B', statusText: 'متاح' },
    { id: 'language-learning', name: 'تعلم اللغات', icon: '🌍', description: 'تعلم الإنجليزية أو الفرنسية أو العربية', features: ['محادثة ذكية', 'قواعد', 'مفردات', 'اختبارات'], category: 'التعليم', status: 'available', statusColor: '#00A86B', statusText: 'متاح' },
    { id: 'homework-helper', name: 'مساعد الواجبات', icon: '✏️', description: 'مساعد لحل التمارين', features: ['الرياضيات', 'الفيزياء', 'العلوم', 'الشرح'], category: 'التعليم', status: 'available', statusColor: '#00A86B', statusText: 'متاح' },
    // ===== التطوير =====
    { id: 'code-editor', name: 'محرر الكود الذكي', icon: '💻', description: 'محرر كود بمساعدة الذكاء الاصطناعي', features: ['إكمال تلقائي', 'تصحيح', 'إعادة الهيكلة', 'متعدد اللغات'], category: 'التطوير', status: 'available', statusColor: '#00A86B', statusText: 'متاح' },
    { id: 'api-portal', name: 'بوابة API', icon: '🔌', description: 'الوصول إلى APIs المصنع الذكي', features: ['التوثيق', 'مفاتيح API', 'الاستخدام', 'الدعم'], category: 'التطوير', status: 'available', statusColor: '#00A86B', statusText: 'متاح' },
    { id: 'no-code-builder', name: 'منشئ بدون كود', icon: '🧩', description: 'أنشئ تطبيقات بدون برمجة', features: ['سحب وإفلات', 'قوالب', 'تكاملات', 'نشر'], category: 'التطوير', status: 'beta', statusColor: '#3B82F6', statusText: 'تجريبي' },
    { id: 'database-studio', name: 'استوديو قواعد البيانات', icon: '🗄️', description: 'إدارة قواعد البيانات', features: ['مرئي', 'استعلامات ذكية', 'ترحيل', 'نسخ احتياطي'], category: 'التطوير', status: 'coming_soon', statusColor: '#F59E0B', statusText: 'قريباً' },
    { id: 'git-assistant', name: 'مساعد Git', icon: '🔀', description: 'مساعد لـ Git والإصدارات', features: ['Commits ذكية', 'مساعد الدمج', 'التعارضات', 'السجل'], category: 'التطوير', status: 'available', statusColor: '#00A86B', statusText: 'متاح' },
    // ===== القانون =====
    { id: 'legal-assistant', name: 'المساعد القانوني', icon: '⚖️', description: 'مساعدة قانونية لرواد الأعمال', features: ['العقود', 'النصائح', 'المتابعة', 'قوالب'], category: 'القانون', status: 'available', statusColor: '#00A86B', statusText: 'متاح' },
    { id: 'contract-generator', name: 'منشئ العقود', icon: '📜', description: 'أنشئ عقوداً مخصصة', features: ['50+ نموذج', 'تخصيص', 'توقيع', 'أرشفة'], category: 'القانون', status: 'available', statusColor: '#00A86B', statusText: 'متاح' },
    { id: 'droit-travail-dz', name: 'قانون العمل الجزائري', icon: '📋', description: 'دليل قانون العمل الجزائري', features: ['قانون العمل', 'الفصل', 'الإجازات', 'الرواتب'], category: 'القانون', status: 'available', statusColor: '#00A86B', statusText: 'متاح' },
    { id: 'registre-commerce', name: 'السجل التجاري', icon: '🏢', description: 'مساعدة إنشاء الشركات في الجزائر', features: ['السجل التجاري', 'القوانين', 'النماذج', 'المتابعة'], category: 'القانون', status: 'available', statusColor: '#00A86B', statusText: 'متاح' },
    // ===== الإدارة الجزائرية =====
    { id: 'admin-dz', name: 'الإدارة الجزائرية', icon: '🇩🇿', description: 'دليل الإجراءات الإدارية الجزائرية', features: ['الضمان الاجتماعي', 'السجل التجاري', 'الضرائب', 'الجمارك'], category: 'الإدارة الجزائرية', status: 'available', statusColor: '#00A86B', statusText: 'متاح' },
    { id: 'tax-calculator', name: 'حاسبة الضرائب', icon: '🧮', description: 'احسب ضرائبك ورسومك', features: ['IRG', 'IBS', 'TVA', 'TAP'], category: 'الإدارة الجزائرية', status: 'available', statusColor: '#00A86B', statusText: 'متاح' },
    { id: 'cnas-assistant', name: 'مساعد الضمان الاجتماعي', icon: '🏥', description: 'مساعدة لإجراءات الضمان الاجتماعي', features: ['الاشتراكات', 'التعويضات', 'النماذج', 'المحاكاة'], category: 'الإدارة الجزائرية', status: 'available', statusColor: '#00A86B', statusText: 'متاح' },
    { id: 'baridimob-helper', name: 'مساعد بريدي موب', icon: '💳', description: 'دليل المدفوعات والتحويلات', features: ['التحويل', 'الشحن', 'الفواتير', 'الدعم'], category: 'الإدارة الجزائرية', status: 'available', statusColor: '#00A86B', statusText: 'متاح' },
    { id: 'visa-dz', name: 'التأشيرة وجواز السفر', icon: '🛂', description: 'إجراءات التأشيرة وجواز السفر البيومتري', features: ['حجز موعد', 'الوثائق', 'المتابعة', 'الأسئلة الشائعة'], category: 'الإدارة الجزائرية', status: 'available', statusColor: '#00A86B', statusText: 'متاح' },
  ],
  en: [
    // ===== PRODUCTIVITY =====
    { id: 'cv-builder', name: 'AI CV Builder', icon: '📄', description: 'Create professional ATS-optimized resumes', features: ['Modern Templates', 'ATS Optimization', 'PDF Export', 'Multi-language'], category: 'Productivity', status: 'available', statusColor: '#00A86B', statusText: 'Available' },
    { id: 'document-editor', name: 'AI Document Editor', icon: '📝', description: 'Write and edit documents with AI assistance', features: ['Assisted Writing', 'Correction', 'Formatting', 'Export'], category: 'Productivity', status: 'available', statusColor: '#00A86B', statusText: 'Available' },
    { id: 'presentation-maker', name: 'Presentation Maker', icon: '🎯', description: 'Generate professional presentations automatically', features: ['Auto Design', 'Templates', 'Animations', 'PPT Export'], category: 'Productivity', status: 'available', statusColor: '#00A86B', statusText: 'Available' },
    { id: 'note-taker', name: 'AI Note Taker', icon: '📋', description: 'Smart notes with automatic summary', features: ['Transcription', 'Summary', 'Auto Tags', 'Search'], category: 'Productivity', status: 'available', statusColor: '#00A86B', statusText: 'Available' },
    { id: 'task-manager', name: 'Task Manager', icon: '✅', description: 'Organize your tasks with AI', features: ['Prioritization', 'Reminders', 'Collaboration', 'Analytics'], category: 'Productivity', status: 'beta', statusColor: '#3B82F6', statusText: 'Beta' },
    { id: 'calendar-ai', name: 'AI Calendar', icon: '📅', description: 'Smart scheduling for your calendar', features: ['Auto-scheduling', 'Smart Reminders', 'Calendar Sync', 'Suggestions'], category: 'Productivity', status: 'available', statusColor: '#00A86B', statusText: 'Available' },
    // ===== CREATION =====
    { id: 'image-studio', name: 'AI Image Studio', icon: '🎨', description: 'Generate and edit images with AI', features: ['Generation', 'Retouching', 'Styles', 'Upscaling'], category: 'Creation', status: 'available', statusColor: '#00A86B', statusText: 'Available' },
    { id: 'video-studio', name: 'AI Video Studio', icon: '🎬', description: 'Create and edit videos automatically', features: ['Auto Editing', 'Subtitles', 'Effects', 'HD Export'], category: 'Creation', status: 'coming_soon', statusColor: '#F59E0B', statusText: 'Coming Soon' },
    { id: 'audio-studio', name: 'AI Audio Studio', icon: '🎵', description: 'Create music and podcasts', features: ['Voice Over', 'Music', 'Cleaning', 'MP3 Export'], category: 'Creation', status: 'beta', statusColor: '#3B82F6', statusText: 'Beta' },
    { id: 'logo-maker', name: 'Logo Maker', icon: '✨', description: 'Create professional logos in minutes', features: ['100+ Styles', 'Vector', 'Palette', 'Variations'], category: 'Creation', status: 'available', statusColor: '#00A86B', statusText: 'Available' },
    { id: 'banner-studio', name: 'Banner Studio', icon: '🖼️', description: 'Create banners for all your networks', features: ['Multi-format', 'Templates', 'Animation', 'Export'], category: 'Creation', status: 'available', statusColor: '#00A86B', statusText: 'Available' },
    { id: '3d-model-maker', name: '3D Modeling', icon: '🎲', description: 'Create 3D models with AI', features: ['Text-to-3D', 'Textures', 'Animation', 'GLB Export'], category: 'Creation', status: 'coming_soon', statusColor: '#F59E0B', statusText: 'Coming Soon' },
    // ===== BUSINESS =====
    { id: 'crm-app', name: 'Smart CRM', icon: '👥', description: 'Manage your customers with AI', features: ['Contacts', 'Pipeline', 'Automation', 'Reports'], category: 'Business', status: 'available', statusColor: '#00A86B', statusText: 'Available' },
    { id: 'invoice-app', name: 'AI Invoicing', icon: '🧾', description: 'Create and manage invoices automatically', features: ['Templates', 'Payment Tracking', 'Reminders', 'Export'], category: 'Business', status: 'available', statusColor: '#00A86B', statusText: 'Available' },
    { id: 'accounting-app', name: 'AI Accounting', icon: '📊', description: 'Simplified accounting for entrepreneurs', features: ['Auto Entry', 'Reports', 'VAT', 'Accounting Export'], category: 'Business', status: 'beta', statusColor: '#3B82F6', statusText: 'Beta' },
    { id: 'hr-app', name: 'HR Manager', icon: '💼', description: 'Human resources management', features: ['Recruitment', 'Onboarding', 'Payroll', 'Leave'], category: 'Business', status: 'coming_soon', statusColor: '#F59E0B', statusText: 'Coming Soon' },
    { id: 'project-app', name: 'Project Management', icon: '📋', description: 'Manage your projects efficiently', features: ['Kanban', 'Gantt', 'Teams', 'Deadlines'], category: 'Business', status: 'available', statusColor: '#00A86B', statusText: 'Available' },
    { id: 'business-plan', name: 'AI Business Plan', icon: '📑', description: 'Generate your complete business plan', features: ['DZ Templates', 'Projections', 'Auto SWOT', 'PDF Export'], category: 'Business', status: 'available', statusColor: '#00A86B', statusText: 'Available' },
    // ===== MARKETING =====
    { id: 'social-manager', name: 'Social Media Manager', icon: '📱', description: 'Manage all your social networks', features: ['Planning', 'Publishing', 'Analytics', 'Multi-account'], category: 'Marketing', status: 'available', statusColor: '#00A86B', statusText: 'Available' },
    { id: 'email-marketing', name: 'Email Marketing', icon: '📧', description: 'Automated email campaigns', features: ['Templates', 'Sequences', 'A/B Testing', 'Analytics'], category: 'Marketing', status: 'available', statusColor: '#00A86B', statusText: 'Available' },
    { id: 'seo-tools', name: 'SEO Tools', icon: '🔍', description: 'Optimize your SEO', features: ['Audit', 'Keywords', 'Backlinks', 'Position Tracking'], category: 'Marketing', status: 'available', statusColor: '#00A86B', statusText: 'Available' },
    { id: 'analytics-dashboard', name: 'Analytics Dashboard', icon: '📈', description: 'Complete analytics dashboard', features: ['Multi-source', 'Visualization', 'Reports', 'Alerts'], category: 'Marketing', status: 'beta', statusColor: '#3B82F6', statusText: 'Beta' },
    { id: 'ad-manager', name: 'Ads Manager', icon: '📣', description: 'Manage your multi-platform ads', features: ['Google', 'Facebook', 'Optimization', 'Budget'], category: 'Marketing', status: 'coming_soon', statusColor: '#F59E0B', statusText: 'Coming Soon' },
    // ===== E-COMMERCE =====
    { id: 'store-builder', name: 'Store Builder', icon: '🛍️', description: 'Create your online store', features: ['Templates', 'DZ Payment', 'Inventory', 'Shipping'], category: 'E-Commerce', status: 'available', statusColor: '#00A86B', statusText: 'Available' },
    { id: 'product-manager', name: 'Product Manager', icon: '📦', description: 'Manage your product catalog', features: ['AI Descriptions', 'Photos', 'Pricing', 'Stock'], category: 'E-Commerce', status: 'available', statusColor: '#00A86B', statusText: 'Available' },
    { id: 'order-tracker', name: 'Order Tracker', icon: '🚚', description: 'Order and delivery tracking', features: ['Real-time', 'SMS', 'History', 'Returns'], category: 'E-Commerce', status: 'available', statusColor: '#00A86B', statusText: 'Available' },
    { id: 'marketplace-sync', name: 'Marketplace Sync', icon: '🔗', description: 'Multi-marketplace synchronization', features: ['Jumia', 'Ouedkniss', 'Facebook', 'Stock Sync'], category: 'E-Commerce', status: 'beta', statusColor: '#3B82F6', statusText: 'Beta' },
    { id: 'pricing-optimizer', name: 'Price Optimizer', icon: '💰', description: 'Optimize your prices with AI', features: ['Market Analysis', 'Competition', 'Auto Margin', 'Alerts'], category: 'E-Commerce', status: 'available', statusColor: '#00A86B', statusText: 'Available' },
    // ===== EDUCATION =====
    { id: 'academy-app', name: 'AI Academy', icon: '🎓', description: 'Personalized learning platform', features: ['AI Courses', 'Quiz', 'Certificates', 'Progress'], category: 'Education', status: 'available', statusColor: '#00A86B', statusText: 'Available' },
    { id: 'tutor-app', name: 'Personal Tutor', icon: '👨‍🏫', description: 'AI tutor for students', features: ['All Subjects', 'Exercises', 'Corrections', 'Notes'], category: 'Education', status: 'available', statusColor: '#00A86B', statusText: 'Available' },
    { id: 'exam-prep', name: 'Exam Prep', icon: '📚', description: 'Preparation for Algerian exams', features: ['BAC', 'BEM', 'MCQ', 'Past Papers'], category: 'Education', status: 'available', statusColor: '#00A86B', statusText: 'Available' },
    { id: 'flashcards', name: 'AI Flashcards', icon: '🃏', description: 'Memorization with spaced repetition', features: ['Auto Generation', 'Spaced Rep', 'Stats', 'Import'], category: 'Education', status: 'available', statusColor: '#00A86B', statusText: 'Available' },
    { id: 'language-learning', name: 'Language Learning', icon: '🌍', description: 'Learn English, French or Arabic', features: ['AI Conversation', 'Grammar', 'Vocabulary', 'Tests'], category: 'Education', status: 'available', statusColor: '#00A86B', statusText: 'Available' },
    { id: 'homework-helper', name: 'Homework Helper', icon: '✏️', description: 'Assistant for solving exercises', features: ['Math', 'Physics', 'Science', 'Explanations'], category: 'Education', status: 'available', statusColor: '#00A86B', statusText: 'Available' },
    // ===== DEVELOPMENT =====
    { id: 'code-editor', name: 'AI Code Editor', icon: '💻', description: 'Code editor with AI assistance', features: ['Autocomplete', 'Debug', 'Refactoring', 'Multi-lang'], category: 'Development', status: 'available', statusColor: '#00A86B', statusText: 'Available' },
    { id: 'api-portal', name: 'API Portal', icon: '🔌', description: 'Access to IA Factory APIs', features: ['Documentation', 'API Keys', 'Usage', 'Support'], category: 'Development', status: 'available', statusColor: '#00A86B', statusText: 'Available' },
    { id: 'no-code-builder', name: 'No-Code Builder', icon: '🧩', description: 'Create apps without coding', features: ['Drag & Drop', 'Templates', 'Integrations', 'Publish'], category: 'Development', status: 'beta', statusColor: '#3B82F6', statusText: 'Beta' },
    { id: 'database-studio', name: 'Database Studio', icon: '🗄️', description: 'Database management', features: ['Visual', 'AI Queries', 'Migration', 'Backup'], category: 'Development', status: 'coming_soon', statusColor: '#F59E0B', statusText: 'Coming Soon' },
    { id: 'git-assistant', name: 'Git Assistant', icon: '🔀', description: 'Assistant for Git and versioning', features: ['AI Commits', 'Merge Helper', 'Conflicts', 'History'], category: 'Development', status: 'available', statusColor: '#00A86B', statusText: 'Available' },
    // ===== LEGAL =====
    { id: 'legal-assistant', name: 'Legal Assistant', icon: '⚖️', description: 'Legal help for entrepreneurs', features: ['Contracts', 'Advice', 'Watch', 'Templates'], category: 'Legal', status: 'available', statusColor: '#00A86B', statusText: 'Available' },
    { id: 'contract-generator', name: 'Contract Generator', icon: '📜', description: 'Create customized contracts', features: ['50+ Templates', 'Customization', 'Signature', 'Archive'], category: 'Legal', status: 'available', statusColor: '#00A86B', statusText: 'Available' },
    { id: 'droit-travail-dz', name: 'DZ Labor Law', icon: '📋', description: 'Algerian labor law guide', features: ['Labor Code', 'Dismissal', 'Leave', 'Salaries'], category: 'Legal', status: 'available', statusColor: '#00A86B', statusText: 'Available' },
    { id: 'registre-commerce', name: 'Trade Registry', icon: '🏢', description: 'Help creating business in Algeria', features: ['CNRC', 'Statutes', 'Forms', 'Tracking'], category: 'Legal', status: 'available', statusColor: '#00A86B', statusText: 'Available' },
    // ===== ADMIN DZ =====
    { id: 'admin-dz', name: 'Admin DZ', icon: '🇩🇿', description: 'Guide to Algerian administrative procedures', features: ['CNAS', 'CNRC', 'Taxes', 'Customs'], category: 'Admin DZ', status: 'available', statusColor: '#00A86B', statusText: 'Available' },
    { id: 'tax-calculator', name: 'Tax Calculator', icon: '🧮', description: 'Calculate your taxes', features: ['IRG', 'IBS', 'VAT', 'TAP'], category: 'Admin DZ', status: 'available', statusColor: '#00A86B', statusText: 'Available' },
    { id: 'cnas-assistant', name: 'CNAS Assistant', icon: '🏥', description: 'Help for CNAS/CASNOS procedures', features: ['Contributions', 'Reimbursements', 'Forms', 'Simulation'], category: 'Admin DZ', status: 'available', statusColor: '#00A86B', statusText: 'Available' },
    { id: 'baridimob-helper', name: 'BaridiMob Helper', icon: '💳', description: 'Guide to BaridiMob payments and transfers', features: ['Transfer', 'Recharge', 'Bills', 'Support'], category: 'Admin DZ', status: 'available', statusColor: '#00A86B', statusText: 'Available' },
    { id: 'visa-dz', name: 'Visa & Passport DZ', icon: '🛂', description: 'Visa and biometric passport procedures', features: ['Online Appointment', 'Documents', 'Tracking', 'FAQ'], category: 'Admin DZ', status: 'available', statusColor: '#00A86B', statusText: 'Available' },
  ],
};

// Fonction pour obtenir les apps selon la langue
const getApps = (lang: string): App[] => {
  return appsData[lang] || appsData['fr'];
};

// Fonction pour obtenir les catégories selon la langue
const getCategories = (lang: string): string[] => {
  const apps = getApps(lang);
  return [...new Set(apps.map(a => a.category))];
};

export default function Apps() {
  const { t, lang } = useTranslation();
  const navigate = useNavigate();
  const [theme, setTheme] = useState<Theme>('dark');
  const isRTL = lang === 'ar';
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [isLoggedIn] = useState(() => localStorage.getItem('isLoggedIn') === 'true');

  // Obtenir les apps et catégories selon la langue
  const allApps = getApps(lang);
  const categories = getCategories(lang);

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
  const filteredApps = allApps.filter((app: App) => {
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
  // Couleurs synchronisées avec Home.tsx
  const bgColor = isDark ? '#0A0F1A' : '#F6F3EE';
  const cardBg = isDark ? 'rgba(255,255,255,0.06)' : '#EDE9E3';
  const textColor = isDark ? '#F8FAFC' : '#141414';
  const textMuted = isDark ? 'rgba(248,250,252,0.65)' : 'rgba(20,20,20,0.62)';
  const borderColor = isDark ? 'rgba(255,255,255,0.10)' : 'rgba(20,20,20,0.10)';
  const inputBg = isDark ? 'rgba(255,255,255,0.06)' : '#EDE9E3';
  const accentColor = isDark ? '#22C55E' : '#1C7A5F';
  const accentGradient = `linear-gradient(135deg, ${isDark ? '#22C55E' : '#1C7A5F'}, ${isDark ? '#57D6AA' : '#22C55E'})`;

  const availableCount = allApps.filter((a: App) => a.status === 'available').length;
  const betaCount = allApps.filter((a: App) => a.status === 'beta').length;

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
                padding: isRTL ? '14px 50px 14px 20px' : '14px 20px 14px 50px',
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
                left: isRTL ? 'auto' : '18px',
                right: isRTL ? '18px' : 'auto',
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
                border: `1px solid ${selectedCategory === 'all' ? accentColor : borderColor}`,
                background: selectedCategory === 'all' ? (isDark ? 'rgba(34, 197, 94, 0.15)' : 'rgba(0, 98, 51, 0.15)') : 'transparent',
                color: selectedCategory === 'all' ? accentColor : textMuted,
                fontSize: '14px',
                fontWeight: 500,
                cursor: 'pointer',
              }}
            >
              {t('apps_all')} ({allApps.length})
            </button>
            {categories.map((cat: string) => {
              const count = allApps.filter((a: App) => a.category === cat).length;
              return (
                <button
                  key={cat}
                  type="button"
                  onClick={() => setSelectedCategory(cat)}
                  style={{
                    padding: '8px 16px',
                    borderRadius: '20px',
                    border: `1px solid ${selectedCategory === cat ? accentColor : borderColor}`,
                    background: selectedCategory === cat ? (isDark ? 'rgba(34, 197, 94, 0.15)' : 'rgba(0, 98, 51, 0.15)') : 'transparent',
                    color: selectedCategory === cat ? accentColor : textMuted,
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
          {filteredApps.map((app: App) => (
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
                  e.currentTarget.style.borderColor = accentColor;
                  e.currentTarget.style.boxShadow = isDark ? '0 12px 24px rgba(34, 197, 94, 0.15)' : '0 12px 24px rgba(0, 98, 51, 0.15)';
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
                  color: accentColor,
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
                  {app.features.map((feature: string) => (
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
                    : accentGradient,
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
                    <span>{isRTL ? '←' : '→'}</span>
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
            border: `2px solid ${accentColor}`,
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
              background: accentGradient,
              color: '#fff',
              fontSize: 'clamp(16px, 2.5vw, 18px)',
              fontWeight: 600,
              border: 'none',
              borderRadius: '12px',
              cursor: 'pointer',
              boxShadow: isDark ? '0 4px 16px rgba(34, 197, 94, 0.3)' : '0 4px 16px rgba(0, 98, 51, 0.3)',
            }}
          >
            {isLoggedIn ? t('apps_access') : t('apps_start_free')}
          </button>
        </div>
      </div>
    </div>
  );
}
