"""
Social Publishing Service - Multi-platform video publishing
"""
from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
import httpx
from app.core.config import settings


@dataclass
class PublishResult:
    success: bool
    platform: str
    post_id: Optional[str] = None
    url: Optional[str] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = None


class BaseSocialProvider(ABC):
    """Base class for social media providers"""

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    async def publish_video(
        self,
        video_url: str,
        title: str,
        description: str,
        tags: List[str] = None,
        **kwargs
    ) -> PublishResult:
        pass

    @abstractmethod
    async def get_analytics(self, post_id: str) -> Dict[str, Any]:
        pass


class YouTubeProvider(BaseSocialProvider):
    """YouTube Data API v3"""

    @property
    def name(self) -> str:
        return "youtube"

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = "https://www.googleapis.com/youtube/v3"

    async def publish_video(
        self,
        video_url: str,
        title: str,
        description: str,
        tags: List[str] = None,
        privacy: str = "public",
        category_id: str = "22",  # People & Blogs
        **kwargs
    ) -> PublishResult:
        """Upload video to YouTube"""
        async with httpx.AsyncClient() as client:
            # Step 1: Initialize upload
            metadata = {
                "snippet": {
                    "title": title,
                    "description": description,
                    "tags": tags or [],
                    "categoryId": category_id,
                },
                "status": {
                    "privacyStatus": privacy,
                    "selfDeclaredMadeForKids": False,
                }
            }

            init_response = await client.post(
                f"{self.base_url}/videos?uploadType=resumable&part=snippet,status",
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json",
                },
                json=metadata,
            )

            if init_response.status_code != 200:
                return PublishResult(
                    success=False,
                    platform=self.name,
                    error=init_response.text,
                )

            upload_url = init_response.headers.get("Location")

            # Step 2: Download and upload video
            video_response = await client.get(video_url)
            video_bytes = video_response.content

            upload_response = await client.put(
                upload_url,
                headers={"Content-Type": "video/*"},
                content=video_bytes,
                timeout=600.0,
            )

            if upload_response.status_code in [200, 201]:
                data = upload_response.json()
                return PublishResult(
                    success=True,
                    platform=self.name,
                    post_id=data["id"],
                    url=f"https://youtube.com/watch?v={data['id']}",
                    metadata=data,
                )

            return PublishResult(
                success=False,
                platform=self.name,
                error=upload_response.text,
            )

    async def get_analytics(self, post_id: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/videos",
                params={
                    "id": post_id,
                    "part": "statistics,snippet",
                },
                headers={"Authorization": f"Bearer {self.access_token}"},
            )
            data = response.json()
            if data.get("items"):
                stats = data["items"][0]["statistics"]
                return {
                    "views": int(stats.get("viewCount", 0)),
                    "likes": int(stats.get("likeCount", 0)),
                    "comments": int(stats.get("commentCount", 0)),
                }
            return {}


class TikTokProvider(BaseSocialProvider):
    """TikTok Content Posting API"""

    @property
    def name(self) -> str:
        return "tiktok"

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = "https://open.tiktokapis.com/v2"

    async def publish_video(
        self,
        video_url: str,
        title: str,
        description: str,
        tags: List[str] = None,
        **kwargs
    ) -> PublishResult:
        async with httpx.AsyncClient() as client:
            # Initialize upload
            init_response = await client.post(
                f"{self.base_url}/post/publish/video/init/",
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json",
                },
                json={
                    "post_info": {
                        "title": title[:150],  # TikTok limit
                        "privacy_level": "PUBLIC_TO_EVERYONE",
                        "disable_duet": False,
                        "disable_stitch": False,
                        "disable_comment": False,
                    },
                    "source_info": {
                        "source": "PULL_FROM_URL",
                        "video_url": video_url,
                    }
                }
            )

            if init_response.status_code == 200:
                data = init_response.json()
                publish_id = data.get("data", {}).get("publish_id")
                return PublishResult(
                    success=True,
                    platform=self.name,
                    post_id=publish_id,
                    metadata=data,
                )

            return PublishResult(
                success=False,
                platform=self.name,
                error=init_response.text,
            )

    async def get_analytics(self, post_id: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/video/query/",
                headers={"Authorization": f"Bearer {self.access_token}"},
                params={"video_ids": post_id},
            )
            data = response.json()
            if data.get("data", {}).get("videos"):
                video = data["data"]["videos"][0]
                return {
                    "views": video.get("view_count", 0),
                    "likes": video.get("like_count", 0),
                    "comments": video.get("comment_count", 0),
                    "shares": video.get("share_count", 0),
                }
            return {}


