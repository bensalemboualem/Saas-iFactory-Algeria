<?php

use Illuminate\Support\Facades\Route;
use Modules\AIAssistant\Http\Controllers\ChatbotController;

/*
|--------------------------------------------------------------------------
| AI Assistant API Routes
|--------------------------------------------------------------------------
*/

Route::prefix('ai')->group(function () {
    // Public chat endpoint (with rate limiting)
    Route::post('/chat', [ChatbotController::class, 'chat'])->name('ai.chat');

    // Authenticated routes
    Route::middleware('auth:sanctum')->group(function () {
        Route::get('/history', [ChatbotController::class, 'history'])->name('ai.history');
    });

    // Admin routes
    Route::middleware(['auth:sanctum'])->prefix('admin')->group(function () {
        Route::get('/analytics', [ChatbotController::class, 'analytics'])->name('ai.analytics');
        Route::post('/seed-knowledge', [ChatbotController::class, 'seedKnowledge'])->name('ai.seed');
        Route::post('/knowledge', [ChatbotController::class, 'addKnowledge'])->name('ai.add-knowledge');
    });
});
