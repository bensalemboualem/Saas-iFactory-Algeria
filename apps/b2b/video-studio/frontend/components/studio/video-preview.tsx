"use client";

import { motion } from "framer-motion";
import { Play, Download, Loader2 } from "lucide-react";
import { Button } from "@/components/ui";
import { Progress } from "@/components/ui/progress";

interface VideoPreviewProps {
  status: "idle" | "generating" | "completed" | "error";
  progress: number;
  videoUrl?: string;
  error?: string;
  onDownload?: () => void;
}

export function VideoPreview({
  status,
  progress,
  videoUrl,
  error,
  onDownload,
}: VideoPreviewProps) {
  return (
    <div className="aspect-video bg-surface border border-border rounded-xl flex items-center justify-center overflow-hidden">
      {status === "idle" && (
        <div className="text-center">
          <Play className="w-16 h-16 mx-auto mb-4 text-text-muted" />
          <p className="text-text-muted">Votre vidéo apparaîtra ici</p>
        </div>
      )}

      {status === "generating" && (
        <div className="text-center w-full px-8">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
          >
            <Loader2 className="w-16 h-16 mx-auto mb-4 text-primary" />
          </motion.div>
          <p className="text-text-muted mb-4">Génération en cours...</p>
          <Progress value={progress} showLabel className="max-w-xs mx-auto" />
        </div>
      )}

      {status === "completed" && videoUrl && (
        <div className="w-full h-full relative">
          <video
            src={videoUrl}
            controls
            className="w-full h-full object-contain bg-black"
          />
          {onDownload && (
            <Button
              onClick={onDownload}
              className="absolute bottom-4 right-4"
              size="sm"
            >
              <Download className="w-4 h-4" />
              Télécharger
            </Button>
          )}
        </div>
      )}

      {status === "error" && (
        <div className="text-center">
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-error/20 flex items-center justify-center">
            <span className="text-2xl">❌</span>
          </div>
          <p className="text-error font-medium">Erreur de génération</p>
          <p className="text-sm text-text-muted mt-2">{error}</p>
        </div>
      )}
    </div>
  );
}
