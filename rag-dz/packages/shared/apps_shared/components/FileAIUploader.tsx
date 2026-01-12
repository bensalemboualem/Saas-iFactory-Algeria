import React, { useState, useRef, useCallback } from 'react';

// ============================================
// Types
// ============================================
interface UploadedFile {
  id: string;
  name: string;
  size: number;
  type: string;
  status: 'uploading' | 'processing' | 'ready' | 'error';
  progress: number;
  summary?: string;
  keyPoints?: string[];
  error?: string;
}

interface AnalysisResult {
  file_id: string;
  summary: string;
  key_points: string[];
  entities: Array<{ name: string; type: string }>;
  language: string;
  page_count?: number;
  word_count?: number;
}

interface FileAIUploaderProps {
  /** URL d'upload (défaut: /api/upload) */
  uploadUrl?: string;
  /** URL d'analyse (défaut: /api/agent/analyze) */
  analyzeUrl?: string;
  /** Types de fichiers acceptés */
  acceptedTypes?: string[];
  /** Taille max en MB */
  maxSizeMB?: number;
  /** Mode démo (limite le nombre d'uploads) */
  maxUploads?: number;
  /** Callback après analyse */
  onAnalysisComplete?: (result: AnalysisResult) => void;
  /** Titre */
  title?: string;
  /** Mode compact */
  compact?: boolean;
}

// ============================================
// Helpers
// ============================================
const formatFileSize = (bytes: number): string => {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
};

const getFileIcon = (type: string): string => {
  if (type.includes('pdf')) return '📄';
  if (type.includes('word') || type.includes('document')) return '📝';
  if (type.includes('excel') || type.includes('spreadsheet')) return '📊';
  if (type.includes('image')) return '🖼️';
  if (type.includes('text')) return '📃';
  return '📎';
};

