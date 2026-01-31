<?php

namespace Modules\AIAssistant\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;
use Illuminate\Support\Facades\RateLimiter;
use Modules\AIAssistant\Services\AIService;

class ChatbotController extends Controller
{
    protected AIService $aiService;

    public function __construct(AIService $aiService)
    {
        $this->aiService = $aiService;
    }

    /**
     * Handle chat request
     */
    public function chat(Request $request): JsonResponse
    {
        $request->validate([
            'message' => 'required|string|max:1000',
        ]);

        // Check if AI is enabled
        if (!config('aiassistant.enabled', true)) {
            return response()->json([
                'success' => false,
                'message' => 'Le service d\'assistant IA est temporairement indisponible.'
            ], 503);
        }

        // Rate limiting
        $key = $this->getRateLimitKey($request);
        $limit = $this->getRateLimit($request);

        if (RateLimiter::tooManyAttempts($key, $limit)) {
            $seconds = RateLimiter::availableIn($key);
            return response()->json([
                'success' => false,
                'message' => "Trop de requêtes. Réessayez dans {$seconds} secondes."
            ], 429);
        }

        RateLimiter::hit($key, 3600); // 1 hour window

        // Get user info
        $userId = auth()->id();
        $role = $this->getUserRole();

        // Call AI service
        $result = $this->aiService->chat(
            $request->input('message'),
            $userId,
            $role
        );

        return response()->json($result);
    }

    /**
     * Get chat history for current user
     */
    public function history(Request $request): JsonResponse
    {
        if (!auth()->check()) {
            return response()->json([
                'success' => false,
                'message' => 'Authentification requise.'
            ], 401);
        }

        $history = \DB::table('chatbot_logs')
            ->where('user_id', auth()->id())
            ->orderBy('created_at', 'desc')
            ->limit($request->input('limit', 20))
            ->get(['message', 'response', 'created_at']);

        return response()->json([
            'success' => true,
            'history' => $history
        ]);
    }

    /**
     * Get chatbot analytics (admin only)
     */
    public function analytics(Request $request): JsonResponse
    {
        if (!auth()->check() || !hasPermission('chatbot_analytics')) {
            return response()->json([
                'success' => false,
                'message' => 'Accès non autorisé.'
            ], 403);
        }

        $startDate = $request->input('start_date', now()->subDays(30)->toDateString());
        $endDate = $request->input('end_date', now()->toDateString());

        $analytics = \DB::table('chatbot_analytics')
            ->whereBetween('date', [$startDate, $endDate])
            ->orderBy('date', 'asc')
            ->get();

        $totalConversations = $analytics->sum('conversations');
        $byRole = $analytics->groupBy('user_role')->map->sum('conversations');

        return response()->json([
            'success' => true,
            'total_conversations' => $totalConversations,
            'by_role' => $byRole,
            'daily' => $analytics
        ]);
    }

    /**
     * Seed knowledge base (admin only)
     */
    public function seedKnowledge(Request $request): JsonResponse
    {
        if (!auth()->check() || !isSuperAdmin()) {
            return response()->json([
                'success' => false,
                'message' => 'Accès non autorisé.'
            ], 403);
        }

        AIService::seedKnowledgeBase();

        return response()->json([
            'success' => true,
            'message' => 'Base de connaissances initialisée avec succès.'
        ]);
    }

    /**
     * Add knowledge entry (admin only)
     */
    public function addKnowledge(Request $request): JsonResponse
    {
        if (!auth()->check() || !hasPermission('chatbot_manage')) {
            return response()->json([
                'success' => false,
                'message' => 'Accès non autorisé.'
            ], 403);
        }

        $request->validate([
            'category' => 'required|string|max:50',
            'question' => 'required|string|max:500',
            'answer' => 'required|string|max:2000',
            'keywords' => 'nullable|string|max:255',
            'priority' => 'nullable|integer|min:1|max:10',
        ]);

        \DB::table('bbc_knowledge_base')->insert([
            'category' => $request->input('category'),
            'question' => $request->input('question'),
            'answer' => $request->input('answer'),
            'keywords' => $request->input('keywords', ''),
            'priority' => $request->input('priority', 5),
            'created_at' => now(),
            'updated_at' => now(),
        ]);

        return response()->json([
            'success' => true,
            'message' => 'Entrée ajoutée à la base de connaissances.'
        ]);
    }

    /**
     * Get rate limit key
     */
    protected function getRateLimitKey(Request $request): string
    {
        if (auth()->check()) {
            return 'chatbot:user:' . auth()->id();
        }
        return 'chatbot:ip:' . $request->ip();
    }

    /**
     * Get rate limit based on user type
     */
    protected function getRateLimit(Request $request): int
    {
        $limits = config('aiassistant.rate_limit');

        if (!auth()->check()) {
            return $limits['guest'] ?? 10;
        }

        // Check if premium user (you can customize this logic)
        $user = auth()->user();
        if ($user->is_premium ?? false) {
            return $limits['premium'] ?? 200;
        }

        return $limits['user'] ?? 50;
    }

    /**
     * Get user role for context
     */
    protected function getUserRole(): string
    {
        if (!auth()->check()) {
            return 'guest';
        }

        $user = auth()->user();

        if ($user->role_id == 6) return 'student';
        if ($user->role_id == 7) return 'parent';
        if ($user->role_id == 5) return 'teacher';
        if (in_array($user->role_id, [1, 2])) return 'admin';

        return 'user';
    }
}
