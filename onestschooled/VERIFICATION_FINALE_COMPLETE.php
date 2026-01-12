<?php
/**
 * VÉRIFICATION FINALE ET COMPLÈTE
 * Vérifie ligne par ligne tous les fichiers JSON pour s'assurer qu'il ne reste AUCUN terme anglais
 */

echo "\n========================================\n";
echo "VÉRIFICATION FINALE COMPLÈTE\n";
echo "========================================\n\n";

$langPath = __DIR__ . '/lang';

// Liste complète de mots anglais à détecter
$englishWords = [
    // Common words
    'the', 'is', 'are', 'and', 'or', 'of', 'to', 'in', 'on', 'at', 'for', 'with', 'by', 'from',

    // Actions
    'Add', 'Edit', 'Delete', 'Update', 'Save', 'Cancel', 'Submit', 'Search', 'View', 'Print',
    'Export', 'Import', 'Download', 'Upload', 'Back', 'Next', 'Previous', 'Close', 'Select',

    // Status
    'Active', 'Inactive', 'Pending', 'Approved', 'Rejected', 'Status', 'Action', 'Actions',

    // Common terms
    'Yes', 'No', 'All', 'Name', 'Email', 'Phone', 'Address', 'Date', 'Time', 'Description',
    'Details', 'Type', 'Category', 'Amount', 'Total', 'From', 'To',

    // School terms
    'Student', 'Students', 'Teacher', 'Teachers', 'Parent', 'Parents', 'Staff',
    'Class', 'Classes', 'Section', 'Sections', 'Subject', 'Subjects',
    'Session', 'Sessions', 'School', 'Academic', 'Dashboard', 'Home',

    // Modules
    'Attendance', 'Leave', 'Fees', 'Examination', 'Exam', 'Library', 'Book', 'Books',
    'Accounts', 'Income', 'Expense', 'Report', 'Reports', 'Settings',

    // Fees related
    'Payment', 'Method', 'Cash', 'Cheque', 'Bank', 'Transfer', 'Online',
    'Paid', 'Unpaid', 'Partial', 'Due', 'Balance', 'Discount', 'Fine',

    // Attendance
    'Present', 'Absent', 'Late', 'Half', 'Day', 'Daily',

    // Exam
    'Marks', 'Grade', 'Result', 'Pass', 'Fail', 'Question', 'Answer',

    // General
    'First', 'Last', 'Male', 'Female', 'Gender', 'Blood', 'Group',
    'Father', 'Mother', 'Guardian', 'Mobile', 'City', 'State', 'Zip', 'Code',
    'Photo', 'Certificate', 'Card', 'Number', 'Roll', 'Admission',

    // Library
    'Author', 'Publisher', 'ISBN', 'Quantity', 'Available', 'Issued',
    'Issue', 'Return', 'Member', 'Members',

    // Staff
    'Role', 'Roles', 'Department', 'Departments', 'Designation', 'Salary',
    'Basic', 'Joining', 'Qualification', 'Experience', 'Permission', 'Permissions',

    // Settings
    'General', 'System', 'Language', 'Currency', 'Zone', 'Format', 'Logo',
    'Current', 'Website',

    // Additional
    'Profile', 'Logout', 'Login', 'Password', 'Change', 'Forgot', 'Reset',
    'Remember', 'Me', 'Notification', 'Notifications', 'Message', 'Messages',
    'Inbox', 'Sent', 'Compose', 'Reply', 'Forward', 'Notice', 'Board',
    'Event', 'Events', 'Calendar', 'Homework', 'Assignment', 'Download',
    'Center', 'Gallery', 'Video', 'Forums', 'Memories', 'Transport',
    'Vehicle', 'Route', 'Hostel', 'Room', 'Dormitory', 'Inventory',
    'Item', 'Store',

    // Phrases
    'Time Schedule', 'Class Room', 'Class Routine', 'Student Info', 'Student List',
    'Add Student', 'Student Admission', 'Student Details', 'Admission Number',
    'Roll Number', 'First Name', 'Last Name', 'Date of Birth', 'Blood Group',
    'Father Name', 'Mother Name', 'ID Card', 'Transfer Certificate',
    'Daily Attendance', 'Subject Attendance', 'Attendance Report',
    'Leave Type', 'Leave Define', 'Leave Request', 'Apply Leave', 'Leave List',
    'Fees Group', 'Fees Type', 'Fees Master', 'Fees Assign', 'Fees Collect',
    'Fees Collection', 'Fees Report', 'Fees Invoice', 'Payment Method',
    'Bank Transfer', 'Exam Setup', 'Exam Schedule', 'Exam Routine',
    'Marks Register', 'Marks Grade', 'Marks Distribution', 'Grade Point',
    'Pass Mark', 'Full Marks', 'Online Exam', 'Question Bank',
    'Book List', 'Add Book', 'Book Category', 'Book Number', 'Issue Book',
    'Return Book', 'Issue Date', 'Return Date', 'Income Head', 'Expense Head',
    'Add Income', 'Add Expense', 'Chart of Account', 'Staff List', 'Add Staff',
    'Staff Details', 'Staff Manage', 'Basic Salary', 'Joining Date',
    'General Settings', 'System Settings', 'Email Settings', 'SMS Settings',
    'Payment Settings', 'School Name', 'School Code', 'School Logo',
    'School Address', 'School Phone', 'School Email', 'Academic Year',
    'Current Session', 'Change Password', 'Forgot Password', 'Reset Password',
    'Remember Me', 'Notice Board', 'Download Center', 'Video Gallery',
    'Character Certificate', 'Bonafide Certificate', 'Certificate Generate',
    'ID Card Generate', 'Complain List', 'Postal Receive', 'Postal Dispatch',
    'Front CMS', 'Admission Query', 'Visitor Book', 'Phone Call Log',
    'Module Manager', 'Half Day',

    // More specific terms
    'teacher', 'fees_collection', 'Revenue', 'Promote Students', 'Disabled Students',
    'Caste', 'Religion', 'Zip Code', 'Profit', 'Loss', 'Transaction', 'Invoice',
    'Receipt', 'Voucher', 'Mark Sheet', 'Progress Card', 'Merit List', 'Generate Report',
    'Generate', 'Promote', 'Disabled', 'Setup', 'Backup', 'Utilities', 'Complain',
    'Postal', 'Visitor', 'Call', 'Query', 'Approve', 'Reject', 'Created', 'Updated',
];

