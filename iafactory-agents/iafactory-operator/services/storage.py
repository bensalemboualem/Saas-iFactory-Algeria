"""
IA Factory Operator - Storage Client
S3-compatible storage for video files
"""

import os
import tempfile
import mimetypes
from typing import Optional, BinaryIO
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse

import structlog
import httpx

from core.config import settings

logger = structlog.get_logger(__name__)


class StorageClient:
    """
    S3-compatible storage client for:
    - Downloading source videos
    - Uploading rendered outputs
    - Managing thumbnails
    """
    
    def __init__(
        self,
        endpoint: Optional[str] = None,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        bucket: Optional[str] = None,
        region: Optional[str] = None,
    ):
        self.endpoint = endpoint or settings.s3_endpoint_url
        self.access_key = access_key or settings.s3_access_key
        self.secret_key = secret_key or settings.s3_secret_key
        self.bucket = bucket or settings.s3_bucket
        self.region = region or settings.s3_region
        
        self._s3_client = None
    
    @property
    def s3_client(self):
        """Lazy-load S3 client"""
        if self._s3_client is None and self.access_key:
            import boto3
            from botocore.config import Config
            
            config = Config(
                signature_version='s3v4',
                s3={'addressing_style': 'path'},
            )
            
            self._s3_client = boto3.client(
                's3',
                endpoint_url=self.endpoint,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                region_name=self.region,
                config=config,
            )
        return self._s3_client
    
    async def download_video(
        self,
        url: str,
        work_dir: Optional[str] = None,
    ) -> str:
        """
        Download video from URL to local file.
        Supports: HTTP(S), S3 URLs
        """
        parsed = urlparse(url)
        
        # Determine output path
        if work_dir is None:
            work_dir = tempfile.mkdtemp(prefix="iafactory_")
        
        # Get filename from URL
        filename = os.path.basename(parsed.path) or "source_video.mp4"
        local_path = os.path.join(work_dir, filename)
        
        logger.info(f"Downloading video: {url} -> {local_path}")
        
        if parsed.scheme == "s3":
            # S3 URL
            bucket = parsed.netloc
            key = parsed.path.lstrip("/")
            await self._download_from_s3(bucket, key, local_path)
        else:
            # HTTP(S) URL
            await self._download_from_http(url, local_path)
        
        return local_path
    
    async def _download_from_http(self, url: str, local_path: str):
        """Download file via HTTP"""
        async with httpx.AsyncClient(timeout=300.0) as client:
            async with client.stream("GET", url) as response:
                response.raise_for_status()
                
                with open(local_path, "wb") as f:
                    async for chunk in response.aiter_bytes(chunk_size=8192):
                        f.write(chunk)
        
        logger.info(f"Downloaded {os.path.getsize(local_path)} bytes")
    
    async def _download_from_s3(self, bucket: str, key: str, local_path: str):
        """Download file from S3"""
        if not self.s3_client:
            raise RuntimeError("S3 client not configured")
        
        self.s3_client.download_file(bucket, key, local_path)
        logger.info(f"Downloaded from S3: s3://{bucket}/{key}")
    
    async def upload_video(
        self,
        local_path: str,
        key: Optional[str] = None,
        content_type: Optional[str] = None,
    ) -> str:
        """
        Upload video to S3 storage.
        Returns public URL.
        """
        if not self.s3_client:
            raise RuntimeError("S3 client not configured")
        
        # Generate key if not provided
        if key is None:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = os.path.basename(local_path)
            key = f"outputs/{timestamp}_{filename}"
        
        # Detect content type
        if content_type is None:
            content_type, _ = mimetypes.guess_type(local_path)
            content_type = content_type or "video/mp4"
        
        logger.info(f"Uploading to S3: {local_path} -> s3://{self.bucket}/{key}")
        
        # Upload with public-read ACL
        self.s3_client.upload_file(
            local_path,
            self.bucket,
            key,
            ExtraArgs={
                "ContentType": content_type,
                "ACL": "public-read",
            }
        )
        
        # Generate public URL
        if self.endpoint:
            url = f"{self.endpoint}/{self.bucket}/{key}"
        else:
            url = f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{key}"
        
        logger.info(f"Uploaded: {url}")
        return url
    
    async def upload_thumbnail(
        self,
        local_path: str,
        key: Optional[str] = None,
    ) -> str:
        """Upload thumbnail image to S3"""
        if key is None:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = os.path.basename(local_path)
            key = f"thumbnails/{timestamp}_{filename}"
        
        return await self.upload_video(
            local_path,
            key=key,
            content_type="image/jpeg",
        )
    
    async def delete_file(self, key: str):
        """Delete file from S3"""
        if not self.s3_client:
            return
        
        try:
            self.s3_client.delete_object(Bucket=self.bucket, Key=key)
            logger.info(f"Deleted from S3: {key}")
        except Exception as e:
            logger.warning(f"Failed to delete S3 object: {e}")
    
    async def get_presigned_url(
        self,
        key: str,
        expires_in: int = 3600,
    ) -> str:
        """Generate presigned URL for private file"""
        if not self.s3_client:
            raise RuntimeError("S3 client not configured")
        
        url = self.s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': self.bucket, 'Key': key},
            ExpiresIn=expires_in,
        )
        return url


# =============================================================================
# SINGLETON
# =============================================================================

_storage_client: Optional[StorageClient] = None


def get_storage_client() -> StorageClient:
    """Get or create storage client singleton"""
    global _storage_client
    if _storage_client is None:
        _storage_client = StorageClient()
    return _storage_client
