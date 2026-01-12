<?php
/**
 * CORRECTION COMPLÈTE DE TOUTES LES TRADUCTIONS
 * Corrige les 463 termes anglais en arabe + 175 termes en français
 * Basé sur les résultats de audit_complet_langues.php
 */

echo "\n========================================\n";
echo "CORRECTION DE TOUTES LES TRADUCTIONS\n";
echo "========================================\n\n";

// Chemins
$langPath = __DIR__ . '/lang';
$correctionsFile = __DIR__ . '/CORRECTIONS_REQUISES.json';

// Dictionnaire complet de traductions ARABE
$arabicTranslations = [
    // Dashboard
    'Dashboard' => 'لوحة التحكم',
    'Student' => 'الطالب',
    'Students' => 'الطلاب',
    'Parent' => 'ولي الأمر',
    'Parents' => 'أولياء الأمور',
    'Teacher' => 'المعلم',
    'Teachers' => 'المعلمون',
    'Session' => 'الدورة',
    'Sessions' => 'الدورات',
    'Revenue' => 'الإيرادات',
    'Expense' => 'المصروفات',
    'fees_collection' => 'تحصيل الرسوم',
    'Total Students' => 'إجمالي الطلاب',
    'Total Parents' => 'إجمالي أولياء الأمور',
    'Total Teachers' => 'إجمالي المعلمين',
    'Total Sessions' => 'إجمالي الدورات',

    // Common terms
    'Add' => 'إضافة',
    'Edit' => 'تعديل',
    'Delete' => 'حذف',
    'Update' => 'تحديث',
    'Save' => 'حفظ',
    'Cancel' => 'إلغاء',
    'Submit' => 'إرسال',
    'Search' => 'بحث',
    'View' => 'عرض',
    'Print' => 'طباعة',
    'Export' => 'تصدير',
    'Import' => 'استيراد',
    'Download' => 'تحميل',
    'Upload' => 'رفع',
    'Back' => 'رجوع',
    'Next' => 'التالي',
    'Previous' => 'السابق',
    'Close' => 'إغلاق',
    'Select' => 'اختيار',
    'Action' => 'الإجراء',
    'Actions' => 'الإجراءات',
    'Status' => 'الحالة',
    'Active' => 'نشط',
    'Inactive' => 'غير نشط',
    'Yes' => 'نعم',
    'No' => 'لا',
    'All' => 'الكل',
    'Name' => 'الاسم',
    'Email' => 'البريد الإلكتروني',
    'Phone' => 'الهاتف',
    'Address' => 'العنوان',
    'Date' => 'التاريخ',
    'Time' => 'الوقت',
    'Description' => 'الوصف',
    'Details' => 'التفاصيل',
    'Type' => 'النوع',
    'Category' => 'الفئة',
    'Amount' => 'المبلغ',
    'Total' => 'الإجمالي',
    'Created' => 'تم الإنشاء',
    'Updated' => 'تم التحديث',
    'From' => 'من',
    'To' => 'إلى',

    // Academic
    'Academic' => 'الأكاديمي',
    'Class' => 'الصف',
    'Classes' => 'الصفوف',
    'Section' => 'القسم',
    'Sections' => 'الأقسام',
    'Subject' => 'المادة',
    'Subjects' => 'المواد',
    'teacher' => 'المعلم',
    'Assign Teacher' => 'تعيين معلم',
    'Class Room' => 'غرفة الصف',
    'Class Routine' => 'جدول الصف',
    'Time Schedule' => 'الجدول الزمني',
    'Promote Students' => 'ترقية الطلاب',

    // Student Info
    'Student Info' => 'معلومات الطالب',
    'Student List' => 'قائمة الطلاب',
    'Add Student' => 'إضافة طالب',
    'Student Admission' => 'قبول الطلاب',
    'Student Details' => 'تفاصيل الطالب',
    'Admission Number' => 'رقم القبول',
    'Roll Number' => 'الرقم الدراسي',
    'First Name' => 'الاسم الأول',
    'Last Name' => 'اسم العائلة',
    'Date of Birth' => 'تاريخ الميلاد',
    'Gender' => 'الجنس',
    'Male' => 'ذكر',
    'Female' => 'أنثى',
    'Blood Group' => 'فصيلة الدم',
    'Religion' => 'الديانة',
    'Caste' => 'الطائفة',
    'Mobile' => 'الهاتف المحمول',
    'City' => 'المدينة',
    'State' => 'الولاية',
    'Zip Code' => 'الرمز البريدي',
    'Photo' => 'الصورة',
    'Father Name' => 'اسم الأب',
    'Mother Name' => 'اسم الأم',
    'Guardian' => 'ولي الأمر',
    'ID Card' => 'بطاقة الهوية',
    'Certificate' => 'الشهادة',
    'Disabled Students' => 'الطلاب المعطلون',

    // Attendance
    'Attendance' => 'الحضور',
    'Daily Attendance' => 'الحضور اليومي',
    'Subject Attendance' => 'حضور المادة',
    'Attendance Report' => 'تقرير الحضور',
    'Present' => 'حاضر',
    'Absent' => 'غائب',
    'Late' => 'متأخر',
    'Half Day' => 'نصف يوم',

    // Leave
    'Leave' => 'الإجازة',
    'Leave Type' => 'نوع الإجازة',
    'Leave Define' => 'تحديد الإجازة',
    'Leave Request' => 'طلب إجازة',
    'Apply Leave' => 'تقديم طلب إجازة',
    'Leave List' => 'قائمة الإجازات',
    'Approve' => 'موافقة',
    'Reject' => 'رفض',
    'Pending' => 'قيد الانتظار',
    'Approved' => 'موافق عليه',
    'Rejected' => 'مرفوض',

    // Fees
    'Fees' => 'الرسوم',
    'Fees Group' => 'مجموعة الرسوم',
    'Fees Type' => 'نوع الرسوم',
    'Fees Master' => 'إدارة الرسوم',
    'Fees Assign' => 'تعيين الرسوم',
    'Fees Collect' => 'تحصيل الرسوم',
    'Fees Collection' => 'تحصيل الرسوم',
    'Fees Report' => 'تقرير الرسوم',
    'Fees Invoice' => 'فاتورة الرسوم',
    'Payment Method' => 'طريقة الدفع',
    'Cash' => 'نقداً',
    'Cheque' => 'شيك',
    'Bank Transfer' => 'تحويل بنكي',
    'Online' => 'عبر الإنترنت',
    'Paid' => 'مدفوع',
    'Unpaid' => 'غير مدفوع',
    'Partial' => 'جزئي',
    'Due' => 'مستحق',
    'Balance' => 'الرصيد',
    'Discount' => 'الخصم',
    'Fine' => 'الغرامة',

    // Examination
    'Examination' => 'الامتحان',
    'Exam' => 'الامتحان',
    'Exam Setup' => 'إعداد الامتحان',
    'Exam Schedule' => 'جدول الامتحان',
    'Exam Routine' => 'روتين الامتحان',
    'Marks Register' => 'سجل العلامات',
    'Marks Grade' => 'درجة العلامات',
    'Marks Distribution' => 'توزيع العلامات',
    'Grade' => 'الدرجة',
    'Marks' => 'العلامات',
    'Grade Point' => 'نقطة الدرجة',
    'Pass Mark' => 'علامة النجاح',
    'Full Marks' => 'العلامة الكاملة',
    'Result' => 'النتيجة',
    'Pass' => 'ناجح',
    'Fail' => 'راسب',
    'Online Exam' => 'امتحان عبر الإنترنت',
    'Question Bank' => 'بنك الأسئلة',
    'Question' => 'السؤال',
    'Answer' => 'الإجابة',

    // Library
    'Library' => 'المكتبة',
    'Book' => 'الكتاب',
    'Books' => 'الكتب',
    'Book List' => 'قائمة الكتب',
    'Add Book' => 'إضافة كتاب',
    'Book Category' => 'فئة الكتاب',
    'Author' => 'المؤلف',
    'Publisher' => 'الناشر',
    'ISBN' => 'الرقم الدولي',
    'Book Number' => 'رقم الكتاب',
    'Quantity' => 'الكمية',
    'Available' => 'متوفر',
    'Issued' => 'مُصدر',
    'Issue Book' => 'إصدار كتاب',
    'Return Book' => 'إرجاع كتاب',
    'Member' => 'العضو',
    'Members' => 'الأعضاء',
    'Issue Date' => 'تاريخ الإصدار',
    'Return Date' => 'تاريخ الإرجاع',

    // Accounts
    'Accounts' => 'الحسابات',
    'Income' => 'الدخل',
    'Expense' => 'المصروفات',
    'Income Head' => 'بند الدخل',
    'Expense Head' => 'بند المصروفات',
    'Add Income' => 'إضافة دخل',
    'Add Expense' => 'إضافة مصروفات',
    'Chart of Account' => 'شجرة الحسابات',
    'Profit' => 'الربح',
    'Loss' => 'الخسارة',
    'Transaction' => 'المعاملة',
    'Invoice' => 'الفاتورة',
    'Receipt' => 'الإيصال',
    'Voucher' => 'القسيمة',

    // Report
    'Report' => 'التقرير',
    'Reports' => 'التقارير',
    'Student Report' => 'تقرير الطلاب',
    'Attendance Report' => 'تقرير الحضور',
    'Fees Report' => 'تقرير الرسوم',
    'Account Report' => 'تقرير الحسابات',
    'Mark Sheet' => 'كشف العلامات',
    'Progress Card' => 'بطاقة التقدم',
    'Merit List' => 'قائمة الشرف',
    'Generate Report' => 'إنشاء تقرير',
    'Generate' => 'إنشاء',

    // Staff
    'Staff' => 'الموظفون',
    'Staff List' => 'قائمة الموظفين',
    'Add Staff' => 'إضافة موظف',
    'Staff Details' => 'تفاصيل الموظف',
    'Staff Manage' => 'إدارة الموظفين',
    'Role' => 'الدور',
    'Roles' => 'الأدوار',
    'Department' => 'القسم',
    'Departments' => 'الأقسام',
    'Designation' => 'المنصب',
    'Salary' => 'الراتب',
    'Basic Salary' => 'الراتب الأساسي',
    'Joining Date' => 'تاريخ الالتحاق',
    'Qualification' => 'المؤهل',
    'Experience' => 'الخبرة',
    'Permission' => 'الصلاحية',
    'Permissions' => 'الصلاحيات',

    // Settings
    'Settings' => 'الإعدادات',
    'General Settings' => 'الإعدادات العامة',
    'System Settings' => 'إعدادات النظام',
    'Email Settings' => 'إعدادات البريد الإلكتروني',
    'SMS Settings' => 'إعدادات الرسائل النصية',
    'Payment Settings' => 'إعدادات الدفع',
    'Website' => 'الموقع الإلكتروني',
    'Language' => 'اللغة',
    'Currency' => 'العملة',
    'Time Zone' => 'المنطقة الزمنية',
    'Date Format' => 'تنسيق التاريخ',
    'School' => 'المدرسة',
    'School Name' => 'اسم المدرسة',
    'School Code' => 'رمز المدرسة',
    'School Logo' => 'شعار المدرسة',
    'School Address' => 'عنوان المدرسة',
    'School Phone' => 'هاتف المدرسة',
    'School Email' => 'البريد الإلكتروني للمدرسة',
    'Academic Year' => 'العام الدراسي',
    'Current Session' => 'الدورة الحالية',

    // Additional terms
    'Home' => 'الصفحة الرئيسية',
    'Profile' => 'الملف الشخصي',
    'Logout' => 'تسجيل الخروج',
    'Login' => 'تسجيل الدخول',
    'Password' => 'كلمة المرور',
    'Change Password' => 'تغيير كلمة المرور',
    'Forgot Password' => 'نسيت كلمة المرور',
    'Reset Password' => 'إعادة تعيين كلمة المرور',
    'Remember Me' => 'تذكرني',
    'Dashboard' => 'لوحة التحكم',
    'Notification' => 'الإشعار',
    'Notifications' => 'الإشعارات',
    'Message' => 'الرسالة',
    'Messages' => 'الرسائل',
    'Inbox' => 'البريد الوارد',
    'Sent' => 'المرسل',
    'Compose' => 'إنشاء',
    'Reply' => 'رد',
    'Forward' => 'إعادة توجيه',
    'Notice' => 'الإشعار',
    'Notice Board' => 'لوحة الإعلانات',
    'Event' => 'الحدث',
    'Events' => 'الأحداث',
    'Calendar' => 'التقويم',
    'Homework' => 'الواجب المنزلي',
    'Assignment' => 'المهمة',
    'Download Center' => 'مركز التحميل',
    'Gallery' => 'المعرض',
    'Video Gallery' => 'معرض الفيديو',
    'Forums' => 'المنتديات',
    'Memories' => 'الذكريات',
    'Transport' => 'النقل',
    'Vehicle' => 'المركبة',
    'Route' => 'المسار',
    'Hostel' => 'السكن',
    'Room' => 'الغرفة',
    'Dormitory' => 'النوم',
    'Inventory' => 'المخزون',
    'Item' => 'العنصر',
    'Store' => 'المخزن',
    'Issue' => 'إصدار',
    'Return' => 'إرجاع',
    'Certificate' => 'الشهادة',
    'Transfer Certificate' => 'شهادة النقل',
    'Character Certificate' => 'شهادة حسن السيرة',
    'Bonafide Certificate' => 'شهادة الأصالة',
    'Certificate Generate' => 'إنشاء الشهادة',
    'ID Card Generate' => 'إنشاء بطاقة الهوية',
    'Complain' => 'الشكوى',
    'Complain List' => 'قائمة الشكاوى',
    'Postal' => 'البريد',
    'Postal Receive' => 'استلام البريد',
    'Postal Dispatch' => 'إرسال البريد',
    'Front CMS' => 'نظام إدارة الواجهة',
    'Admission Query' => 'استفسار القبول',
    'Visitor Book' => 'دفتر الزوار',
    'Phone Call Log' => 'سجل المكالمات الهاتفية',
    'Setup' => 'الإعداد',
    'Module Manager' => 'مدير الوحدات',
    'Backup' => 'النسخ الاحتياطي',
    'Utilities' => 'الأدوات',
];

