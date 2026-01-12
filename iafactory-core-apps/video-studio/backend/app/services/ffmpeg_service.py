"""
FFmpeg Video Assembly Service
Assemble video segments, audio, music and subtitles into final video
"""

import asyncio
import os
import shutil
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from pathlib import Path
import structlog
import aiohttp
import aiofiles

logger = structlog.get_logger()


@dataclass
class VideoSegment:
    """A video segment to include in the timeline"""
    url: str
    start_time: float
    duration: float
    transition: str = "fade"
    shot_id: Optional[int] = None


@dataclass 
class AudioTrack:
    """An audio track (narration or music)"""
    url: str
    start_time: float = 0
    volume: float = 1.0
    fade_in: float = 0
    fade_out: float = 0
    is_music: bool = False


@dataclass
class Subtitle:
    """A subtitle entry"""
    text: str
    start_time: float
    end_time: float
    style: str = "default"


@dataclass
class AssemblyConfig:
    """Configuration for video assembly"""
    output_path: str
    resolution: str = "1920x1080"
    fps: int = 30
    codec: str = "libx264"
    preset: str = "medium"
    crf: int = 23
    audio_codec: str = "aac"
    audio_bitrate: str = "192k"


class FFmpegService:
    """Service for assembling videos with FFmpeg"""
    
    def __init__(self, work_dir: Optional[str] = None):
        self.work_dir = work_dir or "/tmp/video-studio"
        Path(self.work_dir).mkdir(parents=True, exist_ok=True)
        
    async def download_file(self, url: str, filename: str) -> str:
        """Download a file from URL"""
        filepath = os.path.join(self.work_dir, filename)
        
        if url.startswith("https://example.com"):
            logger.warning("Mock URL detected, creating placeholder", url=url)
            await self._create_placeholder_video(filepath, 5)
            return filepath
            
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        async with aiofiles.open(filepath, mode="wb") as f:
                            await f.write(await resp.read())
                        return filepath
                    else:
                        raise Exception(f"Download failed: {resp.status}")
        except Exception as e:
            logger.error("Download error", url=url, error=str(e))
            raise
    
    async def _create_placeholder_video(self, filepath: str, duration: int = 5):
        """Create a placeholder black video"""
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", f"color=c=black:s=1920x1080:d={duration}",
            "-f", "lavfi",
            "-i", f"anullsrc=r=44100:cl=stereo",
            "-t", str(duration),
            "-c:v", "libx264",
            "-c:a", "aac",
            "-shortest",
            filepath
        ]
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await process.wait()
        
    async def concat_videos(
        self,
        segments: List[VideoSegment],
        output_path: str,
        config: Optional[AssemblyConfig] = None
    ) -> str:
        """Concatenate video segments with transitions"""
        if not config:
            config = AssemblyConfig(output_path=output_path)
            
        local_files = []
        for i, seg in enumerate(segments):
            try:
                local_path = await self.download_file(seg.url, f"segment_{i}.mp4")
                local_files.append(local_path)
            except Exception as e:
                logger.error("Failed to download segment", index=i, error=str(e))
                continue
                
        if not local_files:
            raise Exception("No video segments available")
            
        concat_file = os.path.join(self.work_dir, "concat.txt")
        with open(concat_file, "w") as f:
            for path in local_files:
                f.write(f"file '{path}'\n")
                
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_file,
            "-c:v", config.codec,
            "-preset", config.preset,
            "-crf", str(config.crf),
            "-c:a", config.audio_codec,
            "-b:a", config.audio_bitrate,
            "-s", config.resolution,
            "-r", str(config.fps),
            output_path
        ]
        
        logger.info("Running FFmpeg concat", cmd=" ".join(cmd))
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            logger.error("FFmpeg concat failed", stderr=stderr.decode())
            raise Exception(f"FFmpeg error: {stderr.decode()[-500:]}")
            
        return output_path
        
    async def add_audio_tracks(
        self,
        video_path: str,
        audio_tracks: List[AudioTrack],
        output_path: str
    ) -> str:
        """Add audio tracks (narration and music) to video"""
        
        audio_inputs = []
        for i, track in enumerate(audio_tracks):
            try:
                suffix = "music" if track.is_music else "narration"
                local_path = await self.download_file(track.url, f"{suffix}_{i}.mp3")
                audio_inputs.append((local_path, track))
            except Exception as e:
                logger.warning("Failed to download audio", index=i, error=str(e))
                continue
                
        if not audio_inputs:
            shutil.copy(video_path, output_path)
            return output_path
            
        inputs = ["-i", video_path]
        filter_parts = []
        
        for i, (path, track) in enumerate(audio_inputs):
            inputs.extend(["-i", path])
            input_idx = i + 1
            filter_parts.append(
                f"[{input_idx}:a]volume={track.volume},adelay={int(track.start_time*1000)}|{int(track.start_time*1000)}[a{i}]"
            )
            
        audio_labels = "".join([f"[a{i}]" for i in range(len(audio_inputs))])
        filter_parts.append(f"[0:a]{audio_labels}amix=inputs={len(audio_inputs)+1}:duration=longest[aout]")
        
        filter_complex = ";".join(filter_parts)
        
        cmd = [
            "ffmpeg", "-y",
            *inputs,
            "-filter_complex", filter_complex,
            "-map", "0:v",
            "-map", "[aout]",
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            output_path
        ]
        
        logger.info("Adding audio tracks", num_tracks=len(audio_inputs))
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            logger.error("FFmpeg audio mix failed", stderr=stderr.decode()[-500:])
            shutil.copy(video_path, output_path)
            
        return output_path
        
    async def add_subtitles(
        self,
        video_path: str,
        subtitles: List[Subtitle],
        output_path: str,
        burn_in: bool = True
    ) -> str:
        """Add subtitles to video"""
        
        srt_path = os.path.join(self.work_dir, "subtitles.srt")
        with open(srt_path, "w", encoding="utf-8") as f:
            for i, sub in enumerate(subtitles, 1):
                start = self._seconds_to_srt_time(sub.start_time)
                end = self._seconds_to_srt_time(sub.end_time)
                f.write(f"{i}\n{start} --> {end}\n{sub.text}\n\n")
        
        if not subtitles:
            shutil.copy(video_path, output_path)
            return output_path
                
        if burn_in:
            style = "FontSize=24,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=2"
            cmd = [
                "ffmpeg", "-y",
                "-i", video_path,
                "-vf", f"subtitles={srt_path}:force_style='{style}'",
                "-c:a", "copy",
                output_path
            ]
        else:
            cmd = [
                "ffmpeg", "-y",
                "-i", video_path,
                "-i", srt_path,
                "-c:v", "copy",
                "-c:a", "copy",
                "-c:s", "mov_text",
                output_path
            ]
            
        logger.info("Adding subtitles", num_subs=len(subtitles), burn_in=burn_in)
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            logger.error("FFmpeg subtitles failed", stderr=stderr.decode()[-500:])
            shutil.copy(video_path, output_path)
            
        return output_path
        
    def _seconds_to_srt_time(self, seconds: float) -> str:
        """Convert seconds to SRT time format"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds - int(seconds)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
        
    async def full_assembly(
        self,
        segments: List[VideoSegment],
        audio_tracks: List[AudioTrack],
        subtitles: List[Subtitle],
        output_path: str,
        config: Optional[AssemblyConfig] = None
    ) -> Dict[str, Any]:
        """Full video assembly pipeline"""
        try:
            temp_concat = os.path.join(self.work_dir, "temp_concat.mp4")
            await self.concat_videos(segments, temp_concat, config)
            
            temp_audio = os.path.join(self.work_dir, "temp_audio.mp4")
            await self.add_audio_tracks(temp_concat, audio_tracks, temp_audio)
            
            await self.add_subtitles(temp_audio, subtitles, output_path)
            
            duration = await self._get_duration(output_path)
            file_size = os.path.getsize(output_path)
            
            return {
                "success": True,
                "output_path": output_path,
                "duration": duration,
                "file_size": file_size,
                "file_size_mb": round(file_size / (1024 * 1024), 2)
            }
            
        except Exception as e:
            logger.error("Full assembly failed", error=str(e))
            return {
                "success": False,
                "error": str(e)
            }
        finally:
            for f in ["temp_concat.mp4", "temp_audio.mp4", "concat.txt", "subtitles.srt"]:
                try:
                    os.remove(os.path.join(self.work_dir, f))
                except:
                    pass
                    
    async def _get_duration(self, video_path: str) -> float:
        """Get video duration using ffprobe"""
        cmd = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            video_path
        ]
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, _ = await process.communicate()
        try:
            return float(stdout.decode().strip())
        except:
            return 0.0

    def cleanup(self):
        """Remove all temp files"""
        try:
            shutil.rmtree(self.work_dir)
        except:
            pass