// ============================================
// Composant Principal
// ============================================
export const FileAIUploader: React.FC<FileAIUploaderProps> = ({
  uploadUrl = '/api/upload',
  analyzeUrl = '/api/agent/analyze',
  acceptedTypes = ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.xls'],
  maxSizeMB = 10,
  maxUploads = 3,
  onAnalysisComplete,
  title = '📁 FileAI - Analyse de Documents',
  compact = false,
}) => {
  // State
  const [files, setFiles] = useState<UploadedFile[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [remainingUploads, setRemainingUploads] = useState(maxUploads);

  // Refs
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Générer un ID unique
  const generateId = () => `file_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

  // Validation du fichier
  const validateFile = (file: File): string | null => {
    const extension = `.${file.name.split('.').pop()?.toLowerCase()}`;
    
    if (!acceptedTypes.some(t => t.toLowerCase() === extension)) {
      return `Type de fichier non supporté. Acceptés: ${acceptedTypes.join(', ')}`;
    }
    
    if (file.size > maxSizeMB * 1024 * 1024) {
      return `Fichier trop volumineux. Maximum: ${maxSizeMB} MB`;
    }
    
    return null;
  };

  // Upload du fichier
  const uploadFile = async (file: File): Promise<string> => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(uploadUrl, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `Erreur upload: ${response.status}`);
    }

    const data = await response.json();
    return data.file_id;
  };

  // Analyse du fichier
  const analyzeFile = async (fileId: string): Promise<AnalysisResult> => {
    const response = await fetch(analyzeUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ file_id: fileId }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `Erreur analyse: ${response.status}`);
    }

    return response.json();
  };

  // Traitement d'un fichier
  const processFile = async (file: File) => {
    const id = generateId();
    const validationError = validateFile(file);

    if (validationError) {
      setError(validationError);
      return;
    }

    if (remainingUploads <= 0) {
      setError('Limite de démo atteinte. Créez un compte pour continuer.');
      return;
    }

    // Ajouter le fichier en état uploading
    const newFile: UploadedFile = {
      id,
      name: file.name,
      size: file.size,
      type: file.type,
      status: 'uploading',
      progress: 0,
    };
    setFiles(prev => [...prev, newFile]);
    setError(null);

    try {
      // Simuler la progression d'upload
      for (let i = 0; i <= 100; i += 20) {
        await new Promise(r => setTimeout(r, 100));
        setFiles(prev => prev.map(f => 
          f.id === id ? { ...f, progress: i } : f
        ));
      }

      // Upload réel
      const fileId = await uploadFile(file);

      // Passer en mode processing
      setFiles(prev => prev.map(f => 
        f.id === id ? { ...f, status: 'processing', progress: 100 } : f
      ));

      // Analyse
      const result = await analyzeFile(fileId);

      // Mettre à jour avec les résultats
      setFiles(prev => prev.map(f => 
        f.id === id ? { 
          ...f, 
          status: 'ready',
          summary: result.summary,
          keyPoints: result.key_points,
        } : f
      ));

      // Décrémenter le compteur
      setRemainingUploads(prev => prev - 1);

      // Callback
      if (onAnalysisComplete) {
        onAnalysisComplete(result);
      }

    } catch (err) {
      console.error('Erreur FileAI:', err);
      setFiles(prev => prev.map(f => 
        f.id === id ? { 
          ...f, 
          status: 'error',
          error: err instanceof Error ? err.message : 'Erreur inconnue',
        } : f
      ));
    }
  };

  // Drag & Drop handlers
  const handleDragEnter = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const droppedFiles = Array.from(e.dataTransfer.files);
    droppedFiles.forEach(processFile);
  }, [remainingUploads]);

  // File input handler
  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = Array.from(e.target.files || []);
    selectedFiles.forEach(processFile);
    
    // Reset input
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  // Supprimer un fichier
  const removeFile = (id: string) => {
    setFiles(prev => prev.filter(f => f.id !== id));
  };

  return (
    <div className={`
      bg-slate-900 border border-slate-700 rounded-2xl overflow-hidden
      shadow-xl shadow-black/20
      ${compact ? 'max-w-md' : 'max-w-2xl'} w-full
    `}>
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-cyan-600 px-4 py-3 flex items-center justify-between">
        <h3 className="text-white font-semibold text-sm flex items-center gap-2">
          {title}
        </h3>
        <span className="text-white/80 text-xs bg-white/20 px-2 py-1 rounded-full">
          {remainingUploads} upload{remainingUploads !== 1 ? 's' : ''} restant{remainingUploads !== 1 ? 's' : ''}
        </span>
      </div>

      {/* Zone de drop */}
      <div
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`
          m-4 p-8 border-2 border-dashed rounded-xl cursor-pointer
          transition-all duration-200 text-center
          ${isDragging 
            ? 'border-blue-400 bg-blue-500/10' 
            : 'border-slate-600 hover:border-blue-500 hover:bg-slate-800/50'}
          ${remainingUploads <= 0 ? 'opacity-50 cursor-not-allowed' : ''}
        `}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept={acceptedTypes.join(',')}
          onChange={handleFileSelect}
          className="hidden"
          disabled={remainingUploads <= 0}
        />
        
        <div className="text-4xl mb-3">
          {isDragging ? '📥' : '📎'}
        </div>
        <p className="text-slate-300 font-medium mb-1">
          {isDragging 
            ? 'Déposez le fichier ici' 
            : 'Glissez un fichier ou cliquez pour sélectionner'}
        </p>
        <p className="text-slate-500 text-sm">
          {acceptedTypes.join(', ')} • Max {maxSizeMB} MB
        </p>
      </div>

      {/* Error */}
      {error && (
        <div className="mx-4 mb-4 bg-red-900/30 border border-red-700 text-red-300 rounded-lg px-4 py-3 text-sm">
          ⚠️ {error}
        </div>
      )}

      {/* Liste des fichiers */}
      {files.length > 0 && (
        <div className="px-4 pb-4 space-y-3">
          {files.map((file) => (
            <div 
              key={file.id}
              className="bg-slate-800 rounded-xl p-4 border border-slate-700"
            >
              {/* Header fichier */}
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center gap-3">
                  <span className="text-2xl">{getFileIcon(file.type)}</span>
                  <div>
                    <p className="text-white font-medium text-sm truncate max-w-xs">
                      {file.name}
                    </p>
                    <p className="text-slate-500 text-xs">
                      {formatFileSize(file.size)}
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => removeFile(file.id)}
                  className="text-slate-500 hover:text-red-400 transition-colors"
                >
                  ✕
                </button>
              </div>

              {/* Progress bar */}
              {(file.status === 'uploading' || file.status === 'processing') && (
                <div className="mt-3">
                  <div className="flex justify-between text-xs text-slate-400 mb-1">
                    <span>
                      {file.status === 'uploading' ? 'Upload...' : 'Analyse en cours...'}
                    </span>
                    <span>{file.progress}%</span>
                  </div>
                  <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
                    <div 
                      className={`h-full transition-all duration-300 ${
                        file.status === 'processing' 
                          ? 'bg-gradient-to-r from-blue-500 to-cyan-500 animate-pulse' 
                          : 'bg-blue-500'
                      }`}
                      style={{ width: `${file.progress}%` }}
                    />
                  </div>
                </div>
              )}

              {/* Résultats */}
              {file.status === 'ready' && file.summary && (
                <div className="mt-3 pt-3 border-t border-slate-700">
                  <p className="text-xs text-slate-400 mb-2">📋 Résumé :</p>
                  <p className="text-sm text-slate-300 leading-relaxed">
                    {file.summary}
                  </p>
                  
                  {file.keyPoints && file.keyPoints.length > 0 && (
                    <div className="mt-3">
                      <p className="text-xs text-slate-400 mb-2">🎯 Points clés :</p>
                      <ul className="space-y-1">
                        {file.keyPoints.slice(0, 5).map((point, idx) => (
                          <li key={idx} className="text-sm text-slate-300 flex items-start gap-2">
                            <span className="text-blue-400">•</span>
                            {point}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}

              {/* Erreur */}
              {file.status === 'error' && (
                <div className="mt-3 text-red-400 text-sm">
                  ❌ {file.error}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Limite atteinte */}
      {remainingUploads <= 0 && (
        <div className="p-4 border-t border-slate-700 text-center">
          <p className="text-amber-400 text-sm mb-3">
            🔒 Limite de démo atteinte
          </p>
          <a 
            href="/auth/register" 
            className="inline-block bg-gradient-to-r from-blue-500 to-cyan-500 text-white px-6 py-2 rounded-lg font-semibold text-sm hover:opacity-90 transition-opacity"
          >
            Créer un compte gratuit →
          </a>
        </div>
      )}
    </div>
  );
};

export default FileAIUploader;
