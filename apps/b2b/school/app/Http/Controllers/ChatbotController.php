<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;
use App\Models\User;
use App\Models\Staff;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Auth;

class ChatbotController extends Controller
{
    /**
     * Display the chatbot interface
     */
    public function index()
    {
        $user = Auth::user();
        $userType = $this->getUserType($user);
        
        return view('chatbot.index', [
            'user' => $user,
            'userType' => $userType,
            'bbcStats' => $this->getBBCStats()
        ]);
    }

    /**
     * Handle chatbot API requests
     */
    public function api(Request $request): JsonResponse
    {
        $action = $request->get('action');
        $message = $request->get('message', '');
        $userType = $request->get('user_type', 'student');
        
        switch ($action) {
            case 'chat':
                return $this->handleChat($message, $userType);
                
            case 'quick_action':
                return $this->handleQuickAction($request->get('quick_action'), $userType);
                
            case 'stats':
                return response()->json($this->getBBCStats());
                
            case 'user_data':
                return $this->getUserData();
                
            default:
                return response()->json(['error' => 'Action non reconnue'], 400);
        }
    }

    /**
     * Handle chat messages with AI responses
     */
    private function handleChat(string $message, string $userType): JsonResponse
    {
        $user = Auth::user();
        $response = $this->generateAIResponse($message, $userType, $user);
        
        // Log the conversation
        $this->logConversation($user->id ?? null, $message, $response, $userType);
        
        return response()->json([
            'response' => $response,
            'timestamp' => now()->format('H:i'),
            'user_type' => $userType
        ]);
    }

    /**
     * Generate AI response based on user type and message
     */
    private function generateAIResponse(string $message, string $userType, $user = null): string
    {
        $message = strtolower($message);
        
        // Responses spécialisées par type d'utilisateur
        switch ($userType) {
            case 'employee':
                return $this->getEmployeeResponse($message, $user);
                
            case 'parent':
                return $this->getParentResponse($message, $user);
                
            case 'student':
                return $this->getStudentResponse($message, $user);
                
            default:
                return $this->getGeneralResponse($message);
        }
    }

    /**
     * Responses for employees
     */
    private function getEmployeeResponse(string $message, $user): string
    {
        if (strpos($message, 'classe') !== false || strpos($message, 'class') !== false) {
            $classCount = DB::table('staff')->where('role_id', 2)->count();
            return "🏫 Vous gérez actuellement {$classCount} classes. Voulez-vous consulter les détails d'une classe spécifique ?";
        }
        
        if (strpos($message, 'rapport') !== false || strpos($message, 'report') !== false) {
            return "📊 Je peux générer des rapports automatiques pour :\n• Présences des étudiants\n• Performance académique\n• Communications parents\n• Statistiques de classe\n\nQuel type de rapport souhaitez-vous ?";
        }
        
        if (strpos($message, 'planning') !== false || strpos($message, 'schedule') !== false) {
            return "📅 Votre planning d'aujourd'hui :\n• 08h00-10h00 : Cours Mathématiques\n• 10h30-12h00 : Réunion équipe\n• 14h00-16h00 : Cours Sciences\n• 16h30-17h00 : Rencontre parents";
        }
        
        return "👨‍🏫 En tant qu'employé BBC School, je peux vous aider avec :\n• Gestion des classes\n• Génération de rapports\n• Planning des cours\n• Communication avec les parents\n\nQue souhaitez-vous faire ?";
    }

