<?php
/**
 * CORRECTION DES MODULES SPÉCIFIQUES
 * Online Examination, Leave, Contact, Accounts, Staff, Forums
 */

echo "\n========================================\n";
echo "CORRECTION MODULES SPÉCIFIQUES\n";
echo "========================================\n\n";

$langPath = __DIR__ . '/lang/ar';

// Traductions manquantes pour chaque module
$corrections = [
    'online-examination.json' => [
        'Question Group' => 'مجموعة الأسئلة',
        'question_group' => 'مجموعة الأسئلة',
        'Question Bank' => 'بنك الأسئلة',
        'question_bank' => 'بنك الأسئلة',
        'Online Exam' => 'الامتحان عبر الإنترنت',
        'online_exam' => 'الامتحان عبر الإنترنت',
        'Homeworks' => 'الواجبات المنزلية',
        'homeworks' => 'الواجبات المنزلية',
        'Gmeet' => 'جوجل ميت',
        'gmeet' => 'جوجل ميت',
    ],

    'leave.json' => [
        'Request' => 'طلب',
        'Request Log' => 'سجل الطلبات',
    ],

    'live_chat.json' => [
        'Active' => 'نشط',
        'Search' => 'بحث',
        'Conversation List' => 'قائمة المحادثات',
    ],

    'livechat.json' => [
        'Active' => 'نشط',
        'Search' => 'بحث',
        'Conversation List' => 'قائمة المحادثات',
        'Live_Chat' => 'الدردشة المباشرة',
        'Live Chat' => 'الدردشة المباشرة',
    ],

    'account.json' => [
        'account_head' => 'رأس الحساب',
        'Account Head' => 'رأس الحساب',
        'Enter Sibling Order' => 'أدخل ترتيب الأخوة',
        'enter_amount' => 'أدخل المبلغ',
        'Enter Amount' => 'أدخل المبلغ',
    ],

    'staff.json' => [
        'Designations' => 'المناصب',
        'designations' => 'المناصب',
        'Emergency Contact' => 'جهة اتصال الطوارئ',
        'emergency_contact' => 'جهة اتصال الطوارئ',
        'Enter Emergency Contact' => 'أدخل جهة اتصال الطوارئ',
        'enter_emergency_contact' => 'أدخل جهة اتصال الطوارئ',
        'Unmarried' => 'أعزب',
        'unmarried' => 'أعزب',
        'Married' => 'متزوج',
        'married' => 'متزوج',
        'Documents' => 'الوثائق',
        'documents' => 'الوثائق',
    ],

    'common.json' => [
        'communication' => 'التواصل',
        'Communication' => 'التواصل',
        'Contact' => 'اتصل بنا',
        'contact' => 'اتصل بنا',
    ],
];

$totalCorrections = 0;

foreach ($corrections as $fileName => $translations) {
    $filePath = $langPath . '/' . $fileName;

    echo "📝 Module: $fileName\n";

    if (!file_exists($filePath)) {
        echo "⚠️  Fichier non trouvé, création...\n";
        file_put_contents($filePath, json_encode([], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
    }

    $content = file_get_contents($filePath);
    $data = json_decode($content, true);

    if ($data === null) {
        echo "❌ Erreur de décodage JSON\n";
        continue;
    }

    $corrected = 0;

    foreach ($translations as $key => $value) {
        if (!isset($data[$key]) || $data[$key] === $key || empty($data[$key])) {
            $data[$key] = $value;
            echo "  ✓ '$key' → '$value'\n";
            $corrected++;
        } elseif ($data[$key] !== $value) {
            // Mise à jour si valeur différente
            $data[$key] = $value;
            echo "  🔄 '$key' mis à jour → '$value'\n";
            $corrected++;
        }
    }

    if ($corrected > 0) {
        $json = json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
        file_put_contents($filePath, $json);
        echo "✅ $corrected correction(s) dans $fileName\n\n";
        $totalCorrections += $corrected;
    } else {
        echo "✅ Aucune correction nécessaire\n\n";
    }
}

echo "========================================\n";
echo "📊 TOTAL: $totalCorrections corrections\n";
echo "========================================\n\n";

echo "✅ TERMINÉ!\n";
echo "⚠️  Nettoyez les caches:\n";
echo '   "C:/xampp/php/php.exe" CLEAR_ALL_CACHES_FINAL.php' . "\n\n";
