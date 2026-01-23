<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Http\Response;

/**
 * Contrôleur de Fallback pour LiveChat
 * BBC School Algeria - Temporary Solution
 */
class LiveChatFallbackController extends Controller
{
    /**
     * Affichage temporaire pour les conversations
     */
    public function conversationList()
    {
        return response()->view('livechat.temporary-disabled', [
            'title' => 'Live Chat Conversations',
            'message' => 'This feature is temporarily unavailable. The LiveChat module is being updated.',
            'return_url' => route('dashboard')
        ]);
    }
    
    /**
     * Page principale LiveChat
     */
    public function liveChat()
    {
        return response()->view('livechat.temporary-disabled', [
            'title' => 'Live Chat',
            'message' => 'LiveChat functionality is being updated. Please check back later.',
            'return_url' => route('dashboard')
        ]);
    }
}
