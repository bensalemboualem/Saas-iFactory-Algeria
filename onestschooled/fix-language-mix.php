<?php
/**
 * BBC School Algeria - Correction Simple de la Cohérence Linguistique
 * Version standalone pour résoudre le mélange des langues
 */

echo "🌍 === BBC SCHOOL ALGERIA - CORRECTION COHÉRENCE LINGUISTIQUE ===\n\n";

try {
    // Configuration de base de données
    $host = 'localhost';
    $dbname = 'onest_school';
    $username = 'root';
    $password = '';
    
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8mb4", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    echo "📊 Connexion à la base de données réussie\n\n";

    // 1. CORRECTION DES LANGUES DANS LA BASE
    echo "🌐 1. Configuration des langues...\n";
    
    $languages = [
        ['code' => 'en', 'name' => 'English', 'direction' => 'ltr'],
        ['code' => 'fr', 'name' => 'Français', 'direction' => 'ltr'],
        ['code' => 'ar', 'name' => 'العربية', 'direction' => 'rtl']
    ];
    
    foreach ($languages as $lang) {
        // Vérifier si la langue existe
        $stmt = $pdo->prepare("SELECT id FROM languages WHERE code = ?");
        $stmt->execute([$lang['code']]);
        
        if (!$stmt->fetch()) {
            // Créer la langue
            $stmt = $pdo->prepare("INSERT INTO languages (code, name, direction, status, created_at, updated_at) VALUES (?, ?, ?, 1, NOW(), NOW())");
            $stmt->execute([$lang['code'], $lang['name'], $lang['direction']]);
            echo "   ✅ Langue {$lang['code']} créée\n";
        } else {
            // Mettre à jour
            $stmt = $pdo->prepare("UPDATE languages SET name = ?, direction = ?, updated_at = NOW() WHERE code = ?");
            $stmt->execute([$lang['name'], $lang['direction'], $lang['code']]);
            echo "   ✅ Langue {$lang['code']} mise à jour\n";
        }
    }

    // 2. TRADUCTIONS COMPLÈTES POUR LES SECTIONS
    echo "\n📝 2. Mise à jour des traductions de sections...\n";
    
    $sectionTranslations = [
        'en' => [
            'Home' => 'Home',
            'About' => 'About',
            'Courses' => 'Courses',
            'Admissions' => 'Admissions',
            'Contact' => 'Contact',
            'News' => 'News',
            'Gallery' => 'Gallery',
            'Our Mission' => 'Our Mission',
            'Why Choose Us' => 'Why Choose Us',
            'Our Teachers' => 'Our Teachers',
            'Student Life' => 'Student Life',
            'Infrastructure' => 'Infrastructure',
            'Welcome to BBC School Algeria' => 'Welcome to BBC School Algeria',
            'Excellence in Education Since 2009' => 'Excellence in Education Since 2009',
            'Bilingual Education' => 'Bilingual Education',
            'Qualified Teachers' => 'Qualified Teachers',
            'Success Rate' => 'Success Rate',
            'Students' => 'Students',
            'Years of Experience' => 'Years of Experience'
        ],
        'fr' => [
            'Home' => 'Accueil',
            'About' => 'À Propos',
            'Courses' => 'Cours',
            'Admissions' => 'Admissions',
            'Contact' => 'Contact',
            'News' => 'Actualités',
            'Gallery' => 'Galerie',
            'Our Mission' => 'Notre Mission',
            'Why Choose Us' => 'Pourquoi Nous Choisir',
            'Our Teachers' => 'Nos Enseignants',
            'Student Life' => 'Vie Étudiante',
            'Infrastructure' => 'Infrastructure',
            'Welcome to BBC School Algeria' => 'Bienvenue à BBC School Algeria',
            'Excellence in Education Since 2009' => 'Excellence en Éducation Depuis 2009',
            'Bilingual Education' => 'Éducation Bilingue',
            'Qualified Teachers' => 'Enseignants Qualifiés',
            'Success Rate' => 'Taux de Réussite',
            'Students' => 'Étudiants',
            'Years of Experience' => 'Années d\'Expérience'
        ],
        'ar' => [
            'Home' => 'الرئيسية',
            'About' => 'حول المدرسة',
            'Courses' => 'الدورات',
            'Admissions' => 'القبول',
            'Contact' => 'اتصل بنا',
            'News' => 'الأخبار',
            'Gallery' => 'المعرض',
            'Our Mission' => 'مهمتنا',
            'Why Choose Us' => 'لماذا تختارنا',
            'Our Teachers' => 'معلمونا',
            'Student Life' => 'حياة الطلاب',
            'Infrastructure' => 'البنية التحتية',
            'Welcome to BBC School Algeria' => 'مرحباً بكم في مدرسة بي بي سي الجزائر',
            'Excellence in Education Since 2009' => 'التميز في التعليم منذ 2009',
            'Bilingual Education' => 'التعليم ثنائي اللغة',
            'Qualified Teachers' => 'معلمون مؤهلون',
            'Success Rate' => 'معدل النجاح',
            'Students' => 'طلاب',
            'Years of Experience' => 'سنوات من الخبرة'
        ]
    ];

    foreach ($sectionTranslations as $lang => $translations) {
        echo "   → Mise à jour des sections en {$lang}...\n";
        
        foreach ($translations as $key => $value) {
            // Vérifier si la section existe
            $stmt = $pdo->prepare("SELECT id FROM sections WHERE name = ? AND lang = ?");
            $stmt->execute([$key, $lang]);
            
            if ($stmt->fetch()) {
                // Mettre à jour
                $stmt = $pdo->prepare("UPDATE sections SET value = ?, updated_at = NOW() WHERE name = ? AND lang = ?");
                $stmt->execute([$value, $key, $lang]);
            } else {
                // Créer
                $stmt = $pdo->prepare("INSERT INTO sections (name, value, lang, created_at, updated_at) VALUES (?, ?, ?, NOW(), NOW())");
                $stmt->execute([$key, $value, $lang]);
            }
        }
        echo "     ✅ {$lang} - " . count($translations) . " traductions mises à jour\n";
    }

    // 3. CRÉATION DU SYSTÈME JAVASCRIPT MULTILINGUE
    echo "\n📱 3. Création du système JavaScript multilingue...\n";
    
    $jsContent = '// BBC School Algeria - Système Multilingue Cohérent
document.addEventListener("DOMContentLoaded", function() {
    
    // Configuration des langues
    const languageConfig = {
        en: { name: "English", direction: "ltr", flag: "🇬🇧" },
        fr: { name: "Français", direction: "ltr", flag: "🇫🇷" },
        ar: { name: "العربية", direction: "rtl", flag: "🇩🇿" }
    };
    
    // Traductions pour éléments dynamiques
    const translations = {
        en: {
            "Accueil": "Home",
            "À Propos": "About", 
            "Cours": "Courses",
            "Admissions": "Admissions",
            "Contact": "Contact",
            "Actualités": "News",
            "Galerie": "Gallery",
            "Bienvenue à BBC School Algeria": "Welcome to BBC School Algeria",
            "Excellence en Éducation Depuis 2009": "Excellence in Education Since 2009",
            "Éducation Bilingue": "Bilingual Education",
            "Enseignants Qualifiés": "Qualified Teachers",
            "Taux de Réussite": "Success Rate",
            "Étudiants": "Students",
            "Années d\'Expérience": "Years of Experience"
        },
        fr: {
            "Home": "Accueil",
            "About": "À Propos",
            "Courses": "Cours", 
            "Admissions": "Admissions",
            "Contact": "Contact",
            "News": "Actualités",
            "Gallery": "Galerie",
            "Welcome to BBC School Algeria": "Bienvenue à BBC School Algeria",
            "Excellence in Education Since 2009": "Excellence en Éducation Depuis 2009",
            "Bilingual Education": "Éducation Bilingue",
            "Qualified Teachers": "Enseignants Qualifiés",
            "Success Rate": "Taux de Réussite",
            "Students": "Étudiants",
            "Years of Experience": "Années d\'Expérience"
        },
        ar: {
            "Home": "الرئيسية",
            "Accueil": "الرئيسية",
            "About": "حول المدرسة",
            "À Propos": "حول المدرسة",
            "Courses": "الدورات",
            "Cours": "الدورات",
            "Admissions": "القبول",
            "Contact": "اتصل بنا",
            "News": "الأخبار",
            "Actualités": "الأخبار",
            "Gallery": "المعرض",
            "Galerie": "المعرض",
            "Welcome to BBC School Algeria": "مرحباً بكم في مدرسة بي بي سي الجزائر",
            "Bienvenue à BBC School Algeria": "مرحباً بكم في مدرسة بي بي سي الجزائر",
            "Excellence in Education Since 2009": "التميز في التعليم منذ 2009",
            "Excellence en Éducation Depuis 2009": "التميز في التعليم منذ 2009",
            "Bilingual Education": "التعليم ثنائي اللغة",
            "Éducation Bilingue": "التعليم ثنائي اللغة",
            "Qualified Teachers": "معلمون مؤهلون",
            "Enseignants Qualifiés": "معلمون مؤهلون",
            "Success Rate": "معدل النجاح",
            "Taux de Réussite": "معدل النجاح",
            "Students": "طلاب",
            "Étudiants": "طلاب",
            "Years of Experience": "سنوات من الخبرة",
            "Années d\'Expérience": "سنوات من الخبرة"
        }
    };
    
    // Obtenir la langue actuelle
    function getCurrentLanguage() {
        const urlParams = new URLSearchParams(window.location.search);
        const langFromUrl = urlParams.get("lang");
        if (langFromUrl && languageConfig[langFromUrl]) {
            localStorage.setItem("bbc_current_language", langFromUrl);
            return langFromUrl;
        }
        return localStorage.getItem("bbc_current_language") || "fr";
    }
    
    // Appliquer les traductions
    function applyTranslations() {
        const currentLang = getCurrentLanguage();
        const langTranslations = translations[currentLang];
        
        if (!langTranslations) return;
        
        // Traduire les éléments de navigation
        document.querySelectorAll(".navbar-nav a, .nav-link").forEach(link => {
            const text = link.textContent.trim();
            if (langTranslations[text]) {
                link.textContent = langTranslations[text];
            }
        });
        
        // Traduire les titres principaux
        document.querySelectorAll("h1, h2, h3, .hero-title, .section-title").forEach(element => {
            const text = element.textContent.trim();
            if (langTranslations[text]) {
                element.textContent = langTranslations[text];
            }
        });
        
        // Traduire les textes courts
        document.querySelectorAll("span, .badge, .btn, .card-title").forEach(element => {
            if (element.children.length === 0) {
                const text = element.textContent.trim();
                if (langTranslations[text]) {
                    element.textContent = langTranslations[text];
                }
            }
        });
        
        console.log(`🌍 Traductions appliquées: ${currentLang}`);
    }
    
    // Appliquer la direction RTL/LTR
    function applyDirection() {
        const currentLang = getCurrentLanguage();
        const config = languageConfig[currentLang];
        
        if (config) {
            document.documentElement.setAttribute("lang", currentLang);
            document.documentElement.setAttribute("dir", config.direction);
            
            if (config.direction === "rtl") {
                document.body.classList.add("rtl", "arabic-layout");
                document.body.classList.remove("ltr");
            } else {
                document.body.classList.add("ltr");
                document.body.classList.remove("rtl", "arabic-layout");
            }
        }
    }
    
    // Créer le sélecteur de langue
    function createLanguageSwitcher() {
        const switcher = document.createElement("div");
        switcher.className = "bbc-language-switcher";
        switcher.style.cssText = `
            position: fixed;
            top: 20px;
            left: 20px;
            z-index: 9999;
            background: white;
            border-radius: 25px;
            padding: 5px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            display: flex;
            gap: 5px;
        `;
        
        Object.entries(languageConfig).forEach(([code, config]) => {
            const button = document.createElement("button");
            button.textContent = config.flag;
            button.title = config.name;
            button.style.cssText = `
                border: none;
                background: ${getCurrentLanguage() === code ? "#392C7D" : "transparent"};
                color: ${getCurrentLanguage() === code ? "white" : "#333"};
                padding: 8px 12px;
                border-radius: 20px;
                cursor: pointer;
                font-size: 16px;
                transition: all 0.3s ease;
            `;
            
            button.addEventListener("click", () => {
                const url = new URL(window.location);
                url.searchParams.set("lang", code);
                window.location.href = url.toString();
            });
            
            switcher.appendChild(button);
        });
        
        document.body.appendChild(switcher);
    }
    
    // Initialisation
    function initializeLanguageSystem() {
        applyDirection();
        setTimeout(() => {
            applyTranslations();
        }, 500);
        createLanguageSwitcher();
        
        console.log("🌍 Système multilingue initialisé");
    }
    
    // Démarrage
    initializeLanguageSystem();
    
    // Reappliquer après chargement complet
    window.addEventListener("load", () => {
        setTimeout(() => {
            applyTranslations();
        }, 1000);
    });
});';

    file_put_contents('public/js/bbc-language-fix.js', $jsContent);
    echo "   ✅ Fichier JavaScript multilingue créé\n";

    // 4. CSS POUR RTL
    echo "\n🎨 4. Création du CSS RTL...\n";
    
    $cssContent = '/* BBC School Algeria - Support RTL */
.rtl {
    direction: rtl !important;
    text-align: right !important;
}

.rtl .navbar-nav {
    flex-direction: row-reverse !important;
}

.rtl .navbar-brand {
    margin-left: auto !important;
    margin-right: 0 !important;
}

.rtl .text-left {
    text-align: right !important;
}

.rtl .text-right {
    text-align: left !important;
}

.rtl .float-left {
    float: right !important;
}

.rtl .float-right {
    float: left !important;
}

.arabic-layout {
    font-family: "Arial", "Tahoma", "Segoe UI", sans-serif !important;
}

.arabic-layout h1, .arabic-layout h2, .arabic-layout h3 {
    font-weight: bold !important;
    line-height: 1.8 !important;
}

.bbc-language-switcher button:hover {
    background: #FF5170 !important;
    color: white !important;
    transform: scale(1.1);
}

/* Navigation responsive RTL */
@media (max-width: 768px) {
    .rtl .navbar-toggler {
        margin-left: 0 !important;
        margin-right: auto !important;
    }
}';

    file_put_contents('public/css/bbc-language-fix.css', $cssContent);
    echo "   ✅ Fichier CSS RTL créé\n";

    // 5. STATISTIQUES FINALES
    echo "\n📊 5. Vérification finale...\n";
    
    $stmt = $pdo->query("SELECT code, name FROM languages ORDER BY code");
    $languages = $stmt->fetchAll(PDO::FETCH_ASSOC);
    echo "   Langues configurées :\n";
    foreach ($languages as $lang) {
        echo "   → {$lang['code']}: {$lang['name']}\n";
    }
    
    $stmt = $pdo->query("SELECT lang, COUNT(*) as total FROM sections GROUP BY lang ORDER BY lang");
    $sections = $stmt->fetchAll(PDO::FETCH_ASSOC);
    echo "\n   Sections traduites :\n";
    foreach ($sections as $section) {
        echo "   → {$section['lang']}: {$section['total']} sections\n";
    }

    echo "\n✅ === CORRECTION COHÉRENCE LINGUISTIQUE TERMINÉE ===\n";
    echo "🌍 Résultats :\n";
    echo "   ✅ Base de données: Langues et traductions mises à jour\n";
    echo "   ✅ JavaScript: Système multilingue cohérent\n";
    echo "   ✅ CSS: Support RTL pour l'arabe\n";
    echo "   ✅ Interface: Sélecteur de langue intégré\n\n";
    
    echo "📋 INSTRUCTIONS POUR FINALISER :\n";
    echo "1. Ajouter ces lignes au fichier master.blade.php :\n";
    echo "   <link rel=\"stylesheet\" href=\"{{ asset('css/bbc-language-fix.css') }}\">\n";
    echo "   <script src=\"{{ asset('js/bbc-language-fix.js') }}\"></script>\n\n";
    
    echo "🌐 URLs de test :\n";
    echo "   🇫🇷 Français: http://localhost/onestschooled-test/public?lang=fr\n";
    echo "   🇬🇧 Anglais: http://localhost/onestschooled-test/public?lang=en\n";
    echo "   🇩🇿 Arabe: http://localhost/onestschooled-test/public?lang=ar\n\n";
    
    echo "🎓 BBC School Algeria - Mélange des langues corrigé !\n";

} catch (Exception $e) {
    echo "❌ Erreur : " . $e->getMessage() . "\n";
}
?>