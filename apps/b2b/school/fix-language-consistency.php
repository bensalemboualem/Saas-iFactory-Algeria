<?php
/**
 * BBC School Algeria - Correction de la cohérence linguistique
 * Résout le problème de mélange des langues (arabe, français, anglais)
 */

require_once 'bootstrap/app.php';

echo "🌍 === BBC SCHOOL ALGERIA - CORRECTION COHÉRENCE LINGUISTIQUE ===\n\n";

try {
    // Configuration de la base de données
    $app = require_once 'bootstrap/app.php';
    $kernel = $app->make(Illuminate\Contracts\Http\Kernel::class);
    $response = $kernel->handle(
        $request = Illuminate\Http\Request::capture()
    );

    // 1. CORRECTIONS DES TRADUCTIONS DE SECTIONS
    echo "📝 1. Mise à jour des traductions de sections...\n";
    
    $sectionTranslations = [
        // Anglais
        'en' => [
            'Home' => 'Home',
            'About' => 'About',
            'Courses' => 'Courses',
            'Admissions' => 'Admissions',
            'Contact' => 'Contact',
            'News' => 'News',
            'Gallery' => 'Gallery',
            'Academic Results' => 'Academic Results',
            'Our Mission' => 'Our Mission',
            'Why Choose Us' => 'Why Choose Us',
            'Our Teachers' => 'Our Teachers',
            'Student Life' => 'Student Life',
            'Transportation' => 'Transportation',
            'Cafeteria' => 'Cafeteria',
            'Infrastructure' => 'Infrastructure',
            'Primary Education' => 'Primary Education',
            'Middle School' => 'Middle School',
            'High School' => 'High School',
            'Bilingual Program' => 'Bilingual Program',
            'Scientific Program' => 'Scientific Program',
            'Literary Program' => 'Literary Program',
            'Registration Process' => 'Registration Process',
            'Required Documents' => 'Required Documents',
            'Fees Structure' => 'Fees Structure',
            'Scholarships' => 'Scholarships',
            'Address' => 'Address',
            'Phone' => 'Phone',
            'Email' => 'Email',
            'Office Hours' => 'Office Hours',
            'Welcome to BBC School Algeria' => 'Welcome to BBC School Algeria',
            'Excellence in Education Since 2009' => 'Excellence in Education Since 2009',
            'Bilingual Education' => 'Bilingual Education',
            'French & Arabic' => 'French & Arabic',
            'Qualified Teachers' => 'Qualified Teachers',
            'Success Rate' => 'Success Rate',
            'Students' => 'Students',
            'Years of Experience' => 'Years of Experience'
        ],
        
        // Français
        'fr' => [
            'Home' => 'Accueil',
            'About' => 'À Propos',
            'Courses' => 'Cours',
            'Admissions' => 'Admissions',
            'Contact' => 'Contact',
            'News' => 'Actualités',
            'Gallery' => 'Galerie',
            'Academic Results' => 'Résultats Académiques',
            'Our Mission' => 'Notre Mission',
            'Why Choose Us' => 'Pourquoi Nous Choisir',
            'Our Teachers' => 'Nos Enseignants',
            'Student Life' => 'Vie Étudiante',
            'Transportation' => 'Transport',
            'Cafeteria' => 'Cafétéria',
            'Infrastructure' => 'Infrastructure',
            'Primary Education' => 'Enseignement Primaire',
            'Middle School' => 'Collège',
            'High School' => 'Lycée',
            'Bilingual Program' => 'Programme Bilingue',
            'Scientific Program' => 'Programme Scientifique',
            'Literary Program' => 'Programme Littéraire',
            'Registration Process' => 'Processus d\'Inscription',
            'Required Documents' => 'Documents Requis',
            'Fees Structure' => 'Structure des Frais',
            'Scholarships' => 'Bourses d\'Études',
            'Address' => 'Adresse',
            'Phone' => 'Téléphone',
            'Email' => 'Email',
            'Office Hours' => 'Heures de Bureau',
            'Welcome to BBC School Algeria' => 'Bienvenue à BBC School Algeria',
            'Excellence in Education Since 2009' => 'Excellence en Éducation Depuis 2009',
            'Bilingual Education' => 'Éducation Bilingue',
            'French & Arabic' => 'Français & Arabe',
            'Qualified Teachers' => 'Enseignants Qualifiés',
            'Success Rate' => 'Taux de Réussite',
            'Students' => 'Étudiants',
            'Years of Experience' => 'Années d\'Expérience'
        ],
        
        // Arabe
        'ar' => [
            'Home' => 'الرئيسية',
            'About' => 'حول المدرسة',
            'Courses' => 'الدورات',
            'Admissions' => 'القبول',
            'Contact' => 'اتصل بنا',
            'News' => 'الأخبار',
            'Gallery' => 'المعرض',
            'Academic Results' => 'النتائج الأكاديمية',
            'Our Mission' => 'مهمتنا',
            'Why Choose Us' => 'لماذا تختارنا',
            'Our Teachers' => 'معلمونا',
            'Student Life' => 'حياة الطلاب',
            'Transportation' => 'النقل',
            'Cafeteria' => 'المطعم',
            'Infrastructure' => 'البنية التحتية',
            'Primary Education' => 'التعليم الابتدائي',
            'Middle School' => 'المتوسط',
            'High School' => 'الثانوي',
            'Bilingual Program' => 'البرنامج ثنائي اللغة',
            'Scientific Program' => 'البرنامج العلمي',
            'Literary Program' => 'البرنامج الأدبي',
            'Registration Process' => 'عملية التسجيل',
            'Required Documents' => 'الوثائق المطلوبة',
            'Fees Structure' => 'هيكل الرسوم',
            'Scholarships' => 'المنح الدراسية',
            'Address' => 'العنوان',
            'Phone' => 'الهاتف',
            'Email' => 'البريد الإلكتروني',
            'Office Hours' => 'ساعات العمل',
            'Welcome to BBC School Algeria' => 'مرحباً بكم في مدرسة بي بي سي الجزائر',
            'Excellence in Education Since 2009' => 'التميز في التعليم منذ 2009',
            'Bilingual Education' => 'التعليم ثنائي اللغة',
            'French & Arabic' => 'الفرنسية والعربية',
            'Qualified Teachers' => 'معلمون مؤهلون',
            'Success Rate' => 'معدل النجاح',
            'Students' => 'طلاب',
            'Years of Experience' => 'سنوات من الخبرة'
        ]
    ];

    // Mise à jour de la table sections pour chaque langue
    foreach ($sectionTranslations as $lang => $translations) {
        echo "   → Mise à jour des sections en {$lang}...\n";
        
        // Vérifier si la langue existe
        $languageExists = DB::table('languages')->where('code', $lang)->exists();
        
        if (!$languageExists) {
            // Créer la langue si elle n'existe pas
            $languageNames = [
                'en' => 'English',
                'fr' => 'Français', 
                'ar' => 'العربية'
            ];
            
            DB::table('languages')->insert([
                'code' => $lang,
                'name' => $languageNames[$lang],
                'direction' => $lang === 'ar' ? 'rtl' : 'ltr',
                'status' => 1,
                'created_at' => now(),
                'updated_at' => now()
            ]);
            echo "     ✅ Langue {$lang} créée\n";
        }
        
        foreach ($translations as $key => $value) {
            try {
                // Vérifier si la section existe déjà
                $existing = DB::table('sections')
                    ->where('name', $key)
                    ->where('lang', $lang)
                    ->first();
                
                if ($existing) {
                    // Mettre à jour
                    DB::table('sections')
                        ->where('name', $key)
                        ->where('lang', $lang)
                        ->update([
                            'value' => $value,
                            'updated_at' => now()
                        ]);
                } else {
                    // Créer nouvelle section
                    DB::table('sections')->insert([
                        'name' => $key,
                        'value' => $value,
                        'lang' => $lang,
                        'created_at' => now(),
                        'updated_at' => now()
                    ]);
                }
            } catch (Exception $e) {
                echo "     ⚠️  Erreur pour {$key}: " . $e->getMessage() . "\n";
            }
        }
        echo "     ✅ {$lang} - " . count($translations) . " traductions mises à jour\n";
    }

    echo "\n📱 2. Mise à jour du JavaScript multilingue...\n";
    
    // 2. MISE À JOUR DU SYSTÈME JAVASCRIPT
    $jsMultilingualContent = '
// BBC School Algeria - Système Multilingue Cohérent
document.addEventListener("DOMContentLoaded", function() {
    
    // Configuration des langues BBC School
    const bbcLanguageConfig = {
        en: {
            name: "English",
            code: "en",
            direction: "ltr",
            flag: "🇬🇧"
        },
        fr: {
            name: "Français", 
            code: "fr",
            direction: "ltr",
            flag: "🇫🇷"
        },
        ar: {
            name: "العربية",
            code: "ar", 
            direction: "rtl",
            flag: "🇩🇿"
        }
    };
    
    // Traductions complètes pour le site
    const bbcTranslations = {
        en: {
            // Navigation
            "Home": "Home",
            "About": "About",
            "Courses": "Courses", 
            "Admissions": "Admissions",
            "Contact": "Contact",
            "News": "News",
            "Gallery": "Gallery",
            
            // Contenu principal
            "Welcome to BBC School Algeria": "Welcome to BBC School Algeria",
            "Excellence in Education Since 2009": "Excellence in Education Since 2009",
            "Bilingual Education": "Bilingual Education",
            "French & Arabic": "French & Arabic",
            "Qualified Teachers": "Qualified Teachers",
            "Success Rate": "Success Rate",
            "Students": "Students",
            "Years of Experience": "Years of Experience",
            
            // Boutons et actions
            "Learn More": "Learn More",
            "Contact Us": "Contact Us",
            "Apply Now": "Apply Now",
            "Read More": "Read More",
            
            // Footer
            "Quick Links": "Quick Links",
            "Contact Information": "Contact Information", 
            "Follow Us": "Follow Us",
            "All Rights Reserved": "All Rights Reserved"
        },
        
        fr: {
            // Navigation
            "Home": "Accueil",
            "About": "À Propos", 
            "Courses": "Cours",
            "Admissions": "Admissions",
            "Contact": "Contact",
            "News": "Actualités",
            "Gallery": "Galerie",
            
            // Contenu principal
            "Welcome to BBC School Algeria": "Bienvenue à BBC School Algeria",
            "Excellence in Education Since 2009": "Excellence en Éducation Depuis 2009",
            "Bilingual Education": "Éducation Bilingue",
            "French & Arabic": "Français & Arabe",
            "Qualified Teachers": "Enseignants Qualifiés",
            "Success Rate": "Taux de Réussite",
            "Students": "Étudiants", 
            "Years of Experience": "Années d\'Expérience",
            
            // Boutons et actions
            "Learn More": "En Savoir Plus",
            "Contact Us": "Nous Contacter",
            "Apply Now": "Postuler Maintenant",
            "Read More": "Lire Plus",
            
            // Footer
            "Quick Links": "Liens Rapides",
            "Contact Information": "Informations de Contact",
            "Follow Us": "Suivez-Nous", 
            "All Rights Reserved": "Tous Droits Réservés"
        },
        
        ar: {
            // Navigation
            "Home": "الرئيسية",
            "About": "حول المدرسة",
            "Courses": "الدورات",
            "Admissions": "القبول", 
            "Contact": "اتصل بنا",
            "News": "الأخبار",
            "Gallery": "المعرض",
            
            // Contenu principal
            "Welcome to BBC School Algeria": "مرحباً بكم في مدرسة بي بي سي الجزائر",
            "Excellence in Education Since 2009": "التميز في التعليم منذ 2009",
            "Bilingual Education": "التعليم ثنائي اللغة",
            "French & Arabic": "الفرنسية والعربية",
            "Qualified Teachers": "معلمون مؤهلون",
            "Success Rate": "معدل النجاح",
            "Students": "طلاب",
            "Years of Experience": "سنوات من الخبرة",
            
            // Boutons et actions
            "Learn More": "اعرف المزيد",
            "Contact Us": "اتصل بنا",
            "Apply Now": "قدم الآن", 
            "Read More": "اقرأ المزيد",
            
            // Footer
            "Quick Links": "روابط سريعة",
            "Contact Information": "معلومات الاتصال",
            "Follow Us": "تابعونا",
            "All Rights Reserved": "جميع الحقوق محفوظة"
        }
    };
    
    // Fonction pour obtenir la langue actuelle
    function getCurrentLanguage() {
        const urlParams = new URLSearchParams(window.location.search);
        const langFromUrl = urlParams.get("lang");
        if (langFromUrl && bbcLanguageConfig[langFromUrl]) {
            localStorage.setItem("bbc_current_language", langFromUrl);
            return langFromUrl;
        }
        
        const langFromStorage = localStorage.getItem("bbc_current_language");
        if (langFromStorage && bbcLanguageConfig[langFromStorage]) {
            return langFromStorage;
        }
        
        return "fr"; // Par défaut français
    }
    
    // Fonction pour appliquer les traductions
    function applyTranslations() {
        const currentLang = getCurrentLanguage();
        const translations = bbcTranslations[currentLang];
        
        if (!translations) return;
        
        // Appliquer les traductions à tous les éléments avec data-translate
        document.querySelectorAll("[data-translate]").forEach(element => {
            const key = element.getAttribute("data-translate");
            if (translations[key]) {
                element.textContent = translations[key];
            }
        });
        
        // Appliquer les traductions par correspondance de texte
        Object.entries(translations).forEach(([key, value]) => {
            // Chercher les éléments contenant le texte original
            const elements = document.querySelectorAll("*");
            elements.forEach(element => {
                // Vérifier les liens de navigation
                if (element.tagName === "A" && element.textContent.trim() === key) {
                    element.textContent = value;
                }
                
                // Vérifier les titres et headers
                if (["H1", "H2", "H3", "H4", "H5", "H6"].includes(element.tagName) && 
                    element.textContent.trim() === key) {
                    element.textContent = value;
                }
                
                // Vérifier les boutons
                if (element.tagName === "BUTTON" && element.textContent.trim() === key) {
                    element.textContent = value;
                }
                
                // Vérifier les spans et divs courts
                if (["SPAN", "DIV", "P"].includes(element.tagName) && 
                    element.textContent.trim() === key &&
                    element.children.length === 0) {
                    element.textContent = value;
                }
            });
        });
        
        console.log(`🌍 Traductions appliquées pour: ${currentLang}`);
    }
    
    // Fonction pour appliquer la direction RTL/LTR
    function applyLanguageDirection() {
        const currentLang = getCurrentLanguage();
        const config = bbcLanguageConfig[currentLang];
        
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
            
            // Mettre à jour le titre de la page
            const titles = {
                en: "BBC School Algeria - Educational Excellence",
                fr: "BBC School Algeria - Excellence Éducative",
                ar: "مدرسة بي بي سي الجزائر - التميز التعليمي"
            };
            
            if (titles[currentLang]) {
                document.title = titles[currentLang];
            }
        }
    }
    
    // Fonction pour créer les boutons de langue
    function createLanguageSwitcher() {
        const languageSwitcher = document.createElement("div");
        languageSwitcher.className = "bbc-language-switcher";
        languageSwitcher.style.cssText = `
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
        
        Object.entries(bbcLanguageConfig).forEach(([code, config]) => {
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
                const currentUrl = new URL(window.location);
                currentUrl.searchParams.set("lang", code);
                window.location.href = currentUrl.toString();
            });
            
            languageSwitcher.appendChild(button);
        });
        
        document.body.appendChild(languageSwitcher);
    }
    
    // Initialisation du système multilingue
    function initializeMultilingualSystem() {
        applyLanguageDirection();
        setTimeout(() => {
            applyTranslations();
        }, 500);
        createLanguageSwitcher();
        
        console.log("🌍 Système multilingue BBC School initialisé");
        console.log("📝 Langue actuelle:", getCurrentLanguage());
    }
    
    // Démarrage automatique
    initializeMultilingualSystem();
    
    // Reappliquer les traductions après chargement complet
    window.addEventListener("load", () => {
        setTimeout(applyTranslations, 1000);
    });
    
});';

    // Écrire le fichier JavaScript multilingue
    file_put_contents(
        'public/js/bbc-multilingual-system.js',
        $jsMultilingualContent
    );
    echo "   ✅ Fichier JavaScript multilingue créé\n";

    echo "\n🎨 3. Mise à jour du template principal...\n";
    
    // 3. MISE À JOUR DU TEMPLATE MASTER
    $masterTemplatePath = 'resources/views/frontend/master.blade.php';
    $currentMasterContent = file_get_contents($masterTemplatePath);
    
    // Ajouter le script multilingue au template
    if (!strpos($currentMasterContent, 'bbc-multilingual-system.js')) {
        $scriptTag = '<script src="{{ asset(\'js/bbc-multilingual-system.js\') }}"></script>';
        
        // Ajouter avant la fermeture du body ou avant le script BBC
        if (strpos($currentMasterContent, 'bbc-script.js')) {
            $newContent = str_replace(
                '<script src="{{ asset(\'js/bbc-script.js\') }}"></script>',
                $scriptTag . "\n" . '<script src="{{ asset(\'js/bbc-script.js\') }}"></script>',
                $currentMasterContent
            );
        } else {
            $newContent = str_replace(
                '</body>',
                $scriptTag . "\n</body>",
                $currentMasterContent
            );
        }
        
        file_put_contents($masterTemplatePath, $newContent);
        echo "   ✅ Script multilingue ajouté au template\n";
    }

    echo "\n💻 4. Correction du CSS pour RTL...\n";
    
    // 4. CSS POUR SUPPORT RTL
    $rtlCSS = '
/* BBC School Algeria - Support RTL pour l\'arabe */
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

.rtl .container,
.rtl .container-fluid {
    direction: rtl !important;
}

.rtl .row {
    direction: rtl !important;
}

.rtl .col,
.rtl [class*="col-"] {
    direction: rtl !important;
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

.rtl .ml-auto {
    margin-left: 0 !important;
    margin-right: auto !important;
}

.rtl .mr-auto {
    margin-right: 0 !important;
    margin-left: auto !important;
}

.rtl .pl-3 {
    padding-left: 0 !important;
    padding-right: 1rem !important;
}

.rtl .pr-3 {
    padding-right: 0 !important;
    padding-left: 1rem !important;
}

/* Boutons de langue */
.bbc-language-switcher {
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif !important;
}

.bbc-language-switcher button:hover {
    background: #FF5170 !important;
    color: white !important;
    transform: scale(1.1);
}

/* Améliorations pour l\'arabe */
.arabic-layout {
    font-family: "Arial", "Tahoma", "Segoe UI", sans-serif !important;
}

.arabic-layout h1,
.arabic-layout h2, 
.arabic-layout h3,
.arabic-layout h4,
.arabic-layout h5,
.arabic-layout h6 {
    font-weight: bold !important;
    line-height: 1.8 !important;
}

.arabic-layout p,
.arabic-layout span,
.arabic-layout div {
    line-height: 1.6 !important;
}

/* Navigation RTL */
.rtl .navbar-toggler {
    margin-left: 0 !important;
    margin-right: auto !important;
}

.rtl .dropdown-menu {
    right: 0 !important;
    left: auto !important;
}
';

    // Écrire le CSS RTL
    file_put_contents('public/css/bbc-rtl.css', $rtlCSS);
    echo "   ✅ CSS RTL créé\n";
    
    // Ajouter le CSS RTL au template s'il n'y est pas déjà
    if (!strpos($currentMasterContent, 'bbc-rtl.css')) {
        $cssLink = '<link rel="stylesheet" href="{{ asset(\'css/bbc-rtl.css\') }}">';
        
        $updatedContent = str_replace(
            '</head>',
            $cssLink . "\n</head>",
            file_get_contents($masterTemplatePath)
        );
        
        file_put_contents($masterTemplatePath, $updatedContent);
        echo "   ✅ CSS RTL ajouté au template\n";
    }

    echo "\n📋 5. Test des langues...\n";
    
    // Vérification des langues dans la base de données
    $languages = DB::table('languages')->get();
    echo "   Langues configurées :\n";
    foreach ($languages as $lang) {
        echo "   → {$lang->code}: {$lang->name} (direction: " . ($lang->direction ?? 'ltr') . ")\n";
    }
    
    // Compter les sections par langue
    $sectionCounts = DB::table('sections')
        ->select('lang', DB::raw('count(*) as total'))
        ->groupBy('lang')
        ->get();
    
    echo "\n   Sections traduites :\n";
    foreach ($sectionCounts as $count) {
        echo "   → {$count->lang}: {$count->total} sections\n";
    }

    echo "\n✅ === CORRECTION COHÉRENCE LINGUISTIQUE TERMINÉE ===\n";
    echo "🌍 Résultats :\n";
    echo "   ✅ Traductions complètes pour EN/FR/AR\n";
    echo "   ✅ Support RTL pour l'arabe\n"; 
    echo "   ✅ Sélecteur de langue intégré\n";
    echo "   ✅ CSS adaptatif pour toutes les langues\n";
    echo "   ✅ Cohérence linguistique assurée\n\n";
    
    echo "🌐 URLs de test :\n";
    echo "   🇫🇷 Français: http://localhost/onestschooled-test/public?lang=fr\n";
    echo "   🇬🇧 Anglais: http://localhost/onestschooled-test/public?lang=en\n";  
    echo "   🇩🇿 Arabe: http://localhost/onestschooled-test/public?lang=ar\n\n";
    
    echo "🎓 BBC School Algeria - Système multilingue parfaitement cohérent !\n";

} catch (Exception $e) {
    echo "❌ Erreur : " . $e->getMessage() . "\n";
    echo "📍 Ligne : " . $e->getLine() . "\n";
    echo "📁 Fichier : " . $e->getFile() . "\n";
}
?>