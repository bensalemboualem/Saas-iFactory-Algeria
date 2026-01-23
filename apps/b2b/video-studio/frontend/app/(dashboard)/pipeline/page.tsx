"use client";

import { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Sparkles,
  Play,
  Loader2,
  Download,
  Film,
  Music,
  Mic,
  Wand2,
  Cpu,
  Zap,
  Clock,
  CheckCircle2,
  XCircle,
  ChevronRight,
  Settings2,
  Volume2,
  Subtitles,
  Scissors,
  RefreshCw,
  Pause,
  AlertTriangle,
  Rocket,
  Layers,
} from "lucide-react";
import { useLocaleStore, useThemeStore } from "@/lib/store";
import { isRTL } from "@/lib/i18n";

// Types
interface FreeModel {
  id: string;
  name: string;
  vram: string;
  duration: number;
  credits: number;
  quality: number;
  available: boolean;
}

interface MusicPreset {
  id: string;
  name: string;
  genre: string;
  duration: number;
  url?: string;
}

interface PipelineSegment {
  id: number;
  prompt: string;
  status: "pending" | "generating" | "completed" | "error";
  progress: number;
  videoUrl?: string;
  error?: string;
}

interface PipelineState {
  id?: string;
  status: "idle" | "scripting" | "generating" | "audio" | "montage" | "completed" | "error";
  currentStep: number;
  totalSteps: number;
  segments: PipelineSegment[];
  script?: string;
  audioUrl?: string;
  finalVideoUrl?: string;
  error?: string;
}

// Free models data
const FREE_MODELS: FreeModel[] = [
  { id: "wan-2.1", name: "Wan 2.1", vram: "8GB", duration: 5, credits: 0, quality: 4, available: true },
  { id: "cogvideox-2b", name: "CogVideoX 2B", vram: "8GB", duration: 6, credits: 0, quality: 3, available: true },
  { id: "cogvideox-5b", name: "CogVideoX 5B", vram: "12GB", duration: 6, credits: 2, quality: 4, available: false },
  { id: "ltx-video-2", name: "LTX Video 2", vram: "12GB", duration: 5, credits: 2, quality: 4, available: false },
  { id: "hunyuan-video", name: "HunyuanVideo", vram: "16GB", duration: 5, credits: 3, quality: 5, available: false },
];

// Music presets
const MUSIC_PRESETS: MusicPreset[] = [
  { id: "epic-cinematic", name: "Epic Cinematic", genre: "Cinematic", duration: 60 },
  { id: "upbeat-corporate", name: "Upbeat Corporate", genre: "Corporate", duration: 45 },
  { id: "ambient-chill", name: "Ambient Chill", genre: "Ambient", duration: 90 },
  { id: "arabic-traditional", name: "Arabic Traditional", genre: "World", duration: 60 },
  { id: "electronic-modern", name: "Electronic Modern", genre: "Electronic", duration: 45 },
  { id: "motivational", name: "Motivational", genre: "Inspirational", duration: 60 },
];

