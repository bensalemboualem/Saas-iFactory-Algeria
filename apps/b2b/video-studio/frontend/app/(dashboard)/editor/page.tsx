"use client";

import { useState, useRef, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Play,
  Pause,
  SkipBack,
  SkipForward,
  Volume2,
  Maximize,
  Scissors,
  Trash2,
  Copy,
  Lock,
  Unlock,
  Eye,
  EyeOff,
  Plus,
  Upload,
  Video,
  Music,
  Image,
  Wand2,
  Sparkles,
  Download,
  Save,
  Undo,
  Redo,
  ZoomIn,
  ZoomOut,
  Layers,
  Settings,
  Film,
} from "lucide-react";
import { useLocaleStore, useThemeStore } from "@/lib/store";
import { t, isRTL } from "@/lib/i18n";

// Types
interface MediaItem {
  id: string;
  type: "video" | "audio" | "image";
  name: string;
  duration?: number;
  thumbnail?: string;
  url?: string;
}

interface TimelineClip {
  id: string;
  trackId: string;
  mediaId: string;
  startTime: number;
  duration: number;
  color: string;
  name: string;
}

interface Track {
  id: string;
  name: string;
  type: "video" | "audio";
  locked: boolean;
  visible: boolean;
  clips: TimelineClip[];
}

// Couleurs des clips
const CLIP_COLORS = ["#ff6b6b", "#4ecdc4", "#ffe66d", "#a8dadc", "#ff00ff", "#00f0ff"];

