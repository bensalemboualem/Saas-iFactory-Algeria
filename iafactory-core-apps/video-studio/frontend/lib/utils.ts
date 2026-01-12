import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatCredits(credits: number): string {
  return new Intl.NumberFormat("fr-FR").format(credits);
}

export function formatDate(date: string | Date): string {
  return new Intl.DateTimeFormat("fr-FR", {
    day: "numeric",
    month: "short",
    year: "numeric",
  }).format(new Date(date));
}

export function formatDuration(seconds: number): string {
  if (seconds < 60) return `${seconds}s`;
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins}m ${secs}s`;
}

export function estimateCredits(
  mode: "text-to-video" | "image-to-video",
  duration: number,
  quality: "720p" | "1080p" | "4k"
): number {
  const baseCost = mode === "text-to-video" ? 10 : 8;
  const durationMultiplier = duration / 5;
  const qualityMultiplier = quality === "4k" ? 2 : quality === "1080p" ? 1.5 : 1;
  return Math.ceil(baseCost * durationMultiplier * qualityMultiplier);
}