    /**
     * Responses for parents
     */
    private function getParentResponse(string $message, $user): string
    {
        if (strpos($message, 'note') !== false || strpos($message, 'grade') !== false) {
            return "📊 Notes de votre enfant cette semaine :\n• Mathématiques : 16/20 ✅\n• Français : 14/20 ✅\n• Sciences : 18/20 ✅\n• Anglais : 15/20 ✅\n\nMoyenne générale : 15.75/20";
        }
        
        if (strpos($message, 'absence') !== false || strpos($message, 'présence') !== false) {
            return "📅 Présences cette semaine :\n• Lundi : Présent ✅\n• Mardi : Présent ✅\n• Mercredi : Absent (justifié) ⚠️\n• Jeudi : Présent ✅\n• Vendredi : Présent ✅";
        }
        
        if (strpos($message, 'paiement') !== false || strpos($message, 'payment') !== false) {
            return "💳 État des paiements :\n• Frais de scolarité : ✅ Payé\n• Cantine : ✅ Payé\n• Transport : ⏳ En attente\n• Activités : ✅ Payé\n\nSouhaitez-vous effectuer un paiement ?";
        }
        
        return "👨‍👩‍👧‍👦 En tant que parent, je peux vous aider avec :\n• Consultation des notes\n• Suivi des présences\n• Communication avec les enseignants\n• Gestion des paiements\n\nQue souhaitez-vous consulter ?";
    }

    /**
     * Responses for students
     */
    private function getStudentResponse(string $message, $user): string
    {
        if (strpos($message, 'devoir') !== false || strpos($message, 'homework') !== false) {
            return "📚 Vos devoirs pour demain :\n• Mathématiques : Exercices page 45-47\n• Français : Rédaction sur l'environnement\n• Sciences : Lecture chapitre 8\n• Anglais : Vocabulaire leçon 12\n\nBesoin d'aide pour un devoir spécifique ?";
        }
        
        if (strpos($message, 'emploi') !== false || strpos($message, 'schedule') !== false) {
            return "📅 Votre emploi du temps demain :\n• 08h00-09h00 : Mathématiques\n• 09h00-10h00 : Français\n• 10h30-11h30 : Sciences\n• 11h30-12h30 : Sport\n• 14h00-15h00 : Anglais\n• 15h00-16h00 : Arts";
        }
        
        if (strpos($message, 'note') !== false || strpos($message, 'grade') !== false) {
            return "📊 Vos dernières notes :\n• Mathématiques : 16/20 ✅\n• Français : 14/20 ✅\n• Sciences : 18/20 ✅\n• Anglais : 15/20 ✅\n\nContinuez vos efforts !";
        }
        
        return "🎓 En tant qu'étudiant, je peux vous aider avec :\n• Aide aux devoirs\n• Consultation de l'emploi du temps\n• Révisions guidées\n• Consultation des notes\n\nQue souhaitez-vous faire ?";
    }

    /**
     * General responses
     */
    private function getGeneralResponse(string $message): string
    {
        if (strpos($message, 'bonjour') !== false || strpos($message, 'hello') !== false || strpos($message, 'مرحبا') !== false) {
            return "🤖 Bonjour ! Je suis l'assistant IA de BBC School Algeria. Comment puis-je vous aider aujourd'hui ?";
        }
        
        if (strpos($message, 'contact') !== false) {
            return "📞 Contacts BBC School Algeria :\n• Téléphone : +213-XX-XXX-XXX\n• Email : contact@bbcschoolalgeria.com\n• Facebook : facebook.com/bbc.bestbridgeforcreation\n• Adresse : Alger, Algérie";
        }
        
        return "🏫 Bienvenue à BBC School Algeria ! Je suis votre assistant IA. Je peux vous aider selon votre profil :\n• 👨‍🏫 Employés : Gestion administrative\n• 👨‍👩‍👧‍👦 Parents : Suivi scolaire\n• 🎓 Étudiants : Aide pédagogique\n\nQuel est votre profil ?";
    }

    /**
     * Handle quick actions
     */
    private function handleQuickAction(string $action, string $userType): JsonResponse
    {
        switch ($action) {
            case 'help':
                $response = $this->getHelpResponse($userType);
                break;
                
            case 'grades':
                $response = $this->getGradesResponse($userType);
                break;
                
            case 'schedule':
                $response = $this->getScheduleResponse($userType);
                break;
                
            case 'contact':
                $response = $this->getContactResponse();
                break;
                
            default:
                $response = "Action non reconnue.";
        }
        
        return response()->json([
            'response' => $response,
            'timestamp' => now()->format('H:i'),
            'action' => $action
        ]);
    }

