<?php
/**
 * CORRECTION MASSIVE FINALE - TOUS LES MODULES
 * Corrige 352 termes (162 AR + 190 FR)
 * Basé sur le système de traduction OnestSchool
 */

echo "\n========================================\n";
echo "CORRECTION MASSIVE FINALE\n";
echo "========================================\n\n";

$langPath = __DIR__ . '/lang';

// ========================================
// DICTIONNAIRE ARABE COMPLET
// ========================================
$arabicDictionary = [
    // Common Actions
    'Add' => 'إضافة',
    'Edit' => 'تعديل',
    'Delete' => 'حذف',
    'Update' => 'تحديث',
    'Updated' => 'محدث',
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
    'Create' => 'إنشاء',
    'Created' => 'تم الإنشاء',
    'Show' => 'عرض',
    'Display' => 'عرض',
    'Generate' => 'إنشاء',
    'Manage' => 'إدارة',
    'Management' => 'الإدارة',

    // Status
    'Action' => 'الإجراء',
    'Actions' => 'الإجراءات',
    'Status' => 'الحالة',
    'Active' => 'نشط',
    'Inactive' => 'غير نشط',
    'Yes' => 'نعم',
    'No' => 'لا',
    'All' => 'الكل',
    'Approved' => 'موافق عليه',
    'Rejected' => 'مرفوض',
    'Pending' => 'قيد الانتظار',
    'Complete' => 'مكتمل',
    'Incomplete' => 'غير مكتمل',

    // Common Fields
    'Name' => 'الاسم',
    'First Name' => 'الاسم الأول',
    'Last Name' => 'اسم العائلة',
    'Email' => 'البريد الإلكتروني',
    'Phone' => 'الهاتف',
    'Address' => 'العنوان',
    'Date' => 'التاريخ',
    'Start Date' => 'تاريخ البداية',
    'End Date' => 'تاريخ النهاية',
    'Time' => 'الوقت',
    'Description' => 'الوصف',
    'Details' => 'التفاصيل',
    'Type' => 'النوع',
    'Category' => 'الفئة',
    'Amount' => 'المبلغ',
    'Total' => 'الإجمالي',
    'From' => 'من',
    'To' => 'إلى',
    'Information' => 'المعلومات',
    'Contact' => 'اتصال',
    'Notification' => 'الإشعار',
    'Request' => 'طلب',
    'Approval' => 'الموافقة',

    // People
    'Student' => 'الطالب',
    'Students' => 'الطلاب',
    'Parent' => 'ولي الأمر',
    'Parents' => 'أولياء الأمور',
    'Guardian' => 'ولي الأمر',
    'Teacher' => 'المعلم',
    'Teachers' => 'المعلمون',
    'Staff' => 'الموظفون',
    'Driver' => 'السائق',
    'Drivers' => 'السائقون',
    'User' => 'المستخدم',

    // Education
    'Class' => 'الصف',
    'Classes' => 'الصفوف',
    'Section' => 'القسم',
    'Sections' => 'الأقسام',
    'Subject' => 'المادة',
    'Subjects' => 'المواد',
    'Exam' => 'الامتحان',
    'Examination' => 'الامتحان',
    'Attendance' => 'الحضور',
    'Admission' => 'القبول',
    'Assignment' => 'الواجب',
    'Assign' => 'تعيين',

    // Modules
    'Department' => 'القسم',
    'Designation' => 'المنصب',
    'Fee' => 'الرسوم',
    'Fees' => 'الرسوم',
    'Library' => 'المكتبة',
    'Book' => 'الكتاب',
    'Books' => 'الكتب',
    'Report' => 'التقرير',
    'Reports' => 'التقارير',
    'Account' => 'الحساب',
    'Accounts' => 'الحسابات',
    'Communication' => 'التواصل',
    'Notice' => 'إشعار',
    'Board' => 'اللوحة',
    'SMS' => 'رسالة نصية',
    'Mail' => 'بريد',
    'Template' => 'قالب',
    'Transportation' => 'النقل',
    'Vehicle' => 'المركبة',
    'Vehicles' => 'المركبات',
    'Route' => 'المسار',
    'Routes' => 'المسارات',
    'Schedule' => 'الجدول',
    'Enrollment' => 'التسجيل',
    'Forum' => 'المنتدى',
    'Forums' => 'المنتديات',
    'Memory' => 'الذاكرة',
    'Memories' => 'الذكريات',
    'Live' => 'مباشر',
    'Chat' => 'دردشة',
    'Message' => 'رسالة',
    'Messaging' => 'المراسلة',
    'Conversation' => 'المحادثة',
    'Conversations' => 'المحادثات',
    'List' => 'القائمة',
    'Settings' => 'الإعدادات',
    'Setup' => 'الإعداد',
    'Configuration' => 'التكوين',
    'Terms' => 'الشروط',
    'Content' => 'المحتوى',
    'Contents' => 'المحتويات',

    // Specific Messages
    'Updated Successfully' => 'تم التحديث بنجاح',
    'Created Successfully' => 'تم الإنشاء بنجاح',
    'General Settings Updated Successfully' => 'تم تحديث الإعدادات العامة بنجاح',
    'User Created Successfully' => 'تم إنشاء المستخدم بنجاح',
    'Back To Homepage' => 'العودة للصفحة الرئيسية',
    'Enter First Name' => 'أدخل الاسم الأول',
    'Enter Last Name' => 'أدخل اسم العائلة',
    'Enter Start Date' => 'أدخل تاريخ البداية',
    'Enter End Date' => 'أدخل تاريخ النهاية',
    'Student Details' => 'تفاصيل الطالب',
    'Guardian Details' => 'تفاصيل ولي الأمر',
    'Father Details' => 'تفاصيل الأب',
    'Mother Details' => 'تفاصيل الأم',
    'Admission No' => 'رقم القبول',
    'Admission Date' => 'تاريخ القبول',
    'Class Section' => 'قسم الصف',
    'Driver List' => 'قائمة السائقين',
    'Content Type' => 'نوع المحتوى',
    'Content List' => 'قائمة المحتوى',
    'My Content List' => 'قائمة محتوياتي',
    'Min Tax Eligible Amount' => 'الحد الأدنى للمبلغ الخاضع للضريبة',
    'Max Tax Amount' => 'الحد الأقصى لمبلغ الضريبة',
    'Conversaiton List' => 'قائمة المحادثات',
    'Edit Terms' => 'تعديل الشروط',
    'Twilio Account Sid' => 'معرف حساب Twilio',
    'My Forums' => 'منتدياتي',
    'Forum Feeds' => 'تغذية المنتدى',
    'My Memories' => 'ذكرياتي',
    'Student Category' => 'فئة الطالب',
];

