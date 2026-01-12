'use client';

import React, { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Timeline } from '@/components/video/timeline';
import { api, Project, Script } from '@/lib/api';

type Tab = 'script' | 'assets' | 'timeline' | 'publish';

export default function ProjectEditorPage() {
  const params = useParams();
  const router = useRouter();
  const projectId = params.id as string;

  const [project, setProject] = useState<Project | null>(null);
  const [script, setScript] = useState<Script | null>(null);
  const [activeTab, setActiveTab] = useState<Tab>('script');
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    if (projectId) {
      loadProject();
    }
  }, [projectId]);

  const loadProject = async () => {
    try {
      const data = await api.projects.get(projectId);
      setProject(data);
      if (data.script_id) {
        const scriptData = await api.scripts.get(data.script_id);
        setScript(scriptData);
      }
    } catch (error) {
      console.error('Failed to load project:', error);
    } finally {
      setLoading(false);
    }
  };

  const startPipeline = async () => {
    if (!project) return;
    setGenerating(true);
    try {
      await api.projects.startPipeline(projectId);
      await loadProject();
    } catch (error) {
      console.error('Failed to start pipeline:', error);
    } finally {
      setGenerating(false);
    }
  };

  const tabs = [
    { id: 'script', label: 'Script', icon: '📝' },
    { id: 'assets', label: 'Assets', icon: '🎨' },
    { id: 'timeline', label: 'Timeline', icon: '🎬' },
    { id: 'publish', label: 'Publication', icon: '📤' },
  ];

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-950 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-500"></div>
      </div>
    );
  }

  if (!project) {
    return (
      <div className="min-h-screen bg-gray-950 flex items-center justify-center text-white">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4">Projet non trouve</h1>
          <Button variant="primary">
            <Link href="/projects">Retour aux projets</Link>
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white flex flex-col">
      {/* Header */}
      <header className="border-b border-gray-800 flex-shrink-0">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Link href="/projects" className="text-gray-400 hover:text-white">
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
              </Link>
              <div>
                <h1 className="text-xl font-bold">{project.title}</h1>
                <p className="text-sm text-gray-400">{project.description}</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <span className={`px-3 py-1 rounded-full text-sm ${
                project.status === 'completed' ? 'bg-green-500/20 text-green-400' :
                project.status === 'processing' ? 'bg-yellow-500/20 text-yellow-400' :
                project.status === 'failed' ? 'bg-red-500/20 text-red-400' :
                'bg-gray-500/20 text-gray-400'
              }`}>
                {project.status}
              </span>
              <Button
                variant="primary"
                onClick={startPipeline}
                loading={generating}
                disabled={project.status === 'processing'}
              >
                {project.status === 'processing' ? 'En cours...' : 'Generer Video'}
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Tabs */}
      <div className="border-b border-gray-800 flex-shrink-0">
        <div className="container mx-auto px-6">
          <div className="flex gap-1">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as Tab)}
                className={`px-4 py-3 text-sm font-medium transition-colors relative ${
                  activeTab === tab.id
                    ? 'text-white'
                    : 'text-gray-400 hover:text-white'
                }`}
              >
                <span className="mr-2">{tab.icon}</span>
                {tab.label}
                {activeTab === tab.id && (
                  <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-purple-500"></div>
                )}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Content */}
      <main className="flex-1 overflow-hidden">
        <div className="container mx-auto px-6 py-6 h-full">
          {activeTab === 'script' && (
            <ScriptTab script={script} projectId={projectId} onUpdate={loadProject} />
          )}
          {activeTab === 'assets' && (
            <AssetsTab projectId={projectId} />
          )}
          {activeTab === 'timeline' && (
            <TimelineTab project={project} />
          )}
          {activeTab === 'publish' && (
            <PublishTab project={project} onUpdate={loadProject} />
          )}
        </div>
      </main>
    </div>
  );
}

