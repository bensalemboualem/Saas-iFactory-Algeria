"""
Text-to-Video Engine using Stable Diffusion Video
Professional video generation from text prompts
"""
import os
import logging
from pathlib import Path
from typing import Optional, Dict, List
import torch
from diffusers import StableVideoDiffusionPipeline, DiffusionPipeline
from diffusers.utils import export_to_video
from PIL import Image
import numpy as np

logger = logging.getLogger(__name__)

class TextToVideoEngine:
    """
    Professional Text-to-Video generation using Stable Diffusion

    Models supported:
    - Stable Video Diffusion (SVD)
    - AnimateDiff
    - Zeroscope
    """

    def __init__(
        self,
        model_id: str = "stabilityai/stable-video-diffusion-img2vid-xt",
        device: str = "cuda" if torch.cuda.is_available() else "cpu",
        enable_cpu_offload: bool = True
    ):
        self.model_id = model_id
        self.device = device
        self.enable_cpu_offload = enable_cpu_offload
        self.pipeline = None

        logger.info(f"Initializing TextToVideoEngine with {model_id} on {device}")

    def load_model(self):
        """Load the Stable Video Diffusion model"""
        if self.pipeline is not None:
            return

        try:
            logger.info(f"Loading model {self.model_id}...")

            # For Stable Video Diffusion (image-to-video)
            if "stable-video-diffusion" in self.model_id:
                self.pipeline = StableVideoDiffusionPipeline.from_pretrained(
                    self.model_id,
                    torch_dtype=torch.float16,
                    variant="fp16"
                )
            else:
                # For other text-to-video models
                self.pipeline = DiffusionPipeline.from_pretrained(
                    self.model_id,
                    torch_dtype=torch.float16
                )

            if self.enable_cpu_offload:
                self.pipeline.enable_model_cpu_offload()
            else:
                self.pipeline = self.pipeline.to(self.device)

            logger.info("Model loaded successfully")

        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise

    def generate_initial_frame(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        width: int = 1024,
        height: int = 576
    ) -> Image.Image:
        """
        Generate initial frame from text prompt
        (Used for SVD which requires an initial image)
        """
        try:
            from diffusers import StableDiffusionPipeline

            # Use Stable Diffusion XL for high-quality initial frame
            sd_pipeline = StableDiffusionPipeline.from_pretrained(
                "stabilityai/stable-diffusion-xl-base-1.0",
                torch_dtype=torch.float16
            )

            if self.enable_cpu_offload:
                sd_pipeline.enable_model_cpu_offload()
            else:
                sd_pipeline = sd_pipeline.to(self.device)

            logger.info(f"Generating initial frame: {prompt[:50]}...")

            image = sd_pipeline(
                prompt=prompt,
                negative_prompt=negative_prompt or "blurry, low quality, distorted",
                num_inference_steps=30,
                guidance_scale=7.5,
                width=width,
                height=height
            ).images[0]

            # Clean up
            del sd_pipeline
            torch.cuda.empty_cache()

            return image

        except Exception as e:
            logger.error(f"Failed to generate initial frame: {str(e)}")
            raise

    def generate_video_from_image(
        self,
        image: Image.Image,
        prompt: Optional[str] = None,
        num_frames: int = 25,
        fps: int = 8,
        motion_bucket_id: int = 127,
        noise_aug_strength: float = 0.02
    ) -> List[Image.Image]:
        """
        Generate video from initial image using SVD

        Args:
            image: Initial frame
            prompt: Optional conditioning text
            num_frames: Number of frames to generate
            fps: Frames per second
            motion_bucket_id: Motion intensity (0-255)
            noise_aug_strength: Noise augmentation strength
        """
        try:
            self.load_model()

            logger.info(f"Generating {num_frames} frames at {fps} fps...")

            frames = self.pipeline(
                image=image,
                num_frames=num_frames,
                decode_chunk_size=8,
                motion_bucket_id=motion_bucket_id,
                noise_aug_strength=noise_aug_strength,
                num_inference_steps=25
            ).frames[0]

            return frames

        except Exception as e:
            logger.error(f"Failed to generate video: {str(e)}")
            raise

    def generate_video(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        duration_seconds: float = 3.0,
        fps: int = 8,
        width: int = 1024,
        height: int = 576,
        output_path: Optional[Path] = None
    ) -> Path:
        """
        Complete text-to-video pipeline

        Args:
            prompt: Text description of the video
            negative_prompt: What to avoid in generation
            duration_seconds: Video duration
            fps: Frames per second
            width: Video width
            height: Video height
            output_path: Where to save the video

        Returns:
            Path to generated video file
        """
        try:
            # Calculate number of frames
            num_frames = int(duration_seconds * fps)

            logger.info(f"Starting video generation: {prompt[:50]}...")
            logger.info(f"Duration: {duration_seconds}s, FPS: {fps}, Frames: {num_frames}")

            # Step 1: Generate initial frame
            logger.info("Step 1/3: Generating initial frame...")
            initial_frame = self.generate_initial_frame(
                prompt=prompt,
                negative_prompt=negative_prompt,
                width=width,
                height=height
            )

            # Step 2: Generate video frames
            logger.info("Step 2/3: Generating video frames...")
            frames = self.generate_video_from_image(
                image=initial_frame,
                num_frames=num_frames,
                fps=fps
            )

            # Step 3: Export to video file
            logger.info("Step 3/3: Exporting video...")
            if output_path is None:
                output_path = Path("/tmp") / f"video_{os.urandom(8).hex()}.mp4"

            export_to_video(frames, str(output_path), fps=fps)

            logger.info(f"Video generated successfully: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Video generation failed: {str(e)}")
            raise

    def generate_scene_video(
        self,
        scene: Dict,
        aspect_ratio: str = "16:9",
        fps: int = 8
    ) -> Path:
        """
        Generate video for a specific scene with Algerian context

        Args:
            scene: Scene dictionary with prompt, duration, etc.
            aspect_ratio: Video aspect ratio (16:9, 9:16, 1:1)
            fps: Frames per second
        """
        # Determine dimensions based on aspect ratio
        dimensions = {
            "16:9": (1024, 576),
            "9:16": (576, 1024),
            "1:1": (768, 768)
        }
        width, height = dimensions.get(aspect_ratio, (1024, 576))

        # Enhanced prompt with cinematic quality
        enhanced_prompt = f"{scene['prompt']}, cinematic lighting, professional cinematography, high quality, 4k, detailed"

        # Negative prompt for Algerian content
        negative_prompt = "blurry, low quality, distorted, text, watermark, cartoon, anime, western style"

        return self.generate_video(
            prompt=enhanced_prompt,
            negative_prompt=negative_prompt,
            duration_seconds=scene.get('duration', 3.0),
            fps=fps,
            width=width,
            height=height
        )


