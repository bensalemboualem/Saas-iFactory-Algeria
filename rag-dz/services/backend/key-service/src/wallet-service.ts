/**
 * Wallet Debit Service - IA Factory
 * Gère le débit automatique des clés API après chaque requête LLM/TTS
 */

import { getFirestore, doc, getDoc, updateDoc, collection, query, where, getDocs } from 'firebase/firestore';

const USER_KEYS_COLLECTION = 'user_keys';

// Référence Firestore (initialisée dans index.ts)
let db: ReturnType<typeof getFirestore>;

export function initWalletService(firestore: ReturnType<typeof getFirestore>) {
    db = firestore;
}

// --- INTERFACES ---

export interface DebitRequest {
    userId: string;
    keyCode?: string;  // Optionnel: si fourni, débite cette clé spécifique
    costUsd: number;
    provider: string;
    model?: string;
    description?: string;
}

export interface DebitResponse {
    success: boolean;
    newBalance: number;
    keyCode: string;
    message: string;
}

export interface WalletStatus {
    userId: string;
    totalBalance: number;
    activeKeys: number;
    primaryKey?: {
        keyCode: string;
        provider: string;
        remainingBalance: number;
    };
}

// --- FONCTIONS PRINCIPALES ---

/**
 * Trouve la clé active principale d'un utilisateur
 */
export async function findUserActiveKey(userId: string, provider?: string): Promise<string | null> {
    try {
        const keysRef = collection(db, USER_KEYS_COLLECTION);

        // Construire la query
        let q = query(
            keysRef,
            where('user_id', '==', userId),
            where('status', '==', 'ACTIVE')
        );

        const snapshot = await getDocs(q);

        if (snapshot.empty) {
            return null;
        }

        // Si un provider spécifique est demandé, filtrer
        let bestKey: any = null;
        let bestBalance = 0;

        snapshot.forEach((doc) => {
            const data = doc.data();
            const remaining = (data.balance_usd || 0) - (data.current_usage || 0);

            // Filtrer par provider si spécifié
            if (provider && data.provider !== provider) {
                return;
            }

            // Prendre la clé avec le plus gros solde
            if (remaining > bestBalance) {
                bestBalance = remaining;
                bestKey = { id: doc.id, ...data };
            }
        });

        return bestKey?.id || null;
    } catch (error) {
        console.error('Error finding user active key:', error);
        return null;
    }
}

/**
 * Débite le wallet d'un utilisateur après une requête API
 */
export async function debitWallet(request: DebitRequest): Promise<DebitResponse> {
    const { userId, costUsd, provider, description } = request;
    let { keyCode } = request;

    // Validation
    if (!userId || costUsd <= 0) {
        return {
            success: false,
            newBalance: 0,
            keyCode: '',
            message: 'Invalid request: userId and positive costUsd required'
        };
    }

    try {
        // Si pas de keyCode fourni, trouver la clé active de l'utilisateur
        if (!keyCode) {
            keyCode = await findUserActiveKey(userId, provider) || undefined;

            if (!keyCode) {
                return {
                    success: false,
                    newBalance: 0,
                    keyCode: '',
                    message: `No active key found for user ${userId}${provider ? ` with provider ${provider}` : ''}`
                };
            }
        }

        const keyDocRef = doc(db, USER_KEYS_COLLECTION, keyCode.toUpperCase());
        const docSnap = await getDoc(keyDocRef);

        if (!docSnap.exists()) {
            return {
                success: false,
                newBalance: 0,
                keyCode,
                message: 'Key not found'
            };
        }

        const data = docSnap.data();

        // Vérifications de sécurité
        if (data.user_id !== userId) {
            return {
                success: false,
                newBalance: 0,
                keyCode,
                message: 'Key does not belong to this user'
            };
        }

        if (data.status !== 'ACTIVE') {
            return {
                success: false,
                newBalance: 0,
                keyCode,
                message: `Key is ${data.status}`
            };
        }

        const balance = data.balance_usd || 0;
        const currentUsage = data.current_usage || 0;
        const remainingBalance = balance - currentUsage;

        if (costUsd > remainingBalance) {
            return {
                success: false,
                newBalance: remainingBalance,
                keyCode,
                message: `Insufficient balance. Required: $${costUsd.toFixed(4)}, Available: $${remainingBalance.toFixed(4)}`
            };
        }

        // Effectuer le débit
        const newUsage = currentUsage + costUsd;
        const newBalance = balance - newUsage;

        const updateData: Record<string, any> = {
            current_usage: newUsage,
            last_used_at: new Date(),
            last_provider: provider
        };

        // Marquer comme épuisée si solde <= 0
        if (newBalance <= 0) {
            updateData.status = 'DEPLETED';
        }

        await updateDoc(keyDocRef, updateData);

        console.log(`[WALLET] Debited $${costUsd.toFixed(4)} from ${keyCode} (${provider}). New balance: $${newBalance.toFixed(4)}`);

        return {
            success: true,
            newBalance,
            keyCode,
            message: `Debited $${costUsd.toFixed(4)} for ${provider}${description ? `: ${description}` : ''}`
        };

    } catch (error) {
        console.error('Error debiting wallet:', error);
        return {
            success: false,
            newBalance: 0,
            keyCode: keyCode || '',
            message: 'Server error during debit operation'
        };
    }
}

