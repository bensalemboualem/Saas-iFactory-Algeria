<?php
/**
 * TRADUCTION COMPLÈTE DE TOUS LES MODULES
 * Ajoute toutes les traductions arabes manquantes dans les fichiers JSON
 */

echo "=== TRADUCTION COMPLÈTE DES MODULES ===\n\n";

$translations = [
    // Student Info
    'student' => 'الطالب',
    'Student' => 'الطالب',
    'admission' => 'القبول',
    'Admission' => 'القبول',
    'student_list' => 'قائمة الطلاب',
    'Student List' => 'قائمة الطلاب',
    'student_promote' => 'ترقية الطالب',
    'Student Promote' => 'ترقية الطالب',
    'disabled_students' => 'الطلاب المعطلون',
    'Disabled Students' => 'الطلاب المعطلون',

    // Attendance
    'attendance' => 'الحضور',
    'Attendance' => 'الحضور',
    'student_attendance' => 'حضور الطالب',
    'Student Attendance' => 'حضور الطالب',
    'attendance_report' => 'تقرير الحضور',
    'Attendance Report' => 'تقرير الحضور',

    // Leave
    'leave' => 'الإجازة',
    'Leave' => 'الإجازة',
    'leave_type' => 'نوع الإجازة',
    'Leave Type' => 'نوع الإجازة',
    'leave_request' => 'طلب إجازة',
    'Leave Request' => 'طلب إجازة',
    'leave_list' => 'قائمة الإجازات',
    'Leave List' => 'قائمة الإجازات',

    // Fees
    'fees' => 'الرسوم',
    'Fees' => 'الرسوم',
    'fees_group' => 'مجموعة الرسوم',
    'Fees Group' => 'مجموعة الرسوم',
    'fees_type' => 'نوع الرسوم',
    'Fees Type' => 'نوع الرسوم',
    'fees_master' => 'رئيس الرسوم',
    'Fees Master' => 'رئيس الرسوم',
    'fees_assign' => 'تعيين الرسوم',
    'Fees Assign' => 'تعيين الرسوم',
    'fees_collect' => 'تحصيل الرسوم',
    'Fees Collect' => 'تحصيل الرسوم',

    // Examination
    'examination' => 'الامتحان',
    'Examination' => 'الامتحان',
    'exam' => 'امتحان',
    'Exam' => 'امتحان',
    'exam_setup' => 'إعداد الامتحان',
    'Exam Setup' => 'إعداد الامتحان',
    'exam_routine' => 'جدول الامتحان',
    'Exam Routine' => 'جدول الامتحان',
    'marks_register' => 'سجل الدرجات',
    'Marks Register' => 'سجل الدرجات',
    'marks_grade' => 'درجة العلامات',
    'Marks Grade' => 'درجة العلامات',

    // Accounts
    'income' => 'الدخل',
    'Income' => 'الدخل',
    'expense' => 'المصروفات',
    'Expense' => 'المصروفات',
    'account' => 'الحساب',
    'Account' => 'الحساب',

    // Report
    'student_report' => 'تقرير الطالب',
    'Student Report' => 'تقرير الطالب',
    'fees_report' => 'تقرير الرسوم',
    'Fees Report' => 'تقرير الرسوم',

    // Users & Roles
    'role' => 'الدور',
    'Role' => 'الدور',
    'permission' => 'الصلاحية',
    'Permission' => 'الصلاحية',
];

// Fonction pour mettre à jour un fichier JSON
function updateJsonFile($filePath, $translations) {
    if (!file_exists($filePath)) {
        return 0;
    }

    $content = file_get_contents($filePath);
    $json = json_decode($content, true);

    if ($json === null) {
        return 0;
    }

    $updated = 0;

    foreach ($json as $key => $value) {
        // Si on a une traduction et que la valeur actuelle n'est pas en arabe
        if (isset($translations[$key]) && !preg_match('/[\x{0600}-\x{06FF}]/u', $value)) {
            $json[$key] = $translations[$key];
            $updated++;
        } elseif (isset($translations[$value])) {
            $json[$key] = $translations[$value];
            $updated++;
        }
    }

    if ($updated > 0) {
        file_put_contents($filePath, json_encode($json, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
    }

    return $updated;
}

// Traiter tous les fichiers JSON
$langDir = __DIR__ . '/lang/ar/';
$jsonFiles = glob($langDir . '*.json');

$totalUpdated = 0;

foreach ($jsonFiles as $filePath) {
    $fileName = basename($filePath);
    $updated = updateJsonFile($filePath, $translations);

    if ($updated > 0) {
        echo "✅ $fileName: $updated traduction(s) mise(s) à jour\n";
        $totalUpdated += $updated;
    }
}

echo "\n=== TRADUCTION TERMINÉE ===\n\n";
echo "Total: $totalUpdated traduction(s) mise(s) à jour\n\n";

echo "PROCHAINES ÉTAPES:\n";
echo "1. Nettoyez les caches:\n";
echo "   \"C:/xampp/php/php.exe\" CLEAR_ALL_CACHES_FINAL.php\n\n";
echo "2. Vérifiez les modules:\n";
echo "   \"C:/xampp/php/php.exe\" scanner_modules_anglais.php\n\n";
echo "3. Déconnectez-vous et reconnectez-vous\n\n";

echo "✅ MODULES TRADUITS EN ARABE!\n";
