/**
 * iaFactory API Portal - Overview Dashboard
 * Module 16 - Vue d'ensemble avec stats et graphiques
 */

import React, { useState, useEffect } from 'react';

// Types
interface OverviewStats {
  requests_today: number;
  requests_30d: number;
  credits_consumed_month: number;
  errors_7d: number;
  active_keys: number;
  plan: string;
}

interface EndpointStat {
  endpoint: string;
  count: number;
}

interface TimeseriesPoint {
  date: string;
  count: number;
  errors: number;
}

// Composant Card Stat
const StatCard: React.FC<{
  title: string;
  value: string | number;
  icon: string;
  trend?: { value: number; isPositive: boolean };
  color: 'emerald' | 'blue' | 'purple' | 'amber' | 'red';
}> = ({ title, value, icon, trend, color }) => {
  const colorClasses = {
    emerald: 'from-emerald-500 to-emerald-600',
    blue: 'from-blue-500 to-blue-600',
    purple: 'from-purple-500 to-purple-600',
    amber: 'from-amber-500 to-amber-600',
    red: 'from-red-500 to-red-600',
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 border border-gray-200 dark:border-gray-700 hover:shadow-lg hover:-translate-y-0.5 transition-all duration-300">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-gray-500 dark:text-gray-400">{title}</p>
          <p className="text-3xl font-bold mt-2 text-gray-800 dark:text-white">
            {typeof value === 'number' ? value.toLocaleString() : value}
          </p>
          {trend && (
            <p className={`text-sm mt-2 flex items-center gap-1 ${trend.isPositive ? 'text-emerald-600' : 'text-red-500'}`}>
              {trend.isPositive ? '↑' : '↓'} {Math.abs(trend.value)}%
              <span className="text-gray-400 ml-1">vs hier</span>
            </p>
          )}
        </div>
        <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${colorClasses[color]} flex items-center justify-center text-white text-xl`}>
          {icon}
        </div>
      </div>
    </div>
  );
};

// Mini Bar Chart (simple)
const MiniBarChart: React.FC<{ data: TimeseriesPoint[] }> = ({ data }) => {
  const maxCount = Math.max(...data.map(d => d.count), 1);
  
  return (
    <div className="flex items-end gap-1 h-32">
      {data.slice(-14).map((point, i) => (
        <div key={i} className="flex-1 flex flex-col items-center gap-1">
          <div 
            className="w-full bg-emerald-500 dark:bg-emerald-400 rounded-t transition-all duration-300 hover:bg-emerald-600"
            style={{ height: `${(point.count / maxCount) * 100}%`, minHeight: '4px' }}
            title={`${point.date}: ${point.count} requêtes`}
          />
          {point.errors > 0 && (
            <div 
              className="w-full bg-red-400 rounded"
              style={{ height: `${(point.errors / maxCount) * 100}%`, minHeight: '2px' }}
              title={`${point.errors} erreurs`}
            />
          )}
          {i % 2 === 0 && (
            <span className="text-[10px] text-gray-400 mt-1">
              {new Date(point.date).getDate()}
            </span>
          )}
        </div>
      ))}
    </div>
  );
};

// Endpoint Distribution
const EndpointDistribution: React.FC<{ data: EndpointStat[] }> = ({ data }) => {
  const total = data.reduce((sum, d) => sum + d.count, 0) || 1;
  
  const colors = [
    'bg-emerald-500',
    'bg-blue-500',
    'bg-purple-500',
    'bg-amber-500',
    'bg-pink-500',
  ];
  
  return (
    <div className="space-y-3">
      {data.map((item, i) => {
        const percent = ((item.count / total) * 100).toFixed(1);
        const shortName = item.endpoint.split('/').pop() || item.endpoint;
        
        return (
          <div key={item.endpoint}>
            <div className="flex justify-between text-sm mb-1">
              <span className="text-gray-600 dark:text-gray-300 font-medium">
                {shortName}
              </span>
              <span className="text-gray-500">
                {item.count.toLocaleString()} ({percent}%)
              </span>
            </div>
            <div className="h-2 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden">
              <div 
                className={`h-full ${colors[i % colors.length]} rounded-full transition-all duration-500`}
                style={{ width: `${percent}%` }}
              />
            </div>
          </div>
        );
      })}
    </div>
  );
};

// Credits Progress
const CreditsProgress: React.FC<{ used: number; limit: number }> = ({ used, limit }) => {
  const percent = Math.min((used / limit) * 100, 100);
  const isWarning = percent > 80;
  
  return (
    <div>
      <div className="flex justify-between text-sm mb-2">
        <span className="text-gray-600 dark:text-gray-400">
          {used.toLocaleString()} / {limit.toLocaleString()} crédits
        </span>
        <span className={`font-medium ${isWarning ? 'text-amber-500' : 'text-emerald-500'}`}>
          {percent.toFixed(1)}%
        </span>
      </div>
      <div className="h-3 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden">
        <div 
          className={`h-full rounded-full transition-all duration-500 ${
            isWarning 
              ? 'bg-gradient-to-r from-amber-400 to-red-500' 
              : 'bg-gradient-to-r from-emerald-400 to-emerald-600'
          }`}
          style={{ width: `${percent}%` }}
        />
      </div>
      {isWarning && (
        <p className="text-amber-500 text-sm mt-2 flex items-center gap-1">
          ⚠️ Vous approchez de votre limite mensuelle
        </p>
      )}
    </div>
  );
};

/**
 * Composant Overview principal
 */
export const ApiOverview: React.FC = () => {
  const [stats, setStats] = useState<OverviewStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [timeseries, setTimeseries] = useState<TimeseriesPoint[]>([]);
  const [endpointStats, setEndpointStats] = useState<EndpointStat[]>([]);

  useEffect(() => {
    // Simuler le chargement des données
    const fetchData = async () => {
      setLoading(true);
      
      // TODO: Remplacer par appel API réel
      await new Promise(r => setTimeout(r, 500));
      
      // Données simulées
      setStats({
        requests_today: 1247,
        requests_30d: 34521,
        credits_consumed_month: 8450,
        errors_7d: 23,
        active_keys: 2,
        plan: 'Pro'
      });
      
      // Timeseries simulées (14 jours)
      const now = new Date();
      setTimeseries(
        Array.from({ length: 14 }, (_, i) => {
          const date = new Date(now);
          date.setDate(date.getDate() - (13 - i));
          return {
            date: date.toISOString().split('T')[0],
            count: Math.floor(Math.random() * 500) + 100,
            errors: Math.floor(Math.random() * 10)
          };
        })
      );
      
      // Stats par endpoint
      setEndpointStats([
        { endpoint: '/api/v1/rag/query', count: 15420 },
        { endpoint: '/api/v1/legal/ask', count: 8340 },
        { endpoint: '/api/v1/fiscal/simulate', count: 6210 },
        { endpoint: '/api/v1/park/sparkpage', count: 3120 },
        { endpoint: '/api/v1/fiscal/g50', count: 1431 },
      ]);
      
      setLoading(false);
    };
    
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin text-4xl">⚙️</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Welcome Banner */}
      <div className="bg-gradient-to-r from-emerald-500 to-purple-600 rounded-2xl p-6 text-white">
        <h2 className="text-2xl font-bold">Bienvenue sur votre Developer Dashboard 🚀</h2>
        <p className="mt-2 opacity-90">
          Gérez vos clés API, suivez votre consommation et testez les endpoints iaFactory.
        </p>
        <div className="mt-4 flex gap-3">
          <button className="px-4 py-2 bg-white text-emerald-600 rounded-lg font-medium hover:bg-gray-100 transition-colors">
            Créer une clé API
          </button>
          <button className="px-4 py-2 bg-white/20 text-white rounded-lg font-medium hover:bg-white/30 transition-colors">
            Voir la documentation
          </button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Requêtes aujourd'hui"
          value={stats?.requests_today || 0}
          icon="📊"
          color="emerald"
          trend={{ value: 12, isPositive: true }}
        />
        <StatCard
          title="Requêtes (30 jours)"
          value={stats?.requests_30d || 0}
          icon="📈"
          color="blue"
        />
        <StatCard
          title="Crédits consommés"
          value={stats?.credits_consumed_month || 0}
          icon="💰"
          color="purple"
        />
        <StatCard
          title="Erreurs (7 jours)"
          value={stats?.errors_7d || 0}
          icon="⚠️"
          color={stats?.errors_7d && stats.errors_7d > 50 ? 'red' : 'amber'}
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Requests Chart */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 border border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-bold text-gray-800 dark:text-white mb-4">
            📊 Requêtes (14 derniers jours)
          </h3>
          <MiniBarChart data={timeseries} />
          <div className="mt-4 flex items-center gap-4 text-sm">
            <span className="flex items-center gap-1">
              <span className="w-3 h-3 bg-emerald-500 rounded" />
              Requêtes
            </span>
            <span className="flex items-center gap-1">
              <span className="w-3 h-3 bg-red-400 rounded" />
              Erreurs
            </span>
          </div>
        </div>

        {/* Endpoint Distribution */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 border border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-bold text-gray-800 dark:text-white mb-4">
            🎯 Répartition par endpoint
          </h3>
          <EndpointDistribution data={endpointStats} />
        </div>
      </div>

      {/* Credits & Plan */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Credits Usage */}
        <div className="lg:col-span-2 bg-white dark:bg-gray-800 rounded-2xl p-6 border border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-bold text-gray-800 dark:text-white mb-4">
            💰 Consommation de crédits
          </h3>
          <CreditsProgress used={stats?.credits_consumed_month || 0} limit={10000} />
          <div className="mt-6 grid grid-cols-3 gap-4 text-center">
            <div>
              <p className="text-2xl font-bold text-gray-800 dark:text-white">1,550</p>
              <p className="text-sm text-gray-500">Restants</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-800 dark:text-white">~250</p>
              <p className="text-sm text-gray-500">Moy/jour</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-emerald-500">6 jours</p>
              <p className="text-sm text-gray-500">Avant limite</p>
            </div>
          </div>
        </div>

        {/* Current Plan */}
        <div className="bg-gradient-to-br from-purple-500 to-purple-700 rounded-2xl p-6 text-white">
          <div className="flex items-center gap-2 mb-4">
            <span className="text-2xl">⭐</span>
            <h3 className="text-lg font-bold">Plan {stats?.plan || 'Free'}</h3>
          </div>
          <ul className="space-y-2 text-sm opacity-90">
            <li>✓ 10,000 crédits/mois</li>
            <li>✓ 5 clés API</li>
            <li>✓ Support prioritaire</li>
            <li>✓ Logs 30 jours</li>
          </ul>
          <a 
            href="/pricing"
            className="mt-6 block w-full py-2 bg-white text-purple-600 rounded-lg font-medium text-center hover:bg-gray-100 transition-colors"
          >
            Voir tous les plans
          </a>
        </div>
      </div>

      {/* Quick Links */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <a 
          href="#keys"
          className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700 hover:border-emerald-500 transition-colors flex items-center gap-4"
        >
          <span className="text-3xl">🔑</span>
          <div>
            <p className="font-medium text-gray-800 dark:text-white">Gérer les clés API</p>
            <p className="text-sm text-gray-500">{stats?.active_keys} clé(s) active(s)</p>
          </div>
        </a>
        <a 
          href="#docs"
          className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700 hover:border-emerald-500 transition-colors flex items-center gap-4"
        >
          <span className="text-3xl">📚</span>
          <div>
            <p className="font-medium text-gray-800 dark:text-white">Documentation API</p>
            <p className="text-sm text-gray-500">Guides et références</p>
          </div>
        </a>
        <a 
          href="#playground"
          className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700 hover:border-emerald-500 transition-colors flex items-center gap-4"
        >
          <span className="text-3xl">🧪</span>
          <div>
            <p className="font-medium text-gray-800 dark:text-white">API Playground</p>
            <p className="text-sm text-gray-500">Tester les endpoints</p>
          </div>
        </a>
      </div>
    </div>
  );
};

export default ApiOverview;
