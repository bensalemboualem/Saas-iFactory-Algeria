"""
Utility helpers for the video platform
"""
import re
import hashlib
import secrets
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path
import mimetypes


def generate_id(prefix: str = "") -> str:
    """Generate a unique ID with optional prefix"""
    random_part = secrets.token_hex(8)
    if prefix:
        return f"{prefix}_{random_part}"
    return random_part


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug"""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text[:100]


def hash_content(content: bytes | str) -> str:
    """Generate MD5 hash of content"""
    if isinstance(content, str):
        content = content.encode()
    return hashlib.md5(content).hexdigest()


def format_duration(seconds: float) -> str:
    """Format seconds to HH:MM:SS"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def parse_duration(duration_str: str) -> float:
    """Parse HH:MM:SS or MM:SS to seconds"""
    parts = duration_str.split(":")
    if len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
    elif len(parts) == 2:
        return int(parts[0]) * 60 + float(parts[1])
    return float(duration_str)


def format_file_size(size_bytes: int) -> str:
    """Format bytes to human readable size"""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"


def get_mime_type(filename: str) -> str:
    """Get MIME type from filename"""
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type or "application/octet-stream"


def is_video_file(filename: str) -> bool:
    """Check if file is a video"""
    mime_type = get_mime_type(filename)
    return mime_type and mime_type.startswith("video/")


def is_audio_file(filename: str) -> bool:
    """Check if file is audio"""
    mime_type = get_mime_type(filename)
    return mime_type and mime_type.startswith("audio/")


def is_image_file(filename: str) -> bool:
    """Check if file is an image"""
    mime_type = get_mime_type(filename)
    return mime_type and mime_type.startswith("image/")


def sanitize_filename(filename: str) -> str:
    """Remove unsafe characters from filename"""
    filename = re.sub(r'[<>:"/\\|?*]', "", filename)
    filename = filename.strip(". ")
    return filename[:255]


def extract_hashtags(text: str) -> List[str]:
    """Extract hashtags from text"""
    return re.findall(r"#(\w+)", text)


def extract_mentions(text: str) -> List[str]:
    """Extract @mentions from text"""
    return re.findall(r"@(\w+)", text)


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to max length with suffix"""
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def split_text_for_tts(
    text: str, max_chars: int = 4000, split_on: List[str] = None
) -> List[str]:
    """Split text into chunks suitable for TTS APIs"""
    if len(text) <= max_chars:
        return [text]

    split_on = split_on or ["\n\n", "\n", ". ", "! ", "? ", ", ", " "]
    chunks = []
    current = text

    while len(current) > max_chars:
        split_point = max_chars

        for separator in split_on:
            last_sep = current[:max_chars].rfind(separator)
            if last_sep > max_chars // 2:
                split_point = last_sep + len(separator)
                break

        chunks.append(current[:split_point].strip())
        current = current[split_point:].strip()

    if current:
        chunks.append(current)

    return chunks


def calculate_video_duration(
    scenes: List[Dict[str, Any]], default_scene_duration: float = 5.0
) -> float:
    """Calculate total video duration from scenes"""
    total = 0
    for scene in scenes:
        total += scene.get("duration", default_scene_duration)
    return total


def estimate_credits(
    text_length: int,
    num_images: int,
    video_seconds: int,
    tts_provider: str = "elevenlabs",
    image_provider: str = "dalle",
    video_provider: str = "runway",
) -> Dict[str, int]:
    """Estimate credit usage for generation"""
    # Costs in credits (1 credit = $0.01)
    costs = {
        "tts": {
            "elevenlabs": int(text_length / 1000 * 3),  # ~$0.03 per 1000 chars
            "openai": int(text_length / 1000 * 1.5),  # ~$0.015 per 1000 chars
        },
        "image": {
            "dalle": num_images * 4,  # $0.04 per image
            "flux": num_images * 2,  # $0.02 per image
            "sdxl": num_images * 1,  # $0.01 per image
        },
        "video": {
            "runway": video_seconds * 5,  # $0.05 per second
            "luma": video_seconds * 4,  # $0.04 per second
            "replicate": video_seconds * 2,  # $0.02 per second
        },
    }

    return {
        "tts": costs["tts"].get(tts_provider, 2),
        "images": costs["image"].get(image_provider, 4) * num_images,
        "video": costs["video"].get(video_provider, 5) * video_seconds,
        "total": (
            costs["tts"].get(tts_provider, 2)
            + costs["image"].get(image_provider, 4) * num_images
            + costs["video"].get(video_provider, 5) * video_seconds
        ),
    }


def merge_dicts(base: Dict, override: Dict) -> Dict:
    """Deep merge two dictionaries"""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    return result


def safe_json_loads(data: str, default: Any = None) -> Any:
    """Safely parse JSON with default fallback"""
    import json

    try:
        return json.loads(data)
    except (json.JSONDecodeError, TypeError):
        return default


def get_aspect_ratio(width: int, height: int) -> str:
    """Get aspect ratio as string (16:9, 9:16, etc.)"""
    from math import gcd

    divisor = gcd(width, height)
    w = width // divisor
    h = height // divisor

    # Common ratios
    common = {
        (16, 9): "16:9",
        (9, 16): "9:16",
        (4, 3): "4:3",
        (3, 4): "3:4",
        (1, 1): "1:1",
        (21, 9): "21:9",
    }

    return common.get((w, h), f"{w}:{h}")


def get_platform_resolution(platform: str) -> tuple[int, int]:
    """Get recommended resolution for platform"""
    resolutions = {
        "youtube": (1920, 1080),
        "youtube_shorts": (1080, 1920),
        "tiktok": (1080, 1920),
        "instagram_reel": (1080, 1920),
        "instagram_feed": (1080, 1080),
        "instagram_story": (1080, 1920),
        "linkedin": (1920, 1080),
        "twitter": (1280, 720),
        "facebook": (1280, 720),
    }
    return resolutions.get(platform, (1920, 1080))


def schedule_optimal_time(
    platform: str, timezone: str = "UTC"
) -> datetime:
    """Get optimal posting time for platform"""
    # Best posting times (simplified)
    optimal_hours = {
        "youtube": 15,  # 3 PM
        "tiktok": 19,  # 7 PM
        "instagram": 11,  # 11 AM
        "linkedin": 10,  # 10 AM
        "twitter": 12,  # 12 PM
    }

    now = datetime.utcnow()
    target_hour = optimal_hours.get(platform, 12)

    if now.hour >= target_hour:
        target_date = now + timedelta(days=1)
    else:
        target_date = now

    return target_date.replace(
        hour=target_hour, minute=0, second=0, microsecond=0
    )
