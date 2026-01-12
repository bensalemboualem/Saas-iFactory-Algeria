// Internationalization system
export type Locale = "fr" | "ar" | "en";

export const locales: Locale[] = ["fr", "ar", "en"];

export const localeNames: Record<Locale, string> = {
  fr: "Français",
  ar: "العربية",
  en: "English",
};

export const localeFlags: Record<Locale, string> = {
  fr: "🇫🇷",
  ar: "🇩🇿",
  en: "🇬🇧",
};

// RTL support
export const isRTL = (locale: Locale) => locale === "ar";

// Translations
export const translations: Record<Locale, Record<string, string>> = {
  fr: {
    // Header
    "nav.home": "Accueil",
    "nav.studio": "Studio",
    "nav.editor": "Éditeur",
    "nav.templates": "Modèles",
    "nav.projects": "Projets",
    "nav.credits": "Crédits",
    "nav.settings": "Paramètres",
    
    // Landing
    "hero.title": "Créez des Vidéos IA",
    "hero.subtitle": "en quelques clics",
    "hero.description": "Transformez vos idées en vidéos professionnelles avec l'intelligence artificielle. Génération text-to-video, voix Darija, et montage automatisé.",
    "hero.cta": "Commencer Gratuitement",
    "hero.demo": "Voir la Démo",
    
    // Features
    "features.title": "Fonctionnalités Puissantes",
    "features.text2video.title": "Text-to-Video",
    "features.text2video.desc": "Décrivez votre scène, l'IA génère la vidéo",
    "features.img2video.title": "Image-to-Video",
    "features.img2video.desc": "Animez vos images avec l'IA",
    "features.darija.title": "Voix Darija",
    "features.darija.desc": "Synthèse vocale en dialecte algérien",
    "features.editor.title": "Éditeur Pro",
    "features.editor.desc": "Timeline multi-pistes et effets avancés",
    
    // Studio
    "studio.title": "Studio de Création",
    "studio.description": "Générez des vidéos IA à partir de texte ou d'images",
    "studio.prompt.label": "Description de la vidéo",
    "studio.prompt.placeholder": "Ex: Un coucher de soleil sur le Sahara algérien...",
    "studio.generate": "Générer",
    "studio.generating": "Génération en cours...",
    "studio.success": "Vidéo générée avec succès!",
    "studio.error": "Erreur lors de la génération",
    
    // Editor
    "editor.library": "Bibliothèque",
    "editor.properties": "Propriétés",
    "editor.effects": "Effets Visuels",
    "editor.transitions": "Transitions",
    "editor.addTrack": "Ajouter Piste",
    "editor.export": "Exporter",
    "editor.save": "Sauvegarder",
    "editor.import": "Importer",
    "editor.aiGeneration": "Génération IA",
    
    // Settings
    "settings.title": "Paramètres",
    "settings.theme": "Thème",
    "settings.language": "Langue",
    "settings.dark": "Sombre",
    "settings.light": "Clair",
    
    // Chat
    "chat.title": "Aide IA",
    "chat.placeholder": "Comment puis-je vous aider?",
    "chat.send": "Envoyer",
    
    // Footer
    "footer.rights": "Tous droits réservés",
    "footer.privacy": "Confidentialité",
    "footer.terms": "Conditions",
    "footer.contact": "Contact",
  },
  
  ar: {
    // Header
    "nav.home": "الرئيسية",
    "nav.studio": "الاستوديو",
    "nav.editor": "المحرر",
    "nav.templates": "القوالب",
    "nav.projects": "المشاريع",
    "nav.credits": "الرصيد",
    "nav.settings": "الإعدادات",
    
    // Landing
    "hero.title": "أنشئ فيديوهات بالذكاء الاصطناعي",
    "hero.subtitle": "بنقرات قليلة",
    "hero.description": "حوّل أفكارك إلى فيديوهات احترافية باستخدام الذكاء الاصطناعي. توليد النص إلى فيديو، صوت بالدارجة، ومونتاج آلي.",
    "hero.cta": "ابدأ مجاناً",
    "hero.demo": "شاهد العرض",
    
    // Features
    "features.title": "ميزات قوية",
    "features.text2video.title": "نص إلى فيديو",
    "features.text2video.desc": "صف مشهدك، الذكاء الاصطناعي يولّد الفيديو",
    "features.img2video.title": "صورة إلى فيديو",
    "features.img2video.desc": "حرّك صورك بالذكاء الاصطناعي",
    "features.darija.title": "صوت بالدارجة",
    "features.darija.desc": "تركيب صوتي باللهجة الجزائرية",
    "features.editor.title": "محرر احترافي",
    "features.editor.desc": "تايم لاين متعدد المسارات ومؤثرات متقدمة",
    
    // Studio
    "studio.title": "استوديو الإنشاء",
    "studio.description": "أنشئ فيديوهات ذكاء اصطناعي من النص أو الصور",
    "studio.prompt.label": "وصف الفيديو",
    "studio.prompt.placeholder": "مثال: غروب الشمس على الصحراء الجزائرية...",
    "studio.generate": "توليد",
    "studio.generating": "جاري التوليد...",
    "studio.success": "تم إنشاء الفيديو بنجاح!",
    "studio.error": "خطأ في التوليد",
    
    // Editor
    "editor.library": "المكتبة",
    "editor.properties": "الخصائص",
    "editor.effects": "المؤثرات البصرية",
    "editor.transitions": "الانتقالات",
    "editor.addTrack": "إضافة مسار",
    "editor.export": "تصدير",
    "editor.save": "حفظ",
    "editor.import": "استيراد",
    "editor.aiGeneration": "توليد بالذكاء",
    
    // Settings
    "settings.title": "الإعدادات",
    "settings.theme": "المظهر",
    "settings.language": "اللغة",
    "settings.dark": "داكن",
    "settings.light": "فاتح",
    
    // Chat
    "chat.title": "مساعدة ذكية",
    "chat.placeholder": "كيف يمكنني مساعدتك؟",
    "chat.send": "إرسال",
    
    // Footer
    "footer.rights": "جميع الحقوق محفوظة",
    "footer.privacy": "الخصوصية",
    "footer.terms": "الشروط",
    "footer.contact": "اتصل بنا",
  },
  
  en: {
    // Header
    "nav.home": "Home",
    "nav.studio": "Studio",
    "nav.editor": "Editor",
    "nav.templates": "Templates",
    "nav.projects": "Projects",
    "nav.credits": "Credits",
    "nav.settings": "Settings",
    
    // Landing
    "hero.title": "Create AI Videos",
    "hero.subtitle": "in just a few clicks",
    "hero.description": "Transform your ideas into professional videos with artificial intelligence. Text-to-video generation, Darija voice, and automated editing.",
    "hero.cta": "Start for Free",
    "hero.demo": "Watch Demo",
    
    // Features
    "features.title": "Powerful Features",
    "features.text2video.title": "Text-to-Video",
    "features.text2video.desc": "Describe your scene, AI generates the video",
    "features.img2video.title": "Image-to-Video",
    "features.img2video.desc": "Animate your images with AI",
    "features.darija.title": "Darija Voice",
    "features.darija.desc": "Voice synthesis in Algerian dialect",
    "features.editor.title": "Pro Editor",
    "features.editor.desc": "Multi-track timeline and advanced effects",
    
    // Studio
    "studio.title": "Creation Studio",
    "studio.description": "Generate AI videos from text or images",
    "studio.prompt.label": "Video description",
    "studio.prompt.placeholder": "Ex: A sunset over the Algerian Sahara...",
    "studio.generate": "Generate",
    "studio.generating": "Generating...",
    "studio.success": "Video generated successfully!",
    "studio.error": "Generation error",
    
    // Editor
    "editor.library": "Library",
    "editor.properties": "Properties",
    "editor.effects": "Visual Effects",
    "editor.transitions": "Transitions",
    "editor.addTrack": "Add Track",
    "editor.export": "Export",
    "editor.save": "Save",
    "editor.import": "Import",
    "editor.aiGeneration": "AI Generation",
    
    // Settings
    "settings.title": "Settings",
    "settings.theme": "Theme",
    "settings.language": "Language",
    "settings.dark": "Dark",
    "settings.light": "Light",
    
    // Chat
    "chat.title": "AI Help",
    "chat.placeholder": "How can I help you?",
    "chat.send": "Send",
    
    // Footer
    "footer.rights": "All rights reserved",
    "footer.privacy": "Privacy",
    "footer.terms": "Terms",
    "footer.contact": "Contact",
  },
};

