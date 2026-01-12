<?php
echo "=== BBC SCHOOL ALGERIA - CORRECTION SYSTÈME TRADUCTION ===\n";
echo "Date: " . date("Y-m-d H:i:s") . "\n\n";

// Corrections françaises
$frenchTranslations = [
    "online_admission_fees_enable" => "Frais d'admission en ligne activés",
    "student_first_name" => "Prénom de l'étudiant",
    "student_last_name" => "Nom de famille de l'étudiant",
    "student_phone" => "Téléphone de l'étudiant",
    "student_email" => "Email de l'étudiant",
    "student_dob" => "Date de naissance",
    "student_document" => "Document étudiant",
    "student_photo" => "Photo étudiant",
    "session" => "Session",
    "class" => "Classe",
    "section" => "Section",
    "shift" => "Équipe",
    "gender" => "Genre",
    "religion" => "Religion",
    "previous_school" => "École précédente",
    "previous_school_info" => "Info école précédente",
    "previous_school_doc" => "Doc école précédente",
    "place_of_birth" => "Lieu de naissance",
    "nationality" => "Nationalité",
    "cpr_no" => "Numéro CPR",
    "spoken_lang_at_home" => "Langue parlée à la maison",
    "residance_address" => "Adresse de résidence",
    "father_nationality" => "Nationalité du père",
    "gurdian_name" => "Nom du tuteur",
    "gurdian_email" => "Email du tuteur",
    "gurdian_phone" => "Téléphone du tuteur",
    "gurdian_photo" => "Photo du tuteur",
    "gurdian_profession" => "Profession du tuteur",
    "father_name" => "Nom du père",
    "father_phone" => "Téléphone du père",
    "father_photo" => "Photo du père",
    "father_profession" => "Profession du père",
    "mother_name" => "Nom de la mère",
    "mother_phone" => "Téléphone de la mère",
    "mother_photo" => "Photo de la mère",
    "mother_profession" => "Profession de la mère",
    "Father_Nationality" => "Nationalité du père",
    "Father_ID" => "ID du père",
    "Mother_ID" => "ID de la mère",
    "Username" => "Nom d'utilisateur",
    "Password" => "Mot de passe",
    "Default Password" => "Mot de passe par défaut",
    "Custom Password" => "Mot de passe personnalisé",
    "read_more" => "Lire la suite",
    "contact_us" => "Contactez-nous",
    "learn_more" => "En savoir plus",
    "All" => "Tout",
    "Dashboard" => "Tableau de bord",
    "Home" => "Accueil",
    "About" => "À propos",
    "News" => "Actualités",
    "Events" => "Événements",
    "notices" => "Avis",
    "Result" => "Résultats",
    "online_admission" => "Inscription en ligne",
    "Menus" => "Menus",
    "Pages" => "Pages",
    "subscribe_to_newsletter" => "S'abonner à la newsletter",
    "join_us_and_get_weekly_inspiration" => "Rejoignez-nous et recevez l'inspiration hebdomadaire",
    "type_email_address" => "Tapez l'adresse email",
    "Subscribe" => "S'abonner",
    "Login" => "Connexion",
    "Success" => "Succès",
    "Subscribed" => "Abonné",
    "OK" => "OK"
];

