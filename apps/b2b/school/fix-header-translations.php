<?php
echo "=== Correction des traductions du header BBC School Algeria ===" . PHP_EOL;

try {
    $pdo = new PDO('mysql:host=localhost;dbname=onest_school', 'root', '');
    
    // D'abord, vérifions quelles traductions existent pour le header
    echo "📋 Vérification des traductions existantes..." . PHP_EOL;
    
    $languages = $pdo->query("SELECT * FROM languages WHERE code IN ('en', 'fr', 'ar')")->fetchAll();
    echo "Langues disponibles:" . PHP_EOL;
    foreach($languages as $lang) {
        echo "- {$lang['name']} ({$lang['code']})" . PHP_EOL;
    }
    
    // Définir les traductions pour le header
    $header_translations = [
        'Home' => [
            'en' => 'Home',
            'fr' => 'Accueil',
            'ar' => 'الرئيسية'
        ],
        'About' => [
            'en' => 'About',
            'fr' => 'À Propos',
            'ar' => 'حول'
        ],
        'News' => [
            'en' => 'News',
            'fr' => 'Actualités',
            'ar' => 'أخبار'
        ],
        'Events' => [
            'en' => 'Events',
            'fr' => 'Événements',
            'ar' => 'أحداث'
        ],
        'notices' => [
            'en' => 'Notices',
            'fr' => 'Avis',
            'ar' => 'إشعارات'
        ],
        'Result' => [
            'en' => 'Results',
            'fr' => 'Résultats',
            'ar' => 'النتائج'
        ],
        'contact_us' => [
            'en' => 'Contact',
            'fr' => 'Contact',
            'ar' => 'اتصل بنا'
        ],
        'online_admission' => [
            'en' => 'Online Admission',
            'fr' => 'Inscription en Ligne',
            'ar' => 'التسجيل عبر الإنترنت'
        ],
        'Login' => [
            'en' => 'Login',
            'fr' => 'Connexion',
            'ar' => 'تسجيل الدخول'
        ],
        'Dashboard' => [
            'en' => 'Dashboard',
            'fr' => 'Tableau de Bord',
            'ar' => 'لوحة القيادة'
        ]
    ];
    
    echo PHP_EOL . "🔧 Mise à jour des traductions du header..." . PHP_EOL;
    
    $updated_count = 0;
    
    // Pour chaque terme du header
    foreach($header_translations as $key => $translations) {
        foreach($translations as $locale => $translation) {
            // Vérifier si la traduction existe déjà
            $existing = $pdo->prepare("
                SELECT id FROM translates 
                WHERE locale = ? AND file_name = 'frontend' AND lang_key = ?
            ");
            $existing->execute([$locale, $key]);
            $exists = $existing->fetch();
            
            if($exists) {
                // Mettre à jour
                $update = $pdo->prepare("
                    UPDATE translates 
                    SET lang_value = ?, updated_at = NOW()
                    WHERE locale = ? AND file_name = 'frontend' AND lang_key = ?
                ");
                $update->execute([$translation, $locale, $key]);
                echo "✅ Mis à jour: $key ($locale) = $translation" . PHP_EOL;
            } else {
                // Insérer nouvelle traduction
                $insert = $pdo->prepare("
                    INSERT INTO translates (locale, file_name, lang_key, lang_value, created_at, updated_at)
                    VALUES (?, 'frontend', ?, ?, NOW(), NOW())
                ");
                $insert->execute([$locale, $key, $translation]);
                echo "✅ Ajouté: $key ($locale) = $translation" . PHP_EOL;
            }
            $updated_count++;
        }
    }
    
    echo PHP_EOL . "🎉 $updated_count traductions du header mises à jour !" . PHP_EOL;
    
    // Maintenant, créons un script JavaScript pour mettre à jour le header selon la langue
    $js_script = '
<script>
document.addEventListener("DOMContentLoaded", function() {
    // Traductions du header BBC School Algeria
    const headerTranslations = {
        en: {
            "Home": "Home",
            "About": "About", 
            "News": "News",
            "Events": "Events",
            "Notices": "Notices",
            "Results": "Results",
            "Contact": "Contact",
            "Online Admission": "Online Admission",
            "Login": "Login",
            "Dashboard": "Dashboard"
        },
        fr: {
            "Home": "Accueil",
            "About": "À Propos",
            "News": "Actualités", 
            "Events": "Événements",
            "Notices": "Avis",
            "Results": "Résultats",
            "Contact": "Contact",
            "Online Admission": "Inscription en Ligne",
            "Login": "Connexion",
            "Dashboard": "Tableau de Bord"
        },
        ar: {
            "Home": "الرئيسية",
            "About": "حول",
            "News": "أخبار",
            "Events": "أحداث", 
            "Notices": "إشعارات",
            "Results": "النتائج",
            "Contact": "اتصل بنا",
            "Online Admission": "التسجيل عبر الإنترنت",
            "Login": "تسجيل الدخول",
            "Dashboard": "لوحة القيادة"
        }
    };
    
    // Obtenir la langue actuelle
    const urlParams = new URLSearchParams(window.location.search);
    const currentLang = urlParams.get("lang") || "en";
    
    // Mettre à jour les liens du menu
    if (headerTranslations[currentLang]) {
        const menuLinks = document.querySelectorAll("#mobile-menu a");
        menuLinks.forEach(link => {
            const text = link.textContent.trim();
            for (const [original, translated] of Object.entries(headerTranslations[currentLang])) {
                if (text === original || text.includes(original)) {
                    link.textContent = translated;
                    break;
                }
            }
        });
        
        // Mettre à jour le bouton admission en ligne
        const admissionBtns = document.querySelectorAll("a[href*=\'online-admission\']");
        admissionBtns.forEach(btn => {
            if (headerTranslations[currentLang]["Online Admission"]) {
                btn.textContent = headerTranslations[currentLang]["Online Admission"];
            }
        });
        
        // Mettre à jour login/dashboard
        const loginLinks = document.querySelectorAll("a[href*=\'login\'], a[href*=\'dashboard\']");
        loginLinks.forEach(link => {
            if (link.href.includes("login") && headerTranslations[currentLang]["Login"]) {
                link.textContent = headerTranslations[currentLang]["Login"];
            } else if (link.href.includes("dashboard") && headerTranslations[currentLang]["Dashboard"]) {
                link.textContent = headerTranslations[currentLang]["Dashboard"];
            }
        });
    }
});
</script>';
    
    // Sauvegarder le script
    file_put_contents('C:\xampp\htdocs\onestschooled-test\public\js\header-translations.js', 
        str_replace(['<script>', '</script>'], '', $js_script));
    
    echo "✅ Script JavaScript pour le header créé" . PHP_EOL;
    echo "📁 Fichier: public/js/header-translations.js" . PHP_EOL;
    
    echo PHP_EOL . "📋 Pour tester:" . PHP_EOL;
    echo "- Français: http://localhost/onestschooled-test/public?lang=fr" . PHP_EOL;
    echo "- Anglais: http://localhost/onestschooled-test/public?lang=en" . PHP_EOL;
    echo "- Arabe: http://localhost/onestschooled-test/public?lang=ar" . PHP_EOL;
    
} catch(Exception $e) {
    echo "❌ Erreur: " . $e->getMessage() . PHP_EOL;
}
?>