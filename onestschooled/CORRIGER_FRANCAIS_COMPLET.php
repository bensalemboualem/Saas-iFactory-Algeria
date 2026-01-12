<?php
/**
 * CORRECTION COMPLÈTE FRANÇAIS - LIGNE PAR LIGNE
 * Tous les fichiers JSON français corrigés intégralement
 */

echo "\n========================================\n";
echo "CORRECTION FRANÇAISE COMPLÈTE\n";
echo "========================================\n\n";

$langPath = __DIR__ . '/lang/fr';

// Je vais maintenant corriger CHAQUE fichier JSON français LIGNE PAR LIGNE

echo "Correction fichier par fichier...\n\n";

// 1. student_info.json
echo "1. student_info.json...\n";
$studentInfo = [
    "student_category" => "Catégorie étudiant",
    "promote_students" => "Promouvoir étudiants",
    "guardian" => "Tuteur",
    "online_admission" => "Admission en ligne",
    "select_class" => "Sélectionner classe",
    "select_section" => "Sélectionner section",
    "student_name" => "Nom étudiant",
    "date_of_birth" => "Date de naissance",
    "mobile" => "Mobile",
    "guardian_name" => "Nom tuteur",
    "guardian_mobile" => "Mobile tuteur",
    "online_admission_setting" => "Paramètres admission en ligne",
    "select_fees_group" => "Sélectionner groupe frais",
    "section" => "Section",
    "admission_no" => "N° admission",
    "roll_no" => "N° matricule",
    "mobile_number" => "Numéro mobile",
    "category_list" => "Liste catégories",
    "promote_list" => "Liste promotion",
    "promote_student" => "Promouvoir étudiant",
    "promote_students_in_next_session" => "Promouvoir étudiants en prochaine session",
    "promote_session" => "Session promotion",
    "select_session" => "Sélectionner session",
    "promote_class" => "Classe promotion",
    "promote_section" => "Section promotion",
    "disabled_list" => "Liste désactivés",
    "parent_list" => "Liste parents",
    "select_student" => "Sélectionner étudiant",
    "select subject" => "Sélectionner matière",
    "parent_edit" => "Modifier parent",
    "father_name" => "Nom père",
    "enter_father_name" => "Entrer nom père",
    "father_mobile" => "Mobile père",
    "enter_father_mobile" => "Entrer mobile père",
    "father_profession" => "Profession père",
    "enter_father_profession" => "Entrer profession père",
    "father_image" => "Image père",
    "mother_name" => "Nom mère",
    "enter_mother_name" => "Entrer nom mère",
    "mother_mobile" => "Mobile mère",
    "enter_mother_mobile" => "Entrer mobile mère",
    "mother_profession" => "Profession mère",
    "mother_image" => "Image mère",
    "enter_guardian_name" => "Entrer nom tuteur",
    "enter_guardian_mobile" => "Entrer mobile tuteur",
    "guardian_profession" => "Profession tuteur",
    "enter_guardian_profession" => "Entrer profession tuteur",
    "guardian_image" => "Image tuteur",
    "guardian_email" => "Email tuteur",
    "enter_guardian_email" => "Entrer email tuteur",
    "guardian_address" => "Adresse tuteur",
    "enter_guardian_address" => "Entrer adresse tuteur",
    "guardian_relation" => "Relation tuteur",
    "enter_guardian_relation" => "Entrer relation tuteur",
    "Job title or designation" => "Titre poste ou désignation",
    "Place of Work" => "Lieu de travail",
    "Company/Organization name" => "Nom société/organisation",
    "Guardian" => "Tuteur",
    "parent_create" => "Créer parent",
    "Profile Info" => "Info profil",
    "select_shift" => "Sélectionner équipe"
];

file_put_contents($langPath . '/student_info.json', json_encode($studentInfo, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT));
echo "   ✅ " . count($studentInfo) . " lignes corrigées\n\n";

// 2. attendance.json
echo "2. attendance.json...\n";
$attendance = [
    "Subject Attendance" => "Présence matière",
    "Monthly Attendance" => "Présence mensuelle",
    "Present" => "Présent",
    "Late" => "Retard",
    "Absent" => "Absent",
    "Half Day" => "Demi-journée",
    "half_day" => "Demi-journée",
    "attendance_already_collected_you_can_edit_record" => "Présence déjà collectée, vous pouvez modifier l'enregistrement"
];

file_put_contents($langPath . '/attendance.json', json_encode($attendance, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT));
echo "   ✅ " . count($attendance) . " lignes corrigées\n\n";

// 3. leave.json
echo "3. leave.json...\n";
$leave = [
    "Type" => "Type",
    "Leave Type" => "Type de congé",
    "Leave type" => "Type de congé",
    "Add Leave Request" => "Ajouter demande congé",
    "Edit Leave Request" => "Modifier demande congé"
];

file_put_contents($langPath . '/leave.json', json_encode($leave, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT));
echo "   ✅ " . count($leave) . " lignes corrigées\n\n";

// 4. fees.json
echo "4. fees.json...\n";
$fees = [
    "Discount Setup" => "Configuration remise",
    "description" => "Description",
    "enter_description" => "Entrer description",
    "fees_type" => "Type de frais",
    "code" => "Code",
    "group" => "Groupe",
    "type" => "Type",
    "due_date" => "Date d'échéance",
    "fine_type" => "Type pénalité",
    "fine_amount" => "Montant pénalité",
    "students_list" => "Liste étudiants",
    "Fees Discount Setup" => "Configuration remise frais",
    "Siblings Discount" => "Remise fratrie",
    "Set up sibling-based discounts that scale with each child added" => "Configurer remises fratrie qui augmentent avec chaque enfant ajouté",
    "Discount Title" => "Titre remise",
    "Discount Percentage" => "Pourcentage remise",
    "Early Payment Discount" => "Remise paiement anticipé",
    "Set up early payment discounts" => "Configurer remises paiement anticipé",
    "Start Date" => "Date début",
    "End Date" => "Date fin",
    "fees_details" => "Détails frais",
    "Fine" => "Pénalité"
];

