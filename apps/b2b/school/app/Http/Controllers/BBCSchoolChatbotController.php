<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Auth;
use App\Models\User;
use App\Models\StudentInfo\Student;
use App\Models\Staff\Staff;
use App\Models\StudentInfo\ParentGuardian;

class BBCSchoolChatbotController extends Controller
{
    /**
     * Chatbot IA pour BBC School Algeria
     * Support personnalisé selon le profil utilisateur
     */
    
    public function chat(Request $request)
    {
        try {
            $message = $request->input('message');
            $user = Auth::user();
            $userProfile = $this->getUserProfile($user);
            
            // Log de la conversation
            $this->logConversation($user?->id, $message, $userProfile['type']);
            
            // Générer réponse IA contextuelle pour BBC School
            $response = $this->generateBBCResponse($message, $userProfile);
            
            return response()->json([
                'success' => true,
                'response' => $response,
                'userType' => $userProfile['type'],
                'userInfo' => $userProfile['info'],
                'timestamp' => now()->format('H:i')
            ]);
            
        } catch (\Exception $e) {
            Log::error('BBC Chatbot Error: ' . $e->getMessage());
            
            return response()->json([
                'success' => false,
                'response' => $this->getFallbackResponse(),
                'error' => 'Erreur système BBC School'
            ], 500);
        }
    }
    
    /**
     * Actions rapides personnalisées BBC School
     */
    public function quickAction(Request $request)
    {
        $action = $request->input('action');
        $user = Auth::user();
        $userProfile = $this->getUserProfile($user);
        
        return response()->json([
            'success' => true,
            'response' => $this->getPersonalizedResponse($action, $userProfile),
            'action' => $action
        ]);
    }
    
    /**
     * Données contextuelles BBC School
     */
    public function getContextData()
    {
        $user = Auth::user();
        $userProfile = $this->getUserProfile($user);
        
        $data = [
            'user' => $user?->name ?? 'Visiteur',
            'userType' => $userProfile['type'],
            'userInfo' => $userProfile['info'],
            'school' => 'BBC School Algeria',
            'suggestions' => $this->getBBCSuggestions($userProfile['type'], $userProfile),
            'personalizedData' => $this->getPersonalizedData($userProfile)
        ];
        
        return response()->json($data);
    }
    
    /**
     * Détermine le profil complet de l'utilisateur BBC School
     */
    private function getUserProfile($user)
    {
        if (!$user) {
            return [
                'type' => 'visitor',
                'info' => null,
                'permissions' => []
            ];
        }
        
        // Vérifier si c'est un étudiant
        $student = $user->student;
        if ($student) {
            return [
                'type' => 'student',
                'info' => $student,
                'permissions' => ['view_courses', 'view_grades', 'submit_assignments'],
                'classes' => $this->getStudentClasses($student),
                'subjects' => $this->getStudentSubjects($student)
            ];
        }
        
        // Vérifier si c'est un parent
        $parent = $user->parent;
        if ($parent) {
            return [
                'type' => 'parent',
                'info' => $parent,
                'permissions' => ['view_child_progress', 'communicate_teachers'],
                'children' => $this->getParentChildren($parent)
            ];
        }
        
        // Vérifier si c'est un membre du staff
        $staff = $user->staff;
        if ($staff) {
            $role = $this->getStaffRole($staff);
            return [
                'type' => $role,
                'info' => $staff,
                'permissions' => $this->getStaffPermissions($staff),
                'classes' => $this->getTeacherClasses($staff),
                'subjects' => $this->getTeacherSubjects($staff)
            ];
        }
        
        return [
            'type' => 'user',
            'info' => $user,
            'permissions' => []
        ];
    }
    
