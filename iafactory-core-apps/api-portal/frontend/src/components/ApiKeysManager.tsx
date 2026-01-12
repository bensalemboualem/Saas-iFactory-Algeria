/**
 * iaFactory API Portal - API Keys Manager
 * Module 16 - Gestion des clés API façon OpenAI
 */

import React, { useState, useEffect } from 'react';

// Types
interface ApiKey {
  id: string;
  name: string;
  prefix: string;
  created_at: string;
  last_used_at: string | null;
  status: 'active' | 'revoked';
}

interface NewKeyResponse {
  id: string;
  name: string;
  key: string;
  prefix: string;
  warning: string;
}

// Modal de création
const CreateKeyModal: React.FC<{
  isOpen: boolean;
  onClose: () => void;
  onCreate: (name: string) => Promise<NewKeyResponse>;
}> = ({ isOpen, onClose, onCreate }) => {
  const [name, setName] = useState('');
  const [loading, setLoading] = useState(false);
  const [newKey, setNewKey] = useState<NewKeyResponse | null>(null);
  const [copied, setCopied] = useState(false);

  const handleCreate = async () => {
    if (!name.trim()) return;
    setLoading(true);
    try {
      const result = await onCreate(name);
      setNewKey(result);
    } catch (error) {
      console.error('Erreur création clé:', error);
    }
    setLoading(false);
  };

  const handleCopy = async () => {
    if (newKey) {
      await navigator.clipboard.writeText(newKey.key);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleClose = () => {
    setName('');
    setNewKey(null);
    setCopied(false);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-gray-800 rounded-2xl max-w-lg w-full shadow-2xl">
        {/* Header */}
        <div className="p-6 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-xl font-bold text-gray-800 dark:text-white flex items-center gap-2">
            🔑 {newKey ? 'Nouvelle clé créée !' : 'Créer une clé API'}
          </h2>
        </div>

        {/* Content */}
        <div className="p-6">
          {!newKey ? (
            <>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Nom de la clé
              </label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Ex: Backend Production, Test Local..."
                className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-xl bg-white dark:bg-gray-700 text-gray-800 dark:text-white focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all"
              />
              <p className="mt-2 text-sm text-gray-500">
                Donnez un nom descriptif pour identifier cette clé.
              </p>
            </>
          ) : (
            <div className="space-y-4">
              {/* Warning */}
              <div className="bg-amber-50 dark:bg-amber-900/30 border border-amber-200 dark:border-amber-700 rounded-xl p-4">
                <p className="text-amber-800 dark:text-amber-200 font-medium flex items-center gap-2">
                  ⚠️ {newKey.warning}
                </p>
              </div>

              {/* Key Display */}
              <div className="bg-gray-100 dark:bg-gray-900 rounded-xl p-4">
                <label className="block text-sm font-medium text-gray-500 mb-2">
                  Votre clé API
                </label>
                <div className="flex items-center gap-2">
                  <code className="flex-1 font-mono text-sm bg-gray-200 dark:bg-gray-800 px-3 py-2 rounded-lg overflow-x-auto text-gray-800 dark:text-gray-200">
                    {newKey.key}
                  </code>
                  <button
                    onClick={handleCopy}
                    className={`px-4 py-2 rounded-lg font-medium transition-all ${
                      copied
                        ? 'bg-emerald-500 text-white'
                        : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'
                    }`}
                  >
                    {copied ? '✓ Copié !' : '📋 Copier'}
                  </button>
                </div>
              </div>

              {/* Instructions */}
              <div className="text-sm text-gray-600 dark:text-gray-400 space-y-2">
                <p><strong>Comment utiliser cette clé :</strong></p>
                <code className="block bg-gray-100 dark:bg-gray-900 p-3 rounded-lg overflow-x-auto">
                  Authorization: Bearer {newKey.prefix.slice(0, 15)}...
                </code>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-6 border-t border-gray-200 dark:border-gray-700 flex gap-3">
          {!newKey ? (
            <>
              <button
                onClick={handleClose}
                className="flex-1 px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-xl font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              >
                Annuler
              </button>
              <button
                onClick={handleCreate}
                disabled={!name.trim() || loading}
                className="flex-1 px-4 py-3 bg-emerald-500 text-white rounded-xl font-medium hover:bg-emerald-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
              >
                {loading ? (
                  <>
                    <span className="animate-spin">⚙️</span>
                    Création...
                  </>
                ) : (
                  <>
                    🔐 Créer la clé
                  </>
                )}
              </button>
            </>
          ) : (
            <button
              onClick={handleClose}
              className="w-full px-4 py-3 bg-emerald-500 text-white rounded-xl font-medium hover:bg-emerald-600 transition-colors"
            >
              ✓ Terminé
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

// Modal de confirmation révocation
const RevokeConfirmModal: React.FC<{
  isOpen: boolean;
  keyName: string;
  onClose: () => void;
  onConfirm: () => void;
  loading: boolean;
}> = ({ isOpen, keyName, onClose, onConfirm, loading }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-gray-800 rounded-2xl max-w-md w-full shadow-2xl">
        <div className="p-6">
          <div className="text-center mb-4">
            <span className="text-5xl">🗑️</span>
          </div>
          <h2 className="text-xl font-bold text-gray-800 dark:text-white text-center mb-2">
            Révoquer cette clé ?
          </h2>
          <p className="text-gray-600 dark:text-gray-400 text-center">
            La clé <strong>"{keyName}"</strong> sera définitivement désactivée.
            Toutes les applications utilisant cette clé cesseront de fonctionner.
          </p>
        </div>
        <div className="p-6 border-t border-gray-200 dark:border-gray-700 flex gap-3">
          <button
            onClick={onClose}
            disabled={loading}
            className="flex-1 px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-xl font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
          >
            Annuler
          </button>
          <button
            onClick={onConfirm}
            disabled={loading}
            className="flex-1 px-4 py-3 bg-red-500 text-white rounded-xl font-medium hover:bg-red-600 disabled:opacity-50 transition-colors flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <span className="animate-spin">⚙️</span>
                Révocation...
              </>
            ) : (
              <>
                🗑️ Révoquer
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

/**
 * Composant principal de gestion des clés
 */
export const ApiKeysManager: React.FC = () => {
  const [keys, setKeys] = useState<ApiKey[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [revokeTarget, setRevokeTarget] = useState<ApiKey | null>(null);
  const [revokeLoading, setRevokeLoading] = useState(false);

  // Charger les clés
  useEffect(() => {
    const fetchKeys = async () => {
      setLoading(true);
      // TODO: Appel API réel
      await new Promise(r => setTimeout(r, 500));
      
      // Données simulées
      setKeys([
        {
          id: '1',
          name: 'Backend Production',
          prefix: 'IAFK_live_a1b2c3d4...wxyz',
          created_at: '2025-10-15T10:30:00Z',
          last_used_at: '2025-11-29T08:45:00Z',
          status: 'active'
        },
        {
          id: '2',
          name: 'Mobile App',
          prefix: 'IAFK_live_e5f6g7h8...abcd',
          created_at: '2025-11-01T14:20:00Z',
          last_used_at: '2025-11-28T22:15:00Z',
          status: 'active'
        },
        {
          id: '3',
          name: 'Test Local (old)',
          prefix: 'IAFK_live_i9j0k1l2...efgh',
          created_at: '2025-09-20T09:00:00Z',
          last_used_at: '2025-10-01T11:30:00Z',
          status: 'revoked'
        }
      ]);
      
      setLoading(false);
    };
    
    fetchKeys();
  }, []);

  const handleCreate = async (name: string): Promise<NewKeyResponse> => {
    // TODO: Appel API réel POST /api/dev/api-keys
    await new Promise(r => setTimeout(r, 1000));
    
    const newKey: NewKeyResponse = {
      id: Date.now().toString(),
      name,
      key: `IAFK_live_${Math.random().toString(36).substring(2, 34)}`,
      prefix: 'IAFK_live_xxxx...yyyy',
      warning: 'Copiez cette clé maintenant. Vous ne pourrez plus la revoir.'
    };
    
    // Ajouter à la liste
    setKeys(prev => [{
      id: newKey.id,
      name: newKey.name,
      prefix: newKey.prefix,
      created_at: new Date().toISOString(),
      last_used_at: null,
      status: 'active'
    }, ...prev]);
    
    return newKey;
  };

  const handleRevoke = async () => {
    if (!revokeTarget) return;
    
    setRevokeLoading(true);
    // TODO: Appel API réel POST /api/dev/api-keys/{id}/revoke
    await new Promise(r => setTimeout(r, 1000));
    
    setKeys(prev => prev.map(k => 
      k.id === revokeTarget.id ? { ...k, status: 'revoked' as const } : k
    ));
    
    setRevokeLoading(false);
    setRevokeTarget(null);
  };

  const formatDate = (dateStr: string | null) => {
    if (!dateStr) return 'Jamais';
    return new Date(dateStr).toLocaleDateString('fr-FR', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const activeKeys = keys.filter(k => k.status === 'active');
  const revokedKeys = keys.filter(k => k.status === 'revoked');

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-800 dark:text-white">
            Vos clés API
          </h2>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            {activeKeys.length} clé(s) active(s) sur 10 maximum
          </p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          disabled={activeKeys.length >= 10}
          className="px-6 py-3 bg-emerald-500 text-white rounded-xl font-medium hover:bg-emerald-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center gap-2 shadow-lg shadow-emerald-500/30 hover:shadow-emerald-500/50"
        >
          <span className="text-xl">+</span>
          Créer une clé
        </button>
      </div>

      {/* Info Box */}
      <div className="bg-blue-50 dark:bg-blue-900/30 border border-blue-200 dark:border-blue-700 rounded-xl p-4">
        <p className="text-blue-800 dark:text-blue-200 flex items-start gap-2">
          <span className="text-xl">ℹ️</span>
          <span>
            <strong>Sécurité :</strong> Les clés API complètes ne sont affichées qu'une seule fois lors de leur création. 
            Conservez-les dans un gestionnaire de secrets sécurisé (ex: HashiCorp Vault, AWS Secrets Manager).
          </span>
        </p>
      </div>

      {/* Active Keys */}
      <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 overflow-hidden">
        <div className="p-4 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900">
          <h3 className="font-semibold text-gray-800 dark:text-white flex items-center gap-2">
            <span className="w-2 h-2 bg-emerald-500 rounded-full"></span>
            Clés actives ({activeKeys.length})
          </h3>
        </div>
        
        {loading ? (
          <div className="p-8 text-center">
            <span className="animate-spin text-3xl">⚙️</span>
          </div>
        ) : activeKeys.length === 0 ? (
          <div className="p-8 text-center text-gray-500">
            <span className="text-4xl block mb-2">🔑</span>
            Aucune clé active. Créez votre première clé API.
          </div>
        ) : (
          <div className="divide-y divide-gray-100 dark:divide-gray-700">
            {activeKeys.map((key) => (
              <div key={key.id} className="p-4 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3">
                      <h4 className="font-semibold text-gray-800 dark:text-white">
                        {key.name}
                      </h4>
                      <span className="px-2 py-0.5 bg-emerald-100 dark:bg-emerald-900/50 text-emerald-600 dark:text-emerald-400 text-xs font-medium rounded-full">
                        Active
                      </span>
                    </div>
                    <code className="text-sm text-gray-500 font-mono mt-1 block">
                      {key.prefix}
                    </code>
                  </div>
                  <div className="text-right mr-4">
                    <p className="text-sm text-gray-500">
                      Créée le {formatDate(key.created_at)}
                    </p>
                    <p className="text-sm text-gray-400">
                      Dernière utilisation: {formatDate(key.last_used_at)}
                    </p>
                  </div>
                  <button
                    onClick={() => setRevokeTarget(key)}
                    className="px-4 py-2 text-red-500 hover:bg-red-50 dark:hover:bg-red-900/30 rounded-lg transition-colors font-medium"
                  >
                    Révoquer
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Revoked Keys */}
      {revokedKeys.length > 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 overflow-hidden opacity-75">
          <div className="p-4 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900">
            <h3 className="font-semibold text-gray-500 dark:text-gray-400 flex items-center gap-2">
              <span className="w-2 h-2 bg-gray-400 rounded-full"></span>
              Clés révoquées ({revokedKeys.length})
            </h3>
          </div>
          <div className="divide-y divide-gray-100 dark:divide-gray-700">
            {revokedKeys.map((key) => (
              <div key={key.id} className="p-4">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3">
                      <h4 className="font-semibold text-gray-500 line-through">
                        {key.name}
                      </h4>
                      <span className="px-2 py-0.5 bg-gray-100 dark:bg-gray-700 text-gray-500 text-xs font-medium rounded-full">
                        Révoquée
                      </span>
                    </div>
                    <code className="text-sm text-gray-400 font-mono mt-1 block">
                      {key.prefix}
                    </code>
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-gray-400">
                      Créée le {formatDate(key.created_at)}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Modals */}
      <CreateKeyModal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        onCreate={handleCreate}
      />
      
      <RevokeConfirmModal
        isOpen={!!revokeTarget}
        keyName={revokeTarget?.name || ''}
        onClose={() => setRevokeTarget(null)}
        onConfirm={handleRevoke}
        loading={revokeLoading}
      />
    </div>
  );
};

export default ApiKeysManager;
