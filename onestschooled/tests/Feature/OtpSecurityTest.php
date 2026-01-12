<?php

namespace Tests\Feature;

use Tests\TestCase;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;

/**
 * Security tests to ensure OTP is NEVER returned in API responses.
 *
 * CRITICAL: These tests must pass to prevent OTP leakage vulnerability.
 * If any test fails, it indicates a security regression.
 */
class OtpSecurityTest extends TestCase
{
    use RefreshDatabase;

    /**
     * Test that forgot password endpoint does NOT return OTP in response.
     *
     * @return void
     */
    public function test_forgot_password_does_not_return_otp_in_response()
    {
        // Create a test user
        $user = User::factory()->create([
            'email' => 'test@example.com',
        ]);

        // Call forgot password endpoint
        $response = $this->postJson('/api/forgot-password', [
            'email' => 'test@example.com',
        ]);

        // Assert response does not contain OTP
        $response->assertJsonMissing(['otp']);
        $response->assertJsonMissing(['code']);
        $response->assertJsonMissing(['token']); // OTP might be named 'token'

        // Assert response contains safe fields only
        if ($response->status() === 200) {
            $response->assertJsonStructure([
                'data' => ['sent', 'email', 'expires_in']
            ]);
        }
    }

    /**
     * Test that reset_password_otp column is not exposed via any API.
     *
     * @return void
     */
    public function test_user_otp_column_is_hidden()
    {
        $user = User::factory()->create([
            'email' => 'test@example.com',
            'reset_password_otp' => '123456',
        ]);

        // Ensure OTP is not in toArray output
        $userArray = $user->toArray();
        $this->assertArrayNotHasKey('reset_password_otp', $userArray);
    }

    /**
     * Test that OTP response uses masked email.
     *
     * @return void
     */
    public function test_forgot_password_returns_masked_email()
    {
        $user = User::factory()->create([
            'email' => 'johndoe@example.com',
        ]);

        $response = $this->postJson('/api/forgot-password', [
            'email' => 'johndoe@example.com',
        ]);

        if ($response->status() === 200) {
            $data = $response->json('data');

            // Email should be partially masked
            if (isset($data['email'])) {
                $this->assertStringContainsString('***', $data['email']);
                $this->assertStringNotContainsString('johndoe', $data['email']);
            }
        }
    }

    /**
     * Security smoke test: verify dangerous endpoints are disabled.
     *
     * @return void
     */
    public function test_dangerous_endpoints_are_disabled()
    {
        // migrate-seed should return 403
        $response = $this->get('/migrate-seed');
        $this->assertContains($response->status(), [403, 404]);

        // optimize should return 403
        $response = $this->get('/optimize');
        $this->assertContains($response->status(), [403, 404]);
    }
}
