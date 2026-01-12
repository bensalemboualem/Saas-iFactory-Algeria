"""
Background Removal Service
Uses rembg (open-source, free) for background removal
"""
import logging
import io
from typing import Optional, Tuple
from PIL import Image
import numpy as np

logger = logging.getLogger(__name__)


class BackgroundRemovalService:
    """Background removal using rembg"""
    
    def __init__(self):
        """Initialize rembg session"""
        try:
            from rembg import remove, new_session
            self.remove = remove
            # Use u2net model (best quality)
            self.session = new_session("u2net")
            logger.info("rembg initialized successfully")
        except ImportError:
            logger.error("rembg not installed. Run: pip install rembg[gpu]")
            raise
    
    async def remove_background(
        self,
        input_image: bytes,
        return_mask: bool = False,
        alpha_matting: bool = True
    ) -> Tuple[bytes, Optional[bytes]]:
        """
        Remove background from image
        
        Args:
            input_image: Input image bytes
            return_mask: Whether to return the mask
            alpha_matting: Use alpha matting for better edges
            
        Returns:
            Tuple of (processed_image_bytes, mask_bytes or None)
        """
        try:
            # Convert bytes to PIL Image
            input_pil = Image.open(io.BytesIO(input_image))
            
            # Remove background
            output_pil = self.remove(
                input_pil,
                session=self.session,
                alpha_matting=alpha_matting,
                alpha_matting_foreground_threshold=240,
                alpha_matting_background_threshold=10,
                alpha_matting_erode_size=10
            )
            
            # Convert result to bytes
            output_buffer = io.BytesIO()
            output_pil.save(output_buffer, format="PNG")
            output_bytes = output_buffer.getvalue()
            
            # Generate mask if requested
            mask_bytes = None
            if return_mask:
                mask_bytes = self._extract_mask(output_pil)
            
            return output_bytes, mask_bytes
        
        except Exception as e:
            logger.error(f"Background removal error: {str(e)}")
            raise
    
    def _extract_mask(self, image_with_alpha: Image.Image) -> bytes:
        """Extract alpha channel as mask"""
        try:
            # Get alpha channel
            if image_with_alpha.mode == 'RGBA':
                alpha = image_with_alpha.split()[-1]
            else:
                # If no alpha channel, create full white mask
                alpha = Image.new('L', image_with_alpha.size, 255)
            
            # Convert to bytes
            mask_buffer = io.BytesIO()
            alpha.save(mask_buffer, format="PNG")
            return mask_buffer.getvalue()
        
        except Exception as e:
            logger.error(f"Mask extraction error: {str(e)}")
            raise
    
    async def batch_remove_background(
        self,
        images: list[bytes],
        return_masks: bool = False
    ) -> list[Tuple[bytes, Optional[bytes]]]:
        """Batch background removal"""
        import asyncio
        
        tasks = [
            self.remove_background(img, return_mask=return_masks)
            for img in images
        ]
        
        return await asyncio.gather(*tasks)
    
    def get_image_dimensions(self, image_bytes: bytes) -> dict:
        """Get image dimensions"""
        try:
            image = Image.open(io.BytesIO(image_bytes))
            return {
                "width": image.width,
                "height": image.height
            }
        except Exception as e:
            logger.error(f"Error getting image dimensions: {str(e)}")
            raise


# Alternative: remove.bg API (paid but better quality)
class RemoveBgAPIService:
    """
    Alternative service using remove.bg API
    Requires API key: https://www.remove.bg/api
    Free tier: 50 images/month
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://api.remove.bg/v1.0/removebg"
    
    async def remove_background(
        self,
        input_image: bytes,
        size: str = "auto"  # preview, full, auto
    ) -> bytes:
        """Remove background using remove.bg API"""
        import aiohttp
        
        try:
            async with aiohttp.ClientSession() as session:
                data = aiohttp.FormData()
                data.add_field('image_file', input_image, filename='image.jpg')
                data.add_field('size', size)
                
                headers = {'X-Api-Key': self.api_key}
                
                async with session.post(
                    self.api_url,
                    headers=headers,
                    data=data
                ) as response:
                    if response.status == 200:
                        return await response.read()
                    else:
                        error_data = await response.json()
                        raise Exception(f"remove.bg API error: {error_data}")
        
        except Exception as e:
            logger.error(f"remove.bg API error: {str(e)}")
            raise
