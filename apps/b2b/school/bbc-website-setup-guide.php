<?php

/**
 * BBC School Algeria - Configuration via Module Website Setup OnestSchool
 * Guide d'utilisation du module intégré
 */

require_once __DIR__ . '/vendor/autoload.php';
$app = require_once __DIR__ . '/bootstrap/app.php';
$app->make('Illuminate\Contracts\Console\Kernel')->bootstrap();

use Illuminate\Support\Facades\DB;

echo "🌐 BBC SCHOOL ALGERIA - CONFIGURATION MODULE WEBSITE SETUP\n";
echo "=========================================================\n\n";

echo "📋 GUIDE D'UTILISATION DU MODULE WEBSITE SETUP ONESTSCHOOL\n";
echo "==========================================================\n\n";

// 1. VÉRIFICATION DE L'ACCÈS ADMIN
echo "🔐 ÉTAPE 1 : ACCÈS À L'ADMINISTRATION\n";
echo "====================================\n";
echo "   🌐 URL Admin : http://localhost/onestschooled-test/public/login\n";
echo "   📧 Email : admin@onestschool.com (ou votre email admin)\n";
echo "   🔑 Mot de passe : [votre mot de passe admin]\n\n";

// 2. NAVIGATION VERS WEBSITE SETUP
echo "🧭 ÉTAPE 2 : NAVIGATION VERS WEBSITE SETUP\n";
echo "==========================================\n";
echo "   1. Se connecter à l'administration OnestSchool\n";
echo "   2. Aller dans le menu 'Website Setup' ou 'Configuration Site'\n";
echo "   3. Vous verrez les sous-modules :\n";
echo "      📝 Sections (Page Sections)\n";
echo "      🖼️  Sliders \n";
echo "      📊 Compteurs (Counters)\n";
echo "      📰 Actualités (News)\n";
echo "      📅 Événements (Events)\n";
echo "      🖼️  Galerie (Gallery)\n";
echo "      📄 Pages\n";
echo "      📞 Contact Info\n\n";

// 3. CONFIGURATION DES SECTIONS BBC SCHOOL
echo "📝 ÉTAPE 3 : CONFIGURATION DES SECTIONS BBC SCHOOL\n";
echo "=================================================\n";

try {
    // Lister les sections disponibles
    $sections = DB::table('sections')
        ->join('section_translates', 'sections.id', '=', 'section_translates.section_id')
        ->where('section_translates.locale', 'fr')
        ->select('sections.key', 'section_translates.name', 'sections.id')
        ->orderBy('sections.key')
        ->get();
    
    echo "   📋 SECTIONS DISPONIBLES POUR BBC SCHOOL :\n";
    foreach ($sections as $section) {
        $editUrl = "http://localhost/onestschooled-test/public/page-sections/edit/{$section->id}";
        echo "      ✅ {$section->key} : {$section->name}\n";
        echo "         🔗 URL Édition : $editUrl\n";
    }
} catch (Exception $e) {
    echo "   ❌ Erreur accès sections: " . $e->getMessage() . "\n";
}

echo "\n📋 SECTIONS À PERSONNALISER POUR BBC SCHOOL :\n";
$bbcSections = [
    'statement' => 'Excellence Éducative BBC School Algeria',
    'study_at' => 'Pourquoi Étudier à BBC School Algeria ?',
    'explore' => 'Explorez BBC School Algeria',
    'why_choose_us' => 'Pourquoi Choisir BBC School Algeria ?',
    'coming_up' => 'Événements à Venir',
    'news' => 'Actualités BBC School',
    'our_gallery' => 'Notre Galerie',
    'our_teachers' => 'Notre Équipe Pédagogique'
];

foreach ($bbcSections as $key => $name) {
    echo "   📝 $key → $name\n";
}