export default function EditorPage() {
  const { locale } = useLocaleStore();
  const { theme } = useThemeStore();
  const rtl = isRTL(locale);
  
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration] = useState(300); // 5 minutes
  const [zoom, setZoom] = useState(1);
  const [activeTab, setActiveTab] = useState<"video" | "audio" | "image">("video");
  const [selectedClip, setSelectedClip] = useState<string | null>(null);
  
  // Media library
  const [mediaItems] = useState<MediaItem[]>([
    { id: "1", type: "video", name: "Intro.mp4", duration: 15 },
    { id: "2", type: "video", name: "Scene_01.mp4", duration: 45 },
    { id: "3", type: "video", name: "Interview.mp4", duration: 120 },
    { id: "4", type: "audio", name: "Music_bg.mp3", duration: 180 },
    { id: "5", type: "image", name: "Logo.png" },
    { id: "6", type: "image", name: "Overlay.png" },
  ]);

  // Tracks
  const [tracks, setTracks] = useState<Track[]>([
    {
      id: "v1",
      name: "Video 1",
      type: "video",
      locked: false,
      visible: true,
      clips: [
        { id: "c1", trackId: "v1", mediaId: "1", startTime: 0, duration: 15, color: CLIP_COLORS[0], name: "Intro" },
        { id: "c2", trackId: "v1", mediaId: "2", startTime: 20, duration: 45, color: CLIP_COLORS[1], name: "Scene 01" },
      ],
    },
    {
      id: "v2",
      name: "Video 2",
      type: "video",
      locked: false,
      visible: true,
      clips: [
        { id: "c3", trackId: "v2", mediaId: "3", startTime: 10, duration: 30, color: CLIP_COLORS[2], name: "Overlay" },
      ],
    },
    {
      id: "a1",
      name: "Audio 1",
      type: "audio",
      locked: false,
      visible: true,
      clips: [
        { id: "c4", trackId: "a1", mediaId: "4", startTime: 0, duration: 120, color: CLIP_COLORS[3], name: "Music" },
      ],
    },
  ]);

  // Properties panel state
  const [properties, setProperties] = useState({
    opacity: 100,
    scale: 100,
    rotation: 0,
    posX: 0,
    posY: 0,
  });

  const formatTimecode = (seconds: number) => {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = Math.floor(seconds % 60);
    const f = Math.floor((seconds % 1) * 30);
    return `${h.toString().padStart(2, "0")}:${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}:${f.toString().padStart(2, "0")}`;
  };

  const toggleTrackLock = (trackId: string) => {
    setTracks((prev) =>
      prev.map((t) => (t.id === trackId ? { ...t, locked: !t.locked } : t))
    );
  };

  const toggleTrackVisibility = (trackId: string) => {
    setTracks((prev) =>
      prev.map((t) => (t.id === trackId ? { ...t, visible: !t.visible } : t))
    );
  };

  return (
    <div className={`h-screen overflow-hidden flex flex-col ${theme === 'dark' ? 'bg-[#0a0a0f] text-white' : 'bg-gray-100 text-gray-900'}`} dir={rtl ? 'rtl' : 'ltr'}>
      {/* Animated Background */}
      <div className="fixed inset-0 opacity-[0.03] pointer-events-none z-0">
        <div className="absolute inset-0 bg-gradient-radial from-cyan-500/20 via-transparent to-transparent" 
             style={{ background: "radial-gradient(circle at 20% 50%, rgba(0,240,255,0.15), transparent 50%)" }} />
        <div className="absolute inset-0" 
             style={{ background: "radial-gradient(circle at 80% 80%, rgba(255,0,255,0.15), transparent 50%)" }} />
      </div>

      {/* Header */}
      <header className={`relative z-10 h-[60px] border-b-2 flex items-center justify-between px-6 ${
        theme === 'dark' ? 'bg-[#141419] border-[#2a2a35]' : 'bg-white border-gray-200'
      }`}>
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-cyan-400 to-fuchsia-500 flex items-center justify-center font-bold text-sm text-white shadow-lg shadow-cyan-500/40">
            IA
          </div>
          <span className="font-mono font-bold text-lg bg-gradient-to-r from-cyan-400 to-fuchsia-500 bg-clip-text text-transparent">
            {locale === 'ar' ? 'استوديو IA Factory' : 'IA Factory Studio'}
          </span>
        </div>

        <div className="flex items-center gap-3">
          <button className={`flex items-center gap-2 px-3 py-2 rounded-lg border transition-all text-sm ${
            theme === 'dark' ? 'bg-[#1a1a24] border-[#2a2a35] hover:border-cyan-400' : 'bg-white border-gray-200 hover:border-cyan-500'
          }`}>
            <Undo className="w-4 h-4" />
          </button>
          <button className={`flex items-center gap-2 px-3 py-2 rounded-lg border transition-all text-sm ${
            theme === 'dark' ? 'bg-[#1a1a24] border-[#2a2a35] hover:border-cyan-400' : 'bg-white border-gray-200 hover:border-cyan-500'
          }`}>
            <Redo className="w-4 h-4" />
          </button>
          <button className={`flex items-center gap-2 px-4 py-2 rounded-lg border transition-all text-sm font-semibold ${
            theme === 'dark' ? 'bg-[#1a1a24] border-[#2a2a35] hover:border-cyan-400' : 'bg-white border-gray-200 hover:border-cyan-500'
          }`}>
            <Save className="w-4 h-4" />
            {t("editor.save", locale)}
          </button>
          <button className="flex items-center gap-2 px-4 py-2 rounded-lg bg-gradient-to-r from-cyan-400 to-fuchsia-500 text-white font-semibold text-sm shadow-lg shadow-cyan-500/30 hover:shadow-cyan-500/50 hover:-translate-y-0.5 transition-all">
            <Download className="w-4 h-4" />
            {t("editor.export", locale)}
          </button>
        </div>
      </header>

      {/* Main Content */}
      <div className={`flex-1 relative z-10 grid grid-cols-[280px_1fr_320px] gap-px ${theme === 'dark' ? 'bg-[#2a2a35]' : 'bg-gray-300'}`}>
        {/* Media Library */}
        <div className={`p-5 overflow-y-auto ${theme === 'dark' ? 'bg-[#141419]' : 'bg-white'}`}>
          <div className="flex items-center gap-2 mb-4">
            <div className="w-0.5 h-3 bg-gradient-to-b from-cyan-400 to-fuchsia-500 rounded" />
            <span className={`text-[11px] font-bold uppercase tracking-wider ${theme === 'dark' ? 'text-gray-400' : 'text-gray-500'}`}>
              {t("editor.library", locale)}
            </span>
          </div>

          {/* Tabs */}
          <div className="flex gap-2 mb-4">
            {[
              { id: "video", icon: Video, label: locale === 'ar' ? 'فيديو' : locale === 'en' ? 'Video' : 'Vidéo' },
              { id: "audio", icon: Music, label: locale === 'ar' ? 'صوت' : 'Audio' },
              { id: "image", icon: Image, label: 'Image' },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as typeof activeTab)}
                className={`flex-1 flex items-center justify-center gap-1.5 py-2 px-3 rounded-md text-[11px] font-semibold transition-all ${
                  activeTab === tab.id
                    ? "bg-cyan-400 text-[#0a0a0f]"
                    : theme === 'dark' 
                      ? "bg-[#1a1a24] border border-[#2a2a35] hover:border-cyan-400/50"
                      : "bg-gray-100 border border-gray-200 hover:border-cyan-500/50"
                }`}
              >
                <tab.icon className="w-3.5 h-3.5" />
                {tab.label}
              </button>
            ))}
          </div>

          {/* Upload Button */}
          <button className={`w-full flex items-center justify-center gap-2 py-3 mb-4 rounded-lg border-2 border-dashed transition-all ${
            theme === 'dark' ? 'border-[#2a2a35] hover:border-cyan-400 text-gray-400' : 'border-gray-300 hover:border-cyan-500 text-gray-500'
          } hover:text-cyan-400`}>
            <Upload className="w-4 h-4" />
            <span className="text-sm font-medium">{t("editor.import", locale)}</span>
          </button>

          {/* Media Grid */}
          <div className="grid grid-cols-2 gap-3">
            {mediaItems
              .filter((m) => m.type === activeTab)
              .map((item) => (
                <motion.div
                  key={item.id}
                  whileHover={{ scale: 1.05 }}
                  className={`aspect-video rounded-lg overflow-hidden cursor-pointer border-2 border-transparent hover:border-cyan-400 hover:shadow-lg hover:shadow-cyan-500/30 transition-all ${
                    theme === 'dark' ? 'bg-[#1a1a24]' : 'bg-gray-200'
                  }`}
                >
                  <div className={`w-full h-full flex items-center justify-center text-3xl ${
                    theme === 'dark' ? 'bg-gradient-to-br from-[#1a1a24] to-[#0a0a0f]' : 'bg-gradient-to-br from-gray-200 to-gray-300'
                  }`}>
                    {item.type === "video" && "🎬"}
                    {item.type === "audio" && "🎵"}
                    {item.type === "image" && "🖼️"}
                  </div>
                  <div className="absolute bottom-0 left-0 right-0 p-2 bg-gradient-to-t from-black/90 to-transparent">
                    <p className="text-[10px] font-semibold truncate">{item.name}</p>
                    {item.duration && (
                      <p className="text-[9px] text-gray-400">{item.duration}s</p>
                    )}
                  </div>
                </motion.div>
              ))}
          </div>
        </div>

        {/* Preview Area */}
        <div className={`flex flex-col p-5 ${theme === 'dark' ? 'bg-[#141419]' : 'bg-white'}`}>
          {/* Preview Tools */}
          <div className="flex gap-2 mb-4">
            {[
              { icon: Scissors, label: locale === 'ar' ? 'قص' : locale === 'en' ? 'Cut' : 'Couper' },
              { icon: Copy, label: locale === 'ar' ? 'نسخ' : locale === 'en' ? 'Copy' : 'Copier' },
              { icon: Trash2, label: locale === 'ar' ? 'حذف' : locale === 'en' ? 'Delete' : 'Supprimer' },
              { icon: Wand2, label: locale === 'ar' ? 'سحر ذكاء' : 'IA Magic' },
            ].map((tool, i) => (
              <button
                key={i}
                className={`flex items-center gap-2 px-3 py-2 rounded-lg border transition-all text-sm ${
                  theme === 'dark' ? 'bg-[#1a1a24] border-[#2a2a35] hover:border-cyan-400' : 'bg-gray-100 border-gray-200 hover:border-cyan-500'
                }`}
              >
                <tool.icon className="w-4 h-4" />
                <span className="hidden lg:inline text-xs">{tool.label}</span>
              </button>
            ))}
            <div className="flex-1" />
            <button className="flex items-center gap-2 px-3 py-2 rounded-lg bg-gradient-to-r from-fuchsia-500 to-cyan-400 text-white font-semibold text-sm">
              <Sparkles className="w-4 h-4" />
              {t("editor.aiGeneration", locale)}
            </button>
          </div>

          {/* Preview Screen */}
          <div className={`flex-1 rounded-xl border-2 overflow-hidden flex items-center justify-center ${theme === 'dark' ? 'bg-[#0a0a0f] border-[#2a2a35]' : 'bg-gray-100 border-gray-200'}`}>
            <div className="text-6xl opacity-30">
              <Film />
            </div>
          </div>

          {/* Playback Controls */}
          <div className="mt-4 flex items-center justify-center gap-3">
            <button className="w-10 h-10 rounded-full bg-[#1a1a24] border-2 border-[#2a2a35] flex items-center justify-center hover:bg-cyan-400 hover:text-[#0a0a0f] hover:border-cyan-400 transition-all">
              <SkipBack className="w-5 h-5" />
            </button>
            <button
              onClick={() => setIsPlaying(!isPlaying)}
              className="w-14 h-14 rounded-full bg-gradient-to-r from-cyan-400 to-fuchsia-500 flex items-center justify-center text-[#0a0a0f] shadow-lg shadow-cyan-500/30"
            >
              {isPlaying ? <Pause className="w-7 h-7" /> : <Play className="w-7 h-7 ml-1" />}
            </button>
            <button className="w-10 h-10 rounded-full bg-[#1a1a24] border-2 border-[#2a2a35] flex items-center justify-center hover:bg-cyan-400 hover:text-[#0a0a0f] hover:border-cyan-400 transition-all">
              <SkipForward className="w-5 h-5" />
            </button>
            <span className="font-mono text-cyan-400 font-semibold mx-4">
              {formatTimecode(currentTime)}
            </span>
            <span className="text-gray-500">/</span>
            <span className="font-mono text-gray-400 mx-2">
              {formatTimecode(duration)}
            </span>
            <button className="w-10 h-10 rounded-full bg-[#1a1a24] border-2 border-[#2a2a35] flex items-center justify-center hover:bg-cyan-400 hover:text-[#0a0a0f] hover:border-cyan-400 transition-all">
              <Volume2 className="w-5 h-5" />
            </button>
            <button className="w-10 h-10 rounded-full bg-[#1a1a24] border-2 border-[#2a2a35] flex items-center justify-center hover:bg-cyan-400 hover:text-[#0a0a0f] hover:border-cyan-400 transition-all">
              <Maximize className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Properties Panel */}
        <div className={`p-5 overflow-y-auto ${theme === 'dark' ? 'bg-[#141419]' : 'bg-white'}`}>
          <div className="flex items-center gap-2 mb-4">
            <div className="w-0.5 h-3 bg-gradient-to-b from-cyan-400 to-fuchsia-500 rounded" />
            <span className={`text-[11px] font-bold uppercase tracking-wider ${theme === 'dark' ? 'text-gray-400' : 'text-gray-500'}`}>
              {t("editor.properties", locale)}
            </span>
          </div>

          {/* Transform */}
          <div className="mb-6">
            <h3 className={`text-[11px] font-bold uppercase tracking-wider mb-3 ${theme === 'dark' ? 'text-gray-400' : 'text-gray-500'}`}>
              {locale === 'ar' ? 'التحويل' : locale === 'en' ? 'Transform' : 'Transformation'}
            </h3>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className={`block text-[10px] mb-1 ${theme === 'dark' ? 'text-gray-500' : 'text-gray-600'}`}>Position X</label>
                <input
                  type="number"
                  value={properties.posX}
                  onChange={(e) => setProperties((p) => ({ ...p, posX: Number(e.target.value) }))}
                  className={`w-full px-3 py-2 rounded-md text-sm focus:border-cyan-400 focus:outline-none focus:ring-1 focus:ring-cyan-400/20 ${
                    theme === 'dark' ? 'bg-[#1a1a24] border border-[#2a2a35]' : 'bg-gray-100 border border-gray-200'
                  }`}
                />
              </div>
              <div>
                <label className={`block text-[10px] mb-1 ${theme === 'dark' ? 'text-gray-500' : 'text-gray-600'}`}>Position Y</label>
                <input
                  type="number"
                  value={properties.posY}
                  onChange={(e) => setProperties((p) => ({ ...p, posY: Number(e.target.value) }))}
                  className={`w-full px-3 py-2 rounded-md text-sm focus:border-cyan-400 focus:outline-none focus:ring-1 focus:ring-cyan-400/20 ${
                    theme === 'dark' ? 'bg-[#1a1a24] border border-[#2a2a35]' : 'bg-gray-100 border border-gray-200'
                  }`}
                />
              </div>
            </div>

            <div className="mt-3">
              <label className={`block text-[10px] mb-1 ${theme === 'dark' ? 'text-gray-500' : 'text-gray-600'}`}>{locale === 'ar' ? 'مقياس' : locale === 'en' ? 'Scale' : 'Échelle'}: {properties.scale}%</label>
              <input
                type="range"
                min="0"
                max="200"
                value={properties.scale}
                onChange={(e) => setProperties((p) => ({ ...p, scale: Number(e.target.value) }))}
                className="w-full h-1.5 bg-[#1a1a24] rounded-full appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-cyan-400 [&::-webkit-slider-thumb]:shadow-lg [&::-webkit-slider-thumb]:shadow-cyan-500/60"
              />
            </div>

            <div className="mt-3">
              <label className={`block text-[10px] mb-1 ${theme === 'dark' ? 'text-gray-500' : 'text-gray-600'}`}>{locale === 'ar' ? 'دوران' : 'Rotation'}: {properties.rotation}°</label>
              <input
                type="range"
                min="-180"
                max="180"
                value={properties.rotation}
                onChange={(e) => setProperties((p) => ({ ...p, rotation: Number(e.target.value) }))}
                className="w-full h-1.5 bg-[#1a1a24] rounded-full appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-cyan-400 [&::-webkit-slider-thumb]:shadow-lg [&::-webkit-slider-thumb]:shadow-cyan-500/60"
              />
            </div>

            <div className="mt-3">
              <label className={`block text-[10px] mb-1 ${theme === 'dark' ? 'text-gray-500' : 'text-gray-600'}`}>{locale === 'ar' ? 'شفافية' : locale === 'en' ? 'Opacity' : 'Opacité'}: {properties.opacity}%</label>
              <input
                type="range"
                min="0"
                max="100"
                value={properties.opacity}
                onChange={(e) => setProperties((p) => ({ ...p, opacity: Number(e.target.value) }))}
                className="w-full h-1.5 bg-[#1a1a24] rounded-full appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-cyan-400 [&::-webkit-slider-thumb]:shadow-lg [&::-webkit-slider-thumb]:shadow-cyan-500/60"
              />
            </div>
          </div>

          {/* Effects */}
          <div className="mb-6">
            <h3 className={`text-[11px] font-bold uppercase tracking-wider mb-3 ${theme === 'dark' ? 'text-gray-400' : 'text-gray-500'}`}>
              {locale === 'ar' ? 'المؤثرات البصرية' : locale === 'en' ? 'Visual Effects' : 'Effets Visuels'}
            </h3>
            <div className="grid grid-cols-2 gap-2">
              {[locale === 'ar' ? 'ضبابي' : locale === 'en' ? 'Blur' : 'Flou', 'Chroma', 'Glitch', 'Grain', 'Vignette', 'LUT'].map((effect) => (
                <button
                  key={effect}
                  className={`py-2.5 px-3 rounded-md text-xs font-medium transition-all ${theme === 'dark' ? 'bg-[#1a1a24] border border-[#2a2a35] hover:border-cyan-400 hover:bg-cyan-400/10' : 'bg-gray-100 border border-gray-200 hover:border-cyan-500 hover:bg-cyan-500/10'}`}
                >
                  {effect}
                </button>
              ))}
            </div>
          </div>

          {/* Transitions */}
          <div>
            <h3 className={`text-[11px] font-bold uppercase tracking-wider mb-3 ${theme === 'dark' ? 'text-gray-400' : 'text-gray-500'}`}>
              {locale === 'ar' ? 'الانتقالات' : 'Transitions'}
            </h3>
            <div className="grid grid-cols-2 gap-2">
              {['Fade', 'Dissolve', 'Wipe', 'Zoom'].map((transition) => (
                <button
                  key={transition}
                  className={`py-2.5 px-3 rounded-md text-xs font-medium transition-all ${theme === 'dark' ? 'bg-[#1a1a24] border border-[#2a2a35] hover:border-fuchsia-500 hover:bg-fuchsia-500/10' : 'bg-gray-100 border border-gray-200 hover:border-fuchsia-500 hover:bg-fuchsia-500/10'}`}
                >
                  {transition}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Timeline */}
      <div className={`relative z-10 h-[280px] border-t-2 ${theme === 'dark' ? 'bg-[#0f0f16] border-[#2a2a35]' : 'bg-gray-50 border-gray-300'}`}>
        {/* Timeline Header */}
        <div className={`h-10 border-b flex items-center px-4 gap-3 ${theme === 'dark' ? 'bg-[#141419] border-[#2a2a35]' : 'bg-white border-gray-200'}`}>
          <button
            onClick={() => setZoom((z) => Math.max(0.5, z - 0.25))}
            className={`p-1.5 rounded transition-colors ${theme === 'dark' ? 'hover:bg-[#2a2a35]' : 'hover:bg-gray-200'}`}
          >
            <ZoomOut className="w-4 h-4" />
          </button>
          <div className={`w-20 h-1.5 rounded-full ${theme === 'dark' ? 'bg-[#2a2a35]' : 'bg-gray-300'}`}>
            <div
              className="h-full bg-cyan-400 rounded-full"
              style={{ width: `${(zoom / 2) * 100}%` }}
            />
          </div>
          <button
            onClick={() => setZoom((z) => Math.min(2, z + 0.25))}
            className={`p-1.5 rounded transition-colors ${theme === 'dark' ? 'hover:bg-[#2a2a35]' : 'hover:bg-gray-200'}`}
          >
            <ZoomIn className="w-4 h-4" />
          </button>
          <div className="flex-1" />
          <button className={`flex items-center gap-2 px-3 py-1.5 rounded-md border text-sm ${theme === 'dark' ? 'bg-[#1a1a24] border-[#2a2a35] hover:border-cyan-400' : 'bg-gray-100 border-gray-200 hover:border-cyan-500'}`}>
            <Plus className="w-4 h-4" />
            {locale === 'ar' ? 'إضافة مسار' : locale === 'en' ? 'Add Track' : 'Ajouter Piste'}
          </button>
        </div>

        {/* Timeline Tracks */}
        <div className="flex h-[calc(100%-40px)]">
          {/* Track Headers */}
          <div className={`w-[200px] border-r ${theme === 'dark' ? 'bg-[#141419] border-[#2a2a35]' : 'bg-white border-gray-200'}`}>
            {tracks.map((track) => (
              <div
                key={track.id}
                className={`h-16 border-b flex items-center px-3 gap-2 ${theme === 'dark' ? 'border-[#2a2a35]' : 'border-gray-200'}`}
              >
                <div
                  className={`w-2 h-8 rounded-sm ${
                    track.type === "video" ? "bg-cyan-400" : "bg-fuchsia-500"
                  }`}
                />
                <span className="flex-1 text-sm font-medium truncate">{track.name}</span>
                <button
                  onClick={() => toggleTrackLock(track.id)}
                  className={`p-1.5 rounded ${track.locked ? "text-yellow-500" : "text-gray-500 hover:text-white"}`}
                >
                  {track.locked ? <Lock className="w-4 h-4" /> : <Unlock className="w-4 h-4" />}
                </button>
                <button
                  onClick={() => toggleTrackVisibility(track.id)}
                  className={`p-1.5 rounded ${!track.visible ? "text-red-500" : "text-gray-500 hover:text-white"}`}
                >
                  {track.visible ? <Eye className="w-4 h-4" /> : <EyeOff className="w-4 h-4" />}
                </button>
              </div>
            ))}
          </div>

          {/* Timeline Content */}
          <div className="flex-1 overflow-x-auto relative">
            {/* Time Ruler */}
            <div className={`h-6 border-b flex items-end px-2 sticky top-0 ${theme === 'dark' ? 'bg-[#1a1a24] border-[#2a2a35]' : 'bg-gray-100 border-gray-200'}`}>
              {Array.from({ length: Math.ceil(duration / 10) }).map((_, i) => (
                <div
                  key={i}
                  className="flex-shrink-0"
                  style={{ width: `${100 * zoom}px` }}
                >
                  <span className="text-[10px] text-gray-500 font-mono">
                    {formatTimecode(i * 10).slice(3, 8)}
                  </span>
                </div>
              ))}
            </div>

            {/* Tracks */}
            {tracks.map((track) => (
              <div
                key={track.id}
                className={`h-16 border-b relative ${theme === 'dark' ? 'border-[#2a2a35]' : 'border-gray-200'}`}
              >
                {track.clips.map((clip) => (
                  <motion.div
                    key={clip.id}
                    onClick={() => setSelectedClip(clip.id)}
                    className={`absolute top-2 h-12 rounded-md cursor-pointer transition-all ${
                      selectedClip === clip.id
                        ? `ring-2 ring-white ring-offset-2 ${theme === 'dark' ? 'ring-offset-[#0f0f16]' : 'ring-offset-gray-50'}`
                        : "hover:brightness-110"
                    }`}
                    style={{
                      left: `${clip.startTime * 10 * zoom}px`,
                      width: `${clip.duration * 10 * zoom}px`,
                      backgroundColor: clip.color,
                    }}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                  >
                    <div className="px-2 py-1 text-xs font-semibold text-black truncate">
                      {clip.name}
                    </div>
                    <div className="absolute bottom-1 right-2 text-[10px] text-black/70 font-mono">
                      {clip.duration}s
                    </div>
                  </motion.div>
                ))}
              </div>
            ))}

            {/* Playhead */}
            <div
              className="absolute top-0 bottom-0 w-0.5 bg-cyan-400 z-10 pointer-events-none"
              style={{ left: `${currentTime * 10 * zoom}px` }}
            >
              <div className="absolute -top-1 -left-2 w-4 h-4 bg-cyan-400 rotate-45" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
