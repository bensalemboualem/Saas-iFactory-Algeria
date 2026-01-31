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
        // Chatbot conversation logs
        if (!Schema::hasTable('chatbot_logs')) {
            Schema::create('chatbot_logs', function (Blueprint $table) {
                $table->id();
                $table->unsignedBigInteger('user_id')->nullable();
                $table->text('message');
                $table->text('response');
                $table->string('user_role', 20)->default('guest');
                $table->string('provider', 20)->default('openai');
                $table->string('model', 50)->nullable();
                $table->integer('tokens_used')->nullable();
                $table->decimal('cost', 10, 6)->nullable();
                $table->timestamps();

                $table->index('user_id');
                $table->index('created_at');
                $table->index('user_role');
            });
        }

        // Chatbot analytics
        if (!Schema::hasTable('chatbot_analytics')) {
            Schema::create('chatbot_analytics', function (Blueprint $table) {
                $table->id();
                $table->date('date');
                $table->string('user_role', 20)->default('guest');
                $table->integer('conversations')->default(0);
                $table->integer('tokens_total')->default(0);
                $table->decimal('cost_total', 10, 4)->default(0);
                $table->timestamps();

                $table->unique(['date', 'user_role']);
                $table->index('date');
            });
        }

        // Knowledge base for RAG
        if (!Schema::hasTable('bbc_knowledge_base')) {
            Schema::create('bbc_knowledge_base', function (Blueprint $table) {
                $table->id();
                $table->string('category', 50);
                $table->string('question', 500);
                $table->text('answer');
                $table->string('keywords', 255)->nullable();
                $table->integer('priority')->default(5);
                $table->string('language', 5)->default('fr');
                $table->boolean('is_active')->default(true);
                $table->timestamps();

                $table->index('category');
                $table->index('priority');
                $table->index('is_active');
                $table->fullText(['question', 'answer', 'keywords']);
            });
        }
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('chatbot_logs');
        Schema::dropIfExists('chatbot_analytics');
        Schema::dropIfExists('bbc_knowledge_base');
    }
};