// 4. CONFIGURATION DES SLIDERS
echo "\n🖼️  ÉTAPE 4 : CONFIGURATION DES SLIDERS BBC SCHOOL\n";
echo "================================================\n";
echo "   🌐 URL Sliders : http://localhost/onestschooled-test/public/slider\n";
echo "   \n   📋 SLIDERS À CRÉER/MODIFIER :\n";
echo "      1. 'Bienvenue à BBC School Algeria'\n";
echo "         - Description : Excellence éducative bilingue français-arabe\n";
echo "         - Image : Photo de l'école ou étudiants\n";
echo "      \n";
echo "      2. 'Préparation BEM & BAC'\n";
echo "         - Description : Accompagnement personnalisé pour réussir\n";
echo "         - Image : Étudiants en classe ou laboratoire\n";
echo "      \n";
echo "      3. 'Infrastructure Moderne'\n";
echo "         - Description : Laboratoires, bibliothèque, salles équipées\n";
echo "         - Image : Vue des installations\n\n";

// 5. GESTION DES COMPTEURS
echo "📊 ÉTAPE 5 : CONFIGURATION DES COMPTEURS\n";
echo "========================================\n";
echo "   🌐 URL Compteurs : http://localhost/onestschooled-test/public/counter\n";

try {
    $counters = DB::table('counters')
        ->join('counter_translates', 'counters.id', '=', 'counter_translates.counter_id')
        ->where('counter_translates.locale', 'fr')
        ->select('counter_translates.name', 'counter_translates.total_count', 'counters.id')
        ->get();
    
    echo "   \n   📊 COMPTEURS ACTUELS :\n";
    foreach ($counters as $counter) {
        $editUrl = "http://localhost/onestschooled-test/public/counter/edit/{$counter->id}";
        echo "      ✅ {$counter->name} : {$counter->total_count}\n";
        echo "         🔗 URL Édition : $editUrl\n";
    }
} catch (Exception $e) {
    echo "   ❌ Erreur accès compteurs: " . $e->getMessage() . "\n";
}

// 6. GESTION DES ACTUALITÉS
echo "\n📰 ÉTAPE 6 : GESTION DES ACTUALITÉS BBC SCHOOL\n";
echo "==============================================\n";
echo "   🌐 URL Actualités : http://localhost/onestschooled-test/public/admin-news\n";

try {
    $news = DB::table('news')
        ->join('news_translates', 'news.id', '=', 'news_translates.news_id')
        ->where('news_translates.locale', 'fr')
        ->select('news_translates.title', 'news.date', 'news.id', 'news.status')
        ->orderBy('news.date', 'desc')
        ->limit(5)
        ->get();
    
    echo "   \n   📰 DERNIÈRES ACTUALITÉS :\n";
    foreach ($news as $article) {
        $status = $article->status == 1 ? '✅' : '❌';
        $editUrl = "http://localhost/onestschooled-test/public/admin-news/edit/{$article->id}";
        echo "      $status [{$article->date}] {$article->title}\n";
        echo "         🔗 URL Édition : $editUrl\n";
    }
} catch (Exception $e) {
    echo "   ❌ Erreur accès actualités: " . $e->getMessage() . "\n";
}

// 7. GESTION DE LA GALERIE
echo "\n🖼️  ÉTAPE 7 : GESTION DE LA GALERIE BBC SCHOOL\n";
echo "==============================================\n";
echo "   🌐 URL Galerie : http://localhost/onestschooled-test/public/gallery\n";
echo "   🌐 URL Catégories : http://localhost/onestschooled-test/public/gallery-category\n";
echo "   \n   📋 CATÉGORIES À CRÉER :\n";
echo "      📚 Vie Scolaire\n";
echo "      🏫 Infrastructure\n";
echo "      🎓 Examens & Remises de Prix\n";
echo "      🚌 Transport & Cantine\n";
echo "      🎨 Activités Parascolaires\n";
echo "      👨‍🏫 Équipe Pédagogique\n\n";