class InstagramProvider(BaseSocialProvider):
    """Instagram Graph API for Reels"""

    @property
    def name(self) -> str:
        return "instagram"

    def __init__(self, access_token: str, ig_user_id: str):
        self.access_token = access_token
        self.ig_user_id = ig_user_id
        self.base_url = "https://graph.facebook.com/v18.0"

    async def publish_video(
        self,
        video_url: str,
        title: str,
        description: str,
        tags: List[str] = None,
        **kwargs
    ) -> PublishResult:
        caption = f"{title}\n\n{description}"
        if tags:
            caption += "\n\n" + " ".join([f"#{t}" for t in tags])

        async with httpx.AsyncClient() as client:
            # Step 1: Create media container
            container_response = await client.post(
                f"{self.base_url}/{self.ig_user_id}/media",
                data={
                    "media_type": "REELS",
                    "video_url": video_url,
                    "caption": caption[:2200],  # Instagram limit
                    "access_token": self.access_token,
                }
            )

            if container_response.status_code != 200:
                return PublishResult(
                    success=False,
                    platform=self.name,
                    error=container_response.text,
                )

            container_id = container_response.json().get("id")

            # Step 2: Publish
            publish_response = await client.post(
                f"{self.base_url}/{self.ig_user_id}/media_publish",
                data={
                    "creation_id": container_id,
                    "access_token": self.access_token,
                }
            )

            if publish_response.status_code == 200:
                media_id = publish_response.json().get("id")
                return PublishResult(
                    success=True,
                    platform=self.name,
                    post_id=media_id,
                    url=f"https://instagram.com/reel/{media_id}",
                )

            return PublishResult(
                success=False,
                platform=self.name,
                error=publish_response.text,
            )

    async def get_analytics(self, post_id: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/{post_id}/insights",
                params={
                    "metric": "plays,likes,comments,shares,saved",
                    "access_token": self.access_token,
                }
            )
            data = response.json()
            metrics = {m["name"]: m["values"][0]["value"] for m in data.get("data", [])}
            return {
                "views": metrics.get("plays", 0),
                "likes": metrics.get("likes", 0),
                "comments": metrics.get("comments", 0),
                "shares": metrics.get("shares", 0),
                "saves": metrics.get("saved", 0),
            }


class LinkedInProvider(BaseSocialProvider):
    """LinkedIn Video API"""

    @property
    def name(self) -> str:
        return "linkedin"

    def __init__(self, access_token: str, person_urn: str):
        self.access_token = access_token
        self.person_urn = person_urn
        self.base_url = "https://api.linkedin.com/v2"

    async def publish_video(
        self,
        video_url: str,
        title: str,
        description: str,
        tags: List[str] = None,
        **kwargs
    ) -> PublishResult:
        async with httpx.AsyncClient() as client:
            # Register upload
            register_response = await client.post(
                f"{self.base_url}/assets?action=registerUpload",
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json",
                },
                json={
                    "registerUploadRequest": {
                        "recipes": ["urn:li:digitalmediaRecipe:feedshare-video"],
                        "owner": self.person_urn,
                        "serviceRelationships": [{
                            "relationshipType": "OWNER",
                            "identifier": "urn:li:userGeneratedContent"
                        }]
                    }
                }
            )

            if register_response.status_code != 200:
                return PublishResult(
                    success=False,
                    platform=self.name,
                    error=register_response.text,
                )

            upload_data = register_response.json()
            asset_urn = upload_data["value"]["asset"]
            upload_url = upload_data["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]

            # Download and upload video
            video_response = await client.get(video_url)
            await client.put(
                upload_url,
                headers={"Authorization": f"Bearer {self.access_token}"},
                content=video_response.content,
            )

            # Create post
            text = f"{title}\n\n{description}"
            if tags:
                text += "\n\n" + " ".join([f"#{t}" for t in tags])

            post_response = await client.post(
                f"{self.base_url}/ugcPosts",
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json",
                },
                json={
                    "author": self.person_urn,
                    "lifecycleState": "PUBLISHED",
                    "specificContent": {
                        "com.linkedin.ugc.ShareContent": {
                            "shareCommentary": {"text": text},
                            "shareMediaCategory": "VIDEO",
                            "media": [{
                                "status": "READY",
                                "media": asset_urn,
                                "title": {"text": title},
                            }]
                        }
                    },
                    "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
                }
            )

            if post_response.status_code in [200, 201]:
                post_id = post_response.headers.get("x-restli-id")
                return PublishResult(
                    success=True,
                    platform=self.name,
                    post_id=post_id,
                )

            return PublishResult(
                success=False,
                platform=self.name,
                error=post_response.text,
            )

    async def get_analytics(self, post_id: str) -> Dict[str, Any]:
        # LinkedIn analytics require separate permissions
        return {}


