"""
IA Factory - Content Adapter Service
Phase 3: Platform-specific content customization
"""

import asyncio
import logging
from typing import List, Dict, Any
from anthropic import Anthropic

from ..config import settings
from ..models.distribution import Platform, PLATFORM_SPECS

logger = logging.getLogger(__name__)


class ContentAdapter:
    """
    Phase 3: Customize content for each platform
    
    Uses Claude to adapt captions, generate hashtags,
    and optimize content for platform-specific audiences.
    """
    
    def __init__(self):
        self.client = Anthropic(api_key=settings.anthropic_api_key)
        self.model = settings.claude_model
        
        # Platform style guides
        self.platform_styles = {
            Platform.INSTAGRAM_REELS: {
                "description": "Emoji-heavy, conversational, engaging",
                "hashtag_count": 20,
                "tone": "Friendly, visual, trendy",
                "max_length": 2200,
                "tips": "Use line breaks, include CTA, mention in Stories"
            },
            Platform.TIKTOK: {
                "description": "Trending, youthful, authentic",
                "hashtag_count": 5,
                "tone": "Casual, fun, relatable",
                "max_length": 2200,
                "tips": "Reference trends, use trending sounds, engage comments"
            },
            Platform.YOUTUBE_SHORTS: {
                "description": "Educational, SEO-focused",
                "hashtag_count": 10,
                "tone": "Informative, clear, value-driven",
                "max_length": 5000,
                "tips": "Include keywords, link to full video, ask to subscribe"
            },
            Platform.LINKEDIN: {
                "description": "Professional, insightful, industry-focused",
                "hashtag_count": 5,
                "tone": "Professional, thought-leadership",
                "max_length": 3000,
                "tips": "Share insights, ask questions, tag companies"
            },
            Platform.FACEBOOK_REELS: {
                "description": "Community-focused, shareable",
                "hashtag_count": 10,
                "tone": "Friendly, inclusive, engaging",
                "max_length": 2200,
                "tips": "Encourage shares, tag friends prompt"
            },
            Platform.TWITTER: {
                "description": "Concise, witty, timely",
                "hashtag_count": 3,
                "tone": "Sharp, engaging, conversation-starter",
                "max_length": 280,
                "tips": "Thread if needed, engage replies"
            }
        }
    
    async def adapt_caption(
        self,
        original: str,
        platform: Platform,
        brand_guidelines: Dict[str, Any],
        language: str = "en"
    ) -> str:
        """
        Customize caption for a specific platform
        
        Args:
            original: Original caption text
            platform: Target platform
            brand_guidelines: Brand voice guidelines
            language: Content language
        
        Returns:
            Platform-adapted caption
        """
        
        style = self.platform_styles.get(platform, {})
        spec = PLATFORM_SPECS.get(platform)
        max_length = spec.max_caption_length if spec else 2200
        
        language_instruction = {
            "en": "in English",
            "fr": "en français",
            "ar": "بالعربية"
        }.get(language, "in English")
        
        prompt = f"""
Adapt this caption for {platform.value} {language_instruction}:

Original Caption:
"{original}"

Platform Style: {style.get('description', 'Engaging and relevant')}
Tone: {style.get('tone', 'Professional')}
Max Length: {max_length} characters
Tips: {style.get('tips', '')}

Brand Voice: {brand_guidelines.get('tone', 'professional')}
Brand Values: {', '.join(brand_guidelines.get('key_values', []))}

Requirements:
- Adapt tone and style for {platform.value}
- Keep the core message
- Add relevant emojis if appropriate
- Include a CTA
- Stay under {max_length} characters

Return ONLY the adapted caption text (no explanation, no hashtags).
"""
        
        try:
            response = await asyncio.to_thread(
                self.client.messages.create,
                model=self.model,
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            caption = response.content[0].text.strip()
            
            # Ensure within length limit
            if len(caption) > max_length:
                caption = caption[:max_length-3] + "..."
            
            return caption
            
        except Exception as e:
            logger.error(f"Caption adaptation failed: {e}")
            # Return truncated original
            return original[:max_length-3] + "..." if len(original) > max_length else original
    
    async def generate_hashtags(
        self,
        content: str,
        platform: Platform,
        niche: str,
        language: str = "en"
    ) -> List[str]:
        """
        Generate platform-optimized hashtags
        
        Args:
            content: Content description/caption
            platform: Target platform
            niche: Industry/niche
            language: Content language
        
        Returns:
            List of relevant hashtags
        """
        
        style = self.platform_styles.get(platform, {})
        count = style.get('hashtag_count', 10)
        
        # Platform-specific hashtag strategies
        strategies = {
            Platform.INSTAGRAM_REELS: "Mix of popular (1M+), medium (100K-1M), and niche (<100K) hashtags",
            Platform.TIKTOK: "Focus on trending hashtags and niche-specific tags",
            Platform.YOUTUBE_SHORTS: "SEO-focused hashtags that match search intent",
            Platform.LINKEDIN: "Industry-specific and professional hashtags",
            Platform.TWITTER: "Trending topics and conversation hashtags"
        }
        
        prompt = f"""
Generate {count} relevant hashtags for {platform.value}:

Content: {content}
Niche: {niche}
Language: {language}

Strategy: {strategies.get(platform, 'Mix of popular and niche hashtags')}

Requirements:
- Each hashtag should start with #
- Mix of reach levels (some popular, some niche)
- Relevant to the content
- No spaces in hashtags

Return ONLY hashtags (one per line, starting with #).
"""
        
        try:
            response = await asyncio.to_thread(
                self.client.messages.create,
                model=self.model,
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )
            
            text = response.content[0].text.strip()
            
            # Parse hashtags
            hashtags = []
            for line in text.split('\n'):
                line = line.strip()
                if line.startswith('#'):
                    # Clean hashtag
                    tag = line.split()[0]  # Take first word only
                    tag = ''.join(c for c in tag if c.isalnum() or c == '#')
                    if tag and tag != '#':
                        hashtags.append(tag)
            
            return hashtags[:count]
            
        except Exception as e:
            logger.error(f"Hashtag generation failed: {e}")
            return []
    
    async def adapt_for_all_platforms(
        self,
        original_caption: str,
        original_hashtags: List[str],
        platforms: List[Platform],
        brand_guidelines: Dict[str, Any],
        niche: str,
        language: str = "en"
    ) -> Dict[str, Dict[str, Any]]:
        """
        Adapt content for multiple platforms
        
        Args:
            original_caption: Original caption
            original_hashtags: Original hashtags
            platforms: Target platforms
            brand_guidelines: Brand guidelines
            niche: Industry niche
            language: Content language
        
        Returns:
            Dictionary mapping platform to adapted content
        """
        
        results = {}
        
        for platform in platforms:
            try:
                # Adapt caption
                adapted_caption = await self.adapt_caption(
                    original=original_caption,
                    platform=platform,
                    brand_guidelines=brand_guidelines,
                    language=language
                )
                
                # Generate platform-specific hashtags
                hashtags = await self.generate_hashtags(
                    content=original_caption,
                    platform=platform,
                    niche=niche,
                    language=language
                )
                
                # Get platform spec for validation
                spec = PLATFORM_SPECS.get(platform)
                
                results[platform.value] = {
                    "caption": adapted_caption,
                    "hashtags": hashtags[:spec.max_hashtags if spec else 10],
                    "full_post": f"{adapted_caption}\n\n{' '.join(hashtags)}",
                    "character_count": len(adapted_caption),
                    "hashtag_count": len(hashtags),
                    "platform_style": self.platform_styles.get(platform, {}).get('description', '')
                }
                
            except Exception as e:
                logger.error(f"Adaptation failed for {platform}: {e}")
                results[platform.value] = {
                    "caption": original_caption,
                    "hashtags": original_hashtags,
                    "error": str(e)
                }
        
        return results
    
    async def generate_platform_cta(
        self,
        platform: Platform,
        action: str = "follow",
        brand_name: str = "",
        language: str = "en"
    ) -> str:
        """
        Generate platform-specific call-to-action
        
        Args:
            platform: Target platform
            action: Desired action (follow, like, share, comment, etc.)
            brand_name: Brand name to mention
            language: Content language
        
        Returns:
            Platform-optimized CTA
        """
        
        # Pre-defined CTAs by platform and action
        ctas = {
            Platform.INSTAGRAM_REELS: {
                "follow": f"Follow @{brand_name} for more! 🔔",
                "like": "Double tap if you agree! ❤️",
                "share": "Share this with someone who needs it! 📤",
                "comment": "Drop a 🔥 in comments!",
                "save": "Save this for later! 🔖"
            },
            Platform.TIKTOK: {
                "follow": f"Follow for Part 2! 🎬",
                "like": "Like if this helped! 💖",
                "share": "Send to a friend! 📱",
                "comment": "Comment your thoughts! 💬",
                "duet": "Duet this with your reaction! 🎤"
            },
            Platform.YOUTUBE_SHORTS: {
                "follow": "Subscribe for more shorts! 🔔",
                "like": "👍 Like if helpful!",
                "share": "Share with your network!",
                "comment": "Questions? Ask below! 💬"
            },
            Platform.LINKEDIN: {
                "follow": f"Follow {brand_name} for insights",
                "like": "👍 if you found this valuable",
                "share": "Repost to share with your network",
                "comment": "What's your take? Share below"
            }
        }
        
        platform_ctas = ctas.get(platform, {})
        return platform_ctas.get(action, f"Follow {brand_name}!")