    /**
     * Réponses IA spécialisées BBC School Algeria
     */
    private function generateBBCResponse($message, $userProfile)
    {
        $message = strtolower(trim($message));
        $userType = $userProfile['type'];
        
        // D'abord chercher dans la base de connaissances
        $knowledgeResponse = $this->searchKnowledgeBase($message, $userType);
        if ($knowledgeResponse) {
            return $knowledgeResponse;
        }
        
        // Réponses pour "mes cours" selon le profil
        if (str_contains($message, 'mes cours') || str_contains($message, 'cours')) {
            return $this->getMyCoursesResponse($userProfile);
        }
        
        // Réponses pour les notes personnalisées
        if (str_contains($message, 'mes notes') || str_contains($message, 'note')) {
            return $this->getMyGradesResponse($userProfile);
        }
        
        // Réponses pour l'emploi du temps personnel
        if (str_contains($message, 'emploi du temps') || str_contains($message, 'planning')) {
            return $this->getMyScheduleResponse($userProfile);
        }
        
        // Réponses selon le type d'utilisateur
        switch ($userType) {
            case 'student':
                return $this->getStudentResponse($message, $userProfile);
            case 'parent':
                return $this->getParentResponse($message, $userProfile);
            case 'teacher':
                return $this->getTeacherResponse($message, $userProfile);
            case 'admin':
                return $this->getAdminResponse($message, $userProfile);
            default:
                return $this->getVisitorResponse($message);
        }
    }
    
    /**
     * Recherche dans la base de connaissances BBC School
     */
    private function searchKnowledgeBase($message, $userType)
    {
        try {
            // Recherche par mots-clés et contenu
            $results = DB::table('bbc_knowledge_base')
                ->where('is_active', true)
                ->where(function($query) use ($userType) {
                    $query->where('user_type', $userType)
                          ->orWhere('user_type', 'all');
                })
                ->where(function($query) use ($message) {
                    $query->whereRaw('LOWER(title) LIKE ?', ['%' . $message . '%'])
                          ->orWhereRaw('LOWER(question) LIKE ?', ['%' . $message . '%'])
                          ->orWhereRaw('LOWER(answer) LIKE ?', ['%' . $message . '%']);
                })
                ->orderBy('priority', 'desc')
                ->first();
            
            if ($results) {
                // Incrémenter le compteur de vues
                DB::table('bbc_knowledge_base')
                    ->where('id', $results->id)
                    ->increment('view_count');
                
                return "📚 **" . $results->title . "**\n\n" . $results->answer;
            }
            
            // Si pas de résultat exact, recherche par mots-clés
            $keywordResults = DB::table('bbc_knowledge_base')
                ->where('is_active', true)
                ->where(function($query) use ($userType) {
                    $query->where('user_type', $userType)
                          ->orWhere('user_type', 'all');
                })
                ->get();
            
            foreach ($keywordResults as $item) {
                $keywords = json_decode($item->keywords, true) ?: [];
                foreach ($keywords as $keyword) {
                    if (str_contains($message, strtolower($keyword))) {
                        // Incrémenter le compteur
                        DB::table('bbc_knowledge_base')
                            ->where('id', $item->id)
                            ->increment('view_count');
                            
                        return "🔍 **" . $item->title . "**\n\n" . $item->answer;
                    }
                }
            }
            
            return null;
            
        } catch (\Exception $e) {
            Log::error('Knowledge Base Search Error: ' . $e->getMessage());
            return null;
        }
    }
    
