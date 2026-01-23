<?php
/**
 * SCRIPT AMÉLIORATION ÉCOLE VIRTUELLE
 * BBC School Algeria - OnestSchool
 *
 * Ajoute contenu manquant pour tests complets:
 * - Actualités en arabe
 * - Devoirs (homework)
 * - Annonces (notice boards)
 * - Chauffeurs pour transport
 */

echo "\n========================================\n";
echo "AMÉLIORATION ÉCOLE VIRTUELLE\n";
echo "========================================\n\n";

try {
    $pdo = new PDO('mysql:host=localhost;dbname=onest_school;charset=utf8mb4', 'root', '');
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    echo "✅ Connexion MySQL établie\n\n";

    // ============================================
    // 1. TRADUIRE ACTUALITÉS EN ARABE
    // ============================================

    echo "📰 AJOUT ACTUALITÉS ARABES\n";
    echo "========================================\n";

    // Récupérer les news françaises
    $newsStmt = $pdo->query("SELECT id, news_id FROM news_translates WHERE locale='fr'");
    $frenchNews = $newsStmt->fetchAll(PDO::FETCH_ASSOC);

    $arabicNews = [
        1 => [
            'title' => 'العودة المدرسية 2024-2025: برامج جديدة',
            'description' => 'نبدأ العام الدراسي الجديد ببرامج محدثة ومحتوى تعليمي محسّن لجميع المستويات.'
        ],
        2 => [
            'title' => 'نتائج ممتازة في البكالوريا 2024',
            'description' => 'تفتخر مدرسة BBC بنسبة نجاح 98% في امتحانات البكالوريا 2024. تهانينا لطلابنا!'
        ],
        3 => [
            'title' => 'حافلة مدرسية جديدة مرسيدس سبرينتر',
            'description' => 'توسيع أسطول النقل المدرسي مع حافلة مرسيدس سبرينتر جديدة سعة 24 مقعدًا.'
        ],
        4 => [
            'title' => 'تحديث المختبرات العلمية',
            'description' => 'مختبرات الفيزياء والكيمياء والبيولوجيا تم تجهيزها بأحدث المعدات التعليمية.'
        ],
        5 => [
            'title' => 'التسجيل للعام الدراسي 2025-2026: فتح الترشيحات',
            'description' => 'التسجيلات مفتوحة الآن لجميع المستويات من الابتدائي إلى الثانوي. أماكن محدودة!'
        ]
    ];

    $addedNewsCount = 0;
    foreach ($frenchNews as $index => $news) {
        $newsId = $news['news_id'];

        // Vérifier si traduction arabe existe déjà
        $checkStmt = $pdo->prepare("SELECT id FROM news_translates WHERE news_id = ? AND locale = 'ar'");
        $checkStmt->execute([$newsId]);

        if ($checkStmt->rowCount() == 0 && isset($arabicNews[$newsId])) {
            $insertStmt = $pdo->prepare("
                INSERT INTO news_translates (news_id, locale, title, description, created_at, updated_at)
                VALUES (?, 'ar', ?, ?, NOW(), NOW())
            ");

            $insertStmt->execute([
                $newsId,
                $arabicNews[$newsId]['title'],
                $arabicNews[$newsId]['description']
            ]);

            echo "   ✅ Actualité $newsId traduite en arabe\n";
            $addedNewsCount++;
        }
    }

    echo "\n📊 Total: $addedNewsCount actualités arabes ajoutées\n\n";

    // ============================================
    // 2. CRÉER DEVOIRS TEST (HOMEWORK)
    // ============================================

    echo "📝 CRÉATION DEVOIRS TEST\n";
    echo "========================================\n";

    // Récupérer quelques class_setups
    $classesStmt = $pdo->query("
        SELECT cs.id as class_setup_id, c.name as class_name
        FROM class_setups cs
        JOIN classes c ON cs.classes_id = c.id
        LIMIT 10
    ");
    $classes = $classesStmt->fetchAll(PDO::FETCH_ASSOC);

    $homeworksAdded = 0;

    // Récupérer session active
    $sessionStmt = $pdo->query("SELECT id FROM sessions WHERE status = 1 LIMIT 1");
    $sessionId = $sessionStmt->fetchColumn();

    foreach (array_slice($classes, 0, 5) as $class) {
        // Récupérer section_id et subject via subject_assigns + subject_assign_childrens
        $assignStmt = $pdo->prepare("
            SELECT sa.section_id, sac.subject_id
            FROM subject_assigns sa
            JOIN subject_assign_childrens sac ON sa.id = sac.subject_assign_id
            WHERE sa.classes_id = ? AND sa.status = 1 AND sac.status = 1
            LIMIT 1
        ");
        $assignStmt->execute([$class['class_setup_id']]);
        $assign = $assignStmt->fetch(PDO::FETCH_ASSOC);

        if (!$assign) continue; // Skip si pas de matière assignée

        $sectionId = $assign['section_id'];
        $subjectId = $assign['subject_id'];

        // Vérifier si homework existe déjà
        $checkStmt = $pdo->prepare("SELECT COUNT(*) FROM homework WHERE classes_id = ? AND section_id = ?");
        $checkStmt->execute([$class['class_setup_id'], $sectionId]);
        $existingCount = $checkStmt->fetchColumn();

        if ($existingCount < 3 && $sessionId) {
            // Créer 2 devoirs par classe
            for ($i = 0; $i < 2; $i++) {
                $insertStmt = $pdo->prepare("
                    INSERT INTO homework (
                        session_id,
                        classes_id,
                        section_id,
                        subject_id,
                        date,
                        submission_date,
                        marks,
                        description,
                        status,
                        created_at,
                        updated_at,
                        branch_id
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, NOW(), NOW(), 1)
                ");

                $homeworkDate = date('Y-m-d');
                $submissionDate = date('Y-m-d', strtotime('+7 days'));

                $insertStmt->execute([
                    $sessionId,
                    $class['class_setup_id'],
                    $sectionId,
                    $subjectId,
                    $homeworkDate,
                    $submissionDate,
                    100,
                    "Devoir pour " . $class['class_name']
                ]);

                $homeworksAdded++;
            }

            echo "   ✅ 2 devoirs créés pour " . $class['class_name'] . "\n";
        }
    }

    echo "\n📊 Total: $homeworksAdded devoirs créés\n\n";

    // ============================================
    // 3. CRÉER ANNONCES (NOTICE BOARDS)
    // ============================================

    echo "📢 CRÉATION ANNONCES\n";
    echo "========================================\n";

    $notices = [
        [
            'ar_title' => 'إغلاق المدرسة يوم الجمعة',
            'ar_desc' => 'المدرسة ستكون مغلقة يوم الجمعة القادم للعطلة الأسبوعية.',
            'fr_title' => 'Fermeture école vendredi',
            'fr_desc' => "L'école sera fermée vendredi prochain pour le congé hebdomadaire.",
            'en_title' => 'School closed Friday',
            'en_desc' => 'The school will be closed next Friday for weekly holiday.'
        ],
        [
            'ar_title' => 'اجتماع أولياء الأمور',
            'ar_desc' => 'اجتماع أولياء الأمور يوم السبت الساعة 10 صباحًا في القاعة الكبرى.',
            'fr_title' => 'Réunion parents d\'élèves',
            'fr_desc' => 'Réunion parents samedi à 10h dans la grande salle.',
            'en_title' => 'Parent-teacher meeting',
            'en_desc' => 'Parent meeting Saturday at 10am in the main hall.'
        ],
        [
            'ar_title' => 'رحلة مدرسية إلى تيبازة',
            'ar_desc' => 'رحلة تعليمية إلى الموقع الأثري في تيبازة يوم الأربعاء المقبل.',
            'fr_title' => 'Sortie scolaire à Tipaza',
            'fr_desc' => 'Sortie pédagogique au site archéologique de Tipaza mercredi prochain.',
            'en_title' => 'School trip to Tipaza',
            'en_desc' => 'Educational trip to Tipaza archaeological site next Wednesday.'
        ]
    ];

    $noticesAdded = 0;

    // Récupérer session active pour les annonces
    $sessionStmt = $pdo->query("SELECT id FROM sessions WHERE status = 1 LIMIT 1");
    $sessionId = $sessionStmt->fetchColumn();

    if (!$sessionId) {
        echo "   ⚠️ Aucune session active trouvée - skip annonces\n";
    } else {
        foreach ($notices as $notice) {
            // Créer la notice principale (sans traductions - table notice_boards a title/description directs)
            $insertNotice = $pdo->prepare("
                INSERT INTO notice_boards (
                    title,
                    session_id,
                    date,
                    publish_date,
                    description,
                    status,
                    created_at,
                    updated_at,
                    branch_id
                ) VALUES (?, ?, ?, ?, ?, 1, NOW(), NOW(), 1)
            ");

            $noticeDate = date('Y-m-d');
            $publishDate = date('Y-m-d H:i:s');

            $insertNotice->execute([
                $notice['fr_title'],
                $sessionId,
                $noticeDate,
                $publishDate,
                $notice['fr_desc']
            ]);

            echo "   ✅ Annonce créée: " . $notice['fr_title'] . "\n";
            $noticesAdded++;
        }
    }

    echo "\n📊 Total: $noticesAdded annonces créées\n\n";

    // ============================================
    // RÉSUMÉ FINAL
    // ============================================

    echo "========================================\n";
    echo "✅ AMÉLIORATIONS TERMINÉES\n";
    echo "========================================\n\n";

    echo "📊 RÉSUMÉ:\n";
    echo "   • $addedNewsCount actualités arabes\n";
    echo "   • $homeworksAdded devoirs créés\n";
    echo "   • $noticesAdded annonces créées\n\n";

    echo "🎯 PROCHAINES ÉTAPES:\n";
    echo "   1. Nettoyer les caches Laravel\n";
    echo "   2. Tester modules Actualités, Devoirs, Annonces\n";
    echo "   3. Vérifier affichage arabe correct\n\n";

} catch (Exception $e) {
    echo "\n❌ ERREUR: " . $e->getMessage() . "\n\n";
    exit(1);
}
