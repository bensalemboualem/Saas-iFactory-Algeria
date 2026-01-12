"""
FFmpeg Service - Video processing and montage
"""
import asyncio
import subprocess
import json
from typing import List, Dict, Any, Optional
from pathlib import Path
from dataclasses import dataclass
from enum import Enum


class TransitionType(Enum):
    CUT = "cut"
    FADE = "fade"
    DISSOLVE = "dissolve"
    WIPE = "wipe"
    SLIDE_LEFT = "slide_left"
    SLIDE_RIGHT = "slide_right"
    ZOOM = "zoom"


@dataclass
class VideoClip:
    path: str
    start: float = 0
    end: Optional[float] = None
    volume: float = 1.0
    speed: float = 1.0


@dataclass
class AudioClip:
    path: str
    start: float = 0
    duration: Optional[float] = None
    volume: float = 1.0
    fade_in: float = 0
    fade_out: float = 0


@dataclass
class TextOverlay:
    text: str
    x: str = "center"
    y: str = "center"
    font_size: int = 48
    font_color: str = "white"
    font: str = "Arial"
    start: float = 0
    duration: float = 5
    shadow: bool = True


@dataclass
class ImageOverlay:
    path: str
    x: int = 0
    y: int = 0
    width: Optional[int] = None
    height: Optional[int] = None
    start: float = 0
    duration: float = 5
    opacity: float = 1.0


