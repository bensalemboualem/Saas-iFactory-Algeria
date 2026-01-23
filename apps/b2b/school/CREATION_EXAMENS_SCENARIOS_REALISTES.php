<?php
/**
 * CRÉATION EXAMENS ET SCÉNARIOS RÉALISTES
 * BBC School Algeria - OnestSchool
 *
 * Crée une simulation réaliste d'école avec:
 * - Examens créés et assignés
 * - Notes réalistes avec variations (bons, moyens, faibles élèves)
 * - Absences d'élèves
 * - Messages parents fâchés
 * - Enseignants malades (absences)
 * - Scénarios réalistes du quotidien
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
    // 1. CRÉER EXAMEN TRIMESTRIEL 1 (Contrôle Continu)
    // ============================================

    echo "📝 CRÉATION EXAMENS TRIMESTRIEL 1\n";
    echo "========================================\n";

    $examTypeId = 1; // Contrôle Continu
    $examCreated = 0;

    // Récupérer quelques classes actives avec matières assignées
    $classesStmt = $pdo->query("
        SELECT DISTINCT sa.id as subject_assign_id,
               sa.classes_id,
               c.name as class_name,
               sa.section_id,
               s.name as section_name
        FROM subject_assigns sa
        JOIN classes c ON sa.classes_id = c.id
        JOIN sections s ON sa.section_id = s.id
        WHERE sa.status = 1 AND c.status = 1
        LIMIT 15
    ");
    $classes = $classesStmt->fetchAll(PDO::FETCH_ASSOC);

    foreach ($classes as $class) {
        // Récupérer les matières assignées pour cette classe
        $subjectsStmt = $pdo->prepare("
            SELECT sac.id, sac.subject_id, sub.name as subject_name, sac.staff_id
            FROM subject_assign_childrens sac
            JOIN subjects sub ON sac.subject_id = sub.id
            WHERE sac.subject_assign_id = ? AND sac.status = 1
            LIMIT 5
        ");
        $subjectsStmt->execute([$class['subject_assign_id']]);
        $subjects = $subjectsStmt->fetchAll(PDO::FETCH_ASSOC);

        if (empty($subjects)) continue;

        // Vérifier si examen existe déjà pour cette classe
        $checkExamStmt = $pdo->prepare("
            SELECT id FROM exam_assigns
            WHERE session_id = ?
            AND classes_id = ?
            AND section_id = ?
            AND exam_type_id = ?
        ");
        $checkExamStmt->execute([$sessionId, $class['classes_id'], $class['section_id'], $examTypeId]);

        if ($checkExamStmt->rowCount() == 0) {
            // Créer l'exam_assign
            $insertExamStmt = $pdo->prepare("
                INSERT INTO exam_assigns (
                    session_id,
                    classes_id,
                    section_id,
                    exam_type_id,
                    status,
                    created_at,
                    updated_at,
                    branch_id
                ) VALUES (?, ?, ?, ?, 1, NOW(), NOW(), 1)
            ");

            $insertExamStmt->execute([
                $sessionId,
                $class['classes_id'],
                $class['section_id'],
                $examTypeId
            ]);

            $examAssignId = $pdo->lastInsertId();

            // Créer exam_assign_childrens pour chaque matière
            foreach ($subjects as $subject) {
                $insertExamChildStmt = $pdo->prepare("
                    INSERT INTO exam_assign_childrens (
                        exam_assign_id,
                        subject_id,
                        staff_id,
                        total_marks,
                        pass_marks,
                        status,
                        created_at,
                        updated_at,
                        branch_id
                    ) VALUES (?, ?, ?, 20, 10, 1, NOW(), NOW(), 1)
                ");

                $insertExamChildStmt->execute([
                    $examAssignId,
                    $subject['subject_id'],
                    $subject['staff_id']
                ]);
            }

            echo "   ✅ Examen créé: " . $class['class_name'] . " - " . $class['section_name'] . " (" . count($subjects) . " matières)\n";
            $examCreated++;
        }
    }

    echo "\n📊 Total: $examCreated examens créés\n\n";

    // ============================================
    // 2. CRÉER CALENDRIER D'EXAMENS (EXAM ROUTINE)
    // ============================================

    echo "📅 CRÉATION CALENDRIER EXAMENS\n";
    echo "========================================\n";

    $routinesCreated = 0;
    $startDate = date('Y-m-d', strtotime('+7 days')); // Commence dans 7 jours

    foreach ($classes as $class) {
        // Récupérer exam_assign pour cette classe
        $examAssignStmt = $pdo->prepare("
            SELECT id FROM exam_assigns
            WHERE session_id = ?
            AND classes_id = ?
            AND section_id = ?
            AND exam_type_id = ?
        ");
        $examAssignStmt->execute([$sessionId, $class['classes_id'], $class['section_id'], $examTypeId]);
        $examAssign = $examAssignStmt->fetch(PDO::FETCH_ASSOC);

        if (!$examAssign) continue;

        // Récupérer les matières pour cet examen
        $examSubjectsStmt = $pdo->prepare("
            SELECT eac.id, eac.subject_id, s.name as subject_name
            FROM exam_assign_childrens eac
            JOIN subjects s ON eac.subject_id = s.id
            WHERE eac.exam_assign_id = ?
        ");
        $examSubjectsStmt->execute([$examAssign['id']]);
        $examSubjects = $examSubjectsStmt->fetchAll(PDO::FETCH_ASSOC);

        // Créer routine pour chaque matière (sur 5 jours)
        $dayOffset = 0;
        foreach ($examSubjects as $index => $examSub) {
            // Vérifier si routine existe déjà
            $checkRoutineStmt = $pdo->prepare("
                SELECT id FROM exam_routines
                WHERE exam_assign_id = ?
                AND exam_assign_children_id = ?
            ");
            $checkRoutineStmt->execute([$examAssign['id'], $examSub['id']]);

            if ($checkRoutineStmt->rowCount() == 0) {
                $examDate = date('Y-m-d', strtotime($startDate . " +$dayOffset days"));
                $startTime = "08:00:00";
                $endTime = "10:00:00";
                $roomNo = 100 + ($index % 10); // Salles 100-110

                $insertRoutineStmt = $pdo->prepare("
                    INSERT INTO exam_routines (
                        exam_assign_id,
                        exam_assign_children_id,
                        date,
                        start_time,
                        end_time,
                        room_no,
                        status,
                        created_at,
                        updated_at,
                        branch_id
                    ) VALUES (?, ?, ?, ?, ?, ?, 1, NOW(), NOW(), 1)
                ");

                $insertRoutineStmt->execute([
                    $examAssign['id'],
                    $examSub['id'],
                    $examDate,
                    $startTime,
                    $endTime,
                    $roomNo
                ]);

                $routinesCreated++;
                $dayOffset++; // Prochain jour
            }
        }
    }

    echo "   ✅ $routinesCreated calendriers d'examens créés\n\n";

    // ============================================
    // 3. CRÉER MARKS REGISTERS (Pour saisie notes)
    // ============================================

    echo "📊 CRÉATION REGISTRES DE NOTES\n";
    echo "========================================\n";

    $registersCreated = 0;

    foreach ($classes as $class) {
        // Récupérer exam_assign
        $examAssignStmt = $pdo->prepare("
            SELECT id FROM exam_assigns
            WHERE session_id = ?
            AND classes_id = ?
            AND section_id = ?
            AND exam_type_id = ?
        ");
        $examAssignStmt->execute([$sessionId, $class['classes_id'], $class['section_id'], $examTypeId]);
        $examAssign = $examAssignStmt->fetch(PDO::FETCH_ASSOC);

        if (!$examAssign) continue;

        // Récupérer les étudiants de cette classe
        $studentsStmt = $pdo->prepare("
            SELECT s.id, s.user_id
            FROM students s
            WHERE s.class_id = ?
            AND s.section_id = ?
            AND s.status = 1
            LIMIT 30
        ");
        $studentsStmt->execute([$class['classes_id'], $class['section_id']]);
        $students = $studentsStmt->fetchAll(PDO::FETCH_ASSOC);

        if (empty($students)) continue;

        // Récupérer les matières
        $examSubjectsStmt = $pdo->prepare("
            SELECT eac.id, eac.subject_id, eac.total_marks, s.name as subject_name
            FROM exam_assign_childrens eac
            JOIN subjects s ON eac.subject_id = s.id
            WHERE eac.exam_assign_id = ?
        ");
        $examSubjectsStmt->execute([$examAssign['id']]);
        $examSubjects = $examSubjectsStmt->fetchAll(PDO::FETCH_ASSOC);

        // Créer marks_register pour cette classe
        $checkRegisterStmt = $pdo->prepare("
            SELECT id FROM marks_registers
            WHERE exam_assign_id = ?
        ");
        $checkRegisterStmt->execute([$examAssign['id']]);

        if ($checkRegisterStmt->rowCount() == 0) {
            $insertRegisterStmt = $pdo->prepare("
                INSERT INTO marks_registers (
                    session_id,
                    exam_assign_id,
                    classes_id,
                    section_id,
                    status,
                    created_at,
                    updated_at,
                    branch_id
                ) VALUES (?, ?, ?, ?, 1, NOW(), NOW(), 1)
            ");

            $insertRegisterStmt->execute([
                $sessionId,
                $examAssign['id'],
                $class['classes_id'],
                $class['section_id']
            ]);

            $marksRegisterId = $pdo->lastInsertId();

            // Créer marks_register_childrens pour chaque élève x matière
            foreach ($students as $student) {
                foreach ($examSubjects as $subject) {
                    // Générer notes réalistes
                    $mark = generateRealisticMark($subject['total_marks']);

                    // Simuler absences (5% des élèves absents par matière)
                    $isAbsent = (rand(1, 100) <= 5);

                    $insertMarkStmt = $pdo->prepare("
                        INSERT INTO marks_register_childrens (
                            marks_register_id,
                            student_id,
                            exam_assign_children_id,
                            mark,
                            is_absent,
                            status,
                            created_at,
                            updated_at,
                            branch_id
                        ) VALUES (?, ?, ?, ?, ?, 1, NOW(), NOW(), 1)
                    ");

                    $insertMarkStmt->execute([
                        $marksRegisterId,
                        $student['id'],
                        $subject['id'],
                        $isAbsent ? null : $mark,
                        $isAbsent ? 1 : 0
                    ]);
                }
            }

            echo "   ✅ Notes créées: " . $class['class_name'] . " (" . count($students) . " élèves × " . count($examSubjects) . " matières)\n";
            $registersCreated++;
        }
    }

    echo "\n📊 Total: $registersCreated registres de notes créés\n\n";

    // ============================================
    // 4. CRÉER SCÉNARIOS RÉALISTES - ABSENCES
    // ============================================

    echo "🏥 CRÉATION ABSENCES RÉALISTES\n";
    echo "========================================\n";

    // Récupérer quelques élèves pour créer absences
    $studentsStmt = $pdo->query("
        SELECT s.id, s.user_id, u.first_name, u.last_name, s.class_id, s.section_id
        FROM students s
        JOIN users u ON s.user_id = u.id
        WHERE s.status = 1
        LIMIT 50
    ");
    $students = $studentsStmt->fetchAll(PDO::FETCH_ASSOC);

    $absencesCreated = 0;
    $today = date('Y-m-d');

    foreach ($students as $student) {
        // 20% des élèves ont des absences récentes
        if (rand(1, 100) <= 20) {
            // Créer 1-3 absences sur les 7 derniers jours
            $numAbsences = rand(1, 3);

            for ($i = 0; $i < $numAbsences; $i++) {
                $absenceDate = date('Y-m-d', strtotime("-" . rand(1, 7) . " days"));

                // Vérifier si absence existe déjà
                $checkAbsenceStmt = $pdo->prepare("
                    SELECT id FROM student_attendances
                    WHERE student_id = ? AND date = ?
                ");
                $checkAbsenceStmt->execute([$student['id'], $absenceDate]);

                if ($checkAbsenceStmt->rowCount() == 0) {
                    $insertAbsenceStmt = $pdo->prepare("
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

                    // Raisons d'absence réalistes
                    $reasons = [
                        'Maladie',
                        'Rendez-vous médical',
                        'Problème familial',
                        'Transport',
                        null // Sans justification
                    ];
                    $reason = $reasons[array_rand($reasons)];

                    $insertAbsenceStmt->execute([
                        $sessionId,
                        $student['id'],
                        $student['class_id'],
                        $student['section_id'],
                        $absenceDate,
                        $reason
                    ]);

                    $absencesCreated++;
                }
            }

            echo "   ⚠️ Absences créées pour: " . $student['first_name'] . " " . $student['last_name'] . " ($numAbsences jours)\n";
        }
    }

    echo "\n📊 Total: $absencesCreated absences créées\n\n";

    // ============================================
    // 5. CRÉER MESSAGES PARENTS FÂCHÉS
    // ============================================

    echo "😠 CRÉATION MESSAGES PARENTS FÂCHÉS\n";
    echo "========================================\n";

    $messagesCreated = 0;

    // Récupérer quelques parents
    $parentsStmt = $pdo->query("
        SELECT DISTINCT pg.id, pg.guardians_name, pg.guardians_email, pg.guardians_mobile, s.id as student_id
        FROM parent_guardians pg
        JOIN students s ON pg.student_id = s.id
        WHERE pg.status = 1
        LIMIT 20
    ");
    $parents = $parentsStmt->fetchAll(PDO::FETCH_ASSOC);

    // Messages réalistes de parents fâchés
    $angryMessages = [
        [
            'title' => 'Note injuste en mathématiques',
            'message' => 'Bonjour, je conteste la note de mon fils en mathématiques (8/20). Il avait pourtant bien révisé et mérite au moins 12/20. Je demande une révision urgente de sa copie. Cordialement.'
        ],
        [
            'title' => 'Professeur absent trop souvent',
            'message' => 'C\'est inadmissible! Le professeur de français est absent pour la 3ème fois ce mois-ci! Mon enfant prend du retard et je paie la scolarité complète. J\'exige une explication et un remplaçant qualifié!'
        ],
        [
            'title' => 'Harcèlement dans la cour',
            'message' => 'Mon fils se fait harceler par des élèves de 4AM dans la cour de récréation. Il rentre en pleurant. L\'école doit IMMÉDIATEMENT intervenir! C\'est inacceptable et je tiendrai l\'école responsable.'
        ],
        [
            'title' => 'Retard du bus scolaire',
            'message' => 'Le bus scolaire a 30 minutes de retard TOUS LES JOURS! Mon enfant arrive en retard en classe et manque le début des cours. C\'est du n\'importe quoi. Je veux un remboursement partiel du transport!'
        ],
        [
            'title' => 'Devoirs trop nombreux',
            'message' => 'Les devoirs sont beaucoup trop nombreux! Mon enfant travaille jusqu\'à 22h tous les soirs. C\'est épuisant et contre-productif. Les professeurs doivent coordonner entre eux pour réduire la charge.'
        ],
        [
            'title' => 'Bulletin non disponible',
            'message' => 'Bonjour, cela fait 2 semaines que j\'essaie de télécharger le bulletin de ma fille sur le site et ça ne marche pas. Votre système est défaillant! J\'ai besoin du bulletin AUJOURD\'HUI pour une inscription.'
        ],
        [
            'title' => 'Absence non justifiée marquée à tort',
            'message' => 'Mon enfant a été marqué absent le 15/01 alors qu\'il était présent! J\'ai même la photo de lui en classe. Corrigez cette erreur immédiatement car cela impacte son taux de présence!'
        ],
        [
            'title' => 'Cantine - Qualité médiocre',
            'message' => 'La nourriture de la cantine est vraiment médiocre. Mon fils refuse de manger là-bas. Pour le prix que je paie, j\'attends un minimum de qualité. Revoyez vos menus!'
        ]
    ];

    foreach (array_slice($parents, 0, 8) as $index => $parent) {
        $message = $angryMessages[$index % count($angryMessages)];

        // Créer notice board (message) du parent vers l'école
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

        $noticeDate = date('Y-m-d', strtotime('-' . rand(1, 5) . ' days'));

        $insertNoticeStmt->execute([
            '⚠️ PARENT: ' . $message['title'],
            $sessionId,
            $noticeDate,
            date('Y-m-d H:i:s'),
            "De: " . $parent['guardians_name'] . " (" . $parent['guardians_email'] . ")\n\n" . $message['message']
        ]);

        echo "   😠 Message créé: " . $message['title'] . " (Parent: " . $parent['guardians_name'] . ")\n";
        $messagesCreated++;
    }

    echo "\n📊 Total: $messagesCreated messages parents créés\n\n";

    // ============================================
    // 6. CRÉER SCÉNARIOS PROFS MALADES
    // ============================================

    echo "🤒 CRÉATION ABSENCES ENSEIGNANTS\n";
    echo "========================================\n";

    $teacherAbsencesCreated = 0;

    // Récupérer quelques enseignants
    $teachersStmt = $pdo->query("
        SELECT st.id, st.user_id, u.first_name, u.last_name
        FROM staff st
        JOIN users u ON st.user_id = u.id
        WHERE st.status = 1 AND st.role_id = 4
        LIMIT 10
    ");
    $teachers = $teachersStmt->fetchAll(PDO::FETCH_ASSOC);

    foreach ($teachers as $teacher) {
        // 30% des profs ont eu une absence récente
        if (rand(1, 100) <= 30) {
            $absenceDays = rand(1, 3);
            $absenceDate = date('Y-m-d', strtotime('-' . rand(1, 10) . ' days'));

            // Créer leave (demande de congé/maladie)
            $checkLeaveStmt = $pdo->prepare("
                SELECT id FROM leaves
                WHERE staff_id = ? AND leave_from = ?
            ");
            $checkLeaveStmt->execute([$teacher['id'], $absenceDate]);

            if ($checkLeaveStmt->rowCount() == 0) {
                $leaveTo = date('Y-m-d', strtotime($absenceDate . " +$absenceDays days"));

                $reasons = [
                    'Grippe',
                    'Gastro-entérite',
                    'Migraine sévère',
                    'Urgence familiale',
                    'Rendez-vous médical'
                ];
                $reason = $reasons[array_rand($reasons)];

                $insertLeaveStmt = $pdo->prepare("
                    INSERT INTO leaves (
                        staff_id,
                        leave_type_id,
                        leave_from,
                        leave_to,
                        reason,
                        attachment,
                        apply_date,
                        approve_status,
                        status,
                        created_at,
                        updated_at,
                        branch_id
                    ) VALUES (?, 2, ?, ?, ?, NULL, ?, 1, 1, NOW(), NOW(), 1)
                ");

                $insertLeaveStmt->execute([
                    $teacher['id'],
                    $absenceDate,
                    $leaveTo,
                    $reason,
                    date('Y-m-d', strtotime($absenceDate . ' -1 day'))
                ]);

                echo "   🤒 Congé maladie: " . $teacher['first_name'] . " " . $teacher['last_name'] . " ($absenceDays jours - $reason)\n";
                $teacherAbsencesCreated++;
            }
        }
    }

    echo "\n📊 Total: $teacherAbsencesCreated absences enseignants créées\n\n";

    // ============================================
    // RÉSUMÉ FINAL
    // ============================================

    echo "========================================\n";
    echo "✅ SIMULATION RÉALISTE COMPLÉTÉE\n";
    echo "========================================\n\n";

    echo "📊 RÉSUMÉ:\n";
    echo "   • $examCreated examens créés\n";
    echo "   • $routinesCreated calendriers d'examens\n";
    echo "   • $registersCreated registres de notes avec variations réalistes\n";
    echo "   • $absencesCreated absences élèves\n";
    echo "   • $messagesCreated messages parents fâchés\n";
    echo "   • $teacherAbsencesCreated absences enseignants\n\n";

    echo "🎯 SCÉNARIOS RÉALISTES CRÉÉS:\n";
    echo "   ✅ Examens assignés aux professeurs pour correction\n";
    echo "   ✅ Notes variées (excellents, moyens, faibles élèves)\n";
    echo "   ✅ 5% élèves absents aux examens\n";
    echo "   ✅ 20% élèves avec absences récentes\n";
    echo "   ✅ 8 cas de parents mécontents (notes, profs absents, harcèlement, etc.)\n";
    echo "   ✅ 30% enseignants avec absences maladie\n\n";

    echo "🔄 PROCHAINES ÉTAPES:\n";
    echo "   1. Nettoyer caches Laravel\n";
    echo "   2. Tester examens dans Staff Panel\n";
    echo "   3. Approuver les notes (Admin)\n";
    echo "   4. Publier résultats pour parents/étudiants\n";
    echo "   5. Gérer les messages parents\n\n";

} catch (Exception $e) {
    echo "\n❌ ERREUR: " . $e->getMessage() . "\n\n";
    exit(1);
}

// ============================================
// FONCTIONS AUXILIAIRES
// ============================================

/**
 * Génère une note réaliste suivant distribution normale
 *
 * @param int $totalMarks Note maximale
 * @return float Note générée
 */
function generateRealisticMark($totalMarks) {
    // Distribution réaliste:
    // 10% excellents (16-20)
    // 30% bons (13-15)
    // 40% moyens (10-12)
    // 15% faibles (8-9)
    // 5% très faibles (<8)

    $rand = rand(1, 100);

    if ($rand <= 10) {
        // Excellents
        $mark = rand(16 * 100, 20 * 100) / 100;
    } elseif ($rand <= 40) {
        // Bons
        $mark = rand(13 * 100, 15 * 100) / 100;
    } elseif ($rand <= 80) {
        // Moyens
        $mark = rand(10 * 100, 12 * 100) / 100;
    } elseif ($rand <= 95) {
        // Faibles
        $mark = rand(8 * 100, 9 * 100) / 100;
    } else {
        // Très faibles
        $mark = rand(4 * 100, 7 * 100) / 100;
    }

    // Ajuster selon le total de points
    $mark = ($mark / 20) * $totalMarks;

    // Arrondir à 0.5 près (notes réalistes: 14, 14.5, 15, etc.)
    $mark = round($mark * 2) / 2;

    return $mark;
}
