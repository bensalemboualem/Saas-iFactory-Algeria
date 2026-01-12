/**
 * IAFactory Internationalization System
 * Supports: French, English, Arabic, Darija (Moroccan/Algerian), Amazigh
 */

export type Language = 'fr' | 'en' | 'ar' | 'darija' | 'amazigh'

export interface Translations {
  [key: string]: string
}

export const translations: Record<Language, Translations> = {
  fr: {
    // Header
    pricing: 'Tarifs',
    apps: 'Applications',
    ai_agents: 'Agents IA',
    workflows: 'Workflows',
    user: 'Utilisateur',
    developer: 'Développeur',
    login: 'Connexion',
    get_started: 'Commencer',
    try_free: 'Essayer gratuitement',

    // Video Platform
    create_video: 'Créer une vidéo',
    projects: 'Projets',
    assets: 'Assets',
    publish: 'Publications',
    new_project: 'Nouveau projet',

    // Hero
    hero_title: 'Créez des vidéos professionnelles',
    hero_title_highlight: 'en quelques secondes',
    hero_subtitle: "Décrivez votre vidéo en langage naturel et laissez l'IA créer le script, les visuels, la voix off et le montage final.",

    // Prompt input
    prompt_placeholder: "Décrivez la vidéo que vous souhaitez créer...\n\nEx: Crée une vidéo de 60 secondes expliquant les avantages de l'intelligence artificielle pour les entreprises, avec un ton professionnel et des visuels modernes.",

    // Duration
    duration_15s: '15 secondes (Short)',
    duration_30s: '30 secondes',
    duration_60s: '60 secondes',
    duration_3min: '3 minutes',
    duration_10min: '10 minutes',

    // Aspect ratio
    ratio_16_9: '16:9 (YouTube)',
    ratio_9_16: '9:16 (TikTok/Reels)',
    ratio_1_1: '1:1 (Instagram)',

    // Style
    style_professional: 'Professionnel',
    style_casual: 'Casual',
    style_cinematic: 'Cinématique',
    style_fun: 'Fun',

    // Button
    generate_video: 'Générer la vidéo',
    generating: 'Génération...',
    creating: 'Création...',

    // Progress
    creating_project: 'Création du projet...',
    analyzing_prompt: 'Analyse du prompt...',
    generating_script: 'Génération du script...',
    creating_images: 'Création des images...',
    generating_video: 'Génération de la vidéo...',
    creating_voiceover: 'Création de la voix off...',
    final_editing: 'Montage final...',
    final_render: 'Rendu final...',
    preparing_publish: 'Préparation publication...',

    // Results
    video_success: 'Vidéo générée avec succès!',
    download_video: 'Télécharger la vidéo',

    // Features
    pipeline_title: 'Pipeline de création complet',
    feature_script: 'Script IA',
    feature_script_desc: 'Génération automatique de scripts structurés',
    feature_visuals: 'Visuels IA',
    feature_visuals_desc: 'Images et vidéos générées avec DALL-E, Runway, etc.',
    feature_audio: 'Audio IA',
    feature_audio_desc: 'Voix off avec ElevenLabs, musique avec Suno',
    feature_multiplatform: 'Multi-plateforme',
    feature_multiplatform_desc: 'Publication automatique sur tous les réseaux',

    // Providers
    providers_title: 'Propulsé par les meilleures IA',
    providers_subtitle: 'Intégration avec tous les providers majeurs pour une qualité optimale',

    // Footer
    products: 'Produits',
    directory: 'Directory IA',
    resources: 'Ressources',
    company: 'Entreprise',
    legal: 'Légal',
    docs: 'Documentation',
    getstarted: 'Démarrage rapide',
    blog: 'Blog',
    support: 'Support',
    about: 'À propos',
    contact: 'Contact',
    newsletter: 'Newsletter',
    mentions: 'Mentions légales',
    privacy: 'Confidentialité',
    terms: 'CGU',
    desc: "Plateforme IA souveraine pour l'Algérie. Applications intelligentes, agents IA, RAG Assistants et workflows automatisés.",
    location: 'Alger, Algérie',
    rights: 'Tous droits réservés.',
    made: 'Fait avec',
    for: "pour l'Algérie",

    // Theme
    dark_mode: 'Mode sombre',
    light_mode: 'Mode clair',
  },

  en: {
    // Header
    pricing: 'Pricing',
    apps: 'Applications',
    ai_agents: 'AI Agents',
    workflows: 'Workflows',
    user: 'User',
    developer: 'Developer',
    login: 'Log in',
    get_started: 'Get Started',
    try_free: 'Try for free',

    // Video Platform
    create_video: 'Create Video',
    projects: 'Projects',
    assets: 'Assets',
    publish: 'Publications',
    new_project: 'New Project',

    // Hero
    hero_title: 'Create professional videos',
    hero_title_highlight: 'in seconds',
    hero_subtitle: 'Describe your video in natural language and let AI create the script, visuals, voiceover and final editing.',

    // Prompt input
    prompt_placeholder: "Describe the video you want to create...\n\nEx: Create a 60-second video explaining the benefits of artificial intelligence for businesses, with a professional tone and modern visuals.",

    // Duration
    duration_15s: '15 seconds (Short)',
    duration_30s: '30 seconds',
    duration_60s: '60 seconds',
    duration_3min: '3 minutes',
    duration_10min: '10 minutes',

    // Aspect ratio
    ratio_16_9: '16:9 (YouTube)',
    ratio_9_16: '9:16 (TikTok/Reels)',
    ratio_1_1: '1:1 (Instagram)',

    // Style
    style_professional: 'Professional',
    style_casual: 'Casual',
    style_cinematic: 'Cinematic',
    style_fun: 'Fun',

    // Button
    generate_video: 'Generate Video',
    generating: 'Generating...',
    creating: 'Creating...',

    // Progress
    creating_project: 'Creating project...',
    analyzing_prompt: 'Analyzing prompt...',
    generating_script: 'Generating script...',
    creating_images: 'Creating images...',
    generating_video: 'Generating video...',
    creating_voiceover: 'Creating voiceover...',
    final_editing: 'Final editing...',
    final_render: 'Final render...',
    preparing_publish: 'Preparing publication...',

    // Results
    video_success: 'Video generated successfully!',
    download_video: 'Download video',

    // Features
    pipeline_title: 'Complete creation pipeline',
    feature_script: 'AI Script',
    feature_script_desc: 'Automatic generation of structured scripts',
    feature_visuals: 'AI Visuals',
    feature_visuals_desc: 'Images and videos generated with DALL-E, Runway, etc.',
    feature_audio: 'AI Audio',
    feature_audio_desc: 'Voiceover with ElevenLabs, music with Suno',
    feature_multiplatform: 'Multi-platform',
    feature_multiplatform_desc: 'Automatic publication on all networks',

    // Providers
    providers_title: 'Powered by the best AI',
    providers_subtitle: 'Integration with all major providers for optimal quality',

    // Footer
    products: 'Products',
    directory: 'IA Directory',
    resources: 'Resources',
    company: 'Company',
    legal: 'Legal',
    docs: 'Documentation',
    getstarted: 'Quick Start',
    blog: 'Blog',
    support: 'Support',
    about: 'About',
    contact: 'Contact',
    newsletter: 'Newsletter',
    mentions: 'Legal Notice',
    privacy: 'Privacy',
    terms: 'Terms',
    desc: 'Sovereign AI platform for Algeria. Intelligent applications, AI agents, RAG Assistants and automated workflows.',
    location: 'Algiers, Algeria',
    rights: 'All rights reserved.',
    made: 'Made with',
    for: 'for Algeria',

    // Theme
    dark_mode: 'Dark mode',
    light_mode: 'Light mode',
  },

  ar: {
    // Header
    pricing: 'الأسعار',
    apps: 'التطبيقات',
    ai_agents: 'وكلاء الذكاء الاصطناعي',
    workflows: 'سير العمل',
    user: 'مستخدم',
    developer: 'مطور',
    login: 'تسجيل الدخول',
    get_started: 'ابدأ الآن',
    try_free: 'جرب مجاناً',

    // Video Platform
    create_video: 'إنشاء فيديو',
    projects: 'المشاريع',
    assets: 'الأصول',
    publish: 'النشر',
    new_project: 'مشروع جديد',

    // Hero
    hero_title: 'أنشئ فيديوهات احترافية',
    hero_title_highlight: 'في ثوانٍ',
    hero_subtitle: 'صف الفيديو الذي تريده بلغة طبيعية ودع الذكاء الاصطناعي يصنع السيناريو والصور والتعليق الصوتي والمونتاج النهائي.',

    // Prompt input
    prompt_placeholder: "صف الفيديو الذي تريد إنشاءه...\n\nمثال: أنشئ فيديو مدته 60 ثانية يشرح فوائد الذكاء الاصطناعي للشركات، بنبرة احترافية ومرئيات حديثة.",

    // Duration
    duration_15s: '15 ثانية (قصير)',
    duration_30s: '30 ثانية',
    duration_60s: '60 ثانية',
    duration_3min: '3 دقائق',
    duration_10min: '10 دقائق',

    // Aspect ratio
    ratio_16_9: '16:9 (يوتيوب)',
    ratio_9_16: '9:16 (تيك توك/ريلز)',
    ratio_1_1: '1:1 (انستغرام)',

    // Style
    style_professional: 'احترافي',
    style_casual: 'عادي',
    style_cinematic: 'سينمائي',
    style_fun: 'ممتع',

    // Button
    generate_video: 'إنشاء الفيديو',
    generating: 'جاري الإنشاء...',
    creating: 'جاري التحضير...',

    // Progress
    creating_project: 'جاري إنشاء المشروع...',
    analyzing_prompt: 'تحليل الطلب...',
    generating_script: 'كتابة السيناريو...',
    creating_images: 'إنشاء الصور...',
    generating_video: 'إنشاء الفيديو...',
    creating_voiceover: 'إنشاء التعليق الصوتي...',
    final_editing: 'المونتاج النهائي...',
    final_render: 'التصيير النهائي...',
    preparing_publish: 'تحضير النشر...',

    // Results
    video_success: 'تم إنشاء الفيديو بنجاح!',
    download_video: 'تحميل الفيديو',

    // Features
    pipeline_title: 'خط إنتاج متكامل',
    feature_script: 'سيناريو ذكي',
    feature_script_desc: 'إنشاء تلقائي لسيناريوهات منظمة',
    feature_visuals: 'مرئيات ذكية',
    feature_visuals_desc: 'صور وفيديوهات بـ DALL-E و Runway وغيرها',
    feature_audio: 'صوت ذكي',
    feature_audio_desc: 'تعليق صوتي مع ElevenLabs وموسيقى مع Suno',
    feature_multiplatform: 'متعدد المنصات',
    feature_multiplatform_desc: 'نشر تلقائي على جميع الشبكات',

    // Providers
    providers_title: 'مدعوم بأفضل تقنيات الذكاء الاصطناعي',
    providers_subtitle: 'تكامل مع جميع مزودي الخدمة الرئيسيين لجودة مثالية',

    // Footer
    products: 'المنتجات',
    directory: 'دليل الذكاء الاصطناعي',
    resources: 'الموارد',
    company: 'الشركة',
    legal: 'قانوني',
    docs: 'التوثيق',
    getstarted: 'البدء السريع',
    blog: 'المدونة',
    support: 'الدعم',
    about: 'من نحن',
    contact: 'اتصل بنا',
    newsletter: 'النشرة الإخبارية',
    mentions: 'الإشعارات القانونية',
    privacy: 'الخصوصية',
    terms: 'الشروط',
    desc: 'منصة ذكاء اصطناعي سيادية للجزائر. تطبيقات ذكية ووكلاء ذكاء اصطناعي ومساعدات RAG وسير عمل آلي.',
    location: 'الجزائر العاصمة',
    rights: 'جميع الحقوق محفوظة.',
    made: 'صنع بـ',
    for: 'للجزائر',

    // Theme
    dark_mode: 'الوضع الداكن',
    light_mode: 'الوضع الفاتح',
  },

  darija: {
    // Header (Algerian/Moroccan Darija)
    pricing: 'الأسعار',
    apps: 'التطبيقات',
    ai_agents: 'عملاء الذكاء',
    workflows: 'سير الخدمة',
    user: 'مستعمل',
    developer: 'مطور',
    login: 'دخول',
    get_started: 'بدا دابا',
    try_free: 'جرب بلاش',

    // Video Platform
    create_video: 'دير فيديو',
    projects: 'المشاريع',
    assets: 'الملفات',
    publish: 'النشر',
    new_project: 'مشروع جديد',

    // Hero
    hero_title: 'دير فيديوهات محترفة',
    hero_title_highlight: 'في ثواني',
    hero_subtitle: 'قول شنو تبغي في الفيديو بالدارجة و خلي الذكاء الاصطناعي يخدم السيناريو والصور والصوت والمونتاج.',

    // Prompt input
    prompt_placeholder: "قول شنو تبغي تدير...\n\nمثال: دير فيديو ديال 60 ثانية على فوائد الذكاء الاصطناعي للشركات، بأسلوب محترف وصور عصرية.",

    // Duration
    duration_15s: '15 ثانية (قصير)',
    duration_30s: '30 ثانية',
    duration_60s: 'دقيقة',
    duration_3min: '3 دقايق',
    duration_10min: '10 دقايق',

    // Aspect ratio
    ratio_16_9: '16:9 (يوتيوب)',
    ratio_9_16: '9:16 (تيك توك)',
    ratio_1_1: '1:1 (انستا)',

    // Style
    style_professional: 'محترف',
    style_casual: 'عادي',
    style_cinematic: 'سينمائي',
    style_fun: 'مرح',

    // Button
    generate_video: 'دير الفيديو',
    generating: 'راه يخدم...',
    creating: 'راه يتحضر...',

    // Progress
    creating_project: 'راه يتحضر المشروع...',
    analyzing_prompt: 'راه يقرا الطلب...',
    generating_script: 'راه يكتب السيناريو...',
    creating_images: 'راه يدير الصور...',
    generating_video: 'راه يدير الفيديو...',
    creating_voiceover: 'راه يدير الصوت...',
    final_editing: 'راه يمونتي...',
    final_render: 'اللمسات الأخيرة...',
    preparing_publish: 'راه يحضر للنشر...',

    // Results
    video_success: 'الفيديو خدم مزيان!',
    download_video: 'حمل الفيديو',

    // Features
    pipeline_title: 'كل شي مدمج',
    feature_script: 'سيناريو ذكي',
    feature_script_desc: 'يكتبلك السيناريو وحدو',
    feature_visuals: 'صور ذكية',
    feature_visuals_desc: 'صور وفيديوهات بالذكاء الاصطناعي',
    feature_audio: 'صوت ذكي',
    feature_audio_desc: 'تعليق صوتي وموسيقى',
    feature_multiplatform: 'كل المنصات',
    feature_multiplatform_desc: 'ينشر وحدو في كل مكان',

    // Providers
    providers_title: 'بأحسن التقنيات',
    providers_subtitle: 'مدمج مع كبار مزودي الذكاء الاصطناعي',

    // Footer
    products: 'المنتجات',
    directory: 'الدليل',
    resources: 'الموارد',
    company: 'الشركة',
    legal: 'قانوني',
    docs: 'الدوكيمنتاسيون',
    getstarted: 'بدا هنا',
    blog: 'المدونة',
    support: 'المساعدة',
    about: 'علينا',
    contact: 'تواصل معانا',
    newsletter: 'الجديد',
    mentions: 'قانوني',
    privacy: 'الخصوصية',
    terms: 'الشروط',
    desc: 'منصة ذكاء اصطناعي جزائرية. تطبيقات ذكية ووكلاء وRAG وworkflows.',
    location: 'الدزاير العاصمة',
    rights: 'كل الحقوق محفوظة.',
    made: 'مصنوع بـ',
    for: 'للدزاير',

    // Theme
    dark_mode: 'الوضع الليلي',
    light_mode: 'الوضع النهاري',
  },

  amazigh: {
    // Header (Tamazight/Amazigh)
    pricing: 'ⵜⵉⵎⴰⵢⵉⵏ',
    apps: 'ⵜⵉⵙⵏⵙⵉⵡⵉⵏ',
    ai_agents: 'ⵉⵎⵓⵔⴰⵏ ⵏ AI',
    workflows: 'ⵜⵉⵡⵓⵔⵉⵡⵉⵏ',
    user: 'ⴰⵎⵙⵙⵎⵔⵙ',
    developer: 'ⴰⵎⵙⵏⴼⵍⵓⵍ',
    login: 'ⴽⵛⵎ',
    get_started: 'ⴱⴷⵓ ⵜⵓⵔⴰ',
    try_free: 'ⴰⵔⵎ ⵓⵍⴰⵛ',

    // Video Platform
    create_video: 'ⵙⵏⵓⵍⴼⵓ ⴰⴼⵉⴷⵢⵓ',
    projects: 'ⵉⵙⵏⴼⴰⵔⵏ',
    assets: 'ⵜⵉⵖⴰⵡⵙⵉⵡⵉⵏ',
    publish: 'ⵙⵓⴼⵖ',
    new_project: 'ⴰⵙⵏⴼⴰⵔ ⴰⵎⴰⵢⵏⵓ',

    // Hero
    hero_title: 'ⵙⵏⵓⵍⴼⵓ ⵉⴼⵉⴷⵢⵓⵜⵏ',
    hero_title_highlight: 'ⴳ ⵜⵉⵙⵉⵏⵜⵉⵏ',
    hero_subtitle: 'ⵙⵎⵍ ⴰⴼⵉⴷⵢⵓ ⵙ ⵜⵓⵜⵍⴰⵢⵜ ⵜⴰⵖⴰⵔⴰⵏⵜ, ⴰⴷ ⵉⵙⵏⵓⵍⴼⵓ AI ⴰⵙⵉⵏⴰⵔⵢⵓ, ⵜⵉⵡⵍⴰⴼⵉⵏ, ⴰⵎⵙⵍⵉ ⴷ ⵓⵎⵓⵏⵜⴰⵊ.',

    // Prompt input
    prompt_placeholder: "ⵙⵎⵍ ⴰⴼⵉⴷⵢⵓ...\n\nⴰⵎⴷⵢⴰ: ⵙⵏⵓⵍⴼⵓ ⴰⴼⵉⴷⵢⵓ ⵏ 60 ⵜⵉⵙⵉⵏⵜⵉⵏ ⵖⴼ ⵜⴰⵎⴼⴰⵢⵜ ⵏ AI ⵉ ⵜⵎⵙⵙⵏⵜⵉⵢⵉⵏ.",

    // Duration
    duration_15s: '15 ⵜⵉⵙⵉⵏⵜⵉⵏ',
    duration_30s: '30 ⵜⵉⵙⵉⵏⵜⵉⵏ',
    duration_60s: '60 ⵜⵉⵙⵉⵏⵜⵉⵏ',
    duration_3min: '3 ⵜⵉⵙⴷⵉⴷⵉⵏ',
    duration_10min: '10 ⵜⵉⵙⴷⵉⴷⵉⵏ',

    // Aspect ratio
    ratio_16_9: '16:9 (YouTube)',
    ratio_9_16: '9:16 (TikTok)',
    ratio_1_1: '1:1 (Instagram)',

    // Style
    style_professional: 'ⴰⵎⵀⵉⵔⴼ',
    style_casual: 'ⴰⵖⴰⵔⴰⵏ',
    style_cinematic: 'ⴰⵙⵉⵏⵉⵎⴰ',
    style_fun: 'ⴰⵙⵎⵔⵃ',

    // Button
    generate_video: 'ⵙⵏⵓⵍⴼⵓ',
    generating: 'ⵉⵜⵜⵓⵙⵏⵓⵍⴼⵓ...',
    creating: 'ⵉⵜⵜⵡⴰⵙⵖⴰⵡⵙⴰ...',

    // Progress
    creating_project: 'ⴰⵙⵖⴰⵡⵙ ⵏ ⵓⵙⵏⴼⴰⵔ...',
    analyzing_prompt: 'ⴰⵙⵍⴳⵎ...',
    generating_script: 'ⴰⵙⵉⵏⴰⵔⵢⵓ...',
    creating_images: 'ⵜⵉⵡⵍⴰⴼⵉⵏ...',
    generating_video: 'ⴰⴼⵉⴷⵢⵓ...',
    creating_voiceover: 'ⴰⵎⵙⵍⵉ...',
    final_editing: 'ⴰⵎⵓⵏⵜⴰⵊ...',
    final_render: 'ⴰⵙⵎⴷⵉ...',
    preparing_publish: 'ⴰⵙⵓⴼⵖ...',

    // Results
    video_success: 'ⵉⵜⵜⵓⵙⵏⵓⵍⴼⵓ ⵓⴼⵉⴷⵢⵓ!',
    download_video: 'ⴰⴳⵎ ⴰⴼⵉⴷⵢⵓ',

    // Features
    pipeline_title: 'ⴰⴱⵔⵉⴷ ⴰⴽⴽⵯ',
    feature_script: 'ⴰⵙⵉⵏⴰⵔⵢⵓ AI',
    feature_script_desc: 'ⴰⵙⵏⵓⵍⴼⵓ ⵏ ⵉⵙⵉⵏⴰⵔⵢⵓⵜⵏ',
    feature_visuals: 'ⵜⵉⵡⵍⴰⴼⵉⵏ AI',
    feature_visuals_desc: 'ⵜⵉⵡⵍⴰⴼⵉⵏ ⴷ ⵉⴼⵉⴷⵢⵓⵜⵏ',
    feature_audio: 'ⴰⵎⵙⵍⵉ AI',
    feature_audio_desc: 'ⴰⵎⵙⵍⵉ ⴷ ⵜⴰⵥⵓⵔⵉ',
    feature_multiplatform: 'ⴰⴽⴽⵯ ⵉⵙⵓⵔⴰⵙⵏ',
    feature_multiplatform_desc: 'ⴰⵙⵓⴼⵖ ⵙ ⴽⵔⴰ ⵏ ⵓⵙⵓⵔⴰⵙ',

    // Providers
    providers_title: 'ⵙ ⵉⵎⵉⵔ ⵏ AI',
    providers_subtitle: 'ⴰⵎⴷⴰⵏ ⴷ ⵉⵎⵓⴼⴰⵢⵏ ⵉⵎⵇⵇⵔⴰⵏⵏ',

    // Footer
    products: 'ⵉⴼⴰⵔⵉⵙⵏ',
    directory: 'ⴰⵙⴳⴳⵯⴰⵙ',
    resources: 'ⵜⵉⵖⴱⵓⵍⴰ',
    company: 'ⵜⴰⵎⵙⵙⵏⵜⵉⵜ',
    legal: 'ⴰⵣⵔⴼ',
    docs: 'ⵜⵉⵙⵖⴰⵍ',
    getstarted: 'ⴱⴷⵓ',
    blog: 'ⴰⴱⵍⵓⴳ',
    support: 'ⵜⴰⵡⵉⵙⵉ',
    about: 'ⵖⴼ ⵏⵖ',
    contact: 'ⴰⵎⵢⴰⵡⴰⴹ',
    newsletter: 'ⵜⴰⴱⵔⴰⵜ',
    mentions: 'ⵉⵣⵔⴼⴰⵏ',
    privacy: 'ⵜⵓⴼⵔⵉⵏⵜ',
    terms: 'ⵜⵉⵡⵜⵉⵍⵉⵏ',
    desc: 'ⴰⵙⵓⵔⴰⵙ ⵏ AI ⵉ ⴷⵣⴰⵢⵔ. ⵜⵉⵙⵏⵙⵉⵡⵉⵏ, ⵉⵎⵓⵔⴰⵏ, RAG ⴷ workflows.',
    location: 'ⴷⵣⴰⵢⵔ ⵜⴰⵎⴰⵏⵖⵜ',
    rights: 'ⵉⵣⵔⴼⴰⵏ ⵎⴰⵕⵕⴰ.',
    made: 'ⵉⵜⵜⵓⵙⴽⴰⵔ ⵙ',
    for: 'ⵉ ⴷⵣⴰⵢⵔ',

    // Theme
    dark_mode: 'ⴰⴱⴰⴷⵓ ⴰⴱⵔⴽⴰⵏ',
    light_mode: 'ⴰⴱⴰⴷⵓ ⴰⵎⵍⵍⴰⵍ',
  }
}

