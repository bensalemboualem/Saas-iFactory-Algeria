import { useState, useEffect } from 'react';
import './App.css';
import './styles/ithy-presentation.css';
import './styles/iafactory-unified.css';
import './styles/iafactory-components.css';
import { IthyStyleRenderer } from './components/presentation';
import { BigRAGChat } from './components/ia';
import { AppHeader, AppFooter, HelpChatbot, Sidebar } from './components/layout';
import type { IthyResponseProps } from './components/presentation';

// Correction : Fonction intégrée pour remplacer l'import manquant
const transformToIthyFormat = (data: any): any => {
  return {
    query: data.query || "",
    answer: data.answer || "",
    sources: data.sources || [],
    chunks: data.chunks || [],
    confidence: data.confidence || 0.75
  };
};

const API_URL = import.meta.env.VITE_API_URL || (window.location.origin.includes('localhost') ? 'http://localhost:8180' : '');
const API_KEY = import.meta.env.VITE_API_KEY || (window.location.origin.includes('localhost') ? 'ragdz_dev_demo_key_12345678901234567890' : '9b793e7f8dc29d64c7b655217a196ddc5831e0df5584c8f1ada3d43de44a5f46');

type SourceType = 'file' | 'url';

interface Message {
  role: string;
  content: string;
  rawData?: any; 
  ithyData?: IthyResponseProps; 
}

