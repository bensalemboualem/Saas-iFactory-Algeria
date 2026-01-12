import express, { Request, Response } from 'express';
import cors from 'cors';
import { initializeApp, FirebaseApp } from 'firebase/app';
import { getFirestore, doc, getDoc, updateDoc, setDoc, Firestore } from 'firebase/firestore';
import dotenv from 'dotenv';

dotenv.config();

// --- CONFIGURATION ---
const PORT = process.env.PORT || 3001;

const firebaseConfig = {
    apiKey: process.env.FIREBASE_API_KEY,
    authDomain: process.env.FIREBASE_AUTH_DOMAIN,
    projectId: process.env.FIREBASE_PROJECT_ID,
    storageBucket: process.env.FIREBASE_STORAGE_BUCKET,
    messagingSenderId: process.env.FIREBASE_MESSAGING_SENDER_ID,
    appId: process.env.FIREBASE_APP_ID
};

let app: FirebaseApp;
let db: Firestore;

try {
    app = initializeApp(firebaseConfig);
    db = getFirestore(app);
    console.log('Firebase initialized successfully');
} catch (e) {
    console.error('Firebase initialization error:', e);
    process.exit(1);
}

const USER_KEYS_COLLECTION = 'user_keys';

// --- TYPES ---
type KeyStatus = 'NEW' | 'ACTIVE' | 'DEPLETED' | 'EXPIRED' | 'UNKNOWN';

interface KeyValidationResponse {
    valid: boolean;
    provider: string;
    status: KeyStatus;
    balance_usd: number;
    current_usage: number;
    remaining_balance: number;
    error?: string;
    user_id?: string;
}

interface KeyCreateRequest {
    key_code?: string;
    provider: string;
    balance_usd: number;
    expires_days?: number;
}

interface KeyDebitRequest {
    key_code: string;
    amount_usd: number;
    description?: string;
}

interface TokenDebitRequest {
    user_id?: string;
    key_code?: string;
    provider: string;
    model: string;
    input_tokens: number;
    output_tokens: number;
    description?: string;
}

// --- PRICING TABLE (Coûts par million de tokens) ---
const COST_PER_1M_TOKENS: Record<string, Record<string, { input: number; output: number }>> = {
    Groq: {
        'llama-3.3-70b-versatile': { input: 0.59, output: 0.79 },
        'llama-3.1-8b-instant': { input: 0.05, output: 0.08 },
        'mixtral-8x7b-32768': { input: 0.24, output: 0.24 },
        'whisper-large-v3': { input: 0.111, output: 0 },
        'whisper-large-v3-turbo': { input: 0.04, output: 0 }
    },
    OpenRouter: {
        'anthropic/claude-3.5-sonnet': { input: 3.0, output: 15.0 },
        'anthropic/claude-3.5-haiku': { input: 0.8, output: 4.0 },
        'google/gemini-2.0-flash': { input: 0.1, output: 0.4 },
        'google/gemini-1.5-pro': { input: 1.25, output: 5.0 },
        'meta-llama/llama-3.3-70b': { input: 0.4, output: 0.4 },
        'openai/gpt-4o': { input: 2.5, output: 10.0 }
    },
    OpenAI: {
        'gpt-4o': { input: 2.5, output: 10.0 },
        'gpt-4o-mini': { input: 0.15, output: 0.6 },
        'gpt-4-turbo': { input: 10.0, output: 30.0 },
        'tts-1': { input: 15.0, output: 0 },
        'tts-1-hd': { input: 30.0, output: 0 }
    },
    Anthropic: {
        'claude-3-5-sonnet-20241022': { input: 3.0, output: 15.0 },
        'claude-3-5-haiku-20241022': { input: 0.8, output: 4.0 },
        'claude-3-opus-20240229': { input: 15.0, output: 75.0 }
    }
};

// Marge commerciale (30% comme défini dans les CGV)
const MARGIN = 1.3;

/**
 * Calcule le coût d'une requête LLM basé sur les tokens
 */
