"""
OpenAI Service
Handles: Translation, Text Generation, Speech-to-Text, Image Generation
"""
import logging
from typing import Optional, List, BinaryIO
from openai import AsyncOpenAI
from app.core.config import settings
from app.models.requests import (
    TranslateRequest,
    TextGenerationRequest,
    ImageGenerationRequest,
    LanguageCode
)
from app.models.responses import (
    TranslateResponse,
    TextGenerationResponse,
    SpeechToTextResponse,
    ImageGenerationResponse
)

logger = logging.getLogger(__name__)


class OpenAIService:
    """OpenAI API service"""
    
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY,
            organization=settings.OPENAI_ORG_ID if settings.OPENAI_ORG_ID else None
        )
    
    # ===================================
    # Translation
    # ===================================
    
    async def translate(self, request: TranslateRequest) -> TranslateResponse:
        """
        Translate text using GPT-4o-mini
        Supporte FR, AR, EN et autres langues
        """
        try:
            # Construire le prompt de traduction
            system_prompt = self._build_translation_system_prompt(
                request.source_language,
                request.target_language,
                request.preserve_formatting
            )
            
            response = await self.client.chat.completions.create(
                model=settings.DEFAULT_TRANSLATION_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": request.text}
                ],
                temperature=0.3,  # Low temperature for accurate translation
                max_tokens=len(request.text.split()) * 3  # Approximation
            )
            
            translated_text = response.choices[0].message.content.strip()
            
            return TranslateResponse(
                translated_text=translated_text,
                source_language=request.source_language.value,
                target_language=request.target_language.value,
                character_count=len(translated_text),
                provider="openai"
            )
        
        except Exception as e:
            logger.error(f"OpenAI translation error: {str(e)}")
            raise
    
    def _build_translation_system_prompt(
        self,
        source: LanguageCode,
        target: LanguageCode,
        preserve_formatting: bool
    ) -> str:
        """Build translation system prompt"""
        
        language_names = {
            LanguageCode.FRENCH: "français",
            LanguageCode.ARABIC: "arabe",
            LanguageCode.ENGLISH: "anglais",
            LanguageCode.SPANISH: "espagnol",
            LanguageCode.GERMAN: "allemand",
            LanguageCode.ITALIAN: "italien"
        }
        
        prompt = f"Tu es un traducteur professionnel expert. "
        prompt += f"Traduis le texte suivant de {language_names[source]} vers {language_names[target]}. "
        
        if preserve_formatting:
            prompt += "Préserve exactement la mise en forme, les sauts de ligne et la ponctuation. "
        
        if target == LanguageCode.ARABIC:
            prompt += "Assure-toi que l'arabe est correctement vocalisé si nécessaire. "
        
        prompt += "Ne fournis QUE la traduction, sans commentaire ni explication."
        
        return prompt
    
    async def batch_translate(
        self,
        texts: List[str],
        source_language: LanguageCode,
        target_language: LanguageCode
    ) -> List[TranslateResponse]:
        """Batch translation"""
        import asyncio
        
        tasks = [
            self.translate(TranslateRequest(
                text=text,
                source_language=source_language,
                target_language=target_language
            ))
            for text in texts
        ]
        
        return await asyncio.gather(*tasks)
    
    # ===================================
    # Text Generation
    # ===================================
    
    async def generate_text(self, request: TextGenerationRequest) -> TextGenerationResponse:
        """Generate text using GPT models"""
        try:
            model = request.model or settings.DEFAULT_TEXT_MODEL
            
            system_prompt = self._build_generation_system_prompt(
                request.language,
                request.style
            )
            
            response = await self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": request.prompt}
                ],
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )
            
            generated_text = response.choices[0].message.content.strip()
            
            return TextGenerationResponse(
                generated_text=generated_text,
                prompt=request.prompt,
                language=request.language.value,
                model=model,
                tokens_used=response.usage.total_tokens,
                finish_reason=response.choices[0].finish_reason
            )
        
        except Exception as e:
            logger.error(f"OpenAI text generation error: {str(e)}")
            raise
    
    def _build_generation_system_prompt(self, language: LanguageCode, style: str) -> str:
        """Build text generation system prompt"""
        
        language_instructions = {
            LanguageCode.FRENCH: "Rédige en français.",
            LanguageCode.ARABIC: "اكتب باللغة العربية.",
            LanguageCode.ENGLISH: "Write in English.",
        }
        
        style_instructions = {
            "professional": "Adopte un ton professionnel et formel.",
            "casual": "Adopte un ton décontracté et amical.",
            "creative": "Sois créatif et original.",
            "technical": "Utilise un langage technique précis.",
            "marketing": "Rédige un contenu marketing convaincant."
        }
        
        return f"{language_instructions.get(language, 'Write in the specified language.')} {style_instructions.get(style, '')}"
    
    # ===================================
    # Speech to Text
    # ===================================
    
    async def transcribe_audio(
        self,
        audio_file: BinaryIO,
        language: Optional[LanguageCode] = None
    ) -> SpeechToTextResponse:
        """Transcribe audio using Whisper"""
        try:
            transcription = await self.client.audio.transcriptions.create(
                model=settings.WHISPER_MODEL,
                file=audio_file,
                language=language.value if language else None,
                response_format="verbose_json"  # Includes duration
            )
            
            return SpeechToTextResponse(
                text=transcription.text,
                language=transcription.language,
                duration_seconds=transcription.duration,
                provider="openai"
            )
        
        except Exception as e:
            logger.error(f"OpenAI transcription error: {str(e)}")
            raise
    
    # ===================================
    # Image Generation
    # ===================================
    
    async def generate_image(self, request: ImageGenerationRequest) -> ImageGenerationResponse:
        """Generate image using DALL-E"""
        try:
            model = request.model or settings.DEFAULT_IMAGE_MODEL
            
            response = await self.client.images.generate(
                model=model,
                prompt=request.prompt,
                size=request.size.value,
                style=request.style,
                quality=request.quality,
                n=1
            )
            
            image_data = response.data[0]
            
            return ImageGenerationResponse(
                image_url=image_data.url,
                prompt=request.prompt,
                revised_prompt=image_data.revised_prompt if hasattr(image_data, 'revised_prompt') else None,
                size=request.size.value,
                model=model
            )
        
        except Exception as e:
            logger.error(f"OpenAI image generation error: {str(e)}")
            raise
    
    # ===================================
    # Health Check
    # ===================================
    
    async def health_check(self) -> bool:
        """Check OpenAI API connectivity"""
        try:
            await self.client.models.list()
            return True
        except Exception as e:
            logger.error(f"OpenAI health check failed: {str(e)}")
            return False