    /**
     * Get BBC School statistics
     */
    private function getBBCStats(): array
    {
        return [
            'students' => DB::table('staff')->where('role_id', 3)->count(),
            'teachers' => DB::table('staff')->where('role_id', 2)->count(),
            'parents' => DB::table('staff')->where('role_id', 4)->count(),
            'classes' => 238,
            'active_sessions' => DB::table('sessions')->count(),
            'last_updated' => now()->format('Y-m-d H:i:s')
        ];
    }

    /**
     * Get user type
     */
    private function getUserType($user): string
    {
        if (!$user) return 'guest';
        
        // Logique pour déterminer le type d'utilisateur
        // Basé sur la table staff et role_id
        $staff = DB::table('staff')->where('user_id', $user->id)->first();
        
        if ($staff) {
            switch ($staff->role_id) {
                case 1:
                case 2:
                    return 'employee';
                case 3:
                    return 'student';
                case 4:
                    return 'parent';
            }
        }
        
        return 'student'; // Default
    }

    /**
     * Get user specific data
     */
    private function getUserData(): JsonResponse
    {
        $user = Auth::user();
        if (!$user) {
            return response()->json(['error' => 'Non authentifié'], 401);
        }
        
        $userData = [
            'name' => $user->name,
            'email' => $user->email,
            'type' => $this->getUserType($user),
            'stats' => $this->getBBCStats()
        ];
        
        return response()->json($userData);
    }

    /**
     * Handle chatbot messages - New API endpoint for widget
     */
    public function handleMessage(Request $request)
    {
        try {
            $message = $request->input('message');
            $userId = Auth::id();
            
            // Log du message
            $this->logChatMessage($message, $userId);
            
            // Générer la réponse basée sur le message
            $response = $this->generateResponse($message);
            
            return response()->json([
                'success' => true,
                'response' => $response,
                'timestamp' => now()->toISOString()
            ]);
            
        } catch (\Exception $e) {
            Log::error('Chatbot Error: ' . $e->getMessage());
            
            return response()->json([
                'success' => false,
                'response' => ___('Désolé, une erreur est survenue. Veuillez réessayer.'),
                'error' => $e->getMessage()
            ], 500);
        }
    }
    
    /**
     * Analytics du chatbot
     */
    public function analytics(Request $request)
    {
        try {
            $event = $request->input('event');
            $data = $request->input('data');
            $timestamp = $request->input('timestamp');
            $userId = Auth::id();
            
            // Log analytics
            DB::table('chatbot_analytics')->insert([
                'user_id' => $userId,
                'event' => $event,
                'data' => json_encode($data),
                'ip_address' => $request->ip(),
                'user_agent' => $request->userAgent(),
                'created_at' => now(),
                'updated_at' => now()
            ]);
            
            return response()->json(['success' => true]);
            
        } catch (\Exception $e) {
            Log::error('Chatbot Analytics Error: ' . $e->getMessage());
            return response()->json(['success' => false], 500);
        }
    }

