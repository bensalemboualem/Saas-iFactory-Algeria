// apps/video-studio/frontend/components/VideoStudio/PreviewPlayer.tsx

import React from 'react';

interface PreviewPlayerProps {
  videoUrl: string | null;
  className?: string; // Pour permettre un style additionnel via les props
}

const PreviewPlayer: React.FC<PreviewPlayerProps> = ({ videoUrl, className }) => {
  if (!videoUrl) {
    return (
      <div className={`flex items-center justify-center bg-gray-800 rounded-lg overflow-hidden ${className || 'w-full h-auto min-h-[300px]'}`}>
        <p className="text-gray-400 text-lg">Aucune vidéo à prévisualiser.</p>
      </div>
    );
  }

  return (
    <div className={`bg-black rounded-lg overflow-hidden shadow-xl ${className || 'w-full h-auto'}`}>
      <video
        src={videoUrl}
        controls
        className="w-full h-full object-contain" // Utiliser object-contain pour éviter le cropping si les ratios ne correspondent pas
        autoPlay // Démarrer la lecture automatiquement
        loop // Boucler la vidéo
        muted // Mute par défaut pour autoplay
      >
        Votre navigateur ne supporte pas la lecture de vidéo.
      </video>
    </div>
  );
};

export default PreviewPlayer;
