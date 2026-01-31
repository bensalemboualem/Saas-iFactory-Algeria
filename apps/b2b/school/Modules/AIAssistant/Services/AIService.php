<?php

namespace Modules\AIAssistant\Services;

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Log;

class AIService
{
    protected $provider;
    protected $apiKey;
    protected $model;
    protected $maxTokens;
    protected $temperature;

    public function __construct()
    {
        $this->provider = config('aiassistant.provider', 'openai');
        $this->apiKey = config('aiassistant.api_key');
        $this->model = config('aiassistant.model', 'gpt-4o-mini');
        $this->maxTokens = config('aiassistant.max_tokens', 1000);
        $this->temperature = config('aiassistant.temperature', 0.7);
    }

    /**
     * Main chat function with RAG support
     */
    public function chat(string $message, ?int $userId = null, string $role = 'guest'): array
    {
        try {
            // 1. Search relevant knowledge base entries (RAG)
            $context = $this->retrieveContext($message);

            // 2. Build system prompt with school context
            $systemPrompt = $this->buildSystemPrompt($context, $role);

            // 3. Get conversation history if user is logged in
            $history = $userId ? $this->getConversationHistory($userId) : [];

            // 4. Call AI API
            $response = $this->callAI($systemPrompt, $message, $history);

            // 5. Log conversation
            $this->logConversation($userId, $message, $response, $role);

            // 6. Update analytics
            $this->updateAnalytics($role);

            return [
                'success' => true,
                'response' => $response,
                'context_used' => !empty($context)
            ];
        } catch (\Exception $e) {
            Log::error('AI Service Error: ' . $e->getMessage());
            return [
                'success' => false,
                'response' => $this->getFallbackResponse($message),
                'error' => $e->getMessage()
            ];
        }
    }

    /**
     * Retrieve relevant context from knowledge base (RAG)
     */
    protected function retrieveContext(string $query): string
    {
        // Search in knowledge base table
        $keywords = $this->extractKeywords($query);

        $results = DB::table('bbc_knowledge_base')
            ->where(function($q) use ($keywords) {
                foreach ($keywords as $keyword) {
                    $q->orWhere('question', 'LIKE', "%{$keyword}%")
                      ->orWhere('answer', 'LIKE', "%{$keyword}%")
                      ->orWhere('keywords', 'LIKE', "%{$keyword}%");
                }
            })
            ->orderBy('priority', 'desc')
            ->limit(3)
            ->get();

        if ($results->isEmpty()) {
            // Fallback to FAQ/settings
            return $this->getGeneralSchoolContext();
        }

        $context = "Informations pertinentes de la base de connaissances:\n\n";
        foreach ($results as $result) {
            $context .= "Q: {$result->question}\nR: {$result->answer}\n\n";
        }

        return $context;
    }

    /**
     * Extract keywords from user query
     */
    protected function extractKeywords(string $query): array
    {
        $stopWords = ['le', 'la', 'les', 'de', 'du', 'des', 'un', 'une', 'et', 'ou', 'je', 'tu', 'il', 'elle',
                      'nous', 'vous', 'ils', 'elles', 'mon', 'ma', 'mes', 'son', 'sa', 'ses', 'comment',
                      'quoi', 'que', 'qui', 'est', 'sont', 'pour', 'avec', 'dans', 'sur', 'par'];

        $words = preg_split('/\s+/', mb_strtolower($query));
        $keywords = array_filter($words, function($word) use ($stopWords) {
            return strlen($word) > 2 && !in_array($word, $stopWords);
        });

        return array_values($keywords);
    }

    /**
     * Build system prompt with school context
     */
    protected function buildSystemPrompt(string $context, string $role): string
    {
        $schoolName = setting('application_name') ?? 'IAFactory School';

        $basePrompt = <<<PROMPT
Tu es l'assistant virtuel de {$schoolName}, une plateforme de gestion scolaire moderne en Algérie.

CONTEXTE ÉCOLE:
- Système éducatif algérien (Primaire: 1AP-5AP, Moyen: 1AM-4AM, Secondaire: 1AS-3AS)
- Langues: Arabe, Français, Anglais, Amazigh
- Monnaie: Dinar Algérien (DZD)

TON RÔLE:
- Aider les parents, élèves et enseignants avec leurs questions
- Fournir des informations sur les notes, présences, frais, emplois du temps
- Guider pour l'utilisation de la plateforme
- Répondre en français ou arabe selon la langue de l'utilisateur

RÈGLES:
- Sois professionnel, courtois et précis
- Si tu ne connais pas la réponse, oriente vers le secrétariat
- Ne divulgue jamais d'informations personnelles d'autres élèves
- Pour les questions techniques, suggère de contacter le support

{$context}
PROMPT;

        // Add role-specific instructions
        switch ($role) {
            case 'parent':
                $basePrompt .= "\n\nL'utilisateur est un PARENT. Il peut demander des infos sur son enfant.";
                break;
            case 'student':
                $basePrompt .= "\n\nL'utilisateur est un ÉLÈVE. Aide-le avec ses devoirs et questions scolaires.";
                break;
            case 'teacher':
                $basePrompt .= "\n\nL'utilisateur est un ENSEIGNANT. Aide-le avec la gestion de classe.";
                break;
            default:
                $basePrompt .= "\n\nL'utilisateur est un VISITEUR. Fournis des informations générales.";
        }

        return $basePrompt;
    }