class TwitterProvider(BaseSocialProvider):
    """Twitter/X API v2"""

    @property
    def name(self) -> str:
        return "twitter"

    def __init__(self, bearer_token: str, oauth_token: str, oauth_secret: str):
        self.bearer_token = bearer_token
        self.oauth_token = oauth_token
        self.oauth_secret = oauth_secret
        self.base_url = "https://api.twitter.com/2"
        self.upload_url = "https://upload.twitter.com/1.1"

    async def publish_video(
        self,
        video_url: str,
        title: str,
        description: str,
        tags: List[str] = None,
        **kwargs
    ) -> PublishResult:
        # Twitter video upload is complex with chunked uploads
        # This is a simplified version
        async with httpx.AsyncClient() as client:
            # Download video
            video_response = await client.get(video_url)
            video_bytes = video_response.content

            # Initialize upload
            init_response = await client.post(
                f"{self.upload_url}/media/upload.json",
                headers={"Authorization": f"Bearer {self.bearer_token}"},
                data={
                    "command": "INIT",
                    "media_type": "video/mp4",
                    "total_bytes": len(video_bytes),
                    "media_category": "tweet_video",
                }
            )

            media_id = init_response.json().get("media_id_string")

            # Append (simplified - real impl needs chunking)
            await client.post(
                f"{self.upload_url}/media/upload.json",
                headers={"Authorization": f"Bearer {self.bearer_token}"},
                data={"command": "APPEND", "media_id": media_id, "segment_index": 0},
                files={"media": video_bytes},
            )

            # Finalize
            await client.post(
                f"{self.upload_url}/media/upload.json",
                headers={"Authorization": f"Bearer {self.bearer_token}"},
                data={"command": "FINALIZE", "media_id": media_id},
            )

            # Create tweet
            text = f"{title}\n\n{description}"
            if tags:
                text += "\n\n" + " ".join([f"#{t}" for t in tags])

            tweet_response = await client.post(
                f"{self.base_url}/tweets",
                headers={
                    "Authorization": f"Bearer {self.bearer_token}",
                    "Content-Type": "application/json",
                },
                json={
                    "text": text[:280],
                    "media": {"media_ids": [media_id]},
                }
            )

            if tweet_response.status_code in [200, 201]:
                tweet_id = tweet_response.json()["data"]["id"]
                return PublishResult(
                    success=True,
                    platform=self.name,
                    post_id=tweet_id,
                    url=f"https://twitter.com/i/status/{tweet_id}",
                )

            return PublishResult(
                success=False,
                platform=self.name,
                error=tweet_response.text,
            )

    async def get_analytics(self, post_id: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/tweets/{post_id}",
                headers={"Authorization": f"Bearer {self.bearer_token}"},
                params={"tweet.fields": "public_metrics"},
            )
            data = response.json()
            metrics = data.get("data", {}).get("public_metrics", {})
            return {
                "views": metrics.get("impression_count", 0),
                "likes": metrics.get("like_count", 0),
                "comments": metrics.get("reply_count", 0),
                "retweets": metrics.get("retweet_count", 0),
            }


class SocialPublishingService:
    """Unified social media publishing service"""

    def __init__(self):
        self._providers: Dict[str, BaseSocialProvider] = {}

    def register_provider(self, provider: BaseSocialProvider):
        """Register a social media provider"""
        self._providers[provider.name] = provider

    def configure_youtube(self, access_token: str):
        self.register_provider(YouTubeProvider(access_token))

    def configure_tiktok(self, access_token: str):
        self.register_provider(TikTokProvider(access_token))

    def configure_instagram(self, access_token: str, ig_user_id: str):
        self.register_provider(InstagramProvider(access_token, ig_user_id))

    def configure_linkedin(self, access_token: str, person_urn: str):
        self.register_provider(LinkedInProvider(access_token, person_urn))

    def configure_twitter(
        self, bearer_token: str, oauth_token: str, oauth_secret: str
    ):
        self.register_provider(
            TwitterProvider(bearer_token, oauth_token, oauth_secret)
        )

    async def publish(
        self,
        platform: str,
        video_url: str,
        title: str,
        description: str,
        tags: List[str] = None,
        **kwargs
    ) -> PublishResult:
        """Publish to a single platform"""
        if platform not in self._providers:
            return PublishResult(
                success=False,
                platform=platform,
                error=f"Provider {platform} not configured",
            )

        return await self._providers[platform].publish_video(
            video_url, title, description, tags, **kwargs
        )

    async def publish_to_all(
        self,
        video_url: str,
        title: str,
        description: str,
        tags: List[str] = None,
        platforms: List[str] = None,
        **kwargs
    ) -> List[PublishResult]:
        """Publish to multiple platforms"""
        target_platforms = platforms or list(self._providers.keys())
        results = []

        for platform in target_platforms:
            if platform in self._providers:
                result = await self.publish(
                    platform, video_url, title, description, tags, **kwargs
                )
                results.append(result)

        return results

    async def get_analytics(
        self, platform: str, post_id: str
    ) -> Dict[str, Any]:
        """Get analytics for a published post"""
        if platform not in self._providers:
            return {"error": f"Provider {platform} not configured"}

        return await self._providers[platform].get_analytics(post_id)

    def available_platforms(self) -> List[str]:
        """List configured platforms"""
        return list(self._providers.keys())


# Singleton
social_service = SocialPublishingService()
