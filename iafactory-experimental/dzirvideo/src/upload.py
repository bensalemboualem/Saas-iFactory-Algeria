"""
DzirVideo - YouTube Upload Module
Uploads videos to YouTube using the official YouTube Data API v3
"""

import os
import logging
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)


class YouTubeUploader:
    """Upload videos to YouTube using official API"""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        refresh_token: str
    ):
        """
        Initialize YouTube uploader

        Args:
            client_id: OAuth client ID from Google Cloud Console
            client_secret: OAuth client secret
            refresh_token: OAuth refresh token
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.youtube = None

    def authenticate(self):
        """Authenticate with YouTube API using refresh token"""
        logger.info("Authenticating with YouTube API...")

        credentials = Credentials(
            token=None,
            refresh_token=self.refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=self.client_id,
            client_secret=self.client_secret
        )

        self.youtube = build('youtube', 'v3', credentials=credentials)
        logger.info("YouTube API authenticated successfully")

    def upload_video(
        self,
        video_path: str | Path,
        title: str,
        description: str = "",
        tags: list[str] | None = None,
        category_id: str = "22",  # People & Blogs
        privacy_status: str = "public",
        made_for_kids: bool = False
    ) -> dict:
        """
        Upload video to YouTube

        Args:
            video_path: Path to video file
            title: Video title (max 100 characters)
            description: Video description (max 5000 characters)
            tags: List of tags (max 500 characters total)
            category_id: YouTube category ID (default: 22 = People & Blogs)
            privacy_status: "public", "private", or "unlisted"
            made_for_kids: Whether video is made for kids (COPPA compliance)

        Returns:
            dict: Video metadata including video_id and URL
        """
        if not self.youtube:
            self.authenticate()

        video_path = Path(video_path)
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")

        logger.info(f"Uploading video: {video_path.name}")
        logger.info(f"Title: {title}")

        # Prepare metadata
        body = {
            'snippet': {
                'title': title[:100],  # Max 100 chars
                'description': description[:5000],  # Max 5000 chars
                'tags': tags or [],
                'categoryId': category_id
            },
            'status': {
                'privacyStatus': privacy_status,
                'selfDeclaredMadeForKids': made_for_kids,
                'madeForKids': made_for_kids
            }
        }

        # Add #Shorts to description if not present
        if '#Shorts' not in body['snippet']['description']:
            body['snippet']['description'] += '\n\n#Shorts'

        # Create media upload
        media = MediaFileUpload(
            str(video_path),
            mimetype='video/mp4',
            resumable=True,
            chunksize=1024 * 1024  # 1MB chunks
        )

        try:
            # Upload video
            request = self.youtube.videos().insert(
                part='snippet,status',
                body=body,
                media_body=media
            )

            response = None
            logger.info("Upload in progress...")

            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    logger.info(f"Upload progress: {progress}%")

            video_id = response['id']
            video_url = f"https://www.youtube.com/watch?v={video_id}"

            logger.info(f"Upload successful!")
            logger.info(f"Video ID: {video_id}")
            logger.info(f"Video URL: {video_url}")

            return {
                'success': True,
                'video_id': video_id,
                'url': video_url,
                'title': title,
                'response': response
            }

        except HttpError as e:
            logger.error(f"YouTube API error: {e}")
            return {
                'success': False,
                'error': str(e),
                'video_id': None,
                'url': None
            }

    def get_video_info(self, video_id: str) -> dict:
        """
        Get video information

        Args:
            video_id: YouTube video ID

        Returns:
            dict: Video metadata
        """
        if not self.youtube:
            self.authenticate()

        try:
            request = self.youtube.videos().list(
                part='snippet,statistics,status',
                id=video_id
            )
            response = request.execute()

            if response['items']:
                return response['items'][0]
            else:
                return {'error': 'Video not found'}

        except HttpError as e:
            logger.error(f"Error fetching video info: {e}")
            return {'error': str(e)}


# Helper function to get OAuth refresh token (run once)
def get_refresh_token_interactive():
    """
    Interactive helper to get refresh token (run once manually)

    Instructions:
    1. Go to https://console.cloud.google.com/
    2. Create OAuth 2.0 credentials
    3. Download client_secret.json
    4. Run this function
    """
    from google_auth_oauthlib.flow import InstalledAppFlow

    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secret.json',  # Download from Google Cloud Console
        SCOPES
    )

    credentials = flow.run_local_server(port=8080)

    print("\n=== Save these credentials in your .env ===")
    print(f"YOUTUBE_CLIENT_ID={credentials.client_id}")
    print(f"YOUTUBE_CLIENT_SECRET={credentials.client_secret}")
    print(f"YOUTUBE_REFRESH_TOKEN={credentials.refresh_token}")
    print("==========================================\n")


if __name__ == "__main__":
    # Test upload (requires valid credentials in .env)
    logging.basicConfig(level=logging.INFO)

    from dotenv import load_dotenv
    load_dotenv()

    uploader = YouTubeUploader(
        client_id=os.getenv('YOUTUBE_CLIENT_ID'),
        client_secret=os.getenv('YOUTUBE_CLIENT_SECRET'),
        refresh_token=os.getenv('YOUTUBE_REFRESH_TOKEN')
    )

    # Example: upload test video
    # result = uploader.upload_video(
    #     video_path="./output/videos/test.mp4",
    #     title="Test YouTube Short",
    #     description="Test video generated automatically",
    #     tags=["shorts", "test"],
    #     privacy_status="private"
    # )
    # print(result)