// ========================================
// DICTIONNAIRE FRANÇAIS COMPLET
// ========================================
$frenchDictionary = [
    // Common Actions
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
    'Create' => 'Créer',
    'Show' => 'Afficher',
    'Display' => 'Afficher',
    'Generate' => 'Générer',
    'Manage' => 'Gérer',

    // Status
    'Action' => 'Action',
    'Actions' => 'Actions',
    'Status' => 'Statut',
    'Active' => 'Actif',
    'Inactive' => 'Inactif',
    'Yes' => 'Oui',
    'No' => 'Non',
    'All' => 'Tous',
    'OK' => 'OK',
    'Approved' => 'Approuvé',
    'Rejected' => 'Rejeté',
    'Pending' => 'En attente',

    // Common Fields
    'Name' => 'Nom',
    'First Name' => 'Prénom',
    'Last Name' => 'Nom de famille',
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
    'From' => 'De',
    'To' => 'À',
    'Information' => 'Information',
    'Contact' => 'Contact',
    'Notification' => 'Notification',
    'Notifications' => 'Notifications',
    'Request' => 'Demande',
    'Photo' => 'Photo',
    'Position' => 'Position',
    'Documents' => 'Documents',
    'Password' => 'Mot de passe',

    // People
    'Student' => 'Étudiant',
    'Students' => 'Étudiants',
    'Parent' => 'Parent',
    'Parents' => 'Parents',
    'Guardian' => 'Tuteur',
    'Teacher' => 'Enseignant',
    'Teachers' => 'Enseignants',
    'Staff' => 'Personnel',
    'Driver' => 'Chauffeur',

    // Education
    'Class' => 'Classe',
    'Classes' => 'Classes',
    'Section' => 'Section',
    'Sections' => 'Sections',
    'Subject' => 'Matière',
    'Subjects' => 'Matières',
    'Exam' => 'Examen',
    'Examination' => 'Examen',
    'Attendance' => 'Présence',
    'Admission' => 'Admission',
    'Absent' => 'Absent',
    'Leaves' => 'Congés',

    // Modules
    'Department' => 'Département',
    'Designation' => 'Désignation',
    'Fee' => 'Frais',
    'Fees' => 'Frais',
    'Library' => 'Bibliothèque',
    'Book' => 'Livre',
    'Books' => 'Livres',
    'Report' => 'Rapport',
    'Reports' => 'Rapports',
    'Account' => 'Compte',
    'Accounts' => 'Comptes',
    'Communication' => 'Communication',
    'Notice' => 'Avis',
    'Notices' => 'Avis',
    'Board' => 'Tableau',
    'Template' => 'Modèle',
    'Transportation' => 'Transport',
    'Vehicle' => 'Véhicule',
    'Vehicles' => 'Véhicules',
    'Route' => 'Itinéraire',
    'Routes' => 'Itinéraires',
    'Schedule' => 'Horaire',
    'Forum' => 'Forum',
    'Forums' => 'Forums',
    'Memory' => 'Souvenir',
    'Memories' => 'Souvenirs',
    'Chat' => 'Chat',
    'Message' => 'Message',
    'Messaging' => 'Messagerie',
    'Conversation' => 'Conversation',
    'Conversations' => 'Conversations',
    'List' => 'Liste',
    'Settings' => 'Paramètres',
    'Setup' => 'Configuration',
    'Configuration' => 'Configuration',
    'Member' => 'Membre',
    'Session' => 'Session',
    'Sessions' => 'Sessions',
    'Routines' => 'Routines',
    'Slider' => 'Slider',
    'Gallery' => 'Galerie',
    'Branches' => 'Branches',
    'Addon' => 'Extension',
    'Menus' => 'Menus',
    'Pages' => 'Pages',

    // Specific Terms
    'Student Details' => 'Détails de l\'étudiant',
    'Guardian Details' => 'Détails du tuteur',
    'Father Details' => 'Détails du père',
    'Mother Details' => 'Détails de la mère',
    'Admission No' => 'N° admission',
    'Admission Date' => 'Date d\'admission',
    'Class Section' => 'Section de classe',
    'Driver List' => 'Liste des chauffeurs',
    'Content Type' => 'Type de contenu',
    'Content List' => 'Liste de contenus',
    'My Content List' => 'Ma liste de contenus',
    'Contents' => 'Contenus',
    'Content Share' => 'Partage de contenu',
    'Shared Content' => 'Contenu partagé',
    'Shared Content Group' => 'Groupe de contenu partagé',
    'Study Material' => 'Matériel d\'étude',
    'Study Material Group' => 'Groupe de matériel d\'étude',
    'Conversaiton List' => 'Liste des conversations',
    'Conversation List' => 'Liste des conversations',
    'Request Log' => 'Journal des demandes',
    'Enter Sibling Order' => 'Entrez l\'ordre des frères et sœurs',
    'Prev School' => 'École précédente',
    'Tax Setup' => 'Configuration des taxes',
    'Tax Percentage' => 'Pourcentage de taxe',
    'Enter Tax Percentage' => 'Entrez le pourcentage de taxe',
    'Tax Income Head' => 'Chef de revenu fiscal',
    'Min Tax Eligible Amount' => 'Montant minimum éligible à la taxe',
    'Max Tax Amount' => 'Montant maximum de taxe',
    'Enter start date' => 'Entrez la date de début',
    'Enter end date' => 'Entrez la date de fin',
    'Welcome To Installation' => 'Bienvenue dans l\'installation',
    'Get Started' => 'Commencer',
    'Check Your Environment For Ischool Installation' => 'Vérifiez votre environnement pour l\'installation d\'Ischool',
    'Server Requirements' => 'Exigences du serveur',
    'Folder Requirements' => 'Exigences des dossiers',
    'My Forums' => 'Mes forums',
    'Forum Feeds' => 'Flux du forum',
    'My Memories' => 'Mes souvenirs',
];

