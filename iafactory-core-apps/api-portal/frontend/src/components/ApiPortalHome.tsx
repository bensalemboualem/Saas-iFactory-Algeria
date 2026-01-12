/**
 * iaFactory API Portal - Main Layout
 * Module 16 - Dashboard développeur façon OpenAI/Stripe
 */

import React, { useState } from 'react';
import { ApiOverview } from './ApiOverview';
import { ApiKeysManager } from './ApiKeysManager';
import { ApiUsageOverview } from './ApiUsageOverview';
import { ApiLogsTable } from './ApiLogsTable';
import { ApiDocsPlayground } from './ApiDocsPlayground';

// Types
type TabId = 'overview' | 'keys' | 'usage' | 'logs' | 'docs';

interface Tab {
  id: TabId;
  label: string;
  icon: string;
  description: string;
}

// Configuration des onglets
const TABS: Tab[] = [
  { id: 'overview', label: 'Overview', icon: '📊', description: "Vue d'ensemble" },
  { id: 'keys', label: 'API Keys', icon: '🔑', description: 'Gérer vos clés' },
  { id: 'usage', label: 'Usage', icon: '📈', description: 'Statistiques' },
  { id: 'logs', label: 'Logs', icon: '📋', description: 'Historique' },
  { id: 'docs', label: 'Docs & Playground', icon: '📚', description: 'Documentation & Test' },
];

/**
 * Composant principal du Developer Portal
 */
export const ApiPortalHome: React.FC = () => {
  const [activeTab, setActiveTab] = useState<TabId>('overview');
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  // Rendu du contenu selon l'onglet actif
  const renderContent = () => {
    switch (activeTab) {
      case 'overview':
        return <ApiOverview />;
      case 'keys':
        return <ApiKeysManager />;
      case 'usage':
        return <ApiUsageOverview />;
      case 'logs':
        return <ApiLogsTable />;
      case 'docs':
        return <ApiDocsPlayground />;
      default:
        return <ApiOverview />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex">
      {/* Sidebar */}
      <aside 
        className={`
          ${sidebarCollapsed ? 'w-16' : 'w-64'} 
          bg-white dark:bg-gray-800 
          border-r border-gray-200 dark:border-gray-700
          flex flex-col
          transition-all duration-300
          fixed h-full z-40
          lg:relative
        `}
      >
        {/* Logo & Toggle */}
        <div className="h-16 flex items-center justify-between px-4 border-b border-gray-200 dark:border-gray-700">
          {!sidebarCollapsed && (
            <div className="flex items-center gap-2">
              <span className="text-2xl">🚀</span>
              <span className="font-bold text-lg bg-gradient-to-r from-emerald-500 to-purple-500 bg-clip-text text-transparent">
                Developer Portal
              </span>
            </div>
          )}
          <button
            onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
            className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            title={sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
          >
            {sidebarCollapsed ? '→' : '←'}
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 py-4 px-2 space-y-1">
          {TABS.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`
                w-full flex items-center gap-3 px-3 py-3 rounded-xl
                transition-all duration-200
                ${activeTab === tab.id
                  ? 'bg-emerald-50 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400 shadow-sm'
                  : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700/50'
                }
              `}
            >
              <span className="text-xl">{tab.icon}</span>
              {!sidebarCollapsed && (
                <div className="flex flex-col items-start">
                  <span className="font-medium">{tab.label}</span>
                  <span className="text-xs opacity-70">{tab.description}</span>
                </div>
              )}
            </button>
          ))}
        </nav>

        {/* Footer Sidebar */}
        {!sidebarCollapsed && (
          <div className="p-4 border-t border-gray-200 dark:border-gray-700">
            <div className="bg-gradient-to-r from-emerald-500/10 to-purple-500/10 rounded-xl p-4">
              <p className="text-sm font-medium text-gray-700 dark:text-gray-300">
                Plan actuel
              </p>
              <p className="text-lg font-bold text-emerald-600 dark:text-emerald-400">
                Free Tier
              </p>
              <a 
                href="/pricing" 
                className="text-sm text-purple-600 dark:text-purple-400 hover:underline mt-2 inline-block"
              >
                Voir les plans →
              </a>
            </div>
          </div>
        )}
      </aside>

      {/* Main Content */}
      <main className={`flex-1 ${sidebarCollapsed ? 'lg:ml-16' : 'lg:ml-64'} transition-all duration-300`}>
        {/* Top Bar */}
        <header className="h-16 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between px-6 sticky top-0 z-30">
          <div>
            <h1 className="text-xl font-bold text-gray-800 dark:text-white">
              {TABS.find(t => t.id === activeTab)?.icon} {TABS.find(t => t.id === activeTab)?.label}
            </h1>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              {TABS.find(t => t.id === activeTab)?.description}
            </p>
          </div>
          
          <div className="flex items-center gap-4">
            {/* Quick Stats */}
            <div className="hidden md:flex items-center gap-2 px-3 py-1.5 bg-emerald-50 dark:bg-emerald-900/30 rounded-lg">
              <span className="text-emerald-600 dark:text-emerald-400 font-medium">
                🔑 2 clés actives
              </span>
            </div>
            
            {/* Docs Link */}
            <a 
              href="https://docs.iafactoryalgeria.com"
              target="_blank"
              rel="noopener noreferrer"
              className="px-4 py-2 text-sm font-medium text-gray-600 dark:text-gray-300 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors"
            >
              📖 Documentation
            </a>
            
            {/* Profile */}
            <button className="w-10 h-10 bg-gradient-to-br from-emerald-500 to-purple-500 rounded-full flex items-center justify-center text-white font-bold">
              U
            </button>
          </div>
        </header>

        {/* Content Area */}
        <div className="p-6">
          {renderContent()}
        </div>
      </main>
    </div>
  );
};

export default ApiPortalHome;
