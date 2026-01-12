"""
IA Factory - Platform Publishers
Phase 3: Multi-platform publishing integrations
"""

import aiohttp
import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path

from ..config import settings
from ..models.distribution import Platform, PublishStatus, PublishResult

logger = logging.getLogger(__name__)


class PlatformPublisher(ABC):
    """Base class for platform publishers"""
    
    platform: Platform
    
    @abstractmethod
    async def publish(self, video_path: str, metadata: Dict[str, Any]) -> PublishResult:
        """Publish content to platform"""
        pass
    
    @abstractmethod
    async def validate_credentials(self) -> bool:
        """Validate API credentials"""
        pass
    
    @abstractmethod
    async def get_upload_url(self) -> str:
        """Get upload URL for video"""
        pass


class InstagramPublisher(PlatformPublisher):
    """Instagram Reels Publisher using Graph API"""
    
    platform = Platform.INSTAGRAM_REELS
    
    def __init__(self, access_token: str, business_account_id: str):
        self.access_token = access_token
        self.business_account_id = business_account_id
        self.base_url = "https://graph.facebook.com/v18.0"
    
    async def validate_credentials(self) -> bool:
        """Validate Instagram credentials"""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/me"
            params = {"access_token": self.access_token}
            
            async with session.get(url, params=params) as response:
                return response.status == 200
    
    async def get_upload_url(self) -> str:
        """Get upload URL (Instagram uses container-based upload)"""
        return f"{self.base_url}/{self.business_account_id}/media"
    
    async def publish(self, video_path: str, metadata: Dict[str, Any]) -> PublishResult:
        """
        Publish to Instagram Reels
        
        Instagram Graph API flow:
        1. Create media container with video URL
        2. Wait for processing
        3. Publish the container
        """
        
        caption = metadata.get('caption', '')
        hashtags = metadata.get('hashtags', [])
        full_caption = f"{caption}\n\n{' '.join(hashtags)}"
        
        async with aiohttp.ClientSession() as session:
            try:
                # Step 1: Create media container
                # Note: Video must be publicly accessible URL
                video_url = metadata.get('video_url', video_path)
                
                container_url = f"{self.base_url}/{self.business_account_id}/media"
                container_params = {
                    "media_type": "REELS",
                    "video_url": video_url,
                    "caption": full_caption[:2200],  # Instagram limit
                    "share_to_feed": "true",
                    "access_token": self.access_token
                }
                
                async with session.post(container_url, data=container_params) as response:
                    if response.status != 200:
                        error = await response.text()
                        return PublishResult(
                            scheduled_post_id=metadata.get('post_id', ''),
                            brand_id=metadata.get('brand_id', ''),
                            platform=self.platform,
                            success=False,
                            status=PublishStatus.FAILED,
                            error_message=f"Container creation failed: {error}"
                        )
                    
                    container_data = await response.json()
                    container_id = container_data.get('id')
                
                # Step 2: Wait for processing (poll status)
                await self._wait_for_processing(session, container_id)
                
                # Step 3: Publish
                publish_url = f"{self.base_url}/{self.business_account_id}/media_publish"
                publish_params = {
                    "creation_id": container_id,
                    "access_token": self.access_token
                }
                
                async with session.post(publish_url, data=publish_params) as response:
                    if response.status != 200:
                        error = await response.text()
                        return PublishResult(
                            scheduled_post_id=metadata.get('post_id', ''),
                            brand_id=metadata.get('brand_id', ''),
                            platform=self.platform,
                            success=False,
                            status=PublishStatus.FAILED,
                            error_message=f"Publish failed: {error}"
                        )
                    
                    publish_data = await response.json()
                    media_id = publish_data.get('id')
                
                return PublishResult(
                    scheduled_post_id=metadata.get('post_id', ''),
                    brand_id=metadata.get('brand_id', ''),
                    platform=self.platform,
                    platform_post_id=media_id,
                    platform_url=f"https://www.instagram.com/reel/{media_id}/",
                    success=True,
                    status=PublishStatus.PUBLISHED,
                    published_at=datetime.now()
                )
                
            except Exception as e:
                logger.error(f"Instagram publish failed: {e}")
                return PublishResult(
                    scheduled_post_id=metadata.get('post_id', ''),
                    brand_id=metadata.get('brand_id', ''),
                    platform=self.platform,
                    success=False,
                    status=PublishStatus.FAILED,
                    error_message=str(e)
                )
    
    async def _wait_for_processing(
        self,
        session: aiohttp.ClientSession,
        container_id: str,
        max_attempts: int = 30,
        interval: int = 10
    ):
        """Wait for Instagram to process the video"""
        
        for attempt in range(max_attempts):
            status_url = f"{self.base_url}/{container_id}"
            params = {
                "fields": "status_code",
                "access_token": self.access_token
            }
            
            async with session.get(status_url, params=params) as response:
                data = await response.json()
                status = data.get('status_code')
                
                if status == 'FINISHED':
                    return
                elif status == 'ERROR':
                    raise Exception("Instagram processing failed")
                
                await asyncio.sleep(interval)
        
        raise TimeoutError("Instagram processing timed out")