// 8. CONFIGURATION DES PAGES
echo "📄 ÉTAPE 8 : GESTION DES PAGES BBC SCHOOL\n";
echo "=========================================\n";
echo "   🌐 URL Pages : http://localhost/onestschooled-test/public/page\n";
echo "   \n   📋 PAGES À CRÉER/MODIFIER :\n";
echo "      📖 À Propos de BBC School Algeria\n";
echo "      🎓 Programmes Éducatifs\n";
echo "      🚌 Transport Scolaire\n";
echo "      🍽️ Cantine & Restauration\n";
echo "      📞 Contact & Admission\n";
echo "      💰 Frais de Scolarité\n\n";

// 9. CONTACT & INFORMATIONS
echo "📞 ÉTAPE 9 : INFORMATIONS DE CONTACT\n";
echo "===================================\n";
echo "   🌐 URL Contact Info : http://localhost/onestschooled-test/public/contact-info\n";
echo "   \n   📋 INFORMATIONS À RENSEIGNER :\n";
echo "      📧 Email : contact@bbcschool.dz\n";
echo "      📞 Téléphone : +213 XX XX XX XX\n";
echo "      📍 Adresse : [Adresse de BBC School Algeria]\n";
echo "      🌐 Site Web : www.bbcschool.dz\n";
echo "      📘 Facebook : /bbcschoolalgeria\n";
echo "      📷 Instagram : @bbcschoolalgeria\n\n";

// 10. INTÉGRATION DU CHATBOT
echo "🤖 ÉTAPE 10 : INTÉGRATION DU CHATBOT IA\n";
echo "======================================\n";
echo "   ✅ Le chatbot IA BBC School est déjà intégré dans :\n";
echo "      📁 resources/views/frontend/partials/bbc-ai-chatbot.blade.php\n";
echo "      📁 resources/views/frontend/master.blade.php\n";
echo "   \n   🎨 Styles personnalisés BBC School :\n";
echo "      📁 public/css/bbc-style.css\n";
echo "      📁 public/js/bbc-script.js\n\n";

// 11. CHECKLIST FINAL
echo "✅ CHECKLIST FINAL BBC SCHOOL ALGERIA\n";
echo "====================================\n";
echo "   🔲 1. Se connecter à l'administration OnestSchool\n";
echo "   🔲 2. Modifier les sections avec le contenu BBC School\n";
echo "   🔲 3. Créer/modifier les sliders avec images BBC School\n";
echo "   🔲 4. Vérifier les compteurs (étudiants, enseignants, etc.)\n";
echo "   🔲 5. Ajouter des actualités BBC School\n";
echo "   🔲 6. Créer les catégories de galerie\n";
echo "   🔲 7. Uploader les photos dans la galerie\n";
echo "   🔲 8. Créer les pages informatives\n";
echo "   🔲 9. Renseigner les informations de contact\n";
echo "   🔲 10. Tester le chatbot IA sur le site\n\n";

// 12. LIENS DIRECTS
echo "🔗 LIENS D'ACCÈS RAPIDE\n";
echo "======================\n";
echo "   🏠 Site Public : http://localhost/onestschooled-test/public\n";
echo "   🔐 Administration : http://localhost/onestschooled-test/public/login\n";
echo "   📝 Page Sections : http://localhost/onestschooled-test/public/page-sections\n";
echo "   🖼️  Sliders : http://localhost/onestschooled-test/public/slider\n";
echo "   📊 Compteurs : http://localhost/onestschooled-test/public/counter\n";
echo "   📰 Actualités : http://localhost/onestschooled-test/public/admin-news\n";
echo "   🖼️  Galerie : http://localhost/onestschooled-test/public/gallery\n";
echo "   📄 Pages : http://localhost/onestschooled-test/public/page\n";
echo "   📞 Contact Info : http://localhost/onestschooled-test/public/contact-info\n\n";

echo "🎓 BBC SCHOOL ALGERIA - PRÊT POUR LA PERSONNALISATION !\n";
echo "Utilisez l'interface d'administration OnestSchool pour personnaliser votre site ! 🇩🇿\n";

?>