// BBC School Algeria - Chatbot Dashboard Translations
// Système trilingue: العربية / Français / English

const translations = {
    en: {
        // Navigation
        dashboard: "Dashboard",
        conversations: "Conversations", 
        analytics: "Analytics",
        students: "Students",
        teachers: "Teachers",
        settings: "Settings",
        
        // Stats
        quick_stats: "Quick Stats",
        parents: "Parents",
        follow_us: "Follow Us",
        
        // Dashboard
        ai_dashboard: "AI Chatbot Dashboard",
        dashboard_subtitle: "Manage your school's AI assistant",
        total_chats: "Total Chats",
        avg_response: "Avg Response",
        satisfaction: "Satisfaction",
        languages: "Languages",
        
        // Chat
        live_chat: "Live Chat Interface",
        online: "Online",
        welcome_message: "Welcome to BBC School Algeria! How can I help you today?",
        type_message: "Type your message...",
        
        // Analytics
        chat_analytics: "Chat Analytics",
        recent_activity: "Recent Activity",
        student_inquiry: "Student inquiry about enrollment",
        arabic_chat: "Arabic language chat session",
        positive_feedback: "Positive feedback received",
        
        // Loading
        conversations_loading: "Loading conversations...",
        analytics_loading: "Loading analytics...",
        students_loading: "Loading students data...",
        teachers_loading: "Loading teachers data...",
        settings_loading: "Loading settings..."
    },
    
    fr: {
        // Navigation
        dashboard: "Tableau de Bord",
        conversations: "Conversations",
        analytics: "Analyses",
        students: "Étudiants",
        teachers: "Professeurs",
        settings: "Paramètres",
        
        // Stats
        quick_stats: "Stats Rapides",
        parents: "Parents",
        follow_us: "Nous Suivre",
        
        // Dashboard
        ai_dashboard: "Tableau de Bord IA Chatbot",
        dashboard_subtitle: "Gérez l'assistant IA de votre école",
        total_chats: "Total Discussions",
        avg_response: "Réponse Moy.",
        satisfaction: "Satisfaction",
        languages: "Langues",
        
        // Chat
        live_chat: "Interface Chat en Direct",
        online: "En Ligne",
        welcome_message: "Bienvenue à BBC School Algeria ! Comment puis-je vous aider aujourd'hui ?",
        type_message: "Tapez votre message...",
        
        // Analytics
        chat_analytics: "Analyses des Chats",
        recent_activity: "Activité Récente",
        student_inquiry: "Demande d'étudiant sur l'inscription",
        arabic_chat: "Session de chat en arabe",
        positive_feedback: "Commentaire positif reçu",
        
        // Loading
        conversations_loading: "Chargement des conversations...",
        analytics_loading: "Chargement des analyses...",
        students_loading: "Chargement des données étudiants...",
        teachers_loading: "Chargement des données professeurs...",
        settings_loading: "Chargement des paramètres..."
    },
    
    ar: {
        // Navigation
        dashboard: "لوحة التحكم",
        conversations: "المحادثات",
        analytics: "التحليلات",
        students: "الطلاب",
        teachers: "المعلمون",
        settings: "الإعدادات",
        
        // Stats
        quick_stats: "إحصائيات سريعة",
        parents: "أولياء الأمور",
        follow_us: "تابعونا",
        
        // Dashboard
        ai_dashboard: "لوحة تحكم الذكاء الاصطناعي",
        dashboard_subtitle: "إدارة مساعد الذكاء الاصطناعي للمدرسة",
        total_chats: "إجمالي المحادثات",
        avg_response: "متوسط الاستجابة",
        satisfaction: "الرضا",
        languages: "اللغات",
        
        // Chat
        live_chat: "واجهة الدردشة المباشرة",
        online: "متصل",
        welcome_message: "مرحباً بكم في مدرسة بي بي سي الجزائر! كيف يمكنني مساعدتكم اليوم؟",
        type_message: "اكتب رسالتك...",
        
        // Analytics
        chat_analytics: "تحليلات المحادثات",
        recent_activity: "النشاط الأخير",
        student_inquiry: "استفسار طالب حول التسجيل",
        arabic_chat: "جلسة دردشة باللغة العربية",
        positive_feedback: "تلقي تعليق إيجابي",
        
        // Loading
        conversations_loading: "جاري تحميل المحادثات...",
        analytics_loading: "جاري تحميل التحليلات...",
        students_loading: "جاري تحميل بيانات الطلاب...",
        teachers_loading: "جاري تحميل بيانات المعلمين...",
        settings_loading: "جاري تحميل الإعدادات..."
    }
};

// Current language state
let currentLanguage = 'en';

// Change language function
function changeLanguage() {
    const languageSelect = document.getElementById('languageSelect');
    currentLanguage = languageSelect.value;
    
    // Update document direction for Arabic
    if (currentLanguage === 'ar') {
        document.documentElement.setAttribute('dir', 'rtl');
        document.documentElement.setAttribute('lang', 'ar');
    } else {
        document.documentElement.setAttribute('dir', 'ltr');
        document.documentElement.setAttribute('lang', currentLanguage);
    }
    
    // Update all translatable elements
    updateTranslations();
    
    // Save language preference
    localStorage.setItem('bbc_chatbot_language', currentLanguage);
}

// Update translations on page
function updateTranslations() {
    const elements = document.querySelectorAll('[data-translate]');
    
    elements.forEach(element => {
        const key = element.getAttribute('data-translate');
        if (translations[currentLanguage] && translations[currentLanguage][key]) {
            element.textContent = translations[currentLanguage][key];
        }
    });
    
    // Update placeholders
    const placeholders = document.querySelectorAll('[data-translate-placeholder]');
    placeholders.forEach(element => {
        const key = element.getAttribute('data-translate-placeholder');
        if (translations[currentLanguage] && translations[currentLanguage][key]) {
            element.placeholder = translations[currentLanguage][key];
        }
    });
}

// Initialize language on page load
function initializeLanguage() {
    // Get saved language or default to English
    const savedLanguage = localStorage.getItem('bbc_chatbot_language') || 'en';
    currentLanguage = savedLanguage;
    
    // Set select value
    const languageSelect = document.getElementById('languageSelect');
    if (languageSelect) {
        languageSelect.value = currentLanguage;
    }
    
    // Apply language
    changeLanguage();
}

// Auto-detect browser language
function detectBrowserLanguage() {
    const browserLang = navigator.language.substring(0, 2);
    if (translations[browserLang]) {
        currentLanguage = browserLang;
        const languageSelect = document.getElementById('languageSelect');
        if (languageSelect) {
            languageSelect.value = currentLanguage;
        }
    }
}

// Export for use in other scripts
window.translations = translations;
window.currentLanguage = currentLanguage;
window.changeLanguage = changeLanguage;
window.updateTranslations = updateTranslations;
window.initializeLanguage = initializeLanguage;