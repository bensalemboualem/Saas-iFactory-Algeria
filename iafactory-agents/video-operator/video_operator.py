"""
IA Factory Video Operator - Core Agent
Montage Vidéo Automatisé avec Claude + FFmpeg

Architecture:
1. ANALYZE  → Détection scènes, transcription, moments clés
2. PLAN     → Décisions de montage (cuts, transitions)  
3. EXECUTE  → FFmpeg processing
4. EXPORT   → Multi-platform (IG, TikTok, YouTube)
"""

import os
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("video_operator")

# ============================================================
# DATA MODELS
# ============================================================

class Platform(Enum):
    INSTAGRAM_REELS = "instagram_reels"
    TIKTOK = "tiktok"
    YOUTUBE_SHORTS = "youtube_shorts"
    SQUARE = "square"


class EditStyle(Enum):
    ALGERIAN_MINIMAL = "algerian_minimal"
    PRODUCT_DEMO = "product_demo"
    FOOD_PROMO = "food_promo"
    CINEMATIC = "cinematic"
    ENERGETIC = "energetic"
    PROFESSIONAL = "professional"


@dataclass
class VideoSegment:
    """Un segment de vidéo détecté"""
    start_time: float  # seconds
    end_time: float
    score: float = 0.0  # engagement score (0-1)
    has_face: bool = False
    has_motion: bool = False
    has_speech: bool = False
    transcript: str = ""
    scene_type: str = "unknown"  # intro, demo, cta, etc.


@dataclass
class EditPlan:
    """Plan de montage généré par l'agent"""
    segments: List[VideoSegment]
    total_duration: float
    transitions: List[Dict[str, Any]]
    captions: List[Dict[str, Any]]
    music_sync: Optional[Dict[str, Any]] = None
    color_grade: str = "none"
    speed_adjustments: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class VideoOperatorConfig:
    """Configuration de l'opérateur"""
    target_duration: int = 15  # seconds
    platforms: List[Platform] = field(default_factory=lambda: [Platform.INSTAGRAM_REELS])
    style: EditStyle = EditStyle.ALGERIAN_MINIMAL
    add_captions: bool = True
    add_music: bool = False
    music_path: Optional[str] = None
    watermark_path: Optional[str] = None
    output_dir: str = "/tmp/video_operator"


# ============================================================
# FFMPEG WRAPPER
# ============================================================

