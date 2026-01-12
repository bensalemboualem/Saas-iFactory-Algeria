// apps/video-studio/frontend/pages/video-studio/scripts/[id].tsx

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import ScriptEditor from '../../components/VideoStudio/ScriptEditor';

// Supposons une structure de données pour le script, basée sur les modèles Pydantic
interface Script {
  id: string;
  title: string;
  hook: string;
  intro: string;
  segments: { content: string; visual_direction: string; }[];
  outro: string;
  cta: string;
  status: 'draft' | 'approved' | 'in_production' | 'completed';
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

const EditScriptPage: React.FC = () => {
  const router = useRouter();
  const { id } = router.query; // Récupérer l'ID du script de l'URL

  const [script, setScript] = useState<Script | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (id) {
      const fetchScript = async () => {
        try {
          setIsLoading(true);
          setError(null);
          
          // Simulation d'appel API pour récupérer le script
          // En réalité, vous feriez un appel à votre API FastAPI:
          // const response = await fetch(`${API_BASE_URL}/api/v1/scripts/${id}`);
          // if (!response.ok) {
          //   throw new Error(`Erreur HTTP: ${response.status}`);
          // }
          // const data = await response.json();
          // setScript(data);

          // Pour l'instant, un script fictif
          await new Promise(resolve => setTimeout(resolve, 500)); // Simuler le temps de chargement
          const dummyScript: Script = {
            id: id as string,
            title: `Script pour la vidéo sur le sujet ${id}`,
            hook: "Saviez-vous que 90% des gens échouent à...",
            intro: "Dans cette vidéo, nous allons explorer pourquoi il est crucial de...",
            segments: [
              { content: "Premier point clé à aborder.", visual_direction: "Graphique explicatif" },
              { content: "Deuxième argument important.", visual_direction: "Témoignage client" },
            ],
            outro: "En conclusion, n'oubliez pas que...",
            cta: "Abonnez-vous pour plus de conseils !",
            status: "draft",
          };
          setScript(dummyScript);

        } catch (err) {
          console.error("Échec du chargement du script:", err);
          setError("Impossible de charger le script. Veuillez réessayer.");
        } finally {
          setIsLoading(false);
        }
      };

      fetchScript();
    }
  }, [id]);

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-gray-900 text-white">
        <p>Chargement du script...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-gray-900 text-white">
        <p className="text-red-500">{error}</p>
      </div>
    );
  }

  if (!script) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-gray-900 text-white">
        <p>Aucun script trouvé.</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 py-8">
      <ScriptEditor initialScript={script} />
    </div>
  );
};

export default EditScriptPage;
