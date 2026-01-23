<?php

/**
 * Routes de Fallback pour LiveChat
 * BBC School Algeria - Temporary Routes
 */

use App\Http\Controllers\LiveChatFallbackController;
use Illuminate\Support\Facades\Route;

// Routes administrateur LiveChat
Route::middleware(['web', 'auth', 'AdminPanel'])->prefix('admin')->name('admin.')->group(function () {
    Route::get('/live-chat', [LiveChatFallbackController::class, 'liveChat'])->name('live_chat');
    Route::get('/conversation-list', [LiveChatFallbackController::class, 'conversationList'])->name('livechat.conversation_list');
});

// Routes instructeur LiveChat
Route::middleware(['web', 'auth'])->prefix('instructor')->name('instructor.')->group(function () {
    Route::get('/live-chat', [LiveChatFallbackController::class, 'liveChat'])->name('live_chat');
});

// Routes étudiant LiveChat
Route::middleware(['web', 'auth'])->prefix('student')->name('student.')->group(function () {
    Route::get('/live-chat', [LiveChatFallbackController::class, 'liveChat'])->name('live_chat');
});

// Routes parent/tuteur LiveChat
Route::middleware(['web', 'auth'])->prefix('guardian')->name('guardian.')->group(function () {
    Route::get('/live-chat', [LiveChatFallbackController::class, 'liveChat'])->name('live_chat');
});
