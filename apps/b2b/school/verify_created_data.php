<?php
$pdo = new PDO('mysql:host=localhost;dbname=onest_school', 'root', '');

echo "========================================\n";
echo "VÉRIFICATION DES DONNÉES CRÉÉES\n";
echo "========================================\n\n";

// Check exams
echo "1. EXAMENS CRÉÉS:\n";
$stmt = $pdo->query("
    SELECT ea.id, c.name as class_name, sec.name as section_name,
           sub.name as subject_name, et.name as exam_type
    FROM exam_assigns ea
    JOIN classes c ON ea.classes_id = c.id
    JOIN sections sec ON ea.section_id = sec.id
    JOIN subjects sub ON ea.subject_id = sub.id
    JOIN exam_types et ON ea.exam_type_id = et.id
    WHERE ea.session_id = 1
");
$exams = $stmt->fetchAll(PDO::FETCH_ASSOC);
echo "Total: " . count($exams) . " examens\n";
foreach ($exams as $exam) {
    echo "  - {$exam['class_name']}/{$exam['section_name']}: {$exam['subject_name']} ({$exam['exam_type']})\n";
}

// Check grades
echo "\n2. NOTES CRÉÉES:\n";
$stmt = $pdo->query("
    SELECT COUNT(*) as total FROM marks_register_childrens
");
$gradesCount = $stmt->fetchColumn();
echo "Total: $gradesCount notes entrées\n";

$stmt = $pdo->query("
    SELECT mr.id, c.name as class_name, sec.name as section_name,
           sub.name as subject_name, COUNT(mrc.id) as student_count
    FROM marks_registers mr
    JOIN marks_register_childrens mrc ON mr.id = mrc.marks_register_id
    JOIN classes c ON mr.classes_id = c.id
    JOIN sections sec ON mr.section_id = sec.id
    JOIN subjects sub ON mr.subject_id = sub.id
    WHERE mr.session_id = 1
    GROUP BY mr.id
");
$marksRegisters = $stmt->fetchAll(PDO::FETCH_ASSOC);
foreach ($marksRegisters as $mr) {
    echo "  - {$mr['class_name']}/{$mr['section_name']}: {$mr['subject_name']} ({$mr['student_count']} élèves notés)\n";
}

// Check exam routines
echo "\n3. CALENDRIER D'EXAMENS:\n";
$stmt = $pdo->query("
    SELECT er.*, c.name as class_name, sec.name as section_name
    FROM exam_routines er
    JOIN classes c ON er.classes_id = c.id
    JOIN sections sec ON er.section_id = sec.id
    WHERE er.session_id = 1
");
$routines = $stmt->fetchAll(PDO::FETCH_ASSOC);
echo "Total: " . count($routines) . " calendriers\n";
foreach ($routines as $routine) {
    echo "  - {$routine['class_name']}/{$routine['section_name']}: {$routine['date']}\n";
}

// Check student absences
echo "\n4. ABSENCES ÉLÈVES:\n";
$stmt = $pdo->query("
    SELECT a.*, s.first_name, s.last_name, c.name as class_name
    FROM attendances a
    JOIN students s ON a.student_id = s.id
    JOIN classes c ON a.classes_id = c.id
    WHERE a.attendance = 0
    AND a.session_id = 1
    ORDER BY a.date DESC
");
$absences = $stmt->fetchAll(PDO::FETCH_ASSOC);
echo "Total: " . count($absences) . " absences\n";
foreach ($absences as $absence) {
    echo "  - {$absence['first_name']} {$absence['last_name']} ({$absence['class_name']}): {$absence['date']} - {$absence['note']}\n";
}

// Check teacher leaves
echo "\n5. CONGÉS ENSEIGNANTS:\n";
$stmt = $pdo->query("
    SELECT lr.*, s.first_name, s.last_name, lt.name as leave_type
    FROM leave_requests lr
    JOIN staff s ON lr.user_id = s.user_id
    JOIN leave_types lt ON lr.leave_type_id = lt.id
    WHERE lr.session_id = 1
    ORDER BY lr.start_date DESC
");
$leaves = $stmt->fetchAll(PDO::FETCH_ASSOC);
echo "Total: " . count($leaves) . " congés\n";
foreach ($leaves as $leave) {
    echo "  - {$leave['first_name']} {$leave['last_name']}: {$leave['start_date']} à {$leave['end_date']} ({$leave['leave_days']} jours)\n";
    echo "    Raison: {$leave['description']}\n";
}

// Check parent messages
echo "\n6. MESSAGES PARENTS:\n";
$stmt = $pdo->query("
    SELECT nb.*, s.first_name, s.last_name
    FROM notice_boards nb
    LEFT JOIN students s ON nb.student_id = s.id
    WHERE nb.session_id = 1
    AND nb.title LIKE '%🔴%' OR nb.title LIKE '%😤%' OR nb.title LIKE '%⚠️%'
        OR nb.title LIKE '%🚌%' OR nb.title LIKE '%📚%' OR nb.title LIKE '%💻%'
        OR nb.title LIKE '%❌%' OR nb.title LIKE '%🍽️%'
    ORDER BY nb.created_at DESC
");
$messages = $stmt->fetchAll(PDO::FETCH_ASSOC);
echo "Total: " . count($messages) . " messages de parents fâchés\n";
foreach ($messages as $msg) {
    $studentName = $msg['first_name'] ? "{$msg['first_name']} {$msg['last_name']}" : "N/A";
    echo "  - {$msg['title']}\n";
    echo "    Étudiant: $studentName\n";
    echo "    Date: {$msg['publish_date']}\n\n";
}

echo "\n========================================\n";
echo "VÉRIFICATION TERMINÉE\n";
echo "========================================\n";