    /**
     * Call AI API (OpenAI or Anthropic)
     */
    protected function callAI(string $systemPrompt, string $userMessage, array $history = []): string
    {
        if ($this->provider === 'anthropic') {
            return $this->callAnthropic($systemPrompt, $userMessage, $history);
        }

        return $this->callOpenAI($systemPrompt, $userMessage, $history);
    }

    /**
     * Call OpenAI API
     */
    protected function callOpenAI(string $systemPrompt, string $userMessage, array $history): string
    {
        $messages = [
            ['role' => 'system', 'content' => $systemPrompt]
        ];

        // Add conversation history
        foreach ($history as $msg) {
            $messages[] = ['role' => $msg['role'], 'content' => $msg['content']];
        }

        $messages[] = ['role' => 'user', 'content' => $userMessage];

        $response = Http::withHeaders([
            'Authorization' => 'Bearer ' . $this->apiKey,
            'Content-Type' => 'application/json',
        ])->timeout(30)->post('https://api.openai.com/v1/chat/completions', [
            'model' => $this->model,
            'messages' => $messages,
            'max_tokens' => $this->maxTokens,
            'temperature' => $this->temperature,
        ]);

        if ($response->failed()) {
            throw new \Exception('OpenAI API Error: ' . $response->body());
        }

        return $response->json('choices.0.message.content');
    }

    /**
     * Call Anthropic (Claude) API
     */
    protected function callAnthropic(string $systemPrompt, string $userMessage, array $history): string
    {
        $messages = [];

        // Add conversation history
        foreach ($history as $msg) {
            $messages[] = ['role' => $msg['role'], 'content' => $msg['content']];
        }

        $messages[] = ['role' => 'user', 'content' => $userMessage];

        $response = Http::withHeaders([
            'x-api-key' => $this->apiKey,
            'anthropic-version' => '2023-06-01',
            'Content-Type' => 'application/json',
        ])->timeout(30)->post('https://api.anthropic.com/v1/messages', [
            'model' => $this->model,
            'max_tokens' => $this->maxTokens,
            'system' => $systemPrompt,
            'messages' => $messages,
        ]);

        if ($response->failed()) {
            throw new \Exception('Anthropic API Error: ' . $response->body());
        }

        return $response->json('content.0.text');
    }

    /**
     * Get conversation history for user
     */
    protected function getConversationHistory(int $userId, int $limit = 5): array
    {
        $logs = DB::table('chatbot_logs')
            ->where('user_id', $userId)
            ->orderBy('created_at', 'desc')
            ->limit($limit)
            ->get()
            ->reverse();

        $history = [];
        foreach ($logs as $log) {
            $history[] = ['role' => 'user', 'content' => $log->message];
            $history[] = ['role' => 'assistant', 'content' => $log->response];
        }

        return $history;
    }

    /**
     * Log conversation to database
     */
    protected function logConversation(?int $userId, string $message, string $response, string $role): void
    {
        DB::table('chatbot_logs')->insert([
            'user_id' => $userId,
            'message' => $message,
            'response' => $response,
            'user_role' => $role,
            'provider' => $this->provider,
            'model' => $this->model,
            'created_at' => now(),
            'updated_at' => now(),
        ]);
    }

    /**
     * Update analytics
     */
    protected function updateAnalytics(string $role): void
    {
        $date = now()->toDateString();

        DB::table('chatbot_analytics')
            ->updateOrInsert(
                ['date' => $date, 'user_role' => $role],
                [
                    'conversations' => DB::raw('conversations + 1'),
                    'updated_at' => now()
                ]
            );
    }

    /**
     * Get general school context as fallback
     */
    protected function getGeneralSchoolContext(): string
    {
        $schoolName = setting('application_name') ?? 'IAFactory School';
        $phone = setting('phone') ?? '';
        $email = setting('email') ?? '';

        return <<<CONTEXT
Informations générales:
- École: {$schoolName}
- Contact: {$phone}
- Email: {$email}
- Horaires: 8h00 - 17h00 (Dimanche - Jeudi)

Pour toute question spécifique, veuillez contacter le secrétariat.
CONTEXT;
    }