// Labels
const labels = {
  title: { fr: "Pipeline de Production", ar: "خط إنتاج الفيديو", en: "Production Pipeline" },
  subtitle: { fr: "Créez des vidéos longues avec IA", ar: "إنشاء فيديوهات طويلة بالذكاء الاصطناعي", en: "Create long videos with AI" },
  prompt: { fr: "Décrivez votre vidéo", ar: "صف الفيديو الخاص بك", en: "Describe your video" },
  promptPlaceholder: { 
    fr: "Ex: Une visite touristique d'Alger, montrant la Casbah, le port, la Grande Poste...", 
    ar: "مثال: جولة سياحية في الجزائر العاصمة، تظهر القصبة، الميناء، البريد المركزي...", 
    en: "Ex: A tourist tour of Algiers, showing the Casbah, the port, the Grande Poste..." 
  },
  duration: { fr: "Durée cible", ar: "المدة المستهدفة", en: "Target duration" },
  model: { fr: "Modèle de génération", ar: "نموذج التوليد", en: "Generation model" },
  freeModels: { fr: "Modèles gratuits (GPU local)", ar: "نماذج مجانية (GPU محلي)", en: "Free models (Local GPU)" },
  music: { fr: "Musique de fond", ar: "موسيقى خلفية", en: "Background music" },
  narration: { fr: "Narration vocale", ar: "السرد الصوتي", en: "Voice narration" },
  subtitles: { fr: "Sous-titres automatiques", ar: "ترجمة تلقائية", en: "Auto subtitles" },
  generate: { fr: "Lancer la Production", ar: "بدء الإنتاج", en: "Start Production" },
  generating: { fr: "Production en cours...", ar: "جاري الإنتاج...", en: "Producing..." },
  download: { fr: "Télécharger", ar: "تحميل", en: "Download" },
  step1: { fr: "Génération du script", ar: "إنشاء السيناريو", en: "Script generation" },
  step2: { fr: "Génération des segments", ar: "توليد المقاطع", en: "Segment generation" },
  step3: { fr: "Ajout audio & narration", ar: "إضافة الصوت والسرد", en: "Adding audio & narration" },
  step4: { fr: "Montage & transitions", ar: "المونتاج والانتقالات", en: "Editing & transitions" },
  step5: { fr: "Finalisation", ar: "التنفيذ النهائي", en: "Finalization" },
  credits: { fr: "crédits", ar: "أرصدة", en: "credits" },
  free: { fr: "Gratuit", ar: "مجاني", en: "Free" },
  requiresGpu: { fr: "Nécessite GPU local", ar: "يتطلب GPU محلي", en: "Requires local GPU" },
  seconds: { fr: "secondes", ar: "ثانية", en: "seconds" },
  segment: { fr: "Segment", ar: "مقطع", en: "Segment" },
  parallel: { fr: "Génération parallèle x3", ar: "توليد متوازي x3", en: "Parallel generation x3" },
  noMusic: { fr: "Sans musique", ar: "بدون موسيقى", en: "No music" },
  noNarration: { fr: "Sans narration", ar: "بدون سرد", en: "No narration" },
  darija: { fr: "Darija (Algérien)", ar: "الدارجة (جزائري)", en: "Darija (Algerian)" },
  french: { fr: "Français", ar: "فرنسي", en: "French" },
  arabic: { fr: "Arabe classique", ar: "عربي فصيح", en: "Classical Arabic" },
  english: { fr: "Anglais", ar: "إنجليزي", en: "English" },
};