function calculateRequestCost(
    provider: string,
    model: string,
    inputTokens: number,
    outputTokens: number
): { cost_usd: number; breakdown: { input_cost: number; output_cost: number; margin: number } } {
    const providerCosts = COST_PER_1M_TOKENS[provider];

    // Chercher le modèle exact ou un modèle similaire
    let modelCosts = providerCosts?.[model];

    if (!modelCosts && providerCosts) {
        // Recherche partielle (ex: "llama-3.3-70b" match "llama-3.3-70b-versatile")
        for (const [key, costs] of Object.entries(providerCosts)) {
            if (model.includes(key) || key.includes(model)) {
                modelCosts = costs;
                break;
            }
        }
    }

    // Fallback: coût minimal par défaut
    if (!modelCosts) {
        console.warn(`[PRICING] Unknown model: ${provider}/${model}, using default pricing`);
        modelCosts = { input: 0.1, output: 0.3 };
    }

    const inputCost = (inputTokens / 1_000_000) * modelCosts.input;
    const outputCost = (outputTokens / 1_000_000) * modelCosts.output;
    const baseCost = inputCost + outputCost;
    const finalCost = baseCost * MARGIN;

    return {
        cost_usd: finalCost,
        breakdown: {
            input_cost: inputCost * MARGIN,
            output_cost: outputCost * MARGIN,
            margin: MARGIN
        }
    };
}

