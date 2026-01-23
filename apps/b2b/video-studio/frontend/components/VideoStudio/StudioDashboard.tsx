// apps/video-studio/frontend/components/VideoStudio/StudioDashboard.tsx

import React from 'react';

const StudioDashboard: React.FC = () => {
  // Ici, on pourrait ajouter la logique pour charger les projets de l'utilisateur
  // const [projects, setProjects] = React.useState<any[]>([]);
  // const [isLoading, setIsLoading] = React.useState(true);

  // React.useEffect(() => {
  //   // Simuler un chargement de projets
  //   const fetchProjects = async () => {
  //     // await new Promise(resolve => setTimeout(resolve, 1000));
  //     // setProjects([
  //     //   { id: '1', title: 'Mon premier podcast', type: 'podcast', status: 'completed' },
  //     //   { id: '2', title: 'Vidéo virale #1', type: 'video', status: 'in_progress' },
  //     // ]);
  //     // setIsLoading(false);
  //   };
  //   // fetchProjects();
  // }, []);

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-extrabold text-white mb-8">Votre Studio IAFactory</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          <button className="bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white font-bold py-5 px-8 rounded-lg shadow-lg flex flex-col items-center justify-center transition-all duration-300 transform hover:scale-105">
            <svg className="w-10 h-10 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 17A2 2 0 017 15V3a2 2 0 012-2h6a2 2 0 012 2v12a2 2 0 01-2 2h-6zM9 17v2a2 2 0 002 2h2a2 2 0 002-2v-2"></path></svg>
            <span className="text-lg">Nouveau Projet Vidéo</span>
          </button>

          <button className="bg-gradient-to-r from-pink-600 to-red-600 hover:from-pink-700 hover:to-red-700 text-white font-bold py-5 px-8 rounded-lg shadow-lg flex flex-col items-center justify-center transition-all duration-300 transform hover:scale-105">
            <svg className="w-10 h-10 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m7 0V5a2 2 0 012-2h2a2 2 0 012 2v6m-7 0H9m7 0h-2"></path></svg>
            <span className="text-lg">Nouveau Podcast</span>
          </button>

          <button className="bg-gradient-to-r from-teal-600 to-emerald-600 hover:from-teal-700 hover:to-emerald-700 text-white font-bold py-5 px-8 rounded-lg shadow-lg flex flex-col items-center justify-center transition-all duration-300 transform hover:scale-105">
            <svg className="w-10 h-10 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
            <span className="text-lg">Nouveau Short Viral</span>
          </button>
        </div>

        <h2 className="text-3xl font-bold text-white mb-6">Vos Projets Récents</h2>

        {/* {isLoading ? (
          <p className="text-gray-400">Chargement de vos projets...</p>
        ) : projects.length === 0 ? (
          <p className="text-gray-400">Vous n'avez pas encore de projets. Commencez en un !</p>
        ) : ( */}
          <div className="bg-gray-800 rounded-lg shadow-md p-6">
            <ul className="divide-y divide-gray-700">
              {/* {projects.map(project => ( */}
                <li className="flex items-center justify-between py-4">
                  <div className="flex-1">
                    <p className="text-lg font-semibold text-white">Project Fictif A</p>
                    <p className="text-sm text-gray-400">Type: Vidéo, Statut: En cours</p>
                  </div>
                  <button className="bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium py-2 px-4 rounded-md transition-colors duration-200">
                    Ouvrir
                  </button>
                </li>
                <li className="flex items-center justify-between py-4">
                  <div className="flex-1">
                    <p className="text-lg font-semibold text-white">Project Fictif B</p>
                    <p className="text-sm text-gray-400">Type: Podcast, Statut: Terminé</p>
                  </div>
                  <button className="bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium py-2 px-4 rounded-md transition-colors duration-200">
                    Ouvrir
                  </button>
                </li>
                <li className="flex items-center justify-between py-4">
                  <div className="flex-1">
                    <p className="text-lg font-semibold text-white">Project Fictif C</p>
                    <p className="text-sm text-gray-400">Type: Short, Statut: Erreur</p>
                  </div>
                  <button className="bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium py-2 px-4 rounded-md transition-colors duration-200">
                    Ouvrir
                  </button>
                </li>
              {/* ))} */}
            </ul>
          </div>
        {/* )} */}
      </div>
    </div>
  );
};

export default StudioDashboard;
