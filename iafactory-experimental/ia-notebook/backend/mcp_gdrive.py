"""
MCP Google Drive Connector for IA Notebook Pro
Enables file import from Google Drive, OneDrive, and local sources
"""

import os
import io
import json
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
import asyncio
import httpx

logger = logging.getLogger(__name__)


@dataclass
class DriveFile:
    """Represents a file from cloud storage"""
    id: str
    name: str
    mime_type: str
    size: int
    source: str  # 'gdrive', 'onedrive', 'local'
    path: Optional[str] = None
    download_url: Optional[str] = None
    created_at: Optional[str] = None
    modified_at: Optional[str] = None


class MCPDriveConnector:
    """
    Multi-cloud storage connector using MCP protocol
    Supports: Google Drive, OneDrive, Dropbox, Local files
    """

    # Supported file types for dashboard generation
    SUPPORTED_FORMATS = {
        # Documents
        "application/pdf": "pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
        "application/msword": "doc",
        "text/plain": "txt",
        "text/markdown": "md",

        # Spreadsheets (for dashboards)
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
        "application/vnd.ms-excel": "xls",
        "text/csv": "csv",
        "application/vnd.oasis.opendocument.spreadsheet": "ods",

        # Presentations
        "application/vnd.openxmlformats-officedocument.presentationml.presentation": "pptx",
        "application/vnd.ms-powerpoint": "ppt",

        # Data formats
        "application/json": "json",
        "application/xml": "xml",
        "text/xml": "xml",

        # Audio (for transcription)
        "audio/mpeg": "mp3",
        "audio/wav": "wav",
        "audio/webm": "webm",
        "audio/ogg": "ogg",

        # Images (for OCR)
        "image/png": "png",
        "image/jpeg": "jpg",
        "image/webp": "webp",
    }

    def __init__(self):
        self.gdrive_credentials = None
        self.onedrive_token = None
        self._connected_sources: Dict[str, bool] = {}

    async def connect_google_drive(self, credentials: Dict[str, Any]) -> bool:
        """
        Connect to Google Drive using OAuth2 credentials

        Args:
            credentials: OAuth2 credentials dict with access_token, refresh_token

        Returns:
            True if connected successfully
        """
        try:
            self.gdrive_credentials = credentials

            # Verify connection
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://www.googleapis.com/drive/v3/about",
                    params={"fields": "user"},
                    headers={"Authorization": f"Bearer {credentials.get('access_token')}"}
                )

                if response.status_code == 200:
                    self._connected_sources['gdrive'] = True
                    user = response.json().get('user', {})
                    logger.info(f"Google Drive connected: {user.get('displayName', 'Unknown')}")
                    return True

            return False

        except Exception as e:
            logger.error(f"Failed to connect Google Drive: {e}")
            return False

    async def list_gdrive_files(
        self,
        folder_id: str = "root",
        query: str = None,
        page_size: int = 50
    ) -> List[DriveFile]:
        """
        List files from Google Drive

        Args:
            folder_id: Folder ID to list (default: root)
            query: Optional search query
            page_size: Number of files to return

        Returns:
            List of DriveFile objects
        """
        if not self._connected_sources.get('gdrive'):
            raise ConnectionError("Google Drive not connected")

        files = []
        q = f"'{folder_id}' in parents and trashed = false"
        if query:
            q += f" and fullText contains '{query}'"

        # Add mime type filter for supported formats
        mime_types = list(self.SUPPORTED_FORMATS.keys())
        mime_filter = " or ".join([f"mimeType='{mt}'" for mt in mime_types])
        q += f" and ({mime_filter} or mimeType='application/vnd.google-apps.folder')"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://www.googleapis.com/drive/v3/files",
                    params={
                        "q": q,
                        "fields": "files(id,name,mimeType,size,createdTime,modifiedTime,webContentLink)",
                        "pageSize": page_size
                    },
                    headers={"Authorization": f"Bearer {self.gdrive_credentials.get('access_token')}"}
                )

                if response.status_code == 200:
                    data = response.json()
                    for item in data.get('files', []):
                        files.append(DriveFile(
                            id=item['id'],
                            name=item['name'],
                            mime_type=item.get('mimeType', 'application/octet-stream'),
                            size=int(item.get('size', 0)),
                            source='gdrive',
                            download_url=item.get('webContentLink'),
                            created_at=item.get('createdTime'),
                            modified_at=item.get('modifiedTime')
                        ))

        except Exception as e:
            logger.error(f"Failed to list Google Drive files: {e}")

        return files

    async def download_gdrive_file(self, file_id: str, save_path: str) -> str:
        """
        Download a file from Google Drive

        Args:
            file_id: Google Drive file ID
            save_path: Local path to save the file

        Returns:
            Path to downloaded file
        """
        if not self._connected_sources.get('gdrive'):
            raise ConnectionError("Google Drive not connected")

        try:
            async with httpx.AsyncClient() as client:
                # Get file metadata first
                meta_response = await client.get(
                    f"https://www.googleapis.com/drive/v3/files/{file_id}",
                    params={"fields": "name,mimeType"},
                    headers={"Authorization": f"Bearer {self.gdrive_credentials.get('access_token')}"}
                )

                if meta_response.status_code != 200:
                    raise Exception("Failed to get file metadata")

                metadata = meta_response.json()
                mime_type = metadata.get('mimeType', '')

                # Handle Google Docs export
                if mime_type.startswith('application/vnd.google-apps.'):
                    export_formats = {
                        'application/vnd.google-apps.document': 'application/pdf',
                        'application/vnd.google-apps.spreadsheet': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                        'application/vnd.google-apps.presentation': 'application/pdf'
                    }
                    export_mime = export_formats.get(mime_type, 'application/pdf')

                    response = await client.get(
                        f"https://www.googleapis.com/drive/v3/files/{file_id}/export",
                        params={"mimeType": export_mime},
                        headers={"Authorization": f"Bearer {self.gdrive_credentials.get('access_token')}"}
                    )
                else:
                    # Regular file download
                    response = await client.get(
                        f"https://www.googleapis.com/drive/v3/files/{file_id}",
                        params={"alt": "media"},
                        headers={"Authorization": f"Bearer {self.gdrive_credentials.get('access_token')}"}
                    )

                if response.status_code == 200:
                    os.makedirs(os.path.dirname(save_path), exist_ok=True)
                    with open(save_path, 'wb') as f:
                        f.write(response.content)
                    logger.info(f"Downloaded file to {save_path}")
                    return save_path
                else:
                    raise Exception(f"Download failed: {response.status_code}")

        except Exception as e:
            logger.error(f"Failed to download from Google Drive: {e}")
            raise

    async def connect_onedrive(self, access_token: str) -> bool:
        """Connect to OneDrive using OAuth2 token"""
        try:
            self.onedrive_token = access_token

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://graph.microsoft.com/v1.0/me/drive",
                    headers={"Authorization": f"Bearer {access_token}"}
                )

                if response.status_code == 200:
                    self._connected_sources['onedrive'] = True
                    logger.info("OneDrive connected")
                    return True

            return False

        except Exception as e:
            logger.error(f"Failed to connect OneDrive: {e}")
            return False

    async def list_onedrive_files(
        self,
        folder_path: str = "/",
        page_size: int = 50
    ) -> List[DriveFile]:
        """List files from OneDrive"""
        if not self._connected_sources.get('onedrive'):
            raise ConnectionError("OneDrive not connected")

        files = []

        try:
            endpoint = "https://graph.microsoft.com/v1.0/me/drive/root/children"
            if folder_path != "/":
                endpoint = f"https://graph.microsoft.com/v1.0/me/drive/root:{folder_path}:/children"

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    endpoint,
                    params={"$top": page_size},
                    headers={"Authorization": f"Bearer {self.onedrive_token}"}
                )

                if response.status_code == 200:
                    data = response.json()
                    for item in data.get('value', []):
                        if 'file' in item:  # Skip folders
                            mime_type = item.get('file', {}).get('mimeType', 'application/octet-stream')
                            if mime_type in self.SUPPORTED_FORMATS:
                                files.append(DriveFile(
                                    id=item['id'],
                                    name=item['name'],
                                    mime_type=mime_type,
                                    size=item.get('size', 0),
                                    source='onedrive',
                                    download_url=item.get('@microsoft.graph.downloadUrl'),
                                    created_at=item.get('createdDateTime'),
                                    modified_at=item.get('lastModifiedDateTime')
                                ))

        except Exception as e:
            logger.error(f"Failed to list OneDrive files: {e}")

        return files

    async def download_onedrive_file(self, file_id: str, save_path: str) -> str:
        """Download a file from OneDrive"""
        if not self._connected_sources.get('onedrive'):
            raise ConnectionError("OneDrive not connected")

        try:
            async with httpx.AsyncClient() as client:
                # Get download URL
                response = await client.get(
                    f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}",
                    headers={"Authorization": f"Bearer {self.onedrive_token}"}
                )

                if response.status_code == 200:
                    data = response.json()
                    download_url = data.get('@microsoft.graph.downloadUrl')

                    if download_url:
                        dl_response = await client.get(download_url)
                        if dl_response.status_code == 200:
                            os.makedirs(os.path.dirname(save_path), exist_ok=True)
                            with open(save_path, 'wb') as f:
                                f.write(dl_response.content)
                            return save_path

        except Exception as e:
            logger.error(f"Failed to download from OneDrive: {e}")
            raise

    def get_connected_sources(self) -> Dict[str, bool]:
        """Get status of connected sources"""
        return {
            "gdrive": self._connected_sources.get('gdrive', False),
            "onedrive": self._connected_sources.get('onedrive', False),
            "local": True  # Always available
        }

    def get_supported_formats(self) -> Dict[str, str]:
        """Get dictionary of supported MIME types and their extensions"""
        return self.SUPPORTED_FORMATS.copy()

    def is_format_supported(self, mime_type: str) -> bool:
        """Check if a MIME type is supported"""
        return mime_type in self.SUPPORTED_FORMATS


# Singleton instance
mcp_drive = MCPDriveConnector()
