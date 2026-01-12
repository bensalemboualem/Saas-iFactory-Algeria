"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Sparkles, Upload, Play, Loader2, Download, RefreshCw, AlertTriangle } from "lucide-react";
import { useDropzone } from "react-dropzone";
import toast from "react-hot-toast";
import ModelSelector from "@/components/studio/model-selector";
import { DEFAULT_VIDEO_MODEL, getModelById } from "@/lib/providers";
import { useLocaleStore, useThemeStore } from "@/lib/store";
import { t, isRTL } from "@/lib/i18n";

type GenerationMode = "text-to-video" | "image-to-video";

interface GenerationState {
  status: "idle" | "generating" | "completed" | "error";
  progress: number;
  videoUrl?: string;
  error?: string;
}

export default function StudioPage() {
  const [mode, setMode] = useState<GenerationMode>("text-to-video");
  const [prompt, setPrompt] = useState("");
  const [selectedModel, setSelectedModel] = useState(DEFAULT_VIDEO_MODEL);
  const [uploadedImage, setUploadedImage] = useState<string | null>(null);
  const [generation, setGeneration] = useState<GenerationState>({
    status: "idle",
    progress: 0,
  });

  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const { locale } = useLocaleStore();
  const { theme } = useThemeStore();
  const rtl = isRTL(locale);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: { "image/*": [".png", ".jpg", ".jpeg", ".webp"] },
    maxFiles: 1,
    onDrop: (files) => {
      if (files[0]) {
        setUploadedFile(files[0]);
        const reader = new FileReader();
        reader.onload = () => {
          setUploadedImage(reader.result as string);
        };
        reader.readAsDataURL(files[0]);
      }
    },
  });

  const handleGenerate = async () => {
    if (mode === "text-to-video" && !prompt.trim()) {
      toast.error("Veuillez entrer une description");
      return;
    }
    if (mode === "image-to-video" && !uploadedImage) {
      toast.error("Veuillez uploader une image");
      return;
    }

    setGeneration({ status: "generating", progress: 0 });

    try {
      const model = getModelById(selectedModel);
      
      // Use Replicate API
      const response = await fetch('/api/replicate/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model_id: selectedModel,
          prompt,
          type: mode,
          image_url: mode === 'image-to-video' ? uploadedImage : undefined,
          negative_prompt: 'blurry, low quality, distorted, ugly, watermark',
        }),
      });

      // Simulate progress while waiting
      const progressInterval = setInterval(() => {
        setGeneration(prev => ({
          ...prev,
          progress: Math.min(prev.progress + Math.random() * 10, 90)
        }));
      }, 1000);

      const result = await response.json();
      clearInterval(progressInterval);

      if (!response.ok) {
        throw new Error(result.error || 'Generation failed');
      }
      
      setGeneration({
        status: "completed",
        progress: 100,
        videoUrl: result.url,
      });
      toast.success("Vidéo générée avec succès!");
    } catch (error) {
      console.error("Generation error:", error);
      setGeneration({
        status: "error",
        progress: 0,
        error: error instanceof Error ? error.message : "Erreur lors de la génération",
      });
      toast.error("Erreur lors de la génération");
    }
  };

  return (
    <div className={`p-8 ${theme === 'dark' ? 'bg-[#0a0a0f]' : 'bg-gray-50'}`} dir={rtl ? 'rtl' : 'ltr'}>
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className={`text-3xl font-bold mb-2 ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
            {t("studio.title", locale)}
          </h1>
          <p className={theme === 'dark' ? 'text-gray-400' : 'text-gray-600'}>
            {t("studio.description", locale)}
          </p>
        </div>

        {/* Mode selector */}
        <div className="flex gap-4 mb-8">
          {[
            { id: "text-to-video", label: t("features.text2video.title", locale), icon: Sparkles },
            { id: "image-to-video", label: t("features.img2video.title", locale), icon: Upload },
          ].map((m) => (
            <button
              key={m.id}
              onClick={() => setMode(m.id as GenerationMode)}
              className={`flex items-center gap-2 px-6 py-3 rounded-xl font-medium transition-all ${
                mode === m.id
                  ? "bg-gradient-to-r from-cyan-500 to-fuchsia-500 text-white shadow-lg shadow-cyan-500/25"
                  : theme === 'dark'
                    ? "bg-[#12121a] border border-[#2a2a35] text-gray-300 hover:border-cyan-400/50"
                    : "bg-white border border-gray-200 text-gray-700 hover:border-cyan-500/50"
              }`}
            >
              <m.icon className="w-5 h-5" />
              {m.label}
            </button>
          ))}
        </div>

        {/* Model Selector */}
        <div className="mb-8">
          <label className={`block text-sm font-medium mb-2 ${theme === 'dark' ? 'text-gray-300' : 'text-gray-700'}`}>
            {locale === 'ar' ? 'نموذج الذكاء الاصطناعي' : locale === 'en' ? 'AI Model' : 'Modèle IA'}
          </label>
          <ModelSelector
            type={mode}
            selectedModel={selectedModel}
            onModelChange={setSelectedModel}
          />
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Input panel */}
          <div className="space-y-6">
            {mode === "text-to-video" ? (
              <div>
                <label className="block text-sm font-medium mb-2">
                  Description de la vidéo
                </label>
                <textarea
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  placeholder="Ex: Un coucher de soleil sur le Sahara algérien, avec des dunes dorées qui ondulent sous une brise légère..."
                  className="w-full h-40 px-4 py-3 bg-surface border border-border rounded-xl resize-none focus:outline-none focus:ring-2 focus:ring-primary placeholder:text-text-muted"
                />
                <p className="mt-2 text-sm text-text-muted">
                  Soyez descriptif pour de meilleurs résultats. Vous pouvez écrire en français ou en Darija.
                </p>
              </div>
            ) : (
              <div>
                <label className="block text-sm font-medium mb-2">
                  Image source
                </label>
                <div
                  {...getRootProps()}
                  className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-colors ${
                    isDragActive
                      ? "border-primary bg-primary/10"
                      : "border-border hover:border-primary/50"
                  }`}
                >
                  <input {...getInputProps()} />
                  {uploadedImage ? (
                    <div className="relative">
                      <img
                        src={uploadedImage}
                        alt="Uploaded"
                        className="max-h-48 mx-auto rounded-lg"
                      />
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          setUploadedImage(null);
                        }}
                        className="absolute top-2 right-2 p-2 bg-error rounded-full hover:bg-error/80"
                      >
                        <RefreshCw className="w-4 h-4" />
                      </button>
                    </div>
                  ) : (
                    <>
                      <Upload className="w-12 h-12 mx-auto mb-4 text-text-muted" />
                      <p className="text-text-muted">
                        Glissez une image ici ou cliquez pour sélectionner
                      </p>
                      <p className="text-sm text-text-muted mt-2">
                        PNG, JPG, WEBP (max. 10MB)
                      </p>
                    </>
                  )}
                </div>

                {uploadedImage && (
                  <div className="mt-4">
                    <label className="block text-sm font-medium mb-2">
                      Instructions de mouvement (optionnel)
                    </label>
                    <textarea
                      value={prompt}
                      onChange={(e) => setPrompt(e.target.value)}
                      placeholder="Ex: Zoom lent vers l'avant, le personnage tourne la tête..."
                      className="w-full h-24 px-4 py-3 bg-surface border border-border rounded-xl resize-none focus:outline-none focus:ring-2 focus:ring-primary placeholder:text-text-muted"
                    />
                  </div>
                )}
              </div>
            )}

            {/* Generation settings */}
            <div className="p-4 bg-surface rounded-xl border border-border">
              <h3 className="font-medium mb-4">Paramètres</h3>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm text-text-muted mb-2">Durée</label>
                  <select className="w-full px-3 py-2 bg-background border border-border rounded-lg">
                    <option value="5">5 secondes</option>
                    <option value="10">10 secondes</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm text-text-muted mb-2">Ratio</label>
                  <select className="w-full px-3 py-2 bg-background border border-border rounded-lg">
                    <option value="16:9">16:9 (Paysage)</option>
                    <option value="9:16">9:16 (Portrait)</option>
                    <option value="1:1">1:1 (Carré)</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Generate button */}
            <button
              onClick={handleGenerate}
              disabled={generation.status === "generating"}
              className="w-full py-4 bg-primary hover:bg-primary-hover disabled:opacity-50 disabled:cursor-not-allowed rounded-xl font-semibold text-lg flex items-center justify-center gap-2 transition-colors"
            >
              {generation.status === "generating" ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Génération en cours...
                </>
              ) : (
                <>
                  <Sparkles className="w-5 h-5" />
                  Générer la Vidéo
                </>
              )}
            </button>

            {/* Credits info */}
            <p className="text-center text-sm text-text-muted">
              Coût estimé: <span className="text-primary font-medium">10 crédits</span> • 
              Solde: <span className="text-success font-medium">150 crédits</span>
            </p>
          </div>

          {/* Preview panel */}
          <div>
            <label className="block text-sm font-medium mb-2">Aperçu</label>
            <div className="video-container bg-surface border border-border flex items-center justify-center">
              {generation.status === "generating" ? (
                <div className="text-center">
                  <Loader2 className="w-16 h-16 mx-auto mb-4 text-primary animate-spin" />
                  <p className="text-text-muted mb-2">Génération en cours...</p>
                  <div className="w-48 h-2 bg-background rounded-full overflow-hidden mx-auto">
                    <motion.div
                      className="h-full bg-primary"
                      initial={{ width: 0 }}
                      animate={{ width: `${generation.progress}%` }}
                    />
                  </div>
                  <p className="text-sm text-text-muted mt-2">
                    {Math.round(generation.progress)}%
                  </p>
                </div>
              ) : generation.status === "completed" && generation.videoUrl ? (
                <div className="w-full h-full relative">
                  <video
                    src={generation.videoUrl}
                    controls
                    className="w-full h-full object-contain"
                  />
                  <button className="absolute bottom-4 right-4 px-4 py-2 bg-primary hover:bg-primary-hover rounded-lg flex items-center gap-2">
                    <Download className="w-4 h-4" />
                    Télécharger
                  </button>
                </div>
              ) : (
                <div className="text-center">
                  <Play className="w-16 h-16 mx-auto mb-4 text-text-muted" />
                  <p className="text-text-muted">
                    Votre vidéo apparaîtra ici
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