class ZeroscopeEngine:
    """
    Alternative: Zeroscope V2 (faster but lower quality)
    Good for rapid prototyping
    """

    def __init__(self, device: str = "cuda" if torch.cuda.is_available() else "cpu"):
        self.device = device
        self.pipeline = None

    def load_model(self):
        """Load Zeroscope model"""
        if self.pipeline is not None:
            return

        try:
            logger.info("Loading Zeroscope V2 XL model...")

            self.pipeline = DiffusionPipeline.from_pretrained(
                "cerspense/zeroscope_v2_XL",
                torch_dtype=torch.float16
            )
            self.pipeline.enable_model_cpu_offload()

            logger.info("Zeroscope model loaded")

        except Exception as e:
            logger.error(f"Failed to load Zeroscope: {str(e)}")
            raise

    def generate_video(
        self,
        prompt: str,
        num_frames: int = 24,
        fps: int = 8,
        output_path: Optional[Path] = None
    ) -> Path:
        """Generate video with Zeroscope (faster)"""
        try:
            self.load_model()

            logger.info(f"Generating video with Zeroscope: {prompt[:50]}...")

            video_frames = self.pipeline(
                prompt=prompt,
                num_frames=num_frames,
                num_inference_steps=30
            ).frames[0]

            if output_path is None:
                output_path = Path("/tmp") / f"video_{os.urandom(8).hex()}.mp4"

            export_to_video(video_frames, str(output_path), fps=fps)

            logger.info(f"Video generated: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Zeroscope generation failed: {str(e)}")
            raise


# Factory function
def get_video_engine(engine_type: str = "svd", **kwargs):
    """
    Get video generation engine

    Args:
        engine_type: "svd" (Stable Video Diffusion) or "zeroscope"
        **kwargs: Engine-specific parameters
    """
    if engine_type == "svd":
        return TextToVideoEngine(**kwargs)
    elif engine_type == "zeroscope":
        return ZeroscopeEngine(**kwargs)
    else:
        raise ValueError(f"Unknown engine type: {engine_type}")
