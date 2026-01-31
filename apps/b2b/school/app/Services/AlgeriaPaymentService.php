<?php

namespace App\Services;

use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

/**
 * Service de paiement pour l'Algérie
 *
 * Supporte:
 * - CIB (Carte Interbancaire)
 * - EDAHABIA (Algérie Poste)
 * - Virement bancaire
 * - Espèces (suivi)
 */
class AlgeriaPaymentService
{
    protected $satimUrl;
    protected $merchantId;
    protected $secretKey;
    protected $currency = 'DZD';

    public function __construct()
    {
        $this->satimUrl = config('services.satim.url', 'https://cib.satim.dz');
        $this->merchantId = config('services.satim.merchant_id');
        $this->secretKey = config('services.satim.secret_key');
    }

    /**
     * Initier un paiement CIB/EDAHABIA via SATIM
     */
    public function initiatePayment(array $data): array
    {
        try {
            $amount = $data['amount']; // en centimes
            $orderId = $data['order_id'];
            $description = $data['description'] ?? 'Frais de scolarité';
            $returnUrl = $data['return_url'] ?? route('payment.callback');
            $cancelUrl = $data['cancel_url'] ?? route('payment.cancel');

            // Générer la signature
            $signature = $this->generateSignature([
                'merchant_id' => $this->merchantId,
                'order_id' => $orderId,
                'amount' => $amount,
                'currency' => $this->currency,
            ]);

            // Préparer la requête SATIM
            $payload = [
                'merchant_id' => $this->merchantId,
                'order_id' => $orderId,
                'amount' => $amount,
                'currency' => $this->currency,
                'description' => $description,
                'language' => app()->getLocale() == 'ar' ? 'AR' : 'FR',
                'return_url' => $returnUrl,
                'cancel_url' => $cancelUrl,
                'signature' => $signature,
            ];

            // En mode production, envoyer à SATIM
            if (config('services.satim.mode') === 'production') {
                $response = Http::post($this->satimUrl . '/api/payment/init', $payload);

                if ($response->successful()) {
                    return [
                        'success' => true,
                        'payment_url' => $response->json('payment_url'),
                        'transaction_id' => $response->json('transaction_id'),
                    ];
                }

                throw new \Exception($response->json('message') ?? 'Erreur de paiement');
            }

            // Mode sandbox/test
            return [
                'success' => true,
                'payment_url' => route('payment.sandbox', ['order_id' => $orderId]),
                'transaction_id' => 'TEST-' . time(),
                'sandbox' => true,
            ];

        } catch (\Exception $e) {
            Log::error('AlgeriaPayment Error: ' . $e->getMessage());
            return [
                'success' => false,
                'error' => $e->getMessage(),
            ];
        }
    }

    /**
     * Vérifier le statut d'un paiement
     */
    public function verifyPayment(string $transactionId): array
    {
        try {
            if (config('services.satim.mode') !== 'production') {
                // Mode test
                return [
                    'success' => true,
                    'status' => 'completed',
                    'amount' => 10000,
                    'transaction_id' => $transactionId,
                ];
            }

            $signature = $this->generateSignature([
                'merchant_id' => $this->merchantId,
                'transaction_id' => $transactionId,
            ]);

            $response = Http::post($this->satimUrl . '/api/payment/verify', [
                'merchant_id' => $this->merchantId,
                'transaction_id' => $transactionId,
                'signature' => $signature,
            ]);

            if ($response->successful()) {
                return [
                    'success' => true,
                    'status' => $response->json('status'),
                    'amount' => $response->json('amount'),
                    'transaction_id' => $transactionId,
                    'approval_code' => $response->json('approval_code'),
                ];
            }

            return [
                'success' => false,
                'status' => 'failed',
                'error' => $response->json('message'),
            ];

        } catch (\Exception $e) {
            Log::error('AlgeriaPayment Verify Error: ' . $e->getMessage());
            return [
                'success' => false,
                'status' => 'error',
                'error' => $e->getMessage(),
            ];
        }
    }

    /**
     * Traiter le callback de paiement
     */
    public function handleCallback(array $data): array
    {
        // Vérifier la signature du callback
        if (!$this->verifyCallbackSignature($data)) {
            return [
                'success' => false,
                'error' => 'Invalid signature',
            ];
        }

        $status = $data['status'] ?? 'unknown';
        $transactionId = $data['transaction_id'] ?? null;
        $orderId = $data['order_id'] ?? null;

        if ($status === 'success' || $status === 'approved') {
            // Mettre à jour le paiement dans la base de données
            $this->updatePaymentStatus($orderId, 'completed', $transactionId);

            return [
                'success' => true,
                'status' => 'completed',
                'order_id' => $orderId,
                'transaction_id' => $transactionId,
            ];
        }

        $this->updatePaymentStatus($orderId, 'failed', $transactionId);

        return [
            'success' => false,
            'status' => 'failed',
            'order_id' => $orderId,
            'error' => $data['error_message'] ?? 'Payment failed',
        ];
    }

    /**
     * Générer la signature HMAC
     */
    protected function generateSignature(array $data): string
    {
        ksort($data);
        $signatureString = implode('|', $data);
        return hash_hmac('sha256', $signatureString, $this->secretKey);
    }

    /**
     * Vérifier la signature du callback
     */
    protected function verifyCallbackSignature(array $data): bool
    {
        $receivedSignature = $data['signature'] ?? '';
        unset($data['signature']);

        $expectedSignature = $this->generateSignature($data);

        return hash_equals($expectedSignature, $receivedSignature);
    }

    /**
     * Mettre à jour le statut du paiement
     */
    protected function updatePaymentStatus(string $orderId, string $status, ?string $transactionId): void
    {
        \DB::table('fees_collects')
            ->where('order_id', $orderId)
            ->update([
                'payment_status' => $status,
                'transaction_id' => $transactionId,
                'paid_at' => $status === 'completed' ? now() : null,
                'updated_at' => now(),
            ]);
    }

    /**
     * Formater un montant en DZD
     */
    public static function formatAmount(float $amount): string
    {
        return number_format($amount, 2, ',', ' ') . ' DA';
    }

    /**
     * Convertir en centimes pour SATIM
     */
    public static function toCentimes(float $amount): int
    {
        return (int) ($amount * 100);
    }

    /**
     * Obtenir les méthodes de paiement disponibles
     */
    public static function getAvailableMethods(): array
    {
        return [
            'cib' => [
                'name' => 'Carte CIB',
                'name_ar' => 'بطاقة بين البنوك',
                'description' => 'Paiement par carte interbancaire',
                'icon' => 'cib-card.png',
                'enabled' => config('services.satim.cib_enabled', true),
            ],
            'edahabia' => [
                'name' => 'EDAHABIA',
                'name_ar' => 'الذهبية',
                'description' => 'Carte Algérie Poste',
                'icon' => 'edahabia-card.png',
                'enabled' => config('services.satim.edahabia_enabled', true),
            ],
            'virement' => [
                'name' => 'Virement Bancaire',
                'name_ar' => 'تحويل بنكي',
                'description' => 'Virement sur compte bancaire de l\'école',
                'icon' => 'bank-transfer.png',
                'enabled' => true,
            ],
            'especes' => [
                'name' => 'Espèces',
                'name_ar' => 'نقدا',
                'description' => 'Paiement au secrétariat',
                'icon' => 'cash.png',
                'enabled' => true,
            ],
        ];
    }
}