class FFmpegWrapper:
    """Wrapper FFmpeg pour les opérations vidéo de base"""
    
    @staticmethod
    def get_video_info(video_path: str) -> Dict[str, Any]:
        """Récupère les métadonnées de la vidéo"""
        cmd = [
            "ffprobe", "-v", "quiet",
            "-print_format", "json",
            "-show_format", "-show_streams",
            video_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"FFprobe error: {result.stderr}")
        
        data = json.loads(result.stdout)
        
        # Extract key info
        video_stream = next((s for s in data.get("streams", []) if s["codec_type"] == "video"), {})
        audio_stream = next((s for s in data.get("streams", []) if s["codec_type"] == "audio"), {})
        
        return {
            "duration": float(data.get("format", {}).get("duration", 0)),
            "width": int(video_stream.get("width", 0)),
            "height": int(video_stream.get("height", 0)),
            "fps": eval(video_stream.get("r_frame_rate", "30/1")),
            "has_audio": bool(audio_stream),
            "codec": video_stream.get("codec_name", "unknown")
        }
    
    @staticmethod
    def extract_segment(
        input_path: str,
        output_path: str,
        start_time: float,
        end_time: float
    ) -> bool:
        """Extrait un segment de vidéo"""
        duration = end_time - start_time
        cmd = [
            "ffmpeg", "-y",
            "-ss", str(start_time),
            "-i", input_path,
            "-t", str(duration),
            "-c", "copy",
            output_path
        ]
        result = subprocess.run(cmd, capture_output=True)
        return result.returncode == 0
    
    @staticmethod
    def concat_videos(
        video_paths: List[str],
        output_path: str,
        transition: str = "none"
    ) -> bool:
        """Concatène plusieurs vidéos"""
        # Create concat file
        concat_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
        for path in video_paths:
            concat_file.write(f"file '{path}'\n")
        concat_file.close()
        
        if transition == "none":
            # Simple concat
            cmd = [
                "ffmpeg", "-y",
                "-f", "concat", "-safe", "0",
                "-i", concat_file.name,
                "-c", "copy",
                output_path
            ]
        else:
            # With transition (requires re-encoding)
            cmd = [
                "ffmpeg", "-y",
                "-f", "concat", "-safe", "0",
                "-i", concat_file.name,
                "-c:v", "libx264", "-preset", "fast",
                "-c:a", "aac",
                output_path
            ]
        
        result = subprocess.run(cmd, capture_output=True)
        os.unlink(concat_file.name)
        return result.returncode == 0
    
    @staticmethod
    def add_captions(
        input_path: str,
        output_path: str,
        captions: List[Dict[str, Any]],
        style: str = "default"
    ) -> bool:
        """Ajoute des sous-titres à la vidéo"""
        # Create SRT file
        srt_file = tempfile.NamedTemporaryFile(mode='w', suffix='.srt', delete=False, encoding='utf-8')
        
        for i, cap in enumerate(captions, 1):
            start = cap["start"]
            end = cap["end"]
            text = cap["text"]
            
            # Format SRT timestamps
            start_str = f"{int(start//3600):02d}:{int((start%3600)//60):02d}:{int(start%60):02d},{int((start%1)*1000):03d}"
            end_str = f"{int(end//3600):02d}:{int((end%3600)//60):02d}:{int(end%60):02d},{int((end%1)*1000):03d}"
            
            srt_file.write(f"{i}\n{start_str} --> {end_str}\n{text}\n\n")
        
        srt_file.close()
        
        # Add subtitles with FFmpeg
        # Style for social media (big, centered, white with black outline)
        style_str = "FontSize=24,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=3,Outline=2,Shadow=0,MarginV=50"
        
        cmd = [
            "ffmpeg", "-y",
            "-i", input_path,
            "-vf", f"subtitles={srt_file.name}:force_style='{style_str}'",
            "-c:a", "copy",
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True)
        os.unlink(srt_file.name)
        return result.returncode == 0
    
    @staticmethod
    def resize_for_platform(
        input_path: str,
        output_path: str,
        platform: Platform
    ) -> bool:
        """Redimensionne la vidéo pour une plateforme spécifique"""
        # Platform aspect ratios
        dimensions = {
            Platform.INSTAGRAM_REELS: (1080, 1920),  # 9:16
            Platform.TIKTOK: (1080, 1920),           # 9:16
            Platform.YOUTUBE_SHORTS: (1080, 1920),   # 9:16
            Platform.SQUARE: (1080, 1080),           # 1:1
        }
        
        width, height = dimensions.get(platform, (1080, 1920))
        
        # Scale and pad to fit
        cmd = [
            "ffmpeg", "-y",
            "-i", input_path,
            "-vf", f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black",
            "-c:v", "libx264", "-preset", "fast",
            "-c:a", "aac",
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True)
        return result.returncode == 0
    
    @staticmethod
    def add_watermark(
        input_path: str,
        output_path: str,
        watermark_path: str,
        position: str = "bottom_right"
    ) -> bool:
        """Ajoute un watermark/logo"""
        positions = {
            "top_left": "10:10",
            "top_right": "main_w-overlay_w-10:10",
            "bottom_left": "10:main_h-overlay_h-10",
            "bottom_right": "main_w-overlay_w-10:main_h-overlay_h-10",
            "center": "(main_w-overlay_w)/2:(main_h-overlay_h)/2"
        }
        
        pos = positions.get(position, positions["bottom_right"])
        
        cmd = [
            "ffmpeg", "-y",
            "-i", input_path,
            "-i", watermark_path,
            "-filter_complex", f"[1:v]scale=100:-1[wm];[0:v][wm]overlay={pos}",
            "-c:a", "copy",
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True)
        return result.returncode == 0


# ============================================================
# SCENE DETECTOR
# ============================================================

