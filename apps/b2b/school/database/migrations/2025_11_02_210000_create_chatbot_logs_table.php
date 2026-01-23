<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('chatbot_logs', function (Blueprint $table) {
            $table->id();
            $table->unsignedBigInteger('user_id')->nullable();
            $table->enum('user_type', ['employee', 'parent', 'student', 'guest'])->default('guest');
            $table->text('user_message');
            $table->text('bot_response');
            $table->string('session_id')->nullable();
            $table->string('channel')->default('web'); // web, whatsapp, telegram, etc.
            $table->json('metadata')->nullable(); // Additional data
            $table->timestamps();
            
            $table->index(['user_id', 'created_at']);
            $table->index(['user_type', 'created_at']);
            $table->index('session_id');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('chatbot_logs');
    }
};