    /**
     * Réponse "MES COURS" personnalisée
     */
    private function getMyCoursesResponse($userProfile)
    {
        $userType = $userProfile['type'];
        $userName = $userProfile['info']->user->name ?? 'Utilisateur';
        
        if ($userType === 'student') {
            $classes = $userProfile['classes'] ?? [];
            $subjects = $userProfile['subjects'] ?? [];
            
            $response = "📚 **Vos Cours - {$userName}**\n\n";
            
            if (!empty($classes)) {
                $className = isset($classes[0]->name) ? $classes[0]->name : 'Non définie';
                $response .= "🎓 **Votre Classe:** {$className}\n\n";
            }
            
            if (!empty($subjects)) {
                $response .= "📖 **Vos Matières:**\n";
                foreach ($subjects as $subject) {
                    $response .= "• {$subject->name}\n";
                }
                $response .= "\n";
            }
            
            $response .= "🔗 **Actions disponibles:**\n";
            $response .= "• Accéder aux ressources pédagogiques\n";
            $response .= "• Consulter l'emploi du temps\n";
            $response .= "• Voir les devoirs à rendre\n";
            $response .= "• Participer aux classes virtuelles\n\n";
            $response .= "📱 **BBC School Algeria** - Votre plateforme éducative personnalisée";
            
            return $response;
        }
        
        if ($userType === 'teacher') {
            $classes = $userProfile['classes'] ?? [];
            $subjects = $userProfile['subjects'] ?? [];
            
            $response = "👨‍🏫 **Vos Cours - Prof. {$userName}**\n\n";
            
                if (!empty($classes)) {
                    $response .= "🎯 **Vos Classes:**\n";
                    foreach ($classes as $class) {
                        $studentCount = isset($class->student_count) ? $class->student_count : 0;
                        $response .= "• {$class->name} ({$studentCount} étudiants)\n";
                    }
                    $response .= "\n";
                }            if (!empty($subjects)) {
                $response .= "📚 **Matières enseignées:**\n";
                foreach ($subjects as $subject) {
                    $response .= "• {$subject->name}\n";
                }
                $response .= "\n";
            }
            
            $response .= "⚡ **Gestion rapide:**\n";
            $response .= "• Créer un nouveau cours\n";
            $response .= "• Saisir les notes\n";
            $response .= "• Gérer les présences\n";
            $response .= "• Publier des devoirs\n\n";
            $response .= "🏫 **BBC School Algeria** - Plateforme enseignant";
            
            return $response;
        }
        
        if ($userType === 'parent') {
            $children = $userProfile['children'] ?? [];
            
            $response = "👨‍👩‍👧‍👦 **Cours de vos enfants - {$userName}**\n\n";
            
                if (!empty($children)) {
                    foreach ($children as $child) {
                        $className = isset($child->class->name) ? $child->class->name : 'Non définie';
                        $subjectCount = count(isset($child->subjects) ? $child->subjects : []);
                        $response .= "🧒 **{$child->user->name}:**\n";
                        $response .= "• Classe: {$className}\n";
                        $response .= "• Matières: {$subjectCount} matières\n\n";
                    }
                }            $response .= "📊 **Suivi disponible:**\n";
            $response .= "• Progression par matière\n";
            $response .= "• Présences/Absences\n";
            $response .= "• Communication avec enseignants\n";
            $response .= "• Bulletins et rapports\n\n";
            $response .= "👪 **BBC School Algeria** - Espace parent";
            
            return $response;
        }
        
        return "📚 **Courses BBC School Algeria**\n\nConnectez-vous pour accéder à vos cours personnalisés selon votre profil (étudiant, enseignant, parent).";
    }
    
    /**
     * Réponse "MES NOTES" personnalisée
     */
    private function getMyGradesResponse($userProfile)
    {
        $userType = $userProfile['type'];
        $userName = $userProfile['info']->user->name ?? 'Utilisateur';
        
        if ($userType === 'student') {
            // Récupérer les vraies notes de l'étudiant
            $studentId = $userProfile['info']->id;
            $grades = $this->getStudentGrades($studentId);
            
            $response = "📊 **Vos Notes - {$userName}**\n\n";
            
            if (!empty($grades)) {
                $response .= "🎯 **Résultats par matière:**\n";
                foreach ($grades as $grade) {
                    $response .= "• {$grade->subject}: {$grade->score}/20 ({$grade->grade})\n";
                }
                $response .= "\n📈 **Moyenne générale:** " . $this->calculateAverage($grades) . "/20\n\n";
            } else {
                $response .= "ℹ️ Aucune note disponible actuellement.\n\n";
            }
            
            $response .= "📋 **Actions:**\n";
            $response .= "• Télécharger le bulletin\n";
            $response .= "• Voir l'évolution temporelle\n";
            $response .= "• Comparer avec la classe\n";
            $response .= "• Objectifs d'amélioration\n\n";
            $response .= "🎓 **BBC School Algeria**";
            
            return $response;
        }
        
        return "📊 **Notes BBC School Algeria**\n\nConnectez-vous en tant qu'étudiant pour consulter vos notes personnalisées.";
    }
    
    /**
     * Obtenir les classes d'un étudiant
     */
    private function getStudentClasses($student)
    {
        try {
            // Adapter selon votre structure de base de données
            return DB::table('classes')
                ->where('id', $student->class_id)
                ->get();
        } catch (\Exception $e) {
            return [];
        }
    }
    