class SceneDetector:
    """Détection de scènes et moments clés"""
    
    @staticmethod
    def detect_scenes(video_path: str, threshold: float = 30.0) -> List[VideoSegment]:
        """
        Détecte les changements de scène dans une vidéo.
        Utilise FFmpeg pour analyser les différences entre frames.
        """
        segments = []
        
        # Get video duration first
        info = FFmpegWrapper.get_video_info(video_path)
        duration = info["duration"]
        
        # Use FFmpeg scene detection
        cmd = [
            "ffmpeg", "-i", video_path,
            "-vf", f"select='gt(scene,{threshold/100})',showinfo",
            "-f", "null", "-"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, stderr=subprocess.STDOUT)
        
        # Parse scene timestamps from output
        scene_times = [0.0]  # Start with 0
        
        for line in result.stdout.split('\n'):
            if 'pts_time:' in line:
                try:
                    pts_time = float(line.split('pts_time:')[1].split()[0])
                    scene_times.append(pts_time)
                except:
                    pass
        
        scene_times.append(duration)  # End with duration
        
        # Create segments
        for i in range(len(scene_times) - 1):
            start = scene_times[i]
            end = scene_times[i + 1]
            
            if end - start > 0.5:  # Ignore very short segments
                segment = VideoSegment(
                    start_time=start,
                    end_time=end,
                    score=0.5,  # Default score
                    scene_type="unknown"
                )
                segments.append(segment)
        
        logger.info(f"Detected {len(segments)} scenes in video")
        return segments
    
    @staticmethod
    def analyze_motion(video_path: str, segment: VideoSegment) -> float:
        """
        Analyse le mouvement dans un segment.
        Retourne un score de 0 à 1.
        """
        # Simplified motion detection using FFmpeg
        cmd = [
            "ffmpeg", "-ss", str(segment.start_time),
            "-t", str(segment.end_time - segment.start_time),
            "-i", video_path,
            "-vf", "mpdecimate=hi=64*48:lo=64*24:frac=0.1,showinfo",
            "-f", "null", "-"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, stderr=subprocess.STDOUT)
        
        # Count dropped frames (low motion = more drops)
        drop_count = result.stdout.count('drop')
        total_frames = result.stdout.count('pts_time')
        
        if total_frames == 0:
            return 0.5
        
        # More drops = less motion = lower score
        motion_score = 1 - (drop_count / max(total_frames, 1))
        return min(max(motion_score, 0), 1)


# ============================================================
# VIDEO OPERATOR AGENT
# ============================================================

