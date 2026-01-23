"use client";

import { cn } from "@/lib/utils";

interface GenerationSettingsProps {
  duration: number;
  aspectRatio: string;
  onDurationChange: (duration: number) => void;
  onAspectRatioChange: (ratio: string) => void;
  className?: string;
}

export function GenerationSettings({
  duration,
  aspectRatio,
  onDurationChange,
  onAspectRatioChange,
  className,
}: GenerationSettingsProps) {
  const durations = [
    { value: 5, label: "5s" },
    { value: 10, label: "10s" },
  ];

  const ratios = [
    { value: "16:9", label: "16:9", icon: "▭" },
    { value: "9:16", label: "9:16", icon: "▯" },
    { value: "1:1", label: "1:1", icon: "□" },
  ];

  return (
    <div className={cn("space-y-4", className)}>
      {/* Duration */}
      <div>
        <label className="block text-sm font-medium mb-2">Durée</label>
        <div className="flex gap-2">
          {durations.map((d) => (
            <button
              key={d.value}
              onClick={() => onDurationChange(d.value)}
              className={cn(
                "flex-1 py-2 px-4 rounded-lg font-medium transition-colors",
                duration === d.value
                  ? "bg-primary text-white"
                  : "bg-surface border border-border hover:border-primary/50"
              )}
            >
              {d.label}
            </button>
          ))}
        </div>
      </div>

      {/* Aspect Ratio */}
      <div>
        <label className="block text-sm font-medium mb-2">Format</label>
        <div className="flex gap-2">
          {ratios.map((r) => (
            <button
              key={r.value}
              onClick={() => onAspectRatioChange(r.value)}
              className={cn(
                "flex-1 py-2 px-4 rounded-lg font-medium transition-colors flex items-center justify-center gap-2",
                aspectRatio === r.value
                  ? "bg-primary text-white"
                  : "bg-surface border border-border hover:border-primary/50"
              )}
            >
              <span className="text-lg">{r.icon}</span>
              <span>{r.label}</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