// Fonction pour détecter les termes anglais dans une chaîne
function containsEnglish($string, $englishWords) {
    $string = strtolower($string);
    foreach ($englishWords as $word) {
        $wordLower = strtolower($word);
        // Recherche du mot complet (avec limites de mots)
        if (preg_match('/\b' . preg_quote($wordLower, '/') . '\b/i', $string)) {
            return $word;
        }
    }
    return false;
}

// Fonction pour vérifier un fichier JSON
function verifyJsonFile($filePath, $englishWords, $langName) {
    if (!file_exists($filePath)) {
        return ['missing' => true];
    }

    $content = file_get_contents($filePath);
    $data = json_decode($content, true);

    if ($data === null) {
        return ['error' => 'Invalid JSON'];
    }

    $issues = [];

    foreach ($data as $key => $value) {
        // Vérifier la valeur
        if (is_string($value)) {
            $englishTerm = containsEnglish($value, $englishWords);
            if ($englishTerm) {
                $issues[] = [
                    'key' => $key,
                    'value' => $value,
                    'english_term' => $englishTerm
                ];
            }
        }
    }

    return [
        'total_keys' => count($data),
        'issues' => $issues,
        'issues_count' => count($issues)
    ];
}

// Vérifier ARABE
echo "🇩🇿 VÉRIFICATION ARABE\n";
echo "======================\n\n";