// Corrections arabes
$arabicTranslations = [
    "online_admission_fees_enable" => "تفعيل رسوم القبول الإلكتروني",
    "student_first_name" => "الاسم الأول للطالب",
    "student_last_name" => "اسم العائلة للطالب",
    "student_phone" => "هاتف الطالب",
    "student_email" => "بريد الطالب الإلكتروني",
    "student_dob" => "تاريخ الميلاد",
    "student_document" => "وثيقة الطالب",
    "student_photo" => "صورة الطالب",
    "session" => "الجلسة",
    "class" => "الصف",
    "section" => "القسم",
    "shift" => "الفترة",
    "gender" => "الجنس",
    "religion" => "الديانة",
    "previous_school" => "المدرسة السابقة",
    "previous_school_info" => "معلومات المدرسة السابقة",
    "previous_school_doc" => "وثائق المدرسة السابقة",
    "place_of_birth" => "مكان الولادة",
    "nationality" => "الجنسية",
    "cpr_no" => "رقم CPR",
    "spoken_lang_at_home" => "اللغة المحكية في المنزل",
    "residance_address" => "عنوان الإقامة",
    "father_nationality" => "جنسية الأب",
    "gurdian_name" => "اسم الوصي",
    "gurdian_email" => "بريد الوصي الإلكتروني",
    "gurdian_phone" => "هاتف الوصي",
    "gurdian_photo" => "صورة الوصي",
    "gurdian_profession" => "مهنة الوصي",
    "father_name" => "اسم الأب",
    "father_phone" => "هاتف الأب",
    "father_photo" => "صورة الأب",
    "father_profession" => "مهنة الأب",
    "mother_name" => "اسم الأم",
    "mother_phone" => "هاتف الأم",
    "mother_photo" => "صورة الأم",
    "mother_profession" => "مهنة الأم",
    "Father_Nationality" => "جنسية الأب",
    "Father_ID" => "هوية الأب",
    "Mother_ID" => "هوية الأم",
    "Username" => "اسم المستخدم",
    "Password" => "كلمة المرور",
    "Default Password" => "كلمة المرور الافتراضية",
    "Custom Password" => "كلمة مرور مخصصة",
    "read_more" => "اقرأ المزيد",
    "contact_us" => "اتصل بنا",
    "learn_more" => "تعلم المزيد",
    "All" => "الكل",
    "Dashboard" => "لوحة التحكم",
    "Home" => "الرئيسية",
    "About" => "حولنا",
    "News" => "الأخبار",
    "Events" => "الأحداث",
    "notices" => "الإشعارات",
    "Result" => "النتائج",
    "online_admission" => "التسجيل الإلكتروني",
    "Menus" => "القوائم",
    "Pages" => "الصفحات",
    "subscribe_to_newsletter" => "اشترك في النشرة الإخبارية",
    "join_us_and_get_weekly_inspiration" => "انضم إلينا واحصل على الإلهام الأسبوعي",
    "type_email_address" => "اكتب عنوان البريد الإلكتروني",
    "Subscribe" => "اشتراك",
    "Login" => "تسجيل الدخول",
    "Success" => "نجح",
    "Subscribed" => "مشترك",
    "OK" => "موافق"
];

// Corriger le fichier français
$frPath = __DIR__ . "/lang/fr/frontend.json";
if (file_exists($frPath)) {
    file_put_contents($frPath, json_encode($frenchTranslations, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
    echo "✅ Fichier français corrigé : $frPath\n";
} else {
    echo "❌ Fichier français non trouvé : $frPath\n";
}

// Corriger le fichier arabe
$arPath = __DIR__ . "/lang/ar/frontend.json";
if (file_exists($arPath)) {
    file_put_contents($arPath, json_encode($arabicTranslations, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
    echo "✅ Fichier arabe corrigé : $arPath\n";
} else {
    echo "❌ Fichier arabe non trouvé : $arPath\n";
}

echo "\n=== VERIFICATION ===\n";
echo "Vérifiez maintenant les URL :\n";
echo "1. http://localhost/onestschooled-test/public?lang=en (anglais)\n";
echo "2. http://localhost/onestschooled-test/public?lang=fr (français)\n";
echo "3. http://localhost/onestschooled-test/public?lang=ar (arabe)\n\n";

echo "=== SYSTEME RESTAURÉ ===\n";
echo "OnestSchool utilise maintenant son système Laravel natif :\n";
echo "• LanguageController + LanguageMiddleware\n";
echo "• Fichiers JSON lang/{locale}/module.json\n";
echo "• Fonction ___() dans les templates\n";
echo "• Session Laravel pour persistance\n\n";
?>