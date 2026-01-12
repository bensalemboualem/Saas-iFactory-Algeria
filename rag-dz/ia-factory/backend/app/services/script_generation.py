"""
IA Factory - Script Generation Service
Phase 2: AI-powered script generation using Claude
"""

from anthropic import Anthropic
from typing import List, Dict, Any, Optional
import asyncio
import json
import logging

from ..config import settings

logger = logging.getLogger(__name__)


class ScriptGenerator:
    """
    Phase 2: Script Generation Engine
    
    Generates video scripts using Claude AI, expanding a single topic
    into multiple variations and creating optimized scripts for each.
    """
    
    def __init__(self):
        self.client = Anthropic(api_key=settings.anthropic_api_key)
        self.model = settings.claude_model
    
    async def expand_topic(
        self,
        core_topic: str,
        niche: str,
        num_variations: int = 30,
        language: str = "en"
    ) -> List[str]:
        """
        Generate multiple variations from a single core topic
        
        Args:
            core_topic: The main topic to expand
            niche: The industry/niche for context
            num_variations: Number of unique angles to generate
            language: Content language (en, fr, ar)
        
        Returns:
            List of topic variations/angles
        """
        
        language_context = {
            "en": "in English",
            "fr": "en français",
            "ar": "بالعربية (with transliteration)"
        }.get(language, "in English")
        
        prompt = f"""
You are an expert content strategist for {niche}.

Core Topic: {core_topic}

Generate {num_variations} UNIQUE angles/variations of this topic for 15-second reels {language_context}.

Each variation should be:
- Distinct and engaging
- Suitable for short-form video
- Specific enough to write a script from
- Brand-appropriate for a professional audience

Format each as a numbered list (1. 2. 3. etc).

Focus on diverse angles:
- Storytelling angles (personal stories, case studies)
- Educational/how-to angles (tutorials, tips)
- Entertainment angles (humor, surprises)
- Inspiration/motivation angles (success stories)
- Community/relatable angles (common struggles)
- Contrarian/myth-busting angles
- Behind-the-scenes angles
- Trend commentary angles

Make each variation specific and actionable, not generic.
"""
        
        try:
            response = await asyncio.to_thread(
                self.client.messages.create,
                model=self.model,
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}]
            )
            
            text = response.content[0].text
            
            # Parse numbered variations
            variations = []
            for line in text.split('\n'):
                line = line.strip()
                if line and '. ' in line[:4]:  # Check for numbered list
                    # Extract content after the number
                    parts = line.split('. ', 1)
                    if len(parts) > 1:
                        variations.append(parts[1].strip())
            
            logger.info(f"Generated {len(variations)} topic variations")
            return variations[:num_variations]
            
        except Exception as e:
            logger.error(f"Topic expansion failed: {e}")
            raise
    
    async def generate_script(
        self,
        topic: str,
        brand_guidelines: Dict[str, Any],
        duration: int = 15,
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Generate an optimized video script for a topic
        
        Args:
            topic: The topic/angle to create a script for
            brand_guidelines: Brand voice and guidelines
            duration: Target video duration in seconds
            language: Script language
        
        Returns:
            Script dictionary with hook, body, CTA, and suggestions
        """
        
        tone = brand_guidelines.get('tone', 'energetic')
        target_audience = brand_guidelines.get('target_audience', 'general audience')
        brand_name = brand_guidelines.get('brand_name', 'IA Factory')
        key_values = brand_guidelines.get('key_values', [])
        
        language_instruction = {
            "en": "Write in English",
            "fr": "Écris en français",
            "ar": "اكتب بالعربية مع النطق اللاتيني"
        }.get(language, "Write in English")
        
        prompt = f"""
Generate a compelling {duration}-second reel script for:
"{topic}"

{language_instruction}

Brand Context:
- Brand: {brand_name}
- Tone: {tone}
- Target Audience: {target_audience}
- Values: {', '.join(key_values) if key_values else 'Quality, Innovation'}

Script MUST have:
1. Hook (first 2 seconds) - GRAB attention immediately, create curiosity
2. Body (main message) - Deliver value, keep it punchy
3. CTA (call-to-action) - Tell them what to do next

Requirements:
- Hook must be attention-grabbing (pattern interrupt, question, bold statement)
- Keep sentences SHORT and punchy
- Use conversational language
- Include specific numbers or examples where relevant
- End with a clear CTA

Return ONLY valid JSON (no markdown, no explanation):
{{
    "topic": "{topic}",
    "hook": "Your hook text here (2 seconds)",
    "body": "Your main message here (10-11 seconds)",
    "cta": "Your call-to-action here (2-3 seconds)",
    "full_script": "Complete script for narration",
    "timing": {{
        "hook": "0-2s",
        "body": "2-{duration-3}s",
        "cta": "{duration-3}-{duration}s"
    }},
    "suggested_music_mood": "upbeat/dramatic/chill/inspirational",
    "suggested_visuals": ["visual 1", "visual 2", "visual 3"],
    "text_overlays": [
        {{"text": "Key text 1", "time_start": 0, "time_end": 2}},
        {{"text": "Key text 2", "time_start": 3, "time_end": 7}}
    ],
    "hashtag_suggestions": ["#hashtag1", "#hashtag2"]
}}
"""
        
        try:
            response = await asyncio.to_thread(
                self.client.messages.create,
                model=self.model,
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}]
            )
            
            text = response.content[0].text
            
            # Extract JSON from response
            json_start = text.find('{')
            json_end = text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                script_data = json.loads(text[json_start:json_end])
                script_data['language'] = language
                script_data['duration'] = duration
                return script_data
            else:
                raise ValueError("No valid JSON found in response")
                
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing failed: {e}")
            # Return a basic structure if parsing fails
            return {
                "topic": topic,
                "hook": "Generated hook",
                "body": "Generated body",
                "cta": "Follow for more!",
                "timing": {"hook": "0-2s", "body": f"2-{duration-3}s", "cta": f"{duration-3}-{duration}s"},
                "suggested_music_mood": "upbeat",
                "suggested_visuals": [],
                "text_overlays": [],
                "language": language,
                "duration": duration,
                "error": str(e)
            }
        except Exception as e:
            logger.error(f"Script generation failed: {e}")
            raise
    
    async def generate_bulk_scripts(
        self,
        brand_guidelines: Dict[str, Any],
        num_scripts: int = 30,
        duration: int = 15,
        batch_size: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Phase 2: Generate multiple scripts from a single topic
        
        This is the main entry point for bulk content generation.
        Takes the featured topic and generates multiple variations with scripts.
        
        Args:
            brand_guidelines: Complete brand guidelines including featured_topic
            num_scripts: Number of scripts to generate (default 30)
            duration: Target video duration
            batch_size: Scripts to generate in parallel
        
        Returns:
            List of script dictionaries
        """
        
        core_topic = brand_guidelines.get('featured_topic')
        if not core_topic:
            raise ValueError("No featured_topic set in brand guidelines")
        
        niche = brand_guidelines.get('niche', 'Technology')
        language = brand_guidelines.get('language', 'en')
        
        logger.info(f"🚀 Starting bulk script generation: {num_scripts} scripts from '{core_topic}'")
        
        # Step 1: Expand topic to variations
        logger.info(f"📝 Expanding topic to {num_scripts} variations...")
        variations = await self.expand_topic(
            core_topic=core_topic,
            niche=niche,
            num_variations=num_scripts,
            language=language
        )
        
        if len(variations) < num_scripts:
            logger.warning(f"Only got {len(variations)} variations, expected {num_scripts}")
        
        # Step 2: Generate scripts in batches
        logger.info(f"🎬 Generating {len(variations)} scripts in batches of {batch_size}...")
        
        all_scripts = []
        
        for i in range(0, len(variations), batch_size):
            batch = variations[i:i+batch_size]
            batch_num = i // batch_size + 1
            total_batches = (len(variations) - 1) // batch_size + 1
            
            logger.info(f"Batch {batch_num}/{total_batches}: Generating {len(batch)} scripts...")
            
            # Generate batch in parallel
            batch_tasks = [
                self.generate_script(
                    topic=variation,
                    brand_guidelines=brand_guidelines,
                    duration=duration,
                    language=language
                )
                for variation in batch
            ]
            
            batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
            
            for idx, result in enumerate(batch_results):
                if isinstance(result, Exception):
                    logger.error(f"Script generation failed for variation {i+idx}: {result}")
                    # Add placeholder for failed script
                    all_scripts.append({
                        "topic": batch[idx],
                        "error": str(result),
                        "status": "failed"
                    })
                else:
                    result['variation_index'] = i + idx
                    all_scripts.append(result)
            
            # Small delay between batches to avoid rate limiting
            if i + batch_size < len(variations):
                await asyncio.sleep(1)
        
        successful = len([s for s in all_scripts if 'error' not in s])
        logger.info(f"✅ Generated {successful}/{num_scripts} scripts successfully")
        
        return all_scripts
    
    async def improve_script(
        self,
        script: Dict[str, Any],
        feedback: str,
        brand_guidelines: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Improve an existing script based on feedback
        
        Args:
            script: Original script to improve
            feedback: User feedback or improvement request
            brand_guidelines: Brand guidelines for context
        
        Returns:
            Improved script dictionary
        """
        
        prompt = f"""
Improve this video script based on the feedback:

Original Script:
- Hook: {script.get('hook', '')}
- Body: {script.get('body', '')}
- CTA: {script.get('cta', '')}

Feedback: {feedback}

Brand Tone: {brand_guidelines.get('tone', 'energetic')}
Target Audience: {brand_guidelines.get('target_audience', 'general audience')}

Return the improved script as JSON with the same structure.
Keep the same general topic but apply the feedback.
"""
        
        response = await asyncio.to_thread(
            self.client.messages.create,
            model=self.model,
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )
        
        text = response.content[0].text
        json_start = text.find('{')
        json_end = text.rfind('}') + 1
        
        if json_start >= 0:
            improved = json.loads(text[json_start:json_end])
            improved['original_topic'] = script.get('topic')
            improved['improved'] = True
            return improved
        
        return script  # Return original if parsing fails
