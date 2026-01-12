<?php
/**
 * CRÉATION EXAMENS ET SCÉNARIOS RÉALISTES V2
 * BBC School Algeria - OnestSchool
 *
 * Crée une simulation ultra-réaliste d'école avec:
 * - Examens créés et assignés avec calendrier
 * - Notes réalistes avec distribution statistique
 * - Absences d'élèves réalistes
 * - Absences/congés maladie enseignants
 * - Messages parents fâchés (scénarios réalistes)
 * - Calendrier d'examens pour 7 prochains jours
 */

echo "\n========================================\n";
echo "🎓 CRÉATION EXAMENS ET SCÉNARIOS RÉALISTES V2\n";
echo "🏫 BBC SCHOOL ALGERIA - SIMULATION COMPLÈTE\n";
echo "========================================\n\n";

// Statistiques
$stats = [
    'exams_created' => 0,
    'grades_entered' => 0,
    'student_absences' => 0,
    'teacher_leaves' => 0,
    'parent_messages' => 0,
    'exam_schedules' => 0,
    'errors' => []
];

try {
    $pdo = new PDO('mysql:host=localhost;dbname=onest_school;charset=utf8mb4', 'root', '');
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    echo "✅ Connexion MySQL établie\n\n";

    // Récupérer la session active
    $sessionStmt = $pdo->query("SELECT id FROM sessions WHERE status = 1 LIMIT 1");
    $sessionId = $sessionStmt->fetchColumn();

    if (!$sessionId) {
        die("❌ ERREUR: Aucune session active trouvée\n");
    }

    echo "📊 Session active: ID = $sessionId\n";
    echo "📅 Date: " . date('Y-m-d H:i:s') . "\n\n";

    // ============================================
    // 1. CRÉER EXAMENS CONTRÔLE CONTINU
    // ============================================

    echo "📝 ÉTAPE 1: CRÉATION EXAMENS CONTRÔLE CONTINU\n";
    echo "========================================\n";

    $examTypeId = 1; // Contrôle Continu

    // Récupérer classes actives via subject_assigns
    $classesStmt = $pdo->query("
        SELECT DISTINCT sa.id as subject_assign_id,
               sa.classes_id as class_id,
               c.name as class_name,
               sa.section_id,
               s.name as section_name
        FROM subject_assigns sa
        JOIN classes c ON sa.classes_id = c.id
        JOIN sections s ON sa.section_id = s.id
        WHERE sa.status = 1 AND c.status = 1
        ORDER BY sa.classes_id, sa.section_id
        LIMIT 15
    ");
    $classes = $classesStmt->fetchAll(PDO::FETCH_ASSOC);

    echo "📚 Classes trouvées: " . count($classes) . "\n\n";

    foreach ($classes as $class) {
        echo "  🎯 Classe: {$class['class_name']} - Section: {$class['section_name']}\n";

        // Récupérer les matières assignées pour cette classe via subject_assign_childrens
        $subjectsStmt = $pdo->prepare("
            SELECT sac.id, sac.subject_id, sub.name as subject_name, sub.code as subject_code
            FROM subject_assign_childrens sac
            JOIN subjects sub ON sac.subject_id = sub.id
            WHERE sac.subject_assign_id = ?
            AND sac.status = 1
            LIMIT 8
        ");
        $subjectsStmt->execute([$class['subject_assign_id']]);
        $subjects = $subjectsStmt->fetchAll(PDO::FETCH_ASSOC);

        if (empty($subjects)) {
            echo "    ⚠️ Aucune matière trouvée\n";
            continue;
        }

        foreach ($subjects as $subject) {
            // Vérifier si examen existe déjà
            $checkExamStmt = $pdo->prepare("
                SELECT id FROM exam_assigns
                WHERE session_id = ?
                AND classes_id = ?
                AND section_id = ?
                AND exam_type_id = ?
                AND subject_id = ?
            ");
            $checkExamStmt->execute([
                $sessionId,
                $class['class_id'],
                $class['section_id'],
                $examTypeId,
                $subject['subject_id']
            ]);

            if ($checkExamStmt->rowCount() > 0) {
                echo "    ⏭️ Examen déjà existant pour {$subject['subject_name']}\n";
                continue;
            }

            // Créer l'exam_assign
            $insertExamStmt = $pdo->prepare("
                INSERT INTO exam_assigns (
                    session_id,
                    classes_id,
                    section_id,
                    exam_type_id,
                    subject_id,
                    total_mark,
                    created_at,
                    updated_at,
                    branch_id
                ) VALUES (?, ?, ?, ?, ?, 20, NOW(), NOW(), 1)
            ");

            $insertExamStmt->execute([
                $sessionId,
                $class['class_id'],
                $class['section_id'],
                $examTypeId,
                $subject['subject_id']
            ]);

            $examAssignId = $pdo->lastInsertId();
            $stats['exams_created']++;

            echo "    ✅ Examen créé: {$subject['subject_name']} (ID: $examAssignId)\n";

            // Créer exam_assign_children (composantes de l'examen)
            $examComponents = [
                ['title' => 'Écrit', 'mark' => 15],
                ['title' => 'Oral', 'mark' => 5]
            ];

            foreach ($examComponents as $component) {
                $insertChildStmt = $pdo->prepare("
                    INSERT INTO exam_assign_childrens (
                        exam_assign_id,
                        title,
                        mark,
                        created_at,
                        updated_at,
                        branch_id
                    ) VALUES (?, ?, ?, NOW(), NOW(), 1)
                ");
                $insertChildStmt->execute([
                    $examAssignId,
                    $component['title'],
                    $component['mark']
                ]);
            }

            // Créer marks_register
            $insertMarksRegStmt = $pdo->prepare("
                INSERT INTO marks_registers (
                    session_id,
                    classes_id,
                    section_id,
                    exam_type_id,
                    subject_id,
                    is_marksheet_published,
                    created_at,
                    updated_at,
                    branch_id
                ) VALUES (?, ?, ?, ?, ?, 0, NOW(), NOW(), 1)
            ");
            $insertMarksRegStmt->execute([
                $sessionId,
                $class['class_id'],
                $class['section_id'],
                $examTypeId,
                $subject['subject_id']
            ]);

            $marksRegisterId = $pdo->lastInsertId();

            // Récupérer les élèves de cette classe/section via session_class_students
            $studentsStmt = $pdo->prepare("
                SELECT s.id, CONCAT(s.first_name, ' ', s.last_name) as name
                FROM session_class_students scs
                JOIN students s ON scs.student_id = s.id
                WHERE scs.session_id = ?
                AND scs.classes_id = ?
                AND scs.section_id = ?
                AND s.status = 1
            ");
            $studentsStmt->execute([$sessionId, $class['class_id'], $class['section_id']]);
            $students = $studentsStmt->fetchAll(PDO::FETCH_ASSOC);

            $studentCount = count($students);

            if ($studentCount == 0) {
                echo "    ⚠️ Aucun élève trouvé\n";
                continue;
            }

            // Créer notes réalistes avec distribution statistique
            $gradesDistribution = [];

            // 10% excellent (16-20)
            $excellentCount = (int)($studentCount * 0.10);
            for ($i = 0; $i < $excellentCount; $i++) {
                $gradesDistribution[] = rand(16, 20);
            }

            // 30% bon (13-15)
            $goodCount = (int)($studentCount * 0.30);
            for ($i = 0; $i < $goodCount; $i++) {
                $gradesDistribution[] = rand(13, 15);
            }

            // 40% moyen (10-12)
            $averageCount = (int)($studentCount * 0.40);
            for ($i = 0; $i < $averageCount; $i++) {
                $gradesDistribution[] = rand(10, 12);
            }

            // 15% faible (8-9)
            $weakCount = (int)($studentCount * 0.15);
            for ($i = 0; $i < $weakCount; $i++) {
                $gradesDistribution[] = rand(8, 9);
            }

            // 5% très faible (<8)
            $veryWeakCount = (int)($studentCount * 0.05);
            for ($i = 0; $i < $veryWeakCount; $i++) {
                $gradesDistribution[] = rand(4, 7);
            }

            // Compléter si nécessaire
            while (count($gradesDistribution) < $studentCount) {
                $gradesDistribution[] = rand(10, 12);
            }

            // Mélanger les notes
            shuffle($gradesDistribution);

            // Insérer les notes pour chaque élève
            foreach ($students as $index => $student) {
                $totalMark = $gradesDistribution[$index];

                // Répartir entre écrit et oral
                $writtenMark = round($totalMark * 0.75, 1); // 75% écrit
                $oralMark = $totalMark - $writtenMark; // 25% oral

                // Insérer écrit
                $insertMarkChildStmt = $pdo->prepare("
                    INSERT INTO marks_register_childrens (
                        marks_register_id,
                        student_id,
                        title,
                        mark,
                        created_at,
                        updated_at,
                        branch_id
                    ) VALUES (?, ?, 'Écrit', ?, NOW(), NOW(), 1)
                ");
                $insertMarkChildStmt->execute([
                    $marksRegisterId,
                    $student['id'],
                    $writtenMark
                ]);
                $stats['grades_entered']++;

                // Insérer oral
                $insertMarkChildStmt->execute([
                    $marksRegisterId,
                    $student['id'],
                    $oralMark
                ]);
                $stats['grades_entered']++;
            }

            echo "    📊 Notes créées pour {$studentCount} élèves\n";

            // Créer exam_routines (calendrier) pour les 7 prochains jours
            $examDate = date('Y-m-d', strtotime('+' . rand(1, 7) . ' days'));

            // Vérifier si le calendrier existe déjà pour cette classe/section/type
            $checkRoutineStmt = $pdo->prepare("
                SELECT id FROM exam_routines
                WHERE session_id = ?
                AND classes_id = ?
                AND section_id = ?
                AND type_id = ?
                AND date = ?
            ");
            $checkRoutineStmt->execute([
                $sessionId,
                $class['class_id'],
                $class['section_id'],
                $examTypeId,
                $examDate
            ]);

            if ($checkRoutineStmt->rowCount() == 0) {
                $insertRoutineStmt = $pdo->prepare("
                    INSERT INTO exam_routines (
                        session_id,
                        classes_id,
                        section_id,
                        type_id,
                        date,
                        created_at,
                        updated_at,
                        branch_id
                    ) VALUES (?, ?, ?, ?, ?, NOW(), NOW(), 1)
                ");
                $insertRoutineStmt->execute([
                    $sessionId,
                    $class['class_id'],
                    $class['section_id'],
                    $examTypeId,
                    $examDate
                ]);
                $stats['exam_schedules']++;
                echo "    📅 Calendrier créé pour le $examDate\n";
            }
        }
    }

    echo "\n✅ Total examens créés: {$stats['exams_created']}\n";
    echo "✅ Total notes entrées: {$stats['grades_entered']}\n";
    echo "✅ Total calendriers créés: {$stats['exam_schedules']}\n\n";

    // ============================================
    // 2. CRÉER ABSENCES ÉLÈVES RÉALISTES
    // ============================================

    echo "👨‍🎓 ÉTAPE 2: CRÉATION ABSENCES ÉLÈVES\n";
    echo "========================================\n";

    // Récupérer 20% des élèves actifs via session_class_students
    $studentsForAbsenceStmt = $pdo->query("
        SELECT s.id, CONCAT(s.first_name, ' ', s.last_name) as name, scs.classes_id as class_id, scs.section_id
        FROM session_class_students scs
        JOIN students s ON scs.student_id = s.id
        WHERE scs.session_id = $sessionId
        AND s.status = 1
        ORDER BY RAND()
        LIMIT 30
    ");
    $studentsForAbsence = $studentsForAbsenceStmt->fetchAll(PDO::FETCH_ASSOC);

    foreach ($studentsForAbsence as $student) {
        // Créer 1-3 absences dans les 7 derniers jours
        $absenceCount = rand(1, 3);

        for ($i = 0; $i < $absenceCount; $i++) {
            $absenceDate = date('Y-m-d', strtotime('-' . rand(1, 7) . ' days'));

            // Vérifier si absence existe déjà
            $checkAbsenceStmt = $pdo->prepare("
                SELECT id FROM attendances
                WHERE student_id = ?
                AND date = ?
            ");
            $checkAbsenceStmt->execute([$student['id'], $absenceDate]);

            if ($checkAbsenceStmt->rowCount() == 0) {
                $absenceReasons = [
                    'Malade (grippe)',
                    'Rendez-vous médical',
                    'Problème familial',
                    'Absence injustifiée',
                    'Malade (fièvre)'
                ];

                $reason = $absenceReasons[array_rand($absenceReasons)];
                $attendanceValue = 0; // 0 = Absent, 1 = Present

                $insertAbsenceStmt = $pdo->prepare("
                    INSERT INTO attendances (
                        session_id,
                        student_id,
                        classes_id,
                        section_id,
                        date,
                        attendance,
                        note,
                        created_at,
                        updated_at,
                        branch_id
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, NOW(), NOW(), 1)
                ");
                $insertAbsenceStmt->execute([
                    $sessionId,
                    $student['id'],
                    $student['class_id'],
                    $student['section_id'],
                    $absenceDate,
                    $attendanceValue,
                    $reason
                ]);
                $stats['student_absences']++;
            }
        }

        echo "  ✅ Absences créées pour: {$student['name']}\n";
    }

    echo "\n✅ Total absences élèves créées: {$stats['student_absences']}\n\n";

    // ============================================
    // 3. CRÉER ABSENCES/CONGÉS MALADIE ENSEIGNANTS
    // ============================================

    echo "👨‍🏫 ÉTAPE 3: CRÉATION CONGÉS MALADIE ENSEIGNANTS\n";
    echo "========================================\n";

    // Vérifier si un type de congé maladie existe, sinon le créer
    $leaveTypeStmt = $pdo->query("SELECT id FROM leave_types WHERE name LIKE '%maladie%' OR name LIKE '%sick%' LIMIT 1");
    $leaveType = $leaveTypeStmt->fetch(PDO::FETCH_ASSOC);

    if (!$leaveType) {
        // Créer un type de congé maladie
        $insertLeaveTypeStmt = $pdo->prepare("
            INSERT INTO leave_types (name, short_desc, role_id, active_status, created_at, updated_at)
            VALUES ('Congé Maladie', 'Congé pour raison médicale', 2, 1, NOW(), NOW())
        ");
        $insertLeaveTypeStmt->execute();
        $leaveTypeId = $pdo->lastInsertId();
        echo "  ✅ Type de congé 'Congé Maladie' créé (ID: $leaveTypeId)\n\n";
    } else {
        $leaveTypeId = $leaveType['id'];
    }

    // Récupérer 30% des enseignants actifs
    $staffStmt = $pdo->query("
        SELECT id, user_id, role_id, CONCAT(first_name, ' ', last_name) as name
        FROM staff
        WHERE status = 1
        AND role_id IN (2, 3)
        ORDER BY RAND()
        LIMIT 10
    ");
    $staffs = $staffStmt->fetchAll(PDO::FETCH_ASSOC);

    foreach ($staffs as $staff) {
        // Créer 1-3 jours de congé maladie
        $leaveDays = rand(1, 3);
        $startDate = date('Y-m-d', strtotime('-' . rand(1, 7) . ' days'));
        $endDate = date('Y-m-d', strtotime($startDate . ' +' . ($leaveDays - 1) . ' days'));

        // Vérifier si congé existe déjà
        $checkLeaveStmt = $pdo->prepare("
            SELECT id FROM leave_requests
            WHERE user_id = ?
            AND start_date = ?
        ");
        $checkLeaveStmt->execute([$staff['user_id'], $startDate]);

        if ($checkLeaveStmt->rowCount() == 0) {
            $sickReasons = [
                'Grippe saisonnière - repos médical prescrit',
                'Gastro-entérite - certificat médical joint',
                'Migraine sévère - arrêt de travail',
                'Problème de santé familial urgent',
                'Consultation médicale spécialisée'
            ];

            $reason = $sickReasons[array_rand($sickReasons)];

            $insertLeaveStmt = $pdo->prepare("
                INSERT INTO leave_requests (
                    leave_type_id,
                    user_id,
                    role_id,
                    request_by,
                    session_id,
                    start_date,
                    end_date,
                    description,
                    leave_days,
                    approval_status,
                    created_at,
                    updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'approved', NOW(), NOW())
            ");
            $insertLeaveStmt->execute([
                $leaveTypeId,
                $staff['user_id'],
                $staff['role_id'],
                $staff['user_id'],
                $sessionId,
                $startDate,
                $endDate,
                $reason,
                $leaveDays
            ]);
            $stats['teacher_leaves']++;

            echo "  ✅ Congé maladie créé pour: {$staff['name']} ({$leaveDays} jours)\n";
        }
    }

    echo "\n✅ Total congés enseignants créés: {$stats['teacher_leaves']}\n\n";

    // ============================================
    // 4. CRÉER MESSAGES PARENTS FÂCHÉS
    // ============================================

    echo "😡 ÉTAPE 4: CRÉATION MESSAGES PARENTS FÂCHÉS\n";
    echo "========================================\n";

    // Récupérer quelques élèves pour les messages via session_class_students
    $studentsForMessagesStmt = $pdo->query("
        SELECT s.id, CONCAT(s.first_name, ' ', s.last_name) as name, scs.classes_id as class_id, scs.section_id
        FROM session_class_students scs
        JOIN students s ON scs.student_id = s.id
        WHERE scs.session_id = $sessionId
        AND s.status = 1
        ORDER BY RAND()
        LIMIT 10
    ");
    $studentsForMessages = $studentsForMessagesStmt->fetchAll(PDO::FETCH_ASSOC);

    $angryMessages = [
        [
            'title' => '🔴 URGENT: Notes injustes en mathématiques!',
            'description' => "Monsieur le Directeur,\n\nJe suis TRÈS MÉCONTENT des notes de mon fils en mathématiques. Il a eu 6/20 alors qu'il a bien révisé à la maison! Le professeur ne fait pas attention et ne corrige pas correctement. Mon fils mérite au moins 12/20!\n\nJe demande une révision IMMÉDIATE de sa copie, sinon je vais porter plainte au ministère de l'éducation.\n\nC'est inadmissible! Nos enfants méritent mieux que ça!\n\nParent très mécontent",
            'visible_to' => 'admin'
        ],
        [
            'title' => '😤 Professeur TOUJOURS absent!',
            'description' => "À l'administration BBC School,\n\nCela fait 3 SEMAINES que le professeur d'anglais est absent! Nos enfants n'ont pas cours et vous ne faites RIEN!\n\nOn paye les frais de scolarité pour QUOI exactement? Pour que nos enfants restent à la maison?\n\nJe veux une explication AUJOURD'HUI et un professeur remplaçant DEMAIN, sinon je retire mon enfant de votre école!\n\nHonteux!",
            'visible_to' => 'admin'
        ],
        [
            'title' => '⚠️ HARCÈLEMENT dans la cour de récréation',
            'description' => "Madame, Monsieur,\n\nMa fille rentre TOUS LES JOURS en pleurant car des élèves de 3ème année se moquent d'elle et la poussent dans la cour!\n\nVotre surveillant ne fait RIEN! Il est toujours sur son téléphone!\n\nJe vous préviens: si cela continue, je vais à la gendarmerie pour déposer une plainte officielle. La sécurité de nos enfants est VOTRE RESPONSABILITÉ!\n\nJ'attends des mesures IMMÉDIATES!\n\nParent inquiet et furieux",
            'visible_to' => 'admin'
        ],
        [
            'title' => '🚌 Bus scolaire EN RETARD chaque jour!',
            'description' => "Bonjour,\n\nC'est INACCEPTABLE! Le bus scolaire arrive avec 30-40 minutes de retard CHAQUE MATIN!\n\nMon fils arrive en retard en classe et se fait punir alors que ce n'est PAS SA FAUTE!\n\nLe chauffeur ne respecte pas les horaires, il fume sa cigarette tranquillement pendant que nos enfants attendent sous le soleil!\n\nJe veux une solution MAINTENANT ou je demande le remboursement des frais de transport!\n\nC'est un manque de respect total!",
            'visible_to' => 'admin'
        ],
        [
            'title' => '📚 TROP de devoirs! Les enfants sont épuisés!',
            'description' => "Chers responsables,\n\nC'est TROP! Mon fils a des devoirs jusqu'à 22h TOUS LES SOIRS!\n\nIl est en 4ème année, pas à l'université! Il n'a même pas le temps de jouer ou de se reposer!\n\nLes professeurs donnent des devoirs sans se coordonner. Résultat: 5 matières avec devoirs le même jour!\n\nNos enfants sont ÉPUISÉS, ils ne dorment pas assez et tombent malades!\n\nJe demande une réunion URGENTE avec tous les professeurs pour régler ce problème!\n\nAssez c'est assez!",
            'visible_to' => 'admin'
        ],
        [
            'title' => '💻 Système en ligne NE MARCHE JAMAIS!',
            'description' => "Bonjour,\n\nVotre système en ligne est une CATASTROPHE!\n\nJe ne peux JAMAIS voir les notes de ma fille, ça dit toujours \"Erreur 404\" ou \"Service indisponible\"!\n\nComment je peux suivre sa scolarité si votre système ne marche pas?!\n\nJ'ai appelé 10 FOIS au secrétariat, personne ne répond! C'est un scandale!\n\nRéparez votre système ou donnez-nous les bulletins EN PAPIER comme avant!\n\nOn n'est pas des informaticiens nous!",
            'visible_to' => 'admin'
        ],
        [
            'title' => '❌ Absence INCORRECTE marquée!',
            'description' => "Madame la Directrice,\n\nMon fils était PRÉSENT le 15 novembre mais votre système dit qu'il était ABSENT!\n\nJ'ai le certificat médical de son rendez-vous qui prouve qu'il était à l'école l'après-midi!\n\nVotre secrétaire refuse de corriger l'erreur et me dit que \"c'est comme ça\"!\n\nC'EST INACCEPTABLE! Corrigez cette erreur IMMÉDIATEMENT!\n\nSi cela affecte sa moyenne de présence, je vais porter plainte!\n\nFaites votre travail correctement!",
            'visible_to' => 'admin'
        ],
        [
            'title' => '🍽️ Qualité MÉDIOCRE de la cantine scolaire',
            'description' => "À qui de droit,\n\nLa nourriture de la cantine est DÉGOÛTANTE!\n\nMa fille a eu une intoxication alimentaire la semaine dernière! Elle a vomi toute la nuit!\n\nLe riz est trop cuit, la viande est froide, les légumes sentent mauvais!\n\nOn paye 5000 DA par mois pour cette NOURRITURE DE MAUVAISE QUALITÉ?!\n\nJe vais au ministère de la santé si vous ne changez pas IMMÉDIATEMENT le fournisseur de la cantine!\n\nC'est dangereux pour nos enfants!",
            'visible_to' => 'admin'
        ]
    ];

    foreach ($studentsForMessages as $index => $student) {
        if ($index >= count($angryMessages)) break;

        $message = $angryMessages[$index];

        // Vérifier si message similaire existe déjà
        $checkMessageStmt = $pdo->prepare("
            SELECT id FROM notice_boards
            WHERE student_id = ?
            AND title = ?
        ");
        $checkMessageStmt->execute([$student['id'], $message['title']]);

        if ($checkMessageStmt->rowCount() == 0) {
            $publishDate = date('Y-m-d', strtotime('-' . rand(1, 5) . ' days'));

            $insertMessageStmt = $pdo->prepare("
                INSERT INTO notice_boards (
                    title,
                    session_id,
                    class_id,
                    section_id,
                    student_id,
                    date,
                    publish_date,
                    description,
                    is_visible_web,
                    status,
                    visible_to,
                    created_at,
                    updated_at,
                    branch_id
                ) VALUES (?, ?, ?, ?, ?, NOW(), ?, ?, 1, 1, ?, NOW(), NOW(), 1)
            ");
            $insertMessageStmt->execute([
                $message['title'],
                $sessionId,
                $student['class_id'],
                $student['section_id'],
                $student['id'],
                $publishDate,
                $message['description'],
                $message['visible_to']
            ]);
            $stats['parent_messages']++;

            echo "  ✅ Message parent créé: {$message['title']}\n";
        }
    }

    echo "\n✅ Total messages parents créés: {$stats['parent_messages']}\n\n";

    // ============================================
    // RÉSUMÉ FINAL
    // ============================================

    echo "\n========================================\n";
    echo "📊 RÉSUMÉ DE LA CRÉATION\n";
    echo "========================================\n\n";

    echo "✅ Examens créés: {$stats['exams_created']}\n";
    echo "✅ Notes entrées: {$stats['grades_entered']}\n";
    echo "✅ Calendriers d'examens: {$stats['exam_schedules']}\n";
    echo "✅ Absences élèves: {$stats['student_absences']}\n";
    echo "✅ Congés enseignants: {$stats['teacher_leaves']}\n";
    echo "✅ Messages parents fâchés: {$stats['parent_messages']}\n";

    if (!empty($stats['errors'])) {
        echo "\n⚠️ ERREURS RENCONTRÉES:\n";
        foreach ($stats['errors'] as $error) {
            echo "  ❌ $error\n";
        }
    }

    echo "\n========================================\n";
    echo "🎉 SIMULATION COMPLÈTE TERMINÉE!\n";
    echo "========================================\n\n";

    echo "💡 RECOMMANDATIONS:\n";
    echo "  1. Vérifiez les examens dans le module 'Examens'\n";
    echo "  2. Consultez les notes dans 'Registre des notes'\n";
    echo "  3. Vérifiez les absences dans 'Présences'\n";
    echo "  4. Lisez les messages dans 'Tableau d'affichage'\n";
    echo "  5. Vérifiez les congés dans 'Gestion du personnel'\n\n";

} catch (PDOException $e) {
    echo "\n❌ ERREUR PDO: " . $e->getMessage() . "\n";
    echo "📍 Fichier: " . $e->getFile() . "\n";
    echo "📍 Ligne: " . $e->getLine() . "\n\n";
    $stats['errors'][] = $e->getMessage();
} catch (Exception $e) {
    echo "\n❌ ERREUR: " . $e->getMessage() . "\n";
    $stats['errors'][] = $e->getMessage();
}

echo "\n✅ Script terminé à " . date('H:i:s') . "\n\n";