export function t(key: string, locale: Locale): string {
  return translations[locale][key] || key;
}

// Type-safe translation function for common keys
export type TranslationKey = 
  | "heroTitle"
  | "heroSubtitle"
  | "startFree"
  | "textToVideo"
  | "textToVideoDesc"
  | "imageToVideo"
  | "imageToVideoDesc"
  | "darijaVoice"
  | "darijaVoiceDesc";

const commonTranslations: Record<Locale, Record<TranslationKey, string>> = {
  fr: {
    heroTitle: "Créez des Vidéos IA en Darija",
    heroSubtitle: "Générez des vidéos professionnelles avec voix algérienne en quelques clics. Text-to-Video, Image-to-Video, et synchronisation vocale automatique.",
    startFree: "Commencer Gratuitement",
    textToVideo: "Text-to-Video",
    textToVideoDesc: "Décrivez votre scène et laissez l'IA créer une vidéo HD en quelques minutes",
    imageToVideo: "Image-to-Video",
    imageToVideoDesc: "Animez vos images avec des mouvements réalistes et des effets cinématiques",
    darijaVoice: "Voix Darija",
    darijaVoiceDesc: "Générez des voix-off authentiques en dialecte algérien avec ElevenLabs",
  },
  ar: {
    heroTitle: "أنشئ فيديوهات ذكاء اصطناعي بالدارجة",
    heroSubtitle: "أنشئ فيديوهات احترافية بالصوت الجزائري بنقرات قليلة. نص إلى فيديو، صورة إلى فيديو، ومزامنة صوتية تلقائية.",
    startFree: "ابدأ مجاناً",
    textToVideo: "نص إلى فيديو",
    textToVideoDesc: "صف مشهدك ودع الذكاء الاصطناعي يصنع فيديو عالي الدقة في دقائق",
    imageToVideo: "صورة إلى فيديو",
    imageToVideoDesc: "حرّك صورك بحركات واقعية ومؤثرات سينمائية",
    darijaVoice: "صوت بالدارجة",
    darijaVoiceDesc: "أنشئ تعليقات صوتية أصيلة باللهجة الجزائرية مع ElevenLabs",
  },
  en: {
    heroTitle: "Create AI Videos in Darija",
    heroSubtitle: "Generate professional videos with Algerian voice in just a few clicks. Text-to-Video, Image-to-Video, and automatic voice sync.",
    startFree: "Start for Free",
    textToVideo: "Text-to-Video",
    textToVideoDesc: "Describe your scene and let AI create an HD video in minutes",
    imageToVideo: "Image-to-Video",
    imageToVideoDesc: "Animate your images with realistic movements and cinematic effects",
    darijaVoice: "Darija Voice",
    darijaVoiceDesc: "Generate authentic voice-overs in Algerian dialect with ElevenLabs",
  },
};

export function useTranslation(locale: Locale) {
  return (key: TranslationKey): string => {
    return commonTranslations[locale][key] || key;
  };
}
