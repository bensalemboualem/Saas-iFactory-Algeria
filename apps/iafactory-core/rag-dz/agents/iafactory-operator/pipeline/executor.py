"""
IA Factory Operator - Edit Executor
Executes edit plan using FFmpeg and MoviePy
"""

import os
import tempfile
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

import structlog
import ffmpeg

from core.config import settings
from core.state import (
    VideoEditorState,
    EditPlan,
    EditAction,
    EditActionType,
    PLATFORM_SPECS,
)

logger = structlog.get_logger(__name__)


class EditExecutor:
    """
    Executes the edit plan using FFmpeg.
    Produces output videos for each target platform.
    """
    
    def __init__(self, storage_client=None):
        self.storage_client = storage_client
    
    async def execute(self, state: VideoEditorState) -> VideoEditorState:
        """Execute the edit plan and produce output videos"""
        state.add_log("🎬 Starting video rendering...")
        state.set_status("rendering", progress=75, stage="rendering")
        
        try:
            if not state.edit_plan:
                raise ValueError("No edit plan available")
            if not state.source_video_path:
                raise ValueError("No source video path")
            
            plan = state.edit_plan
            source_path = state.source_video_path
            work_dir = state.work_dir or tempfile.mkdtemp(prefix="iafactory_")
            
            # Process for each target platform
            for platform in state.platforms:
                state.add_log(f"📱 Rendering for {platform}...")
                
                output_path = os.path.join(work_dir, f"output_{platform}.mp4")
                
                # Execute platform-specific render
                await self._render_for_platform(
                    source_path=source_path,
                    output_path=output_path,
                    plan=plan,
                    platform=platform,
                    state=state,
                )
                
                state.output_files[platform] = output_path
                
                # Generate thumbnail
                thumb_path = os.path.join(work_dir, f"thumb_{platform}.jpg")
                await self._generate_thumbnail(output_path, thumb_path)
            
            state.add_log(f"✅ Rendering complete: {len(state.output_files)} videos created")
            state.set_status("rendering", progress=95)
            
            return state
            
        except Exception as e:
            logger.exception("Rendering failed", error=str(e))
            state.error = f"Rendering failed: {str(e)}"
            state.add_log(f"❌ Rendering error: {str(e)}")
            raise
    
    async def _render_for_platform(
        self,
        source_path: str,
        output_path: str,
        plan: EditPlan,
        platform: str,
        state: VideoEditorState,
    ):
        """Render video for a specific platform"""
        specs = PLATFORM_SPECS.get(platform, PLATFORM_SPECS["instagram_reels"])
        
        target_width = specs["width"]
        target_height = specs["height"]
        target_fps = specs.get("fps", 30)
        target_duration = plan.target_duration
        
        # Build FFmpeg filter complex
        filter_parts = []
        
        # 1. Scale and crop to target aspect ratio
        filter_parts.append(
            f"scale={target_width}:{target_height}:force_original_aspect_ratio=increase,"
            f"crop={target_width}:{target_height}"
        )
        
        # 2. Set framerate
        filter_parts.append(f"fps={target_fps}")
        
        # 3. Apply color grading if specified
        if plan.color_grade_preset:
            color_filter = self._get_color_grade_filter(plan.color_grade_preset)
            if color_filter:
                filter_parts.append(color_filter)
        
        # 4. Add fade in/out
        filter_parts.append(f"fade=t=in:st=0:d=0.5,fade=t=out:st={target_duration-0.5}:d=0.5")
        
        # Build filter chain
        vf = ",".join(filter_parts)
        
        # Build FFmpeg command
        try:
            input_stream = ffmpeg.input(source_path)
            
            # Trim to target duration
            video = input_stream.video.filter('trim', duration=target_duration).filter('setpts', 'PTS-STARTPTS')
            audio = input_stream.audio.filter('atrim', duration=target_duration).filter('asetpts', 'PTS-STARTPTS')
            
            # Apply video filters
            video = video.filter('scale', target_width, target_height, force_original_aspect_ratio='increase')
            video = video.filter('crop', target_width, target_height)
            video = video.filter('fps', fps=target_fps)
            video = video.filter('fade', t='in', st=0, d=0.5)
            video = video.filter('fade', t='out', st=target_duration-0.5, d=0.5)
            
            # Output
            output = ffmpeg.output(
                video,
                audio,
                output_path,
                vcodec='libx264',
                acodec='aac',
                video_bitrate='4M',
                audio_bitrate='192k',
                preset='medium',
                movflags='+faststart',
            )
            
            # Run
            output.overwrite_output().run(capture_stdout=True, capture_stderr=True)
            
            logger.info(f"Rendered video for {platform}: {output_path}")
            
        except ffmpeg.Error as e:
            logger.error(f"FFmpeg error: {e.stderr.decode() if e.stderr else str(e)}")
            # Fallback to simpler command
            await self._render_simple(source_path, output_path, target_width, target_height, target_duration)
    
    async def _render_simple(
        self,
        source_path: str,
        output_path: str,
        width: int,
        height: int,
        duration: float,
    ):
        """Simple fallback render using subprocess"""
        cmd = [
            "ffmpeg", "-y",
            "-i", source_path,
            "-t", str(duration),
            "-vf", f"scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height},fps=30",
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "23",
            "-c:a", "aac",
            "-b:a", "192k",
            "-movflags", "+faststart",
            output_path,
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg failed: {result.stderr}")
        
        logger.info(f"Rendered video (simple): {output_path}")
    
    def _get_color_grade_filter(self, preset: str) -> Optional[str]:
        """Get FFmpeg filter for color grading preset"""
        presets = {
            "natural": "eq=saturation=1.0:contrast=1.0:brightness=0.0",
            "vibrant": "eq=saturation=1.3:contrast=1.1:brightness=0.05",
            "warm": "colorbalance=rs=0.1:gs=0.0:bs=-0.1:rm=0.1:gm=0.0:bm=-0.1",
            "cinematic": "eq=saturation=0.9:contrast=1.15,colorbalance=rs=-0.05:bs=0.05",
            "bright": "eq=brightness=0.1:contrast=1.05:saturation=1.1",
        }
        return presets.get(preset)
    
    async def _generate_thumbnail(self, video_path: str, thumb_path: str):
        """Generate thumbnail from video"""
        try:
            (
                ffmpeg
                .input(video_path, ss=1)  # 1 second in
                .output(thumb_path, vframes=1, **{'q:v': 2})
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
            logger.info(f"Generated thumbnail: {thumb_path}")
        except Exception as e:
            logger.warning(f"Thumbnail generation failed: {e}")
    
    async def _add_captions(
        self,
        video_path: str,
        output_path: str,
        captions: List[Dict[str, Any]],
        style: Dict[str, Any],
    ):
        """Add captions/subtitles to video"""
        if not captions:
            return video_path
        
        # Create SRT file
        srt_path = video_path.replace(".mp4", ".srt")
        self._create_srt_file(captions, srt_path)
        
        # Burn in subtitles
        font_size = style.get("font_size", 42)
        font_color = style.get("font_color", "white")
        
        try:
            (
                ffmpeg
                .input(video_path)
                .output(
                    output_path,
                    vf=f"subtitles={srt_path}:force_style='FontSize={font_size},PrimaryColour=&H{font_color[1:]}&'",
                    acodec='copy',
                )
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
            return output_path
        except Exception as e:
            logger.warning(f"Caption burn-in failed: {e}")
            return video_path
    
    def _create_srt_file(self, captions: List[Dict[str, Any]], srt_path: str):
        """Create SRT subtitle file"""
        with open(srt_path, "w", encoding="utf-8") as f:
            for i, cap in enumerate(captions, 1):
                start = self._format_srt_time(cap.get("start", 0))
                end = self._format_srt_time(cap.get("end", 0))
                text = cap.get("text", "")
                
                f.write(f"{i}\n")
                f.write(f"{start} --> {end}\n")
                f.write(f"{text}\n\n")
    
    def _format_srt_time(self, seconds: float) -> str:
        """Format seconds as SRT timestamp"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


# =============================================================================
# MODULE FUNCTION
# =============================================================================

async def execute_edits(state: VideoEditorState, storage_client=None) -> VideoEditorState:
    """Convenience function to execute edits"""
    executor = EditExecutor(storage_client=storage_client)
    return await executor.execute(state)