export default function App() {
  const [sourceType, setSourceType] = useState<SourceType>('file');
  const [file, setFile] = useState<File | null>(null);
  const [url, setUrl] = useState('');
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState<Array<Message>>([]);
  const [loading, setLoading] = useState(false);
  const [ithyMode, setIthyMode] = useState(true); 
  const [viewMode, setViewMode] = useState<'classic' | 'bigrag'>('bigrag'); 

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await fetch(`${API_URL}/api/upload`, {
        method: 'POST',
        headers: { 'X-API-Key': API_KEY },
        body: formData
      });
      const data = await res.json();
      setMessages(prev => [...prev, {
        role: 'system',
        content: `✅ Document uploadé: ${data.filename} (${data.chunks_created} chunks)`
      }]);
      setFile(null);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'system', content: `❌ Erreur: ${error}` }]);
    } finally {
      setLoading(false);
    }
  };

  const handleUploadFromURL = async () => {
    if (!url.trim()) return;
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/api/upload-url`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-API-Key': API_KEY },
        body: JSON.stringify({ url: url.trim() })
      });
      const data = await res.json();
      if (data.error) {
        setMessages(prev => [...prev, { role: 'system', content: `❌ Erreur: ${data.error}` }]);
      } else {
        setMessages(prev => [...prev, {
          role: 'system',
          content: `✅ Contenu extrait de l'URL: ${data.source_type} (${data.chunks_created} chunks)`
        }]);
        setUrl('');
      }
    } catch (error) {
      setMessages(prev => [...prev, { role: 'system', content: `❌ Erreur: ${error}` }]);
    } finally {
      setLoading(false);
    }
  };

  const handleQuery = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    const userMessage = query;
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setQuery('');
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/api/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-API-Key': API_KEY },
        body: JSON.stringify({ query: userMessage, max_results: 5, use_llm: true })
      });
      const data = await res.json();
      let ithyData: IthyResponseProps | undefined;
      if (ithyMode && data.answer) {
        try {
          ithyData = transformToIthyFormat({
            query: userMessage,
            answer: data.answer,
            sources: data.sources || [],
            chunks: data.results || [],
            confidence: data.confidence || 0.75
          });
        } catch (err) {
          console.error('Erreur transformation ithy:', err);
        }
      }
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: data.answer || data.results?.map((r: any) => r.text).join('\n\n') || 'Aucun résultat',
        rawData: data,
        ithyData
      }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'system', content: `❌ Erreur: ${error}` }]);
    } finally {
      setLoading(false);
    }
  };

  const handleSendToBMAD = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/api/orchestrator/workflow`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-API-Key': API_KEY },
        body: JSON.stringify({
          task: 'create_project',
          description: messages.filter(m => m.role === 'user').map(m => m.content).join('\n'),
          target: 'bolt'
        })
      });
      const data = await res.json();
      setMessages(prev => [...prev, { role: 'system', content: `🤖 BMAD Workflow lancé: ${data.workflow_id}` }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'system', content: `❌ Erreur BMAD: ${error}` }]);
    } finally {
      setLoading(false);
    }
  };

  // Initialize theme - sync with IAFactory landing page
  useEffect(() => {
    const savedTheme = localStorage.getItem('iafactory_theme') || 'dark';
    // Apply to both body and html for consistency with landing page
    document.body.setAttribute('data-theme', savedTheme);
    document.documentElement.setAttribute('data-theme', savedTheme);
    // Also toggle .dark class for Tailwind
    if (savedTheme === 'dark') {
      document.body.classList.add('dark');
      document.documentElement.classList.add('dark');
    } else {
      document.body.classList.remove('dark');
      document.documentElement.classList.remove('dark');
    }
  }, []);

  return (
    <div className="app" style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', background: 'var(--bg)' }}>
      {/* Sidebar */}
      <Sidebar />

      {/* Unified Header */}
      <AppHeader />

      {/* Main Content - with padding for fixed header and sidebar */}
      <main style={{
        paddingTop: 'var(--iaf-header-height, 60px)',
        paddingLeft: 'var(--iaf-sidebar-width-collapsed, 60px)',
        flex: 1,
        transition: 'padding-left var(--iaf-sidebar-transition, 250ms)',
        background: 'var(--bg)'
      }}>

      {/* View Mode Toggle */}
      <div style={{ display: 'flex', justifyContent: 'center', padding: '1rem', gap: '8px' }}>
        <button
          onClick={() => setViewMode('bigrag')}
          style={{
            padding: '10px 20px',
            borderRadius: '8px',
            border: 'none',
            background: viewMode === 'bigrag' ? 'var(--iaf-green)' : 'rgba(255,255,255,0.1)',
            color: viewMode === 'bigrag' ? 'white' : 'var(--iaf-text-secondary)',
            cursor: 'pointer',
            fontWeight: 600,
            transition: 'all 0.3s'
          }}
        >
          🤖 BIG RAG
        </button>
        <button
          onClick={() => setViewMode('classic')}
          style={{
            padding: '10px 20px',
            borderRadius: '8px',
            border: 'none',
            background: viewMode === 'classic' ? 'var(--iaf-green)' : 'rgba(255,255,255,0.1)',
            color: viewMode === 'classic' ? 'white' : 'var(--iaf-text-secondary)',
            cursor: 'pointer',
            fontWeight: 600,
            transition: 'all 0.3s'
          }}
        >
          📤 Upload
        </button>
        <a
          href={`${API_URL}/docs`}
          target="_blank"
          rel="noopener noreferrer"
          style={{
            padding: '10px 20px',
            borderRadius: '8px',
            background: 'rgba(255,255,255,0.05)',
            color: 'var(--iaf-green)',
            textDecoration: 'none',
            fontWeight: 500,
            border: '1px solid var(--iaf-border)',
            transition: 'all 0.3s'
          }}
        >
          📚 API Docs
        </a>
      </div>

      {viewMode === 'bigrag' && (
        <div style={{ height: 'calc(100vh - 140px)', padding: '1rem', background: 'var(--bg)' }}>
          <BigRAGChat defaultCountry="DZ" enableVoice={false} />
        </div>
      )}

      {viewMode === 'classic' && (
      <div className="container" style={{ background: 'var(--bg)' }}>
        <div className="upload-section">
          <h2>📤 Ajouter une Source</h2>
          <div className="source-toggle">
            <button className={sourceType === 'file' ? 'active' : ''} onClick={() => setSourceType('file')}>📁 Fichier</button>
            <button className={sourceType === 'url' ? 'active' : ''} onClick={() => setSourceType('url')}>🔗 URL</button>
          </div>
          {sourceType === 'file' && (
            <div className="file-upload">
              <input type="file" onChange={(e) => setFile(e.target.files?.[0] || null)} accept=".txt,.pdf,.docx,.md,.csv,.xlsx,.xls" />
              {file && <button onClick={handleUpload}>Uploader {file.name}</button>}
            </div>
          )}
          {sourceType === 'url' && (
            <div className="url-upload">
              <input type="url" value={url} onChange={(e) => setUrl(e.target.value)} placeholder="URL YouTube ou site..." />
              <button onClick={handleUploadFromURL}>Extraire</button>
            </div>
          )}
        </div>

        <div className="chat-section">
          <div className="chat-header">
            <h2>💬 RAG Chatbot</h2>
            <label><input type="checkbox" checked={ithyMode} onChange={(e) => setIthyMode(e.target.checked)} />🎨 Mode Ithy</label>
          </div>
          <div className="messages">
            {messages.map((msg, i) => (
              <div key={i} className={`message ${msg.role}`}>
                {msg.role === 'assistant' && msg.ithyData && ithyMode ? (
                  <IthyStyleRenderer {...msg.ithyData} />
                ) : (
                  <p>{msg.content}</p>
                )}
              </div>
            ))}
          </div>
          <form onSubmit={handleQuery} className="query-form">
            <input type="text" value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Votre question..." />
            <button type="submit">Envoyer</button>
          </form>
        </div>
      </div>
      )}

      </main>

      {/* Unified Footer */}
      <AppFooter />

      {/* Help Chatbot */}
      <HelpChatbot />
    </div>
  );
}