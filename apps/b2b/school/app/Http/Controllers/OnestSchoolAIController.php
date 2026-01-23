<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Auth;

class OnestSchoolAIController extends Controller
{
    /**
     * Chatbot IA pour OnestSchool Platform
     * Aide les utilisateurs (étudiants, parents, enseignants, admins)
     */
    
    public function chat(Request $request)
    {
        try {
            $message = $request->input('message');
            $userType = $this->getUserType();
            $userId = Auth::id();
            
            // Log de la conversation
            $this->logConversation($userId, $message, $userType);
            
            // Générer réponse IA contextuelle
            $response = $this->generateAIResponse($message, $userType);
            
            return response()->json([
                'success' => true,
                'response' => $response,
                'userType' => $userType,
                'timestamp' => now()->format('H:i')
            ]);
            
        } catch (\Exception $e) {
            Log::error('OnestSchool AI Error: ' . $e->getMessage());
            
            return response()->json([
                'success' => false,
                'response' => $this->getFallbackResponse(),
                'error' => 'Erreur IA'
            ], 500);
        }
    }
    
    /**
     * Actions rapides contextuelles selon le type d'utilisateur
     */
    public function quickAction(Request $request)
    {
        $action = $request->input('action');
        $userType = $this->getUserType();
        
        $responses = $this->getQuickActionResponses($userType);
        
        return response()->json([
            'success' => true,
            'response' => $responses[$action] ?? $this->getFallbackResponse(),
            'action' => $action
        ]);
    }
    
    /**
     * Données contextuelles OnestSchool
     */
    public function getContextData()
    {
        $user = Auth::user();
        $userType = $this->getUserType();
        
        $data = [
            'user' => $user ? $user->name : 'Visiteur',
            'userType' => $userType,
            'platform' => 'OnestSchool',
            'stats' => $this->getPlatformStats(),
            'suggestions' => $this->getSuggestions($userType)
        ];
        
        return response()->json($data);
    }
    
    /**
     * Détermine le type d'utilisateur OnestSchool
     */
    private function getUserType()
    {
        if (!Auth::check()) {
            return 'visitor';
        }
        
        $user = Auth::user();
        
        // Vérifier dans la table staff pour le rôle
        $staff = DB::table('staff')->where('user_id', $user->id)->first();
        
        if ($staff) {
            switch ($staff->role_id) {
                case 1: return 'admin';
                case 2: return 'teacher';
                case 3: return 'student';
                case 4: return 'parent';
                default: return 'staff';
            }
        }
        
        return 'user';
    }
    
    /**
     * IA Réponses contextuelles OnestSchool
     */
    private function generateAIResponse($message, $userType)
    {
        $message = strtolower(trim($message));
        
        // Réponses spécialisées par type d'utilisateur OnestSchool
        
        // Pour les VISITEURS (non connectés)
        if ($userType === 'visitor') {
            return $this->getVisitorResponse($message);
        }
        
        // Pour les ÉTUDIANTS
        if ($userType === 'student') {
            return $this->getStudentResponse($message);
        }
        
        // Pour les PARENTS
        if ($userType === 'parent') {
            return $this->getParentResponse($message);
        }
        
        // Pour les ENSEIGNANTS
        if ($userType === 'teacher') {
            return $this->getTeacherResponse($message);
        }
        
        // Pour les ADMINS
        if ($userType === 'admin') {
            return $this->getAdminResponse($message);
        }
        
        return $this->getGeneralResponse($message);
    }
    
    /**
     * Réponses pour les visiteurs (découverte de la plateforme)
     */
    private function getVisitorResponse($message)
    {
        if (str_contains($message, 'inscription') || str_contains($message, 'rejoindre')) {
            return "🎓 **Bienvenue sur OnestSchool !**\n\nPour rejoindre notre plateforme éducative :\n• 📋 Créez votre compte étudiant/parent\n• 🏫 Choisissez votre établissement\n• 📚 Accédez aux cours et ressources\n• 👨‍🏫 Connectez-vous avec vos enseignants\n\n[Se connecter](/login) • [S'inscrire](/register)";
        }
        
        if (str_contains($message, 'fonctionnalité') || str_contains($message, 'que fait')) {
            return "🚀 **OnestSchool - Plateforme Éducative Complète**\n\n📚 **Gestion Académique :**\n• Cours en ligne et ressources\n• Emplois du temps personnalisés\n• Notes et évaluations\n• Suivi des présences\n\n👥 **Communication :**\n• Messages entre enseignants/parents\n• Notifications automatiques\n• Forums de discussion\n\n📊 **Rapports & Analytics :**\n• Tableaux de bord personnalisés\n• Statistiques de progression\n• Rapports détaillés";
        }
        
        return "🌟 **Découvrez OnestSchool !**\n\nJe suis votre assistant IA pour cette plateforme éducative.\n\n🔹 Posez-moi des questions sur :\n• Comment s'inscrire\n• Les fonctionnalités disponibles\n• L'utilisation de la plateforme\n• Les différents profils utilisateurs\n\nQue souhaitez-vous savoir ?";
    }
    