export default function PipelinePage() {
  const { locale } = useLocaleStore();
  const { theme } = useThemeStore();
  const rtl = isRTL(locale);

  // Form state
  const [prompt, setPrompt] = useState("");
  const [targetDuration, setTargetDuration] = useState(30);
  const [selectedModel, setSelectedModel] = useState("wan-2.1");
  const [selectedMusic, setSelectedMusic] = useState<string | null>(null);
  const [narrationLang, setNarrationLang] = useState<string | null>(null);
  const [enableSubtitles, setEnableSubtitles] = useState(true);

  // Pipeline state
  const [pipeline, setPipeline] = useState<PipelineState>({
    status: "idle",
    currentStep: 0,
    totalSteps: 5,
    segments: [],
  });

  // Compute segments count
  const segmentsCount = Math.ceil(targetDuration / 5);
  const estimatedCredits = FREE_MODELS.find(m => m.id === selectedModel)?.credits || 0;
  const totalCredits = estimatedCredits * segmentsCount;

  // Start pipeline
  const handleStartPipeline = async () => {
    if (!prompt.trim()) return;

    // Initialize segments
    const initialSegments: PipelineSegment[] = Array.from({ length: segmentsCount }, (_, i) => ({
      id: i + 1,
      prompt: "",
      status: "pending",
      progress: 0,
    }));

    setPipeline({
      status: "scripting",
      currentStep: 1,
      totalSteps: 5,
      segments: initialSegments,
    });

    try {
      // Step 1: Generate script
      await simulateStep("scripting", 3000);
      
      // Generate segment prompts from main prompt
      const segmentPrompts = generateSegmentPrompts(prompt, segmentsCount);
      setPipeline(prev => ({
        ...prev,
        status: "generating",
        currentStep: 2,
        script: segmentPrompts.join("\n\n"),
        segments: prev.segments.map((seg, i) => ({
          ...seg,
          prompt: segmentPrompts[i] || prompt,
        })),
      }));

      // Step 2: Generate segments in parallel (3 at a time)
      await generateSegmentsParallel();

      // Step 3: Audio & narration
      setPipeline(prev => ({ ...prev, status: "audio", currentStep: 3 }));
      await simulateStep("audio", 2000);

      // Step 4: Montage
      setPipeline(prev => ({ ...prev, status: "montage", currentStep: 4 }));
      await simulateStep("montage", 3000);

      // Step 5: Finalization
      setPipeline(prev => ({
        ...prev,
        status: "completed",
        currentStep: 5,
        finalVideoUrl: "/demo-final-video.mp4",
      }));

    } catch (error) {
      setPipeline(prev => ({
        ...prev,
        status: "error",
        error: error instanceof Error ? error.message : "Pipeline failed",
      }));
    }
  };

  // Simulate step with delay
  const simulateStep = (step: string, duration: number) => {
    return new Promise(resolve => setTimeout(resolve, duration));
  };

  // Generate segment prompts from main prompt
  const generateSegmentPrompts = (mainPrompt: string, count: number): string[] => {
    // In production, this would call the API to generate AI-powered segment prompts
    const basePrompts = [
      `Opening shot: ${mainPrompt} - establishing wide angle view`,
      `Detail shot: ${mainPrompt} - focusing on key elements`,
      `Movement: ${mainPrompt} - dynamic camera motion`,
      `Close-up: ${mainPrompt} - intimate details`,
      `Transition: ${mainPrompt} - shifting perspective`,
      `Climax: ${mainPrompt} - dramatic moment`,
      `Resolution: ${mainPrompt} - concluding scene`,
    ];
    return basePrompts.slice(0, count);
  };

  // Generate segments in parallel
  const generateSegmentsParallel = async () => {
    const batchSize = 3;
    const segments = pipeline.segments;

    for (let i = 0; i < segments.length; i += batchSize) {
      const batch = segments.slice(i, i + batchSize);
      
      // Start batch
      setPipeline(prev => ({
        ...prev,
        segments: prev.segments.map((seg, idx) => 
          idx >= i && idx < i + batchSize
            ? { ...seg, status: "generating" as const, progress: 0 }
            : seg
        ),
      }));

      // Simulate parallel generation
      await Promise.all(
        batch.map((_, batchIdx) => 
          simulateSegmentGeneration(i + batchIdx)
        )
      );
    }
  };

  // Simulate single segment generation
  const simulateSegmentGeneration = async (segmentIndex: number) => {
    const duration = 2000 + Math.random() * 2000;
    const steps = 10;
    const stepDuration = duration / steps;

    for (let step = 1; step <= steps; step++) {
      await new Promise(resolve => setTimeout(resolve, stepDuration));
      setPipeline(prev => ({
        ...prev,
        segments: prev.segments.map((seg, idx) =>
          idx === segmentIndex
            ? { ...seg, progress: (step / steps) * 100 }
            : seg
        ),
      }));
    }

    // Complete segment
    setPipeline(prev => ({
      ...prev,
      segments: prev.segments.map((seg, idx) =>
        idx === segmentIndex
          ? { ...seg, status: "completed" as const, progress: 100, videoUrl: `/segment-${idx + 1}.mp4` }
          : seg
      ),
    }));
  };

  // Reset pipeline
  const handleReset = () => {
    setPipeline({
      status: "idle",
      currentStep: 0,
      totalSteps: 5,
      segments: [],
    });
  };

  // Render quality stars
  const renderQuality = (quality: number) => (
    <div className="flex gap-0.5">
      {[1, 2, 3, 4, 5].map(star => (
        <span
          key={star}
          className={star <= quality ? "text-yellow-400" : "text-gray-600"}
        >
          ★
        </span>
      ))}
    </div>
  );

  return (
    <div className={`min-h-screen p-8 ${theme === 'dark' ? 'bg-[#0a0a0f] text-white' : 'bg-gray-50 text-gray-900'}`} dir={rtl ? 'rtl' : 'ltr'}>
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 rounded-xl bg-gradient-to-br from-cyan-500/20 to-fuchsia-500/20">
              <Rocket className="w-6 h-6 text-cyan-400" />
            </div>
            <h1 className={`text-3xl font-bold ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
              {labels.title[locale]}
            </h1>
          </div>
          <p className={theme === 'dark' ? 'text-gray-400' : 'text-gray-600'}>
            {labels.subtitle[locale]}
          </p>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Left Column - Configuration */}
          <div className="lg:col-span-2 space-y-6">
            {/* Prompt */}
            <div className={`rounded-2xl p-6 border ${theme === 'dark' ? 'bg-[#141419] border-[#2a2a35]' : 'bg-white border-gray-200'}`}>
              <label className={`block text-sm font-medium mb-2 ${theme === 'dark' ? 'text-gray-300' : 'text-gray-700'}`}>
                {labels.prompt[locale]}
              </label>
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder={labels.promptPlaceholder[locale]}
                rows={4}
                className={`w-full px-4 py-3 rounded-xl border resize-none focus:ring-2 focus:ring-cyan-400 focus:border-transparent ${
                  theme === 'dark'
                    ? 'bg-[#0a0a0f] border-[#2a2a35] text-white placeholder-gray-500'
                    : 'bg-gray-50 border-gray-200 text-gray-900 placeholder-gray-400'
                }`}
                disabled={pipeline.status !== "idle"}
              />
            </div>

            {/* Duration & Model */}
            <div className="grid md:grid-cols-2 gap-6">
              {/* Duration */}
              <div className={`rounded-2xl p-6 border ${theme === 'dark' ? 'bg-[#141419] border-[#2a2a35]' : 'bg-white border-gray-200'}`}>
                <label className={`block text-sm font-medium mb-4 ${theme === 'dark' ? 'text-gray-300' : 'text-gray-700'}`}>
                  {labels.duration[locale]}
                </label>
                <div className="flex items-center gap-4">
                  {[15, 30, 60, 90].map(dur => (
                    <button
                      key={dur}
                      onClick={() => setTargetDuration(dur)}
                      disabled={pipeline.status !== "idle"}
                      className={`px-4 py-2 rounded-xl font-medium transition-all ${
                        targetDuration === dur
                          ? 'bg-gradient-to-r from-cyan-400 to-fuchsia-500 text-white'
                          : theme === 'dark'
                            ? 'bg-[#1a1a24] text-gray-400 hover:text-white border border-[#2a2a35]'
                            : 'bg-gray-100 text-gray-600 hover:text-gray-900 border border-gray-200'
                      }`}
                    >
                      {dur}s
                    </button>
                  ))}
                </div>
                <p className={`text-sm mt-3 ${theme === 'dark' ? 'text-gray-500' : 'text-gray-500'}`}>
                  = {segmentsCount} segments × 5s
                </p>
              </div>

              {/* Model Selector */}
              <div className={`rounded-2xl p-6 border ${theme === 'dark' ? 'bg-[#141419] border-[#2a2a35]' : 'bg-white border-gray-200'}`}>
                <label className={`block text-sm font-medium mb-4 ${theme === 'dark' ? 'text-gray-300' : 'text-gray-700'}`}>
                  {labels.model[locale]}
                </label>
                <select
                  value={selectedModel}
                  onChange={(e) => setSelectedModel(e.target.value)}
                  disabled={pipeline.status !== "idle"}
                  className={`w-full px-4 py-3 rounded-xl border focus:ring-2 focus:ring-cyan-400 ${
                    theme === 'dark'
                      ? 'bg-[#0a0a0f] border-[#2a2a35] text-white'
                      : 'bg-gray-50 border-gray-200 text-gray-900'
                  }`}
                >
                  {FREE_MODELS.map(model => (
                    <option key={model.id} value={model.id} disabled={!model.available}>
                      {model.name} ({model.vram}) - {model.credits === 0 ? labels.free[locale] : `${model.credits} ${labels.credits[locale]}`}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* Free Models Grid */}
            <div className={`rounded-2xl p-6 border ${theme === 'dark' ? 'bg-[#141419] border-[#2a2a35]' : 'bg-white border-gray-200'}`}>
              <div className="flex items-center gap-2 mb-4">
                <Cpu className="w-5 h-5 text-green-400" />
                <h3 className={`font-semibold ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
                  {labels.freeModels[locale]}
                </h3>
              </div>
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-3">
                {FREE_MODELS.map(model => (
                  <button
                    key={model.id}
                    onClick={() => model.available && setSelectedModel(model.id)}
                    disabled={!model.available || pipeline.status !== "idle"}
                    className={`p-4 rounded-xl border text-left transition-all ${
                      selectedModel === model.id
                        ? 'border-cyan-400 bg-cyan-400/10'
                        : model.available
                          ? theme === 'dark'
                            ? 'border-[#2a2a35] hover:border-cyan-400/50 bg-[#0a0a0f]'
                            : 'border-gray-200 hover:border-cyan-500/50 bg-gray-50'
                          : 'opacity-50 cursor-not-allowed border-gray-700 bg-gray-800/50'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <span className={`font-medium ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
                        {model.name}
                      </span>
                      {model.credits === 0 ? (
                        <span className="px-2 py-0.5 bg-green-500/20 text-green-400 text-xs rounded-full">
                          {labels.free[locale]}
                        </span>
                      ) : (
                        <span className="px-2 py-0.5 bg-cyan-500/20 text-cyan-400 text-xs rounded-full">
                          {model.credits} cr
                        </span>
                      )}
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span className={theme === 'dark' ? 'text-gray-500' : 'text-gray-500'}>
                        {model.vram} VRAM
                      </span>
                      {renderQuality(model.quality)}
                    </div>
                    {!model.available && (
                      <p className="text-xs text-yellow-500 mt-2">
                        {labels.requiresGpu[locale]}
                      </p>
                    )}
                  </button>
                ))}
              </div>
            </div>

            {/* Audio Options */}
            <div className="grid md:grid-cols-2 gap-6">
              {/* Music */}
              <div className={`rounded-2xl p-6 border ${theme === 'dark' ? 'bg-[#141419] border-[#2a2a35]' : 'bg-white border-gray-200'}`}>
                <div className="flex items-center gap-2 mb-4">
                  <Music className="w-5 h-5 text-fuchsia-400" />
                  <h3 className={`font-semibold ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
                    {labels.music[locale]}
                  </h3>
                </div>
                <div className="space-y-2 max-h-48 overflow-y-auto">
                  <button
                    onClick={() => setSelectedMusic(null)}
                    disabled={pipeline.status !== "idle"}
                    className={`w-full p-3 rounded-xl border text-left transition-all ${
                      selectedMusic === null
                        ? 'border-fuchsia-400 bg-fuchsia-400/10'
                        : theme === 'dark'
                          ? 'border-[#2a2a35] hover:border-fuchsia-400/50'
                          : 'border-gray-200 hover:border-fuchsia-500/50'
                    }`}
                  >
                    <span className={theme === 'dark' ? 'text-gray-400' : 'text-gray-600'}>
                      {labels.noMusic[locale]}
                    </span>
                  </button>
                  {MUSIC_PRESETS.map(preset => (
                    <button
                      key={preset.id}
                      onClick={() => setSelectedMusic(preset.id)}
                      disabled={pipeline.status !== "idle"}
                      className={`w-full p-3 rounded-xl border text-left transition-all ${
                        selectedMusic === preset.id
                          ? 'border-fuchsia-400 bg-fuchsia-400/10'
                          : theme === 'dark'
                            ? 'border-[#2a2a35] hover:border-fuchsia-400/50'
                            : 'border-gray-200 hover:border-fuchsia-500/50'
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <span className={theme === 'dark' ? 'text-white' : 'text-gray-900'}>
                          {preset.name}
                        </span>
                        <span className={`text-xs ${theme === 'dark' ? 'text-gray-500' : 'text-gray-500'}`}>
                          {preset.genre}
                        </span>
                      </div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Narration */}
              <div className={`rounded-2xl p-6 border ${theme === 'dark' ? 'bg-[#141419] border-[#2a2a35]' : 'bg-white border-gray-200'}`}>
                <div className="flex items-center gap-2 mb-4">
                  <Mic className="w-5 h-5 text-cyan-400" />
                  <h3 className={`font-semibold ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
                    {labels.narration[locale]}
                  </h3>
                </div>
                <div className="space-y-2">
                  {[
                    { id: null, label: labels.noNarration },
                    { id: "darija", label: labels.darija },
                    { id: "french", label: labels.french },
                    { id: "arabic", label: labels.arabic },
                    { id: "english", label: labels.english },
                  ].map(option => (
                    <button
                      key={option.id || "none"}
                      onClick={() => setNarrationLang(option.id)}
                      disabled={pipeline.status !== "idle"}
                      className={`w-full p-3 rounded-xl border text-left transition-all ${
                        narrationLang === option.id
                          ? 'border-cyan-400 bg-cyan-400/10'
                          : theme === 'dark'
                            ? 'border-[#2a2a35] hover:border-cyan-400/50'
                            : 'border-gray-200 hover:border-cyan-500/50'
                      }`}
                    >
                      <span className={narrationLang === option.id 
                        ? 'text-cyan-400' 
                        : theme === 'dark' ? 'text-gray-300' : 'text-gray-700'
                      }>
                        {option.label[locale]}
                      </span>
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Subtitles Toggle */}
            <div className={`rounded-2xl p-6 border ${theme === 'dark' ? 'bg-[#141419] border-[#2a2a35]' : 'bg-white border-gray-200'}`}>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Subtitles className="w-5 h-5 text-yellow-400" />
                  <div>
                    <h3 className={`font-semibold ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
                      {labels.subtitles[locale]}
                    </h3>
                    <p className={`text-sm ${theme === 'dark' ? 'text-gray-500' : 'text-gray-500'}`}>
                      {locale === 'ar' ? 'سيتم إنشاء ترجمة تلقائية للفيديو' : 
                       locale === 'en' ? 'Auto-generated subtitles will be added' :
                       'Des sous-titres seront générés automatiquement'}
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => setEnableSubtitles(!enableSubtitles)}
                  disabled={pipeline.status !== "idle"}
                  className={`w-14 h-8 rounded-full transition-colors ${
                    enableSubtitles 
                      ? 'bg-gradient-to-r from-cyan-400 to-fuchsia-500' 
                      : theme === 'dark' ? 'bg-gray-700' : 'bg-gray-300'
                  }`}
                >
                  <motion.div
                    className="w-6 h-6 bg-white rounded-full shadow-lg"
                    animate={{ x: enableSubtitles ? 26 : 4 }}
                    transition={{ type: "spring", stiffness: 500, damping: 30 }}
                  />
                </button>
              </div>
            </div>
          </div>

          {/* Right Column - Pipeline Status */}
          <div className="space-y-6">
            {/* Credits Summary */}
            <div className={`rounded-2xl p-6 border ${theme === 'dark' ? 'bg-gradient-to-br from-cyan-500/10 via-[#141419] to-fuchsia-500/10 border-[#2a2a35]' : 'bg-gradient-to-br from-cyan-50 via-white to-fuchsia-50 border-gray-200'}`}>
              <div className="flex items-center justify-between mb-4">
                <span className={theme === 'dark' ? 'text-gray-400' : 'text-gray-600'}>
                  {locale === 'ar' ? 'التكلفة المقدرة' : locale === 'en' ? 'Estimated cost' : 'Coût estimé'}
                </span>
                <div className="flex items-center gap-2">
                  <Sparkles className="w-5 h-5 text-cyan-400" />
                  <span className={`text-2xl font-bold ${totalCredits === 0 ? 'text-green-400' : theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
                    {totalCredits === 0 ? labels.free[locale] : `${totalCredits} ${labels.credits[locale]}`}
                  </span>
                </div>
              </div>
              
              <div className={`text-sm ${theme === 'dark' ? 'text-gray-500' : 'text-gray-500'}`}>
                <div className="flex justify-between">
                  <span>Segments</span>
                  <span>{segmentsCount} × {estimatedCredits} cr</span>
                </div>
                <div className="flex justify-between">
                  <span>Durée</span>
                  <span>{targetDuration}s</span>
                </div>
              </div>
            </div>

            {/* Generate Button */}
            <button
              onClick={pipeline.status === "idle" ? handleStartPipeline : handleReset}
              disabled={!prompt.trim() && pipeline.status === "idle"}
              className={`w-full py-4 rounded-2xl font-bold text-lg transition-all flex items-center justify-center gap-3 ${
                pipeline.status === "idle"
                  ? 'bg-gradient-to-r from-cyan-400 to-fuchsia-500 text-white hover:shadow-lg hover:shadow-cyan-500/30 disabled:opacity-50 disabled:cursor-not-allowed'
                  : pipeline.status === "completed"
                    ? 'bg-green-500 text-white'
                    : pipeline.status === "error"
                      ? 'bg-red-500 text-white'
                      : 'bg-gradient-to-r from-cyan-400 to-fuchsia-500 text-white animate-pulse'
              }`}
            >
              {pipeline.status === "idle" ? (
                <>
                  <Play className="w-6 h-6" />
                  {labels.generate[locale]}
                </>
              ) : pipeline.status === "completed" ? (
                <>
                  <RefreshCw className="w-6 h-6" />
                  {locale === 'ar' ? 'إعادة' : locale === 'en' ? 'New Video' : 'Nouvelle vidéo'}
                </>
              ) : pipeline.status === "error" ? (
                <>
                  <RefreshCw className="w-6 h-6" />
                  {locale === 'ar' ? 'إعادة المحاولة' : locale === 'en' ? 'Retry' : 'Réessayer'}
                </>
              ) : (
                <>
                  <Loader2 className="w-6 h-6 animate-spin" />
                  {labels.generating[locale]}
                </>
              )}
            </button>

            {/* Pipeline Progress */}
            <AnimatePresence>
              {pipeline.status !== "idle" && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  className={`rounded-2xl p-6 border ${theme === 'dark' ? 'bg-[#141419] border-[#2a2a35]' : 'bg-white border-gray-200'}`}
                >
                  <h3 className={`font-semibold mb-4 ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
                    {locale === 'ar' ? 'مراحل الإنتاج' : locale === 'en' ? 'Production Steps' : 'Étapes de production'}
                  </h3>
                  
                  <div className="space-y-3">
                    {[
                      { step: 1, label: labels.step1, status: "scripting" },
                      { step: 2, label: labels.step2, status: "generating" },
                      { step: 3, label: labels.step3, status: "audio" },
                      { step: 4, label: labels.step4, status: "montage" },
                      { step: 5, label: labels.step5, status: "completed" },
                    ].map(({ step, label, status }) => {
                      const isCompleted = pipeline.currentStep > step;
                      const isActive = pipeline.currentStep === step;
                      const isPending = pipeline.currentStep < step;

                      return (
                        <div
                          key={step}
                          className={`flex items-center gap-3 p-3 rounded-xl transition-all ${
                            isActive ? 'bg-cyan-400/10 border border-cyan-400/30' : ''
                          }`}
                        >
                          <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                            isCompleted 
                              ? 'bg-green-500 text-white'
                              : isActive
                                ? 'bg-cyan-400 text-white'
                                : theme === 'dark' ? 'bg-gray-700 text-gray-500' : 'bg-gray-200 text-gray-400'
                          }`}>
                            {isCompleted ? (
                              <CheckCircle2 className="w-5 h-5" />
                            ) : isActive ? (
                              <Loader2 className="w-5 h-5 animate-spin" />
                            ) : (
                              step
                            )}
                          </div>
                          <span className={`${
                            isCompleted || isActive 
                              ? theme === 'dark' ? 'text-white' : 'text-gray-900'
                              : theme === 'dark' ? 'text-gray-500' : 'text-gray-400'
                          }`}>
                            {label[locale]}
                          </span>
                        </div>
                      );
                    })}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Segments Progress */}
            <AnimatePresence>
              {pipeline.segments.length > 0 && pipeline.status === "generating" && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  className={`rounded-2xl p-6 border ${theme === 'dark' ? 'bg-[#141419] border-[#2a2a35]' : 'bg-white border-gray-200'}`}
                >
                  <div className="flex items-center justify-between mb-4">
                    <h3 className={`font-semibold ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
                      {labels.segment[locale]}s
                    </h3>
                    <span className="text-xs px-2 py-1 bg-cyan-400/20 text-cyan-400 rounded-full">
                      {labels.parallel[locale]}
                    </span>
                  </div>
                  
                  <div className="space-y-3">
                    {pipeline.segments.map(segment => (
                      <div key={segment.id} className="flex items-center gap-3">
                        <div className={`w-6 h-6 rounded-full flex items-center justify-center text-xs ${
                          segment.status === "completed"
                            ? 'bg-green-500 text-white'
                            : segment.status === "generating"
                              ? 'bg-cyan-400 text-white'
                              : theme === 'dark' ? 'bg-gray-700 text-gray-400' : 'bg-gray-200 text-gray-500'
                        }`}>
                          {segment.status === "completed" ? (
                            <CheckCircle2 className="w-4 h-4" />
                          ) : segment.status === "generating" ? (
                            <Loader2 className="w-4 h-4 animate-spin" />
                          ) : (
                            segment.id
                          )}
                        </div>
                        <div className="flex-1">
                          <div className={`h-2 rounded-full overflow-hidden ${theme === 'dark' ? 'bg-gray-700' : 'bg-gray-200'}`}>
                            <motion.div
                              className="h-full bg-gradient-to-r from-cyan-400 to-fuchsia-500"
                              initial={{ width: 0 }}
                              animate={{ width: `${segment.progress}%` }}
                              transition={{ duration: 0.3 }}
                            />
                          </div>
                        </div>
                        <span className={`text-sm ${theme === 'dark' ? 'text-gray-400' : 'text-gray-500'}`}>
                          {Math.round(segment.progress)}%
                        </span>
                      </div>
                    ))}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Final Video */}
            <AnimatePresence>
              {pipeline.status === "completed" && pipeline.finalVideoUrl && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className={`rounded-2xl p-6 border ${theme === 'dark' ? 'bg-[#141419] border-green-500/30' : 'bg-white border-green-500/30'}`}
                >
                  <div className="flex items-center gap-2 mb-4">
                    <CheckCircle2 className="w-6 h-6 text-green-500" />
                    <h3 className={`font-semibold ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
                      {locale === 'ar' ? 'الفيديو جاهز!' : locale === 'en' ? 'Video Ready!' : 'Vidéo prête !'}
                    </h3>
                  </div>
                  
                  <div className="aspect-video bg-black rounded-xl mb-4 flex items-center justify-center">
                    <Film className="w-16 h-16 text-gray-600" />
                  </div>
                  
                  <div className="grid grid-cols-2 gap-3">
                    <button className="py-3 rounded-xl bg-gradient-to-r from-cyan-400 to-fuchsia-500 text-white font-medium flex items-center justify-center gap-2">
                      <Download className="w-5 h-5" />
                      MP4
                    </button>
                    <button className={`py-3 rounded-xl font-medium flex items-center justify-center gap-2 border ${
                      theme === 'dark' ? 'border-[#2a2a35] text-white hover:border-cyan-400' : 'border-gray-200 text-gray-900 hover:border-cyan-500'
                    }`}>
                      <Scissors className="w-5 h-5" />
                      Shorts
                    </button>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </div>
    </div>
  );
}