    /**
     * Fallback response when AI fails
     */
    protected function getFallbackResponse(string $message): string
    {
        $fallbacks = [
            'notes' => "Pour consulter les notes, connectez-vous et allez dans 'Mon Bulletin' ou 'Mes Notes'.",
            'frais' => "Pour les frais de scolarité, consultez la section 'Frais' ou contactez le secrétariat.",
            'absence' => "Pour justifier une absence, contactez l'administration avec un justificatif.",
            'emploi' => "L'emploi du temps est disponible dans votre espace personnel après connexion.",
            'inscription' => "Pour l'inscription, rendez-vous sur la page 'Admission en ligne' ou contactez le secrétariat.",
        ];

        $message = mb_strtolower($message);
        foreach ($fallbacks as $keyword => $response) {
            if (str_contains($message, $keyword)) {
                return $response;
            }
        }

        return "Je suis désolé, je n'ai pas pu traiter votre demande. Veuillez contacter le secrétariat pour plus d'informations ou reformulez votre question.";
    }

    /**
     * Seed knowledge base with initial data
     */
    public static function seedKnowledgeBase(): void
    {
        $entries = [
            [
                'category' => 'notes',
                'question' => 'Comment voir les notes de mon enfant ?',
                'answer' => "Connectez-vous avec votre compte parent, puis allez dans 'Mes Enfants' > 'Bulletin'. Vous verrez toutes les notes par matière et par trimestre.",
                'keywords' => 'notes,bulletin,résultats,moyenne',
                'priority' => 10,
            ],
            [
                'category' => 'frais',
                'question' => 'Comment payer les frais de scolarité ?',
                'answer' => "Vous pouvez payer: 1) En ligne via CIB/EDAHABIA dans 'Frais > Payer', 2) Par virement bancaire, 3) En espèces au secrétariat. Les reçus sont disponibles dans votre espace.",
                'keywords' => 'frais,paiement,scolarité,cib,edahabia',
                'priority' => 10,
            ],
            [
                'category' => 'absence',
                'question' => 'Comment justifier une absence ?',
                'answer' => "Envoyez le justificatif (certificat médical, etc.) via 'Mes Enfants' > 'Absences' > 'Justifier', ou déposez-le au secrétariat dans les 48h.",
                'keywords' => 'absence,justificatif,présence,retard',
                'priority' => 9,
            ],
            [
                'category' => 'emploi_temps',
                'question' => "Où trouver l'emploi du temps ?",
                'answer' => "L'emploi du temps est dans 'Académique' > 'Emploi du temps'. Il est mis à jour en cas de changement.",
                'keywords' => 'emploi,temps,horaires,planning',
                'priority' => 8,
            ],
            [
                'category' => 'inscription',
                'question' => 'Comment inscrire mon enfant ?',
                'answer' => "1) Remplissez le formulaire sur 'Admission en ligne', 2) Téléversez les documents requis, 3) Payez les frais d'inscription, 4) Attendez la confirmation par email.",
                'keywords' => 'inscription,admission,nouveau,élève',
                'priority' => 10,
            ],
            [
                'category' => 'contact',
                'question' => 'Comment contacter un enseignant ?',
                'answer' => "Utilisez la messagerie intégrée: 'Messages' > 'Nouveau message' > Sélectionnez l'enseignant. Vous pouvez aussi demander un rendez-vous via l'application.",
                'keywords' => 'contact,enseignant,professeur,message',
                'priority' => 7,
            ],
            [
                'category' => 'mot_passe',
                'question' => "J'ai oublié mon mot de passe",
                'answer' => "Cliquez sur 'Mot de passe oublié' sur la page de connexion, entrez votre email, et suivez le lien de réinitialisation envoyé.",
                'keywords' => 'mot,passe,oublié,connexion,login',
                'priority' => 10,
            ],
            [
                'category' => 'devoirs',
                'question' => 'Comment voir les devoirs ?',
                'answer' => "Les devoirs sont dans 'Académique' > 'Devoirs'. Vous verrez les devoirs par matière avec les dates de rendu et les fichiers joints.",
                'keywords' => 'devoirs,travail,maison,exercices',
                'priority' => 8,
            ],
        ];

        foreach ($entries as $entry) {
            DB::table('bbc_knowledge_base')->updateOrInsert(
                ['question' => $entry['question']],
                array_merge($entry, ['created_at' => now(), 'updated_at' => now()])
            );
        }
    }
}