    /**
     * Réponses pour les étudiants
     */
    private function getStudentResponse($message)
    {
        if (str_contains($message, 'cours') || str_contains($message, 'matière')) {
            return "📚 **Vos Cours OnestSchool**\n\n• Accédez à vos cours depuis le tableau de bord\n• Consultez l'emploi du temps personnalisé\n• Téléchargez les ressources pédagogiques\n• Participez aux classes virtuelles\n\n📖 Besoin d'aide pour une matière spécifique ?";
        }
        
        if (str_contains($message, 'note') || str_contains($message, 'résultat')) {
            return "📊 **Consultation des Notes**\n\n• Rendez-vous dans 'Mes Notes'\n• Consultez vos moyennes par matière\n• Suivez votre évolution dans le temps\n• Téléchargez vos bulletins\n\n🎯 Voulez-vous des conseils pour améliorer vos résultats ?";
        }
        
        if (str_contains($message, 'devoir') || str_contains($message, 'exercice')) {
            return "✏️ **Devoirs & Exercices**\n\n• Consultez vos devoirs à rendre\n• Soumettez vos travaux en ligne\n• Vérifiez les corrections\n• Planifiez votre travail\n\n📅 Dates limites importantes à retenir !";
        }
        
        return "🎓 **Assistant Étudiant OnestSchool**\n\nJe peux vous aider avec :\n• 📚 Navigation dans vos cours\n• 📊 Consultation des notes\n• ✏️ Gestion des devoirs\n• 📅 Emploi du temps\n• 🤝 Communication avec enseignants\n\nQue puis-je faire pour vous ?";
    }
    
    /**
     * Réponses pour les parents
     */
    private function getParentResponse($message)
    {
        if (str_contains($message, 'enfant') || str_contains($message, 'suivi')) {
            return "👨‍👩‍👧‍👦 **Suivi de votre enfant**\n\n• Consultez ses notes en temps réel\n• Vérifiez ses présences/absences\n• Communiquez avec ses enseignants\n• Recevez des notifications importantes\n\n📱 Tout depuis votre tableau de bord parent !";
        }
        
        if (str_contains($message, 'communication') || str_contains($message, 'enseignant')) {
            return "💬 **Communication avec l'équipe pédagogique**\n\n• Messagerie directe avec les enseignants\n• Prise de rendez-vous en ligne\n• Participation aux réunions virtuelles\n• Suivi des recommandations\n\n🤝 Restez connecté avec l'éducation de votre enfant !";
        }
        
        return "👪 **Espace Parent OnestSchool**\n\nVotre tableau de bord pour :\n• 📊 Suivre les résultats scolaires\n• ✅ Vérifier les présences\n• 💬 Communiquer avec l'école\n• 📅 Consulter l'emploi du temps\n• 💰 Gérer les paiements\n\nComment puis-je vous accompagner ?";
    }
    
    /**
     * Réponses pour les enseignants
     */
    private function getTeacherResponse($message)
    {
        if (str_contains($message, 'classe') || str_contains($message, 'élève')) {
            return "👨‍🏫 **Gestion de vos classes**\n\n• Consultez la liste de vos élèves\n• Saisissez les notes rapidement\n• Gérez les présences/absences\n• Créez des groupes de travail\n\n📋 Outils pédagogiques à votre disposition !";
        }
        
        if (str_contains($message, 'planning') || str_contains($message, 'emploi')) {
            return "📅 **Votre Planning d'Enseignement**\n\n• Consultez votre emploi du temps\n• Planifiez vos cours\n• Réservez des salles\n• Gérez vos remplacements\n\n⏰ Organisation optimisée pour votre enseignement !";
        }
        
        return "🍎 **Espace Enseignant OnestSchool**\n\nVos outils pédagogiques :\n• 📚 Création de cours en ligne\n• 📊 Saisie des évaluations\n• 👥 Gestion des classes\n• 📱 Communication avec parents\n• 📋 Rapports et statistiques\n\nEn quoi puis-je vous assister ?";
    }
    
    /**
     * Réponses pour les administrateurs
     */
    private function getAdminResponse($message)
    {
        if (str_contains($message, 'rapport') || str_contains($message, 'statistique')) {
            return "📊 **Analytics & Rapports OnestSchool**\n\n• Tableaux de bord en temps réel\n• Statistiques d'utilisation\n• Rapports académiques\n• Analyses de performance\n\n📈 Pilotage data-driven de votre établissement !";
        }
        
        if (str_contains($message, 'utilisateur') || str_contains($message, 'gestion')) {
            return "⚙️ **Administration Utilisateurs**\n\n• Création/modification des comptes\n• Attribution des rôles et permissions\n• Gestion des groupes et classes\n• Paramétrage de la plateforme\n\n🔧 Contrôle total de votre environnement !";
        }
        
        return "👑 **Panneau Administrateur OnestSchool**\n\nGestion complète :\n• 👥 Utilisateurs et permissions\n• 🏫 Configuration établissement\n• 📊 Analytics et rapports\n• ⚙️ Paramètres système\n• 🔒 Sécurité et sauvegardes\n\nQuel aspect souhaitez-vous gérer ?";
    }
    
