// apps/video-studio/frontend/components/VideoStudio/PublishPanel.tsx

import React, { useState } from 'react';

interface PublishPanelProps {
  videoPath: string; // Le chemin ou l'ID de la vidéo à publier
}

type Platform = 'youtube' | 'tiktok' | 'instagram';

const PublishPanel: React.FC<PublishPanelProps> = ({ videoPath }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [tags, setTags] = useState('');
  const [platforms, setPlatforms] = useState<Record<Platform, boolean>>({
    youtube: true,
    tiktok: false,
    instagram: false,
  });
  const [scheduleTime, setScheduleTime] = useState('');
  const [isPublishing, setIsPublishing] = useState(false);

  const handlePlatformChange = (platform: Platform) => {
    setPlatforms(prev => ({ ...prev, [platform]: !prev[platform] }));
  };

  const handlePublish = async () => {
    setIsPublishing(true);
    console.log("Préparation de la publication...");

    const selectedPlatforms = Object.keys(platforms).filter(p => platforms[p as Platform]) as Platform[];

    if (selectedPlatforms.length === 0) {
      alert("Veuillez sélectionner au moins une plateforme.");
      setIsPublishing(false);
      return;
    }

    for (const platform of selectedPlatforms) {
      const payload = {
        video_path: videoPath,
        metadata: {
          title,
          description,
          tags: tags.split(',').map(tag => tag.trim()).filter(Boolean),
        },
        schedule_time: scheduleTime || null,
      };

      console.log(`Publication sur ${platform}:`, payload);
      
      // Simulation d'un appel API pour chaque plateforme
      // En réalité, vous feriez :
      // try {
      //   const response = await fetch(`/api/v1/publish/${platform}`, {
      //     method: 'POST',
      //     headers: { 'Content-Type': 'application/json' },
      //     body: JSON.stringify(payload),
      //   });
      //   if (!response.ok) {
      //     throw new Error(`Erreur lors de la publication sur ${platform}`);
      //   }
      //   console.log(`Succès de la publication sur ${platform}`);
      // } catch (error) {
      //   console.error(error);
      //   alert(`Échec de la publication sur ${platform}.`);
      // }
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simuler la latence réseau
    }

    setIsPublishing(false);
    alert("Publication terminée (simulation) !");
  };

  return (
    <div className="bg-gray-800 text-gray-100 p-8 rounded-lg shadow-2xl max-w-2xl mx-auto">
      <h2 className="text-3xl font-bold text-white mb-6">Publier votre Vidéo</h2>
      
      {/* Métadonnées */}
      <div className="space-y-4 mb-6">
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-gray-400 mb-2">Titre</label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full bg-gray-900 border border-gray-700 rounded-md px-4 py-2 focus:ring-2 focus:ring-purple-500"
            placeholder="Titre accrocheur de votre vidéo"
          />
        </div>
        <div>
          <label htmlFor="description" className="block text-sm font-medium text-gray-400 mb-2">Description</label>
          <textarea
            id="description"
            rows={4}
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full bg-gray-900 border border-gray-700 rounded-md px-4 py-2 focus:ring-2 focus:ring-purple-500"
            placeholder="Description optimisée pour le SEO"
          />
        </div>
        <div>
          <label htmlFor="tags" className="block text-sm font-medium text-gray-400 mb-2">Tags (séparés par des virgules)</label>
          <input
            type="text"
            id="tags"
            value={tags}
            onChange={(e) => setTags(e.target.value)}
            className="w-full bg-gray-900 border border-gray-700 rounded-md px-4 py-2 focus:ring-2 focus:ring-purple-500"
            placeholder="#ia, #video, #algerie"
          />
        </div>
      </div>

      {/* Plateformes */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-400 mb-2">Plateformes de publication</label>
        <div className="flex space-x-4">
          {Object.keys(platforms).map(p => (
            <button
              key={p}
              onClick={() => handlePlatformChange(p as Platform)}
              className={`py-2 px-4 rounded-md font-semibold transition-colors ${
                platforms[p as Platform] ? 'bg-purple-600 text-white' : 'bg-gray-700 hover:bg-gray-600'
              }`}
            >
              {p.charAt(0).toUpperCase() + p.slice(1)}
            </button>
          ))}
        </div>
      </div>
      
      {/* Planification */}
      <div className="mb-8">
        <label htmlFor="schedule" className="block text-sm font-medium text-gray-400 mb-2">Planifier la publication (optionnel)</label>
        <input
          type="datetime-local"
          id="schedule"
          value={scheduleTime}
          onChange={(e) => setScheduleTime(e.target.value)}
          className="w-full bg-gray-900 border border-gray-700 rounded-md px-4 py-2 focus:ring-2 focus:ring-purple-500"
        />
      </div>

      {/* Bouton de publication */}
      <button
        onClick={handlePublish}
        disabled={isPublishing}
        className="w-full bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white font-bold py-3 px-6 rounded-lg shadow-lg transition-all duration-300 disabled:opacity-50 disabled:cursor-wait"
      >
        {isPublishing ? 'Publication en cours...' : 'Lancer la Publication'}
      </button>
    </div>
  );
};

export default PublishPanel;
