import { useState, useEffect } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';
import { Line, Bar, Doughnut } from 'react-chartjs-2';
import {
  LayoutDashboard, Bot, Workflow, Users, Settings, BarChart3,
  MessageSquare, Zap, Globe, Activity, Server, Database,
  Menu, X, ChevronRight, TrendingUp, TrendingDown,
  Clock, CheckCircle, AlertTriangle, XCircle, RefreshCw,
  Download, Filter, ArrowUpRight, ArrowDownRight,
} from 'lucide-react';
import IAFHeader from './components/IAFHeader';
import IAFFooter from './components/IAFFooter';
import './index.css';

// Register Chart.js components
ChartJS.register(
  CategoryScale, LinearScale, PointElement, LineElement,
  BarElement, ArcElement, Title, Tooltip, Legend, Filler
);

// ==================== I18N ====================
type Lang = 'fr' | 'en' | 'ar';

const translations: Record<string, Record<Lang, string>> = {
  dashboard: { fr: 'Tableau de bord', en: 'Dashboard', ar: 'لوحة القيادة' },
  dashboardSubtitle: { fr: 'Vue d\'ensemble de votre plateforme IA', en: 'Overview of your AI platform', ar: 'نظرة عامة على منصة الذكاء الاصطناعي' },
  applications: { fr: 'Applications', en: 'Applications', ar: 'التطبيقات' },
  agents: { fr: 'Agents IA', en: 'AI Agents', ar: 'وكلاء الذكاء الاصطناعي' },
  workflows: { fr: 'Workflows', en: 'Workflows', ar: 'سير العمل' },
  analytics: { fr: 'Analytiques', en: 'Analytics', ar: 'التحليلات' },
  users: { fr: 'Utilisateurs', en: 'Users', ar: 'المستخدمون' },
  settings: { fr: 'Paramètres', en: 'Settings', ar: 'الإعدادات' },
  search: { fr: 'Rechercher...', en: 'Search...', ar: 'بحث...' },
  totalUsers: { fr: 'Utilisateurs totaux', en: 'Total Users', ar: 'إجمالي المستخدمين' },
  activeAgents: { fr: 'Agents actifs', en: 'Active Agents', ar: 'الوكلاء النشطون' },
  conversations: { fr: 'Conversations', en: 'Conversations', ar: 'المحادثات' },
  apiCalls: { fr: 'Appels API', en: 'API Calls', ar: 'استدعاءات API' },
  revenue: { fr: 'Revenus', en: 'Revenue', ar: 'الإيرادات' },
  viewAll: { fr: 'Voir tout', en: 'View all', ar: 'عرض الكل' },
  quickActions: { fr: 'Actions rapides', en: 'Quick Actions', ar: 'إجراءات سريعة' },
  newAgent: { fr: 'Nouvel Agent', en: 'New Agent', ar: 'وكيل جديد' },
  newWorkflow: { fr: 'Nouveau Workflow', en: 'New Workflow', ar: 'سير عمل جديد' },
  systemStatus: { fr: 'État du système', en: 'System Status', ar: 'حالة النظام' },
  healthy: { fr: 'Opérationnel', en: 'Healthy', ar: 'سليم' },
  warning: { fr: 'Attention', en: 'Warning', ar: 'تحذير' },
  error: { fr: 'Erreur', en: 'Error', ar: 'خطأ' },
  online: { fr: 'En ligne', en: 'Online', ar: 'متصل' },
  offline: { fr: 'Hors ligne', en: 'Offline', ar: 'غير متصل' },
  active: { fr: 'Actif', en: 'Active', ar: 'نشط' },
  idle: { fr: 'Inactif', en: 'Idle', ar: 'خامل' },
  trafficOverview: { fr: 'Aperçu du trafic', en: 'Traffic Overview', ar: 'نظرة عامة على حركة المرور' },
  appUsage: { fr: 'Utilisation par app', en: 'App Usage', ar: 'استخدام التطبيقات' },
  agentPerformance: { fr: 'Performance agents', en: 'Agent Performance', ar: 'أداء الوكلاء' },
  recentActivity: { fr: 'Activité récente', en: 'Recent Activity', ar: 'النشاط الأخير' },
  topApplications: { fr: 'Top Applications', en: 'Top Applications', ar: 'أفضل التطبيقات' },
  agentsTable: { fr: 'Tableau des agents', en: 'Agents Table', ar: 'جدول الوكلاء' },
  name: { fr: 'Nom', en: 'Name', ar: 'الاسم' },
  type: { fr: 'Type', en: 'Type', ar: 'النوع' },
  status: { fr: 'Statut', en: 'Status', ar: 'الحالة' },
  tasks: { fr: 'Tâches', en: 'Tasks', ar: 'المهام' },
  lastActive: { fr: 'Dernière activité', en: 'Last Active', ar: 'آخر نشاط' },
  actions: { fr: 'Actions', en: 'Actions', ar: 'الإجراءات' },
  requests: { fr: 'Requêtes', en: 'Requests', ar: 'الطلبات' },
  thisWeek: { fr: 'Cette semaine', en: 'This week', ar: 'هذا الأسبوع' },
  thisMonth: { fr: 'Ce mois', en: 'This month', ar: 'هذا الشهر' },
  vsLastWeek: { fr: 'vs semaine dernière', en: 'vs last week', ar: 'مقارنة بالأسبوع الماضي' },
  refresh: { fr: 'Actualiser', en: 'Refresh', ar: 'تحديث' },
  export: { fr: 'Exporter', en: 'Export', ar: 'تصدير' },
  filter: { fr: 'Filtrer', en: 'Filter', ar: 'تصفية' },
  jan: { fr: 'Jan', en: 'Jan', ar: 'يناير' },
  feb: { fr: 'Fév', en: 'Feb', ar: 'فبراير' },
  mar: { fr: 'Mar', en: 'Mar', ar: 'مارس' },
  apr: { fr: 'Avr', en: 'Apr', ar: 'أبريل' },
  may: { fr: 'Mai', en: 'May', ar: 'مايو' },
  jun: { fr: 'Juin', en: 'Jun', ar: 'يونيو' },
  jul: { fr: 'Juil', en: 'Jul', ar: 'يوليو' },
  legalAssistant: { fr: 'Assistant Juridique', en: 'Legal Assistant', ar: 'المساعد القانوني' },
  fiscalAssistant: { fr: 'Assistant Fiscal', en: 'Fiscal Assistant', ar: 'المساعد الضريبي' },
  agriAssistant: { fr: 'Assistant Agricole', en: 'Agricultural Assistant', ar: 'المساعد الزراعي' },
  crmApp: { fr: 'CRM IAFactory', en: 'IAFactory CRM', ar: 'CRM IAFactory' },
  cvBuilder: { fr: 'CV Builder', en: 'CV Builder', ar: 'منشئ السيرة الذاتية' },
  pricing: { fr: 'Tarifs', en: 'Pricing', ar: 'الأسعار' },
  login: { fr: 'Connexion', en: 'Log in', ar: 'تسجيل الدخول' },
  getStarted: { fr: 'Commencer', en: 'Get Started', ar: 'ابدأ الآن' },
  copyright: { fr: '© 2025 IAFactory Algeria. Tous droits réservés.', en: '© 2025 IAFactory Algeria. All rights reserved.', ar: '© 2025 IAFactory الجزائر. جميع الحقوق محفوظة.' },
  madeWith: { fr: 'Fait avec ❤️ pour l\'Algérie', en: 'Made with ❤️ for Algeria', ar: 'صنع بـ ❤️ للجزائر' },
  products: { fr: 'Produits', en: 'Products', ar: 'المنتجات' },
  resources: { fr: 'Ressources', en: 'Resources', ar: 'الموارد' },
  company: { fr: 'Entreprise', en: 'Company', ar: 'الشركة' },
  legal: { fr: 'Légal', en: 'Legal', ar: 'قانوني' },
  about: { fr: 'À propos', en: 'About', ar: 'حول' },
  contact: { fr: 'Contact', en: 'Contact', ar: 'اتصل بنا' },
  documentation: { fr: 'Documentation', en: 'Documentation', ar: 'التوثيق' },
  privacy: { fr: 'Confidentialité', en: 'Privacy', ar: 'الخصوصية' },
  terms: { fr: 'CGU', en: 'Terms', ar: 'الشروط' },
  location: { fr: 'Alger, Algérie', en: 'Algiers, Algeria', ar: 'الجزائر العاصمة' },
};