// Dictionnaire complet de traductions FRANÇAIS
$frenchTranslations = [
    // Dashboard
    'Dashboard' => 'Tableau de bord',
    'Student' => 'Étudiant',
    'Students' => 'Étudiants',
    'Parent' => 'Parent',
    'Parents' => 'Parents',
    'Teacher' => 'Enseignant',
    'Teachers' => 'Enseignants',
    'Session' => 'Session',
    'Sessions' => 'Sessions',
    'Revenue' => 'Revenus',
    'Expense' => 'Dépenses',
    'fees_collection' => 'Collecte des frais',
    'Total Students' => 'Total étudiants',
    'Total Parents' => 'Total parents',
    'Total Teachers' => 'Total enseignants',
    'Total Sessions' => 'Total sessions',

    // Common terms
    'Add' => 'Ajouter',
    'Edit' => 'Modifier',
    'Delete' => 'Supprimer',
    'Update' => 'Mettre à jour',
    'Save' => 'Enregistrer',
    'Cancel' => 'Annuler',
    'Submit' => 'Soumettre',
    'Search' => 'Rechercher',
    'View' => 'Voir',
    'Print' => 'Imprimer',
    'Export' => 'Exporter',
    'Import' => 'Importer',
    'Download' => 'Télécharger',
    'Upload' => 'Téléverser',
    'Back' => 'Retour',
    'Next' => 'Suivant',
    'Previous' => 'Précédent',
    'Close' => 'Fermer',
    'Select' => 'Sélectionner',
    'Action' => 'Action',
    'Actions' => 'Actions',
    'Status' => 'Statut',
    'Active' => 'Actif',
    'Inactive' => 'Inactif',
    'Yes' => 'Oui',
    'No' => 'Non',
    'All' => 'Tous',
    'Name' => 'Nom',
    'Email' => 'Email',
    'Phone' => 'Téléphone',
    'Address' => 'Adresse',
    'Date' => 'Date',
    'Time' => 'Heure',
    'Description' => 'Description',
    'Details' => 'Détails',
    'Type' => 'Type',
    'Category' => 'Catégorie',
    'Amount' => 'Montant',
    'Total' => 'Total',

    // Academic
    'Academic' => 'Académique',
    'Class' => 'Classe',
    'Classes' => 'Classes',
    'Section' => 'Section',
    'Sections' => 'Sections',
    'Subject' => 'Matière',
    'Subjects' => 'Matières',
    'teacher' => 'Enseignant',
    'Assign Teacher' => 'Affecter enseignant',
    'Class Room' => 'Salle de classe',
    'Class Routine' => 'Emploi du temps',
    'Time Schedule' => 'Horaire',

    // Student Info
    'Student Info' => 'Info étudiant',
    'Student List' => 'Liste étudiants',
    'Add Student' => 'Ajouter étudiant',
    'Student Admission' => 'Admission étudiant',
    'First Name' => 'Prénom',
    'Last Name' => 'Nom',
    'Date of Birth' => 'Date de naissance',
    'Gender' => 'Genre',
    'Male' => 'Masculin',
    'Female' => 'Féminin',

    // Attendance
    'Attendance' => 'Présence',
    'Daily Attendance' => 'Présence quotidienne',
    'Present' => 'Présent',
    'Absent' => 'Absent',

    // Leave
    'Leave' => 'Congé',
    'Leave Type' => 'Type de congé',
    'Leave Request' => 'Demande de congé',
    'Approve' => 'Approuver',
    'Reject' => 'Rejeter',
    'Pending' => 'En attente',
    'Approved' => 'Approuvé',
    'Rejected' => 'Rejeté',

    // Fees
    'Fees' => 'Frais',
    'Fees Group' => 'Groupe de frais',
    'Fees Type' => 'Type de frais',
    'Fees Collect' => 'Collecte frais',
    'Fees Collection' => 'Collecte des frais',
    'Payment Method' => 'Mode de paiement',
    'Cash' => 'Espèces',
    'Cheque' => 'Chèque',
    'Paid' => 'Payé',
    'Unpaid' => 'Non payé',
    'Due' => 'Dû',
    'Balance' => 'Solde',
    'Discount' => 'Remise',

    // Examination
    'Examination' => 'Examen',
    'Exam' => 'Examen',
    'Exam Setup' => 'Configuration examen',
    'Exam Schedule' => 'Calendrier examen',
    'Marks' => 'Notes',
    'Grade' => 'Classe',
    'Result' => 'Résultat',
    'Pass' => 'Réussi',
    'Fail' => 'Échoué',

    // Library
    'Library' => 'Bibliothèque',
    'Book' => 'Livre',
    'Books' => 'Livres',
    'Author' => 'Auteur',
    'Publisher' => 'Éditeur',
    'Available' => 'Disponible',

    // Accounts
    'Accounts' => 'Comptes',
    'Income' => 'Revenus',
    'Expense' => 'Dépenses',
    'Profit' => 'Bénéfice',
    'Loss' => 'Perte',
    'Invoice' => 'Facture',

    // Report
    'Report' => 'Rapport',
    'Reports' => 'Rapports',
    'Generate Report' => 'Générer rapport',
    'Generate' => 'Générer',

    // Staff
    'Staff' => 'Personnel',
    'Staff List' => 'Liste personnel',
    'Add Staff' => 'Ajouter personnel',
    'Role' => 'Rôle',
    'Roles' => 'Rôles',
    'Department' => 'Département',
    'Salary' => 'Salaire',
    'Permission' => 'Permission',
    'Permissions' => 'Permissions',

    // Settings
    'Settings' => 'Paramètres',
    'General Settings' => 'Paramètres généraux',
    'Language' => 'Langue',
    'School' => 'École',
    'School Name' => 'Nom école',

    // Additional
    'Home' => 'Accueil',
    'Profile' => 'Profil',
    'Logout' => 'Déconnexion',
    'Login' => 'Connexion',
    'Password' => 'Mot de passe',
    'Notification' => 'Notification',
    'Notifications' => 'Notifications',
    'Message' => 'Message',
    'Messages' => 'Messages',
    'Calendar' => 'Calendrier',
    'Gallery' => 'Galerie',
];

