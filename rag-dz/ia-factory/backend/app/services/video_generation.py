"""
IA Factory - Video Generation Service
Phase 2: AI Video Generation using VEO 3 / Replicate
"""

import aiohttp
import asyncio
import logging
from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime

from ..config import settings

logger = logging.getLogger(__name__)


class VideoFormat(str, Enum):
    """Video format types"""
    REELS = "9:16"
    LANDSCAPE = "16:9"
    SQUARE = "1:1"


class VideoQuality(str, Enum):
    """Video quality presets"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    ULTRA = "ultra"


class VideoGenerator:
    """
    Phase 2: Video Generation using AI
    
    Supports multiple backends:
    - VEO 3 (Google's video generation)
    - Replicate (various models like minimax/video-01)
    """
    
    def __init__(self):
        self.veo3_api_key = settings.veo3_api_key
        self.veo3_base_url = settings.veo3_base_url
        self.replicate_token = settings.replicate_api_token
        self.replicate_base_url = "https://api.replicate.com/v1"
    
    async def generate_video(
        self,
        script: Dict[str, Any],
        brand_guidelines: Dict[str, Any],
        format: VideoFormat = VideoFormat.REELS,
        quality: VideoQuality = VideoQuality.HIGH,
        backend: str = "replicate"
    ) -> Dict[str, Any]:
        """
        Generate video from script using AI
        
        Args:
            script: Script with hook, body, CTA, and suggestions
            brand_guidelines: Brand visual and voice guidelines
            format: Video aspect ratio
            quality: Output quality
            backend: AI backend to use (veo3, replicate)
        
        Returns:
            Dictionary with video URL and metadata
        """
        
        prompt = self._build_video_prompt(script, brand_guidelines)
        
        if backend == "veo3" and self.veo3_api_key:
            return await self._generate_with_veo3(prompt, format, quality)
        elif backend == "replicate" or self.replicate_token:
            return await self._generate_with_replicate(prompt, format, quality)
        else:
            raise ValueError("No video generation backend configured")
    
    def _build_video_prompt(
        self,
        script: Dict[str, Any],
        brand_guidelines: Dict[str, Any]
    ) -> str:
        """
        Convert script to video generation prompt
        
        Creates a detailed prompt for AI video generation based on
        the script content and brand guidelines.
        """
        
        hook = script.get('hook', '')
        body = script.get('body', '')
        cta = script.get('cta', '')
        visuals = script.get('suggested_visuals', [])
        mood = script.get('suggested_music_mood', 'upbeat')
        
        visual_style = brand_guidelines.get('visual_guidelines', {}).get('visual_style', 'modern, professional')
        brand_name = brand_guidelines.get('brand_name', 'IA Factory')
        
        prompt = f"""
Create a professional {mood} video reel for {brand_name}:

STRUCTURE:
[0-2 seconds - HOOK]
{hook}
Visual: Eye-catching opening, pattern interrupt, dynamic movement

[2-12 seconds - MAIN CONTENT]
{body}
Visuals: {', '.join(visuals) if visuals else 'Professional b-roll, screen recordings, talking head'}

[12-15 seconds - CTA]
{cta}
Visual: Clear call-to-action text overlay, brand colors

STYLE GUIDELINES:
- Visual Style: {visual_style}
- Mood: {mood}
- Pace: Fast-paced, attention-grabbing
- Text: Bold, readable overlays
- Transitions: Smooth, modern cuts

TECHNICAL:
- Vertical format (9:16)
- High contrast
- Vibrant colors
- Professional lighting
"""
        return prompt.strip()
    
    async def _generate_with_veo3(
        self,
        prompt: str,
        format: VideoFormat,
        quality: VideoQuality
    ) -> Dict[str, Any]:
        """Generate video using VEO 3 API"""
        
        async with aiohttp.ClientSession() as session:
            payload = {
                "prompt": prompt,
                "duration": 15,
                "aspect_ratio": format.value,
                "quality": quality.value,
                "style": "cinematic"
            }
            
            headers = {
                "Authorization": f"Bearer {self.veo3_api_key}",
                "Content-Type": "application/json"
            }
            
            # Start generation
            async with session.post(
                f"{self.veo3_base_url}/generate",
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=60)
            ) as response:
                if response.status != 200:
                    error = await response.text()
                    raise Exception(f"VEO 3 API error: {response.status} - {error}")
                
                data = await response.json()
                job_id = data.get('job_id')
            
            # Poll for completion
            video_url = await self._poll_veo3_status(session, job_id, headers)
            
            return {
                "status": "completed",
                "video_url": video_url,
                "backend": "veo3",
                "format": format.value,
                "quality": quality.value,
                "generated_at": datetime.now().isoformat()
            }
    
    async def _poll_veo3_status(
        self,
        session: aiohttp.ClientSession,
        job_id: str,
        headers: Dict[str, str],
        max_attempts: int = 60,
        interval: int = 10
    ) -> str:
        """Poll VEO 3 for job completion"""
        
        for attempt in range(max_attempts):
            async with session.get(
                f"{self.veo3_base_url}/status/{job_id}",
                headers=headers
            ) as response:
                data = await response.json()
                status = data.get('status')
                
                if status == 'completed':
                    return data.get('video_url')
                elif status == 'failed':
                    raise Exception(f"VEO 3 generation failed: {data.get('error')}")
                
                logger.info(f"VEO 3 job {job_id}: {status} (attempt {attempt + 1}/{max_attempts})")
                await asyncio.sleep(interval)
        
        raise TimeoutError(f"VEO 3 job {job_id} timed out")
    
    async def _generate_with_replicate(
        self,
        prompt: str,
        format: VideoFormat,
        quality: VideoQuality
    ) -> Dict[str, Any]:
        """Generate video using Replicate API (minimax/video-01)"""
        
        async with aiohttp.ClientSession() as session:
            # Use minimax/video-01 model
            payload = {
                "version": "minimax/video-01",
                "input": {
                    "prompt": prompt,
                    "prompt_optimizer": True
                }
            }
            
            headers = {
                "Authorization": f"Bearer {self.replicate_token}",
                "Content-Type": "application/json",
                "Prefer": "wait"  # Wait for result
            }
            
            async with session.post(
                f"{self.replicate_base_url}/predictions",
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=600)  # 10 min timeout
            ) as response:
                if response.status not in [200, 201]:
                    error = await response.text()
                    raise Exception(f"Replicate API error: {response.status} - {error}")
                
                data = await response.json()
                
                # If using "wait" header, output should be ready
                if data.get('status') == 'succeeded':
                    output = data.get('output')
                    video_url = output if isinstance(output, str) else output[0] if output else None
                    
                    return {
                        "status": "completed",
                        "video_url": video_url,
                        "backend": "replicate",
                        "model": "minimax/video-01",
                        "format": format.value,
                        "quality": quality.value,
                        "prediction_id": data.get('id'),
                        "generated_at": datetime.now().isoformat()
                    }
                else:
                    # Need to poll
                    prediction_id = data.get('id')
                    return await self._poll_replicate_status(session, prediction_id, headers)
    
    async def _poll_replicate_status(
        self,
        session: aiohttp.ClientSession,
        prediction_id: str,
        headers: Dict[str, str],
        max_attempts: int = 60,
        interval: int = 10
    ) -> Dict[str, Any]:
        """Poll Replicate for prediction completion"""
        
        for attempt in range(max_attempts):
            async with session.get(
                f"{self.replicate_base_url}/predictions/{prediction_id}",
                headers=headers
            ) as response:
                data = await response.json()
                status = data.get('status')
                
                if status == 'succeeded':
                    output = data.get('output')
                    video_url = output if isinstance(output, str) else output[0] if output else None
                    
                    return {
                        "status": "completed",
                        "video_url": video_url,
                        "backend": "replicate",
                        "prediction_id": prediction_id,
                        "generated_at": datetime.now().isoformat()
                    }
                elif status == 'failed':
                    raise Exception(f"Replicate generation failed: {data.get('error')}")
                
                logger.info(f"Replicate prediction {prediction_id}: {status} (attempt {attempt + 1}/{max_attempts})")
                await asyncio.sleep(interval)
        
        raise TimeoutError(f"Replicate prediction {prediction_id} timed out")
    
    async def generate_bulk_videos(
        self,
        scripts: List[Dict[str, Any]],
        brand_guidelines: Dict[str, Any],
        batch_size: int = 2,
        backend: str = "replicate"
    ) -> List[Dict[str, Any]]:
        """
        Phase 2: Generate multiple videos in batches
        
        Args:
            scripts: List of scripts to generate videos for
            brand_guidelines: Brand guidelines
            batch_size: Number of videos to generate in parallel
            backend: AI backend to use
        
        Returns:
            List of video generation results
        """
        
        logger.info(f"🎬 Starting bulk video generation: {len(scripts)} videos")
        
        all_results = []
        
        for i in range(0, len(scripts), batch_size):
            batch = scripts[i:i+batch_size]
            batch_num = i // batch_size + 1
            total_batches = (len(scripts) - 1) // batch_size + 1
            
            logger.info(f"Batch {batch_num}/{total_batches}: Generating {len(batch)} videos...")
            
            # Generate batch (sequentially for rate limits)
            for script in batch:
                try:
                    result = await self.generate_video(
                        script=script,
                        brand_guidelines=brand_guidelines,
                        backend=backend
                    )
                    result['script_topic'] = script.get('topic', '')
                    all_results.append(result)
                except Exception as e:
                    logger.error(f"Video generation failed: {e}")
                    all_results.append({
                        "status": "failed",
                        "error": str(e),
                        "script_topic": script.get('topic', '')
                    })
                
                # Rate limiting between videos
                await asyncio.sleep(5)
            
            # Longer delay between batches
            if i + batch_size < len(scripts):
                logger.info("Waiting between batches...")
                await asyncio.sleep(30)
        
        successful = len([r for r in all_results if r.get('status') == 'completed'])
        logger.info(f"✅ Generated {successful}/{len(scripts)} videos successfully")
        
        return all_results
    
    async def get_generation_status(
        self,
        job_id: str,
        backend: str = "replicate"
    ) -> Dict[str, Any]:
        """Check status of a video generation job"""
        
        if backend == "replicate":
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.replicate_token}",
                }
                
                async with session.get(
                    f"{self.replicate_base_url}/predictions/{job_id}",
                    headers=headers
                ) as response:
                    return await response.json()
        
        # Add other backends as needed
        raise ValueError(f"Unknown backend: {backend}")
