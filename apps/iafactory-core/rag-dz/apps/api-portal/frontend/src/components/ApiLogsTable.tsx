/**
 * iaFactory API Portal - Logs Table
 * Module 16 - Table des logs récents avec pagination
 */

import React, { useState, useEffect } from 'react';

// Types
interface LogEntry {
  id: string;
  timestamp: string;
  api_key_prefix: string;
  endpoint: string;
  method: string;
  status_code: number;
  latency_ms: number;
  credits_used: number;
  request_body_preview?: string;
  error_message?: string;
}

interface LogsResponse {
  logs: LogEntry[];
  total: number;
  page: number;
  page_size: number;
  has_more: boolean;
}

type StatusFilter = 'all' | 'success' | 'error';
type TimeRange = '24h' | '7d' | '30d' | '90d';

// Composant Badge de status HTTP
const StatusBadge: React.FC<{ status: number }> = ({ status }) => {
  const getStatusColor = () => {
    if (status >= 200 && status < 300) return 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/50 dark:text-emerald-400';
    if (status >= 400 && status < 500) return 'bg-amber-100 text-amber-700 dark:bg-amber-900/50 dark:text-amber-400';
    if (status >= 500) return 'bg-red-100 text-red-700 dark:bg-red-900/50 dark:text-red-400';
    return 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300';
  };

  return (
    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor()}`}>
      {status}
    </span>
  );
};

// Composant badge de méthode HTTP
const MethodBadge: React.FC<{ method: string }> = ({ method }) => {
  const colors: Record<string, string> = {
    GET: 'bg-blue-100 text-blue-700 dark:bg-blue-900/50 dark:text-blue-400',
    POST: 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/50 dark:text-emerald-400',
    PUT: 'bg-amber-100 text-amber-700 dark:bg-amber-900/50 dark:text-amber-400',
    DELETE: 'bg-red-100 text-red-700 dark:bg-red-900/50 dark:text-red-400',
  };

  return (
    <span className={`px-2 py-0.5 rounded text-xs font-mono font-medium ${colors[method] || colors.GET}`}>
      {method}
    </span>
  );
};

// Modal de détail du log
const LogDetailModal: React.FC<{
  log: LogEntry | null;
  onClose: () => void;
}> = ({ log, onClose }) => {
  if (!log) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-gray-800 rounded-2xl max-w-2xl w-full shadow-2xl max-h-[90vh] overflow-hidden">
        <div className="p-6 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
          <h2 className="text-xl font-bold text-gray-800 dark:text-white flex items-center gap-2">
            📋 Détail du log
          </h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
          >
            ✕
          </button>
        </div>
        
        <div className="p-6 overflow-y-auto max-h-[60vh] space-y-4">
          {/* Infos principales */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-sm text-gray-500">Timestamp</label>
              <p className="font-medium text-gray-800 dark:text-white">
                {new Date(log.timestamp).toLocaleString('fr-FR')}
              </p>
            </div>
            <div>
              <label className="text-sm text-gray-500">Clé API</label>
              <p className="font-mono text-sm text-gray-800 dark:text-white">
                {log.api_key_prefix}
              </p>
            </div>
            <div>
              <label className="text-sm text-gray-500">Endpoint</label>
              <p className="font-mono text-sm text-gray-800 dark:text-white">
                {log.endpoint}
              </p>
            </div>
            <div>
              <label className="text-sm text-gray-500">Méthode</label>
              <MethodBadge method={log.method} />
            </div>
            <div>
              <label className="text-sm text-gray-500">Status</label>
              <StatusBadge status={log.status_code} />
            </div>
            <div>
              <label className="text-sm text-gray-500">Latence</label>
              <p className={`font-medium ${log.latency_ms > 500 ? 'text-amber-500' : 'text-gray-800 dark:text-white'}`}>
                {log.latency_ms}ms
              </p>
            </div>
            <div>
              <label className="text-sm text-gray-500">Crédits</label>
              <p className="font-medium text-gray-800 dark:text-white">
                {log.credits_used}
              </p>
            </div>
          </div>

          {/* Request body preview */}
          {log.request_body_preview && (
            <div>
              <label className="text-sm text-gray-500 block mb-2">Request Body</label>
              <pre className="bg-gray-100 dark:bg-gray-900 p-4 rounded-lg text-sm overflow-x-auto font-mono text-gray-700 dark:text-gray-300">
                {log.request_body_preview}
              </pre>
            </div>
          )}

          {/* Error message */}
          {log.error_message && (
            <div>
              <label className="text-sm text-red-500 block mb-2">Erreur</label>
              <pre className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 p-4 rounded-lg text-sm overflow-x-auto font-mono text-red-700 dark:text-red-300">
                {log.error_message}
              </pre>
            </div>
          )}
        </div>

        <div className="p-6 border-t border-gray-200 dark:border-gray-700">
          <button
            onClick={onClose}
            className="w-full px-4 py-3 bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-white rounded-xl font-medium hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
          >
            Fermer
          </button>
        </div>
      </div>
    </div>
  );
};

/**
 * Composant principal table des logs
 */
export const ApiLogsTable: React.FC = () => {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [hasMore, setHasMore] = useState(false);
  const [range, setRange] = useState<TimeRange>('7d');
  const [statusFilter, setStatusFilter] = useState<StatusFilter>('all');
  const [endpointFilter, setEndpointFilter] = useState('');
  const [selectedLog, setSelectedLog] = useState<LogEntry | null>(null);

  const pageSize = 20;

  useEffect(() => {
    const fetchLogs = async () => {
      setLoading(true);
      // TODO: Appel API réel GET /api/dev/logs
      await new Promise(r => setTimeout(r, 400));
      
      // Données simulées
      const mockLogs: LogEntry[] = Array.from({ length: pageSize }, (_, i) => {
        const now = new Date();
        now.setMinutes(now.getMinutes() - i * 15);
        
        const endpoints = [
          '/api/v1/rag/query',
          '/api/v1/legal/ask',
          '/api/v1/fiscal/simulate',
          '/api/v1/park/sparkpage',
          '/api/v1/fiscal/g50'
        ];
        
        const isError = Math.random() < 0.1;
        const statusCodes = isError 
          ? [400, 401, 403, 429, 500, 502, 503]
          : [200, 201];
        
        return {
          id: `log-${page}-${i}`,
          timestamp: now.toISOString(),
          api_key_prefix: 'IAFK_live_a1b2...wxyz',
          endpoint: endpoints[Math.floor(Math.random() * endpoints.length)],
          method: 'POST',
          status_code: statusCodes[Math.floor(Math.random() * statusCodes.length)],
          latency_ms: Math.floor(Math.random() * 500) + 50,
          credits_used: Math.floor(Math.random() * 5) + 1,
          request_body_preview: '{"query": "Quels sont les taux de TVA en Algérie ?"}',
          error_message: isError ? 'Rate limit exceeded' : undefined
        };
      });
      
      // Appliquer les filtres (simulation)
      let filtered = mockLogs;
      if (statusFilter === 'success') {
        filtered = filtered.filter(l => l.status_code < 400);
      } else if (statusFilter === 'error') {
        filtered = filtered.filter(l => l.status_code >= 400);
      }
      if (endpointFilter) {
        filtered = filtered.filter(l => l.endpoint.includes(endpointFilter));
      }
      
      setLogs(filtered);
      setTotal(250); // Simulé
      setHasMore(page * pageSize < 250);
      setLoading(false);
    };
    
    fetchLogs();
  }, [page, range, statusFilter, endpointFilter]);

  const formatTime = (timestamp: string) => {
    return new Date(timestamp).toLocaleString('fr-FR', {
      day: '2-digit',
      month: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  return (
    <div className="space-y-6">
      {/* Header & Filtres */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-gray-800 dark:text-white">
            Logs API
          </h2>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            {total.toLocaleString()} requêtes sur la période
          </p>
        </div>

        {/* Filtres */}
        <div className="flex flex-wrap gap-3">
          {/* Période */}
          <select
            value={range}
            onChange={(e) => setRange(e.target.value as TimeRange)}
            className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-xl bg-white dark:bg-gray-700 text-gray-800 dark:text-white focus:ring-2 focus:ring-emerald-500"
          >
            <option value="24h">24 heures</option>
            <option value="7d">7 jours</option>
            <option value="30d">30 jours</option>
            <option value="90d">90 jours</option>
          </select>

          {/* Status */}
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value as StatusFilter)}
            className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-xl bg-white dark:bg-gray-700 text-gray-800 dark:text-white focus:ring-2 focus:ring-emerald-500"
          >
            <option value="all">Tous les status</option>
            <option value="success">✓ Succès (2xx)</option>
            <option value="error">✕ Erreurs (4xx/5xx)</option>
          </select>

          {/* Endpoint */}
          <input
            type="text"
            placeholder="Filtrer par endpoint..."
            value={endpointFilter}
            onChange={(e) => setEndpointFilter(e.target.value)}
            className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-xl bg-white dark:bg-gray-700 text-gray-800 dark:text-white focus:ring-2 focus:ring-emerald-500 w-48"
          />
        </div>
      </div>

      {/* Table */}
      <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 overflow-hidden">
        {loading ? (
          <div className="p-12 text-center">
            <span className="animate-spin text-3xl">⚙️</span>
          </div>
        ) : logs.length === 0 ? (
          <div className="p-12 text-center text-gray-500">
            <span className="text-4xl block mb-2">📋</span>
            Aucun log trouvé avec ces filtres
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 dark:bg-gray-900">
                <tr>
                  <th className="text-left py-3 px-4 text-sm font-medium text-gray-500">Timestamp</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-gray-500">Clé API</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-gray-500">Endpoint</th>
                  <th className="text-center py-3 px-4 text-sm font-medium text-gray-500">Method</th>
                  <th className="text-center py-3 px-4 text-sm font-medium text-gray-500">Status</th>
                  <th className="text-right py-3 px-4 text-sm font-medium text-gray-500">Latence</th>
                  <th className="text-right py-3 px-4 text-sm font-medium text-gray-500">Crédits</th>
                  <th className="text-center py-3 px-4 text-sm font-medium text-gray-500">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
                {logs.map((log) => (
                  <tr 
                    key={log.id} 
                    className={`hover:bg-gray-50 dark:hover:bg-gray-700/50 cursor-pointer ${
                      log.status_code >= 400 ? 'bg-red-50/50 dark:bg-red-900/10' : ''
                    }`}
                    onClick={() => setSelectedLog(log)}
                  >
                    <td className="py-3 px-4 text-sm text-gray-600 dark:text-gray-400 font-mono">
                      {formatTime(log.timestamp)}
                    </td>
                    <td className="py-3 px-4">
                      <code className="text-xs font-mono text-gray-500 bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded">
                        {log.api_key_prefix.substring(0, 15)}...
                      </code>
                    </td>
                    <td className="py-3 px-4">
                      <code className="text-sm font-mono text-gray-700 dark:text-gray-300">
                        {log.endpoint.split('/').slice(-2).join('/')}
                      </code>
                    </td>
                    <td className="py-3 px-4 text-center">
                      <MethodBadge method={log.method} />
                    </td>
                    <td className="py-3 px-4 text-center">
                      <StatusBadge status={log.status_code} />
                    </td>
                    <td className="py-3 px-4 text-right">
                      <span className={`text-sm font-medium ${
                        log.latency_ms > 500 ? 'text-amber-500' : 'text-gray-600 dark:text-gray-400'
                      }`}>
                        {log.latency_ms}ms
                      </span>
                    </td>
                    <td className="py-3 px-4 text-right text-sm text-gray-600 dark:text-gray-400">
                      {log.credits_used}
                    </td>
                    <td className="py-3 px-4 text-center">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          setSelectedLog(log);
                        }}
                        className="p-2 hover:bg-gray-100 dark:hover:bg-gray-600 rounded-lg transition-colors"
                        title="Voir les détails"
                      >
                        👁️
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Pagination */}
        {!loading && logs.length > 0 && (
          <div className="p-4 border-t border-gray-200 dark:border-gray-700 flex items-center justify-between">
            <p className="text-sm text-gray-500">
              Page {page} • {logs.length} sur {total.toLocaleString()} résultats
            </p>
            <div className="flex gap-2">
              <button
                onClick={() => setPage(p => Math.max(1, p - 1))}
                disabled={page === 1}
                className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                ← Précédent
              </button>
              <button
                onClick={() => setPage(p => p + 1)}
                disabled={!hasMore}
                className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                Suivant →
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Export */}
      <div className="flex gap-3">
        <button className="px-4 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-xl text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors flex items-center gap-2">
          📥 Exporter CSV
        </button>
        <button className="px-4 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-xl text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors flex items-center gap-2">
          📊 Exporter JSON
        </button>
      </div>

      {/* Modal détail */}
      <LogDetailModal log={selectedLog} onClose={() => setSelectedLog(null)} />
    </div>
  );
};

export default ApiLogsTable;