    /**
     * Obtenir les matières d'un étudiant
     */
    private function getStudentSubjects($student)
    {
        try {
            // Adapter selon votre structure de base de données
            return DB::table('subjects')
                ->join('class_subjects', 'subjects.id', '=', 'class_subjects.subject_id')
                ->where('class_subjects.class_id', $student->class_id)
                ->select('subjects.*')
                ->get();
        } catch (\Exception $e) {
            return [];
        }
    }
    
    /**
     * Obtenir les vraies notes d'un étudiant
     */
    private function getStudentGrades($studentId)
    {
        try {
            return DB::table('grades')
                ->join('subjects', 'grades.subject_id', '=', 'subjects.id')
                ->where('grades.student_id', $studentId)
                ->select('subjects.name as subject', 'grades.score', 'grades.grade')
                ->get();
        } catch (\Exception $e) {
            return [];
        }
    }
    
    /**
     * Calculer la moyenne
     */
    private function calculateAverage($grades)
    {
        if (empty($grades) || count($grades) === 0) return 0;
        
        $total = array_sum(array_column($grades->toArray(), 'score'));
        return round($total / count($grades), 2);
    }
    
    /**
     * Suggestions BBC School selon profil
     */
    private function getBBCSuggestions($userType, $userProfile)
    {
        $suggestions = [
            'visitor' => [
                "Comment m'inscrire à BBC School Algeria ?",
                "Quels sont les programmes disponibles ?",
                "Où se trouve l'école ?"
            ],
            'student' => [
                "Afficher mes cours",
                "Consulter mes notes",
                "Mon emploi du temps",
                "Mes devoirs à rendre"
            ],
            'parent' => [
                "Suivi de mon enfant",
                "Communiquer avec un enseignant",
                "Bulletin scolaire",
                "Calendrier des événements"
            ],
            'teacher' => [
                "Mes classes",
                "Saisir des notes", 
                "Gérer les présences",
                "Créer un cours"
            ],
            'admin' => [
                "Statistiques école",
                "Gestion utilisateurs",
                "Rapports académiques",
                "Configuration système"
            ]
        ];
        
        return $suggestions[$userType] ?? $suggestions['visitor'];
    }
    
    /**
     * Réponse de secours BBC School
     */
    private function getFallbackResponse()
    {
        return "🤖 **Assistant BBC School Algeria**\n\nJe suis là pour vous aider dans votre parcours éducatif.\n\nPosez-moi vos questions sur :\n• Vos cours et programme\n• Vos notes et résultats\n• L'emploi du temps\n• La vie scolaire\n\nComment puis-je vous accompagner ?";
    }
    
    /**
     * Log des conversations pour améliorer l'IA
     */
    private function logConversation($userId, $message, $userType)
    {
        try {
            DB::table('chatbot_logs')->insert([
                'user_id' => $userId,
                'user_type' => $userType,
                'message' => $message,
                'school' => 'BBC School Algeria',
                'ip_address' => request()->ip(),
                'user_agent' => request()->userAgent(),
                'created_at' => now(),
                'updated_at' => now()
            ]);
        } catch (\Exception $e) {
            Log::error('BBC Chatbot Log Error: ' . $e->getMessage());
        }
    }
    
    // Méthodes additionnelles à implémenter selon la structure de votre DB
    private function getParentChildren($parent) { return []; }
    private function getStaffRole($staff) { return 'teacher'; }
    private function getStaffPermissions($staff) { return []; }
    private function getTeacherClasses($staff) { return []; }
    private function getTeacherSubjects($staff) { return []; }
    private function getPersonalizedResponse($action, $userProfile) { return "Action: " . $action; }
    private function getPersonalizedData($userProfile) { return []; }
    private function getMyScheduleResponse($userProfile) { return "📅 Emploi du temps personnalisé en cours de développement"; }
    private function getStudentResponse($message, $userProfile) { return "Réponse étudiant BBC School"; }
    private function getParentResponse($message, $userProfile) { return "Réponse parent BBC School"; }
    private function getTeacherResponse($message, $userProfile) { return "Réponse enseignant BBC School"; }
    private function getAdminResponse($message, $userProfile) { return "Réponse admin BBC School"; }
    private function getVisitorResponse($message) { return "Bienvenue à BBC School Algeria !"; }
}