// --- HELPERS ---
function generateKeyCode(provider: string): string {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let randomPart = '';
    for (let i = 0; i < 8; i++) {
        randomPart += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return `${provider.toUpperCase()}-${randomPart}`;
}

// --- VALIDATION ENDPOINT ---
async function validateKey(keyCode: string, requestingUserId?: string): Promise<KeyValidationResponse> {
    if (!keyCode) {
        return {
            valid: false,
            provider: 'UNKNOWN',
            status: 'UNKNOWN',
            balance_usd: 0,
            current_usage: 0,
            remaining_balance: 0,
            error: 'Key code is required.'
        };
    }

    const keyDocRef = doc(db, USER_KEYS_COLLECTION, keyCode.toUpperCase());

    try {
        const docSnap = await getDoc(keyDocRef);

        if (!docSnap.exists()) {
            return {
                valid: false,
                provider: 'UNKNOWN',
                status: 'UNKNOWN',
                balance_usd: 0,
                current_usage: 0,
                remaining_balance: 0,
                error: 'Key code not found.'
            };
        }

        const data = docSnap.data();
        const balance = data.balance_usd || 0;
        const currentUsage = data.current_usage || 0;
        const remainingBalance = Math.max(0, balance - currentUsage);

        // Vérifier expiration
        if (data.expires_at && new Date(data.expires_at.toDate()) < new Date()) {
            await updateDoc(keyDocRef, { status: 'EXPIRED' });
            return {
                valid: false,
                provider: data.provider || 'Groq',
                status: 'EXPIRED',
                balance_usd: balance,
                current_usage: currentUsage,
                remaining_balance: remainingBalance,
                error: 'This key has expired.'
            };
        }

        // Vérifier statut DEPLETED
        if (data.status === 'DEPLETED' || remainingBalance <= 0) {
            return {
                valid: false,
                provider: data.provider || 'Groq',
                status: 'DEPLETED',
                balance_usd: balance,
                current_usage: currentUsage,
                remaining_balance: 0,
                error: 'This key has been fully consumed.'
            };
        }

        // Vérifier statut EXPIRED
        if (data.status === 'EXPIRED') {
            return {
                valid: false,
                provider: data.provider || 'Groq',
                status: 'EXPIRED',
                balance_usd: balance,
                current_usage: currentUsage,
                remaining_balance: remainingBalance,
                error: 'This key has expired.'
            };
        }

        // Vérifier attribution utilisateur
        if (data.user_id && requestingUserId && data.user_id !== requestingUserId) {
            return {
                valid: false,
                provider: data.provider || 'Groq',
                status: 'UNKNOWN',
                balance_usd: balance,
                current_usage: currentUsage,
                remaining_balance: remainingBalance,
                error: 'This key is already assigned to another user.'
            };
        }

        // Première activation
        if ((data.status === 'NEW' || !data.user_id) && requestingUserId) {
            await updateDoc(keyDocRef, {
                user_id: requestingUserId,
                status: 'ACTIVE',
                activated_at: new Date()
            });
            console.log(`Key ${keyCode} activated for user ${requestingUserId}`);
        }

        return {
            valid: true,
            provider: data.provider || 'Groq',
            status: 'ACTIVE',
            balance_usd: balance,
            current_usage: currentUsage,
            remaining_balance: remainingBalance,
            user_id: requestingUserId || data.user_id
        };

    } catch (error) {
        console.error('Error validating key:', error);
        return {
            valid: false,
            provider: 'UNKNOWN',
            status: 'UNKNOWN',
            balance_usd: 0,
            current_usage: 0,
            remaining_balance: 0,
            error: 'Server error during validation.'
        };
    }
}

// --- DEBIT ENDPOINT (Art. 4 CGV - Sécurisation du modèle économique) ---

/**
 * Débite le solde de la clé API (version simple par keyCode)
 */
async function debitKey(keyCode: string, amountUsd: number, description?: string): Promise<{
    success: boolean;
    new_balance: number;
    message: string;
    status?: string;
}> {
    return debitWallet(keyCode, undefined, amountUsd, description || 'API');
}

/**
 * Débite le solde de la clé API attribuée à l'utilisateur.
 * C'est l'opération qui sécurise le modèle économique (Art. 4 des CGV).
 * @param keyId L'ID de la clé que l'utilisateur utilise.
 * @param userId L'ID de l'utilisateur (pour la vérification de propriété). Optionnel si débit direct par keyCode.
 * @param costUsd Le montant à débiter.
 * @param keyProvider Le fournisseur utilisé (pour les logs, ex: 'Groq', 'Claude').
 * @returns Le nouveau solde et le statut de la clé.
 */
async function debitWallet(
    keyId: string,
    userId: string | undefined,
    costUsd: number,
    keyProvider: string
): Promise<{
    success: boolean;
    new_balance: number;
    message: string;
    status: 'ACTIVE' | 'DEPLETED' | 'ERROR';
}> {
    // NOTE: keyId doit être converti en majuscules (convention de la validation)
    const keyDocRef = doc(db, USER_KEYS_COLLECTION, keyId.toUpperCase());

    try {
        const docSnap = await getDoc(keyDocRef);

        // Vérification existence
        if (!docSnap.exists()) {
            return {
                success: false,
                new_balance: 0,
                message: 'Key not found.',
                status: 'ERROR'
            };
        }

        const data = docSnap.data();

        // Vérification propriété (si userId fourni)
        if (userId && data.user_id && data.user_id !== userId) {
            console.warn(`Tentative de débit échouée pour ${userId}. Clé ${keyId} appartient à un autre utilisateur.`);
            return {
                success: false,
                new_balance: 0,
                message: 'Key belongs to another user.',
                status: 'ERROR'
            };
        }

        // Vérification statut
        if (data.status !== 'ACTIVE') {
            console.warn(`Tentative de débit échouée. Clé ${keyId} status: ${data.status}`);
            return {
                success: false,
                new_balance: 0,
                message: `Key is ${data.status}.`,
                status: data.status as 'DEPLETED'
            };
        }

        const balance = data.balance_usd || 0;
        const currentUsage = data.current_usage || 0;
        const remainingBalance = balance - currentUsage;

        // --- LOGIQUE DE DÉBIT ET DE CLÔTURE DE CLÉ ---

        if (remainingBalance < costUsd) {
            // Solde insuffisant: on débite le reste et on marque comme DEPLETED
            const finalDebit = remainingBalance;

            await updateDoc(keyDocRef, {
                current_usage: currentUsage + finalDebit,
                status: 'DEPLETED',
                depleted_at: new Date(),
                last_provider: keyProvider
            });

            console.warn(`Clé ${keyId} épuisée. Dernier débit: $${finalDebit.toFixed(4)}`);

            return {
                success: false,
                new_balance: 0,
                message: `Insufficient balance. Key depleted. Final debit: $${finalDebit.toFixed(4)}`,
                status: 'DEPLETED'
            };

        } else {
            // Débit standard
            const newUsage = currentUsage + costUsd;
            const newBalance = balance - newUsage;

            const updateData: Record<string, any> = {
                current_usage: newUsage,
                last_used_at: new Date(),
                last_provider: keyProvider
            };

            // Marquer comme DEPLETED si solde atteint 0
            if (newBalance <= 0) {
                updateData.status = 'DEPLETED';
                updateData.depleted_at = new Date();
            }

            await updateDoc(keyDocRef, updateData);

            console.log(`[WALLET] Débit $${costUsd.toFixed(4)} (${keyProvider}) sur ${keyId}. Solde: $${newBalance.toFixed(4)}`);

            return {
                success: true,
                new_balance: newBalance,
                message: `Debited $${costUsd.toFixed(4)} for ${keyProvider}.`,
                status: newBalance <= 0 ? 'DEPLETED' : 'ACTIVE'
            };
        }

    } catch (error) {
        console.error("Erreur lors de l'opération de débit Firestore:", error);
        return {
            success: false,
            new_balance: 0,
            message: 'Server error during debit.',
            status: 'ERROR'
        };
    }
}

// --- CREATE KEY (ADMIN) ---
async function createKey(request: KeyCreateRequest): Promise<{
    success: boolean;
    key_code?: string;
    message: string;
}> {
    const keyCode = request.key_code || generateKeyCode(request.provider);
    const keyDocRef = doc(db, USER_KEYS_COLLECTION, keyCode);

    try {
        const expiresAt = request.expires_days
            ? new Date(Date.now() + request.expires_days * 24 * 60 * 60 * 1000)
            : null;

        await setDoc(keyDocRef, {
            key_code: keyCode,
            provider: request.provider,
            balance_usd: request.balance_usd,
            current_usage: 0,
            status: 'NEW',
            user_id: null,
            created_at: new Date(),
            expires_at: expiresAt
        });

        console.log(`Created key ${keyCode} with balance $${request.balance_usd}`);

        return {
            success: true,
            key_code: keyCode,
            message: `Key ${keyCode} created successfully.`
        };

    } catch (error) {
        console.error('Error creating key:', error);
        return { success: false, message: 'Server error during key creation.' };
    }
}

// --- EXPRESS SERVER ---
const server = express();
server.use(cors());
server.use(express.json());

// Health check
server.get('/health', (req: Request, res: Response) => {
    res.json({ status: 'ok', service: 'key-validation-service' });
});

// Validate key
server.post('/api/keys/validate', async (req: Request, res: Response) => {
    const { key_code, user_id } = req.body;
    const result = await validateKey(key_code, user_id);
    res.status(result.valid ? 200 : 401).json(result);
});

// Debit key
server.post('/api/keys/debit', async (req: Request, res: Response) => {
    const { key_code, amount_usd, description } = req.body as KeyDebitRequest;
    const result = await debitKey(key_code, amount_usd, description);
    res.status(result.success ? 200 : 400).json(result);
});

// Get balance
server.get('/api/keys/:key_code/balance', async (req: Request, res: Response) => {
    const result = await validateKey(req.params.key_code);
    if (!result.valid && result.error === 'Key code not found.') {
        res.status(404).json(result);
    } else {
        res.json({
            key_code: req.params.key_code.toUpperCase(),
            provider: result.provider,
            balance_usd: result.balance_usd,
            current_usage: result.current_usage,
            remaining_balance: result.remaining_balance,
            status: result.status
        });
    }
});

// Create key (Admin)
server.post('/api/keys/create', async (req: Request, res: Response) => {
    const result = await createKey(req.body as KeyCreateRequest);
    res.status(result.success ? 201 : 500).json(result);
});

// Pricing info (utilise la table COST_PER_1M_TOKENS centralisée)
server.get('/api/keys/pricing', (req: Request, res: Response) => {
    res.json({
        providers: COST_PER_1M_TOKENS,
        margin: MARGIN,
        currency: 'USD',
        unit: 'per_1M_tokens'
    });
});

// Calculer le coût d'une requête AVANT de l'effectuer
server.post('/api/pricing/calculate', (req: Request, res: Response) => {
    const { provider, model, input_tokens, output_tokens } = req.body;

    if (!provider || !model || input_tokens === undefined || output_tokens === undefined) {
        res.status(400).json({
            success: false,
            message: 'provider, model, input_tokens, and output_tokens are required'
        });
        return;
    }

    const { cost_usd, breakdown } = calculateRequestCost(provider, model, input_tokens, output_tokens);

    res.json({
        provider,
        model,
        tokens: { input: input_tokens, output: output_tokens },
        cost_usd,
        breakdown,
        note: `Cost includes ${((MARGIN - 1) * 100).toFixed(0)}% margin`
    });
});

// Get all keys for a user
server.get('/api/keys/user/:user_id', async (req: Request, res: Response) => {
    const userId = req.params.user_id;
    try {
        const keysRef = db.collection ? db.collection(USER_KEYS_COLLECTION) : null;
        if (!keysRef) {
            res.json([]);
            return;
        }
        // Note: Cette requête nécessite un index Firestore sur user_id
        const snapshot = await keysRef.where('user_id', '==', userId).get();
        const keys: any[] = [];
        snapshot.forEach((doc: any) => {
            const data = doc.data();
            keys.push({
                key_code: doc.id,
                provider: data.provider,
                balance_usd: data.balance_usd || 0,
                current_usage: data.current_usage || 0,
                remaining_balance: Math.max(0, (data.balance_usd || 0) - (data.current_usage || 0)),
                status: data.status,
                expires_at: data.expires_at?.toDate?.() || data.expires_at
            });
        });
        res.json(keys);
    } catch (error) {
        console.error('Error fetching user keys:', error);
        res.json([]);
    }
});

// Debit wallet by user (auto-find active key)
server.post('/api/wallet/debit', async (req: Request, res: Response) => {
    const { user_id, amount_usd, provider, model, description } = req.body;

    if (!user_id || !amount_usd || amount_usd <= 0) {
        res.status(400).json({
            success: false,
            message: 'user_id and positive amount_usd required'
        });
        return;
    }

    try {
        // Trouver la clé active de l'utilisateur pour ce provider
        const keysRef = db.collection ? db.collection(USER_KEYS_COLLECTION) : null;
        if (!keysRef) {
            res.status(503).json({ success: false, message: 'Database not available' });
            return;
        }

        const snapshot = await keysRef
            .where('user_id', '==', user_id)
            .where('status', '==', 'ACTIVE')
            .get();

        let targetKey: any = null;
        let maxBalance = 0;

        snapshot.forEach((doc: any) => {
            const data = doc.data();
            const remaining = (data.balance_usd || 0) - (data.current_usage || 0);
            // Filtrer par provider si spécifié
            if (provider && data.provider !== provider) return;
            if (remaining > maxBalance) {
                maxBalance = remaining;
                targetKey = { id: doc.id, ...data };
            }
        });

        if (!targetKey) {
            res.status(402).json({
                success: false,
                message: `No active key found for user ${user_id}`
            });
            return;
        }

        if (amount_usd > maxBalance) {
            res.status(402).json({
                success: false,
                new_balance: maxBalance,
                message: `Insufficient balance. Required: $${amount_usd.toFixed(4)}, Available: $${maxBalance.toFixed(4)}`
            });
            return;
        }

        // Débiter
        const result = await debitKey(targetKey.id, amount_usd, description || `${provider}/${model}`);
        res.status(result.success ? 200 : 400).json({
            ...result,
            key_code: targetKey.id
        });

    } catch (error) {
        console.error('Error debiting wallet:', error);
        res.status(500).json({ success: false, message: 'Server error' });
    }
});

// Debit wallet by tokens (CALCUL AUTOMATIQUE)
server.post('/api/wallet/debit-by-tokens', async (req: Request, res: Response) => {
    const { user_id, key_code, provider, model, input_tokens, output_tokens, description } = req.body as TokenDebitRequest;

    // Validation
    if (!provider || !model || input_tokens === undefined || output_tokens === undefined) {
        res.status(400).json({
            success: false,
            message: 'provider, model, input_tokens, and output_tokens are required'
        });
        return;
    }

    if (!user_id && !key_code) {
        res.status(400).json({
            success: false,
            message: 'Either user_id or key_code is required'
        });
        return;
    }

    // Calculer le coût automatiquement
    const { cost_usd, breakdown } = calculateRequestCost(provider, model, input_tokens, output_tokens);

    console.log(`[TOKENS] ${provider}/${model}: ${input_tokens} in + ${output_tokens} out = $${cost_usd.toFixed(6)}`);

    try {
        let targetKeyCode = key_code;

        // Si pas de key_code mais user_id fourni, trouver la clé active
        if (!targetKeyCode && user_id) {
            const keysRef = db.collection ? db.collection(USER_KEYS_COLLECTION) : null;
            if (!keysRef) {
                res.status(503).json({ success: false, message: 'Database not available' });
                return;
            }

            const snapshot = await keysRef
                .where('user_id', '==', user_id)
                .where('status', '==', 'ACTIVE')
                .get();

            let maxBalance = 0;
            snapshot.forEach((doc: any) => {
                const data = doc.data();
                const remaining = (data.balance_usd || 0) - (data.current_usage || 0);
                // Filtrer par provider si possible
                if (data.provider === provider || !data.provider) {
                    if (remaining > maxBalance) {
                        maxBalance = remaining;
                        targetKeyCode = doc.id;
                    }
                }
            });

            if (!targetKeyCode) {
                res.status(402).json({
                    success: false,
                    message: `No active key found for user ${user_id}`,
                    cost_calculated: cost_usd,
                    breakdown
                });
                return;
            }
        }

        // Effectuer le débit
        const result = await debitWallet(
            targetKeyCode!,
            user_id,
            cost_usd,
            `${provider}/${model}`
        );

        res.status(result.success ? 200 : (result.status === 'DEPLETED' ? 402 : 400)).json({
            ...result,
            key_code: targetKeyCode,
            cost_calculated: cost_usd,
            tokens: { input: input_tokens, output: output_tokens },
            breakdown,
            description: description || `${provider}/${model}`
        });

    } catch (error) {
        console.error('Error debiting by tokens:', error);
        res.status(500).json({
            success: false,
            message: 'Server error',
            cost_calculated: cost_usd,
            breakdown
        });
    }
});

// Get wallet status for a user
server.get('/api/wallet/:user_id', async (req: Request, res: Response) => {
    const userId = req.params.user_id;
    try {
        const keysRef = db.collection ? db.collection(USER_KEYS_COLLECTION) : null;
        if (!keysRef) {
            res.json({ user_id: userId, total_balance: 0, active_keys: 0 });
            return;
        }

        const snapshot = await keysRef.where('user_id', '==', userId).get();

        let totalBalance = 0;
        let activeKeys = 0;
        let primaryKey: any = null;

        snapshot.forEach((doc: any) => {
            const data = doc.data();
            if (data.status === 'ACTIVE') {
                const remaining = (data.balance_usd || 0) - (data.current_usage || 0);
                activeKeys++;
                totalBalance += remaining;
                if (!primaryKey || remaining > primaryKey.remaining_balance) {
                    primaryKey = {
                        key_code: doc.id,
                        provider: data.provider,
                        remaining_balance: remaining
                    };
                }
            }
        });

        res.json({
            user_id: userId,
            total_balance: totalBalance,
            active_keys: activeKeys,
            primary_key: primaryKey
        });

    } catch (error) {
        console.error('Error getting wallet status:', error);
        res.json({ user_id: userId, total_balance: 0, active_keys: 0 });
    }
});

server.listen(PORT, () => {
    console.log(`Key Validation Service running on port ${PORT}`);
});