    /**
     * Générer une réponse intelligente basée sur le message
     */
    private function generateResponse($message)
    {
        $message = strtolower(trim($message));
        
        // Réponses basées sur des mots-clés pour BBC School
        if (preg_match('/(inscription|inscrire|admission)/i', $message)) {
            return ___('Pour inscrire votre enfant à BBC School Algeria :') . "\n\n" .
                   '**📋 ' . ___('Documents requis :') . "**\n" .
                   '• ' . ___('Acte de naissance') . "\n" .
                   '• ' . ___('Photos d\'identité (4x4)') . "\n" .
                   '• ' . ___('Certificat médical') . "\n" .
                   '• ' . ___('Relevé de notes (si transfert)') . "\n\n" .
                   '**💰 ' . ___('Frais :') . "**\n" .
                   '• ' . ___('Inscription : 15,000 DA') . "\n" .
                   '• ' . ___('Scolarité : Variable selon le niveau') . "\n\n" .
                   '**📅 ' . ___('Période :') . '** ' . ___('Septembre - Octobre') . "\n\n" .
                   '📞 ' . ___('Contactez-nous pour un rendez-vous : +213-XX-XXX-XXX');
        }
        
        if (preg_match('/(tarif|prix|coût|frais|scolarité)/i', $message)) {
            return '**📊 ' . ___('Frais de scolarité annuels :') . "**\n\n" .
                   '🧒 **' . ___('Maternelle :') . '** 120,000 DA\n' .
                   '📚 **' . ___('Primaire :') . '** 150,000 DA\n' .
                   '🎓 **' . ___('Cycle Moyen :') . '** 180,000 DA\n\n' .
                   '**💳 ' . ___('Modalités de paiement :') . "**\n" .
                   '• ' . ___('Paiement en 3 tranches') . "\n" .
                   '• ' . ___('Réduction fratrie : -10%') . "\n" .
                   '• ' . ___('Paiement anticipé : -5%') . "\n\n" .
                   '📞 ' . ___('Devis personnalisé : +213-XX-XXX-XXX');
        }
        
        if (preg_match('/(contact|téléphone|adresse|lieu|où)/i', $message)) {
            return '**🏫 BBC School Algeria**\n\n' .
                   '📍 **' . ___('Adresse :') . '** ' . ___('Alger, Algérie') . "\n" .
                   '☎️ **' . ___('Téléphone :') . '** +213-XX-XXX-XXX\n' .
                   '📧 **Email :** contact@bbcschoolalgeria.com\n' .
                   '🌐 **Facebook :** bbc.bestbridgeforcreation\n\n' .
                   '**🕒 ' . ___('Horaires d\'accueil :') . "**\n" .
                   '• ' . ___('Dimanche - Jeudi : 8h00 - 16h00') . "\n" .
                   '• ' . ___('Samedi : 8h00 - 12h00') . "\n\n" .
                   '📅 ' . ___('Prenez rendez-vous pour une rencontre personnalisée !');
        }
        
        if (preg_match('/(programme|cours|matière|enseignement|pédagogie)/i', $message)) {
            return '**🎯 ' . ___('Notre offre pédagogique :') . "**\n\n" .
                   '**🧒 ' . ___('Maternelle (3-5 ans) :') . "**\n" .
                   '• ' . ___('Éveil et socialisation') . "\n" .
                   '• ' . ___('Préparation à la lecture et écriture') . "\n" .
                   '• ' . ___('Activités artistiques et sportives') . "\n\n" .
                   '**📚 ' . ___('Primaire (6-10 ans) :') . "**\n" .
                   '• ' . ___('Programme national renforcé') . "\n" .
                   '• ' . ___('Langues : Arabe, Français, Anglais') . "\n" .
                   '• ' . ___('Sciences et mathématiques') . "\n" .
                   '• ' . ___('Informatique dès le CP') . "\n\n" .
                   '**🎓 ' . ___('Cycle Moyen :') . "**\n" .
                   '• ' . ___('Sections scientifiques et littéraires') . "\n" .
                   '• ' . ___('Préparation intensive au BEM') . "\n" .
                   '• ' . ___('Orientation scolaire personnalisée') . "\n" .
                   '• ' . ___('Clubs scientifiques et culturels');
        }
        
        if (preg_match('/(visite|voir|découvrir|visiter|portes ouvertes)/i', $message)) {
            return '**🏫 ' . ___('Découvrez notre établissement !') . "**\n\n" .
                   '**📅 ' . ___('Journées portes ouvertes :') . "**\n" .
                   '• ' . ___('Chaque samedi de 9h à 12h') . "\n" .
                   '• ' . ___('Visite guidée gratuite') . "\n" .
                   '• ' . ___('Rencontre avec l\'équipe pédagogique') . "\n\n" .
                   '**👨‍🏫 ' . ___('Au programme de la visite :') . "**\n" .
                   '• ' . ___('Salles de classe modernes et équipées') . "\n" .
                   '• ' . ___('Laboratoires de sciences') . "\n" .
                   '• ' . ___('Bibliothèque et salle informatique') . "\n" .
                   '• ' . ___('Espaces de jeux et activités sportives') . "\n" .
                   '• ' . ___('Cantine et espaces de restauration') . "\n\n" .
                   '📞 ' . ___('Réservez votre visite : +213-XX-XXX-XXX') . "\n" .
                   '🗓️ ' . ___('Ou prenez rendez-vous pour une visite privée !');
        }
        
        // Réponse par défaut avec suggestions
        return ___('Bonjour ! Je suis l\'assistant virtuel de BBC School Algeria. 🤖') . "\n\n" .
               ___('Je peux vous renseigner sur :') . "\n\n" .
               '📝 **' . ___('Inscriptions') . '** - ' . ___('Documents, procédures, dates') . "\n" .
               '💰 **' . ___('Tarifs') . '** - ' . ___('Frais de scolarité, modalités de paiement') . "\n" .
               '📚 **' . ___('Programmes') . '** - ' . ___('Cursus, matières, pédagogie') . "\n" .
               '📞 **' . ___('Contact') . '** - ' . ___('Coordonnées, horaires, rendez-vous') . "\n" .
               '👁️ **' . ___('Visite') . '** - ' . ___('Journées portes ouvertes, visites privées') . "\n" .
               '🌟 **' . ___('Activités') . '** - ' . ___('Sports, clubs, sorties éducatives') . "\n\n" .
               ___('Que souhaitez-vous savoir sur BBC School Algeria ?');
    }
    
