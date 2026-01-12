"""
IA Factory - Platform Converter Service
Phase 3: Video format conversion for multiple platforms
"""

import asyncio
import subprocess
import os
import logging
from typing import List, Dict, Any
from pathlib import Path
from dataclasses import dataclass

from ..models.distribution import Platform, PLATFORM_SPECS
from ..config import settings

logger = logging.getLogger(__name__)


@dataclass
class ConversionResult:
    """Result of a video conversion"""
    platform: str
    input_path: str
    output_path: str
    success: bool
    width: int
    height: int
    duration: float
    file_size_mb: float
    error: str = ""


class PlatformConverter:
    """
    Phase 3: Format Conversion for Multiple Platforms
    
    Converts videos to platform-specific formats using FFmpeg.
    Handles aspect ratios, durations, file sizes, and quality.
    """
    
    def __init__(self):
        self.output_dir = Path(settings.output_dir) / "converted"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    async def convert_for_platforms(
        self,
        source_video: str,
        platforms: List[Platform],
        base_name: str = None
    ) -> Dict[str, ConversionResult]:
        """
        Convert video for multiple platforms
        
        Args:
            source_video: Path to source video
            platforms: List of target platforms
            base_name: Base name for output files
        
        Returns:
            Dictionary mapping platform to conversion result
        """
        
        if base_name is None:
            base_name = Path(source_video).stem
        
        results = {}
        
        for platform in platforms:
            try:
                spec = PLATFORM_SPECS.get(platform)
                if not spec:
                    logger.warning(f"No spec for platform: {platform}")
                    continue
                
                result = await self._convert_video(
                    source=source_video,
                    spec=spec,
                    base_name=base_name
                )
                
                results[platform.value] = result
                
            except Exception as e:
                logger.error(f"Conversion failed for {platform}: {e}")
                results[platform.value] = ConversionResult(
                    platform=platform.value,
                    input_path=source_video,
                    output_path="",
                    success=False,
                    width=0,
                    height=0,
                    duration=0,
                    file_size_mb=0,
                    error=str(e)
                )
        
        return results
    
    async def _convert_video(
        self,
        source: str,
        spec,  # PlatformSpec
        base_name: str
    ) -> ConversionResult:
        """
        Convert single video using FFmpeg
        """
        
        output_filename = f"{base_name}_{spec.platform.value}_{spec.width}x{spec.height}.mp4"
        output_path = self.output_dir / output_filename
        
        # Build FFmpeg command
        cmd = [
            "ffmpeg", "-y",
            "-i", source,
            # Video filters
            "-vf", (
                f"scale={spec.width}:{spec.height}:"
                f"force_original_aspect_ratio=decrease,"
                f"pad={spec.width}:{spec.height}:(ow-iw)/2:(oh-ih)/2:black"
            ),
            # Video codec
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "23",
            "-profile:v", "high",
            "-level", "4.0",
            # Frame rate
            "-r", str(spec.recommended_fps),
            # Audio codec
            "-c:a", "aac",
            "-b:a", "128k",
            "-ar", "44100",
            # Duration limit
            "-t", str(spec.max_duration),
            # Optimize for streaming
            "-movflags", "+faststart",
            "-pix_fmt", "yuv420p",
            str(output_path)
        ]
        
        logger.info(f"Converting for {spec.platform.value}: {spec.width}x{spec.height}")
        
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode() if stderr else "Unknown error"
                logger.error(f"FFmpeg failed: {error_msg}")
                return ConversionResult(
                    platform=spec.platform.value,
                    input_path=source,
                    output_path="",
                    success=False,
                    width=spec.width,
                    height=spec.height,
                    duration=0,
                    file_size_mb=0,
                    error=error_msg[:500]
                )
            
            # Get output file info
            file_size_mb = output_path.stat().st_size / (1024 * 1024)
            
            # Check if file is within size limit
            if file_size_mb > spec.max_file_size_mb:
                logger.warning(
                    f"Output file ({file_size_mb:.1f}MB) exceeds "
                    f"{spec.platform.value} limit ({spec.max_file_size_mb}MB)"
                )
            
            # Get duration using ffprobe
            duration = await self._get_video_duration(str(output_path))
            
            logger.info(f"✅ Converted: {output_filename} ({file_size_mb:.1f}MB)")
            
            return ConversionResult(
                platform=spec.platform.value,
                input_path=source,
                output_path=str(output_path),
                success=True,
                width=spec.width,
                height=spec.height,
                duration=duration,
                file_size_mb=round(file_size_mb, 2)
            )
            
        except Exception as e:
            logger.error(f"Conversion error: {e}")
            return ConversionResult(
                platform=spec.platform.value,
                input_path=source,
                output_path="",
                success=False,
                width=spec.width,
                height=spec.height,
                duration=0,
                file_size_mb=0,
                error=str(e)
            )
    
    async def _get_video_duration(self, video_path: str) -> float:
        """Get video duration using ffprobe"""
        
        cmd = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            video_path
        ]
        
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, _ = await process.communicate()
            return float(stdout.decode().strip())
            
        except:
            return 0.0
    
    async def convert_bulk(
        self,
        videos: List[str],
        platforms: List[Platform],
        batch_size: int = 2
    ) -> Dict[str, Dict[str, ConversionResult]]:
        """
        Convert multiple videos for multiple platforms
        
        Args:
            videos: List of video paths
            platforms: Target platforms
            batch_size: Videos to process in parallel
        
        Returns:
            Dictionary mapping video name to platform results
        """
        
        all_results = {}
        
        for i in range(0, len(videos), batch_size):
            batch = videos[i:i+batch_size]
            
            # Process batch
            batch_tasks = [
                self.convert_for_platforms(video, platforms)
                for video in batch
            ]
            
            batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
            
            for video, result in zip(batch, batch_results):
                video_name = Path(video).stem
                if isinstance(result, Exception):
                    logger.error(f"Batch conversion failed for {video}: {result}")
                    all_results[video_name] = {"error": str(result)}
                else:
                    all_results[video_name] = result
        
        return all_results
    
    def get_platform_specs(self, platform: Platform) -> Dict[str, Any]:
        """Get specifications for a platform"""
        
        spec = PLATFORM_SPECS.get(platform)
        if spec:
            return {
                "platform": spec.platform.value,
                "aspect_ratio": spec.aspect_ratio,
                "width": spec.width,
                "height": spec.height,
                "max_duration": spec.max_duration,
                "recommended_fps": spec.recommended_fps,
                "max_file_size_mb": spec.max_file_size_mb
            }
        return {}
