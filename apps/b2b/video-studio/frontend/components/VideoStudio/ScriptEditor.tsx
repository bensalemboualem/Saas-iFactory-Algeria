// apps/video-studio/frontend/components/VideoStudio/ScriptEditor.tsx

import React, { useState, useEffect } from 'react';

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

interface ScriptEditorProps {
  initialScript: Script;
}

const ScriptEditor: React.FC<ScriptEditorProps> = ({ initialScript }) => {
  const [script, setScript] = useState<Script>(initialScript);

  useEffect(() => {
    setScript(initialScript);
  }, [initialScript]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setScript(prev => ({ ...prev, [name]: value }));
  };
  
  const handleSegmentChange = (index: number, field: string, value: string) => {
    const newSegments = [...script.segments];
    newSegments[index] = { ...newSegments[index], [field]: value };
    setScript(prev => ({ ...prev, segments: newSegments }));
  };

  const handleSaveChanges = async () => {
    // Logique pour appeler l'API PUT /api/v1/scripts/{script.id}
    console.log("Sauvegarde des changements:", script);
    // Simuler un appel API
    alert("Changements sauvegardés (simulation) !");
  };

  const handleApproveScript = async () => {
    // Logique pour appeler l'API POST /api/v1/scripts/{script.id}/approve
    console.log("Approbation du script:", script.id);
    setScript(prev => ({ ...prev, status: 'approved' }));
    alert("Script approuvé (simulation) !");
  };

  return (
    <div className="bg-gray-800 text-gray-100 p-8 rounded-lg shadow-2xl max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold text-white">Éditeur de Script</h2>
        <span className={`px-4 py-1 text-sm font-semibold rounded-full ${
          script.status === 'approved' ? 'bg-green-600' :
          script.status === 'in_production' ? 'bg-yellow-600' :
          'bg-gray-600'
        }`}>
          {script.status.charAt(0).toUpperCase() + script.status.slice(1)}
        </span>
      </div>

      {/* Titre */}
      <div className="mb-6">
        <label htmlFor="title" className="block text-sm font-medium text-gray-400 mb-2">Titre de la Vidéo</label>
        <input
          type="text"
          name="title"
          id="title"
          value={script.title}
          onChange={handleInputChange}
          className="w-full bg-gray-900 border border-gray-700 rounded-md px-4 py-2 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition"
        />
      </div>

      {/* Hook */}
      <div className="mb-6">
        <label htmlFor="hook" className="block text-sm font-medium text-gray-400 mb-2">Hook (Accroche)</label>
        <textarea
          name="hook"
          id="hook"
          rows={2}
          value={script.hook}
          onChange={handleInputChange}
          className="w-full bg-gray-900 border border-gray-700 rounded-md px-4 py-2 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition"
        />
      </div>
      
      {/* Intro */}
      <div className="mb-6">
        <label htmlFor="intro" className="block text-sm font-medium text-gray-400 mb-2">Introduction</label>
        <textarea
          name="intro"
          id="intro"
          rows={3}
          value={script.intro}
          onChange={handleInputChange}
          className="w-full bg-gray-900 border border-gray-700 rounded-md px-4 py-2 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition"
        />
      </div>

      {/* Segments */}
      <h3 className="text-xl font-semibold mb-4">Segments</h3>
      <div className="space-y-6">
        {script.segments.map((segment, index) => (
          <div key={index} className="bg-gray-900 p-4 rounded-md border border-gray-700">
            <label className="block text-sm font-medium text-gray-400 mb-2">Segment {index + 1}</label>
            <textarea
              rows={4}
              value={segment.content}
              onChange={(e) => handleSegmentChange(index, 'content', e.target.value)}
              className="w-full bg-gray-700 border border-gray-600 rounded-md px-4 py-2 mb-2 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition"
              placeholder="Contenu du segment..."
            />
            <textarea
              rows={2}
              value={segment.visual_direction}
              onChange={(e) => handleSegmentChange(index, 'visual_direction', e.target.value)}
              className="w-full bg-gray-700 border border-gray-600 rounded-md px-4 py-2 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition"
              placeholder="Direction visuelle..."
            />
          </div>
        ))}
      </div>

      {/* Outro & CTA */}
      <div className="mt-6 mb-8 grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label htmlFor="outro" className="block text-sm font-medium text-gray-400 mb-2">Conclusion</label>
          <textarea
            name="outro"
            id="outro"
            rows={3}
            value={script.outro}
            onChange={handleInputChange}
            className="w-full bg-gray-900 border border-gray-700 rounded-md px-4 py-2 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition"
          />
        </div>
        <div>
          <label htmlFor="cta" className="block text-sm font-medium text-gray-400 mb-2">Appel à l'Action (CTA)</label>
          <textarea
            name="cta"
            id="cta"
            rows={3}
            value={script.cta}
            onChange={handleInputChange}
            className="w-full bg-gray-900 border border-gray-700 rounded-md px-4 py-2 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition"
          />
        </div>
      </div>

      {/* Actions */}
      <div className="flex items-center justify-end space-x-4">
        <button 
          onClick={handleSaveChanges}
          className="bg-gray-600 hover:bg-gray-700 text-white font-bold py-2 px-6 rounded-md transition-colors duration-200">
          Sauvegarder
        </button>
        <button 
          onClick={handleApproveScript}
          disabled={script.status === 'approved'}
          className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-6 rounded-md transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed">
          Approuver
        </button>
      </div>
    </div>
  );
};

export default ScriptEditor;
