"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Cpu,
  Zap,
  Crown,
  ChevronDown,
  Check,
  AlertCircle,
  ExternalLink,
} from "lucide-react";
import { 
  VIDEO_MODELS, 
  IMAGE_MODELS, 
  AIModel, 
  PROVIDER_STATUS,
  getAvailableModels,
} from "@/lib/providers";

interface ModelSelectorProps {
  type: 'text-to-video' | 'image-to-video' | 'text-to-image';
  selectedModel: string;
  onModelChange: (modelId: string) => void;
}

const tierIcons = {
  free: <Zap className="w-3.5 h-3.5 text-green-400" />,
  standard: <Cpu className="w-3.5 h-3.5 text-blue-400" />,
  premium: <Crown className="w-3.5 h-3.5 text-yellow-400" />,
};

const tierColors = {
  free: 'bg-green-500/10 text-green-400 border-green-500/30',
  standard: 'bg-blue-500/10 text-blue-400 border-blue-500/30',
  premium: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/30',
};

export default function ModelSelector({ 
  type, 
  selectedModel, 
  onModelChange 
}: ModelSelectorProps) {
  const [isOpen, setIsOpen] = useState(false);
  
  const availableModels = getAvailableModels(type);
  const currentModel = availableModels.find(m => m.id === selectedModel) || availableModels[0];

  return (
    <div className="relative">
      {/* Trigger Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between gap-3 px-4 py-3 rounded-xl bg-surface border border-border hover:border-primary/50 transition-all"
      >
        <div className="flex items-center gap-3">
          <span className="text-2xl">{currentModel?.icon}</span>
          <div className="text-left">
            <div className="flex items-center gap-2">
              <span className="font-medium">{currentModel?.name}</span>
              <span className={`px-2 py-0.5 text-xs rounded-full border ${tierColors[currentModel?.tier || 'free']}`}>
                {currentModel?.tier}
              </span>
            </div>
            <span className="text-sm text-text-muted">{currentModel?.resolution}</span>
          </div>
        </div>
        <ChevronDown className={`w-5 h-5 text-text-muted transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {/* Dropdown */}
      <AnimatePresence>
        {isOpen && (
          <>
            {/* Backdrop */}
            <div 
              className="fixed inset-0 z-40"
              onClick={() => setIsOpen(false)}
            />
            
            {/* Menu */}
            <motion.div
              initial={{ opacity: 0, y: -10, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -10, scale: 0.95 }}
              transition={{ duration: 0.15 }}
              className="absolute z-50 w-full mt-2 py-2 rounded-xl bg-surface border border-border shadow-2xl max-h-96 overflow-y-auto"
            >
              {/* Provider Status */}
              <div className="px-3 py-2 mb-2 border-b border-border">
                <div className="flex items-center gap-2 text-xs text-text-muted">
                  <div className="flex items-center gap-1">
                    <span className="w-2 h-2 rounded-full bg-green-500"></span>
                    Replicate
                  </div>
                  <span>•</span>
                  <div className="flex items-center gap-1">
                    <span className="w-2 h-2 rounded-full bg-red-500"></span>
                    Fal.ai (désactivé)
                  </div>
                </div>
              </div>

              {/* Model List */}
              {availableModels.map((model) => (
                <button
                  key={model.id}
                  onClick={() => {
                    onModelChange(model.id);
                    setIsOpen(false);
                  }}
                  className={`w-full flex items-start gap-3 px-4 py-3 hover:bg-surface-hover transition-colors ${
                    model.id === selectedModel ? 'bg-primary/10' : ''
                  }`}
                >
                  <span className="text-2xl mt-0.5">{model.icon}</span>
                  <div className="flex-1 text-left">
                    <div className="flex items-center gap-2">
                      <span className="font-medium">{model.name}</span>
                      {model.id === selectedModel && (
                        <Check className="w-4 h-4 text-primary" />
                      )}
                    </div>
                    <p className="text-sm text-text-muted line-clamp-1">
                      {model.description}
                    </p>
                    <div className="flex items-center gap-3 mt-1 text-xs text-text-muted">
                      <span className={`px-2 py-0.5 rounded-full border ${tierColors[model.tier]}`}>
                        {tierIcons[model.tier]}
                        <span className="ml-1">{model.tier}</span>
                      </span>
                      <span>{model.resolution}</span>
                      <span>{model.vram} VRAM</span>
                    </div>
                  </div>
                </button>
              ))}

              {/* Fal.ai Notice */}
              <div className="px-4 py-3 mt-2 mx-3 rounded-lg bg-red-500/10 border border-red-500/30">
                <div className="flex items-start gap-2">
                  <AlertCircle className="w-4 h-4 text-red-400 mt-0.5" />
                  <div className="text-sm">
                    <p className="text-red-400 font-medium">Fal.ai désactivé</p>
                    <p className="text-text-muted text-xs mt-0.5">
                      Crédits épuisés. Utilisation de Replicate.
                    </p>
                    <a 
                      href="https://fal.ai/dashboard/billing" 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 text-xs text-red-400 hover:underline mt-1"
                    >
                      Recharger les crédits <ExternalLink className="w-3 h-3" />
                    </a>
                  </div>
                </div>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </div>
  );
}
