'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { api, Project } from '@/lib/api';

export default function ProjectsPage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      const data = await api.projects.list();
      setProjects(data);
    } catch (error) {
      console.error('Failed to load projects:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      draft: 'bg-gray-500',
      processing: 'bg-yellow-500 animate-pulse',
      completed: 'bg-green-500',
      failed: 'bg-red-500',
      published: 'bg-blue-500',
    };
    return colors[status] || 'bg-gray-500';
  };

  const getStatusLabel = (status: string) => {
    const labels: Record<string, string> = {
      draft: 'Brouillon',
      processing: 'En cours...',
      completed: 'Termine',
      failed: 'Echec',
      published: 'Publie',
    };
    return labels[status] || status;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-950 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      {/* Header */}
      <header className="border-b border-gray-800">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <Link href="/" className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
              IAFactory Video
            </Link>
            <Button variant="primary">
              <Link href="/">Nouveau Projet</Link>
            </Button>
          </div>
        </div>
      </header>

      {/* Content */}
      <main className="container mx-auto px-6 py-8">
        <h1 className="text-3xl font-bold mb-8">Mes Projets</h1>

        {projects.length === 0 ? (
          <Card variant="bordered" className="text-center py-12">
            <CardContent>
              <div className="text-gray-400 mb-4">
                <svg className="w-16 h-16 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M7 4v16M17 4v16M3 8h4m10 0h4M3 12h18M3 16h4m10 0h4M4 20h16a1 1 0 001-1V5a1 1 0 00-1-1H4a1 1 0 00-1 1v14a1 1 0 001 1z" />
                </svg>
              </div>
              <p className="text-gray-400 mb-4">Aucun projet pour le moment</p>
              <Button variant="primary">
                <Link href="/">Creer mon premier projet</Link>
              </Button>
            </CardContent>
          </Card>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {projects.map((project) => (
              <Link key={project.id} href={`/projects/${project.id}`}>
                <Card variant="bordered" className="hover:border-purple-500/50 transition-all cursor-pointer group">
                  {/* Thumbnail */}
                  <div className="aspect-video bg-gray-800 relative overflow-hidden">
                    {project.thumbnail_url ? (
                      <img
                        src={project.thumbnail_url}
                        alt={project.title}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                      />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center text-gray-600">
                        <svg className="w-12 h-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                        </svg>
                      </div>
                    )}
                    {/* Status badge */}
                    <div className="absolute top-2 right-2">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(project.status)} bg-opacity-90`}>
                        {getStatusLabel(project.status)}
                      </span>
                    </div>
                    {/* Duration */}
                    {project.duration && (
                      <div className="absolute bottom-2 right-2 bg-black/70 px-2 py-0.5 rounded text-xs">
                        {Math.floor(project.duration / 60)}:{(project.duration % 60).toString().padStart(2, '0')}
                      </div>
                    )}
                  </div>

                  <CardHeader className="pb-2">
                    <CardTitle className="truncate">{project.title}</CardTitle>
                  </CardHeader>

                  <CardContent>
                    <p className="text-sm text-gray-400 line-clamp-2 mb-3">
                      {project.description || 'Pas de description'}
                    </p>
                    <div className="flex items-center justify-between text-xs text-gray-500">
                      <span>{new Date(project.created_at).toLocaleDateString('fr-FR')}</span>
                      {project.platforms && project.platforms.length > 0 && (
                        <div className="flex gap-1">
                          {project.platforms.slice(0, 3).map((platform) => (
                            <span key={platform} className="bg-gray-700 px-2 py-0.5 rounded">
                              {platform}
                            </span>
                          ))}
                          {project.platforms.length > 3 && (
                            <span className="bg-gray-700 px-2 py-0.5 rounded">
                              +{project.platforms.length - 3}
                            </span>
                          )}
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>
              </Link>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