// ========================================
// FONCTION DE CORRECTION
// ========================================
function correctTranslations($filePath, $dictionary, $language) {
    if (!file_exists($filePath)) {
        return 0;
    }

    $content = file_get_contents($filePath);
    $data = json_decode($content, true);

    if ($data === null) {
        return 0;
    }

    $corrected = 0;

    foreach ($data as $key => $value) {
        // Vérifier si la valeur existe dans le dictionnaire
        if (isset($dictionary[$value])) {
            $data[$key] = $dictionary[$value];
            $corrected++;
        }
        // Vérifier si la clé = valeur (non traduit)
        elseif ($key === $value && isset($dictionary[$key])) {
            $data[$key] = $dictionary[$key];
            $corrected++;
        }
        // Vérifier les correspondances partielles
        else {
            foreach ($dictionary as $english => $translation) {
                if (strpos($value, $english) !== false && $value === $english) {
                    $data[$key] = $translation;
                    $corrected++;
                    break;
                }
            }
        }
    }

    if ($corrected > 0) {
        $json = json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
        file_put_contents($filePath, $json);
    }

    return $corrected;
}

// ========================================
// CORRECTION ARABE
// ========================================
echo "🇩🇿 CORRECTION ARABE:\n";
echo "========================================\n\n";

$arFiles = glob($langPath . '/ar/*.json');
$totalAr = 0;