// Language metadata
export const languageInfo: Record<Language, { name: string; nativeName: string; flag: string; dir: 'ltr' | 'rtl' }> = {
  fr: { name: 'French', nativeName: 'Français', flag: '🇫🇷', dir: 'ltr' },
  en: { name: 'English', nativeName: 'English', flag: '🇬🇧', dir: 'ltr' },
  ar: { name: 'Arabic', nativeName: 'العربية', flag: '🇩🇿', dir: 'rtl' },
  darija: { name: 'Darija', nativeName: 'الدارجة', flag: '🇩🇿', dir: 'rtl' },
  amazigh: { name: 'Amazigh', nativeName: 'ⵜⴰⵎⴰⵣⵉⵖⵜ', flag: '🏳️', dir: 'ltr' }
}

// Get translation
export function t(key: string, lang: Language = 'fr'): string {
  return translations[lang][key] || translations.fr[key] || key
}

// Get stored language
export function getStoredLanguage(): Language {
  if (typeof window === 'undefined') return 'fr'
  const stored = localStorage.getItem('iafactory_lang')
  if (stored && stored in translations) {
    return stored as Language
  }
  return 'fr'
}

// Set stored language
export function setStoredLanguage(lang: Language): void {
  if (typeof window === 'undefined') return
  localStorage.setItem('iafactory_lang', lang)
  // Dispatch event for other components
  window.dispatchEvent(new CustomEvent('languageChanged', { detail: { lang } }))
}

// Get document direction
export function getDirection(lang: Language): 'ltr' | 'rtl' {
  return languageInfo[lang].dir
}
