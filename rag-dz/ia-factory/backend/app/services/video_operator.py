"""
IA Factory - Video Operator (Auto-Editing)
Phase 2: AI-powered video editing using Claude + FFmpeg
"""

import asyncio
import subprocess
import json
import os
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
from anthropic import Anthropic
from datetime import datetime

from ..config import settings

logger = logging.getLogger(__name__)


class VideoOperator:
    """
    Phase 2: IA Factory Video Operator - Auto-Editing
    
    Uses Claude to analyze videos and plan edits,
    then executes them using FFmpeg/MoviePy.
    """
    
    def __init__(self):
        self.llm = Anthropic(api_key=settings.anthropic_api_key)
        self.model = settings.claude_model
        self.output_dir = Path(settings.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    async def auto_edit(
        self,
        video_path: str,
        script: Dict[str, Any],
        brand_guidelines: Dict[str, Any],
        output_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Main auto-editing pipeline
        
        Args:
            video_path: Path to source video
            script: Script with timing and overlay info
            brand_guidelines: Brand visual guidelines
            output_name: Optional output filename
        
        Returns:
            Dictionary with edited video path and metadata
        """
        
        logger.info(f"🎬 Starting auto-edit for: {video_path}")
        
        # Step 1: Analyze video
        analysis = await self._analyze_video(video_path)
        
        # Step 2: Plan edits using Claude
        editing_plan = await self._plan_edits(analysis, script, brand_guidelines)
        
        # Step 3: Execute edits with FFmpeg
        output_path = await self._execute_edits(
            video_path, 
            editing_plan, 
            brand_guidelines,
            output_name
        )
        
        return {
            "status": "completed",
            "input_path": video_path,
            "output_path": output_path,
            "analysis": analysis,
            "editing_plan": editing_plan,
            "edited_at": datetime.now().isoformat()
        }
    
    async def _analyze_video(self, video_path: str) -> Dict[str, Any]:
        """
        Analyze video properties using FFprobe
        """
        
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            video_path
        ]
        
        try:
            result = await asyncio.to_thread(
                subprocess.run,
                cmd,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                logger.error(f"FFprobe failed: {result.stderr}")
                # Return basic analysis
                return {
                    "duration": 15,
                    "width": 1080,
                    "height": 1920,
                    "fps": 30,
                    "has_audio": True
                }
            
            probe_data = json.loads(result.stdout)
            
            # Extract video stream info
            video_stream = next(
                (s for s in probe_data.get('streams', []) if s.get('codec_type') == 'video'),
                {}
            )
            
            audio_stream = next(
                (s for s in probe_data.get('streams', []) if s.get('codec_type') == 'audio'),
                None
            )
            
            format_info = probe_data.get('format', {})
            
            # Parse FPS
            fps_str = video_stream.get('r_frame_rate', '30/1')
            if '/' in fps_str:
                num, den = fps_str.split('/')
                fps = float(num) / float(den) if float(den) > 0 else 30
            else:
                fps = float(fps_str)
            
            return {
                "duration": float(format_info.get('duration', 15)),
                "width": int(video_stream.get('width', 1080)),
                "height": int(video_stream.get('height', 1920)),
                "fps": round(fps, 2),
                "codec": video_stream.get('codec_name', 'unknown'),
                "has_audio": audio_stream is not None,
                "audio_codec": audio_stream.get('codec_name') if audio_stream else None,
                "file_size_mb": float(format_info.get('size', 0)) / (1024 * 1024),
                "bitrate": int(format_info.get('bit_rate', 0))
            }
            
        except Exception as e:
            logger.error(f"Video analysis failed: {e}")
            return {
                "duration": 15,
                "width": 1080,
                "height": 1920,
                "fps": 30,
                "has_audio": True,
                "error": str(e)
            }
    
    async def _plan_edits(
        self,
        analysis: Dict[str, Any],
        script: Dict[str, Any],
        brand_guidelines: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Use Claude to create an intelligent editing plan
        """
        
        visual_style = brand_guidelines.get('visual_guidelines', {})
        primary_color = visual_style.get('primary_color', '#FFFFFF')
        
        prompt = f"""
You are a professional video editor. Create an editing plan for this reel.

VIDEO STATS:
- Duration: {analysis.get('duration', 15):.1f}s
- Resolution: {analysis.get('width', 1080)}x{analysis.get('height', 1920)}
- FPS: {analysis.get('fps', 30)}
- Has Audio: {analysis.get('has_audio', True)}

SCRIPT STRUCTURE:
- Hook: "{script.get('hook', 'Opening hook')}" (0-2s)
- Body: "{script.get('body', 'Main content')}" (2-12s)  
- CTA: "{script.get('cta', 'Call to action')}" (12-15s)

BRAND STYLE:
- Primary Color: {primary_color}
- Style: {visual_style.get('visual_style', 'modern')}

Create an editing plan as JSON with:
1. cuts: Time-based cuts to pace the video
2. transitions: Transition effects between sections
3. text_overlays: Text to display with timing
4. color_grade: Color grading style
5. audio_adjustments: Audio mixing suggestions

Return ONLY valid JSON (no markdown):
{{
    "cuts": [
        {{"start_ms": 0, "end_ms": 2000, "section": "hook"}},
        {{"start_ms": 2000, "end_ms": 12000, "section": "body"}},
        {{"start_ms": 12000, "end_ms": 15000, "section": "cta"}}
    ],
    "transitions": [
        {{"at_ms": 2000, "type": "fade", "duration_ms": 300}},
        {{"at_ms": 12000, "type": "zoom", "duration_ms": 200}}
    ],
    "text_overlays": [
        {{"text": "Key text", "start_ms": 0, "end_ms": 2000, "position": "bottom", "style": "bold"}}
    ],
    "color_grade": "vibrant",
    "audio_adjustments": {{
        "normalize": true,
        "background_music_volume": 0.3,
        "voice_boost": 1.2
    }},
    "export_settings": {{
        "codec": "h264",
        "quality": "high",
        "fps": 30
    }}
}}
"""
        
        try:
            response = await asyncio.to_thread(
                self.llm.messages.create,
                model=self.model,
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}]
            )
            
            text = response.content[0].text
            json_start = text.find('{')
            json_end = text.rfind('}') + 1
            
            if json_start >= 0:
                return json.loads(text[json_start:json_end])
            else:
                raise ValueError("No JSON found in response")
                
        except Exception as e:
            logger.error(f"Edit planning failed: {e}")
            # Return default plan
            return {
                "cuts": [],
                "transitions": [],
                "text_overlays": script.get('text_overlays', []),
                "color_grade": "default",
                "audio_adjustments": {"normalize": True},
                "export_settings": {"codec": "h264", "quality": "high", "fps": 30}
            }
    
    async def _execute_edits(
        self,
        video_path: str,
        plan: Dict[str, Any],
        brand_guidelines: Dict[str, Any],
        output_name: Optional[str] = None
    ) -> str:
        """
        Execute the editing plan using FFmpeg
        """
        
        # Generate output filename
        if output_name:
            output_path = self.output_dir / f"{output_name}.mp4"
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.output_dir / f"edited_{timestamp}.mp4"
        
        # Build FFmpeg filter chain
        filters = []
        
        # Color grading
        color_grade = plan.get('color_grade', 'default')
        if color_grade == 'vibrant':
            filters.append("eq=saturation=1.3:contrast=1.1")
        elif color_grade == 'warm':
            filters.append("colorbalance=rs=0.1:gs=0:bs=-0.1")
        elif color_grade == 'cool':
            filters.append("colorbalance=rs=-0.1:gs=0:bs=0.1")
        
        # Build drawtext filters for overlays
        overlays = plan.get('text_overlays', [])
        visual_style = brand_guidelines.get('visual_guidelines', {})
        font_color = visual_style.get('primary_color', '#FFFFFF').replace('#', '')
        
        for i, overlay in enumerate(overlays):
            text = overlay.get('text', '').replace("'", "\\'")
            start_s = overlay.get('start_ms', 0) / 1000
            end_s = overlay.get('end_ms', 2000) / 1000
            position = overlay.get('position', 'bottom')
            
            # Position mapping
            y_pos = {
                'top': 'h*0.1',
                'center': '(h-text_h)/2',
                'bottom': 'h*0.85'
            }.get(position, 'h*0.85')
            
            drawtext = (
                f"drawtext=text='{text}':"
                f"fontsize=48:fontcolor=white:"
                f"x=(w-text_w)/2:y={y_pos}:"
                f"enable='between(t,{start_s},{end_s})':"
                f"borderw=2:bordercolor=black"
            )
            filters.append(drawtext)
        
        # Build FFmpeg command
        filter_chain = ','.join(filters) if filters else 'null'
        
        export = plan.get('export_settings', {})
        quality = export.get('quality', 'high')
        crf = {'low': 28, 'medium': 23, 'high': 18, 'ultra': 15}.get(quality, 18)
        
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-vf", filter_chain,
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", str(crf),
            "-c:a", "aac",
            "-b:a", "128k",
            "-movflags", "+faststart",
            str(output_path)
        ]
        
        logger.info(f"Executing FFmpeg: {' '.join(cmd)}")
        
        try:
            result = await asyncio.to_thread(
                subprocess.run,
                cmd,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                logger.error(f"FFmpeg failed: {result.stderr}")
                raise Exception(f"FFmpeg error: {result.stderr}")
            
            logger.info(f"✅ Video edited: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Edit execution failed: {e}")
            raise
    
    async def add_captions(
        self,
        video_path: str,
        transcript: List[Dict[str, Any]],
        style: str = "default"
    ) -> str:
        """
        Add captions/subtitles to video
        
        Args:
            video_path: Input video path
            transcript: List of {text, start, end} dictionaries
            style: Caption style preset
        
        Returns:
            Path to captioned video
        """
        
        # Create SRT file
        srt_path = Path(video_path).with_suffix('.srt')
        
        with open(srt_path, 'w', encoding='utf-8') as f:
            for i, segment in enumerate(transcript, 1):
                start = self._format_srt_time(segment.get('start', 0))
                end = self._format_srt_time(segment.get('end', 0))
                text = segment.get('text', '')
                
                f.write(f"{i}\n{start} --> {end}\n{text}\n\n")
        
        # Output path
        output_path = Path(video_path).parent / f"captioned_{Path(video_path).name}"
        
        # Add subtitles with FFmpeg
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-vf", f"subtitles={srt_path}:force_style='FontSize=24,PrimaryColour=&Hffffff'",
            "-c:a", "copy",
            str(output_path)
        ]
        
        await asyncio.to_thread(subprocess.run, cmd, capture_output=True)
        
        # Cleanup
        srt_path.unlink(missing_ok=True)
        
        return str(output_path)
    
    def _format_srt_time(self, seconds: float) -> str:
        """Format seconds to SRT timestamp (HH:MM:SS,mmm)"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    
    async def bulk_edit(
        self,
        videos: List[Dict[str, Any]],
        scripts: List[Dict[str, Any]],
        brand_guidelines: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Process multiple videos in sequence
        
        Args:
            videos: List of video info with paths
            scripts: Corresponding scripts
            brand_guidelines: Brand guidelines
        
        Returns:
            List of editing results
        """
        
        results = []
        
        for i, (video, script) in enumerate(zip(videos, scripts)):
            video_path = video.get('video_url') or video.get('path')
            
            if not video_path:
                results.append({
                    "status": "failed",
                    "error": "No video path provided",
                    "index": i
                })
                continue
            
            try:
                logger.info(f"Editing video {i+1}/{len(videos)}")
                result = await self.auto_edit(
                    video_path=video_path,
                    script=script,
                    brand_guidelines=brand_guidelines,
                    output_name=f"video_{i+1}"
                )
                result['index'] = i
                results.append(result)
                
            except Exception as e:
                logger.error(f"Failed to edit video {i}: {e}")
                results.append({
                    "status": "failed",
                    "error": str(e),
                    "index": i
                })
        
        return results