function ScriptTab({ script, projectId, onUpdate }: { script: Script | null; projectId: string; onUpdate: () => void }) {
  const [editedScript, setEditedScript] = useState(script?.content || '');
  const [generating, setGenerating] = useState(false);

  const regenerateScript = async () => {
    setGenerating(true);
    try {
      await api.scripts.regenerate(projectId);
      onUpdate();
    } catch (error) {
      console.error('Failed to regenerate script:', error);
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-full">
      {/* Script Editor */}
      <Card variant="bordered" className="flex flex-col h-full">
        <CardHeader className="flex-shrink-0 flex flex-row items-center justify-between">
          <CardTitle>Script</CardTitle>
          <Button variant="ghost" size="sm" onClick={regenerateScript} loading={generating}>
            Regenerer
          </Button>
        </CardHeader>
        <CardContent className="flex-1 overflow-hidden">
          <textarea
            value={editedScript}
            onChange={(e) => setEditedScript(e.target.value)}
            className="w-full h-full bg-gray-900 border border-gray-700 rounded-lg p-4 text-white resize-none focus:outline-none focus:border-purple-500"
            placeholder="Le script sera genere automatiquement..."
          />
        </CardContent>
      </Card>

      {/* Scenes */}
      <Card variant="bordered" className="flex flex-col h-full overflow-hidden">
        <CardHeader className="flex-shrink-0">
          <CardTitle>Scenes ({script?.scenes?.length || 0})</CardTitle>
        </CardHeader>
        <CardContent className="flex-1 overflow-auto">
          {script?.scenes && script.scenes.length > 0 ? (
            <div className="space-y-4">
              {script.scenes.map((scene: any, index: number) => (
                <div key={index} className="bg-gray-900 rounded-lg p-4 border border-gray-700">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-purple-400">Scene {index + 1}</span>
                    <span className="text-xs text-gray-500">{scene.duration}s</span>
                  </div>
                  <p className="text-sm text-gray-300 mb-2">{scene.narration}</p>
                  <p className="text-xs text-gray-500 italic">{scene.visual_description}</p>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center text-gray-500 py-8">
              <p>Aucune scene</p>
              <p className="text-sm">Generez le script pour creer les scenes</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

function AssetsTab({ projectId }: { projectId: string }) {
  const [assets, setAssets] = useState<any[]>([]);
  const [filter, setFilter] = useState<'all' | 'images' | 'videos' | 'audio'>('all');

  useEffect(() => {
    loadAssets();
  }, [projectId]);

  const loadAssets = async () => {
    // Load assets from API
    setAssets([]);
  };

  const filteredAssets = assets.filter(
    (asset) => filter === 'all' || asset.type === filter
  );

  return (
    <div className="h-full flex flex-col">
      {/* Filters */}
      <div className="flex gap-2 mb-6 flex-shrink-0">
        {['all', 'images', 'videos', 'audio'].map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f as any)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              filter === f
                ? 'bg-purple-500 text-white'
                : 'bg-gray-800 text-gray-400 hover:text-white'
            }`}
          >
            {f === 'all' ? 'Tous' : f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>

      {/* Assets Grid */}
      {filteredAssets.length === 0 ? (
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center text-gray-500">
            <svg className="w-16 h-16 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <p>Aucun asset genere</p>
            <p className="text-sm">Lancez la generation pour creer les assets</p>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4 flex-1 overflow-auto">
          {filteredAssets.map((asset) => (
            <div key={asset.id} className="aspect-square bg-gray-800 rounded-lg overflow-hidden relative group">
              {asset.type === 'images' ? (
                <img src={asset.url} alt="" className="w-full h-full object-cover" />
              ) : asset.type === 'videos' ? (
                <video src={asset.url} className="w-full h-full object-cover" />
              ) : (
                <div className="w-full h-full flex items-center justify-center">
                  <svg className="w-8 h-8 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3" />
                  </svg>
                </div>
              )}
              <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                <Button variant="ghost" size="sm">Voir</Button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function TimelineTab({ project }: { project: Project }) {
  // Generate placeholder timeline tracks from project duration
  const duration = project.duration || 60; // Default 60 seconds

  const placeholderTracks = [
    {
      id: 'video-track',
      name: 'Video',
      type: 'video' as const,
      clips: [
        { id: 'v1', type: 'video' as const, start: 0, duration: duration, label: 'Main Video' }
      ]
    },
    {
      id: 'audio-track',
      name: 'Narration',
      type: 'audio' as const,
      clips: [
        { id: 'a1', type: 'audio' as const, start: 0, duration: duration, label: 'Voice Over' }
      ]
    },
    {
      id: 'music-track',
      name: 'Music',
      type: 'music' as const,
      clips: [
        { id: 'm1', type: 'music' as const, start: 0, duration: duration, label: 'Background Music' }
      ]
    }
  ];

  const [currentTime, setCurrentTime] = React.useState(0);
  const [isPlaying, setIsPlaying] = React.useState(false);

  return (
    <div className="h-full flex flex-col">
      <Timeline
        tracks={placeholderTracks}
        duration={duration}
        currentTime={currentTime}
        isPlaying={isPlaying}
        onTimeChange={setCurrentTime}
        onPlayPause={() => setIsPlaying(!isPlaying)}
        onClipSelect={(clipId) => console.log('Selected clip:', clipId)}
      />
    </div>
  );
}

function PublishTab({ project, onUpdate }: { project: Project; onUpdate: () => void }) {
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>([]);
  const [publishing, setPublishing] = useState(false);

  const platforms = [
    { id: 'youtube', name: 'YouTube', icon: '📺', connected: true },
    { id: 'tiktok', name: 'TikTok', icon: '🎵', connected: false },
    { id: 'instagram', name: 'Instagram', icon: '📷', connected: true },
    { id: 'linkedin', name: 'LinkedIn', icon: '💼', connected: false },
    { id: 'twitter', name: 'Twitter/X', icon: '🐦', connected: true },
  ];

  const togglePlatform = (platformId: string) => {
    setSelectedPlatforms((prev) =>
      prev.includes(platformId)
        ? prev.filter((p) => p !== platformId)
        : [...prev, platformId]
    );
  };

  const publishVideo = async () => {
    if (selectedPlatforms.length === 0) return;
    setPublishing(true);
    try {
      await api.publish.publish(project.id, selectedPlatforms);
      onUpdate();
    } catch (error) {
      console.error('Failed to publish:', error);
    } finally {
      setPublishing(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <Card variant="bordered">
        <CardHeader>
          <CardTitle>Publier sur les reseaux sociaux</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Video Preview */}
          {project.video_url && (
            <div className="aspect-video bg-gray-800 rounded-lg overflow-hidden">
              <video
                src={project.video_url}
                controls
                className="w-full h-full"
              />
            </div>
          )}

          {/* Platform Selection */}
          <div className="space-y-3">
            <h3 className="font-medium">Plateformes</h3>
            <div className="grid grid-cols-2 gap-3">
              {platforms.map((platform) => (
                <button
                  key={platform.id}
                  onClick={() => platform.connected && togglePlatform(platform.id)}
                  disabled={!platform.connected}
                  className={`p-4 rounded-lg border transition-all text-left ${
                    selectedPlatforms.includes(platform.id)
                      ? 'border-purple-500 bg-purple-500/10'
                      : platform.connected
                      ? 'border-gray-700 hover:border-gray-600'
                      : 'border-gray-800 opacity-50 cursor-not-allowed'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">{platform.icon}</span>
                    <div>
                      <p className="font-medium">{platform.name}</p>
                      <p className="text-xs text-gray-500">
                        {platform.connected ? 'Connecte' : 'Non connecte'}
                      </p>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Publish Button */}
          <Button
            variant="primary"
            className="w-full"
            onClick={publishVideo}
            loading={publishing}
            disabled={selectedPlatforms.length === 0 || !project.video_url}
          >
            Publier sur {selectedPlatforms.length} plateforme{selectedPlatforms.length > 1 ? 's' : ''}
          </Button>

          {/* Published Status */}
          {project.published_urls && Object.keys(project.published_urls).length > 0 && (
            <div className="space-y-2">
              <h3 className="font-medium">Deja publie</h3>
              {Object.entries(project.published_urls).map(([platform, url]) => (
                <a
                  key={platform}
                  href={url as string}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-2 text-sm text-purple-400 hover:text-purple-300"
                >
                  <span>{platform}</span>
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                  </svg>
                </a>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
