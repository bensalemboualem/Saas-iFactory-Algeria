"""
MinIO Storage Service - S3-compatible object storage
"""
from typing import Optional, BinaryIO, Dict, Any, List
from pathlib import Path
import io
import hashlib
from datetime import timedelta
from minio import Minio
from minio.error import S3Error
from app.core.config import settings


class MinIOService:
    """S3-compatible storage service using MinIO"""

    BUCKETS = {
        "assets": "video-platform-assets",
        "videos": "video-platform-videos",
        "exports": "video-platform-exports",
        "temp": "video-platform-temp",
    }

    def __init__(self):
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE,
        )
        self._ensure_buckets()

    def _ensure_buckets(self):
        """Create buckets if they don't exist"""
        for bucket in self.BUCKETS.values():
            try:
                if not self.client.bucket_exists(bucket):
                    self.client.make_bucket(bucket)
            except S3Error as e:
                print(f"Error creating bucket {bucket}: {e}")

    def _get_bucket(self, bucket_type: str) -> str:
        return self.BUCKETS.get(bucket_type, self.BUCKETS["assets"])

    async def upload_file(
        self,
        file_data: bytes | BinaryIO,
        object_name: str,
        bucket_type: str = "assets",
        content_type: str = "application/octet-stream",
        metadata: Dict[str, str] = None,
    ) -> Dict[str, Any]:
        """Upload file to storage"""
        bucket = self._get_bucket(bucket_type)

        if isinstance(file_data, bytes):
            file_data = io.BytesIO(file_data)
            file_data.seek(0, 2)
            length = file_data.tell()
            file_data.seek(0)
        else:
            file_data.seek(0, 2)
            length = file_data.tell()
            file_data.seek(0)

        try:
            result = self.client.put_object(
                bucket,
                object_name,
                file_data,
                length,
                content_type=content_type,
                metadata=metadata or {},
            )

            return {
                "bucket": bucket,
                "object_name": object_name,
                "etag": result.etag,
                "version_id": result.version_id,
                "size": length,
            }
        except S3Error as e:
            raise Exception(f"Upload failed: {e}")

    async def download_file(
        self,
        object_name: str,
        bucket_type: str = "assets",
    ) -> bytes:
        """Download file from storage"""
        bucket = self._get_bucket(bucket_type)

        try:
            response = self.client.get_object(bucket, object_name)
            data = response.read()
            response.close()
            response.release_conn()
            return data
        except S3Error as e:
            raise Exception(f"Download failed: {e}")

    async def get_presigned_url(
        self,
        object_name: str,
        bucket_type: str = "assets",
        expires: timedelta = timedelta(hours=1),
    ) -> str:
        """Get presigned URL for direct access"""
        bucket = self._get_bucket(bucket_type)

        try:
            return self.client.presigned_get_object(
                bucket, object_name, expires=expires
            )
        except S3Error as e:
            raise Exception(f"Presigned URL failed: {e}")

    async def get_upload_url(
        self,
        object_name: str,
        bucket_type: str = "assets",
        expires: timedelta = timedelta(hours=1),
    ) -> str:
        """Get presigned URL for upload"""
        bucket = self._get_bucket(bucket_type)

        try:
            return self.client.presigned_put_object(
                bucket, object_name, expires=expires
            )
        except S3Error as e:
            raise Exception(f"Upload URL failed: {e}")

    async def delete_file(
        self,
        object_name: str,
        bucket_type: str = "assets",
    ) -> bool:
        """Delete file from storage"""
        bucket = self._get_bucket(bucket_type)

        try:
            self.client.remove_object(bucket, object_name)
            return True
        except S3Error as e:
            raise Exception(f"Delete failed: {e}")

    async def list_files(
        self,
        prefix: str = "",
        bucket_type: str = "assets",
        recursive: bool = True,
    ) -> List[Dict[str, Any]]:
        """List files in bucket"""
        bucket = self._get_bucket(bucket_type)

        try:
            objects = self.client.list_objects(
                bucket, prefix=prefix, recursive=recursive
            )
            return [
                {
                    "name": obj.object_name,
                    "size": obj.size,
                    "modified": obj.last_modified,
                    "etag": obj.etag,
                }
                for obj in objects
            ]
        except S3Error as e:
            raise Exception(f"List failed: {e}")

    async def file_exists(
        self,
        object_name: str,
        bucket_type: str = "assets",
    ) -> bool:
        """Check if file exists"""
        bucket = self._get_bucket(bucket_type)

        try:
            self.client.stat_object(bucket, object_name)
            return True
        except S3Error:
            return False

    async def copy_file(
        self,
        source_name: str,
        dest_name: str,
        source_bucket: str = "assets",
        dest_bucket: str = "assets",
    ) -> Dict[str, Any]:
        """Copy file within storage"""
        from minio.commonconfig import CopySource

        src_bucket = self._get_bucket(source_bucket)
        dst_bucket = self._get_bucket(dest_bucket)

        try:
            result = self.client.copy_object(
                dst_bucket,
                dest_name,
                CopySource(src_bucket, source_name),
            )
            return {
                "bucket": dst_bucket,
                "object_name": dest_name,
                "etag": result.etag,
            }
        except S3Error as e:
            raise Exception(f"Copy failed: {e}")

    def generate_object_name(
        self,
        project_id: str,
        asset_type: str,
        filename: str,
    ) -> str:
        """Generate structured object name"""
        ext = Path(filename).suffix
        hash_part = hashlib.md5(filename.encode()).hexdigest()[:8]
        return f"{project_id}/{asset_type}/{hash_part}{ext}"


# Singleton
storage_service = MinIOService()