class VideoOperatorAgent:
    """
    Agent principal pour le montage vidéo automatisé.
    
    Workflow:
    1. Analyze video (scenes, audio, motion)
    2. Plan edit (select best segments, decide cuts)
    3. Execute (FFmpeg processing)
    4. Export (multi-platform)
    """
    
    def __init__(self, config: VideoOperatorConfig):
        self.config = config
        self.ffmpeg = FFmpegWrapper()
        self.scene_detector = SceneDetector()
        
        # Create output directory
        os.makedirs(config.output_dir, exist_ok=True)
    
    async def process_video(
        self,
        input_path: str,
        output_name: str = "edited"
    ) -> Dict[str, str]:
        """
        Pipeline complet de traitement vidéo.
        
        Returns:
            Dict mapping platform -> output path
        """
        logger.info(f"Starting video processing: {input_path}")
        
        # Step 1: Analyze
        logger.info("Step 1: Analyzing video...")
        analysis = await self._analyze_video(input_path)
        
        # Step 2: Plan
        logger.info("Step 2: Planning edit...")
        edit_plan = await self._plan_edit(analysis)
        
        # Step 3: Execute
        logger.info("Step 3: Executing edit...")
        edited_path = await self._execute_edit(input_path, edit_plan)
        
        # Step 4: Export for platforms
        logger.info("Step 4: Exporting for platforms...")
        outputs = await self._export_platforms(edited_path, output_name)
        
        logger.info(f"Processing complete. Outputs: {outputs}")
        return outputs
    
    async def _analyze_video(self, video_path: str) -> Dict[str, Any]:
        """Analyse complète de la vidéo"""
        
        # Get basic info
        info = self.ffmpeg.get_video_info(video_path)
        
        # Detect scenes
        segments = self.scene_detector.detect_scenes(video_path)
        
        # Analyze motion for each segment
        for segment in segments:
            motion_score = self.scene_detector.analyze_motion(video_path, segment)
            segment.has_motion = motion_score > 0.3
            segment.score = motion_score
        
        return {
            "info": info,
            "segments": segments,
            "total_duration": info["duration"]
        }
    
    async def _plan_edit(self, analysis: Dict[str, Any]) -> EditPlan:
        """
        Planifie le montage basé sur l'analyse.
        
        Sélectionne les meilleurs segments pour atteindre la durée cible.
        """
        segments = analysis["segments"]
        target_duration = self.config.target_duration
        
        # Sort segments by score (best first)
        sorted_segments = sorted(segments, key=lambda s: s.score, reverse=True)
        
        # Select segments to reach target duration
        selected_segments = []
        current_duration = 0
        
        for segment in sorted_segments:
            segment_duration = segment.end_time - segment.start_time
            
            if current_duration + segment_duration <= target_duration:
                selected_segments.append(segment)
                current_duration += segment_duration
            elif current_duration < target_duration:
                # Trim segment to fit
                remaining = target_duration - current_duration
                trimmed = VideoSegment(
                    start_time=segment.start_time,
                    end_time=segment.start_time + remaining,
                    score=segment.score
                )
                selected_segments.append(trimmed)
                break
        
        # Sort by original time order
        selected_segments.sort(key=lambda s: s.start_time)
        
        # Generate captions (placeholder - would use Whisper)
        captions = []
        if self.config.add_captions:
            # Simple placeholder captions
            for i, seg in enumerate(selected_segments):
                captions.append({
                    "start": sum(s.end_time - s.start_time for s in selected_segments[:i]),
                    "end": sum(s.end_time - s.start_time for s in selected_segments[:i+1]),
                    "text": f"Scene {i+1}"
                })
        
        return EditPlan(
            segments=selected_segments,
            total_duration=sum(s.end_time - s.start_time for s in selected_segments),
            transitions=[{"type": "cut"}] * (len(selected_segments) - 1),
            captions=captions
        )
    
    async def _execute_edit(
        self,
        input_path: str,
        plan: EditPlan
    ) -> str:
        """Exécute le plan de montage"""
        
        temp_dir = tempfile.mkdtemp()
        segment_paths = []
        
        # Extract each segment
        for i, segment in enumerate(plan.segments):
            segment_path = os.path.join(temp_dir, f"segment_{i:03d}.mp4")
            
            success = self.ffmpeg.extract_segment(
                input_path,
                segment_path,
                segment.start_time,
                segment.end_time
            )
            
            if success:
                segment_paths.append(segment_path)
            else:
                logger.warning(f"Failed to extract segment {i}")
        
        # Concatenate segments
        concat_path = os.path.join(self.config.output_dir, "concat_temp.mp4")
        self.ffmpeg.concat_videos(segment_paths, concat_path)
        
        # Add captions if enabled
        if self.config.add_captions and plan.captions:
            captioned_path = os.path.join(self.config.output_dir, "captioned_temp.mp4")
            self.ffmpeg.add_captions(concat_path, captioned_path, plan.captions)
            os.replace(captioned_path, concat_path)
        
        # Add watermark if provided
        if self.config.watermark_path:
            watermarked_path = os.path.join(self.config.output_dir, "watermarked_temp.mp4")
            self.ffmpeg.add_watermark(concat_path, watermarked_path, self.config.watermark_path)
            os.replace(watermarked_path, concat_path)
        
        # Cleanup temp segments
        for path in segment_paths:
            try:
                os.unlink(path)
            except:
                pass
        
        return concat_path
    
    async def _export_platforms(
        self,
        edited_path: str,
        output_name: str
    ) -> Dict[str, str]:
        """Exporte pour chaque plateforme configurée"""
        
        outputs = {}
        
        for platform in self.config.platforms:
            output_path = os.path.join(
                self.config.output_dir,
                f"{output_name}_{platform.value}.mp4"
            )
            
            success = self.ffmpeg.resize_for_platform(
                edited_path,
                output_path,
                platform
            )
            
            if success:
                outputs[platform.value] = output_path
                logger.info(f"Exported for {platform.value}: {output_path}")
            else:
                logger.warning(f"Failed to export for {platform.value}")
        
        # Cleanup temp edited file
        try:
            os.unlink(edited_path)
        except:
            pass
        
        return outputs


# ============================================================
# CLI INTERFACE
# ============================================================

async def main():
    """CLI pour tester l'agent"""
    import argparse
    
    parser = argparse.ArgumentParser(description="IA Factory Video Operator")
    parser.add_argument("input", help="Input video path")
    parser.add_argument("--duration", type=int, default=15, help="Target duration (seconds)")
    parser.add_argument("--platform", choices=["instagram", "tiktok", "youtube", "square"], 
                        default="instagram", help="Target platform")
    parser.add_argument("--output", default="/tmp/video_operator", help="Output directory")
    parser.add_argument("--captions", action="store_true", help="Add captions")
    
    args = parser.parse_args()
    
    # Map platform string to enum
    platform_map = {
        "instagram": Platform.INSTAGRAM_REELS,
        "tiktok": Platform.TIKTOK,
        "youtube": Platform.YOUTUBE_SHORTS,
        "square": Platform.SQUARE
    }
    
    config = VideoOperatorConfig(
        target_duration=args.duration,
        platforms=[platform_map[args.platform]],
        add_captions=args.captions,
        output_dir=args.output
    )
    
    agent = VideoOperatorAgent(config)
    outputs = await agent.process_video(args.input)
    
    print("\n✅ Processing complete!")
    for platform, path in outputs.items():
        print(f"  {platform}: {path}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