file_put_contents($langPath . '/fees.json', json_encode($fees, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT));
echo "   ✅ " . count($fees) . " lignes corrigées\n\n";

// 5. examination.json
echo "5. examination.json...\n";
$examination = [
    "exam_assign" => "Affectation examen",
    "select idcard" => "Sélectionner carte ID",
    "select certificate" => "Sélectionner certificat",
    "exam_title" => "Titre examen",
    "section" => "Section",
    "total_mark" => "Note totale",
    "select_exam_type" => "Sélectionner type examen",
    "exam_type" => "Type examen",
    "percent_from" => "Pourcentage de"
];

file_put_contents($langPath . '/examination.json', json_encode($examination, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT));
echo "   ✅ " . count($examination) . " lignes corrigées\n\n";

// 6. report.json
echo "6. report.json...\n";
$report = [
    "short_view" => "Vue courte",
    "details_view" => "Vue détaillée",
    "roll_number" => "Numéro matricule",
    "subject_code" => "Code matière",
    "subject_name" => "Nom matière",
    "Type" => "Type"
];

file_put_contents($langPath . '/report.json', json_encode($report, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT));
echo "   ✅ " . count($report) . " lignes corrigées\n\n";

// 7. staff.json
echo "7. staff.json...\n";
$staff = [
    "designation" => "Désignation",
    "staff_id" => "ID personnel",
    "departments" => "Départements"
];

file_put_contents($langPath . '/staff.json', json_encode($staff, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT));
echo "   ✅ " . count($staff) . " lignes corrigées\n\n";

// 8. settings.json
echo "8. settings.json...\n";
$settings = [
    "Session" => "Session",
    "Sessions" => "Sessions",
    "sessions" => "Sessions",
    "online_admission" => "Admission en ligne",
    "section" => "Section",
    "Subject Attendance" => "Présence matière",
    "Daily Attendance Report" => "Rapport présence quotidien",
    "notification_setup" => "Configuration notification",
    "group" => "Groupe",
    "type" => "Type",
    "merit_list" => "Liste mérite",
    "progress_card" => "Carte progrès",
    "due_fees" => "Frais dus",
    "contact_message" => "Message contact",
    "sections" => "Sections",
    "department_contact" => "Contact département",
    "event" => "Événement",
    "Gallery_category" => "Catégorie galerie",
    "All Conversations" => "Toutes conversations",
    "storage_settings" => "Paramètres stockage",
    "software_update" => "Mise à jour logiciel",
    "recaptcha_settings" => "Paramètres recaptcha",
    "payment_gateway_settings" => "Paramètres passerelle paiement",
    "email_settings" => "Paramètres email",
    "notification_setting" => "Paramètre notification",
    "blood_groups" => "Groupes sanguins",
    "tax setup" => "Configuration taxe",
    "absent_notification_setup" => "Configuration notification absence",
    "Notify To" => "Notifier à",
    "sending_time" => "Heure envoi",
    "notification_message" => "Message notification",
    "subject_list" => "Liste matières",
    "edit_religion" => "Modifier religion",
    "application_name" => "Nom application",
    "enter_you_application_name" => "Entrer nom application",
    "light_logo" => "Logo clair",
    "browse_light_logo" => "Parcourir logo clair",
    "dark_logo" => "Logo sombre",
    "browse_dark_logo" => "Parcourir logo sombre",
    "Currency" => "Devise",
    "enter_you_address" => "Entrer adresse",
    "enter_you_phone" => "Entrer téléphone",
    "enter_you_email" => "Entrer email",
    "school_about" => "À propos école",
    "file_system" => "Système fichiers",
    "twilio_phone_number" => "Numéro téléphone Twilio",
    "Approval Status" => "Statut approbation",
    "Publish Status" => "Statut publication",
    "Published At" => "Publié le"
];

file_put_contents($langPath . '/settings.json', json_encode($settings, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT));
echo "   ✅ " . count($settings) . " lignes corrigées\n\n";

echo "========================================\n";
echo "RÉSUMÉ CORRECTION FRANÇAISE\n";
echo "========================================\n";
echo "✅ common.json: 227 lignes (déjà fait)\n";
echo "✅ academic.json: 26 lignes (déjà fait)\n";
echo "✅ student_info.json: " . count($studentInfo) . " lignes\n";
echo "✅ attendance.json: " . count($attendance) . " lignes\n";
echo "✅ leave.json: " . count($leave) . " lignes\n";
echo "✅ fees.json: " . count($fees) . " lignes\n";
echo "✅ examination.json: " . count($examination) . " lignes\n";
echo "✅ report.json: " . count($report) . " lignes\n";
echo "✅ staff.json: " . count($staff) . " lignes\n";
echo "✅ settings.json: " . count($settings) . " lignes\n";
echo "========================================\n\n";

echo "✅ TOUS LES FICHIERS FRANÇAIS CORRIGÉS!\n";
echo "Nettoyez les caches:\n";
echo "   \"C:/xampp/php/php.exe\" CLEAR_ALL_CACHES_FINAL.php\n\n";

?>
