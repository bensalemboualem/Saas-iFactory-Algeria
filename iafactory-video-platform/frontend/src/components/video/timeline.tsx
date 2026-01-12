'use client';

import * as React from 'react';
import { motion } from 'framer-motion';
import { Play, Pause, SkipBack, SkipForward, Volume2, VolumeX } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface TimelineClip {
  id: string;
  type: 'video' | 'audio' | 'music' | 'text';
  start: number;
  duration: number;
  label?: string;
  color?: string;
}

interface TimelineTrack {
  id: string;
  name: string;
  type: 'video' | 'audio' | 'music' | 'text';
  clips: TimelineClip[];
}

interface TimelineProps {
  tracks: TimelineTrack[];
  duration: number; // Total duration in seconds
  currentTime?: number;
  isPlaying?: boolean;
  onTimeChange?: (time: number) => void;
  onPlayPause?: () => void;
  onClipSelect?: (clipId: string) => void;
}

export function Timeline({
  tracks,
  duration,
  currentTime = 0,
  isPlaying = false,
  onTimeChange,
  onPlayPause,
  onClipSelect,
}: TimelineProps) {
  const [zoom, setZoom] = React.useState(1);
  const [isMuted, setIsMuted] = React.useState(false);
  const timelineRef = React.useRef<HTMLDivElement>(null);

  const pixelsPerSecond = 50 * zoom;
  const timelineWidth = duration * pixelsPerSecond;

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const handleTimelineClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!timelineRef.current || !onTimeChange) return;

    const rect = timelineRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left + timelineRef.current.scrollLeft;
    const newTime = Math.max(0, Math.min(duration, x / pixelsPerSecond));
    onTimeChange(newTime);
  };

  const trackColors = {
    video: 'bg-blue-600',
    audio: 'bg-green-600',
    music: 'bg-purple-600',
    text: 'bg-yellow-600',
  };

  return (
    <div className="bg-gray-900 rounded-xl overflow-hidden">
      {/* Controls */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-gray-800">
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="sm" onClick={() => onTimeChange?.(0)}>
            <SkipBack className="h-4 w-4" />
          </Button>
          <Button variant="primary" size="sm" onClick={onPlayPause}>
            {isPlaying ? (
              <Pause className="h-4 w-4" />
            ) : (
              <Play className="h-4 w-4" />
            )}
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => onTimeChange?.(duration)}
          >
            <SkipForward className="h-4 w-4" />
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setIsMuted(!isMuted)}
          >
            {isMuted ? (
              <VolumeX className="h-4 w-4" />
            ) : (
              <Volume2 className="h-4 w-4" />
            )}
          </Button>
        </div>

        <div className="flex items-center gap-4">
          <span className="text-sm text-gray-400 font-mono">
            {formatTime(currentTime)} / {formatTime(duration)}
          </span>

          <div className="flex items-center gap-2">
            <span className="text-xs text-gray-500">Zoom:</span>
            <input
              type="range"
              min="0.5"
              max="3"
              step="0.1"
              value={zoom}
              onChange={(e) => setZoom(parseFloat(e.target.value))}
              className="w-20 h-1 bg-gray-700 rounded-lg appearance-none cursor-pointer"
            />
          </div>
        </div>
      </div>

      {/* Time ruler */}
      <div className="px-4 py-2 border-b border-gray-800 overflow-x-auto">
        <div
          className="relative h-6"
          style={{ width: timelineWidth }}
        >
          {Array.from({ length: Math.ceil(duration) + 1 }).map((_, i) => (
            <div
              key={i}
              className="absolute top-0 flex flex-col items-center"
              style={{ left: i * pixelsPerSecond }}
            >
              <div className="w-px h-3 bg-gray-600" />
              <span className="text-[10px] text-gray-500 mt-0.5">
                {formatTime(i)}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Tracks */}
      <div
        ref={timelineRef}
        className="overflow-x-auto"
        onClick={handleTimelineClick}
      >
        <div className="min-w-full" style={{ width: Math.max(timelineWidth, 800) }}>
          {tracks.map((track) => (
            <div key={track.id} className="flex border-b border-gray-800">
              {/* Track label */}
              <div className="w-24 flex-shrink-0 px-3 py-3 bg-gray-800/50 border-r border-gray-700">
                <span className="text-xs font-medium text-gray-400">
                  {track.name}
                </span>
              </div>

              {/* Track content */}
              <div
                className="relative h-12 flex-1"
                style={{ width: timelineWidth }}
              >
                {track.clips.map((clip) => (
                  <motion.div
                    key={clip.id}
                    className={`absolute top-1 bottom-1 rounded cursor-pointer ${
                      trackColors[clip.type]
                    } hover:brightness-110 transition-all`}
                    style={{
                      left: clip.start * pixelsPerSecond,
                      width: clip.duration * pixelsPerSecond,
                    }}
                    onClick={(e) => {
                      e.stopPropagation();
                      onClipSelect?.(clip.id);
                    }}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                  >
                    <div className="px-2 py-1 text-[10px] text-white truncate">
                      {clip.label}
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          ))}

          {/* Playhead */}
          <div
            className="absolute top-0 bottom-0 w-0.5 bg-red-500 z-10 pointer-events-none"
            style={{
              left: currentTime * pixelsPerSecond + 96, // 96px = track label width
            }}
          >
            <div className="w-3 h-3 bg-red-500 rounded-full -translate-x-1/2 -translate-y-1/2" />
          </div>
        </div>
      </div>
    </div>
  );
}

export type { TimelineTrack, TimelineClip };