    /**
     * Actions rapides selon le profil utilisateur
     */
    private function getQuickActionResponses($userType)
    {
        $actions = [
            'visitor' => [
                'inscription' => "Créer un compte sur OnestSchool",
                'demo' => "Découvrir les fonctionnalités",
                'contact' => "Contacter l'équipe support",
                'info' => "En savoir plus sur la plateforme"
            ],
            'student' => [
                'courses' => "Accéder à mes cours",
                'grades' => "Consulter mes notes", 
                'schedule' => "Voir mon emploi du temps",
                'assignments' => "Mes devoirs à rendre"
            ],
            'parent' => [
                'child_progress' => "Suivi de mon enfant",
                'messages' => "Messages enseignants",
                'attendance' => "Présences/Absences",
                'meetings' => "Prendre rendez-vous"
            ],
            'teacher' => [
                'my_classes' => "Mes classes",
                'gradebook' => "Saisir des notes",
                'attendance' => "Gérer présences",
                'resources' => "Ressources pédagogiques"
            ],
            'admin' => [
                'users' => "Gestion utilisateurs",
                'reports' => "Rapports & Analytics", 
                'settings' => "Configuration système",
                'backups' => "Sauvegardes"
            ]
        ];
        
        return $actions[$userType] ?? $actions['visitor'];
    }
    
    /**
     * Statistiques de la plateforme
     */
    private function getPlatformStats()
    {
        try {
            return [
                'students' => DB::table('staff')->where('role_id', 3)->count(),
                'teachers' => DB::table('staff')->where('role_id', 2)->count(),
                'parents' => DB::table('staff')->where('role_id', 4)->count(),
                'active_users' => DB::table('users')->where('status', 1)->count(),
                'total_users' => DB::table('users')->count()
            ];
        } catch (\Exception $e) {
            return ['error' => 'Stats indisponibles'];
        }
    }
    
    /**
     * Suggestions contextuelles
     */
    private function getSuggestions($userType)
    {
        $suggestions = [
            'visitor' => [
                "Comment m'inscrire sur OnestSchool ?",
                "Quelles sont les fonctionnalités disponibles ?",
                "Est-ce que la plateforme est gratuite ?"
            ],
            'student' => [
                "Où trouver mes cours ?",
                "Comment consulter mes notes ?",
                "Comment rendre un devoir ?"
            ],
            'parent' => [
                "Comment suivre les résultats de mon enfant ?",
                "Comment contacter un enseignant ?",
                "Où voir l'emploi du temps ?"
            ],
            'teacher' => [
                "Comment créer un nouveau cours ?",
                "Comment saisir les notes ?",
                "Comment gérer les présences ?"
            ],
            'admin' => [
                "Comment ajouter un nouvel utilisateur ?",
                "Où voir les statistiques d'usage ?",
                "Comment configurer l'établissement ?"
            ]
        ];
        
        return $suggestions[$userType] ?? $suggestions['visitor'];
    }
    
    /**
     * Réponse de secours
     */
    private function getFallbackResponse()
    {
        return "🤖 **Assistant IA OnestSchool**\n\nJe suis là pour vous aider à naviguer sur cette plateforme éducative.\n\nPosez-moi vos questions sur :\n• Navigation et utilisation\n• Fonctionnalités disponibles\n• Résolution de problèmes\n• Conseils d'usage\n\nComment puis-je vous assister ?";
    }
    
    /**
     * Réponse générale
     */
    private function getGeneralResponse($message)
    {
        if (str_contains($message, 'aide') || str_contains($message, 'help')) {
            return $this->getFallbackResponse();
        }
        
        return "💡 Je n'ai pas bien compris votre demande.\n\nEssayez de reformuler ou utilisez les suggestions disponibles.\n\nVous pouvez me demander de l'aide sur les fonctionnalités OnestSchool !";
    }
    
    /**
     * Log des conversations pour améliorer l'IA
     */
    private function logConversation($userId, $message, $userType)
    {
        try {
            DB::table('ai_conversations')->insert([
                'user_id' => $userId,
                'user_type' => $userType,
                'message' => $message,
                'platform' => 'OnestSchool',
                'ip_address' => request()->ip(),
                'user_agent' => request()->userAgent(),
                'created_at' => now(),
                'updated_at' => now()
            ]);
        } catch (\Exception $e) {
            Log::error('AI Conversation Log Error: ' . $e->getMessage());
        }
    }
}