foreach ($arFiles as $file) {
    $fileName = basename($file);
    $corrected = correctTranslations($file, $arabicDictionary, 'ar');

    if ($corrected > 0) {
        echo "✅ $fileName: $corrected correction(s)\n";
        $totalAr += $corrected;
    }
}

// ========================================
// CORRECTION FRANÇAIS
// ========================================
echo "\n🇫🇷 CORRECTION FRANÇAIS:\n";
echo "========================================\n\n";

$frFiles = glob($langPath . '/fr/*.json');
$totalFr = 0;

foreach ($frFiles as $file) {
    $fileName = basename($file);
    $corrected = correctTranslations($file, $frenchDictionary, 'fr');

    if ($corrected > 0) {
        echo "✅ $fileName: $corrected correction(s)\n";
        $totalFr += $corrected;
    }
}

// ========================================
// RÉSUMÉ
// ========================================
echo "\n========================================\n";
echo "📊 RÉSUMÉ FINAL\n";
echo "========================================\n";
echo "🇩🇿 Arabe: $totalAr corrections\n";
echo "🇫🇷 Français: $totalFr corrections\n";
echo "📊 TOTAL: " . ($totalAr + $totalFr) . " corrections\n";
echo "========================================\n\n";

echo "✅ CORRECTION MASSIVE TERMINÉE!\n\n";
echo "⚠️  ÉTAPES FINALES OBLIGATOIRES:\n";
echo "   1. Nettoyez les caches:\n";
echo '      "C:/xampp/php/php.exe" artisan cache:clear' . "\n";
echo '      "C:/xampp/php/php.exe" artisan config:clear' . "\n";
echo '      "C:/xampp/php/php.exe" artisan view:clear' . "\n";
echo "   2. DÉCONNECTEZ-VOUS du dashboard\n";
echo "   3. RECONNECTEZ-VOUS\n";
echo "   4. Appuyez sur Ctrl+Shift+R dans le navigateur\n\n";
