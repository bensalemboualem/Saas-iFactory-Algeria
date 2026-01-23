"""
IA Factory Operator - Video Analyzer
Analyzes video content, detects scenes, extracts transcript
"""

import os
import json
import tempfile
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

import structlog
import ffmpeg

from core.config import settings
from core.state import (
    VideoAnalysis,
    SceneSegment,
    SceneType,
    EmotionalTone,
    VideoEditorState,
)

logger = structlog.get_logger(__name__)


class VideoAnalyzer:
    """
    Analyzes source video to extract:
    - Basic metadata (duration, resolution, fps, codec)
    - Scene detection with timestamps
    - Audio analysis
    - Transcript via Whisper (optional)
    """
    
    def __init__(self, whisper_client=None):
        self.whisper_client = whisper_client
    
    async def analyze(self, state: VideoEditorState) -> VideoEditorState:
        """Main analysis entry point"""
        state.add_log("🔍 Starting video analysis...")
        state.set_status("analyzing", progress=10, stage="analysis")
        
        try:
            video_path = state.source_video_path
            if not video_path or not os.path.exists(video_path):
                raise FileNotFoundError(f"Video not found: {video_path}")
            
            # 1. Get basic metadata
            state.add_log("📊 Extracting video metadata...")
            metadata = await self._get_video_metadata(video_path)
            state.set_status("analyzing", progress=20)
            
            # 2. Detect scenes
            state.add_log("🎬 Detecting scenes...")
            scenes = await self._detect_scenes(video_path, metadata)
            state.set_status("analyzing", progress=40)
            
            # 3. Extract transcript if has audio
            transcript = ""
            transcript_segments = []
            if metadata.get("has_audio", False) and self.whisper_client:
                state.add_log("🎤 Transcribing audio with Whisper...")
                transcript, transcript_segments = await self._transcribe(video_path)
                state.set_status("analyzing", progress=60)
            
            # 4. Analyze audio levels per scene
            if metadata.get("has_audio", False):
                state.add_log("🔊 Analyzing audio levels...")
                scenes = await self._analyze_audio_per_scene(video_path, scenes)
                state.set_status("analyzing", progress=70)
            
            # 5. Generate thumbnails for scenes
            state.add_log("🖼️ Extracting scene thumbnails...")
            # thumbnails = await self._extract_thumbnails(video_path, scenes, state.work_dir)
            state.set_status("analyzing", progress=80)
            
            # 6. Build analysis object
            analysis = VideoAnalysis(
                file_path=video_path,
                duration=metadata["duration"],
                width=metadata["width"],
                height=metadata["height"],
                fps=metadata["fps"],
                codec=metadata["codec"],
                bitrate=metadata.get("bitrate", 0),
                file_size=metadata.get("file_size", 0),
                scenes=scenes,
                total_scenes=len(scenes),
                has_audio=metadata.get("has_audio", False),
                audio_channels=metadata.get("audio_channels", 2),
                audio_sample_rate=metadata.get("audio_sample_rate", 44100),
                full_transcript=transcript,
                transcript_segments=transcript_segments,
                detected_language=state.language,
            )
            
            state.analysis = analysis
            state.add_log(f"✅ Analysis complete: {len(scenes)} scenes detected, duration: {metadata['duration']:.1f}s")
            state.set_status("analyzing", progress=90)
            
            return state
            
        except Exception as e:
            logger.exception("Video analysis failed", error=str(e))
            state.error = f"Analysis failed: {str(e)}"
            state.add_log(f"❌ Analysis error: {str(e)}")
            raise
    
    async def _get_video_metadata(self, video_path: str) -> Dict[str, Any]:
        """Extract video metadata using ffprobe"""
        try:
            probe = ffmpeg.probe(video_path)
            
            # Find video stream
            video_stream = None
            audio_stream = None
            
            for stream in probe.get("streams", []):
                if stream["codec_type"] == "video" and not video_stream:
                    video_stream = stream
                elif stream["codec_type"] == "audio" and not audio_stream:
                    audio_stream = stream
            
            if not video_stream:
                raise ValueError("No video stream found")
            
            # Calculate FPS
            fps_parts = video_stream.get("r_frame_rate", "30/1").split("/")
            fps = float(fps_parts[0]) / float(fps_parts[1]) if len(fps_parts) == 2 else 30.0
            
            # Get duration
            duration = float(probe["format"].get("duration", 0))
            
            return {
                "duration": duration,
                "width": int(video_stream.get("width", 1920)),
                "height": int(video_stream.get("height", 1080)),
                "fps": fps,
                "codec": video_stream.get("codec_name", "unknown"),
                "bitrate": int(probe["format"].get("bit_rate", 0)),
                "file_size": int(probe["format"].get("size", 0)),
                "has_audio": audio_stream is not None,
                "audio_channels": int(audio_stream.get("channels", 2)) if audio_stream else 0,
                "audio_sample_rate": int(audio_stream.get("sample_rate", 44100)) if audio_stream else 0,
            }
            
        except ffmpeg.Error as e:
            logger.error("FFprobe error", error=str(e))
            raise ValueError(f"Failed to probe video: {str(e)}")
    
    async def _detect_scenes(
        self,
        video_path: str,
        metadata: Dict[str, Any]
    ) -> List[SceneSegment]:
        """
        Detect scene changes using FFmpeg scene detection filter.
        Falls back to fixed intervals if scene detection fails.
        """
        scenes = []
        duration = metadata["duration"]
        
        try:
            # Use FFmpeg scene detection
            scene_threshold = 0.3  # Default threshold
            cmd = [
                "ffmpeg",
                "-i", video_path,
                "-vf", f"select='gt(scene,{scene_threshold})',showinfo",
                "-f", "null",
                "-"
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            # Parse scene change timestamps from stderr
            scene_times = [0.0]  # Always start at 0
            
            for line in result.stderr.split("\n"):
                if "pts_time:" in line:
                    try:
                        pts_time = float(line.split("pts_time:")[1].split()[0])
                        if pts_time > scene_times[-1] + 0.5:  # Min 0.5s between scenes
                            scene_times.append(pts_time)
                    except (IndexError, ValueError):
                        continue
            
            # Add end time if not present
            if scene_times[-1] < duration - 0.5:
                scene_times.append(duration)
            
            # Create scene segments
            for i in range(len(scene_times) - 1):
                start = scene_times[i]
                end = scene_times[i + 1]
                
                scene = SceneSegment(
                    start_time=start,
                    end_time=end,
                    duration=end - start,
                    scene_type=SceneType.unknown,
                    confidence=0.7,
                )
                scenes.append(scene)
            
            logger.info(f"Detected {len(scenes)} scenes via FFmpeg")
            
        except (subprocess.TimeoutExpired, Exception) as e:
            logger.warning(f"Scene detection failed, using fixed intervals: {e}")
            
            # Fallback: fixed 3-second intervals
            interval = 3.0
            current = 0.0
            
            while current < duration:
                end = min(current + interval, duration)
                scenes.append(SceneSegment(
                    start_time=current,
                    end_time=end,
                    duration=end - current,
                    scene_type=SceneType.unknown,
                    confidence=0.5,
                ))
                current = end
        
        # If too few scenes, subdivide
        if len(scenes) < 3 and duration > 10:
            scenes = self._subdivide_scenes(scenes, target_count=max(3, int(duration / 5)))
        
        return scenes
    
    def _subdivide_scenes(
        self,
        scenes: List[SceneSegment],
        target_count: int
    ) -> List[SceneSegment]:
        """Subdivide scenes if too few detected"""
        new_scenes = []
        
        for scene in scenes:
            if scene.duration > 5 and len(new_scenes) < target_count:
                # Split this scene
                mid = scene.start_time + scene.duration / 2
                new_scenes.append(SceneSegment(
                    start_time=scene.start_time,
                    end_time=mid,
                    duration=mid - scene.start_time,
                    scene_type=scene.scene_type,
                    confidence=scene.confidence * 0.8,
                ))
                new_scenes.append(SceneSegment(
                    start_time=mid,
                    end_time=scene.end_time,
                    duration=scene.end_time - mid,
                    scene_type=scene.scene_type,
                    confidence=scene.confidence * 0.8,
                ))
            else:
                new_scenes.append(scene)
        
        return new_scenes
    
    async def _transcribe(
        self,
        video_path: str
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """Transcribe audio using Whisper client"""
        if not self.whisper_client:
            return "", []
        
        try:
            result = await self.whisper_client.transcribe(video_path)
            
            full_text = result.get("text", "")
            segments = result.get("segments", [])
            
            return full_text, segments
            
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            return "", []
    
    async def _analyze_audio_per_scene(
        self,
        video_path: str,
        scenes: List[SceneSegment]
    ) -> List[SceneSegment]:
        """Analyze audio characteristics for each scene"""
        for scene in scenes:
            try:
                # Use FFmpeg to get audio stats for this segment
                cmd = [
                    "ffmpeg",
                    "-ss", str(scene.start_time),
                    "-t", str(scene.duration),
                    "-i", video_path,
                    "-af", "volumedetect",
                    "-f", "null",
                    "-"
                ]
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                # Parse mean volume
                for line in result.stderr.split("\n"):
                    if "mean_volume:" in line:
                        try:
                            volume = float(line.split("mean_volume:")[1].split("dB")[0].strip())
                            scene.audio_level = volume
                            # Assume speech if volume above threshold
                            scene.has_speech = volume > -30
                        except (IndexError, ValueError):
                            pass
                        break
                
            except Exception as e:
                logger.warning(f"Audio analysis failed for scene: {e}")
        
        return scenes
    
    async def _extract_thumbnails(
        self,
        video_path: str,
        scenes: List[SceneSegment],
        work_dir: str
    ) -> Dict[int, str]:
        """Extract thumbnail at midpoint of each scene"""
        thumbnails = {}
        
        for i, scene in enumerate(scenes):
            mid_time = scene.start_time + scene.duration / 2
            thumb_path = os.path.join(work_dir, f"thumb_scene_{i}.jpg")
            
            try:
                (
                    ffmpeg
                    .input(video_path, ss=mid_time)
                    .output(thumb_path, vframes=1, **{'q:v': 2})
                    .overwrite_output()
                    .run(capture_stdout=True, capture_stderr=True)
                )
                thumbnails[i] = thumb_path
            except Exception as e:
                logger.warning(f"Thumbnail extraction failed for scene {i}: {e}")
        
        return thumbnails


# =============================================================================
# MODULE FUNCTION
# =============================================================================

async def analyze_video(state: VideoEditorState, whisper_client=None) -> VideoEditorState:
    """Convenience function to analyze video"""
    analyzer = VideoAnalyzer(whisper_client=whisper_client)
    return await analyzer.analyze(state)