/**
 * Récupère le statut du wallet d'un utilisateur
 */
export async function getWalletStatus(userId: string): Promise<WalletStatus> {
    try {
        const keysRef = collection(db, USER_KEYS_COLLECTION);
        const q = query(keysRef, where('user_id', '==', userId));
        const snapshot = await getDocs(q);

        let totalBalance = 0;
        let activeKeys = 0;
        let primaryKey: WalletStatus['primaryKey'] = undefined;
        let maxBalance = 0;

        snapshot.forEach((doc) => {
            const data = doc.data();
            const remaining = (data.balance_usd || 0) - (data.current_usage || 0);

            if (data.status === 'ACTIVE') {
                activeKeys++;
                totalBalance += remaining;

                if (remaining > maxBalance) {
                    maxBalance = remaining;
                    primaryKey = {
                        keyCode: doc.id,
                        provider: data.provider,
                        remainingBalance: remaining
                    };
                }
            }
        });

        return {
            userId,
            totalBalance,
            activeKeys,
            primaryKey
        };

    } catch (error) {
        console.error('Error getting wallet status:', error);
        return {
            userId,
            totalBalance: 0,
            activeKeys: 0
        };
    }
}

/**
 * Vérifie si l'utilisateur a assez de crédit pour une opération
 */
export async function checkSufficientBalance(userId: string, requiredAmount: number, provider?: string): Promise<{
    sufficient: boolean;
    availableBalance: number;
    keyCode?: string;
}> {
    const keyCode = await findUserActiveKey(userId, provider);

    if (!keyCode) {
        return { sufficient: false, availableBalance: 0 };
    }

    const keyDocRef = doc(db, USER_KEYS_COLLECTION, keyCode);
    const docSnap = await getDoc(keyDocRef);

    if (!docSnap.exists()) {
        return { sufficient: false, availableBalance: 0 };
    }

    const data = docSnap.data();
    const remaining = (data.balance_usd || 0) - (data.current_usage || 0);

    return {
        sufficient: remaining >= requiredAmount,
        availableBalance: remaining,
        keyCode
    };
}

// --- CALCUL DE COÛTS ---

export const COST_PER_1M_TOKENS: Record<string, Record<string, { input: number; output: number }>> = {
    Groq: {
        'llama-3.3-70b-versatile': { input: 0.59, output: 0.79 },
        'llama-3.1-8b-instant': { input: 0.05, output: 0.08 },
        'mixtral-8x7b-32768': { input: 0.24, output: 0.24 },
        'whisper-large-v3': { input: 0.111, output: 0 }  // TTS/STT
    },
    OpenRouter: {
        'anthropic/claude-3.5-sonnet': { input: 3.0, output: 15.0 },
        'google/gemini-2.0-flash': { input: 0.1, output: 0.4 },
        'meta-llama/llama-3.3-70b': { input: 0.4, output: 0.4 }
    },
    OpenAI: {
        'gpt-4o': { input: 2.5, output: 10.0 },
        'gpt-4o-mini': { input: 0.15, output: 0.6 },
        'tts-1': { input: 15.0, output: 0 }  // $15 per 1M characters
    }
};

/**
 * Calcule le coût d'une requête LLM
 */
export function calculateRequestCost(
    provider: string,
    model: string,
    inputTokens: number,
    outputTokens: number,
    margin: number = 1.3
): number {
    const providerCosts = COST_PER_1M_TOKENS[provider];
    if (!providerCosts) {
        return 0.001; // Coût minimal par défaut
    }

    const modelCosts = providerCosts[model] || Object.values(providerCosts)[0];

    const inputCost = (inputTokens / 1_000_000) * modelCosts.input;
    const outputCost = (outputTokens / 1_000_000) * modelCosts.output;

    return (inputCost + outputCost) * margin;
}
