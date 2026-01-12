<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Carbon\Carbon;

class KnowledgeBaseSeeder extends Controller
{
    /**
     * Alimenter la base de connaissances BBC School Algeria
     * avec le Guide Utilisateur OnestSchool complet
     */
    
    public function seedOnestSchoolGuide()
    {
        $knowledgeData = [];
        
        // 1. GUIDE CONNEXION ET ACCÈS
        $knowledgeData[] = [
            'category' => 'guide',
            'user_type' => 'all',
            'title' => 'Comment se connecter à OnestSchool',
            'question' => 'Comment se connecter à la plateforme OnestSchool ?',
            'answer' => "**🔐 Connexion à OnestSchool**\n\n**1. Accès à la plateforme :**\n• Ouvrez votre navigateur\n• Rendez-vous sur : http://localhost/onestschooled-test/public/\n• Cliquez sur \"Se connecter\" en haut à droite\n\n**2. Saisie des identifiants :**\n• **Email** : Votre adresse email d'inscription\n• **Mot de passe** : Votre mot de passe personnel\n• Cochez \"Se souvenir de moi\" si souhaité\n\n**3. Première connexion :**\n• Vous serez redirigé vers votre tableau de bord\n• Complétez votre profil si demandé\n• Explorez les fonctionnalités selon votre rôle\n\n**❗ Problèmes de connexion :**\n• Vérifiez vos identifiants\n• Utilisez \"Mot de passe oublié\" si nécessaire\n• Contactez l'administration si le problème persiste",
            'keywords' => json_encode(['connexion', 'login', 'identifiants', 'email', 'mot de passe']),
            'language' => 'fr',
            'priority' => 5,
            'tags' => json_encode(['essentiel', 'connexion', 'accès'])
        ];
        
        // 2. GUIDE NAVIGATION GÉNÉRALE
        $knowledgeData[] = [
            'category' => 'guide',
            'user_type' => 'all',
            'title' => 'Navigation dans OnestSchool',
            'question' => 'Comment naviguer dans l\'interface OnestSchool ?',
            'answer' => "**🧭 Navigation OnestSchool**\n\n**Interface Principale :**\n• **Menu principal** : Barre de navigation en haut\n• **Sidebar** : Menu latéral avec toutes les fonctions\n• **Tableau de bord** : Vue d'ensemble personnalisée\n• **Profil utilisateur** : Coin supérieur droit\n\n**Structure des menus :**\n• **Accueil** : Tableau de bord principal\n• **Académique** : Cours, classes, matières\n• **Étudiants** : Gestion des élèves\n• **Personnel** : Enseignants et staff\n• **Examens** : Tests et évaluations\n• **Comptabilité** : Finances et paiements\n• **Rapports** : Statistiques et analyses\n• **Paramètres** : Configuration\n\n**Navigation rapide :**\n• Utilisez la barre de recherche\n• Favoris pour accès rapide\n• Raccourcis clavier disponibles\n• Menu contextuel clic-droit",
            'keywords' => json_encode(['navigation', 'menu', 'interface', 'sidebar', 'tableau de bord']),
            'language' => 'fr',
            'priority' => 4,
            'tags' => json_encode(['interface', 'navigation', 'utilisation'])
        ];
        
        // 3. GUIDE ÉTUDIANT
        $knowledgeData[] = [
            'category' => 'guide',
            'user_type' => 'student',
            'title' => 'Guide Étudiant OnestSchool',
            'question' => 'Comment utiliser OnestSchool en tant qu\'étudiant ?',
            'answer' => "**🎓 Guide Étudiant OnestSchool**\n\n**📚 MES COURS :**\n• Accès via \"Académique\" > \"Mes Cours\"\n• Consultation de vos matières inscrites\n• Planning des cours en temps réel\n• Ressources pédagogiques téléchargeables\n• Classes virtuelles et vidéoconférences\n\n**📊 MES NOTES :**\n• Menu \"Examens\" > \"Mes Résultats\"\n• Notes par matière et période\n• Moyennes et classements\n• Bulletins téléchargeables\n• Graphiques d'évolution\n\n**✏️ DEVOIRS :**\n• \"Académique\" > \"Devoirs\"\n• Consulter les devoirs assignés\n• Soumettre vos travaux en ligne\n• Vérifier les corrections\n• Dates limites et rappels\n\n**👤 MON PROFIL :**\n• Compléter informations personnelles\n• Photo de profil\n• Contacts d'urgence\n• Préférences de notification",
            'keywords' => json_encode(['étudiant', 'cours', 'notes', 'devoirs', 'profil']),
            'language' => 'fr',
            'priority' => 5,
            'tags' => json_encode(['étudiant', 'académique', 'cours'])
        ];
        
        // 4. GUIDE PARENT
        $knowledgeData[] = [
            'category' => 'guide',
            'user_type' => 'parent',
            'title' => 'Guide Parent OnestSchool',
            'question' => 'Comment suivre mon enfant sur OnestSchool ?',
            'answer' => "**👨‍👩‍👧‍👦 Guide Parent OnestSchool**\n\n**📊 SUIVI ENFANT :**\n• Tableau de bord parent personnalisé\n• Sélectionner l'enfant à suivre\n• Vue d'ensemble des résultats\n• Présences et absences\n• Comportement et remarques\n\n**📚 SUIVI ACADÉMIQUE :**\n• Notes en temps réel\n• Progression par matière\n• Devoirs et projets\n• Planning des cours\n• Calendrier des examens\n\n**💬 COMMUNICATION :**\n• \"Messages\" > \"Enseignants\"\n• Prendre rendez-vous\n• Participer aux réunions parents\n• Recevoir notifications importantes\n• Groupes de discussion classe\n\n**📄 DOCUMENTS :**\n• Bulletins de notes\n• Certificats de scolarité\n• Factures et paiements\n• Autorisations et formulaires\n• Rapports de comportement",
            'keywords' => json_encode(['parent', 'enfant', 'suivi', 'notes', 'communication']),
            'language' => 'fr',
            'priority' => 5,
            'tags' => json_encode(['parent', 'suivi', 'enfant'])
        ];
        
        // 5. GUIDE ENSEIGNANT
        $knowledgeData[] = [
            'category' => 'guide',
            'user_type' => 'teacher',
            'title' => 'Guide Enseignant OnestSchool',
            'question' => 'Comment gérer mes classes sur OnestSchool ?',
            'answer' => "**👨‍🏫 Guide Enseignant OnestSchool**\n\n**📚 MES CLASSES :**\n• \"Académique\" > \"Mes Classes\"\n• Vue d'ensemble des classes assignées\n• Liste des étudiants par classe\n• Planning d'enseignement\n• Matières enseignées\n\n**📝 GESTION NOTES :**\n• \"Examens\" > \"Saisie Notes\"\n• Créer évaluations et examens\n• Saisir notes rapidement\n• Calcul automatique moyennes\n• Publier résultats aux étudiants\n\n**✅ PRÉSENCES :**\n• \"Académique\" > \"Présences\"\n• Pointer présences quotidiennes\n• Gérer absences et retards\n• Justificatifs d'absence\n• Rapports de présence\n\n**📖 COURS ET RESSOURCES :**\n• Créer contenu pédagogique\n• Partager documents et ressources\n• Organiser classes virtuelles\n• Assigner devoirs et projets\n• Système de forum classe",
            'keywords' => json_encode(['enseignant', 'classes', 'notes', 'présences', 'cours']),
            'language' => 'fr',
            'priority' => 5,
            'tags' => json_encode(['enseignant', 'pédagogie', 'gestion'])
        ];
        
        // 6. FAQ TECHNIQUES
        $knowledgeData[] = [
            'category' => 'faq',
            'user_type' => 'all',
            'title' => 'Problèmes techniques courants',
            'question' => 'Que faire en cas de problème technique ?',
            'answer' => "**🔧 Support Technique OnestSchool**\n\n**Problèmes de connexion :**\n• Vérifier connexion internet\n• Vider cache navigateur (Ctrl+F5)\n• Essayer navigateur différent\n• Désactiver bloqueurs de publicité\n\n**Interface qui bug :**\n• Actualiser la page (F5)\n• Déconnexion/reconnexion\n• Vérifier compatibilité navigateur\n• Signaler le bug à l'administration\n\n**Upload de fichiers :**\n• Vérifier taille fichier (max 10MB)\n• Formats acceptés : PDF, DOC, JPG, PNG\n• Connexion stable requise\n• Réessayer si échec\n\n**Performance lente :**\n• Fermer onglets inutiles\n• Vider cache navigateur\n• Vérifier débit internet\n• Utiliser heures creuses\n\n**🆘 Contact Support :**\n• Email : support@bbcschool.dz\n• Téléphone : +213 XXX XXX XXX\n• Assistance en ligne via chatbot",
            'keywords' => json_encode(['technique', 'problème', 'bug', 'support', 'aide']),
            'language' => 'fr',
            'priority' => 3,
            'tags' => json_encode(['technique', 'support', 'dépannage'])
        ];
        
        // 7. FAQ SPÉCIFIQUE BBC SCHOOL
        $knowledgeData[] = [
            'category' => 'faq',
            'user_type' => 'all',
            'title' => 'Questions fréquentes BBC School Algeria',
            'question' => 'Informations spécifiques à BBC School Algeria',
            'answer' => "**🇩🇿 BBC School Algeria - FAQ**\n\n**Horaires établissement :**\n• Ouverture : 7h30 - 17h00\n• Pause déjeuner : 12h00 - 13h30\n• Samedi : 8h00 - 12h00\n• Fermé vendredi et dimanche\n\n**Contact BBC School :**\n• Adresse : [Adresse BBC School Algeria]\n• Téléphone : +213 XXX XXX XXX\n• Email : contact@bbcschool.dz\n• Site web : www.bbcschool.dz\n\n**Programmes d'études :**\n• Enseignement primaire\n• Enseignement moyen\n• Enseignement secondaire\n• Programme algérien + international\n• Langues : Arabe, Français, Anglais\n\n**Inscription :**\n• Dossier complet requis\n• Test d'admission selon niveau\n• Frais de scolarité\n• Assurance scolaire obligatoire\n\n**Services disponibles :**\n• Transport scolaire\n• Restauration\n• Activités extrascolaires\n• Suivi psychopédagogique",
            'keywords' => json_encode(['BBC School', 'Algeria', 'horaires', 'contact', 'inscription']),
            'language' => 'fr',
            'priority' => 4,
            'tags' => json_encode(['BBC School', 'Algeria', 'informations'])
        ];
        
        // 8. PROCÉDURES ADMINISTRATIVES
        $knowledgeData[] = [
            'category' => 'procedure',
            'user_type' => 'all',
            'title' => 'Procédures administratives OnestSchool',
            'question' => 'Comment effectuer les démarches administratives ?',
            'answer' => "**📋 Procédures Administratives**\n\n**INSCRIPTION NOUVELLE :**\n1. Créer compte sur OnestSchool\n2. Compléter dossier d'inscription\n3. Joindre documents requis\n4. Payer frais d'inscription\n5. Confirmation par l'école\n\n**CERTIFICATS ET ATTESTATIONS :**\n• \"Documents\" > \"Demandes\"\n• Sélectionner type de document\n• Remplir formulaire en ligne\n• Délai : 3-5 jours ouvrables\n• Récupération ou envoi postal\n\n**PAIEMENTS EN LIGNE :**\n• \"Comptabilité\" > \"Mes Paiements\"\n• Frais de scolarité mensuels\n• Activités extrascolaires\n• Transport et restauration\n• Cartes bancaires acceptées\n\n**CHANGEMENT D'INFORMATIONS :**\n• \"Profil\" > \"Modifier\"\n• Adresse, téléphone, email\n• Contact d'urgence\n• Informations médicales\n• Validation administration requise",
            'keywords' => json_encode(['procédure', 'administrative', 'inscription', 'certificat', 'paiement']),
            'language' => 'fr',
            'priority' => 3,
            'tags' => json_encode(['procédure', 'administration', 'démarche'])
        ];
        
        // Insérer toutes les données
        foreach ($knowledgeData as $item) {
            $item['created_at'] = Carbon::now();
            $item['updated_at'] = Carbon::now();
            
            DB::table('bbc_knowledge_base')->insert($item);
        }
        
        return response()->json([
            'success' => true,
            'message' => 'Base de connaissances OnestSchool créée avec succès',
            'entries_created' => count($knowledgeData)
        ]);
    }
}