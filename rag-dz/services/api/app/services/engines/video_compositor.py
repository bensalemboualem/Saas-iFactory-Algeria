"""
Professional Video Composition with MoviePy
Combines video clips, audio, music, and effects
"""
import logging
from pathlib import Path
from typing import List, Optional, Dict, Tuple
import numpy as np
from moviepy.editor import (
    VideoFileClip, AudioFileClip, ImageClip, TextClip,
    concatenate_videoclips, CompositeVideoClip, CompositeAudioClip,
    vfx, afx
)
from moviepy.video.fx import all as vfx_all
from moviepy.audio.fx import all as afx_all
from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)

class VideoCompositor:
    """
    Professional video composition and editing

    Features:
    - Multi-clip concatenation
    - Audio mixing (voice-over + background music)
    - Transitions (fade, crossfade)
    - Text overlays
    - Watermarks
    - Aspect ratio adjustment
    - Color grading
    """

    def __init__(self, output_dir: Path = Path("/tmp/dzirvideo")):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"VideoCompositor initialized, output: {output_dir}")

    def compose_video(
        self,
        scene_videos: List[Path],
        voiceover_audio: Optional[Path] = None,
        background_music: Optional[Path] = None,
        aspect_ratio: str = "16:9",
        fps: int = 30,
        add_watermark: bool = False,
        watermark_text: str = "Dzir IA Video",
        transitions: str = "fade",
        output_path: Optional[Path] = None
    ) -> Path:
        """
        Compose final video from scenes and audio

        Args:
            scene_videos: List of scene video file paths
            voiceover_audio: Voice-over audio file
            background_music: Background music file
            aspect_ratio: Target aspect ratio (16:9, 9:16, 1:1)
            fps: Frames per second
            add_watermark: Add watermark to video
            watermark_text: Watermark text
            transitions: Transition type (fade, crossfade, none)
            output_path: Output video path

        Returns:
            Path to composed video
        """
        try:
            logger.info(f"Composing video from {len(scene_videos)} scenes...")

            # Load video clips
            clips = [VideoFileClip(str(path)) for path in scene_videos]

            # Resize clips to match aspect ratio
            target_size = self._get_target_size(aspect_ratio)
            clips = [self._resize_clip(clip, target_size) for clip in clips]

            # Apply transitions
            if transitions == "fade":
                final_clip = self._apply_fade_transitions(clips)
            elif transitions == "crossfade":
                final_clip = self._apply_crossfade_transitions(clips)
            else:
                final_clip = concatenate_videoclips(clips, method="compose")

            # Adjust FPS
            final_clip = final_clip.set_fps(fps)

            # Add watermark
            if add_watermark:
                final_clip = self._add_watermark(final_clip, watermark_text)

            # Compose audio
            audio_clips = []

            # Add voice-over
            if voiceover_audio:
                voiceover = AudioFileClip(str(voiceover_audio))
                audio_clips.append(voiceover)

            # Add background music
            if background_music:
                music = AudioFileClip(str(background_music))
                # Loop music to match video duration
                if music.duration < final_clip.duration:
                    music = afx.audio_loop(music, duration=final_clip.duration)
                # Reduce music volume to 20% (ducking for voice-over)
                music = music.volumex(0.2 if voiceover_audio else 0.6)
                audio_clips.append(music)

            # Mix audio
            if audio_clips:
                final_audio = CompositeAudioClip(audio_clips)
                final_clip = final_clip.set_audio(final_audio)

            # Generate output path
            if output_path is None:
                output_path = self.output_dir / f"final_video_{aspect_ratio.replace(':', 'x')}.mp4"

            # Write final video
            logger.info(f"Writing final video to {output_path}...")
            final_clip.write_videofile(
                str(output_path),
                codec='libx264',
                audio_codec='aac',
                fps=fps,
                preset='medium',
                threads=4,
                logger=None  # Suppress moviepy logging
            )

            # Clean up
            for clip in clips:
                clip.close()
            final_clip.close()
            if audio_clips:
                for audio in audio_clips:
                    audio.close()

            logger.info(f"Video composition complete: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Video composition failed: {str(e)}")
            raise

    def _get_target_size(self, aspect_ratio: str) -> Tuple[int, int]:
        """Get target dimensions for aspect ratio"""
        sizes = {
            "16:9": (1920, 1080),
            "9:16": (1080, 1920),
            "1:1": (1080, 1080),
            "4:3": (1440, 1080)
        }
        return sizes.get(aspect_ratio, (1920, 1080))

    def _resize_clip(self, clip: VideoFileClip, target_size: Tuple[int, int]) -> VideoFileClip:
        """Resize and crop clip to target size"""
        target_w, target_h = target_size
        target_ratio = target_w / target_h

        clip_ratio = clip.w / clip.h

        if clip_ratio > target_ratio:
            # Clip is wider - fit height and crop width
            new_clip = clip.resize(height=target_h)
            x_center = new_clip.w / 2
            x1 = x_center - target_w / 2
            new_clip = new_clip.crop(x1=x1, x2=x1 + target_w)
        else:
            # Clip is taller - fit width and crop height
            new_clip = clip.resize(width=target_w)
            y_center = new_clip.h / 2
            y1 = y_center - target_h / 2
            new_clip = new_clip.crop(y1=y1, y2=y1 + target_h)

        return new_clip

    def _apply_fade_transitions(
        self,
        clips: List[VideoFileClip],
        fade_duration: float = 0.5
    ) -> VideoFileClip:
        """Apply fade in/out transitions between clips"""
        processed_clips = []

        for i, clip in enumerate(clips):
            # Fade in on first clip
            if i == 0:
                clip = clip.fadein(fade_duration)

            # Fade out on last clip
            if i == len(clips) - 1:
                clip = clip.fadeout(fade_duration)

            processed_clips.append(clip)

        return concatenate_videoclips(processed_clips, method="compose")

    def _apply_crossfade_transitions(
        self,
        clips: List[VideoFileClip],
        crossfade_duration: float = 0.5
    ) -> VideoFileClip:
        """Apply crossfade transitions between clips"""
        if len(clips) == 1:
            return clips[0]

        # Apply crossfade
        result = clips[0]
        for next_clip in clips[1:]:
            result = concatenate_videoclips(
                [result, next_clip],
                method="compose",
                padding=-crossfade_duration
            )

        return result

    def _add_watermark(
        self,
        clip: VideoFileClip,
        text: str,
        position: str = "bottom-right",
        opacity: float = 0.5
    ) -> CompositeVideoClip:
        """Add watermark to video"""
        try:
            # Create text clip
            txt_clip = TextClip(
                text,
                fontsize=24,
                color='white',
                font='Arial',
                stroke_color='black',
                stroke_width=1
            )

            # Set duration to match video
            txt_clip = txt_clip.set_duration(clip.duration)

            # Set position
            if position == "bottom-right":
                txt_clip = txt_clip.set_position(('right', 'bottom')).margin(right=20, bottom=20, opacity=0)
            elif position == "bottom-left":
                txt_clip = txt_clip.set_position(('left', 'bottom')).margin(left=20, bottom=20, opacity=0)
            elif position == "top-right":
                txt_clip = txt_clip.set_position(('right', 'top')).margin(right=20, top=20, opacity=0)
            elif position == "top-left":
                txt_clip = txt_clip.set_position(('left', 'top')).margin(left=20, top=20, opacity=0)

            # Set opacity
            txt_clip = txt_clip.set_opacity(opacity)

            # Composite watermark onto video
            return CompositeVideoClip([clip, txt_clip])

        except Exception as e:
            logger.warning(f"Failed to add watermark: {str(e)}")
            return clip

    def add_intro_outro(
        self,
        video_clip: VideoFileClip,
        intro_clip: Optional[VideoFileClip] = None,
        outro_clip: Optional[VideoFileClip] = None
    ) -> VideoFileClip:
        """Add intro and outro to video"""
        clips = []

        if intro_clip:
            clips.append(intro_clip)

        clips.append(video_clip)

        if outro_clip:
            clips.append(outro_clip)

        if len(clips) == 1:
            return clips[0]

        return concatenate_videoclips(clips, method="compose")

    def create_title_card(
        self,
        title: str,
        subtitle: Optional[str] = None,
        duration: float = 3.0,
        size: Tuple[int, int] = (1920, 1080),
        bg_color: str = "#00843D"  # Algerian green
    ) -> VideoFileClip:
        """
        Create a title card for video intro

        Args:
            title: Main title text
            subtitle: Optional subtitle
            duration: Duration in seconds
            size: Video size (width, height)
            bg_color: Background color (hex)
        """
        try:
            # Create background image
            bg_img = Image.new('RGB', size, bg_color)
            draw = ImageDraw.Draw(bg_img)

            # Save background
            bg_path = self.output_dir / "title_bg.png"
            bg_img.save(bg_path)

            # Create background clip
            bg_clip = ImageClip(str(bg_path), duration=duration)

            # Create title text
            title_clip = TextClip(
                title,
                fontsize=80,
                color='white',
                font='Arial-Bold',
                size=size
            ).set_duration(duration).set_position('center')

            # Create subtitle if provided
            clips = [bg_clip, title_clip]
            if subtitle:
                subtitle_clip = TextClip(
                    subtitle,
                    fontsize=40,
                    color='white',
                    font='Arial',
                    size=size
                ).set_duration(duration).set_position(('center', 0.6), relative=True)
                clips.append(subtitle_clip)

            # Composite
            final_clip = CompositeVideoClip(clips)

            return final_clip

        except Exception as e:
            logger.error(f"Failed to create title card: {str(e)}")
            raise

    def apply_color_grading(
        self,
        clip: VideoFileClip,
        preset: str = "cinematic"
    ) -> VideoFileClip:
        """
        Apply color grading preset

        Presets:
        - cinematic: Warm, contrasty look
        - bright: Increased brightness and saturation
        - vintage: Faded, nostalgic look
        - cool: Cool blue tones
        """
        try:
            if preset == "cinematic":
                # Increase contrast and warmth
                clip = clip.fx(vfx_all.colorx, 1.2)  # Slight brightness boost
                # Note: More advanced color grading would require custom functions
            elif preset == "bright":
                clip = clip.fx(vfx_all.colorx, 1.3)
            elif preset == "vintage":
                clip = clip.fx(vfx_all.colorx, 0.9)
            elif preset == "cool":
                clip = clip.fx(vfx_all.colorx, 1.0)

            return clip

        except Exception as e:
            logger.warning(f"Color grading failed: {str(e)}")
            return clip

    def create_thumbnail(
        self,
        video_path: Path,
        timestamp: float = 0.5,
        output_path: Optional[Path] = None
    ) -> Path:
        """
        Extract thumbnail from video

        Args:
            video_path: Video file path
            timestamp: Time position to extract (seconds or fraction)
            output_path: Thumbnail output path

        Returns:
            Path to thumbnail image
        """
        try:
            clip = VideoFileClip(str(video_path))

            # Calculate timestamp
            if timestamp < 1.0:
                timestamp = clip.duration * timestamp

            # Extract frame
            frame = clip.get_frame(timestamp)

            # Generate output path
            if output_path is None:
                output_path = self.output_dir / f"{video_path.stem}_thumb.jpg"

            # Save as image
            img = Image.fromarray(frame)
            img.save(output_path, quality=95)

            clip.close()

            logger.info(f"Thumbnail created: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Thumbnail creation failed: {str(e)}")
            raise


# Utility functions
def get_video_info(video_path: Path) -> Dict:
    """Get video file information"""
    try:
        clip = VideoFileClip(str(video_path))
        info = {
            "duration": clip.duration,
            "fps": clip.fps,
            "size": (clip.w, clip.h),
            "aspect_ratio": f"{clip.w}:{clip.h}",
            "has_audio": clip.audio is not None
        }
        clip.close()
        return info
    except Exception as e:
        logger.error(f"Failed to get video info: {str(e)}")
        return {}


def get_compositor(**kwargs):
    """Get video compositor instance"""
    return VideoCompositor(**kwargs)
