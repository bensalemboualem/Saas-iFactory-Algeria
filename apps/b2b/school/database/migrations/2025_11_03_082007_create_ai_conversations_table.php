<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('ai_conversations', function (Blueprint $table) {
            $table->id();
            $table->bigInteger('user_id')->nullable()->index();
            $table->string('user_type', 50)->default('visitor');
            $table->text('message');
            $table->text('response')->nullable();
            $table->string('platform', 50)->default('OnestSchool');
            $table->string('session_id', 100)->nullable();
            $table->string('ip_address', 45)->nullable();
            $table->text('user_agent')->nullable();
            $table->json('metadata')->nullable(); // Pour stocker des données contextuelles
            $table->boolean('is_resolved')->default(false);
            $table->integer('rating')->nullable(); // Note de satisfaction 1-5
            $table->text('feedback')->nullable();
            $table->timestamps();
            
            // Index pour optimiser les requêtes
            $table->index(['user_id', 'created_at']);
            $table->index(['user_type', 'created_at']);
            $table->index(['platform', 'created_at']);
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('ai_conversations');
    }
};