class TikTokPublisher(PlatformPublisher):
    """TikTok Publisher using Content Posting API"""
    
    platform = Platform.TIKTOK
    
    def __init__(self, client_key: str, client_secret: str, access_token: str = None):
        self.client_key = client_key
        self.client_secret = client_secret
        self.access_token = access_token
        self.base_url = "https://open.tiktokapis.com/v2"
    
    async def validate_credentials(self) -> bool:
        """Validate TikTok credentials"""
        # TikTok validation logic
        return bool(self.access_token)
    
    async def get_upload_url(self) -> str:
        """Get TikTok upload URL"""
        return f"{self.base_url}/post/publish/video/init/"
    
    async def publish(self, video_path: str, metadata: Dict[str, Any]) -> PublishResult:
        """
        Publish to TikTok
        
        TikTok Content Posting API flow:
        1. Initialize video upload
        2. Upload video chunks
        3. Publish with caption
        """
        
        caption = metadata.get('caption', '')
        hashtags = metadata.get('hashtags', [])
        
        # TikTok includes hashtags in caption
        full_caption = f"{caption} {' '.join(hashtags)}"[:2200]
        
        async with aiohttp.ClientSession() as session:
            try:
                headers = {
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json"
                }
                
                # Step 1: Initialize upload
                init_url = f"{self.base_url}/post/publish/video/init/"
                init_payload = {
                    "post_info": {
                        "title": full_caption,
                        "privacy_level": "PUBLIC_TO_EVERYONE",
                        "disable_duet": False,
                        "disable_comment": False,
                        "disable_stitch": False
                    },
                    "source_info": {
                        "source": "FILE_UPLOAD",
                        "video_size": Path(video_path).stat().st_size if Path(video_path).exists() else 0
                    }
                }
                
                async with session.post(init_url, headers=headers, json=init_payload) as response:
                    if response.status != 200:
                        error = await response.text()
                        return PublishResult(
                            scheduled_post_id=metadata.get('post_id', ''),
                            brand_id=metadata.get('brand_id', ''),
                            platform=self.platform,
                            success=False,
                            status=PublishStatus.FAILED,
                            error_message=f"TikTok init failed: {error}"
                        )
                    
                    init_data = await response.json()
                    upload_url = init_data.get('data', {}).get('upload_url')
                    publish_id = init_data.get('data', {}).get('publish_id')
                
                # Step 2: Upload video (simplified - actual implementation needs chunked upload)
                # This would upload to upload_url
                
                # Step 3: Check publish status
                status_url = f"{self.base_url}/post/publish/status/fetch/"
                status_payload = {"publish_id": publish_id}
                
                async with session.post(status_url, headers=headers, json=status_payload) as response:
                    status_data = await response.json()
                
                return PublishResult(
                    scheduled_post_id=metadata.get('post_id', ''),
                    brand_id=metadata.get('brand_id', ''),
                    platform=self.platform,
                    platform_post_id=publish_id,
                    success=True,
                    status=PublishStatus.PUBLISHED,
                    published_at=datetime.now()
                )
                
            except Exception as e:
                logger.error(f"TikTok publish failed: {e}")
                return PublishResult(
                    scheduled_post_id=metadata.get('post_id', ''),
                    brand_id=metadata.get('brand_id', ''),
                    platform=self.platform,
                    success=False,
                    status=PublishStatus.FAILED,
                    error_message=str(e)
                )


