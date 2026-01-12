<?php
/**
 * SCANNER TOUS LES MODULES POUR TROUVER L'ANGLAIS RESTANT
 */

require __DIR__.'/vendor/autoload.php';
$app = require_once __DIR__.'/bootstrap/app.php';
$kernel = $app->make('Illuminate\Contracts\Console\Kernel');
$kernel->bootstrap();

Session::put('locale', 'ar');

echo "=== SCAN DES MODULES POUR ANGLAIS RESTANT ===\n\n";

// Liste des modules/catégories à vérifier
$modules = [
    // Menu principal
    'dashboard' => [
        'dashboard.Dashboard',
        'dashboard.welcome',
    ],

    // Student Info
    'student_info' => [
        'student_info.student',
        'student_info.admission',
        'student_info.student_list',
        'student_info.student_promote',
        'student_info.disabled_students',
        'common.Student',
    ],

    // Academic
    'academic' => [
        'academic.class',
        'academic.section',
        'academic.shift',
        'academic.class_setup',
        'academic.subject',
        'academic.subject_assign',
        'academic.class_room',
        'academic.teacher',
    ],

    // Routines
    'routines' => [
        'settings.class_routine',
        'settings.exam_routine',
    ],

    // Attendance
    'attendance' => [
        'attendance.attendance',
        'attendance.student_attendance',
        'attendance.attendance_report',
    ],

    // Leave
    'leave' => [
        'leave.leave',
        'leave.leave_type',
        'leave.leave_request',
        'leave.leave_list',
    ],

    // Fees
    'fees' => [
        'fees.fees',
        'fees.fees_group',
        'fees.fees_type',
        'fees.fees_master',
        'fees.fees_assign',
        'fees.fees_collect',
    ],

    // Examination
    'examination' => [
        'examination.examination',
        'examination.exam',
        'examination.exam_setup',
        'examination.exam_routine',
        'examination.marks_register',
        'examination.marks_grade',
    ],

    // Library
    'library' => [
        'settings.Library',
        'settings.book_category',
        'settings.Book',
        'settings.member_category',
        'settings.Member',
        'settings.issue_book',
    ],

    // Accounts
    'accounts' => [
        'account.income',
        'account.expense',
        'account.account',
    ],

    // Report
    'report' => [
        'report.student_report',
        'report.attendance_report',
        'report.fees_report',
    ],

    // Staff
    'staff' => [
        'staff.staff',
        'staff.staff_list',
        'staff.add_staff',
        'users_roles.role',
        'users_roles.permission',
    ],

    // Settings
    'settings' => [
        'settings.general_settings',
        'settings.email_settings',
        'settings.sms_settings',
    ],
];

$issues = [];
$totalChecked = 0;
$arabicCount = 0;
$englishCount = 0;

foreach ($modules as $moduleName => $keys) {
    echo "MODULE: " . strtoupper($moduleName) . "\n";

    foreach ($keys as $key) {
        $totalChecked++;
        $result = ___($key);
        $hasArabic = preg_match('/[\x{0600}-\x{06FF}]/u', $result);

        if ($hasArabic) {
            echo "   ✅ $key → $result\n";
            $arabicCount++;
        } else {
            echo "   ❌ $key → $result (ANGLAIS!)\n";
            $englishCount++;
            $issues[] = [
                'module' => $moduleName,
                'key' => $key,
                'value' => $result
            ];
        }
    }
    echo "\n";
}

echo str_repeat("=", 70) . "\n\n";

echo "RÉSUMÉ DU SCAN:\n";
echo "   Total vérifié: $totalChecked\n";
echo "   ✅ En arabe: $arabicCount\n";
echo "   ❌ En anglais: $englishCount\n\n";

if ($englishCount > 0) {
    echo "TERMES EN ANGLAIS TROUVÉS:\n\n";

    $byModule = [];
    foreach ($issues as $issue) {
        $byModule[$issue['module']][] = $issue;
    }

    foreach ($byModule as $module => $moduleIssues) {
        echo "Module: $module\n";
        foreach ($moduleIssues as $issue) {
            echo "   - {$issue['key']} → \"{$issue['value']}\"\n";
        }
        echo "\n";
    }

    echo "PROCHAINE ÉTAPE:\n";
    echo "Créer un script de traduction pour ces termes manquants.\n\n";
} else {
    echo "✅ ✅ ✅ PARFAIT! ✅ ✅ ✅\n";
    echo "Tous les modules sont en arabe!\n\n";
}

echo str_repeat("=", 70) . "\n";