// Fonction pour corriger un fichier JSON
function correctJsonFile($filePath, $translations) {
    if (!file_exists($filePath)) {
        echo "⚠️  Fichier introuvable: $filePath\n";
        return 0;
    }

    $content = file_get_contents($filePath);
    $data = json_decode($content, true);

    if ($data === null) {
        echo "❌ Erreur JSON dans: $filePath\n";
        return 0;
    }

    $corrections = 0;

    // Parcourir toutes les clés
    foreach ($data as $key => $value) {
        // Si la valeur existe dans le dictionnaire de traduction
        if (isset($translations[$value])) {
            $data[$key] = $translations[$value];
            $corrections++;
            echo "  ✓ '$value' → '{$translations[$value]}'\n";
        }
        // Si la clé existe dans le dictionnaire
        elseif (isset($translations[$key])) {
            $data[$key] = $translations[$key];
            $corrections++;
            echo "  ✓ Clé '$key' → '{$translations[$key]}'\n";
        }
    }

    if ($corrections > 0) {
        // Sauvegarder avec formatage propre
        $jsonContent = json_encode($data, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
        file_put_contents($filePath, $jsonContent);
        echo "✅ $corrections corrections dans " . basename($filePath) . "\n\n";
    }

    return $corrections;
}

// CORRECTION ARABE
echo "🇩🇿 CORRECTION DE L'ARABE\n";
echo "========================\n\n";

$arPath = $langPath . '/ar';
$totalArabicCorrections = 0;

$arabicFiles = [
    'dashboard.json',
    'common.json',
    'academic.json',
    'student_info.json',
    'attendance.json',
    'leave.json',
    'fees.json',
    'examination.json',
    'library.json',
    'accounts.json',
    'report.json',
    'staff.json',
    'settings.json',
    'homework.json',
    'communicate.json',
    'transport.json',
    'dormitory.json',
    'inventory.json',
    'certificate.json',
    'front_settings.json',
];

foreach ($arabicFiles as $file) {
    $filePath = $arPath . '/' . $file;
    echo "📝 Traitement: $file\n";
    $corrections = correctJsonFile($filePath, $arabicTranslations);
    $totalArabicCorrections += $corrections;
}

echo "\n✅ ARABE: $totalArabicCorrections corrections totales\n\n";

// CORRECTION FRANÇAIS
echo "🇫🇷 CORRECTION DU FRANÇAIS\n";
echo "==========================\n\n";

$frPath = $langPath . '/fr';
$totalFrenchCorrections = 0;

foreach ($arabicFiles as $file) {
    $filePath = $frPath . '/' . $file;
    echo "📝 Traitement: $file\n";
    $corrections = correctJsonFile($filePath, $frenchTranslations);
    $totalFrenchCorrections += $corrections;
}

echo "\n✅ FRANÇAIS: $totalFrenchCorrections corrections totales\n\n";

// RÉSUMÉ FINAL
echo "\n========================================\n";
echo "RÉSUMÉ DES CORRECTIONS\n";
echo "========================================\n";
echo "🇩🇿 Arabe: $totalArabicCorrections corrections\n";
echo "🇫🇷 Français: $totalFrenchCorrections corrections\n";
echo "📊 TOTAL: " . ($totalArabicCorrections + $totalFrenchCorrections) . " corrections\n";
echo "========================================\n\n";

echo "✅ CORRECTION TERMINÉE!\n";
echo "⚠️  N'oubliez pas de nettoyer les caches:\n";
echo "   \"C:/xampp/php/php.exe\" CLEAR_ALL_CACHES_FINAL.php\n\n";

?>