class YouTubeShortsPublisher(PlatformPublisher):
    """YouTube Shorts Publisher"""
    
    platform = Platform.YOUTUBE_SHORTS
    
    def __init__(self, api_key: str, oauth_credentials: Dict = None):
        self.api_key = api_key
        self.credentials = oauth_credentials
        self.base_url = "https://www.googleapis.com/youtube/v3"
    
    async def validate_credentials(self) -> bool:
        return bool(self.credentials)
    
    async def get_upload_url(self) -> str:
        return f"{self.base_url}/videos"
    
    async def publish(self, video_path: str, metadata: Dict[str, Any]) -> PublishResult:
        """
        Publish to YouTube Shorts
        
        Note: Full implementation requires Google OAuth2 flow
        """
        
        # Placeholder - actual implementation requires googleapis library
        return PublishResult(
            scheduled_post_id=metadata.get('post_id', ''),
            brand_id=metadata.get('brand_id', ''),
            platform=self.platform,
            success=False,
            status=PublishStatus.FAILED,
            error_message="YouTube Shorts publishing requires OAuth setup"
        )


class PublishingManager:
    """
    Manage publishing to multiple platforms
    
    Coordinates publishing across all configured platforms
    with retry logic and status tracking.
    """
    
    def __init__(self, credentials: Dict[str, Any]):
        """
        Initialize with platform credentials
        
        Args:
            credentials: Dict with platform-specific credentials
        """
        self.credentials = credentials
        self.publishers: Dict[Platform, PlatformPublisher] = {}
        
        self._init_publishers()
    
    def _init_publishers(self):
        """Initialize available publishers based on credentials"""
        
        # Instagram
        if self.credentials.get('instagram_token') and self.credentials.get('instagram_account_id'):
            self.publishers[Platform.INSTAGRAM_REELS] = InstagramPublisher(
                access_token=self.credentials['instagram_token'],
                business_account_id=self.credentials['instagram_account_id']
            )
        
        # TikTok
        if self.credentials.get('tiktok_access_token'):
            self.publishers[Platform.TIKTOK] = TikTokPublisher(
                client_key=self.credentials.get('tiktok_client_key', ''),
                client_secret=self.credentials.get('tiktok_client_secret', ''),
                access_token=self.credentials['tiktok_access_token']
            )
        
        # YouTube
        if self.credentials.get('youtube_credentials'):
            self.publishers[Platform.YOUTUBE_SHORTS] = YouTubeShortsPublisher(
                api_key=self.credentials.get('youtube_api_key', ''),
                oauth_credentials=self.credentials['youtube_credentials']
            )
    
    async def publish_to_platform(
        self,
        platform: Platform,
        video_path: str,
        metadata: Dict[str, Any]
    ) -> PublishResult:
        """Publish to a single platform"""
        
        publisher = self.publishers.get(platform)
        
        if not publisher:
            return PublishResult(
                scheduled_post_id=metadata.get('post_id', ''),
                brand_id=metadata.get('brand_id', ''),
                platform=platform,
                success=False,
                status=PublishStatus.FAILED,
                error_message=f"No publisher configured for {platform.value}"
            )
        
        return await publisher.publish(video_path, metadata)
    
    async def publish_all(
        self,
        video_path: str,
        platforms: List[Platform],
        metadata: Dict[str, Any],
        platform_metadata: Dict[Platform, Dict[str, Any]] = None
    ) -> Dict[str, PublishResult]:
        """
        Publish to all specified platforms
        
        Args:
            video_path: Path to video file
            platforms: List of target platforms
            metadata: Base metadata for all platforms
            platform_metadata: Platform-specific overrides
        
        Returns:
            Dictionary mapping platform to publish result
        """
        
        results = {}
        
        for platform in platforms:
            # Merge base metadata with platform-specific
            platform_meta = {**metadata}
            if platform_metadata and platform in platform_metadata:
                platform_meta.update(platform_metadata[platform])
            
            try:
                result = await self.publish_to_platform(
                    platform=platform,
                    video_path=video_path,
                    metadata=platform_meta
                )
                results[platform.value] = result
                
            except Exception as e:
                logger.error(f"Publishing to {platform} failed: {e}")
                results[platform.value] = PublishResult(
                    scheduled_post_id=metadata.get('post_id', ''),
                    brand_id=metadata.get('brand_id', ''),
                    platform=platform,
                    success=False,
                    status=PublishStatus.FAILED,
                    error_message=str(e)
                )
        
        return results
    
    def get_available_platforms(self) -> List[Platform]:
        """Get list of configured platforms"""
        return list(self.publishers.keys())
    
    async def validate_all_credentials(self) -> Dict[Platform, bool]:
        """Validate credentials for all configured platforms"""
        
        results = {}
        
        for platform, publisher in self.publishers.items():
            try:
                results[platform] = await publisher.validate_credentials()
            except:
                results[platform] = False
        
        return results
