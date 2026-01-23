<?php
/**
 * CRÉATION EXAMENS ET SCÉNARIOS RÉALISTES V2
 * BBC School Algeria - OnestSchool
 * Adapté à la structure réelle de la base de données
 */

echo "\n========================================\n";
echo "CRÉATION EXAMENS ET SCÉNARIOS RÉALISTES\n";
echo "BBC SCHOOL ALGERIA - SIMULATION COMPLÈTE\n";
echo "========================================\n\n";

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

    echo "📊 Session active: ID = $sessionId\n\n";

    // ============================================
    // 1. CRÉER EXAMENS ET NOTES RÉALISTES
    // ============================================

    echo "📝 CRÉATION EXAMENS TRIMESTRIEL 1\n";
    echo "========================================\n";

    $examTypeId = 1; // Contrôle Continu
    $examsCreated = 0;
    $gradesEntered = 0;

    // Récupérer classes avec matières et enseignants
    $assignmentsStmt = $pdo->query("
        SELECT
            sa.classes_id,
            c.name as class_name,
            sa.section_id,
            sec.name as section_name,
            sac.subject_id,
            sub.name as subject_name,
            sac.staff_id
        FROM subject_assigns sa
        JOIN classes c ON sa.classes_id = c.id
        JOIN sections sec ON sa.section_id = sec.id
        JOIN subject_assign_childrens sac ON sa.id = sac.subject_assign_id
        JOIN subjects sub ON sac.subject_id = sub.id
        WHERE c.status = 1
        LIMIT 30
    ");
    $assignments = $assignmentsStmt->fetchAll(PDO::FETCH_ASSOC);

    foreach ($assignments as $assignment) {
        // Vérifier si exam_assign existe déjà
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
            $assignment['classes_id'],
            $assignment['section_id'],
            $examTypeId,
            $assignment['subject_id']
        ]);

        if ($checkExamStmt->rowCount() == 0) {
            // Créer exam_assign
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
                $assignment['classes_id'],
                $assignment['section_id'],
                $examTypeId,
                $assignment['subject_id']
            ]);

            $examAssignId = $pdo->lastInsertId();
            $examsCreated++;

            // Créer marks_register
            $insertRegisterStmt = $pdo->prepare("
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

            $insertRegisterStmt->execute([
                $sessionId,
                $assignment['classes_id'],
                $assignment['section_id'],
                $examTypeId,
                $assignment['subject_id']
            ]);

            $marksRegisterId = $pdo->lastInsertId();

            // Récupérer les étudiants de cette classe
            $studentsStmt = $pdo->prepare("
                SELECT s.id, u.name
                FROM students s
                JOIN users u ON s.user_id = u.id
                WHERE s.class_id = ?
                AND s.section_id = ?
                AND s.status = 1
                LIMIT 40
            ");
            $studentsStmt->execute([
                $assignment['classes_id'],
                $assignment['section_id']
            ]);
            $students = $studentsStmt->fetchAll(PDO::FETCH_ASSOC);

            // Créer notes pour chaque élève
            foreach ($students as $student) {
                // Générer note réaliste
                $mark = generateRealisticMark(20);

                // 5% d'absents
                $isAbsent = (rand(1, 100) <= 5);

                $insertMarkStmt = $pdo->prepare("
                    INSERT INTO marks_register_childrens (
                        marks_register_id,
                        student_id,
                        title,
                        mark,
                        created_at,
                        updated_at,
                        branch_id
                    ) VALUES (?, ?, ?, ?, NOW(), NOW(), 1)
                ");

                $title = $isAbsent ? 'Absent' : 'Note';
                $finalMark = $isAbsent ? 0 : $mark;

                $insertMarkStmt->execute([
                    $marksRegisterId,
                    $student['id'],
                    $title,
                    $finalMark
                ]);

                $gradesEntered++;
            }

            echo "   ✅ Examen créé: " . $assignment['class_name'] . " - " . $assignment['section_name'] . " - " . $assignment['subject_name'] . " (" . count($students) . " élèves)\n";
        }
    }

    echo "\n📊 Total: $examsCreated examens créés, $gradesEntered notes saisies\n\n";

    // ============================================
    // 2. CRÉER ABSENCES ÉLÈVES RÉALISTES
    // ============================================

    echo "🏥 CRÉATION ABSENCES ÉLÈVES\n";
    echo "========================================\n";

    $absencesCreated = 0;
    $studentsStmt = $pdo->query("
        SELECT s.id, u.name, s.class_id, s.section_id
        FROM students s
        JOIN users u ON s.user_id = u.id
        WHERE s.status = 1
        LIMIT 100
    ");
    $allStudents = $studentsStmt->fetchAll(PDO::FETCH_ASSOC);

    foreach ($allStudents as $student) {
        // 20% des élèves ont des absences
        if (rand(1, 100) <= 20) {
            $numAbsences = rand(1, 3);

            for ($i = 0; $i < $numAbsences; $i++) {
                $absenceDate = date('Y-m-d', strtotime('-' . rand(1, 7) . ' days'));

                // Vérifier si absence existe
                $checkAbsStmt = $pdo->prepare("
                    SELECT id FROM student_attendances
                    WHERE student_id = ? AND date = ?
                ");
                $checkAbsStmt->execute([$student['id'], $absenceDate]);

                if ($checkAbsStmt->rowCount() == 0) {
                    $reasons = [
                        'Maladie',
                        'Rendez-vous médical',
                        'Problème familial',
                        'Transport en panne',
                        null
                    ];

                    $insertAbsStmt = $pdo->prepare("
                        INSERT INTO student_attendances (
                            session_id,
                            student_id,
                            class_id,
                            section_id,
                            date,
                            attendance_type_id,
                            note,
                            status,
                            created_at,
                            updated_at,
                            branch_id
                        ) VALUES (?, ?, ?, ?, ?, 2, ?, 1, NOW(), NOW(), 1)
                    ");

                    $insertAbsStmt->execute([
                        $sessionId,
                        $student['id'],
                        $student['class_id'],
                        $student['section_id'],
                        $absenceDate,
                        $reasons[array_rand($reasons)]
                    ]);

                    $absencesCreated++;
                }
            }

            if ($numAbsences > 0) {
                echo "   ⚠️ " . $student['name'] . ": $numAbsences absences\n";
            }
        }
    }

    echo "\n📊 Total: $absencesCreated absences créées\n\n";

    // ============================================
    // 3. CRÉER MESSAGES PARENTS FÂCHÉS
    // ============================================

    echo "😠 CRÉATION MESSAGES PARENTS FÂCHÉS\n";
    echo "========================================\n";

    $angryMessages = [
        [
            'title' => '⚠️ URGENT - Note injuste en Mathématiques',
            'message' => 'Bonjour Madame/Monsieur le Directeur,

Je suis la maman d\'Ahmed et je conteste formellement la note de 8/20 qu\'il a obtenue en mathématiques. Mon fils a travaillé jour et nuit pour cet examen et mérite au minimum 14/20.

Je demande une révision IMMÉDIATE de sa copie par un autre professeur. Cette note injuste va impacter sa moyenne générale et son moral.

J\'attends un retour URGENT.

Cordialement,
Mme Benali'
        ],
        [
            'title' => '😡 INADMISSIBLE - Professeur absent 3 fois ce mois',
            'message' => 'C\'EST INADMISSIBLE!

Le professeur de Français de la classe 3AP est absent pour la TROISIÈME FOIS ce mois-ci! Mes enfants prennent du retard sur le programme et je paie 25.000 DA par mois!

Je veux:
1. Une explication officielle
2. Un professeur remplaçant QUALIFIÉ immédiatement
3. Un remboursement partiel des frais

Si rien n\'est fait d\'ici 48h, je retire mes 2 enfants de l\'école!

M. Kaci (Parent de 2 élèves)'
        ],
        [
            'title' => '🚨 HARCÈLEMENT - Mon fils pleure tous les jours',
            'message' => 'URGENT - HARCÈLEMENT SCOLAIRE

Mon fils Yacine (2AM Section A) se fait harceler QUOTIDIENNEMENT par 3 élèves de 4AM dans la cour de récréation. Ils lui prennent son goûter, le poussent et l\'insultent.

Il rentre en PLEURANT tous les jours et refuse d\'aller à l\'école.

L\'ÉCOLE DOIT INTERVENIR IMMÉDIATEMENT!

Je tiendrai l\'établissement RESPONSABLE si cela continue. Je vais porter plainte si nécessaire.

Mme Amrani
Tél: 0555 XX XX XX'
        ],
        [
            'title' => '🚌 Bus scolaire - 40 minutes de retard TOUS LES JOURS',
            'message' => 'Bonjour,

Le bus scolaire (Circuit Dely Ibrahim) a entre 30 et 40 minutes de retard TOUS LES MATINS sans exception depuis 2 semaines.

Conséquences:
- Ma fille arrive en retard en classe (marquée absente 3 fois!)
- Elle manque le début des cours
- Elle est stressée et fatiguée

Pour 8.000 DA/mois de transport, c\'est du n\'importe quoi!

JE DEMANDE:
1. Respect des horaires OU
2. Remboursement partiel

M. Touati'
        ],
        [
            'title' => '📚 TROP DE DEVOIRS - Mon enfant dort à 23h',
            'message' => 'Les devoirs sont BEAUCOUP TROP NOMBREUX!

Ma fille (5AP) travaille tous les soirs de 17h à 23h sans interruption. C\'est ÉPUISANT et CONTRE-PRODUCTIF.

Hier soir:
- 2 pages de math
- Rédaction de 30 lignes en français
- Apprendre 15 mots d\'anglais
- Réviser sciences (3 leçons)
- Devoirs d\'arabe

Elle a 10 ans! Elle doit aussi jouer et se reposer!

Les professeurs doivent SE COORDONNER pour réduire la charge de travail.

Mme Hamdi'
        ],
        [
            'title' => '💻 SYSTÈME EN PANNE - Impossible de voir les notes',
            'message' => 'Bonjour,

Cela fait 3 SEMAINES que j\'essaie de télécharger le bulletin de mon fils sur votre site et ça ne marche JAMAIS!

Erreur à chaque fois: "Bulletin non disponible"

J\'ai besoin du bulletin AUJOURD\'HUI pour une inscription dans un club sportif.

Votre système informatique est DÉFAILLANT. Pour le prix de la scolarité, c\'est inadmissible.

Envoyez-moi le bulletin par EMAIL immédiatement: parent@email.dz

M. Meziane'
        ],
        [
            'title' => '❌ ERREUR - Absence marquée à tort le 15/01',
            'message' => 'ERREUR DANS VOS REGISTRES!

Mon fils Karim a été marqué ABSENT le 15/01/2025 alors qu\'il était PRÉSENT toute la journée!

J\'ai même la photo de lui en classe avec ses camarades (voir pièce jointe).

Cette erreur impacte son taux de présence (maintenant 92% au lieu de 98%) et risque de lui faire perdre sa bourse d\'excellence.

CORRIGEZ cette erreur IMMÉDIATEMENT dans le système!

Mme Bouzid
Tél: 0770 XX XX XX'
        ],
        [
            'title' => '🍽️ Cantine - Qualité MÉDIOCRE, mon fils refuse de manger',
            'message' => 'La qualité de la cantine est VRAIMENT MÉDIOCRE!

Mon fils refuse de manger là-bas depuis 2 semaines. Il me dit:
- La nourriture est froide
- Les portions sont minuscules
- Pas de variété (toujours pâtes)
- Pas de fruits

Il rentre affamé à 16h et doit attendre 18h pour manger.

Pour 6.000 DA/mois, j\'attends un MINIMUM de qualité!

REVOYEZ vos menus et vos fournisseurs!

M. Rahmani'
        ]
    ];

    $messagesCreated = 0;

    foreach ($angryMessages as $msg) {
        $noticeDate = date('Y-m-d', strtotime('-' . rand(1, 5) . ' days'));

        $insertNoticeStmt = $pdo->prepare("
            INSERT INTO notice_boards (
                title,
                session_id,
                date,
                publish_date,
                description,
                status,
                is_visible_web,
                created_at,
                updated_at,
                branch_id
            ) VALUES (?, ?, ?, ?, ?, 1, 0, NOW(), NOW(), 1)
        ");

        $insertNoticeStmt->execute([
            $msg['title'],
            $sessionId,
            $noticeDate,
            date('Y-m-d H:i:s'),
            $msg['message']
        ]);

        echo "   😠 " . $msg['title'] . "\n";
        $messagesCreated++;
    }

    echo "\n📊 Total: $messagesCreated messages parents fâchés créés\n\n";

    // ============================================
    // 4. CRÉER ABSENCES ENSEIGNANTS (MALADES)
    // ============================================

    echo "🤒 CRÉATION ABSENCES ENSEIGNANTS\n";
    echo "========================================\n";

    $teacherAbsences = 0;

    $teachersStmt = $pdo->query("
        SELECT st.id, u.name
        FROM staff st
        JOIN users u ON st.user_id = u.id
        WHERE st.status = 1 AND st.role_id = 4
        LIMIT 15
    ");
    $teachers = $teachersStmt->fetchAll(PDO::FETCH_ASSOC);

    foreach ($teachers as $teacher) {
        // 30% des profs ont eu un congé maladie
        if (rand(1, 100) <= 30) {
            $leaveDays = rand(1, 4);
            $leaveFrom = date('Y-m-d', strtotime('-' . rand(1, 10) . ' days'));
            $leaveTo = date('Y-m-d', strtotime($leaveFrom . " +$leaveDays days"));

            $reasons = [
                'Grippe saisonnière',
                'Gastro-entérite',
                'Migraine sévère',
                'Urgence familiale - décès',
                'Rendez-vous médical (analyses)',
                'Angine',
                'Lombalgie aiguë'
            ];

            $checkLeaveStmt = $pdo->prepare("
                SELECT id FROM leaves
                WHERE staff_id = ? AND leave_from = ?
            ");
            $checkLeaveStmt->execute([$teacher['id'], $leaveFrom]);

            if ($checkLeaveStmt->rowCount() == 0) {
                $insertLeaveStmt = $pdo->prepare("
                    INSERT INTO leaves (
                        staff_id,
                        leave_type_id,
                        leave_from,
                        leave_to,
                        reason,
                        apply_date,
                        approve_status,
                        status,
                        created_at,
                        updated_at,
                        branch_id
                    ) VALUES (?, 2, ?, ?, ?, ?, 1, 1, NOW(), NOW(), 1)
                ");

                $insertLeaveStmt->execute([
                    $teacher['id'],
                    $leaveFrom,
                    $leaveTo,
                    $reasons[array_rand($reasons)],
                    date('Y-m-d', strtotime($leaveFrom . ' -1 day'))
                ]);

                echo "   🤒 " . $teacher['name'] . ": $leaveDays jours (" . $reasons[array_rand($reasons)] . ")\n";
                $teacherAbsences++;
            }
        }
    }

    echo "\n📊 Total: $teacherAbsences congés maladie enseignants\n\n";

    // ============================================
    // RÉSUMÉ FINAL
    // ============================================

    echo "========================================\n";
    echo "✅ SIMULATION RÉALISTE COMPLÉTÉE\n";
    echo "========================================\n\n";

    echo "📊 RÉSUMÉ FINAL:\n";
    echo "   ✅ $examsCreated examens créés\n";
    echo "   ✅ $gradesEntered notes saisies (réalistes)\n";
    echo "   ✅ $absencesCreated absences élèves\n";
    echo "   ✅ $messagesCreated messages parents fâchés\n";
    echo "   ✅ $teacherAbsences congés maladie profs\n\n";

    echo "🎯 SCÉNARIOS RÉALISTES:\n";
    echo "   ⭐ Distribution notes réaliste:\n";
    echo "      • 10% excellents (16-20)\n";
    echo "      • 30% bons (13-15)\n";
    echo "      • 40% moyens (10-12)\n";
    echo "      • 15% faibles (8-9)\n";
    echo "      • 5% très faibles (<8)\n";
    echo "   ⭐ 5% élèves absents aux examens\n";
    echo "   ⭐ 20% élèves avec absences récentes\n";
    echo "   ⭐ 8 cas parents mécontents (réalistes)\n";
    echo "   ⭐ 30% enseignants malades\n\n";

    echo "🔄 PROCHAINES ÉTAPES:\n";
    echo "   1. Nettoyer caches Laravel\n";
    echo "   2. Publier les bulletins (Admin Panel)\n";
    echo "   3. Vérifier notes dans Parent Panel\n";
    echo "   4. Gérer les messages parents\n";
    echo "   5. Tester scénarios complets\n\n";

} catch (Exception $e) {
    echo "\n❌ ERREUR: " . $e->getMessage() . "\n";
    echo "Trace: " . $e->getTraceAsString() . "\n\n";
    exit(1);
}

/**
 * Génère une note réaliste selon distribution normale
 */
function generateRealisticMark($totalMarks) {
    $rand = rand(1, 100);

    if ($rand <= 10) {
        // 10% excellents
        $mark = rand(16 * 100, 20 * 100) / 100;
    } elseif ($rand <= 40) {
        // 30% bons
        $mark = rand(13 * 100, 15 * 100) / 100;
    } elseif ($rand <= 80) {
        // 40% moyens
        $mark = rand(10 * 100, 12 * 100) / 100;
    } elseif ($rand <= 95) {
        // 15% faibles
        $mark = rand(8 * 100, 9 * 100) / 100;
    } else {
        // 5% très faibles
        $mark = rand(4 * 100, 7 * 100) / 100;
    }

    // Ajuster selon total
    $mark = ($mark / 20) * $totalMarks;

    // Arrondir à 0.5 près
    $mark = round($mark * 2) / 2;

    return $mark;
}