class FFmpegService:
    """Professional video processing with FFmpeg"""

    def __init__(self, ffmpeg_path: str = "ffmpeg", ffprobe_path: str = "ffprobe"):
        self.ffmpeg = ffmpeg_path
        self.ffprobe = ffprobe_path

    async def get_media_info(self, file_path: str) -> Dict[str, Any]:
        """Get media file information"""
        cmd = [
            self.ffprobe,
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            file_path
        ]

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, _ = await proc.communicate()

        data = json.loads(stdout.decode())

        result = {
            "duration": float(data.get("format", {}).get("duration", 0)),
            "size": int(data.get("format", {}).get("size", 0)),
            "format": data.get("format", {}).get("format_name"),
        }

        for stream in data.get("streams", []):
            if stream["codec_type"] == "video":
                result["video"] = {
                    "codec": stream.get("codec_name"),
                    "width": stream.get("width"),
                    "height": stream.get("height"),
                    "fps": eval(stream.get("r_frame_rate", "30/1")),
                    "bitrate": stream.get("bit_rate"),
                }
            elif stream["codec_type"] == "audio":
                result["audio"] = {
                    "codec": stream.get("codec_name"),
                    "channels": stream.get("channels"),
                    "sample_rate": stream.get("sample_rate"),
                    "bitrate": stream.get("bit_rate"),
                }

        return result

    async def concatenate_videos(
        self,
        clips: List[VideoClip],
        output_path: str,
        transition: TransitionType = TransitionType.CUT,
        transition_duration: float = 0.5,
    ) -> str:
        """Concatenate video clips with transitions"""

        if transition == TransitionType.CUT:
            # Simple concat
            return await self._concat_simple(clips, output_path)
        else:
            # Complex concat with transitions
            return await self._concat_with_transitions(
                clips, output_path, transition, transition_duration
            )

    async def _concat_simple(
        self,
        clips: List[VideoClip],
        output_path: str,
    ) -> str:
        """Simple concatenation without transitions"""
        # Create concat file
        concat_file = Path(output_path).parent / "concat.txt"

        with open(concat_file, "w") as f:
            for clip in clips:
                f.write(f"file '{clip.path}'\n")

        cmd = [
            self.ffmpeg, "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_file),
            "-c", "copy",
            output_path
        ]

        await self._run_ffmpeg(cmd)
        concat_file.unlink()

        return output_path

    async def _concat_with_transitions(
        self,
        clips: List[VideoClip],
        output_path: str,
        transition: TransitionType,
        duration: float,
    ) -> str:
        """Concatenation with xfade transitions"""
        if len(clips) < 2:
            return await self._concat_simple(clips, output_path)

        # Build complex filter
        filter_parts = []
        inputs = []

        for i, clip in enumerate(clips):
            inputs.extend(["-i", clip.path])

        # Get durations
        durations = []
        for clip in clips:
            info = await self.get_media_info(clip.path)
            durations.append(info["duration"])

        # Build xfade chain
        prev_label = "[0:v]"
        for i in range(1, len(clips)):
            offset = sum(durations[:i]) - duration * i
            next_label = f"[v{i}]" if i < len(clips) - 1 else "[vout]"

            transition_name = self._get_xfade_name(transition)
            filter_parts.append(
                f"{prev_label}[{i}:v]xfade=transition={transition_name}:duration={duration}:offset={offset}{next_label}"
            )
            prev_label = next_label

        # Audio crossfade
        prev_audio = "[0:a]"
        for i in range(1, len(clips)):
            offset = sum(durations[:i]) - duration * i
            next_audio = f"[a{i}]" if i < len(clips) - 1 else "[aout]"
            filter_parts.append(
                f"{prev_audio}[{i}:a]acrossfade=d={duration}:c1=tri:c2=tri{next_audio}"
            )
            prev_audio = next_audio

        filter_complex = ";".join(filter_parts)

        cmd = [
            self.ffmpeg, "-y",
            *inputs,
            "-filter_complex", filter_complex,
            "-map", "[vout]",
            "-map", "[aout]",
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "23",
            "-c:a", "aac",
            "-b:a", "192k",
            output_path
        ]

        await self._run_ffmpeg(cmd)
        return output_path

    def _get_xfade_name(self, transition: TransitionType) -> str:
        """Map transition type to FFmpeg xfade name"""
        mapping = {
            TransitionType.FADE: "fade",
            TransitionType.DISSOLVE: "dissolve",
            TransitionType.WIPE: "wipeleft",
            TransitionType.SLIDE_LEFT: "slideleft",
            TransitionType.SLIDE_RIGHT: "slideright",
            TransitionType.ZOOM: "zoomin",
        }
        return mapping.get(transition, "fade")

    async def add_audio_track(
        self,
        video_path: str,
        audio: AudioClip,
        output_path: str,
        mix_original: bool = True,
        original_volume: float = 0.3,
    ) -> str:
        """Add audio track to video"""
        filter_parts = []

        # Audio processing
        audio_filter = f"[1:a]volume={audio.volume}"
        if audio.fade_in > 0:
            audio_filter += f",afade=t=in:d={audio.fade_in}"
        if audio.fade_out > 0:
            audio_filter += f",afade=t=out:st={audio.duration - audio.fade_out}:d={audio.fade_out}"
        audio_filter += "[music]"
        filter_parts.append(audio_filter)

        if mix_original:
            filter_parts.append(f"[0:a]volume={original_volume}[orig]")
            filter_parts.append("[orig][music]amix=inputs=2:duration=first[aout]")
        else:
            filter_parts.append("[music]anull[aout]")

        filter_complex = ";".join(filter_parts)

        cmd = [
            self.ffmpeg, "-y",
            "-i", video_path,
            "-i", audio.path,
            "-filter_complex", filter_complex,
            "-map", "0:v",
            "-map", "[aout]",
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            output_path
        ]

        await self._run_ffmpeg(cmd)
        return output_path

    async def add_text_overlay(
        self,
        video_path: str,
        overlays: List[TextOverlay],
        output_path: str,
    ) -> str:
        """Add text overlays to video"""
        filter_parts = []

        for i, overlay in enumerate(overlays):
            x = overlay.x if overlay.x not in ["center", "left", "right"] else {
                "center": "(w-text_w)/2",
                "left": "20",
                "right": "w-text_w-20",
            }[overlay.x]

            y = overlay.y if overlay.y not in ["center", "top", "bottom"] else {
                "center": "(h-text_h)/2",
                "top": "20",
                "bottom": "h-text_h-20",
            }[overlay.y]

            shadow_str = ":shadowcolor=black:shadowx=2:shadowy=2" if overlay.shadow else ""

            text_filter = (
                f"drawtext=text='{overlay.text}'"
                f":fontsize={overlay.font_size}"
                f":fontcolor={overlay.font_color}"
                f":x={x}:y={y}"
                f":enable='between(t,{overlay.start},{overlay.start + overlay.duration})'"
                f"{shadow_str}"
            )
            filter_parts.append(text_filter)

        filter_str = ",".join(filter_parts)

        cmd = [
            self.ffmpeg, "-y",
            "-i", video_path,
            "-vf", filter_str,
            "-c:a", "copy",
            output_path
        ]

        await self._run_ffmpeg(cmd)
        return output_path

    async def add_image_overlay(
        self,
        video_path: str,
        overlay: ImageOverlay,
        output_path: str,
    ) -> str:
        """Add image overlay (logo, watermark, etc.)"""
        scale_str = ""
        if overlay.width or overlay.height:
            w = overlay.width or -1
            h = overlay.height or -1
            scale_str = f"[1:v]scale={w}:{h}[ovr];"
            overlay_ref = "[ovr]"
        else:
            overlay_ref = "[1:v]"

        filter_complex = (
            f"{scale_str}[0:v]{overlay_ref}overlay={overlay.x}:{overlay.y}"
            f":enable='between(t,{overlay.start},{overlay.start + overlay.duration})'"
        )

        cmd = [
            self.ffmpeg, "-y",
            "-i", video_path,
            "-i", overlay.path,
            "-filter_complex", filter_complex,
            "-c:a", "copy",
            output_path
        ]

        await self._run_ffmpeg(cmd)
        return output_path

    async def resize_video(
        self,
        video_path: str,
        output_path: str,
        width: int,
        height: int,
        maintain_aspect: bool = True,
    ) -> str:
        """Resize video to specific dimensions"""
        if maintain_aspect:
            scale = f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2"
        else:
            scale = f"scale={width}:{height}"

        cmd = [
            self.ffmpeg, "-y",
            "-i", video_path,
            "-vf", scale,
            "-c:a", "copy",
            output_path
        ]

        await self._run_ffmpeg(cmd)
        return output_path

    async def create_thumbnail(
        self,
        video_path: str,
        output_path: str,
        timestamp: float = 0,
        width: int = 1280,
        height: int = 720,
    ) -> str:
        """Extract thumbnail from video"""
        cmd = [
            self.ffmpeg, "-y",
            "-ss", str(timestamp),
            "-i", video_path,
            "-vframes", "1",
            "-vf", f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2",
            output_path
        ]

        await self._run_ffmpeg(cmd)
        return output_path

    async def extract_audio(
        self,
        video_path: str,
        output_path: str,
        format: str = "mp3",
    ) -> str:
        """Extract audio from video"""
        codec = "libmp3lame" if format == "mp3" else "aac"

        cmd = [
            self.ffmpeg, "-y",
            "-i", video_path,
            "-vn",
            "-c:a", codec,
            "-b:a", "192k",
            output_path
        ]

        await self._run_ffmpeg(cmd)
        return output_path

    async def image_to_video(
        self,
        image_path: str,
        output_path: str,
        duration: float = 5,
        zoom_effect: bool = False,
    ) -> str:
        """Convert still image to video with optional Ken Burns effect"""
        if zoom_effect:
            # Ken Burns effect
            filter_str = (
                f"zoompan=z='min(zoom+0.0015,1.5)':d={int(duration * 30)}"
                f":x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080"
            )
        else:
            filter_str = "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2"

        cmd = [
            self.ffmpeg, "-y",
            "-loop", "1",
            "-i", image_path,
            "-vf", filter_str,
            "-t", str(duration),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-r", "30",
            output_path
        ]

        await self._run_ffmpeg(cmd)
        return output_path

    async def change_speed(
        self,
        video_path: str,
        output_path: str,
        speed: float = 1.0,
    ) -> str:
        """Change video playback speed"""
        video_filter = f"setpts={1/speed}*PTS"
        audio_filter = f"atempo={speed}"

        # atempo only supports 0.5 to 2.0, chain for extreme values
        if speed < 0.5 or speed > 2.0:
            audio_filters = []
            remaining = speed
            while remaining < 0.5:
                audio_filters.append("atempo=0.5")
                remaining *= 2
            while remaining > 2.0:
                audio_filters.append("atempo=2.0")
                remaining /= 2
            audio_filters.append(f"atempo={remaining}")
            audio_filter = ",".join(audio_filters)

        cmd = [
            self.ffmpeg, "-y",
            "-i", video_path,
            "-vf", video_filter,
            "-af", audio_filter,
            "-c:v", "libx264",
            "-c:a", "aac",
            output_path
        ]

        await self._run_ffmpeg(cmd)
        return output_path

    async def export_for_platform(
        self,
        video_path: str,
        output_path: str,
        platform: str = "youtube",
    ) -> str:
        """Export video optimized for specific platform"""
        presets = {
            "youtube": {
                "resolution": "1920x1080",
                "bitrate": "8M",
                "audio_bitrate": "320k",
            },
            "tiktok": {
                "resolution": "1080x1920",
                "bitrate": "6M",
                "audio_bitrate": "192k",
            },
            "instagram_reel": {
                "resolution": "1080x1920",
                "bitrate": "5M",
                "audio_bitrate": "192k",
            },
            "instagram_feed": {
                "resolution": "1080x1080",
                "bitrate": "5M",
                "audio_bitrate": "192k",
            },
            "linkedin": {
                "resolution": "1920x1080",
                "bitrate": "6M",
                "audio_bitrate": "192k",
            },
            "twitter": {
                "resolution": "1280x720",
                "bitrate": "5M",
                "audio_bitrate": "192k",
            },
        }

        preset = presets.get(platform, presets["youtube"])
        w, h = preset["resolution"].split("x")

        cmd = [
            self.ffmpeg, "-y",
            "-i", video_path,
            "-vf", f"scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2",
            "-c:v", "libx264",
            "-preset", "slow",
            "-b:v", preset["bitrate"],
            "-c:a", "aac",
            "-b:a", preset["audio_bitrate"],
            "-movflags", "+faststart",
            output_path
        ]

        await self._run_ffmpeg(cmd)
        return output_path

    async def _run_ffmpeg(self, cmd: List[str]) -> None:
        """Run FFmpeg command"""
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        _, stderr = await proc.communicate()

        if proc.returncode != 0:
            raise Exception(f"FFmpeg error: {stderr.decode()}")


# Singleton
ffmpeg_service = FFmpegService()
