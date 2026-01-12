<?php
/**
 * ACTIVATION DE LA VERSION FRANÇAISE ORIGINALE
 * Traduit tous les fichiers JSON français
 */

echo "=== ACTIVATION DU FRANÇAIS ===\n\n";

$frenchTranslations = [
    // Dashboard
    'Dashboard' => 'Tableau de bord',
    'Student' => 'Étudiant',
    'Parent' => 'Parent',
    'fees_collection' => 'Collecte des frais',
    'Revenue' => 'Revenu',
    'total_income' => 'Revenu total',
    'total_expense' => 'Dépense totale',
    'total_balance' => 'Solde total',
    'income_and_expense' => 'Revenus et dépenses',
    'upcoming_events' => 'Événements à venir',
    'todays_attendance' => 'Présence aujourd\'hui',
    'welcome' => 'Bienvenue',
    'total_students' => 'Total des étudiants',
    'total_teachers' => 'Total des enseignants',
    'total_parents' => 'Total des parents',

    // Menu principal
    'Branch' => 'Branche',
    'Online Admission' => 'Admission en ligne',
    'online_admission' => 'Admission en ligne',
    'Student Info' => 'Info étudiant',
    'student_info' => 'Info étudiant',
    'student' => 'étudiant',
    'admission' => 'admission',
    'student_list' => 'Liste des étudiants',
    'Student List' => 'Liste des étudiants',
    'student_promote' => 'Promouvoir étudiant',
    'Student Promote' => 'Promouvoir étudiant',
    'disabled_students' => 'Étudiants désactivés',
    'Disabled Students' => 'Étudiants désactivés',

    // Academic
    'Academic' => 'Académique',
    'academic' => 'académique',
    'class' => 'classe',
    'Class' => 'Classe',
    'section' => 'section',
    'Section' => 'Section',
    'shift' => 'équipe',
    'Shift' => 'Équipe',
    'class_setup' => 'Configuration de classe',
    'Class Setup' => 'Configuration de classe',
    'subject' => 'matière',
    'Subject' => 'Matière',
    'subject_assign' => 'Affectation de matière',
    'Subject Assign' => 'Affectation de matière',
    'class_room' => 'salle de classe',
    'Class Room' => 'Salle de classe',
    'teacher' => 'enseignant',
    'Teacher' => 'Enseignant',

    // Routines
    'Routines' => 'Horaires',
    'class_routine' => 'Horaire de classe',
    'Class Routine' => 'Horaire de classe',
    'exam_routine' => 'Horaire d\'examen',
    'Exam Routine' => 'Horaire d\'examen',

    // Attendance
    'Attendance' => 'Présence',
    'attendance' => 'présence',
    'student_attendance' => 'Présence des étudiants',
    'Student Attendance' => 'Présence des étudiants',
    'attendance_report' => 'Rapport de présence',
    'Attendance Report' => 'Rapport de présence',
    'Present' => 'Présent',
    'Absent' => 'Absent',

    // Leave
    'Leave' => 'Congé',
    'leave' => 'congé',
    'leave_type' => 'Type de congé',
    'Leave Type' => 'Type de congé',
    'leave_request' => 'Demande de congé',
    'Leave Request' => 'Demande de congé',
    'leave_list' => 'Liste des congés',
    'Leave List' => 'Liste des congés',

    // Fees
    'Fees' => 'Frais',
    'fees' => 'frais',
    'fees_group' => 'Groupe de frais',
    'Fees Group' => 'Groupe de frais',
    'fees_type' => 'Type de frais',
    'Fees Type' => 'Type de frais',
    'fees_master' => 'Maître des frais',
    'Fees Master' => 'Maître des frais',
    'fees_assign' => 'Affectation des frais',
    'Fees Assign' => 'Affectation des frais',
    'fees_collect' => 'Collecte des frais',
    'Fees Collect' => 'Collecte des frais',
    'fees_report' => 'Rapport des frais',
    'Fees Report' => 'Rapport des frais',

    // Examination
    'Examination' => 'Examen',
    'examination' => 'examen',
    'Exam' => 'Examen',
    'exam' => 'examen',
    'exam_setup' => 'Configuration d\'examen',
    'Exam Setup' => 'Configuration d\'examen',
    'marks_register' => 'Registre des notes',
    'Marks Register' => 'Registre des notes',
    'marks_grade' => 'Niveau des notes',
    'Marks Grade' => 'Niveau des notes',
    'Online Examination' => 'Examen en ligne',

    // Library
    'Library' => 'Bibliothèque',
    'book_category' => 'Catégorie de livre',
    'Book Category' => 'Catégorie de livre',
    'Book' => 'Livre',
    'member_category' => 'Catégorie de membre',
    'Member Category' => 'Catégorie de membre',
    'Member' => 'Membre',
    'issue_book' => 'Prêter un livre',
    'Issue Book' => 'Prêter un livre',

    // Accounts
    'Accounts' => 'Comptes',
    'account' => 'compte',
    'Account' => 'Compte',
    'income' => 'revenu',
    'Income' => 'Revenu',
    'expense' => 'dépense',
    'Expense' => 'Dépense',

    // Report
    'Report' => 'Rapport',
    'student_report' => 'Rapport étudiant',
    'Student Report' => 'Rapport étudiant',

    // Staff
    'Staff Manage' => 'Gestion du personnel',
    'staff_manage' => 'gestion du personnel',
    'staff' => 'personnel',
    'Staff' => 'Personnel',
    'staff_list' => 'Liste du personnel',
    'Staff List' => 'Liste du personnel',
    'add_staff' => 'Ajouter personnel',
    'Add Staff' => 'Ajouter personnel',

    // Users & Roles
    'role' => 'rôle',
    'Role' => 'Rôle',
    'permission' => 'permission',
    'Permission' => 'Permission',

    // Settings
    'Settings' => 'Paramètres',
    'settings' => 'paramètres',
    'general_settings' => 'Paramètres généraux',
    'General Settings' => 'Paramètres généraux',
    'email_settings' => 'Paramètres email',
    'Email Settings' => 'Paramètres email',
    'sms_settings' => 'Paramètres SMS',
    'Sms Settings' => 'Paramètres SMS',

    // Others
    'Subscribers' => 'Abonnés',
    'subscribers' => 'abonnés',
    'Contact Message' => 'Message de contact',
    'contact_message' => 'message de contact',
    'Website Setup' => 'Configuration du site',
    'Website_setup' => 'Configuration du site',
    'Gallery' => 'Galerie',
    'Live Chat' => 'Chat en direct',
    'Forums' => 'Forums',
    'Memories' => 'Souvenirs',
    'language' => 'langue',

    // Common
    'Search' => 'Rechercher',
    'Cancel' => 'Annuler',
    'Yes' => 'Oui',
    'No' => 'Non',
    'Notifications' => 'Notifications',
    'logout' => 'déconnexion',
    'my_profile' => 'Mon profil',
    'update_password' => 'Mettre à jour le mot de passe',
    'add' => 'Ajouter',
    'edit' => 'Modifier',
    'delete' => 'Supprimer',
    'action' => 'Action',
    'status' => 'Statut',
    'active' => 'actif',
    'inactive' => 'inactif',
    'name' => 'nom',
    'email' => 'email',
    'phone' => 'téléphone',
    'address' => 'adresse',
    'date' => 'date',
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
        if (isset($translations[$key])) {
            // Ne mettre à jour que si ce n'est pas déjà en français
            if (!preg_match('/[àâäéèêëïîôùûüÿçœæÀÂÄÉÈÊËÏÎÔÙÛÜŸÇŒÆ]/', $value)) {
                $json[$key] = $translations[$key];
                $updated++;
            }
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

// Traiter tous les fichiers JSON français
$langDir = __DIR__ . '/lang/fr/';
$jsonFiles = glob($langDir . '*.json');

$totalUpdated = 0;

foreach ($jsonFiles as $filePath) {
    $fileName = basename($filePath);
    $updated = updateJsonFile($filePath, $frenchTranslations);

    if ($updated > 0) {
        echo "✅ $fileName: $updated traduction(s) mise(s) à jour\n";
        $totalUpdated += $updated;
    }
}

echo "\n=== ACTIVATION DU FRANÇAIS TERMINÉE ===\n\n";
echo "Total: $totalUpdated traduction(s) française(s) ajoutée(s)\n\n";

echo "Le français est maintenant disponible comme langue secondaire!\n\n";

echo "CONFIGURATION:\n";
echo "- Langue par défaut: Arabe (ar)\n";
echo "- Langue secondaire: Français (fr) ✅ ACTIVÉE\n\n";

echo "Les utilisateurs peuvent choisir entre:\n";
echo "- 🇩🇿 العربية (Arabe) - Langue par défaut\n";
echo "- 🇫🇷 Français - Langue secondaire\n\n";

echo "✅ FRANÇAIS ACTIVÉ!\n";
