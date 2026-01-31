<?php

return [
    'name' => 'AIAssistant',

    /*
    |--------------------------------------------------------------------------
    | AI Provider Configuration
    |--------------------------------------------------------------------------
    | Supported: "openai", "anthropic"
    */
    'provider' => env('AI_PROVIDER', 'openai'),

    /*
    |--------------------------------------------------------------------------
    | API Keys
    |--------------------------------------------------------------------------
    */
    'api_key' => env('AI_API_KEY', env('OPENAI_API_KEY')),

    /*
    |--------------------------------------------------------------------------
    | Model Configuration
    |--------------------------------------------------------------------------
    | OpenAI: gpt-4o-mini, gpt-4o, gpt-4-turbo
    | Anthropic: claude-3-haiku-20240307, claude-3-sonnet-20240229, claude-3-opus-20240229
    */
    'model' => env('AI_MODEL', 'gpt-4o-mini'),

    /*
    |--------------------------------------------------------------------------
    | Generation Parameters
    |--------------------------------------------------------------------------
    */
    'max_tokens' => env('AI_MAX_TOKENS', 1000),
    'temperature' => env('AI_TEMPERATURE', 0.7),

    /*
    |--------------------------------------------------------------------------
    | Rate Limiting
    |--------------------------------------------------------------------------
    */
    'rate_limit' => [
        'guest' => 10,      // requests per hour for guests
        'user' => 50,       // requests per hour for logged-in users
        'premium' => 200,   // requests per hour for premium users
    ],

    /*
    |--------------------------------------------------------------------------
    | Enable/Disable Features
    |--------------------------------------------------------------------------
    */
    'enabled' => env('AI_ASSISTANT_ENABLED', true),
    'log_conversations' => env('AI_LOG_CONVERSATIONS', true),
    'enable_rag' => env('AI_ENABLE_RAG', true),
];
