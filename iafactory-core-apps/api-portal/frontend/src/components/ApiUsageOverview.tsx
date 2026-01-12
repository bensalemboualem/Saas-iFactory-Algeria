/**
 * iaFactory API Portal - Usage Overview
 * Module 16 - Statistiques d'usage avec graphiques
 */

import React, { useState, useEffect } from 'react';

// Types
interface UsageStats {
  range: string;
  total_requests: number;
  avg_requests_per_day: number;
  error_rate: number;
  avg_latency_ms: number;
  credits_consumed: number;
  credits_remaining: number;
  by_endpoint: EndpointStat[];
  timeseries: TimeseriesPoint[];
}

interface EndpointStat {
  endpoint: string;
  count: number;
  avg_latency_ms: number;
  error_count: number;
}

interface TimeseriesPoint {
  date: string;
  count: number;
  errors: number;
  avg_latency_ms: number;
}

type TimeRange = '24h' | '7d' | '30d' | '90d';

// Composant de sélection de période
const RangeSelector: React.FC<{
  value: TimeRange;
  onChange: (range: TimeRange) => void;
}> = ({ value, onChange }) => {
  const ranges: { value: TimeRange; label: string }[] = [
    { value: '24h', label: '24 heures' },
    { value: '7d', label: '7 jours' },
    { value: '30d', label: '30 jours' },
    { value: '90d', label: '90 jours' },
  ];

  return (
    <div className="flex gap-2 bg-gray-100 dark:bg-gray-700 p-1 rounded-xl">
      {ranges.map((r) => (
        <button
          key={r.value}
          onClick={() => onChange(r.value)}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
            value === r.value
              ? 'bg-white dark:bg-gray-600 text-emerald-600 dark:text-emerald-400 shadow-sm'
              : 'text-gray-600 dark:text-gray-300 hover:text-gray-800 dark:hover:text-white'
          }`}
        >
          {r.label}
        </button>
      ))}
    </div>
  );
};

// Stat Card simple
const StatCard: React.FC<{
  label: string;
  value: string | number;
  subtitle?: string;
  color?: string;
}> = ({ label, value, subtitle, color = 'emerald' }) => (
  <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
    <p className="text-sm text-gray-500 dark:text-gray-400">{label}</p>
    <p className={`text-2xl font-bold mt-1 text-${color}-600 dark:text-${color}-400`}>
      {typeof value === 'number' ? value.toLocaleString() : value}
    </p>
    {subtitle && <p className="text-xs text-gray-400 mt-1">{subtitle}</p>}
  </div>
);

// Graphique en barres simple
const BarChart: React.FC<{
  data: TimeseriesPoint[];
  height?: number;
}> = ({ data, height = 200 }) => {
  const maxCount = Math.max(...data.map(d => d.count), 1);

  return (
    <div className="relative" style={{ height }}>
      <div className="absolute inset-0 flex items-end gap-1">
        {data.map((point, i) => {
          const barHeight = (point.count / maxCount) * 100;
          const errorHeight = point.errors > 0 ? (point.errors / maxCount) * 100 : 0;
          
          return (
            <div key={i} className="flex-1 flex flex-col items-center justify-end h-full group">
              {/* Tooltip */}
              <div className="absolute bottom-full mb-2 hidden group-hover:block bg-gray-900 text-white text-xs rounded-lg px-3 py-2 whitespace-nowrap z-10">
                <p className="font-medium">{point.date}</p>
                <p>{point.count.toLocaleString()} requêtes</p>
                {point.errors > 0 && <p className="text-red-400">{point.errors} erreurs</p>}
                <p className="text-gray-400">{point.avg_latency_ms}ms latence</p>
              </div>
              
              {/* Bar */}
              <div className="w-full flex flex-col justify-end" style={{ height: `${barHeight}%` }}>
                {errorHeight > 0 && (
                  <div 
                    className="w-full bg-red-400 rounded-t-sm"
                    style={{ height: `${(errorHeight / barHeight) * 100}%`, minHeight: '2px' }}
                  />
                )}
                <div 
                  className="w-full bg-emerald-500 dark:bg-emerald-400 rounded-t-sm group-hover:bg-emerald-600 transition-colors"
                  style={{ height: `${100 - (errorHeight / barHeight) * 100}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
      
      {/* Y-axis labels */}
      <div className="absolute left-0 top-0 h-full flex flex-col justify-between text-xs text-gray-400 -ml-10">
        <span>{maxCount.toLocaleString()}</span>
        <span>{Math.round(maxCount / 2).toLocaleString()}</span>
        <span>0</span>
      </div>
    </div>
  );
};

// Graphique de latence
const LatencyChart: React.FC<{
  data: TimeseriesPoint[];
  height?: number;
}> = ({ data, height = 150 }) => {
  const maxLatency = Math.max(...data.map(d => d.avg_latency_ms), 1);
  
  // Générer les points du path SVG
  const points = data.map((point, i) => {
    const x = (i / (data.length - 1)) * 100;
    const y = 100 - (point.avg_latency_ms / maxLatency) * 100;
    return `${x},${y}`;
  }).join(' ');

  return (
    <div className="relative" style={{ height }}>
      <svg className="w-full h-full" viewBox="0 0 100 100" preserveAspectRatio="none">
        {/* Area fill */}
        <polygon
          points={`0,100 ${points} 100,100`}
          fill="url(#latencyGradient)"
          opacity="0.3"
        />
        {/* Line */}
        <polyline
          points={points}
          fill="none"
          stroke="#8B5CF6"
          strokeWidth="2"
          vectorEffect="non-scaling-stroke"
        />
        <defs>
          <linearGradient id="latencyGradient" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#8B5CF6" />
            <stop offset="100%" stopColor="#8B5CF6" stopOpacity="0" />
          </linearGradient>
        </defs>
      </svg>
      
      {/* Labels */}
      <div className="absolute left-0 top-0 h-full flex flex-col justify-between text-xs text-gray-400 -ml-10">
        <span>{maxLatency}ms</span>
        <span>0ms</span>
      </div>
    </div>
  );
};

// Table des endpoints
const EndpointsTable: React.FC<{
  data: EndpointStat[];
}> = ({ data }) => {
  const total = data.reduce((sum, d) => sum + d.count, 0) || 1;

  return (
    <div className="overflow-x-auto">
      <table className="w-full">
        <thead>
          <tr className="border-b border-gray-200 dark:border-gray-700">
            <th className="text-left py-3 px-4 text-sm font-medium text-gray-500">Endpoint</th>
            <th className="text-right py-3 px-4 text-sm font-medium text-gray-500">Requêtes</th>
            <th className="text-right py-3 px-4 text-sm font-medium text-gray-500">%</th>
            <th className="text-right py-3 px-4 text-sm font-medium text-gray-500">Latence</th>
            <th className="text-right py-3 px-4 text-sm font-medium text-gray-500">Erreurs</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
          {data.map((endpoint) => {
            const percent = ((endpoint.count / total) * 100).toFixed(1);
            const shortName = endpoint.endpoint.split('/').slice(-2).join('/');
            
            return (
              <tr key={endpoint.endpoint} className="hover:bg-gray-50 dark:hover:bg-gray-700/50">
                <td className="py-3 px-4">
                  <code className="text-sm font-mono text-gray-700 dark:text-gray-300">
                    {shortName}
                  </code>
                </td>
                <td className="py-3 px-4 text-right font-medium text-gray-800 dark:text-white">
                  {endpoint.count.toLocaleString()}
                </td>
                <td className="py-3 px-4 text-right">
                  <div className="flex items-center justify-end gap-2">
                    <div className="w-16 h-2 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-emerald-500 rounded-full"
                        style={{ width: `${percent}%` }}
                      />
                    </div>
                    <span className="text-sm text-gray-500">{percent}%</span>
                  </div>
                </td>
                <td className="py-3 px-4 text-right">
                  <span className={`text-sm ${endpoint.avg_latency_ms > 500 ? 'text-amber-500' : 'text-gray-500'}`}>
                    {endpoint.avg_latency_ms}ms
                  </span>
                </td>
                <td className="py-3 px-4 text-right">
                  <span className={`text-sm ${endpoint.error_count > 0 ? 'text-red-500 font-medium' : 'text-gray-400'}`}>
                    {endpoint.error_count}
                  </span>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

/**
 * Composant principal Usage Overview
 */
export const ApiUsageOverview: React.FC = () => {
  const [range, setRange] = useState<TimeRange>('7d');
  const [stats, setStats] = useState<UsageStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      setLoading(true);
      // TODO: Appel API réel GET /api/dev/usage?range=${range}
      await new Promise(r => setTimeout(r, 500));
      
      // Générer des données simulées selon la période
      const days = range === '24h' ? 24 : range === '7d' ? 7 : range === '30d' ? 30 : 90;
      const now = new Date();
      
      const timeseries: TimeseriesPoint[] = Array.from({ length: Math.min(days, 30) }, (_, i) => {
        const date = new Date(now);
        date.setDate(date.getDate() - (days - 1 - i));
        return {
          date: date.toISOString().split('T')[0],
          count: Math.floor(Math.random() * 500) + 50,
          errors: Math.floor(Math.random() * 10),
          avg_latency_ms: Math.floor(Math.random() * 300) + 100
        };
      });
      
      setStats({
        range,
        total_requests: timeseries.reduce((sum, t) => sum + t.count, 0),
        avg_requests_per_day: Math.round(timeseries.reduce((sum, t) => sum + t.count, 0) / days),
        error_rate: 0.023,
        avg_latency_ms: 187,
        credits_consumed: 4520,
        credits_remaining: 5480,
        by_endpoint: [
          { endpoint: '/api/v1/rag/query', count: 8450, avg_latency_ms: 245, error_count: 12 },
          { endpoint: '/api/v1/legal/ask', count: 3210, avg_latency_ms: 312, error_count: 5 },
          { endpoint: '/api/v1/fiscal/simulate', count: 2890, avg_latency_ms: 89, error_count: 2 },
          { endpoint: '/api/v1/park/sparkpage', count: 1240, avg_latency_ms: 520, error_count: 8 },
          { endpoint: '/api/v1/fiscal/g50', count: 890, avg_latency_ms: 156, error_count: 1 },
        ],
        timeseries
      });
      
      setLoading(false);
    };
    
    fetchStats();
  }, [range]);

  if (loading || !stats) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin text-4xl">⚙️</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header avec sélecteur de période */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-gray-800 dark:text-white">
            Statistiques d'usage
          </h2>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            Analyse de votre consommation API
          </p>
        </div>
        <RangeSelector value={range} onChange={setRange} />
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          label="Total requêtes"
          value={stats.total_requests}
          subtitle={`~${stats.avg_requests_per_day}/jour`}
        />
        <StatCard
          label="Taux d'erreur"
          value={`${(stats.error_rate * 100).toFixed(2)}%`}
          subtitle={stats.error_rate > 0.05 ? '⚠️ Élevé' : '✓ Normal'}
          color={stats.error_rate > 0.05 ? 'red' : 'emerald'}
        />
        <StatCard
          label="Latence moyenne"
          value={`${stats.avg_latency_ms}ms`}
          subtitle={stats.avg_latency_ms > 500 ? '⚠️ Lente' : '✓ Rapide'}
          color={stats.avg_latency_ms > 500 ? 'amber' : 'emerald'}
        />
        <StatCard
          label="Crédits consommés"
          value={stats.credits_consumed}
          subtitle={`${stats.credits_remaining} restants`}
        />
      </div>

      {/* Graphiques */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Requêtes par jour */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 border border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-bold text-gray-800 dark:text-white mb-4">
            📊 Requêtes par jour
          </h3>
          <BarChart data={stats.timeseries} height={200} />
          <div className="mt-4 flex items-center gap-4 text-sm">
            <span className="flex items-center gap-1">
              <span className="w-3 h-3 bg-emerald-500 rounded" />
              Succès
            </span>
            <span className="flex items-center gap-1">
              <span className="w-3 h-3 bg-red-400 rounded" />
              Erreurs
            </span>
          </div>
        </div>

        {/* Latence */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 border border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-bold text-gray-800 dark:text-white mb-4">
            ⚡ Latence moyenne
          </h3>
          <LatencyChart data={stats.timeseries} height={200} />
          <div className="mt-4 flex items-center gap-4 text-sm">
            <span className="flex items-center gap-1">
              <span className="w-3 h-3 bg-purple-500 rounded" />
              Latence (ms)
            </span>
            <span className="text-gray-500">
              Moyenne: {stats.avg_latency_ms}ms
            </span>
          </div>
        </div>
      </div>

      {/* Table des endpoints */}
      <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 overflow-hidden">
        <div className="p-4 border-b border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-bold text-gray-800 dark:text-white">
            🎯 Répartition par endpoint
          </h3>
        </div>
        <EndpointsTable data={stats.by_endpoint} />
      </div>
    </div>
  );
};

export default ApiUsageOverview;