    /**
     * Log des messages du chatbot
     */
    private function logChatMessage($message, $userId = null)
    {
        try {
            DB::table('chatbot_logs')->insert([
                'user_id' => $userId,
                'message' => $message,
                'response_generated' => true,
                'ip_address' => request()->ip(),
                'user_agent' => request()->userAgent(),
                'created_at' => now(),
                'updated_at' => now()
            ]);
        } catch (\Exception $e) {
            Log::error('Failed to log chatbot message: ' . $e->getMessage());
        }
    }

    /**
     * Helper response methods
     */
    private function getHelpResponse(string $userType): string
    {
        $helps = [
            'employee' => "👨‍🏫 Aide pour employés :\n• Gestion des classes\n• Génération de rapports\n• Planning des cours\n• Communication parents",
            'parent' => "👨‍👩‍👧‍👦 Aide pour parents :\n• Consultation des notes\n• Suivi des présences\n• Communication enseignants\n• Gestion des paiements",
            'student' => "🎓 Aide pour étudiants :\n• Aide aux devoirs\n• Emploi du temps\n• Révisions guidées\n• Consultation des notes"
        ];
        
        return $helps[$userType] ?? $helps['student'];
    }

    private function getGradesResponse(string $userType): string
    {
        if ($userType === 'parent') {
            return "📊 Notes de votre enfant :\n• Mathématiques : 16/20\n• Français : 14/20\n• Sciences : 18/20\n• Moyenne : 16/20";
        }
        
        return "📊 Vos notes récentes :\n• Mathématiques : 16/20\n• Français : 14/20\n• Sciences : 18/20\n• Moyenne : 16/20";
    }

    private function getScheduleResponse(string $userType): string
    {
        return "📅 Planning d'aujourd'hui :\n• 08h00 : Mathématiques\n• 10h00 : Français\n• 14h00 : Sciences\n• 16h00 : Sport";
    }

    private function getContactResponse(): string
    {
        return "📞 BBC School Algeria :\n• Tel : +213-XX-XXX-XXX\n• Email : contact@bbcschoolalgeria.com\n• Facebook : bbc.bestbridgeforcreation";
    }
}