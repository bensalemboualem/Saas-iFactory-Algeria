'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';

type SettingsTab = 'api-keys' | 'platforms' | 'preferences' | 'billing';

interface ApiKey {
  id: string;
  name: string;
  provider: string;
  masked: string;
  configured: boolean;
}

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState<SettingsTab>('api-keys');

  const tabs = [
    { id: 'api-keys', label: 'Cles API', icon: '🔑' },
    { id: 'platforms', label: 'Plateformes', icon: '📱' },
    { id: 'preferences', label: 'Preferences', icon: '⚙️' },
    { id: 'billing', label: 'Facturation', icon: '💳' },
  ];

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      {/* Header */}
      <header className="border-b border-gray-800">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center gap-4">
            <Link href="/projects" className="text-gray-400 hover:text-white">
              <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
            </Link>
            <h1 className="text-xl font-bold">Parametres</h1>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-6 py-8">
        <div className="flex gap-8">
          {/* Sidebar */}
          <div className="w-64 flex-shrink-0">
            <nav className="space-y-1">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as SettingsTab)}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left transition-colors ${
                    activeTab === tab.id
                      ? 'bg-purple-500/20 text-purple-400'
                      : 'text-gray-400 hover:bg-gray-800 hover:text-white'
                  }`}
                >
                  <span>{tab.icon}</span>
                  <span>{tab.label}</span>
                </button>
              ))}
            </nav>
          </div>

          {/* Content */}
          <div className="flex-1">
            {activeTab === 'api-keys' && <ApiKeysTab />}
            {activeTab === 'platforms' && <PlatformsTab />}
            {activeTab === 'preferences' && <PreferencesTab />}
            {activeTab === 'billing' && <BillingTab />}
          </div>
        </div>
      </div>
    </div>
  );
}

function ApiKeysTab() {
  const [apiKeys, setApiKeys] = useState<ApiKey[]>([
    { id: '1', name: 'OpenAI', provider: 'openai', masked: 'sk-...abc', configured: true },
    { id: '2', name: 'Anthropic', provider: 'anthropic', masked: '', configured: false },
    { id: '3', name: 'ElevenLabs', provider: 'elevenlabs', masked: 'xi-...xyz', configured: true },
    { id: '4', name: 'Runway', provider: 'runway', masked: '', configured: false },
    { id: '5', name: 'Replicate', provider: 'replicate', masked: 'r8_...123', configured: true },
    { id: '6', name: 'FAL.ai', provider: 'fal', masked: '', configured: false },
    { id: '7', name: 'Luma', provider: 'luma', masked: '', configured: false },
    { id: '8', name: 'HeyGen', provider: 'heygen', masked: '', configured: false },
  ]);

  const [editingKey, setEditingKey] = useState<string | null>(null);
  const [keyValue, setKeyValue] = useState('');

  const saveKey = (id: string) => {
    setApiKeys((keys) =>
      keys.map((k) =>
        k.id === id
          ? { ...k, configured: true, masked: keyValue.slice(0, 3) + '...' + keyValue.slice(-3) }
          : k
      )
    );
    setEditingKey(null);
    setKeyValue('');
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold mb-2">Cles API</h2>
        <p className="text-gray-400">Configurez vos cles API pour les differents providers IA</p>
      </div>

      <div className="grid gap-4">
        {apiKeys.map((key) => (
          <Card key={key.id} variant="bordered">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className={`w-3 h-3 rounded-full ${key.configured ? 'bg-green-500' : 'bg-gray-600'}`} />
                  <div>
                    <h3 className="font-medium">{key.name}</h3>
                    <p className="text-sm text-gray-500">
                      {key.configured ? key.masked : 'Non configure'}
                    </p>
                  </div>
                </div>
                <div>
                  {editingKey === key.id ? (
                    <div className="flex items-center gap-2">
                      <input
                        type="password"
                        value={keyValue}
                        onChange={(e) => setKeyValue(e.target.value)}
                        className="bg-gray-800 border border-gray-700 rounded px-3 py-1.5 text-sm focus:outline-none focus:border-purple-500"
                        placeholder="Entrez la cle API"
                      />
                      <Button variant="primary" size="sm" onClick={() => saveKey(key.id)}>
                        Sauver
                      </Button>
                      <Button variant="ghost" size="sm" onClick={() => setEditingKey(null)}>
                        Annuler
                      </Button>
                    </div>
                  ) : (
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => setEditingKey(key.id)}
                    >
                      {key.configured ? 'Modifier' : 'Configurer'}
                    </Button>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card variant="bordered" className="bg-yellow-500/5 border-yellow-500/20">
        <CardContent className="p-4">
          <div className="flex items-start gap-3">
            <span className="text-yellow-500 text-xl">⚠️</span>
            <div>
              <h3 className="font-medium text-yellow-500">Securite</h3>
              <p className="text-sm text-gray-400">
                Vos cles API sont stockees de maniere securisee et chiffrees.
                Ne partagez jamais vos cles avec personne.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

function PlatformsTab() {
  const platforms = [
    { id: 'youtube', name: 'YouTube', icon: '📺', connected: true, username: '@moncanal' },
    { id: 'tiktok', name: 'TikTok', icon: '🎵', connected: false, username: '' },
    { id: 'instagram', name: 'Instagram', icon: '📷', connected: true, username: '@moncompte' },
    { id: 'linkedin', name: 'LinkedIn', icon: '💼', connected: false, username: '' },
    { id: 'twitter', name: 'Twitter/X', icon: '🐦', connected: true, username: '@montwitter' },
    { id: 'facebook', name: 'Facebook', icon: '👤', connected: false, username: '' },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold mb-2">Plateformes connectees</h2>
        <p className="text-gray-400">Gerez vos connexions aux reseaux sociaux</p>
      </div>

      <div className="grid gap-4">
        {platforms.map((platform) => (
          <Card key={platform.id} variant="bordered">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <span className="text-3xl">{platform.icon}</span>
                  <div>
                    <h3 className="font-medium">{platform.name}</h3>
                    <p className="text-sm text-gray-500">
                      {platform.connected ? platform.username : 'Non connecte'}
                    </p>
                  </div>
                </div>
                <Button
                  variant={platform.connected ? 'ghost' : 'primary'}
                  size="sm"
                >
                  {platform.connected ? 'Deconnecter' : 'Connecter'}
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}

function PreferencesTab() {
  const [preferences, setPreferences] = useState({
    defaultTTS: 'elevenlabs',
    defaultImageProvider: 'dalle',
    defaultVideoProvider: 'runway',
    autoPublish: false,
    watermark: true,
    language: 'fr',
    quality: 'high',
  });

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold mb-2">Preferences</h2>
        <p className="text-gray-400">Personnalisez votre experience</p>
      </div>

      <Card variant="bordered">
        <CardHeader>
          <CardTitle>Providers par defaut</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Synthese vocale (TTS)</label>
            <select
              value={preferences.defaultTTS}
              onChange={(e) => setPreferences({ ...preferences, defaultTTS: e.target.value })}
              className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 focus:outline-none focus:border-purple-500"
            >
              <option value="elevenlabs">ElevenLabs</option>
              <option value="openai">OpenAI TTS</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">Generation d'images</label>
            <select
              value={preferences.defaultImageProvider}
              onChange={(e) => setPreferences({ ...preferences, defaultImageProvider: e.target.value })}
              className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 focus:outline-none focus:border-purple-500"
            >
              <option value="dalle">DALL-E 3</option>
              <option value="flux">Flux</option>
              <option value="sdxl">SDXL</option>
              <option value="leonardo">Leonardo</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">Generation video</label>
            <select
              value={preferences.defaultVideoProvider}
              onChange={(e) => setPreferences({ ...preferences, defaultVideoProvider: e.target.value })}
              className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 focus:outline-none focus:border-purple-500"
            >
              <option value="runway">Runway Gen-3</option>
              <option value="luma">Luma Dream Machine</option>
              <option value="replicate">Replicate SVD</option>
            </select>
          </div>
        </CardContent>
      </Card>

      <Card variant="bordered">
        <CardHeader>
          <CardTitle>Options de sortie</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Qualite video</label>
            <select
              value={preferences.quality}
              onChange={(e) => setPreferences({ ...preferences, quality: e.target.value })}
              className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 focus:outline-none focus:border-purple-500"
            >
              <option value="standard">Standard (720p)</option>
              <option value="high">Haute (1080p)</option>
              <option value="ultra">Ultra (4K)</option>
            </select>
          </div>
          <div className="flex items-center justify-between">
            <div>
              <p className="font-medium">Filigrane</p>
              <p className="text-sm text-gray-500">Ajouter le logo IAFactory</p>
            </div>
            <button
              onClick={() => setPreferences({ ...preferences, watermark: !preferences.watermark })}
              className={`w-12 h-6 rounded-full transition-colors ${
                preferences.watermark ? 'bg-purple-500' : 'bg-gray-700'
              }`}
            >
              <div
                className={`w-5 h-5 bg-white rounded-full transition-transform ${
                  preferences.watermark ? 'translate-x-6' : 'translate-x-0.5'
                }`}
              />
            </button>
          </div>
          <div className="flex items-center justify-between">
            <div>
              <p className="font-medium">Publication automatique</p>
              <p className="text-sm text-gray-500">Publier des que la video est prete</p>
            </div>
            <button
              onClick={() => setPreferences({ ...preferences, autoPublish: !preferences.autoPublish })}
              className={`w-12 h-6 rounded-full transition-colors ${
                preferences.autoPublish ? 'bg-purple-500' : 'bg-gray-700'
              }`}
            >
              <div
                className={`w-5 h-5 bg-white rounded-full transition-transform ${
                  preferences.autoPublish ? 'translate-x-6' : 'translate-x-0.5'
                }`}
              />
            </button>
          </div>
        </CardContent>
      </Card>

      <Button variant="primary">Sauvegarder les preferences</Button>
    </div>
  );
}

function BillingTab() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold mb-2">Facturation</h2>
        <p className="text-gray-400">Gerez votre abonnement et vos credits</p>
      </div>

      <Card variant="bordered" className="bg-gradient-to-r from-purple-500/10 to-blue-500/10">
        <CardContent className="p-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-xl font-bold">Plan Pro</h3>
              <p className="text-gray-400">Renouvellement le 15 janvier 2025</p>
            </div>
            <span className="text-3xl font-bold">49€<span className="text-sm text-gray-400">/mois</span></span>
          </div>
          <div className="flex gap-3">
            <Button variant="ghost" size="sm">Changer de plan</Button>
            <Button variant="ghost" size="sm">Annuler</Button>
          </div>
        </CardContent>
      </Card>

      <Card variant="bordered">
        <CardHeader>
          <CardTitle>Credits restants</CardTitle>
          <CardDescription>Utilisez vos credits pour generer du contenu</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span>Generation d'images</span>
                <span>450 / 500</span>
              </div>
              <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
                <div className="h-full bg-purple-500 rounded-full" style={{ width: '90%' }} />
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span>Generation video</span>
                <span>12 / 50 minutes</span>
              </div>
              <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
                <div className="h-full bg-blue-500 rounded-full" style={{ width: '24%' }} />
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span>Synthese vocale</span>
                <span>85,000 / 100,000 caracteres</span>
              </div>
              <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
                <div className="h-full bg-green-500 rounded-full" style={{ width: '85%' }} />
              </div>
            </div>
          </div>
          <Button variant="primary" className="w-full mt-6">Acheter des credits</Button>
        </CardContent>
      </Card>

      <Card variant="bordered">
        <CardHeader>
          <CardTitle>Historique de facturation</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {[
              { date: '15 Dec 2024', amount: '49.00€', status: 'Paye' },
              { date: '15 Nov 2024', amount: '49.00€', status: 'Paye' },
              { date: '15 Oct 2024', amount: '49.00€', status: 'Paye' },
            ].map((invoice, i) => (
              <div key={i} className="flex items-center justify-between py-2 border-b border-gray-800 last:border-0">
                <span>{invoice.date}</span>
                <span>{invoice.amount}</span>
                <span className="text-green-400 text-sm">{invoice.status}</span>
                <Button variant="ghost" size="sm">Telecharger</Button>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
