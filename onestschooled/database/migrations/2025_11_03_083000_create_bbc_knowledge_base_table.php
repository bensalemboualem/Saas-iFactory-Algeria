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
        Schema::create('bbc_knowledge_base', function (Blueprint $table) {
            $table->id();
            $table->string('category', 100); // 'faq', 'guide', 'procedure', 'help'
            $table->string('user_type', 50); // 'student', 'parent', 'teacher', 'admin', 'all'
            $table->string('title', 255);
            $table->text('question');
            $table->longText('answer');
            $table->json('keywords')->nullable(); // Mots-clés pour la recherche
            $table->string('language', 10)->default('fr'); // 'fr', 'ar', 'en'
            $table->integer('priority')->default(0); // 0 = faible, 5 = très important
            $table->boolean('is_active')->default(true);
            $table->integer('view_count')->default(0);
            $table->integer('helpful_count')->default(0);
            $table->json('tags')->nullable(); // Tags pour catégorisation
            $table->timestamps();
            
            // Index pour optimiser la recherche
            $table->index(['category', 'user_type']);
            $table->index(['is_active', 'priority']);
            $table->fullText(['title', 'question', 'answer']); // Recherche full-text
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('bbc_knowledge_base');
    }
};