const getLang = (): Lang => (localStorage.getItem('cockpit_lang') as Lang) || 'fr';
const setLangStorage = (lang: Lang) => localStorage.setItem('cockpit_lang', lang);
const t = (key: string, lang: Lang): string => translations[key]?.[lang] || key;

// ==================== THEME ====================
const getTheme = (): 'dark' | 'light' => (localStorage.getItem('cockpit_theme') as 'dark' | 'light') || 'dark';
const setThemeStorage = (theme: 'dark' | 'light') => localStorage.setItem('cockpit_theme', theme);

// ==================== MAIN APP ====================
export default function App() {
  const [lang, setLang] = useState<Lang>(getLang);
  const [theme, setTheme] = useState<'dark' | 'light'>(getTheme);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('dashboard');

  const isRtl = lang === 'ar';

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    document.documentElement.setAttribute('dir', isRtl ? 'rtl' : 'ltr');
    document.documentElement.setAttribute('lang', lang);
  }, [theme, lang, isRtl]);

  const _handleLangChange = (newLang: Lang) => {
    setLang(newLang);
    setLangStorage(newLang);
  };
  void _handleLangChange; // Suppress unused warning

  const _handleThemeToggle = () => {
    const newTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
    setThemeStorage(newTheme);
  };
  void _handleThemeToggle; // Suppress unused warning

  // Chart data
  const months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul'].map(m => t(m, lang));

  const trafficData = {
    labels: months,
    datasets: [
      {
        label: t('apiCalls', lang),
        data: [65000, 78000, 90000, 81000, 95000, 110000, 125000],
        borderColor: '#00a651',
        backgroundColor: 'rgba(0, 166, 81, 0.1)',
        fill: true,
        tension: 0.4,
      },
      {
        label: t('conversations', lang),
        data: [28000, 35000, 42000, 38000, 48000, 55000, 62000],
        borderColor: '#3b82f6',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        fill: true,
        tension: 0.4,
      },
    ],
  };

  const appUsageData = {
    labels: [t('legalAssistant', lang), t('fiscalAssistant', lang), t('agriAssistant', lang), t('crmApp', lang), t('cvBuilder', lang)],
    datasets: [{
      data: [35, 25, 20, 12, 8],
      backgroundColor: ['#00a651', '#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6'],
      borderWidth: 0,
    }],
  };

  const agentPerformanceData = {
    labels: months,
    datasets: [
      {
        label: t('tasks', lang),
        data: [420, 580, 650, 720, 890, 950, 1100],
        backgroundColor: '#00a651',
        borderRadius: 8,
      },
    ],
  };

  const stats = [
    { icon: <Users className="w-6 h-6" />, label: t('totalUsers', lang), value: '12,847', change: '+18.2%', positive: true, subtext: t('thisMonth', lang) },
    { icon: <Bot className="w-6 h-6" />, label: t('activeAgents', lang), value: '56', change: '+8', positive: true, subtext: t('thisWeek', lang) },
    { icon: <MessageSquare className="w-6 h-6" />, label: t('conversations', lang), value: '284,521', change: '+32.5%', positive: true, subtext: t('thisMonth', lang) },
    { icon: <Zap className="w-6 h-6" />, label: t('apiCalls', lang), value: '4.2M', change: '-2.1%', positive: false, subtext: t('thisWeek', lang) },
  ];

  const apps = [
    { name: t('legalAssistant', lang), status: 'online', users: 3245, requests: '1.2M', growth: 15.2 },
    { name: t('fiscalAssistant', lang), status: 'online', users: 2189, requests: '890K', growth: 22.8 },
    { name: t('agriAssistant', lang), status: 'warning', users: 1567, requests: '456K', growth: -3.2 },
    { name: t('crmApp', lang), status: 'online', users: 892, requests: '234K', growth: 8.5 },
    { name: t('cvBuilder', lang), status: 'online', users: 654, requests: '123K', growth: 45.2 },
  ];

  const agents = [
    { name: 'Dzir Legal Pro', type: 'RAG', status: 'active', tasks: 15234, lastActive: '2 min' },
    { name: 'Fiscal Expert DZ', type: 'RAG', status: 'active', tasks: 8921, lastActive: '5 min' },
    { name: 'Agri Assistant', type: 'Multi-Agent', status: 'idle', tasks: 4521, lastActive: '1h' },
    { name: 'Support Bot', type: 'Chat', status: 'active', tasks: 12453, lastActive: '1 min' },
    { name: 'Data Analyzer', type: 'Tool', status: 'error', tasks: 234, lastActive: '2h' },
  ];

  const menuItems = [
    { id: 'dashboard', icon: <LayoutDashboard className="w-5 h-5" />, label: t('dashboard', lang) },
    { id: 'apps', icon: <Globe className="w-5 h-5" />, label: t('applications', lang) },
    { id: 'agents', icon: <Bot className="w-5 h-5" />, label: t('agents', lang) },
    { id: 'workflows', icon: <Workflow className="w-5 h-5" />, label: t('workflows', lang) },
    { id: 'analytics', icon: <BarChart3 className="w-5 h-5" />, label: t('analytics', lang) },
    { id: 'users', icon: <Users className="w-5 h-5" />, label: t('users', lang) },
    { id: 'settings', icon: <Settings className="w-5 h-5" />, label: t('settings', lang) },
  ];

  const systemStatus = [
    { name: 'API Gateway', status: 'healthy', icon: <Activity className="w-4 h-4" /> },
    { name: 'Vector DB', status: 'healthy', icon: <Database className="w-4 h-4" /> },
    { name: 'LLM Service', status: 'warning', icon: <Server className="w-4 h-4" /> },
    { name: 'CDN', status: 'healthy', icon: <Globe className="w-4 h-4" /> },
  ];

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy': case 'online': case 'active': return <CheckCircle className="w-4 h-4 text-green-500" />;
      case 'warning': case 'idle': return <AlertTriangle className="w-4 h-4 text-yellow-500" />;
      case 'error': case 'offline': return <XCircle className="w-4 h-4 text-red-500" />;
      default: return <Clock className="w-4 h-4 text-gray-500" />;
    }
  };

  const getStatusClass = (status: string) => {
    switch (status) {
      case 'healthy': case 'online': case 'active': return 'status-healthy';
      case 'warning': case 'idle': return 'status-warning';
      case 'error': case 'offline': return 'status-error';
      default: return '';
    }
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: true, position: 'top' as const, labels: { color: theme === 'dark' ? '#94a3b8' : '#64748b', font: { size: 12 } } },
    },
    scales: {
      x: { grid: { color: theme === 'dark' ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.05)' }, ticks: { color: theme === 'dark' ? '#94a3b8' : '#64748b' } },
      y: { grid: { color: theme === 'dark' ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.05)' }, ticks: { color: theme === 'dark' ? '#94a3b8' : '#64748b' } },
    },
  };

  return (
    <div className="app-container" dir={isRtl ? 'rtl' : 'ltr'}>
      {/* ==================== HEADER ==================== */}
      <IAFHeader lang={lang} />

      <div className="main-layout">
        {/* ==================== SIDEBAR ==================== */}
        <aside className={`sidebar ${sidebarOpen ? 'expanded' : 'collapsed'}`}>
          <div className="sidebar-header">
            <button onClick={() => setSidebarOpen(!sidebarOpen)} className="sidebar-toggle">
              <Menu className="w-5 h-5" />
            </button>
          </div>

          <nav className="sidebar-nav">
            {menuItems.map((item) => (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`sidebar-link ${activeTab === item.id ? 'active' : ''}`}
              >
                {item.icon}
                {sidebarOpen && <span>{item.label}</span>}
              </button>
            ))}
          </nav>

          <div className="sidebar-footer">
            <div className="user-info">
              <div className="user-avatar-sm">A</div>
              {sidebarOpen && (
                <div className="user-details">
                  <span className="user-name">Admin</span>
                  <span className="user-email">admin@iafactory.dz</span>
                </div>
              )}
            </div>
          </div>
        </aside>

        {/* ==================== MOBILE MENU ==================== */}
        {mobileMenuOpen && (
          <div className="mobile-overlay" onClick={() => setMobileMenuOpen(false)}>
            <div className="mobile-menu" onClick={(e) => e.stopPropagation()}>
              <div className="mobile-menu-header">
                <span className="logo-text">IAFactory</span>
                <button onClick={() => setMobileMenuOpen(false)}><X className="w-6 h-6" /></button>
              </div>
              <nav className="mobile-nav">
                {menuItems.map((item) => (
                  <button key={item.id} onClick={() => { setActiveTab(item.id); setMobileMenuOpen(false); }} className={`mobile-link ${activeTab === item.id ? 'active' : ''}`}>
                    {item.icon}
                    <span>{item.label}</span>
                  </button>
                ))}
              </nav>
            </div>
          </div>
        )}

        {/* ==================== MAIN CONTENT ==================== */}
        <main className="main-content">
          {/* Page Header */}
          <div className="page-header">
            <div className="page-header-left">
              <h1 className="page-title">{t('dashboard', lang)}</h1>
              <p className="page-subtitle">{t('dashboardSubtitle', lang)}</p>
            </div>
            <div className="page-header-right">
              <button className="btn btn-secondary"><Filter className="w-4 h-4" />{t('filter', lang)}</button>
              <button className="btn btn-secondary"><Download className="w-4 h-4" />{t('export', lang)}</button>
              <button className="btn btn-primary"><RefreshCw className="w-4 h-4" />{t('refresh', lang)}</button>
            </div>
          </div>

          {/* Stats Grid */}
          <div className="stats-grid">
            {stats.map((stat, i) => (
              <div key={i} className="stat-card">
                <div className="stat-header">
                  <div className="stat-icon">{stat.icon}</div>
                  <div className={`stat-change ${stat.positive ? 'positive' : 'negative'}`}>
                    {stat.positive ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
                    {stat.change}
                  </div>
                </div>
                <div className="stat-value">{stat.value}</div>
                <div className="stat-label">{stat.label}</div>
                <div className="stat-subtext">{stat.subtext}</div>
              </div>
            ))}
          </div>

          {/* Charts Row */}
          <div className="charts-row">
            <div className="chart-card large">
              <div className="chart-header">
                <h3 className="chart-title">{t('trafficOverview', lang)}</h3>
                <div className="chart-actions">
                  <button className="chart-period active">{t('thisWeek', lang)}</button>
                  <button className="chart-period">{t('thisMonth', lang)}</button>
                </div>
              </div>
              <div className="chart-body">
                <Line data={trafficData} options={chartOptions} />
              </div>
            </div>

            <div className="chart-card">
              <div className="chart-header">
                <h3 className="chart-title">{t('appUsage', lang)}</h3>
              </div>
              <div className="chart-body doughnut">
                <Doughnut data={appUsageData} options={{ ...chartOptions, cutout: '70%' }} />
              </div>
            </div>
          </div>

          {/* Second Row */}
          <div className="charts-row">
            <div className="chart-card">
              <div className="chart-header">
                <h3 className="chart-title">{t('agentPerformance', lang)}</h3>
              </div>
              <div className="chart-body">
                <Bar data={agentPerformanceData} options={chartOptions} />
              </div>
            </div>

            <div className="chart-card">
              <div className="chart-header">
                <h3 className="chart-title">{t('systemStatus', lang)}</h3>
              </div>
              <div className="system-status-list">
                {systemStatus.map((sys, i) => (
                  <div key={i} className="system-status-item">
                    <div className="system-info">
                      <span className="system-icon">{sys.icon}</span>
                      <span className="system-name">{sys.name}</span>
                    </div>
                    <span className={`status-badge ${getStatusClass(sys.status)}`}>
                      {getStatusIcon(sys.status)}
                      {t(sys.status, lang)}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Data Tables */}
          <div className="tables-row">
            {/* Applications Table */}
            <div className="table-card">
              <div className="table-header">
                <h3 className="table-title">{t('topApplications', lang)}</h3>
                <button className="view-all-btn">{t('viewAll', lang)} <ChevronRight className="w-4 h-4" /></button>
              </div>
              <div className="table-wrapper">
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>{t('name', lang)}</th>
                      <th>{t('status', lang)}</th>
                      <th>{t('users', lang)}</th>
                      <th>{t('requests', lang)}</th>
                      <th>Growth</th>
                    </tr>
                  </thead>
                  <tbody>
                    {apps.map((app, i) => (
                      <tr key={i}>
                        <td className="app-name-cell">
                          <div className="app-icon-sm"><Globe className="w-4 h-4" /></div>
                          {app.name}
                        </td>
                        <td><span className={`status-badge ${getStatusClass(app.status)}`}>{getStatusIcon(app.status)} {t(app.status, lang)}</span></td>
                        <td>{app.users.toLocaleString()}</td>
                        <td>{app.requests}</td>
                        <td className={app.growth >= 0 ? 'positive' : 'negative'}>
                          {app.growth >= 0 ? <ArrowUpRight className="w-4 h-4" /> : <ArrowDownRight className="w-4 h-4" />}
                          {Math.abs(app.growth)}%
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Agents Table */}
            <div className="table-card">
              <div className="table-header">
                <h3 className="table-title">{t('agentsTable', lang)}</h3>
                <button className="view-all-btn">{t('viewAll', lang)} <ChevronRight className="w-4 h-4" /></button>
              </div>
              <div className="table-wrapper">
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>{t('name', lang)}</th>
                      <th>{t('type', lang)}</th>
                      <th>{t('status', lang)}</th>
                      <th>{t('tasks', lang)}</th>
                      <th>{t('lastActive', lang)}</th>
                    </tr>
                  </thead>
                  <tbody>
                    {agents.map((agent, i) => (
                      <tr key={i}>
                        <td className="agent-name-cell">
                          <div className="agent-icon-sm"><Bot className="w-4 h-4" /></div>
                          {agent.name}
                        </td>
                        <td><span className="type-badge">{agent.type}</span></td>
                        <td><span className={`status-badge ${getStatusClass(agent.status)}`}>{getStatusIcon(agent.status)} {t(agent.status, lang)}</span></td>
                        <td>{agent.tasks.toLocaleString()}</td>
                        <td className="last-active">{agent.lastActive}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </main>
      </div>

      {/* ==================== FOOTER ==================== */}
      <IAFFooter lang={lang} />
    </div>
  );
}