$arPath = $langPath . '/ar';
$arabicFiles = [
    'dashboard.json',
    'common.json',
    'academic.json',
    'student_info.json',
    'attendance.json',
    'leave.json',
    'fees.json',
    'examination.json',
    'report.json',
    'staff.json',
    'settings.json',
];

$totalArabicIssues = 0;
$arabicResults = [];

foreach ($arabicFiles as $file) {
    $filePath = $arPath . '/' . $file;
    $result = verifyJsonFile($filePath, $englishWords, 'ar');

    if (isset($result['missing'])) {
        echo "⚠️  $file: Fichier manquant\n";
        continue;
    }

    if (isset($result['error'])) {
        echo "❌ $file: {$result['error']}\n";
        continue;
    }

    if ($result['issues_count'] > 0) {
        echo "❌ $file: {$result['issues_count']} termes anglais trouvés\n";
        foreach ($result['issues'] as $issue) {
            echo "   - Clé '{$issue['key']}': '{$issue['value']}' contient '{$issue['english_term']}'\n";
        }
        $totalArabicIssues += $result['issues_count'];
    } else {
        echo "✅ $file: 100% arabe ({$result['total_keys']} clés)\n";
    }

    $arabicResults[$file] = $result;
}

echo "\n📊 ARABE: ";
if ($totalArabicIssues == 0) {
    echo "✅ AUCUN terme anglais trouvé! PARFAIT!\n\n";
} else {
    echo "❌ $totalArabicIssues termes anglais trouvés\n\n";
}

// Vérifier FRANÇAIS
echo "🇫🇷 VÉRIFICATION FRANÇAIS\n";
echo "=========================\n\n";

$frPath = $langPath . '/fr';
$totalFrenchIssues = 0;
$frenchResults = [];

foreach ($arabicFiles as $file) {
    $filePath = $frPath . '/' . $file;
    $result = verifyJsonFile($filePath, $englishWords, 'fr');

    if (isset($result['missing'])) {
        echo "⚠️  $file: Fichier manquant\n";
        continue;
    }

    if (isset($result['error'])) {
        echo "❌ $file: {$result['error']}\n";
        continue;
    }

    if ($result['issues_count'] > 0) {
        echo "❌ $file: {$result['issues_count']} termes anglais trouvés\n";
        foreach ($result['issues'] as $issue) {
            echo "   - Clé '{$issue['key']}': '{$issue['value']}' contient '{$issue['english_term']}'\n";
        }
        $totalFrenchIssues += $result['issues_count'];
    } else {
        echo "✅ $file: 100% français ({$result['total_keys']} clés)\n";
    }

    $frenchResults[$file] = $result;
}

echo "\n📊 FRANÇAIS: ";
if ($totalFrenchIssues == 0) {
    echo "✅ AUCUN terme anglais trouvé! PARFAIT!\n\n";
} else {
    echo "❌ $totalFrenchIssues termes anglais trouvés\n\n";
}

// RÉSUMÉ FINAL
echo "\n========================================\n";
echo "RÉSUMÉ FINAL\n";
echo "========================================\n";
echo "🇩🇿 Arabe: ";
if ($totalArabicIssues == 0) {
    echo "✅ 100% CLEAN\n";
} else {
    echo "❌ $totalArabicIssues problèmes\n";
}

echo "🇫🇷 Français: ";
if ($totalFrenchIssues == 0) {
    echo "✅ 100% CLEAN\n";
} else {
    echo "❌ $totalFrenchIssues problèmes\n";
}

echo "\n";
if ($totalArabicIssues == 0 && $totalFrenchIssues == 0) {
    echo "🎉 FÉLICITATIONS! AUCUN TERME ANGLAIS DÉTECTÉ!\n";
    echo "✅ Le système est PRÊT pour la présentation!\n";
} else {
    echo "⚠️  ATTENTION: Des termes anglais subsistent\n";
    echo "   Il faut corriger " . ($totalArabicIssues + $totalFrenchIssues) . " termes avant la présentation\n";
}

echo "========================================\n\n";

?>
